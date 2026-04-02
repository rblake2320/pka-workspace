# SENTINEL Risk Review — Flywheel Connection Implementations
**Review Date**: 2026-03-27
**Reviewer**: SENTINEL
**Scope**: P1–P5 flywheel connections pre-deployment to Spark-1 AI Army production system
**SSH Access at Review Time**: UNAVAILABLE (Spark-1 unreachable) — flagged as finding

---

## What Was Tested

Static design review of all 5 implementations as specified in the brief. Live source code
could not be read because SSH to Spark-1 (192.168.12.132) was unavailable at review time.
This is noted as a hard constraint on review completeness — see Required Fixes section.

Included in scope:
- Data flow correctness and failure mode analysis for each implementation
- Kill switch adequacy
- Dry-run mode reliability
- Inter-component cascade and loop risks
- Cron accumulation and resource contention
- IO load on an active GPU/training system

Excluded from scope:
- Live code audit (SSH unavailable — must be performed before GO)
- Integration testing (not yet deployed)
- MemoryWeb reachability from Spark-1 (network access not verified)

---

## What Passed

**P1 — NLF Queue Consumer design is sound.**
Queue-sits-unprocessed failure mode is graceful and correct for a training pipeline.
Lockfile at `/tmp/nlf_consumer.lock` prevents concurrent hourly cron runs.
Kill switch `NLF_CONSUMER_ENABLED` is properly scoped.
Dry-run-first approach is correctly sequenced.
Data flow (queue JSON → JSONL append) is one-directional with no feedback loop back to chat.

**P5 — Evidence Stats data flow is correct in design.**
The script is read-only on the chat directory. Writes only to a separate stats JSON file.
No feedback loop. No external API calls. Kill switch not required (no side effects outside
the stats file itself). This is the lowest risk item in the set.

**P3 — Kill switch and dry-run architecture is correct.**
`ESCALATION_MONITOR_ENABLED` env var approach is consistent with protocol.
5-minute cron cadence is reasonable for escalation latency requirements.

**P2 — Systemd service is enabled but not started.**
The decision to leave it enabled-but-not-started to avoid duplication with a manual instance
is a valid transitional approach. The restart policy (`Restart=always`, `RestartSec=30`) is
appropriate for a daemon that must survive crashes.

---

## What Failed — Findings With Evidence

### FINDING-01: P2 — ExecStartPre PID Removal Creates Dual-Instance Window
**Severity: HIGH**

The systemd unit runs `ExecStartPre` to remove the stale PID lockfile before each start.
The watcher has its own internal leader election and PID-based locking.

The conflict: `ExecStartPre` fires and deletes the PID file. The watcher then starts and
writes a new PID file. This is clean on normal startup. The failure window occurs when:

1. Watcher is running and crashes mid-operation (e.g., mid-write to a chat file).
2. Systemd detects the crash and schedules a restart (after RestartSec=30).
3. `ExecStartPre` fires and removes the PID lock.
4. The watcher's internal leader election sees no lock and starts a second instance.
5. **If the original instance recovers or has not fully exited**, there is a window where
   two instances exist simultaneously.

The 30-second `RestartSec` reduces but does not eliminate this window. The PID file
removal is unconditional — it does not check whether a process still owns that PID.
If the watcher uses the PID file as its only mutual exclusion mechanism (which is standard
for Python daemon PID files), removing it while the process is alive defeats that mechanism.

**Specific question from brief answered**: Yes, the systemd PID removal can fight with the
watcher's internal locking. They are operating on the same file with no coordination.
A safe implementation checks whether the PID in the lockfile belongs to a live process
before removing it. Unconditional removal is the unsafe pattern.

---

### FINDING-02: P3 — Escalation Loop is a Real Risk, Not Theoretical
**Severity: HIGH**

The escalation monitor writes resolution messages to the same chat directory that the
watcher reads. The question is whether the watcher filters by sender.

The brief does not confirm that the watcher filters outbound messages written by the
escalation monitor. Without that confirmation, the loop scenario is:

1. Escalation monitor writes a message to chat dir with a standard header.
2. Chat watcher detects new file in chat dir.
3. Watcher processes it as an inbound message (because it does not know the monitor wrote it).
4. Watcher generates a response or triggers further escalation logic.
5. That response is written to chat dir.
6. Escalation monitor detects the new file as an unprocessed escalation.
7. Loop begins.

