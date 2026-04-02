# FORGE — MemoryWeb MCP Server

**Status: SHIPPED. All 5 tools tested live against 4,002 memories. Server passes every validation step.**

---

## 1. Goal

Give Claude Code live, on-demand access to Ron's MemoryWeb instance (1,147+ memories now 4,002 active) via MCP tools. Every conversation can now query, search, and add memories without copy-pasting context.

---

## 2. API Schema Discovered

**Base URL:** `https://memoryweb.ultrarag.app` (Cloudflare tunnel) / `http://localhost:8100` (fallback)

**Authentication:** Optional `X-API-Key` header. The running instance has no key set (`MW_API_KEY` is empty = open access). Set `MEMORYWEB_API_KEY` env var when auth is enabled.

### Endpoints Used

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/status` | Stats: memory count, service health, pipeline health |
| `GET` | `/api/memories` | Paginated memory list, ordered by importance DESC + created_at DESC |
| `POST` | `/api/search` | Tiered semantic search (Tier 1 keyword → Tier 2 FTS → Tier 3 vector) |
| `GET` | `/api/search/by-tag` | Tag axis/value filtered search |
| `POST` | `/api/ingest/upload` | Multipart upload of a `.jsonl` session file to create memories |

### Memory Object (key fields)

```
id            int       Primary key
fact          str       The memory content
category      str       Synthesized category (decision, solution, observation...)
importance    int 1-5   Importance score
confidence    float     Confidence 0.0-1.0
created_at    datetime  Creation timestamp (ISO 8601)
tombstoned_at datetime  Null = active; set = soft-deleted
source_id     int       Which ingest source created this memory
belief_state  str       "active" | "superseded" | "invalidated"
```

### Search Request/Response (key fields)

```
POST /api/search
{
  "query": "string",        // required
  "k": 10,                  // result count 1-100
  "filters": {},            // optional: {domain, project, date_from, date_to, ...}
  "include_tombstoned": false
}

