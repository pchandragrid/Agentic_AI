# Nexus AI Engine - Autonomous Research Agent

Welcome to the **Nexus AI Engine** project, an Advanced Multimodal Autonomous Research Agent. This project demonstrates a powerful, multi-agent AI system capable of autonomous reasoning, web research, document analysis, and iterative refinement.

## 🌟 Project Overview

The Nexus AI Engine is designed to tackle complex user queries by automatically routing them to specialized tools and refining the answers through an iterative critique loop. It features a premium dark-themed Streamlit UI and a robust Python backend powered by Google's Gemini models via Vertex AI.

### Key Aspects of the Project

1. **Intelligent Planner (`app/agent.py`)**: An autonomous agent that analyzes queries and delegates tasks to specific tools (Document Search, Web Search, Financial Data, News Agent, or Canvas generation).
2. **Critique Loop (`app/critique.py`)**: The system doesn't just answer once; it reviews its own generated answer against the original query, identifying missing information and formulating follow-up queries until the response is complete.
3. **Multimodal RAG Pipeline (`app/rag/`)**: Ingests PDF documents (`app/data/research.pdf`), chunks the text, and stores embeddings in a local vector store (FAISS) for quick retrieval.
4. **Agent-to-Agent (A2A) Microservices (`news_agent/`)**: Includes a separate FastAPI microservice specifically dedicated to fetching real-time news using DuckDuckGo search. The main agent communicates with this microservice via an A2A client tool.
5. **Specialized Tools (`app/tools/`)**:
    - Web Search Tool
    - Document Search Tool (RAG)
    - Financial Data Tool
    - News Agent Tool
    - Canvas Tool (for generating formatted output like HTML, Markdown, or Code snippets)
6. **Premium UI (`streamlit_app.py`)**: A modern, glassmorphic Streamlit interface that provides a chat-like experience with simulated streaming and capability tags.

## 🎥 Demonstration

Check out our project in action!

🎥 **[Demo Video](https://drive.google.com/file/d/1uhh4dthggjAi_O0Nf3vaKvzr6Wlvh1TC/view?usp=sharing)**

## 🚀 Setup and Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository
Ensure you are in the project root directory (`Agentic_AI`).

### 2. Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# .\venv\Scripts\activate # On Windows
```

### 3. Install Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Ensure you are authenticated with Google Cloud (for Vertex AI) or set the required environment variables:
```bash
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export MODEL_NAME="gemini-2.0-flash"
```

## 💻 How to Run

Because this project utilizes a microservice architecture, you need to run the News Agent and the Main Interface separately.

### Step 1: Start the News Agent Microservice
Open a new terminal, activate your virtual environment, and run the FastAPI server:
```bash
uvicorn news_agent.main:app --port 8000 --reload
```

### Step 2: Launch the Nexus AI Engine
You have two options to run the main agent:

**Option A: Streamlit UI (Recommended)**
Open another terminal, activate your virtual environment, and run:
```bash
streamlit run streamlit_app.py
```
This will open the premium UI in your default web browser.

**Option B: Command Line Interface (CLI)**
If you prefer to interact via the terminal, you can run the core script directly:
```bash
python -m app.main
```
This will initialize the RAG backend, ingest the sample `research.pdf`, and provide a command-line prompt for queries.

## 🧠 Architecture Flow

1. User submits a query via the Streamlit UI or CLI.
2. The **Planner** determines the intent (financial, news, document, web, or canvas).
3. The query is routed to the appropriate **Tool** (or the external News microservice).
4. Information is gathered and passed to the **Generative Model** to draft a response.
5. The draft is sent to the **Critique Module**.
6. If the critique says `COMPLETE`, the answer is returned to the user. If it says `FOLLOW_UP: [question]`, the agent iterates and gathers more data before finalizing the answer.
