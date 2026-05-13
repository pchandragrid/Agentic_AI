# Module 3 — Agentic Systems Capstone

> Grid University · Gen AI Training Program

This branch is the **target** of your submission Pull Request for Module 3. Branch off this branch, build your project, then open a PR back into `agentic`. Two AI reviewers — Claude and Gemini — run in parallel on every PR and each posts a detailed sticky comment with the verdict, phase-by-phase analysis, and concrete action items. For the full submission flow, see the [`main` branch README](https://github.com/griddynamics/gridu-genai/blob/main/README.md).

> ⚠️ **Heads-up:** the Pull Request you will open targets this branch but **will never be merged.** The `agentic` branch is an evaluation target only. Your professor reads your code and the AI reviews on the PR thread, then closes the PR. No code from any submission ever lands on `agentic`.

---

## Overview

You will design and build an advanced **autonomous research agent**. The focus is on system architecture and design thinking. Start with a simple, functional RAG-based agent and incrementally enhance its capabilities, culminating in a system that can autonomously **plan, execute, critique, and refine** its own research process.

---

## Technical requirements

| Area | Requirement |
|---|---|
| LLM | Gemini 2.0 Flash (or newer) via **Vertex AI**. |
| Primary framework | **Agent Development Kit (ADK)** — <https://google.github.io/adk-docs/>. ADK is the course's primary framework — the framework itself is the learning objective. |
| Cloud platform | Google Cloud Platform. Services: Vertex AI (for Gemini models). |
| Tools & libraries | ADK; **FAISS** for in-memory document search; **a2a** *(optional, for A2A communication)*. |
| Language | Python. |
| UI *(optional)* | Streamlit or Gradio. |
| Containerisation | Docker. |

> **Important.** Substituting ADK with another agent framework (LangGraph, AutoGen, CrewAI, etc.) is not acceptable for this module — ADK is itself the learning objective.

---

## Final architecture goal

An agent that can **plan → execute → critique → refine** its own research process, with access to:

- a private document corpus (Phase 1),
- the public web (Phase 2),
- structured external data via an MCP server (Phase 3),
- a self-critique loop (Phase 4),
- a rich output canvas (Phase 6).

---

## Phase 1 — The Core RAG Agent

Build a functioning, end-to-end agent that can answer questions using a private knowledge base. This is your MVP.

- Architect a basic **Plan → Execute → Synthesise** flow as explicit, separable steps.
- Design and build the **Document Search Tool** — an ADK tool that performs retrieval over your local corpus using FAISS.

> You are strongly encouraged to adapt and reuse the RAG module from Module 2 as the foundation for the Document Search Tool.

---

## Phase 2 — Integrating External Knowledge

Expand the agent's awareness by giving it access to the public internet.

- Design and integrate a **Web Search Tool** into the agent's tool suite (Tavily, Serper, Bing, Google Custom Search, Brave — your choice; it must make real API calls, not return stubbed results).
- Update the **Planner** to intelligently delegate tasks between Document Search and Web Search based on the query.
- Update the **Synthesiser** to handle evidence from multiple, potentially conflicting sources and produce a unified, coherent answer.

---

## Phase 3 — Integrating a Model Context Protocol (MCP) Server

Extend the agent with structured, context-verified retrieval through an MCP server.

- **Deploy the MCP server** — use the Anthropic fetch reference implementation at <https://github.com/modelcontextprotocol/servers/tree/main/src/fetch>. For local development, run the Docker image.
- **Build a Financial Data Tool** (ADK tool) that hardcodes the following Yahoo Finance sources and routes requests through the MCP server:
  - <https://finance.yahoo.com/markets/stocks/most-active/>
  - <https://finance.yahoo.com/markets/crypto/all/>
  - <https://finance.yahoo.com/markets/currencies/>

  When a user asks about currencies, crypto, or stocks, the agent must use this tool instead of triggering a general web search.
- **Enhance the Planner** to pick the Financial Data Tool vs. the Web Search Tool based on the query.

---

## Phase 4 — The Autonomous Refinement Loop

Elevate the agent from a simple executor to an autonomous system that can self-critique.

- Design a **Critique** component — craft a prompt that lets an LLM review its own output, identify gaps, and generate actionable follow-up questions.
- Architect the **main Agent Loop** that:
  1. Runs the initial research cycle.
  2. Passes the output to the Critique component.
  3. Decides whether to terminate or feed the follow-up questions back to the Planner for another cycle.
- Add a **`max_iterations` parameter** on the request to bound the loop.

---

## Phase 5 — Agent-to-Agent Collaboration *(Optional)*

Explore distributed AI systems by delegating specialised tasks to an independent agent.

- Design a minimal **News Agent** with its own API endpoint that can search a knowledge base for the latest news on a topic.
- Build an A2A-client tool for the main agent that communicates with the News Agent.
- Update the Planner to delegate when appropriate.

> Phase 5 is explicitly optional and will **not** lower your grade.

---

## Phase 6 — Creating Canvas

Extend the agent with a tool for generating complex outputs — documents or code — based on collected information.

- **Design the Canvas tool:**
  - Define output formats: text documents, reports in Markdown / HTML, code snippets in specific languages.
  - Define the tool interface (how the agent passes data and instructions).
  - Consider integrating libraries like **Jinja2** (templating) or **Pydantic** (structure validation).
- **Integrate Canvas with the agent:**
  - Add Canvas to the agent's toolset.
  - Update the Planner to trigger Canvas when the user asks for a report, summary, or code snippet.
  - Modify the Synthesiser to prepare Canvas input in the appropriate format.

---

## How to submit

1. Branch off `agentic`: `git checkout agentic && git checkout -b <user-ldap-id>/agentic-submission`.
2. Build your project on that branch.
3. Open a Pull Request targeting the `agentic` branch.
4. Two AI reviewers (Claude + Gemini) run automatically and each posts a sticky PR comment with verdict, technical-requirements table, per-phase analysis, and action items.
5. Push more commits to re-trigger the reviewers. Each bot updates its existing comment in place.
6. When you reach `passed` / `passed_with_notes` on both, request final review from your professor.

Good luck.
