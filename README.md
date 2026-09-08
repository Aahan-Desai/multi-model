# Multi-Model Orchestrator

A full-stack AI application for orchestrating multiple model capabilities across chat, document ingestion, vision, web search, and structured math/tool execution.

The repository combines:

- a FastAPI backend in [backend](backend)
- a Next.js frontend in [frontend](frontend)
- shared application configuration and environment settings in [.env](.env)

## Overview

This project provides a single assistant-style interface that can:

- answer user questions through a routed multi-model chat flow
- ingest and process documents for retrieval-augmented generation (RAG)
- analyze uploaded images and media with vision services
- perform web search and compare sources
- run code-based math and execution tasks through a Python executor

## Architecture

At a high level:

- The FastAPI app in [backend/main.py](backend/main.py) initializes services and exposes the API.
- API endpoints live under [backend/api/routers](backend/api/routers).
- Routing and orchestration logic live under [backend/orchestrator](backend/orchestrator).
- Document ingestion, vector search, and specialist services live under [backend/infrastructure](backend/infrastructure) and [backend/specialists](backend/specialists).
- The frontend in [frontend/app/page.tsx](frontend/app/page.tsx) renders the assistant workspace using Next.js.

## Tech Stack

### Backend

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic / Pydantic Settings
- Qdrant
- Ollama
- Google Gemini
- Tavily

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Axios

## Prerequisites

Before running the project, make sure you have:

- Python 3.12 or newer
- Node.js 20+ and npm
- access to the required external services configured in your environment file
- a local or remote Qdrant instance
- Ollama running if you are using embedding or model endpoints through it

## Environment Setup

The backend reads configuration from [.env](.env). Make sure that file exists in the repository root and contains the necessary keys for:

- Groq
- Gemini
- Ollama
- Qdrant
- Tavily
- storage and ingestion settings

## Local Development

### 1. Create and activate the Python virtual environment

```powershell
cd b:\atQor\multi-model-orchestrator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Python dependencies

```powershell
python -m pip install -U pip
python -m pip install -e .
```

### 3. Start the FastAPI backend

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:

- `http://localhost:8000`
- Swagger docs at `http://localhost:8000/docs`
- Health endpoint at `http://localhost:8000/health`

### 4. Start the frontend

```powershell
cd frontend
npm install
npm run dev
```

The frontend will run on:

- `http://localhost:3000`

## Project Structure

```text
backend/
  api/
  core/
  infrastructure/
  models/
  orchestrator/
  processing/
  prompts/
  specialists/
  utils/
frontend/
  app/
  components/
  features/
  hooks/
  lib/
  services/
  stores/
  types/
```

## Main API Routes

The backend exposes endpoints for:

- chat via `/chat`
- health checks via `/health`
- document upload and ingestion via `/upload`
- vision-related requests via `/vision`

## Notes

- The backend entrypoint is defined in [backend/main.py](backend/main.py).
- The frontend API base URL defaults to `http://127.0.0.1:8000` from [frontend/lib/constants.ts](frontend/lib/constants.ts).
- The repo includes an empty starter root script in [main.py](main.py), but the real application entrypoint is the FastAPI backend.

## License

This project does not currently document a separate license in the repository.
