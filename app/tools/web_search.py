from ddgs import DDGS


def web_search_tool(query: str) -> str:
    """Search the public web for current information using DuckDuckGo.

    Use this tool when the user asks about recent events, current facts,
    general knowledge, comparisons, or anything not covered by the
    local document knowledge base or financial data tools.

    Args:
        query: The search query to look up on the web.

    Returns:
        A string containing titles, snippets, and links from web results.
    """
    results_text = ""

    try:
        with DDGS() as ddgs:
            results = ddgs.text(
                query,
                max_results=5
            )

            for i, result in enumerate(results):
                if not result:
                    continue

                results_text += f"\n[Web Source {i+1}]\n"
                results_text += f"Title: {result.get('title', 'No Title')}\n"
                results_text += f"Body: {result.get('body', 'No Body')}\n"
                results_text += f"Link: {result.get('href', 'No Link')}\n\n"

    except Exception as e:
        results_text = f"Web search failed: {str(e)}"

    return results_text