The brief describes the FROM: field as part of the "standard header format" but does not
state that the watcher uses FROM: to skip messages written by known internal agents.
This must be verified before deployment.

Even if the watcher does filter by FROM: today, the loop risk exists at the architectural
level. If the FROM: field is not validated (e.g., a malformed message can omit it), or if
future changes to message format break the filter, the loop reactivates.

**Specific question from brief answered**: The brief does not provide evidence that the
watcher filters by sender. Absence of this confirmation is a blocking issue.

---

### FINDING-03: P4 — Silent Failure with No Alerting is Unacceptable for a 172K-File System
**Severity: HIGH**

`curl -s` suppresses all output including error codes. The cron job has no error handling:

```
*/30 * * * * curl -s -X POST http://localhost:8100/api/ingest/shared-chat
```

This means:
- MemoryWeb being down produces no alert.
- Network failure produces no alert.
- 404 or 500 from the endpoint produces no alert.
- The chat ingest falls silently behind with no observable signal.

At 172K+ messages, a 30-minute polling cycle that silently fails means MemoryWeb can
fall hours or days behind with no indication. On a system running GPU workloads and
continuous autonomous agent activity, MemoryWeb being stale is not just a data quality
issue — it degrades the quality of memory-injected context for every subsequent agent run.

Additionally, the brief raises but does not answer whether the endpoint
`/api/ingest/shared-chat` exists on the MemoryWeb instance reachable from Spark-1. The
MEMORY.md documents the MemoryWeb API on port 8100 but the deployment path for this
endpoint in a Spark-1 context is not verified. If the endpoint returns 404, `curl -s`
will never surface it.

**Specific question from brief answered**: 30-minute polling is not safe at 172K+ files
if failures are silent. The correct pattern is `curl -f` (fail on HTTP errors) piped to
a logger, with a dead man's switch alert if no successful POST is logged within N hours.

---

### FINDING-04: P5 — Partial Write on Kill Is a Real Failure Mode
**Severity: MEDIUM**

`find | wc -l` piped to a write of `evidence_stats.json` is not atomic. If the cron job
is killed mid-write (system load spike, manual kill, OOM), the output file is either
empty or contains a partial JSON object. Any downstream consumer of `evidence_stats.json`
that does not validate the JSON will read corrupt data silently.

The 6-hour cadence means up to 6 hours of stale or corrupt stats before the file is
overwritten.

The fix is one line: write to a temp file, then atomically rename it to the target.
`find ... | wc -l > evidence_stats.json.tmp && mv evidence_stats.json.tmp evidence_stats.json`

---

### FINDING-05: Cron Accumulation — Concurrent File Contention Is Likely
**Severity: MEDIUM**

The existing 8+ cron entries plus 4 new additions create the following overlap scenario:

- P1 (NLF consumer, hourly) and P3 (escalation monitor, every 5 min) both operate on
  the chat directory.
- P3 writes to chat dir; P1 reads from `nlf_queue/` (a subdirectory of chat dir).
- P4 (MemoryWeb ingest, every 30 min) reads all chat files via the API endpoint.
- P5 (evidence stats, every 6 hours) runs `find` across the entire chat dir.

The P5 `find` on 172K+ files is the highest-contention event. It runs at the same
inode-scan level as any operation that creates or deletes files in that directory.
When P5's `find` overlaps with P3 writing new files or P1 moving processed files,
the `wc -l` count is non-deterministic (it will miss or double-count files created
or moved during the scan).

More critically: if P4's curl POST fires while P5's `find` is holding directory locks
at the filesystem level, the API call may see an inconsistent view of the chat directory.
On Linux with ext4 this is generally safe at the POSIX level but will produce inconsistent
stats counts.

The lockfile in P1 (`/tmp/nlf_consumer.lock`) protects P1 from running concurrently
with itself. P3 has no equivalent lock. If the 5-minute cron fires while the previous
P3 instance is still scanning `escalations/`, two P3 instances can write to chat dir
simultaneously. For a 5-minute cron this is a realistic scenario if Spark-1 is under load.

---

### FINDING-06: P4 — MemoryWeb Reachability from Spark-1 Is Unverified
**Severity: HIGH**

MEMORY.md places MemoryWeb on `D:\memory-web` (the Windows PC) at port 8100. The tunnel
routes `memoryweb.ultrarag.app` through Cloudflare to that machine. Spark-1 (192.168.12.132)
reaching `http://localhost:8100` will hit Spark-1's own localhost, not the Windows PC.

