from app.rag.vector_store import search


def document_search_tool(query: str) -> str:
    """Search the local document knowledge base using FAISS vector similarity.

    Use this tool when the user asks about information that might be in
    uploaded PDF documents, reports, or the private knowledge base.

    Args:
        query: The search query to find relevant document passages.

    Returns:
        A string containing the most relevant document passages.
    """
    results = search(query)

    context = ""

    for i, result in enumerate(results):
        context += f"\n[Source {i+1}]\n"
        context += result
        context += "\n"

    return context