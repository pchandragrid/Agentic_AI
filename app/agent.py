"""
Nexus AI Engine — ADK-based Autonomous Research Agent.

This module defines the core agent architecture using Google's Agent Development Kit (ADK).

Architecture:
    root_agent (LoopAgent)
    ├── researcher_agent (LlmAgent) — has tools: [document_search, web_search, financial_data, news_agent, canvas]
    └── critic_agent (LlmAgent) — has tools: [exit_loop]
"""

import asyncio
import os

from dotenv import load_dotenv

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.tools.document_search import document_search_tool
from app.tools.web_search import web_search_tool
from app.tools.financial_tool import financial_data_tool
from app.tools.news_agent_tool import news_agent_tool
from app.tools.canvas_tool import canvas_tool

# Load environment variables for ADK (GOOGLE_GENAI_USE_VERTEXAI, etc.)
load_dotenv()


# --- Exit Loop Tool ---

def exit_loop() -> dict:
    """Signal that the research is complete and no further iterations are needed.

    Call this tool ONLY when the research answer is comprehensive, accurate,
    well-supported by evidence, and fully addresses the original question.
    Do NOT call this if there are gaps, missing information, or weak reasoning.
    """
    # The actual escalation is handled by ADK's LoopAgent via the
    # tool_context. We return a signal dict here; the agent's
    # instruction tells the critic to use this when satisfied.
    return {"status": "Research complete. Exiting refinement loop."}


# --- Researcher Agent ---

researcher_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="researcher_agent",
    description="An autonomous research agent that gathers information using multiple tools.",
    instruction="""You are an advanced autonomous research assistant called Nexus AI Engine.

Your responsibilities:
1. Analyze the user's query carefully to understand what information is needed.
2. Select the most appropriate tool(s) to gather relevant information:
   - Use 'document_search_tool' for questions about uploaded documents, PDFs, or the private knowledge base.
   - Use 'web_search_tool' for current events, general knowledge, or topics not in the documents.
   - Use 'financial_data_tool' for stocks, crypto, currencies, forex, or financial market data.
   - Use 'news_agent_tool' for breaking news, headlines, or latest updates on any topic.
   - Use 'canvas_tool' when the user asks you to generate a report, summary, HTML document, markdown, or code.
3. Synthesize information from multiple sources into a clear, coherent answer.
4. Resolve conflicting information by preferring more authoritative and recent sources.
5. Always cite your sources when possible.

If a previous critique identified gaps, focus your research on addressing those specific gaps.
Store your research answer for the critic to review.""",
    tools=[
        document_search_tool,
        web_search_tool,
        financial_data_tool,
        news_agent_tool,
        canvas_tool,
    ],
    output_key="research_answer",
)


# --- Critic Agent ---

critic_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="critic_agent",
    description="A research critic that evaluates answers and decides if more research is needed.",
    instruction="""You are an expert research critic. Your job is to evaluate the quality
of the research answer produced by the researcher agent.

Read the current research answer from the session state key 'research_answer'.

Evaluate the answer against these criteria:
1. Does it fully address the original user question?
2. Is the information accurate and well-supported?
3. Are there any gaps, missing perspectives, or weak reasoning?
4. Is the answer clear, coherent, and well-organized?

If the answer is strong and complete:
- Call the 'exit_loop' tool to signal that no further research is needed.

If the answer has gaps or needs improvement:
- Provide specific, actionable feedback about what is missing.
- Suggest follow-up research questions.
- Do NOT call exit_loop — let the loop continue for another iteration.""",
    tools=[exit_loop],
    output_key="critique_feedback",
)


# --- Root Agent (LoopAgent) ---

root_agent = LoopAgent(
    name="nexus_engine",
    description="Nexus AI Engine — Autonomous Research Agent with critique loop.",
    sub_agents=[researcher_agent, critic_agent],
    max_iterations=2,
)


# --- Runner Utilities ---

_session_service = InMemorySessionService()
_runner = InMemoryRunner(agent=root_agent, app_name="nexus_engine")


async def _ask_agent_async(query: str, max_iterations: int = 2) -> str:
    """Run the agent asynchronously and return the final answer."""

    # Update max_iterations dynamically
    root_agent.max_iterations = max_iterations

    # Create a unique session for each query
    import uuid
    session_id = str(uuid.uuid4())
    user_id = "streamlit_user"

    session = await _session_service.create_session(
        app_name="nexus_engine",
        user_id=user_id,
        session_id=session_id,
    )

    # Prepare the user message
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=query)]
    )

    # Run the agent and collect the final response
    final_response = ""

    async for event in _runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        # Capture text from agent events
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    final_response = part.text

    # If the runner stored a research_answer in state, prefer that
    updated_session = await _session_service.get_session(
        app_name="nexus_engine",
        user_id=user_id,
        session_id=session_id,
    )

    if updated_session and updated_session.state:
        research_answer = updated_session.state.get("research_answer", "")
        if research_answer:
            final_response = research_answer

    return final_response if final_response else "I could not generate a response. Please try again."


def ask_agent(query: str, max_iterations: int = 2) -> str:
    """Synchronous wrapper for the async ADK agent runner.

    This is called by the Streamlit UI and CLI interfaces.

    Args:
        query: The user's research question.
        max_iterations: Maximum critique/refinement iterations (default: 2).

    Returns:
        The agent's final research answer as a string.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context (e.g., Streamlit),
            # create a new event loop in a thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = pool.submit(
                    asyncio.run,
                    _ask_agent_async(query, max_iterations)
                ).result()
            return result
        else:
            return loop.run_until_complete(
                _ask_agent_async(query, max_iterations)
            )
    except RuntimeError:
        # No event loop exists yet
        return asyncio.run(_ask_agent_async(query, max_iterations))
