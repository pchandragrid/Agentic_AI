import requests


def news_agent_tool(query: str) -> str:
    """Fetch the latest news on a topic from the News Agent microservice.

    Use this tool when the user asks about recent news, headlines,
    breaking events, or latest updates on any topic. This delegates
    to an independent News Agent running as a separate FastAPI service.

    Args:
        query: The news topic to search for.

    Returns:
        A string containing recent news articles with titles, bodies, and links.
    """
    try:
        response = requests.get(
            "http://127.0.0.1:9000/news",
            params={"topic": query},
            timeout=10
        )

        data = response.json()

        return data["news"]

    except Exception as e:
        return f"News Agent Error: {str(e)}"