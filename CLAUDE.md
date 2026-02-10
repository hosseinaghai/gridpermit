# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GridPermit Guide is a workflow-software for managing German electrical grid expansion permitting (NABEG/EnWG processes). It guides projects through multi-stage regulatory workflows with task management, GIS mapping, and AI-assisted text generation. All UI text is in German.

## Tech Stack

- **Frontend:** React 18 + TypeScript (strict), Vite, Tailwind CSS, Zustand (state), TanStack React Query (data fetching), Leaflet (maps)
- **Backend:** Python 3.11, FastAPI, Pydantic, Uvicorn
- **Deployment:** Docker multi-stage build, Render.com

## Development Commands

### Frontend (from `frontend/`)
```bash
npm install              # Install dependencies
npm run dev              # Dev server on http://localhost:5173 (proxies /api to :8000)
npm run build            # TypeScript check + Vite production build → dist/
npm run preview          # Preview production build
```

### Backend (from `backend/`)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000   # Dev server with auto-reload
```

Both servers must run concurrently for local development. Vite proxies `/api` requests to the backend.

FastAPI auto-generates Swagger docs at `http://localhost:8000/docs`.

No test framework, linter, or formatter is currently configured.

## Architecture

**Monorepo** with `frontend/` and `backend/` directories.

### Frontend (`frontend/src/`)

- **Entry:** `main.tsx` → `App.tsx` (wraps app in React Query provider)
- **State:** Single Zustand store (`store/workflowStore.ts`) tracks current project, selected stage, and open task
- **API client:** `api/client.ts` — fetch wrapper with endpoints for projects, tasks, and AI generation
- **Layout:** 3-column design in `components/Layout.tsx`:
  - Left: `ProcessStepper` (stage navigation with progress)
  - Center: `WorkflowWizard` (task list) or `TaskWorker` (task editor with forms, checklists, AI generation, file upload)
  - Right: `InfoPanel` (contextual info: map, risks, blockers, documents, historical cases)
- **Types:** `types/index.ts` — shared TypeScript interfaces mirroring backend Pydantic models
- **TypeScript:** Strict mode with `noUncheckedIndexedAccess: true` — all indexed access returns `T | undefined`

### Backend (`backend/app/`)

- **`main.py`:** FastAPI app init, CORS middleware, static file serving for production SPA
- **`api.py`:** REST endpoints + AI text generation (hardcoded German regulatory text templates, 60+ per-field blocks with generic fallback)
- **`models.py`:** Pydantic models split into **templates** (ProcessTemplate → StageTemplate → TaskTemplate) and **runtime instances** (Project → StageInstance → TaskInstance), plus rich context models (Blocker, GeoLayer, Risk, etc.)
- **`workflow_engine.py`:** Business logic — contains NABEG and EnWG process template definitions (stage/task structure), stage/task evaluation, and status transitions
- **`mock_db.py`:** In-memory dict storage with seeded demo project (`P-DE-TSO-001`). No database — all data lives in memory and resets on restart

### Key Design Pattern: Template vs Instance

The core architecture separates **static definitions** from **runtime state**:
- `ProcessTemplate` → `StageTemplate` → `TaskTemplate` → `FormField` define the workflow structure
- `Project` → `StageInstance` → `TaskInstance` track actual project progress and user data
- The frontend receives both in a single `GET /api/project/{id}/workflow` response and joins them by template IDs

### Data Flow

1. Frontend loads project workflow via React Query (`GET /api/project/{id}/workflow`)
2. Response contains `Project` (runtime state) + `ProcessTemplate` (stage/task definitions)
3. User navigates stages → Zustand store updates → components rerender
4. Task save/complete → mutation → React Query cache invalidation

### Task/Stage Lifecycle

- **Task status:** `pending` → `in_progress` → `done` (can be reopened)
- **Stage status:** `pending` → `active` → `completed`
- Task IDs follow pattern: `s{stage}_{type}{number}` (e.g., `s1_t1`, `s2_t3`)
- Stage transitions are automatic: stage becomes `active` when any task starts, `completed` when all tasks are `done`

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/projects` | List all projects |
| POST | `/api/project/create` | Create new project |
| GET | `/api/project/{id}/workflow` | Get project state + process template |
| POST | `/api/task/{id}/complete` | Mark task done |
| POST | `/api/task/{id}/save` | Save task progress (auto-sets `in_progress`) |
| PATCH | `/api/task/{id}/reopen` | Reopen completed task |
| POST | `/api/ai/generate-field` | Generate German regulatory text for a form field |

### AI Text Generation (`api.py`)

The `/api/ai/generate-field` endpoint uses hardcoded German regulatory text templates — no LLM calls. The `_generate_for_field()` function maps `(task_template_id, field_name)` to specific text blocks (60+ mappings). Unmapped fields fall back to generic templates that match on field name patterns (e.g., names containing "begruendung" or "anschreiben"). Generated text is context-aware, interpolating project data like name, kV level, states, and route length.

## Production Build (Docker)

Multi-stage Dockerfile: Node 20 builds frontend → Python 3.11 serves backend + static assets. Built frontend goes to `/app/static`, with FastAPI catch-all route for SPA routing. Deployed on Render.com (free tier, port 8080).
