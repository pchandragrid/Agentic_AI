"""
Nexus AI Engine — CLI Interface.

This module provides a command-line interface for interacting with the
ADK-based autonomous research agent.
"""

from app.rag.ingest import load_pdf, chunk_text
from app.rag.vector_store import add_documents
from app.agent import ask_agent


def main():
    """Run the CLI interface for the Nexus AI Engine."""

    # Ingest the research PDF into the FAISS vector store
    pdf_path = "app/data/research.pdf"

    try:
        text = load_pdf(pdf_path)
        chunks = chunk_text(text)
        add_documents(chunks)
        print("\n✓ RAG knowledge base loaded successfully.")
    except Exception as e:
        print(f"\n⚠ Could not load PDF ({e}). Document search will be limited.")

    print("\n" + "=" * 50)
    print("  Nexus AI Engine — Autonomous Research Agent")
    print("  Powered by Google ADK + Gemini 2.0 Flash")
    print("=" * 50)
    print("\nType your questions below. Type 'exit' to quit.\n")

    while True:
        query = input("\n🔍 Ask Question: ")

        if query.lower().strip() in ("exit", "quit", "q"):
            print("\nGoodbye!")
            break

        if not query.strip():
            continue

        print("\n⏳ Researching...")

        answer = ask_agent(query, max_iterations=2)

        print("\n📋 Answer:")
        print(answer)


if __name__ == "__main__":
    main()