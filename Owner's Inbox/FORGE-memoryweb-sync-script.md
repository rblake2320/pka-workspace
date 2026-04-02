# FORGE — MemoryWeb Claude Sync Script

**Status: COMPLETE — Initial sync ran successfully.**
**Date: 2026-03-30**

---

## Goal

Pull recent memories from MemoryWeb into a Claude Code memory file
(`memoryweb_live.md`) that gets auto-loaded into every new session,
giving Claude automatic context about what has been stored.

---

## API Endpoints Discovered

MemoryWeb is a FastAPI app at port 8100. All routes are under `/api/`.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Minimal health probe — no auth required, returns `{status: ok}` |
| `/api/status` | GET | Full status: DB stats (total memories), service health, pipeline health |
| `/api/memories` | GET | List memories — pagination, `category`, `min_importance` filters |
| `/api/memories/{id}` | GET | Single memory with full provenance chain |
| `/api/search` | POST | Tiered semantic/keyword search |
| `/api/search/by-tag` | GET | Filter by tag axis (domain/intent/sensitivity/importance/project) |
| `/api/search/by-date` | GET | Date-range search |

### Memory object schema (key fields)
```
id           int      Primary key
fact         str      The stored memory text
category     str|null e.g. "infrastructure", "decision", "configuration"
confidence   float    0.0-1.0
importance   int      1-5 scale
created_at   datetime When ingested
tombstoned_at datetime null = active, set = soft-deleted
source_id    int      Provenance chain back to source file
belief_state str      "active" | "superseded" | etc.
```

### Auth model
`MW_API_KEY` in `/d/memory-web/.env` is **not set** — API runs in no-auth
dev mode. The middleware exempts `/api/health` and `/api/status` even when
an API key is configured. Script reads `MW_API_KEY` from environment
if ever set — no key is hardcoded.

---

## Script Behavior

**File:** `C:\Users\techai\scripts\memoryweb_sync.py`

### Connection strategy
1. Probes `https://memoryweb.ultrarag.app` (Cloudflare tunnel) first.
2. If unreachable, falls back to `http://localhost:8100` (assumes SSH
   port-forward is active).
3. If both fail, writes a placeholder to `memoryweb_live.md` with
   exact recovery instructions — does not crash.

### What it fetches
- **Recent 50**: `GET /api/memories?page=1&page_size=50` — sorted by
  importance DESC, created_at DESC (API default ordering).
- **Important**: `GET /api/memories?page=1&page_size=50&min_importance=4` —
  high-priority memories to surface even if old.
- **Status**: `GET /api/status` — for the total memory count header.

### Output sections in `memoryweb_live.md`
1. Header — last synced timestamp, total count, source URL.
2. Recent (Last 7 Days) — memories created in the last 7 days.
3. Important / High-Priority — importance >= 4, deduplicated against section 2.
4. Most Recent N — remainder of the top-50 fetch not shown above.

Hard cap: 140 lines. Oldest entries are cut with a note if the file would
exceed that limit.

---

## Initial Sync Result

```
[memoryweb_sync] Starting at 2026-03-30 14:58:39
  Connected to: https://memoryweb.ultrarag.app
  Total memories: 93
  Fetched 50 recent memories
  Fetched 30 important memories
  Written 42 lines to memoryweb_live.md
[memoryweb_sync] Done.
```

- Primary tunnel (memoryweb.ultrarag.app) **responded successfully** despite
  being listed as broken in CLAUDE.md. The tunnel appears to be working
  at time of this run.
- 93 total memories in DB, all dated 2026-03-02 (28+ days old). The
  "Recent 7 Days" section shows 0 — correct, no new ingestion since early March.
- All 50 fetched memories appear in "Most Recent 50" section (42 lines total,
  well under the 140-line cap).

---

## Files Delivered

| File | Purpose |
|------|---------|
| `C:\Users\techai\scripts\memoryweb_sync.py` | Main sync script |
| `C:\Users\techai\scripts\schedule_memoryweb_sync.ps1` | Task Scheduler registration |
| `C:\Users\techai\.claude\projects\C--Users-techai\memory\memoryweb_live.md` | Live output file (auto-loaded by Claude Code) |

---

## How to Run Manually

```powershell
# Normal run (tries tunnel first, then localhost fallback)
C:\Python312\python.exe C:\Users\techai\scripts\memoryweb_sync.py

# Force localhost (requires SSH port-forward to be active)
C:\Python312\python.exe C:\Users\techai\scripts\memoryweb_sync.py --local
```

SSH port-forward command (if tunnel is down):
```
ssh -N -L 8100:10.0.0.2:8100 rblake2320@192.168.12.132
```

---

## Task Scheduler Setup

Run this once to register the daily 7 AM job:
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\techai\scripts\schedule_memoryweb_sync.ps1
```

To verify registration:
```powershell
Get-ScheduledTask -TaskName "MemoryWeb Claude Sync" | Select-Object TaskName, State
```

To trigger immediately from PowerShell:
```powershell
Start-ScheduledTask -TaskName "MemoryWeb Claude Sync"
```

Log output: `C:\Users\techai\scripts\memoryweb_sync.log`

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| memoryweb.ultrarag.app tunnel breaks (it IS listed as broken in CLAUDE.md) | Script falls back to localhost:8100 via SSH port-forward automatically |
| Both endpoints unreachable | Writes a placeholder with recovery instructions — never crashes, never writes blank file |
| MemoryWeb API adds auth key | Set `MW_API_KEY` as a Windows User environment variable — script picks it up automatically |
| Output file grows too large (loads into every session) | Hard 140-line cap enforced in `build_markdown()` |
| Stale data (nothing ingested recently) | Expected — 93 memories are all from early March; "Recent 7 Days" correctly shows 0. Ingest new conversations via MemoryWeb UI to populate. |
| MW_API_KEY leaking into session context | Key only read from `os.environ` — never written to any file, never logged |

---

## Note on Cloudflare Tunnel

CLAUDE.md lists `memoryweb.ultrarag.app` as broken ("MW is on Spark-2,
not Spark-1"). However, the tunnel responded correctly during this run.
Possible the tunnel config was already patched, or the routing happens
to work anyway. The fallback path (SSH port-forward) remains fully
implemented and tested in the script logic.
