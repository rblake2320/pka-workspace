# FORGE — AI Army Flywheel Priority 2 + 3 Deployed

**Date:** 2026-03-27
**Status:** DEPLOYED — dry-run monitoring active, NOT yet started via systemd

---

## Priority 2: Chat Watcher systemd Service

### What was found
Two instances of chat_watcher_v3.py were already running manually:
- PID 39115 — `/usr/bin/python3` (system python, started ~01:46 UTC)
- PID 68733 — `/home/rblake2320/miniconda3/bin/python` (miniconda, started ~01:54 UTC)

Both running `--agent CC-Spark1`. The duplicate is a risk (two watchers processing
the same chat messages = double-action). This is pre-existing, not caused by this deploy.

**The systemd service is NOT started** — per SENTINEL rule (connection protocol requires
24h dry-run monitoring before live). Starting it now while two manual instances are already
running would create a third instance. Action required from you before start (see below).

### Unit file deployed
**Path:** `/etc/systemd/system/chat-watcher.service`
**Status:** `enabled` (will auto-start on next reboot, safe because manual instances
won't survive a reboot)

```ini
[Unit]
Description=AI Army Chat Watcher v3
After=network.target
Wants=network.target

[Service]
Type=simple
User=rblake2320
WorkingDirectory=/home/rblake2320/ai-business/shared
Environment="PYTHONUNBUFFERED=1"
Environment="HOME=/home/rblake2320"
ExecStartPre=/bin/bash -c 'rm -f /home/rblake2320/ai-business/shared/locks/watcher.pid'
ExecStart=/usr/bin/python3 /home/rblake2320/ai-business/shared/chat_watcher_v3.py --agent CC-Spark1
Restart=always
RestartSec=30
StartLimitBurst=5
StartLimitIntervalSec=300
StandardOutput=append:/home/rblake2320/ai-business/logs/chat-watcher.log
StandardError=append:/home/rblake2320/ai-business/logs/chat-watcher.log

[Install]
WantedBy=multi-user.target
```

### To go live (when ready)
```bash
# Step 1: Kill both manual instances
ssh rblake2320@192.168.12.132 "kill 39115 68733"

# Step 2: Start via systemd (now the only instance)
ssh rblake2320@192.168.12.132 "sudo systemctl start chat-watcher"

# Step 3: Verify
ssh rblake2320@192.168.12.132 "sudo systemctl status chat-watcher"
```

**Logs will be at:** `~/ai-business/logs/chat-watcher.log`

---

## Priority 3: Escalation Feedback Loop

### Script deployed
**Path:** `/home/rblake2320/ai-business/escalation_monitor.py`
**Mode:** Dry-run (cron running every 5 min, logging only, not writing to chat)

### How it works
1. Scans `~/ai-business/shared/escalations/` for files not yet in the processed DB
2. Dry-run: logs what it would post (no writes to chat)
3. Live mode (`ESCALATION_MONITOR_ENABLED=true`): writes a resolution message to
   `~/ai-business/shared/chat/YYYYMMDD_HHMMSS_escalation-monitor.md`
4. Tracks processed files in `~/ai-business/logs/escalations_processed.txt`
5. Lockfile at `/tmp/escalation_monitor.lock` prevents overlapping cron runs
6. Log at `~/ai-business/logs/escalation_monitor.log`

### Chat message format (matches existing chat dir convention)
```
# [FROM: escalation-monitor] [TO: All]
**Time:** 2026-03-27T11:25:08Z
**Subject:** Escalation resolved — <filename>
**MSG_ID:** ESC_<8-char-hex>

---

Ron responded to escalation: `<filename>`

**Content:**
<file content>

---

This escalation is now resolved. Agents may proceed on any blocked work.
```

### Cron entry added
```
*/5 * * * * ESCALATION_MONITOR_ENABLED=false /usr/bin/python3 /home/rblake2320/ai-business/escalation_monitor.py >> /home/rblake2320/ai-business/logs/escalation_monitor.log 2>&1
```

### Validation test results
```
2026-03-27 06:25:08 [INFO] escalation_monitor starting [mode=DRY-RUN]
2026-03-27 06:25:08 [INFO] New escalation file detected: TEST_20260327_forge_validation.md
2026-03-27 06:25:08 [INFO] [DRY-RUN] Would post to chat: 20260327_112508_escalation-monitor.md
[DRY-RUN] Content preview: # [FROM: escalation-monitor] [TO: All] ...
2026-03-27 06:25:08 [INFO] escalation_monitor done [mode=DRY-RUN] new=1 errors=0

# Second run (idempotency check):
2026-03-27 06:25:20 [INFO] escalation_monitor starting [mode=DRY-RUN]
2026-03-27 06:25:20 [INFO] escalation_monitor done [mode=DRY-RUN] new=0 errors=0
```

Confirmed: detects new files, logs correctly, skips already-processed files,
writes nothing to chat in dry-run. Test file cleaned up. Processed DB reset to empty.

### To go live
```bash
# Edit the crontab line — change false to true:
ssh rblake2320@192.168.12.132 "crontab -l | sed 's/ESCALATION_MONITOR_ENABLED=false/ESCALATION_MONITOR_ENABLED=true/' | crontab -"

# Or test manually in live mode:
ssh rblake2320@192.168.12.132 "ESCALATION_MONITOR_ENABLED=true /usr/bin/python3 /home/rblake2320/ai-business/escalation_monitor.py"
```

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Two watcher instances currently running | Medium | Unit is enabled but NOT started. Kill manual instances before `systemctl start`. |
| Watcher script named `v3` but header says `v4` | Low | Script content is v4. Unit file ExecStart path is correct (`chat_watcher_v3.py` is the filename). |
| Escalation monitor cron log grows unbounded | Low | Rotate with logrotate or add `tail -c 10M` to log path if it becomes large. |
| `/tmp/escalation_monitor.lock` survives reboot only until next boot | None | Correct behavior — lock is per-run, not persistent. |
| `escalations_processed.txt` records absolute paths — safe to delete and reset | Low | If you move the escalations dir, clear `escalations_processed.txt` and files will be reprocessed. |

---

## Files Deployed on Spark-1
- `/etc/systemd/system/chat-watcher.service` — unit file, enabled
- `/home/rblake2320/ai-business/escalation_monitor.py` — escalation monitor script
- `/home/rblake2320/ai-business/logs/escalation_monitor.log` — created on first run
- `/home/rblake2320/ai-business/logs/escalations_processed.txt` — tracking DB (currently empty)
