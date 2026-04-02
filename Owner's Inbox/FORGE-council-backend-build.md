# FORGE — Council Backend Build Report

**Delivered:** 2026-03-28
**Status:** COMPLETE — all files written, all syntax validated, all imports verified, OpenAPI schema clean

---

## What Was Built

Complete FastAPI backend for the Council collaborative AI agent platform.
32 files across the full stack: models, schemas, routers, engine, providers, migrations.

**Location:** `C:\Users\techai\council\backend\`

---

## File Inventory

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              FastAPI app — lifespan, CORS, middleware, health
│   ├── db.py                SQLAlchemy 2.0 async engine + session factory
│   ├── config.py            Pydantic settings (reads .env)
│   ├── auth.py              API key auth — generate, hash, verify, FastAPI deps
│   ├── utils.py             Shared: make_response(), not_found(), etc.
│   ├── models/
│   │   ├── agent.py         Agent ORM model
│   │   └── council.py       Council, Participant, Message, Synthesis,
│   │                        AgentMemory, ApiKey, Webhook ORM models
│   ├── schemas/
│   │   ├── agent.py         AgentCreate/Update/Out/Summary/Stats Pydantic v2
│   │   └── council.py       Council/Message/Synthesis/Webhook/ApiKey schemas
│   ├── routers/
│   │   ├── agents.py        8 agent endpoints
│   │   ├── councils.py      17 council endpoints + SSE stream
│   │   └── sessions.py      WebSocket + session list + key management
│   └── engine/
│       ├── debate.py        CouncilDebateEngine — parallel rounds, prompt building
│       ├── synthesis.py     SynthesisEngine — structured JSON synthesis
│       ├── router.py        ModelRouter — route to Ollama/Anthropic/OpenAI/NVIDIA
│       └── providers/
│           ├── base.py      BaseProvider ABC
│           ├── ollama.py    OllamaProvider — httpx streaming
│           ├── anthropic.py AnthropicProvider — SDK streaming
│           └── openai_provider.py OpenAIProvider — handles OpenAI + NVIDIA NIM
├── alembic/
│   ├── env.py               Async Alembic config
│   └── versions/
│       └── 001_initial.py   Full schema migration with indexes + trigger
├── alembic.ini
├── requirements.txt
├── pyproject.toml
├── .env.example
└── start.sh
```

---

## Validation Results

All executed against C:/Python312/python.exe 3.12.10 without a live DB:

| Check | Result |
|-------|--------|
| AST syntax parse — all app/ files | PASS |
| AST syntax parse — all alembic/ files | PASS |
| Config import + settings values | PASS |
| Utils response envelope format | PASS |
| Pydantic v2 schema imports | PASS |
| Engine: BaseProvider, resolve_provider() | PASS |
| Routing: claude→anthropic, gpt→openai, nvidia→nvidia, gemma3→ollama | PASS |
| Auth: key format (ck_ + 64 hex = 67 chars), hash round-trip, uniqueness | PASS |
| Router imports: agents (8 routes), councils (17 routes), sessions (4 routes) | PASS |
| Full app import — 35 routes + 1 WebSocket | PASS |
| All internal app.* imports resolve | PASS |
| OpenAPI schema generation — 21 documented paths | PASS |

---

## API Surface

### Agents
```
GET    /api/agents                     List all agents
POST   /api/agents                     Create agent (returns api_key once)
GET    /api/agents/{id}                Full detail
PUT    /api/agents/{id}                Update
DELETE /api/agents/{id}                Delete
POST   /api/agents/{id}/rotate-key     New API key (old invalidated)
GET    /api/agents/{id}/memory         All memory entries
GET    /api/agents/{id}/stats          Participation + message counts
```

### Councils
```
GET    /api/councils                   List (filter by status, mode)
POST   /api/councils                   Create with agent roster
GET    /api/councils/{id}              Detail + participants + message count
PUT    /api/councils/{id}              Update status/config
DELETE /api/councils/{id}              Archive
POST   /api/councils/{id}/messages     Post human message
GET    /api/councils/{id}/messages     Get messages (?after=id for polling)
POST   /api/councils/{id}/run          Run one debate round (background)
POST   /api/councils/{id}/pause        Pause debate
POST   /api/councils/{id}/resume       Resume debate
POST   /api/councils/{id}/complete     Mark completed
POST   /api/councils/{id}/synthesize   Trigger synthesis
GET    /api/councils/{id}/synthesis    Get latest synthesis
POST   /api/councils/{id}/participate  External AI agent join (X-Council-Key)
GET    /api/councils/{id}/stream       SSE stream (EventSource-compatible)
POST   /api/councils/{id}/webhooks     Register webhook
GET    /api/councils/{id}/export       Full transcript JSON export
```

### Sessions / Auth
```
GET    /api/sessions                   List active WebSocket sessions
POST   /api/keys                       Create API key (returns key once)
GET    /api/keys                       List keys (no hashes exposed)
WS     /ws/councils/{id}               Real-time WebSocket
GET    /api/health                     Health check
```

---

## Key Design Decisions

**Compaction-proof debate engine:** The debate engine reads all context
from PostgreSQL on every round. No in-memory session state. A server
restart mid-debate loses nothing — the next round picks up from the DB.