If the cron on Spark-1 posts to `http://localhost:8100`, and MemoryWeb is not running
on Spark-1, every cron execution silently fails (see FINDING-03). The correct target
would be either `http://192.168.12.198:8100` (direct LAN) or `https://memoryweb.ultrarag.app`
(via tunnel). Neither is what `localhost:8100` resolves to on Spark-1.

This is not a warning. If the cron target is `localhost:8100` and MemoryWeb is on the
Windows PC, P4 has never successfully ingested a single chat message and cannot until
the host is corrected.

---

### FINDING-07: SSH Unavailability at Review Time
**Severity: MEDIUM (process risk)**

SSH to Spark-1 was unavailable during this review. This means:
- Live source code was not audited — only the specification provided in the brief.
- The actual crontab state, existing lockfiles, and running services were not verified.
- The real watcher's FROM: filtering logic (central to FINDING-02) was not confirmed.

This is a process gap. The protocol requires SENTINEL review before production enablement,
but SENTINEL cannot issue a fully-informed GO without reading the actual implementation.

---

## Risk Severity Summary

| ID | Component | Issue | Severity |
|----|-----------|-------|----------|
| F-01 | P2 Chat Watcher systemd | Unconditional PID removal fights watcher's own locking | HIGH |
| F-02 | P3 Escalation Monitor | Unconfirmed FROM: filtering — infinite loop risk | HIGH |
| F-03 | P4 MemoryWeb Ingest | Silent failure on curl, no alerting | HIGH |
| F-04 | P5 Evidence Stats | Non-atomic write — corrupt JSON on kill | MEDIUM |
| F-05 | Cron set (P1/P3/P4/P5) | No P3 lock, concurrent P5 find + writes creates contention | MEDIUM |
| F-06 | P4 MemoryWeb Ingest | localhost:8100 target likely wrong host on Spark-1 | HIGH |
| F-07 | Process | SSH unavailable — live code not audited | MEDIUM |

---

## Per-Component Verdicts

### P1 — NLF Queue Consumer

**RISK LEVEL**: LOW

**BLOCKING ISSUES**: None in the design specification. Subject to live code audit
confirming the JSONL append is atomic (file open in append mode, not truncate-write).

**WARNINGS**:
- Confirm the lockfile at `/tmp/nlf_consumer.lock` is checked before cron fires
  (not just at script start) — some cron setups can fire a second instance before
  the first acquires the lock if startup time is slow.
- Confirm processed/ directory exists before first run or the move will fail silently.

**GO / NO-GO for dry-run**: GO, conditional on live code audit confirming atomic append
and move-to-processed error handling.

---

### P2 — Chat Watcher systemd Service

**RISK LEVEL**: HIGH

**BLOCKING ISSUES**:
- FINDING-01: ExecStartPre must not unconditionally remove the PID lockfile.
  Replace with a safe stale-lock check: read the PID from the file, check if that
  PID is alive (`kill -0 $PID 2>/dev/null`), remove only if the PID is dead.
  Exact fix:
  ```
  ExecStartPre=/bin/bash -c 'PIDFILE=/tmp/chat_watcher.pid; \
    if [ -f "$PIDFILE" ]; then \
      PID=$(cat "$PIDFILE"); \
      if ! kill -0 "$PID" 2>/dev/null; then rm -f "$PIDFILE"; fi; \
    fi'
  ```
  Without this fix, a crash-recovery cycle can produce two simultaneous watcher
  instances writing conflicting output to the chat directory.

**WARNINGS**:
- The "enabled but not started" state is safe now but requires a documented handoff
  procedure for when the manual instance is decommissioned and systemd takes over.
  Without that procedure, the transition risks a gap in watcher coverage.

**GO / NO-GO for dry-run**: NO-GO until FINDING-01 is fixed. The dual-instance risk
is present even in dry-run mode if the watcher is crash-cycled.

---

### P3 — Escalation Monitor

**RISK LEVEL**: HIGH

**BLOCKING ISSUES**:
- FINDING-02: Confirm via live code audit that the chat watcher has a sender filter
  that skips messages where FROM: matches the escalation monitor's identity.
  If no such filter exists, deployment of P3 in any mode (including dry-run where
  it logs but does not write) is safe — but enabling live mode without this
  confirmation is a NO-GO.