Response:
{
  "total": int,
  "results": [{
    "result_type": "memory|segment|message",
    "id": int,
    "content": str,
    "score": float,
    "tier": 1|2|3,
    "tags": [...]
  }],
  "tiers_used": [1, 2, 3],
  "latency_ms": float
}
```

---

## 3. Files Delivered

| File | Purpose |
|------|---------|
| `C:\Users\techai\mcp-hub\memoryweb-mcp\server.py` | MCP server (5 tools) |
| `C:\Users\techai\mcp-hub\memoryweb-mcp\requirements.txt` | Dependencies |
| `C:\Users\techai\mcp-hub\memoryweb-mcp\test_server.py` | Standalone test harness |
| `C:\Users\techai\.claude.json` | Updated — `memoryweb` MCP entry added |

---

## 4. Tools Implemented

### `search_memories(query, limit=10, tags=[])`
Tiered semantic search (Tier 1 keyword → Tier 2 FTS → Tier 3 vector embeddings). Optional tag filter. Returns ranked results with score, tier, category, importance, and timestamp.

**Example usage from Claude Code:**
```
Use search_memories to find what I know about the Council debate platform
search_memories("council debate", limit=5)
```

### `get_recent_memories(days=7, limit=20)`
Fetches the most recent memories sorted by importance then creation date. Filters client-side to the requested day window.

**Example:**
```
get_recent_memories(days=14, limit=10)
```

### `get_memories_by_tag(tags=["domain:ai"], limit=20)`
Tag format: `"axis:value"` (e.g. `"domain:ai"`, `"project:council"`). Pass bare value for domain axis. Returns deduplicated results across all tags.

**Example:**
```
get_memories_by_tag(["project:council", "domain:agents"])
```

### `add_memory(content, tags=[], importance=3)`
Injects content as a Claude Code session JSONL record via `/api/ingest/upload`. The memory enters the synthesis pipeline and appears in ~30-60 seconds after pipeline processing.

**Example:**
```
add_memory("Decided to use PostgreSQL for the Council platform", importance=4)
```

### `get_memory_stats()`
Returns total memory count, pipeline health, embedding coverage, and service health (postgres, pgvector, redis, ollama, celery).

---

## 5. Live Test Results (2026-03-30)

```
get_memory_stats      -> 4002 active memories, 97.2% embedding coverage, all services OK
get_recent_memories   -> 5 memories returned, correctly filtered to last 30 days
search_memories       -> "AI army project status" returned 5 relevant results in 94ms
search_memories+tag   -> "council debate platform" w/ project tag returned 3 results
get_memories_by_tag   -> ["domain:ai", "project:council"] returned 6 deduplicated results
add_memory            -> task_id=f0f7a55c-bd3a-4853-b28b-024a144654af, status=queued
```

All 5 tools: PASS. Zero crashes. Zero unhandled exceptions.

---

## 6. Registration in Claude Code

Entry added to `~/.claude.json` under `projects["C:/Users/techai"]["mcpServers"]`:

```json
"memoryweb": {
  "type": "stdio",
  "command": "C:\\Python312\\python.exe",
  "args": ["C:\\Users\\techai\\mcp-hub\\memoryweb-mcp\\server.py"],
  "env": {
    "MEMORYWEB_URL": "https://memoryweb.ultrarag.app",
    "MEMORYWEB_FALLBACK": "http://localhost:8100"
  }
}
```

**To activate:** Restart Claude Code (close and reopen). The `memoryweb` server will auto-start as a subprocess. Check with `/mcp` command — should list `memoryweb` with 5 tools.

---

## 7. How to Use From Claude Code

Once active, Claude Code can use the tools directly:

```
# In any Claude Code conversation:
Search my memories for anything about the Council project
Get recent memories from the last week
Add a memory: "Decided to migrate Council to a dedicated VPS in April 2026"
Show me memory stats
```

Or explicitly invoke:
```
mcp__memoryweb__search_memories("AgentForge architecture decisions", limit=10)
mcp__memoryweb__get_recent_memories(days=7)
mcp__memoryweb__get_memory_stats()
```

---

## 8. Risks and Failure Modes

| Risk | Severity | Mitigation |
|------|----------|------------|
| memoryweb.ultrarag.app tunnel down | Medium | Auto-fallback to `http://localhost:8100` (Spark-2 direct via SSH tunnel) |
| MemoryWeb on Spark-2, not port-forwarded | Medium | Tunnel fix in progress (CLAUDE.md notes this); fallback gracefully returns error string, server does not crash |
| `add_memory` latency (pipeline ~30-60s) | Low | Tool confirms queued with task_id; user expectation set in response |
| Tag filter behavior (by-tag always queries "domain" axis by default) | Low | Known — documented in tool docstring; pass `"axis:value"` format to target other axes |
| API key not set in env | Low | Server works with no key (current state); if MW_API_KEY set in future, add to claude.json env block |
| Search score=0.01 on tier-2 results | Info | This is MemoryWeb's score normalization for FTS (BM25) results — not a bug |

---

## 9. Deployment Notes

**Dependencies already installed:** `mcp`, `httpx`, `pydantic` are all present in `C:\Python312`.

**To re-test at any time:**
```
cd C:\Users\techai\mcp-hub\memoryweb-mcp
C:\Python312\python.exe test_server.py
```

**To test with Cloudflare URL specifically:**
```
set MEMORYWEB_URL=https://memoryweb.ultrarag.app
C:\Python312\python.exe test_server.py
```

**If the Cloudflare tunnel for memoryweb gets fixed** (CLAUDE.md notes it's broken — MW is on Spark-2, tunnel points to Spark-1): The server will automatically use the primary URL. No config change needed.

**To add API key auth** (if MW_API_KEY is set on the server in the future):
Edit `~/.claude.json` and add to the `env` block:
```json
"MEMORYWEB_API_KEY": "your-key-here"
```

---

## 10. Architecture Notes for GRID

- Server uses `mcp.server.fastmcp.FastMCP` (built into the installed `mcp` package, not the broken standalone `fastmcp` package)
- Transport: stdio subprocess — Claude Code spawns it as a child process
- All HTTP calls are synchronous (`httpx` sync client) — FastMCP handles concurrency at the MCP protocol layer
- Primary → fallback retry on every call: if primary URL fails, fallback is tried before returning an error
- Tool responses hard-capped at 1,900 chars with `[truncated]` marker
- No state held in process memory — each tool call is a fresh HTTP request
- Server starts cleanly even if MemoryWeb is down (tested: import succeeds, tools return error strings)
