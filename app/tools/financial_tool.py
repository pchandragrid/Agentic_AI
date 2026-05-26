import requests
from bs4 import BeautifulSoup


FINANCIAL_SOURCES = {
    "stocks": {
        "url": "https://finance.yahoo.com/markets/stocks/most-active/",
        "description": "Most active US stocks and market movers"
    },
    "crypto": {
        "url": "https://finance.yahoo.com/markets/crypto/all/",
        "description": "Cryptocurrency market trends including Bitcoin and Ethereum"
    },
    "currencies": {
        "url": "https://finance.yahoo.com/markets/currencies/",
        "description": "Forex and global currency exchange trends"
    }
}


def _detect_source_type(query: str) -> str:
    """Detect the financial source type from the query."""
    query_lower = query.lower()

    if any(word in query_lower for word in [
        "stock", "stocks", "market", "nasdaq", "dow"
    ]):
        return "stocks"
    elif any(word in query_lower for word in [
        "crypto", "bitcoin", "ethereum", "btc", "eth"
    ]):
        return "crypto"
    else:
        return "currencies"


def _fetch_via_mcp(url: str) -> str:
    """Fetch a URL via the MCP fetch server running on localhost:8080.

    The MCP fetch server (Anthropic reference implementation) runs as a
    separate service and provides clean text extraction from web pages.
    Falls back to direct HTTP if the MCP server is not available.
    """
    try:
        # Try the MCP fetch server first (runs on port 8080)
        mcp_response = requests.post(
            "http://127.0.0.1:8080/fetch",
            json={"url": url},
            timeout=15
        )

        if mcp_response.status_code == 200:
            data = mcp_response.json()
            content = data.get("content", "")
            if content:
                return content[:8000]

    except Exception:
        pass

    # Fallback: direct HTTP fetch with BeautifulSoup
    return _fetch_direct(url)


def _fetch_direct(url: str) -> str:
    """Fallback: fetch URL directly with BeautifulSoup."""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return text[:8000]

    except Exception as e:
        return f"Error fetching data: {str(e)}"


def financial_data_tool(query: str) -> str:
    """Retrieve real-time financial data from Yahoo Finance via MCP fetch server.

    Use this tool when the user asks about stocks, stock market, crypto,
    bitcoin, ethereum, currencies, forex, USD, EUR, or any financial
    market data. This tool fetches data from Yahoo Finance sources
    through the MCP (Model Context Protocol) fetch server.

    Args:
        query: The financial query (e.g., 'most active stocks today',
               'bitcoin price', 'USD to EUR exchange rate').

    Returns:
        A string containing financial data from Yahoo Finance.
    """
    source_type = _detect_source_type(query)

    source_info = FINANCIAL_SOURCES[source_type]

    data = _fetch_via_mcp(source_info["url"])

    return f"""
    Financial Category: {source_type}
    Source Description: {source_info["description"]}
    Source URL: {source_info["url"]}
    Retrieved Financial Data:
    {data}
    """