- Add a per-run lockfile to prevent concurrent P3 instances. A 5-minute cron on a
  loaded system will overlap. Without a lock, two instances can write duplicate
  resolution messages to the chat dir simultaneously.

**WARNINGS**:
- The "standard header format" for resolution messages should include a machine-readable
  marker (e.g., `X-SOURCE: escalation-monitor`) that the watcher can reliably filter
  on, independent of the FROM: field content.
- Escalations that fail to resolve (e.g., unknown escalation type) should be moved to
  a dead-letter directory, not left in `escalations/` where the monitor will retry them
  on every 5-minute cycle.

**GO / NO-GO for dry-run**: GO for dry-run (log-only) only. NO-GO for live mode until
FROM: filter is confirmed and per-run lock is added.

---

### P4 — Agent Chat to MemoryWeb Ingest

**RISK LEVEL**: HIGH

**BLOCKING ISSUES**:
- FINDING-06: Verify and fix the target host. `http://localhost:8100` on Spark-1 is
  almost certainly wrong. The correct target must be determined (LAN IP or tunnel URL)
  before any mode of this cron is useful.
- FINDING-03: Replace `curl -s` with `curl -f -s` and redirect stderr to a log file.
  Add a monitoring check: if no successful POST has been logged in the past 2 hours,
  alert via the existing alert system.
  Minimum acceptable fix:
  ```
  */30 * * * * curl -f -s -X POST http://[CORRECT_HOST]:8100/api/ingest/shared-chat \
    >> ~/ai-business/logs/memoryweb_ingest.log 2>&1 || \
    echo "$(date): MemoryWeb ingest FAILED" >> ~/ai-business/logs/memoryweb_ingest_errors.log
  ```

**WARNINGS**:
- At 172K+ files, the ingest endpoint must be paginated or chunked. If the API call
  tries to enumerate and process all 172K files in one POST, Spark-1 will experience
  a significant latency spike every 30 minutes. Confirm the endpoint implements
  incremental ingest (only new files since last run).
- Verify `/api/ingest/shared-chat` actually exists on the target MemoryWeb instance.
  MEMORY.md documents `/api/ingest/session` but not `/api/ingest/shared-chat`.

**GO / NO-GO for dry-run**: NO-GO until FINDING-06 (wrong host) is resolved. A dry-run
posting to the wrong host is not a dry-run — it is a no-op that produces false confidence.

---

### P5 — Evidence Stats

**RISK LEVEL**: MEDIUM

**BLOCKING ISSUES**:
- FINDING-04: Make the JSON write atomic. Current pattern risks corrupt file on kill.
  Required fix before any deployment (including dry-run):
  Write to `evidence_stats.json.tmp`, then rename to `evidence_stats.json`.

**WARNINGS**:
- FINDING-05: Running `find ~/ai-business/shared/chat -name "*.md"` on 172K+ files
  every 6 hours on a machine running GPU training workloads is an IO risk.
  Estimated wall-clock time: 5–30 seconds depending on filesystem cache state.
  Estimated inode reads: 172K+, which will evict GPU training data from page cache.
  On a GB10 with 119GB RAM the page cache pressure is tolerable, but if NLF training
  is actively writing to the same filesystem partition, the find scan creates a read
  head contention period.
  Mitigation: offset the 6-hour schedule to avoid known training windows, or limit
  to once per 12 hours.
- `wc -l` on find output counts newlines, not files. If any filename contains a
  newline character, the count will be inflated. Use `find ... -print0 | xargs -0 echo`
  pattern or `find ... | wc -l` with awareness that the count is approximate.

**GO / NO-GO for dry-run**: NO-GO until atomic write is implemented (FINDING-04).
The fix is a single line change. This should take less than 5 minutes to correct.

---

## Answers to the 5 Critical Questions

**Q1 — P2 loop risk (PID removal vs watcher internal locking)**:
YES, this is a real conflict. The unconditional `ExecStartPre` removal defeats the
watcher's PID-based mutual exclusion during crash-recovery cycles. The 30-second
`RestartSec` gap reduces but does not close the dual-instance window. Fix is specified
in P2 blocking issues above.