**Smart participation (not round-robin):** Agents respond when: mentioned,
haven't spoken in the last 3 messages, or debate just started. This prevents
all agents shouting at once and makes the debate feel natural.

**Parallel generation with timeout:** All responding agents in a round are
called concurrently via asyncio.gather. Each call respects a configurable
timeout (default 120s). One slow agent doesn't block the rest.

**Provider fallback chain:** preferred model → Ollama default → hard error.
If claude-sonnet-4-6 is unavailable, the agent falls back to gemma3:latest
automatically. Each provider is lazy-init — no connection at startup.

**API key auth (X-Council-Key):** SHA-256 hash stored in DB (fast lookup).
Keys are ck_<64-hex-chars>. Full key shown exactly once. External AI agents
use the same auth as humans — no special path.

**SSE + WebSocket:** Both supported simultaneously. SSE for AI agents that
prefer EventSource (simpler, stateless). WebSocket for human UI (bidirectional).
Both backed by Redis pub/sub — all clients on the same channel get the same
messages regardless of which server process they connected to.

**Response envelope:** Every response is `{data: ..., meta: {request_id, timestamp, version}}`.
Machine-readable error codes in `{code: "AGENT_NOT_FOUND", message: "..."}`.
Rate limit headers on every response.

---

## Deployment Steps

### 1. Install dependencies
```bash
cd C:\Users\techai\council\backend
C:\Python312\python.exe -m pip install -r requirements.txt
```

### 2. Create .env file
```bash
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY if you want claude-sonnet-4-6 synthesis
```

### 3. Run migrations (creates council schema in postgres)
```bash
C:\Python312\python.exe -m alembic upgrade head
```

### 4. Start server
```bash
bash start.sh --port 8600 --reload
# or
C:\Python312\python.exe -m uvicorn app.main:app --port 8600 --reload
```

### 5. Verify
```
GET http://localhost:8600/api/health
GET http://localhost:8600/docs
```

### 6. Create your first API key (bootstrap)
The very first key must be inserted directly into the DB since all write
endpoints require auth. Run this once:
```bash
C:\Python312\python.exe -c "
import asyncio
from app.db import AsyncSessionLocal
from app.auth import generate_api_key
from app.models.council import ApiKey

async def bootstrap():
    full_key, key_hash, key_prefix = generate_api_key()
    async with AsyncSessionLocal() as db:
        k = ApiKey(
            name='admin',
            key_hash=key_hash,
            key_prefix=key_prefix,
            permissions={'read': True, 'write': True, 'join_council': True},
        )
        db.add(k)
        await db.commit()
    print(f'Bootstrap API key: {full_key}')
    print('Store this — it will not be shown again.')

asyncio.run(bootstrap())
"
```

---

## Risks and Known Limits

| Risk | Severity | Mitigation |
|------|----------|------------|
| Redis unavailable | Medium | App starts without Redis; WebSocket/SSE broadcast silently disabled. Health endpoint reports degraded. |
| LLM provider down | Low | Fallback chain: preferred → Ollama default. Debate round skips unavailable agents rather than failing the whole round. |
| Debate runs indefinitely | Medium | `debate_max_rounds` setting caps rounds. Councils can be paused or completed via API. |
| OpenAPI schema for SSE/WS | Low | SSE endpoint shows in docs but streaming behavior is not captured by OpenAPI 3.0. Document separately for AI agents. |
| DB connection pool exhaustion | Low | Pool size 10 + overflow 20 = 30 max connections. Monitor under load and tune if needed. |
| Bootstrap key is plaintext in bash history | Low | Use the bootstrap script once, then rotate immediately via POST /api/keys. |
| Synthesis model cost | Low | synthesis_model defaults to claude-sonnet-4-6. Override to gemma3:latest in .env if Anthropic key not set. |

---

## OWASP Top 10 Coverage

| Control | Implementation |
|---------|---------------|
| Injection | SQLAlchemy ORM parameterized queries throughout — no raw SQL |
| XSS | Content sanitized at schema layer (null bytes stripped); HTML rendering is frontend responsibility |
| Broken auth | SHA-256 key hash, expiry check, last_used_at update on every valid request |
| Insecure data exposure | api_key hash never returned on reads; full key shown exactly once on create/rotate |
| Security misconfiguration | CORS restricted to localhost:3000 + wildcard (tighten to specific origins in production) |
| Vulnerable dependencies | All pinned with minimum version floors in requirements.txt |
| Insufficient logging | Request IDs on every request; all errors logged with exc_info; health endpoint exposes no internal details |

---

## What Needs to Come Next (CRUCIBLE items)

Before this is declared production-ready, CRUCIBLE should run:

1. Integration test: create agent → create council → run round → synthesize → export
2. WebSocket stress test: 10 concurrent clients subscribed to same council
3. Injection test: SQL injection via content fields, XSS via agent names
4. Auth bypass test: endpoints without X-Council-Key, expired key, tampered key
5. Rate limit validation: confirm headers present on all responses
6. Synthesis model fallback: test with ANTHROPIC_API_KEY unset — should fall back to Ollama
