# FORGE Deliverable: AI Army Flywheel — Priorities 4 & 5
**Date:** 2026-03-27
**Status:** P4 partially fixed (cron corrected, deeper bug documented) | P5 complete and running

---

## Priority 4: Agent Chat → MemoryWeb Ingest

### What Was Found

**MemoryWeb on Spark-1 is a separate live instance** — not the Windows PC instance.
`~/memory-web/` on Spark-1 runs its own FastAPI + Celery stack on `localhost:8100`.
The Windows PC MemoryWeb at `192.168.12.198:8100` is also reachable from Spark-1
(verified: HTTP 200). These are two independent deployments.

**The cron entry had two bugs:**

| Bug | Old Value | Impact |
|-----|-----------|--------|
| Wrong directory | `/data/shared-chat` (does not exist) | `iter_shared_chat_files` logged a warning and returned empty every run |
| Wrong log path | `/tmp/mw_chat_ingest.log` | Log lost on reboot, not in `~/ai-business/logs/` with other service logs |

**The `/ingest/shared-chat` endpoint exists and works** — it's properly implemented in
`~/memory-web/app/routers/ingest.py`, dispatches to Celery, and the Celery worker is
healthy (1 worker confirmed). The endpoint returns `status: queued` correctly.

**Existing MemoryWeb DB state on Spark-1 (confirmed via `/api/status`):**

```
sources:       18,592
conversations: 23,040
messages:   9,239,781  (from other ingest sources, not shared_chat)
```

The 9.2M messages came from other source types (not shared_chat). The shared_chat
ingest was never successfully processing files.

### What Was Fixed

The cron entry was corrected to point at the real chat directory and log to the
standard log location:

**Before:**
```
*/30 * * * * curl -s -X POST http://localhost:8100/api/ingest/shared-chat \
  -d "{\"directory\": \"/data/shared-chat\", ...}" >> /tmp/mw_chat_ingest.log 2>&1
```

**After:**
```
*/30 * * * * curl -s -X POST http://localhost:8100/api/ingest/shared-chat \
  -d "{\"directory\": \"/home/rblake2320/ai-business/shared/chat\", \"force\": false}" \
  >> /home/rblake2320/ai-business/logs/mw_chat_ingest.log 2>&1
```

### Remaining Issue — Celery Timeout on 514k Files

After the directory fix, test runs returned `{"batches": 0, "conversations": 0, "messages": 0}`
even though `/home/rblake2320/ai-business/shared/chat` contains **514,074 .md files**.

**Root cause:** `batch_parse_shared_chat()` calls `Path(directory).rglob("*.md")` which
must enumerate all 514k files before yielding the first batch. At ~514k entries, this
rglob blocks the Celery worker thread for longer than the task times out. The task
completes with `status: SUCCESS` but zero batches processed.

**Confirmed:** `python3 -c "from pathlib import Path; list(Path('/home/rblake2320/ai-business/shared/chat').rglob('*.md'))"` ran locally and found 514,074 files — rglob itself works but is slow at this scale.

**Action required (not in scope of this task — flagging for GRID/FORGE follow-up):**

The ingest service needs a streaming approach for large directories:

Option A — Date-windowed ingest: Pass `since_date` parameter, pre-filter files by
`mtime` before rglob using `os.scandir()` instead of `rglob`. The cron already runs
every 30 minutes — only new files since last run need processing.

Option B — Archive-first pattern: The 170k archived files should be permanently
excluded. Only ingest from the active (non-archive) subdirectory. The cron command
already sends the chat dir root — pointing it at a `pending/` subdir that only holds
recent unprocessed files would fix the scale problem.

Option C — Patch `iter_shared_chat_files` to accept a `max_age_hours` param and use
`os.scandir` + `os.stat` to skip old files before building the list.

The cron fix is deployed and correct. The ingest will start working once the
scale issue is addressed. Without the fix, it was guaranteed to do nothing
(wrong directory). With the fix, it will at least attempt the real directory.

---

## Priority 5: Evidence Stats Automation

### Deployed

