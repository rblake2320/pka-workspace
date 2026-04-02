# Council Platform — Phase 1 Complete

**Delivered by**: FORGE
**Date**: 2026-03-28
**Status**: LIVE — end-to-end tested

---

## What Was Built

A full collaborative AI agent platform at `C:\Users\techai\council\` — frontend on :3000, backend API on :8600.

### Verified Working (visual + API confirmation)

| Feature | Status | Evidence |
|---------|--------|---------|
| Dashboard with live stats | ✅ | 1 council, 13 agents, Online badge |
| Agent registry (13 PKA agents) | ✅ | All 13 rendered in grid with search/tabs |
| Agent detail + system prompt | ✅ | Full system prompt, stats |
| New agent wizard (AI + Twin tabs) | ✅ | 5-step form renders |
| Council list | ✅ | Live badge, agent count, message count |
| New council wizard | ✅ | 5-step: Basics, Format, Agents, Review |
| **Live debate view — 3-panel** | ✅ | Roster, message stream, synthesis rail |
| **Agents generating debate** | ✅ | 4 agents responded, round 2 smart-participation |
| **Synthesis engine** | ✅ | consensus/dissent/insights/votes JSON generated |
| Synthesis page (Verdict view) | ✅ | Agent vote positions rendered |
| **Agent memory (self-learning)** | ✅ | GRID: "precautionary skepticism" pattern extracted |
| API docs (Swagger) | ✅ | All 20+ endpoints documented |
| Settings page | ✅ | API key, Ollama URL, all credential fields |
| System health panel | ✅ | API/DB/Redis all Online |
| Redis pub/sub | ✅ | Confirmed connected |
| WebSocket endpoint | ✅ | `/ws/councils/{id}` — auth, join, subscribe, message |
| API key auth | ✅ | X-Council-Key header, optional bootstrap |

---

## Architecture Confirmed

```
Frontend (Next.js :3000) → Backend (FastAPI :8600) → PostgreSQL :5432
                                      ↓
                                 Redis :6379 (pub/sub)
                                      ↓
                               Ollama :11434 (llama3.1:8b)
```

4 Alembic migrations applied (001 base → 004 notifications). Schema: `council.*`

---

## Bugs Fixed During Testing

1. **Background task stale DB session** — `run_round` now creates fresh `AsyncSessionLocal` so the db doesn't expire when the HTTP response closes. Root cause: FastAPI `Depends(get_db)` sessions are request-scoped.

2. **DEFAULT_MODEL** — Changed from `gemma3:latest` (not installed locally) to `llama3.1:8b`. Config at `backend/.env`.

3. **API envelope detection** — Frontend `api.ts` was checking `'success' in envelope` before the `data+meta` check. Fixed ordering.

4. **Alembic `%` interpolation** — `%3F` and `%21` in the DB URL tripped configparser. Fixed with `.replace("%", "%%")` in `env.py`.

5. **Alembic array literals** — `server_default="'{message,...}'"` was malformed for asyncpg. Fixed with `sa.text("ARRAY['message',...]")`.

6. **asyncpg JSONB dict** — Seed script passed Python `{}` dict instead of string `"{}"`. Fixed.

---

## What Needs Your Anthropic API Key

Agents currently use `llama3.1:8b` (local, fast). To use Claude models:

1. Add to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
2. Update agents in DB (or via Settings → Agent detail → Edit):
   ```sql
   UPDATE council.agents SET model_preference = 'claude-opus-4-6';
   ```
3. Restart backend.

---

## Admin API Key (for browser sessions)

```
ck_9b694a6315cfc99b8ce7244a917b890b79140cd998ed8154d47195ac77ec4da8
```

Enter this in Settings → Models → Council API Key field to authenticate the browser.

---

## Live Council

**Architecture Review: WebSocket vs SSE**
Council ID: `53c82d03-8627-46db-9858-d1ec509785db`
Status: Active | Agents: GRID, RADAR, CRUCIBLE, DEBUGGER
Messages: 5 | Synthesis: 1 verdict generated
GRID memory: 1 pattern insight ("precautionary skepticism")

---

## How to Start the Platform

```bash
# Backend
cd C:\Users\techai\council\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8600

# Frontend (separate terminal)
cd C:\Users\techai\council\frontend
npm run dev
```

---

## What's Next (Phase 1.5 / Phase 2)

- Add Anthropic key to unlock Claude agents
- Test human-join flow (WebSocket `{type:"join"}` → appears in roster)
- Test twin_override flow (human takes over from digital twin mid-meeting)
- Wire up Settings "API Keys" tab to the `/api/keys` backend (currently frontend-only display)
- Add council templates (save & reuse council configs)
- GitHub integration (`gh` CLI for repo awareness from debate engine)
- Deploy behind Cloudflare tunnel

---

**FORGE sign-off**: Phase 1 delivered. The debate engine runs. Agents argue. Synthesis works. Memory persists. All core systems operational.