**Q2 — P3 loop risk (watcher responding to monitor's own output)**:
UNCONFIRMED. The specification does not establish that the watcher filters by FROM:.
Until the watcher's message-filtering logic is verified via live code audit, the loop
scenario must be treated as a real risk. Dry-run mode for P3 is safe (logs only, no
writes to chat dir). Live mode is blocked.

**Q3 — P4 silent failure safety**:
NOT SAFE. `curl -s` silent failure combined with an unverified (and likely incorrect)
target host means P4 as specified will silently do nothing. The 30-minute polling
cadence is reasonable once the implementation is correct, but a 172K-file system
requires confirmation that the ingest endpoint is incremental, not a full scan on
every call.

**Q4 — P5 IO risk**:
MODERATE. A 172K-file `find` on a system running GPU workloads will cause a
5–30 second IO spike every 6 hours. This is unlikely to crash training but will
cause page cache pressure. At the current scale (172K files and growing) the IO
risk will increase over time. The 6-hour cadence is acceptable now; plan to move
to 12-hour or triggered-on-demand as file count grows past 500K.

**Q5 — Cron accumulation risk**:
YES, there is real contention risk. The P3 lack of a per-run lockfile is the most
acute issue — concurrent P3 instances writing to chat dir simultaneously is a
realistic failure on a loaded system. P5's `find` creating transient IO load while
P1 and P3 are also active is a secondary concern. A cron audit should map all
12 jobs against each other to identify all resource-sharing overlaps before
enabling live mode.

---

## Required Fixes Before Proceeding

These are required changes, not suggestions. Each is blocking the item specified.

| Fix | Blocks | Change Required |
|-----|--------|-----------------|
| F-01-FIX | P2 live | Replace unconditional PID remove with live-PID check in ExecStartPre |
| F-02-FIX | P3 live | Confirm watcher FROM: filter via code audit; add per-run lockfile to P3 |
| F-03-FIX | P4 all modes | Replace `curl -s` with `curl -f -s` + error logging + alert on consecutive failures |
| F-04-FIX | P5 all modes | Write to temp file, atomic rename to target |
| F-06-FIX | P4 all modes | Verify and correct MemoryWeb host target (likely not localhost:8100 on Spark-1) |
| F-07-FIX | All | Restore SSH access to Spark-1 and perform live code audit before enabling any component |

---

## Pass / Hold Decision — Per Component

| Component | Dry-Run GO/NO-GO | Reason |
|-----------|-----------------|--------|
| P1 — NLF Queue Consumer | GO (conditional) | Low risk design; pending live code audit of append atomicity |
| P2 — Chat Watcher systemd | NO-GO | FINDING-01: unconditional PID removal must be fixed first |
| P3 — Escalation Monitor | GO for dry-run only | Dry-run (log-only) is safe; live mode blocked until FROM: filter confirmed |
| P4 — MemoryWeb Ingest | NO-GO | FINDING-06: wrong host + FINDING-03: silent failure, no point running even dry-run |
| P5 — Evidence Stats | NO-GO | FINDING-04: atomic write fix required; fix is trivial (one line) |

---

## Overall Flywheel GO/NO-GO

**NO-GO for simultaneous deployment of all 5 in dry-run mode.**

Reason: Three of the five components (P2, P4, P5) have blocking issues that must be
resolved before even dry-run deployment produces useful signal. Deploying all 5
simultaneously when 3 are broken means:

- P4 will silently do nothing (wrong host, silent failure) and give false confidence
  that the ingest pipeline is running.
- P5 will risk writing corrupt stats files on any load spike.
- P2's PID removal issue is latent — it only manifests on crash, which is exactly
  when you most need clean recovery behavior.

**Recommended sequencing after fixes:**

1. Fix all 5 blocking items (F-01 through F-07). Estimated effort: 2–4 hours.
2. Restore SSH access to Spark-1 and perform live code audit of all 5 scripts.
3. Deploy P1 and P3 (dry-run only) first — these have the lowest interdependency risk.
4. Monitor P1 and P3 for 24 hours.
5. Deploy P5 (after atomic write fix) — read-only, safe to run alongside P1/P3.
6. Deploy P4 (after host and alerting fixes) — confirm endpoint exists and returns 200.
7. Enable P2 systemd (after PID fix) only after manual watcher instance is retired
   and handoff procedure is documented.
8. Do not enable live mode on any component until that component's 24-hour dry-run
   is clean and CRUCIBLE has verified it per the connection protocol.

---

*SENTINEL — QA, Validation and Risk Control*
*No approval was given that was not earned. These findings are gifts.*
