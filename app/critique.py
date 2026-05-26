"""
Critique module for the Nexus AI Engine.

In the ADK architecture, critique functionality is handled by the
critic_agent (LlmAgent) within the LoopAgent in agent.py.

This module is retained for backward compatibility with the CLI interface.
The actual critique loop is managed by ADK's LoopAgent with exit_loop tool.
"""


def critique_response(model, query: str, answer: str) -> str:
    """Legacy critique function for backward compatibility.

    In the new ADK architecture, this is handled by the critic_agent
    within the LoopAgent. This function is kept for the CLI fallback.

    Args:
        model: The generative model instance.
        query: The original user question.
        answer: The generated answer to critique.

    Returns:
        A critique string — either 'COMPLETE' or 'FOLLOW_UP: ...'
    """
    critique_prompt = f"""
    You are an expert research critic.

    Analyze the following answer carefully.

    Original Question:
    {query}

    Generated Answer:
    {answer}

    Your task:
    1. Identify missing information
    2. Detect weak reasoning
    3. Detect incomplete evidence
    4. Suggest follow-up research questions

    If answer is already strong, say:
    COMPLETE

    Otherwise output:

    FOLLOW_UP:
    question 1
    question 2
    """

    response = model.generate_content(critique_prompt)

    return response.text