**Script:** `/home/rblake2320/ai-business/evidence_stats.sh`
**Output:** `/home/rblake2320/ai-business/shared/evidence_stats.json` (readable by all agents)
**Log:** `/home/rblake2320/ai-business/logs/evidence_stats.log`
**Schedule:** Every 6 hours (`0 */6 * * *`)

### First Run Output (2026-03-27T11:25:41Z)

```json
{
  "generated_at": "2026-03-27T11:25:41Z",
  "chat_files_active": 343314,
  "chat_files_archived": 170727,
  "chat_files_total": 514041,
  "nlf_queue_pending": 1,
  "nlf_queue_processed": 0,
  "escalations_open": 0,
  "active_heartbeat_agents": 4,
  "oldest_message_date": "2025-12-28+23:13:47.4602087360",
  "newest_message_date": "2026-03-27+06:25:37.5701560910"
}
```

**What these numbers mean:**
- 514k total chat files: 343k active + 170k archived. This is the full AI Army interaction history.
- NLF queue: 1 pending job, 0 processed — NLF consumer is still disabled (`NLF_CONSUMER_ENABLED=false`)
- Escalations: 0 open — clean state
- Heartbeat agents: 4 active agents reporting in
- Date range: Dec 28 2025 to Mar 27 2026 — ~3 months of continuous operation

---

## Final Crontab (complete listing)

```
*/2 * * * * /home/rblake2320/ai-army-os/keep_tunnel_vps.sh
*/5 * * * * /home/rblake2320/ai-army-os/keep_coder.sh
0 6 * * * bash ~/aihangout-harvester/run_harvest.sh
15 * * * * /usr/bin/python3 /home/rblake2320/ai-business/scripts/aihangout_agents.py >> /home/rblake2320/ai-business/logs/aihangout_agents_cron.log 2>&1
*/30 * * * * curl -s -X POST http://localhost:8100/api/ingest/shared-chat -H "Content-Type: application/json" -d "{\"directory\": \"/home/rblake2320/ai-business/shared/chat\", \"force\": false}" >> /home/rblake2320/ai-business/logs/mw_chat_ingest.log 2>&1
0 */6 * * * bash /home/rblake2320/backup_patent_data.sh >> /tmp/patent_backup_cron.log 2>&1
*/5 * * * * bash /home/rblake2320/current_state_generator.sh --once >> /tmp/current_state.log 2>&1
*/5 * * * * bash /home/rblake2320/gen_current_state.sh >> /tmp/state_gen.log 2>&1
*/5 * * * * ESCALATION_MONITOR_ENABLED=false /usr/bin/python3 /home/rblake2320/ai-business/escalation_monitor.py >> /home/rblake2320/ai-business/logs/escalation_monitor.log 2>&1
0 * * * * NLF_CONSUMER_ENABLED=false /usr/bin/python3 /home/rblake2320/ai-business/nlf_queue_consumer.py >> /home/rblake2320/ai-business/logs/nlf_consumer.log 2>&1
0 */6 * * * bash /home/rblake2320/ai-business/evidence_stats.sh >> /home/rblake2320/ai-business/logs/evidence_stats.log 2>&1
```

---

## Risk Register

| Risk | Severity | Status |
|------|----------|--------|
| shared_chat ingest still returns 0 results due to rglob scale | High | Open — needs Option A/B/C fix above |
| 514k files in flat chat dir will grow unbounded | Medium | Existing archive job runs — OK short term |
| NLF consumer disabled — 1 pending job will never process | Low | Intentional (`NLF_CONSUMER_ENABLED=false`) |
| evidence_stats.sh `find -printf` may not work if non-GNU find installed | Low | Tested on Spark-1, works correctly |

---

## Files Deployed on Spark-1

- `/home/rblake2320/ai-business/evidence_stats.sh` (executable)
- `/home/rblake2320/ai-business/shared/evidence_stats.json` (first run output)
- `/home/rblake2320/ai-business/logs/evidence_stats.log` (cron log)
- Crontab updated (11 active jobs, was 10)
