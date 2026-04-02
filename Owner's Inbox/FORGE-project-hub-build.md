# FORGE Deliverable: Project Hub — Phases 1-3 Complete

**Date:** 2026-03-26
**Agent:** FORGE
**Status:** SHIPPED — all three phases built, tested, and validated

---

## What Was Built

Project Hub is Ron's centralized project registry. It is a FastAPI backend (port 8600) backed by PostgreSQL (`project_hub` schema) with a 10-tool MCP stdio server registered in `.claude.json`. All 15 known AI Army projects are seeded with locations, tags, and status notes.

---

## Architecture

```
D:\project-hub\
├── app\
│   ├── config.py          — Settings (pydantic-settings, .env)
│   ├── database.py        — SQLAlchemy engine, session, schema init
│   ├── models.py          — 6 ORM tables: projects, locations, tags, project_tags, notes, project_links
│   ├── schemas.py         — Pydantic v2 request/response schemas + enums
│   ├── main.py            — FastAPI app, lifespan, CORS, router mounts
│   ├── routers\
│   │   ├── projects.py    — 9 endpoints (list, create, get, patch, tree, tags, links, search)
│   │   ├── notes.py       — 2 endpoints (add note, list notes)
│   │   └── stats.py       — 2 endpoints (stats, health)
│   └── services\
│       └── project_service.py — Business logic layer (12 functions)
├── mcp_server\
│   ├── server.py          — MCP stdio server, 10 tools registered
│   └── tools.py           — 10 async handlers (each owns its own DB session)
├── scripts\
│   ├── seed_from_memory.py — Idempotent seed: 15 projects from CLAUDE.md
│   ├── start.bat
│   └── start.ps1
├── alembic\               — Migrations (001_initial_schema.py)
├── .env                   — PH_DATABASE_URL, PH_PORT=8600, PH_SCHEMA=project_hub
├── .venv\                 — Python 3.12 venv (all deps installed)
└── pyproject.toml
```

**Database:** PostgreSQL `localhost:5432`, schema `project_hub`, 6 tables created by `Base.metadata.create_all()` on startup.

**Dependency decisions:**
- SQLAlchemy 2.0 ORM with `Mapped`/`mapped_column` (modern style matching MemoryWeb patterns)
- Pydantic v2 with `model_validate()` and `ConfigDict(from_attributes=True)`
- MCP 1.26.0 (latest) with `stdio_server` pattern
- psycopg2-binary (no compile requirement)

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | DB connectivity check |
| GET | `/api/stats` | Counts by status, recent 5 projects |
| GET | `/api/projects` | List with `?status=`, `?tag=`, `?tech=`, `?limit=`, `?offset=` |
| POST | `/api/projects` | Create project (201) |
| GET | `/api/projects/{slug}` | Full detail with locations, notes, tags |
| PATCH | `/api/projects/{slug}` | Update fields (patch semantics) |
| GET | `/api/projects/{slug}/tree` | Parent-child subtree |
| POST | `/api/projects/{slug}/tags/{tag_name}` | Add tag |
| DELETE | `/api/projects/{slug}/tags/{tag_name}` | Remove tag |
| POST | `/api/projects/{slug}/notes` | Add note |
| GET | `/api/projects/{slug}/notes` | List notes |
| POST | `/api/links` | Create project relationship |
| GET | `/api/search?q=...` | Full-text search (name, description, notes) |

---

## MCP Tools (10)

Registered in `.claude.json` as `"project-hub"`. All agents can now call these tools directly:

| Tool | Description |
|------|-------------|
| `project_list` | List with status/tag/tech filters |
| `project_get` | Full detail by slug |
| `project_create` | Create new project |
| `project_update` | Patch fields |
| `project_note` | Append timeline note |
| `project_search` | Full-text search |
| `project_tree` | Parent-child subtree |
| `project_tag` | Add or remove tag |
| `project_link` | Create graph relationship |
| `project_stats` | Summary counts and recent activity |

---

## Seeded Projects (15)

| Slug | Name | Status | Port |
|------|------|--------|------|
| datashield | DataShield | active | — |
| aihangout | aihangout.ai | active | — |
| ultra-rag | Ultra RAG | active | 8300 |
| memoryweb | MemoryWeb | active | 8100 |
| agentforge | AgentForge | active | 8400 |
| behaviorshield | BehaviorShield | active | — |
| imds-autoqa | IMDS AutoQA | active | — |
| memory-beast | Memory Beast | planning | — |
| ultrasecure-email | UltraSecure Email | active | — |
| civicmind | CivicMind | planning | — |
| ai-army-os | AI Army OS | active | 8500 |
| memorypulse | MemoryPulse | active | 8200 |
| acq-copilot | Acq-Copilot | active | 8001 |
| shared-toolkit | Shared Toolkit | active | — |
| project-hub | Project Hub | active | 8600 |

Each project has: locations, relevant tags, and one seed note with current status from CLAUDE.md.

---

## Validation Results (Verified Live)

```
GET /api/health   -> {"status":"ok","db":"ok","service":"project-hub","port":8600}
GET /api/projects -> 15 projects returned, all with correct status/port
GET /api/stats    -> {"total_projects":15,"total_notes":15,"by_status":{"active":13,"planning":2}}
GET /api/search?q=IMDS -> 2 results: imds-autoqa, ultra-rag
GET /api/projects/memoryweb -> name, status, port=8100, tags=['active-dev'], 1 note, 1 location
```

Seed script ran idempotently (re-run is safe — skips existing slugs).

---

## How to Start

```powershell
# PowerShell
D:\project-hub\scripts\start.ps1

# Or directly:
cd D:\project-hub
.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8600 --reload
```

Docs available at `http://localhost:8600/docs` once running.

---

## MCP Registration

Already added to `C:\Users\techai\.claude.json` under `mcpServers.project-hub`. Takes effect on next Claude session restart.

```json
"project-hub": {
  "type": "stdio",
  "command": "D:\\project-hub\\.venv\\Scripts\\python.exe",
  "args": ["D:\\project-hub\\mcp_server\\server.py"],
  "env": {
    "PH_DATABASE_URL": "postgresql://postgres:%3FBooker78%21@localhost:5432/postgres"
  }
}
```

---

## Known Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Port 8600 conflict | Check with `netstat -an | findstr 8600` before starting |
| Schema collision with other projects | `project_hub` schema is isolated — no overlap with `memoryweb` or `rag` schemas |
| Seed re-run during data loss | Idempotent: checks slug existence before insert, skips duplicates |
| MCP server import error if app/ not in path | `server.py` inserts parent dir into `sys.path` and `chdir` to project root on startup |
| `.env` not found when MCP called from arbitrary cwd | `os.chdir()` in `server.py` ensures `.env` is always found |
| `location` unique constraint on `(project_id, machine, path)` | Null paths in multi-location projects (e.g. aihangout spark_1 + vps) use different machine values — no conflict |

---

## Next Actions (Optional — not in scope for this build)

- Add `GET /api/projects/{slug}/links` to surface graph edges
- Add pgvector semantic search (currently ILIKE full-text — sufficient for now)
- Wire MemoryPulse telemetry to track Project Hub request counts
- Add a simple HTML dashboard at `/` showing all active projects

---

*Delivered by FORGE. Validated live. No placeholders.*
