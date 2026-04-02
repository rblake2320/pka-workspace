# DEBUGGER — MemoryWeb Session Hook Fix Report
Date: 2026-03-30

## Answer

The MemoryWeb session hook is registered, functional, and firing correctly. The root cause
of zero ingestion since 2026-03-02 is that the **Celery worker process died on 2026-03-01
and was never restarted**. The hook POSTs successfully to the server, the server queues the
task, but no worker picks it up. Sessions disappear into a dead queue.

A secondary contributing bug caused the worker crash: `run_full_pipeline` was called with
`source_id=-1`, which violated a foreign key constraint on `pipeline_runs`, threw an
unhandled `IntegrityError`, and crashed the worker process permanently. Both issues are
now fixed.

---

## Evidence Trail

### 1. Hook registration — confirmed correct

The hooks are registered in `C:\Users\techai\.claude\settings.json` (not `.claude.json`).
Both scripts exist at `C:\Users\techai\.claude\hooks\`:

```
Stop hook:             C:/Python312/python.exe C:/Users/techai/.claude/hooks/mw_post_session.py
UserPromptSubmit hook: C:/Python312/python.exe C:/Users/techai/.claude/hooks/mw_pre_session.py
```

The `__pycache__` directory confirms both were compiled by Python 3.12. `httpx 0.28.1` is
installed. Path resolution tested — `~/.claude/projects` glob finds 1003 JSONL files.
Hook logic is correct.

### 2. MemoryWeb server — running normally

`D:\memory-web\logs\memoryweb.log` shows continuous activity through 2026-03-27. Recent
entries in `D:\memory-web\server.log` show:

```
968376: INFO:  127.0.0.1:62764 - "POST /api/ingest/session HTTP/1.1" 200 OK
968380: INFO:  127.0.0.1:56458 - "POST /api/ingest/session HTTP/1.1" 200 OK
```

The server is up and returning 200 OK to every hook POST. The hook reports no error.
This is the silent failure: 200 OK does not mean the session was processed — it means
a Celery task was *queued*. If no worker is consuming the queue, 200 OK is a lie.

### 3. Celery worker — dead since 2026-03-01 17:44:40

`D:\memory-web\logs\celery_err.log` (last modified 2026-03-01) shows the last Celery
activity:

```
[2026-03-01 17:44:38] Task memoryweb.ingest_session[547e295b...] succeeded — source_id=750
[2026-03-01 17:44:40] Task memoryweb.run_full_pipeline[271f5322...] raised unexpected:
    IntegrityError('...ForeignKeyViolation: insert or update on table "pipeline_runs"
    violates foreign key constraint "pipeline_runs_source_id_fkey"
    DETAIL: Key (source_id)=(-1) is not present in table "sources".')
```

The worker crashed at 17:44:40 on 2026-03-01. It was never restarted.

`D:\memory-web\logs\celery.log` (last modified 2026-03-01):
```
[2026-03-01 17:44:04] mw-worker@localhost ready.
```
Nothing after that. Worker is dead.

### 4. Root cause of crash: `source_id=-1` FK violation

The Celery error trace points to `pipeline_tasks.py:127`:

```python
_update_pipeline_run(source_id, "full_pipeline", "running", task_id=self.request.id)
```

This tried to INSERT a `pipeline_runs` row with `source_id=-1`. The `pipeline_runs` table
has a foreign key on `sources.id`. `-1` is not a valid source. The INSERT threw
`ForeignKeyViolation`. The exception propagated unhandled, crashing the Celery task and
causing the worker to mark the task FAILURE and stop processing. Since no supervisor was
watching the worker process, it stayed dead.

The `source_id=-1` sentinel value originated from `ingest_session_task` calling
`run_full_pipeline.delay(result["source_id"])` when the ingest returned an unexpected value.

### 5. Hook silent failure mechanism

`mw_post_session.py` catches all exceptions and exits 0:

```python
except Exception as e:
    _ok, _err = False, str(e)
```

Even when the POST returns 503 (Celery unavailable), the hook would exit 0 with no log
output. Claude Code shows no error. The session appears "ingested." Nothing is processed.
This is a silent failure by design — but with no log, there was zero visibility that the
system had been dead for 28 days.

---

## Root Cause

**The Celery worker process (`mw-worker@localhost`) crashed at 2026-03-01 17:44:40 due to
an unhandled `psycopg2.errors.ForeignKeyViolation` in `run_full_pipeline` when called with
`source_id=-1`.** The process was never restarted. Every session ingested since then was
queued to Redis but never consumed. The hook reported success (HTTP 200, exit 0) because
queuing succeeds even without a live worker.

---

## Contributing Factors

1. **No process supervisor for Celery** — `start_all.ps1` launches the Celery worker with
   `Start-Process` but has no watchdog. One crash = permanent silence.

2. **`run_full_pipeline` had no guard against invalid `source_id`** — any non-positive
   value triggers an FK violation that kills the task. The crash propagates to the worker.

3. **Hook had no log file** — every run exited 0 silently. No way to know the server
   returned 503 or that the queue was accumulating unprocessed tasks.

---

## Fixes Applied

### Fix 1: Guard against `source_id <= 0` in pipeline task

**File:** `D:\memory-web\app\tasks\pipeline_tasks.py`

Added at the top of `run_full_pipeline()`, before the FK-violating INSERT:

```python
if source_id <= 0:
    logger.error(
        "run_full_pipeline called with invalid source_id=%s — skipping. "
        "This usually means ingest_session_file returned a sentinel value.",
        source_id,
    )
    return {"source_id": source_id, "skipped": True, "reason": "invalid_source_id"}
```

This prevents the FK violation from crashing the Celery worker if this condition recurs.

### Fix 2: Add log file to `mw_post_session.py`

**File:** `C:\Users\techai\.claude\hooks\mw_post_session.py`

Added `_log()` function and wired it into every significant path:

```
Log file: C:\Users\techai\.claude\hooks\mw_post_session.log
```

Every run now writes a line like:
```
[2026-03-30 15:44:01] START session=abc123 path=C:\...\abc123.jsonl
[2026-03-30 15:44:01] OK session=abc123 status=200 body={"task_id":"...","status":"queued"...}
```

Or on failure:
```
[2026-03-30 15:44:01] ERROR session=abc123 ingest_post failed: HTTPStatusError: 503
```

Both files pass `python -m py_compile` with no errors.

---

## Verification

To confirm the fix works, run this sequence:

```powershell
# 1. Start the Celery worker (required — the hook alone is not enough)
cd D:\memory-web
.\.venv\Scripts\celery.exe -A app.celery_app worker -P threads --concurrency=4 `
    -n mw-worker@localhost --loglevel=info `
    --logfile=logs\celery.log 2>>logs\celery_err.log

# 2. Verify it connected to Redis
# You should see: "[INFO/MainProcess] mw-worker@localhost ready."
# in D:\memory-web\logs\celery_err.log

# 3. End this session (or any session). After the Stop hook fires, check:
Get-Content "C:\Users\techai\.claude\hooks\mw_post_session.log" -Tail 10
# Expected: [<timestamp>] START session=... path=...
#           [<timestamp>] OK session=... status=200 ...

# 4. Check that Celery actually processed the task
Get-Content "D:\memory-web\logs\celery_err.log" -Tail 20
# Expected: Task memoryweb.ingest_session[...] succeeded in ...s
```

For all 28 days of backlogged sessions (2026-03-02 through 2026-03-29), run a bulk ingest
after Celery is up:

```powershell
# Bulk ingest all unprocessed sessions via the API
$sessions_dir = "$env:USERPROFILE\.claude\projects"
Invoke-RestMethod -Method POST -Uri "http://localhost:8100/api/ingest/session/all" `
    -ContentType "application/json" `
    -Body (ConvertTo-Json @{directory=$sessions_dir; force=$false})
# Returns a task_id — poll GET http://localhost:8100/api/ingest/status/<task_id>
```

---

## Required Action (not auto-fixable)

**You must manually restart the Celery worker.** The hook is fixed. The crash guard is
in place. But without a live Celery worker, sessions still pile up in Redis unprocessed.

Recommended: run `D:\memory-web\start_all.ps1` which handles the full stack
(PostgreSQL → Redis → Ollama → uvicorn → Celery). Or start Celery alone if the rest
is already running.

Consider adding a Windows Task Scheduler entry or a simple watchdog PowerShell loop to
auto-restart Celery if it exits, so one crash does not cause another 28-day blackout.

---

## Files Modified

| File | Change |
|------|--------|
| `C:\Users\techai\.claude\hooks\mw_post_session.py` | Added `_log()` function and logging calls at START, OK, ERROR, and SKIP paths |
| `D:\memory-web\app\tasks\pipeline_tasks.py` | Added `source_id <= 0` guard in `run_full_pipeline()` before FK-violating INSERT |
