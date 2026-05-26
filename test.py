import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner

# Load ADK-style env vars
load_dotenv()

async def main():
    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="test_agent",
        instruction="Explain what a RAG agent is in simple words"
    )
    runner = InMemoryRunner(agent=agent, app_name="test_agent")
    
    print("Invoking ADK Agent...")
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session"
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(part.text, end="")
    print()

if __name__ == "__main__":
    asyncio.run(main())