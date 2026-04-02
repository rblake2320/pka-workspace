# FORGE Deliverable: NLF Queue Consumer — Priority 1 AI Army Flywheel

**Date**: 2026-03-27
**Status**: DEPLOYED + VALIDATED (dry-run confirmed)
**Script**: `/home/rblake2320/ai-business/nlf_queue_consumer.py`

---

## Goal

Consume NLF correction JSON files written by `chat_watcher_v3.py` and feed them
into the training pipeline. Runs safely as a read-only dry-run by default — no
training data is touched until you flip one env var.

---

## What Was Built

### Field Mapping (discovered by inspecting live data)

The NLF queue JSON schema (from `nlf_harvest()` in `chat_watcher_v3.py`):
```
correction_id   → traceability key
craig_file      → source chat filename
craig_message   → the correction text (truncated at 2000 chars by watcher)
subject         → thread subject (used as the instruction prompt)
matched_patterns → which NLF regex patterns fired
created_at      → UTC ISO timestamp
exported        → int flag (0 = not yet consumed)
```

Training JSONL output format (matches `nlf_corrections_v1.jsonl`):
```json
{
  "instruction": "<subject line or first line of craig_message>",
  "response": "<craig_message text>",
  "source": "nlf_queue",
  "correction_id": "<id>",
  "created_at": "<iso>",
  "matched_patterns": [...]
}
```

The `instruction` is the `subject` field when it is meaningful (>10 chars).
Fallback is the first line of `craig_message` itself. This is accurate:
the subject is what Craig is correcting the AI about, and the message is
what the correct answer should look like.

---

## Architecture

```
chat_watcher_v3.py
  → writes nlf_*.json to ~/ai-business/shared/chat/.nlf_queue/

nlf_queue_consumer.py  (cron: hourly)
  → reads .nlf_queue/*.json
  → validates required fields: correction_id, craig_message, created_at
  → converts each to {"instruction":..., "response":...} + trace fields
  → DRY-RUN (default): logs what it would do, writes nothing
  → LIVE mode: appends to training_log.jsonl, moves files to .nlf_queue/processed/
  → lockfile: /tmp/nlf_consumer.lock  (no concurrent runs)
  → log: ~/ai-business/logs/nlf_consumer.log
```

---

## Deployed Files

| Path | Purpose |
|------|---------|
| `/home/rblake2320/ai-business/nlf_queue_consumer.py` | Main consumer script |
| `/home/rblake2320/ai-business/shared/chat/.nlf_queue/processed/` | Archive dir for consumed files |
| `/home/rblake2320/ai-business/logs/` | Already existed — log dir |
| Crontab entry (hourly) | See below |

---

## Cron Entry Installed

```
0 * * * * NLF_CONSUMER_ENABLED=false /usr/bin/python3 /home/rblake2320/ai-business/nlf_queue_consumer.py >> /home/rblake2320/ai-business/logs/nlf_consumer.log 2>&1
```

Runs at the top of every hour. Dry-run mode until you enable it.

---

## Manual Test Run Output (dry-run, synthetic file injected)

```
2026-03-27T06:25:13 [INFO] === nlf_queue_consumer start [mode=DRY-RUN] ===
2026-03-27T06:25:13 [INFO] Found 1 pending file(s) in queue.
2026-03-27T06:25:13 [INFO] [DRY-RUN] nlf_1774610709_43461f18.json →
    instruction='How many products are in the TimeWise Miracle Set 3D?'
    response_len=84
2026-03-27T06:25:13 [INFO] === DRY-RUN: would process 1 corrections, would skip 0 ===
2026-03-27T06:25:13 [INFO] DRY-RUN: no writes made. Set NLF_CONSUMER_ENABLED=true to go live.
```

Post-run verification:
- Test file remained in queue (not moved)
- `processed/` directory remained empty
- `training_log.jsonl` last entry still shows Jan 25 timestamp (unchanged)

---

## How to Go Live

When you are ready to start feeding corrections into training:

```bash
ssh rblake2320@192.168.12.132
# One-shot live run:
NLF_CONSUMER_ENABLED=true python3 ~/ai-business/nlf_queue_consumer.py

# Switch cron to live mode:
crontab -e
# Change NLF_CONSUMER_ENABLED=false  →  NLF_CONSUMER_ENABLED=true
```

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Corrupt JSON in queue | try/except on every file — skip + log, continue |
| Missing required fields | validate before convert — skip + log |
| Concurrent cron runs | /tmp/nlf_consumer.lock with LOCK_EX\|LOCK_NB — second run exits immediately |
| Training log corruption | Opens in append mode only, writes one JSONL line per entry |
| Accidental live mode | Default env var is "false" — must explicitly set "true" |
| subject field absent | Fallback to first line of craig_message — always produces a valid instruction |
| queue dir not yet created | Checked at runtime — exits cleanly with "nothing to do" |

---

## What Happens with Real Craig Corrections

When `chat_watcher_v3.py` detects Craig's correction patterns and writes a queue
file, the next hourly cron run will log the conversion in dry-run mode. You will
see entries in `~/ai-business/logs/nlf_consumer.log` like:

```
[DRY-RUN] nlf_1774600000_abc12345.json →
    instruction='<subject of the thread>'
    response_len=<N>
DRY-RUN: would process N corrections, would skip M
```

Nothing enters training_log.jsonl until `NLF_CONSUMER_ENABLED=true`.
