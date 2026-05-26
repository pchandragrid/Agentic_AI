from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
from starlette.responses import JSONResponse
from starlette.requests import Request

# Create a FastMCP server listening on port 8080 when running SSE
mcp = FastMCP("FetchServer", port=8080)

@mcp.tool()
def fetch(url: str) -> str:
    """Fetches the content of a URL and returns a cleaned text version.
    
    Args:
        url: The URL to fetch.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # Get text
        text = soup.get_text(separator=" ")
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)
        
        return text[:10000] # Limit to 10k chars
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

@mcp.custom_route("/fetch", methods=["POST"])
async def fetch_endpoint(request: Request):
    """Custom HTTP endpoint to allow direct POST requests from the financial tool."""
    try:
        data = await request.json()
        url = data.get("url")
        if not url:
            return JSONResponse({"error": "Missing url parameter"}, status_code=400)
        
        content = fetch(url)
        return JSONResponse({"content": content})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    mcp.run()
