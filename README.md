# Nexus AI Engine - Autonomous Research Agent

Welcome to the **Nexus AI Engine** project, an Advanced Multimodal Autonomous Research Agent built with **Google's Agent Development Kit (ADK)**. This project demonstrates a powerful, multi-agent AI system capable of autonomous reasoning, web research, document analysis, and iterative refinement.

## 🌟 Project Overview

The Nexus AI Engine is built using **Google ADK**, **Gemini 2.0 Flash via Vertex AI**, **FAISS**, and a premium **Streamlit** UI. It features an autonomous research pipeline with a self-critique loop that iteratively refines answers until they are comprehensive and accurate.

### Architecture

```
root_agent (LoopAgent) — max_iterations configurable
├── researcher_agent (LlmAgent)
│   Tools: document_search, web_search, financial_data, news_agent, canvas
└── critic_agent (LlmAgent)
    Tools: exit_loop
```

### Key Aspects

1. **ADK-Based Agent Architecture (`app/agent.py`)**: Built with `google.adk.agents.LlmAgent` and `google.adk.agents.LoopAgent`. The LLM autonomously decides which tool to call — no hard-coded keyword routing.
2. **Autonomous Critique Loop**: A `LoopAgent` wraps a researcher and critic agent. The critic evaluates the research answer and either calls `exit_loop` (complete) or provides feedback for another iteration.
3. **RAG Pipeline (`app/rag/`)**: Ingests PDF documents, chunks text, and stores embeddings in a local **FAISS** vector store for quick retrieval using `sentence-transformers`.
4. **MCP Server Integration (`app/tools/financial_tool.py`)**: Financial data is fetched via the **Anthropic fetch MCP server**, providing structured context-verified retrieval from Yahoo Finance.
5. **Agent-to-Agent Microservice (`news_agent/`)**: A separate **FastAPI** microservice for fetching real-time news via DuckDuckGo. The main agent communicates with it via HTTP.
6. **Specialized Tools (`app/tools/`)**:
    - **Document Search Tool** — FAISS-based RAG retrieval
    - **Web Search Tool** — DuckDuckGo web search
    - **Financial Data Tool** — Yahoo Finance via MCP fetch server
    - **News Agent Tool** — A2A communication with News microservice
    - **Canvas Tool** — Jinja2-based report/code generation (Markdown, HTML, Code)
7. **Premium UI (`streamlit_app.py`)**: A modern, glassmorphic Streamlit interface with a chat experience.

## 🎥 Demonstration

🎥 **[Demo Video](https://drive.google.com/file/d/1uhh4dthggjAi_O0Nf3vaKvzr6Wlvh1TC/view?usp=sharing)**

## 🚀 Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/pchandragrid/Agentic_AI.git
cd Agentic_AI
```

### 2. Set Up a Virtual Environment (Python 3.11 recommended)
```bash
python3.11 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file (or use the existing one):
```env
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

Ensure you are authenticated with Google Cloud:
```bash
gcloud auth application-default login
```

## 💻 How to Run

### Step 1: Start the News Agent Microservice
```bash
uvicorn news_agent.main:app --port 9000
```

### Step 2: Launch the Nexus AI Engine

**Option A: Streamlit UI (Recommended)**
```bash
streamlit run streamlit_app.py
```
Opens at `http://localhost:8501`.

**Option B: ADK Dev UI**
```bash
adk web app
```

**Option C: CLI**
```bash
python -m app.main
```

## 🐳 Docker

```bash
docker build -t nexus-engine .
docker run -p 8501:8501 -p 9000:9000 nexus-engine
```

## 🧠 Architecture Flow

1. User submits a query via Streamlit UI, ADK Web, or CLI.
2. The **LoopAgent** starts the research cycle.
3. The **Researcher Agent** (LlmAgent) autonomously selects the best tool(s) and gathers information.
4. The gathered context is synthesized into a draft answer by Gemini.
5. The **Critic Agent** evaluates the draft:
   - If **COMPLETE** → calls `exit_loop`, answer is returned.
   - If **gaps found** → provides feedback, loop continues.
6. The cycle repeats up to `max_iterations` times.

## 📁 Repository Structure

- `app/agent.py` — ADK agent definitions (LoopAgent, LlmAgent, Runner)
- `app/critique.py` — Legacy critique module (now handled by ADK CriticAgent)
- `app/tools/` — All tool implementations with ADK-compatible docstrings
- `app/rag/` — FAISS vector store, embeddings, PDF ingestion
- `app/data/` — Source PDFs for RAG
- `news_agent/` — Standalone FastAPI news microservice
- `streamlit_app.py` — Premium Streamlit UI
- `Dockerfile` — Container configuration
