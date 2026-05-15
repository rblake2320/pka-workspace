# Changelog

# Changelog

All notable changes to the PKA workspace should be recorded here.

## 0.9.0 - 2026-05-14

PKA Gap-Fill: adversarial red-team layer, confidence vocabulary, trust ledger, Why Engine.

- Added `.claude/agents/WRAITH.md` — Adversarial Red-Team Agent (14th agent); activates after CRUCIBLE, before SENTINEL on all Build mode tasks
- Added `Team/CONFIDENCE_VOCABULARY.md` — canonical confidence language for all agent claims
- Added `Team/trust_ledger.md` — per-agent, per-domain performance track record; AXIOM reads at routing time
- Installed `tools/why-engine/` — root-cause documentation pipeline; WhyCases stored in `Owner's Inbox/evidence/`
- Updated 8 agent MDs with Specialist Genome, Self-Awareness Protocol, and WRAITH routing position
- Updated `CLAUDE.md` — WRAITH added to Active Agent Roster; Rule 10 (Memory Trust on Write) and Rule 11 (Context Before Routing) added to Core Operating Rules
- Updated `Team/CORE_RULES.md` — Rules extended to 11; Build route updated with WRAITH gate; WhyCase Requirement section added
- Updated `Team/handoff.md` — v0.9.0 state captured
- Verified: 10/10 checkpoints passed; SENTINEL GO issued

## 0.8.0 - 2026-04-02

Durable runtime layer.

- Added `scripts/pka_runtime.py` — persistent job queue, resumable job state, and approval interrupt state machine
- Added `scripts/pka_runtime_check.py` — runtime integrity validation for jobs and approvals
- Updated `scripts/pka_session_gate.py` — RESUME output now includes active jobs and pending approvals
- Updated `scripts/pka_process_audit.py` — runtime state integrity is audited with the rest of the workspace
- Updated `scripts/pka_operator_run.py` — runtime integrity is now part of the operator path
- Updated `scripts/pka_agent_readiness.py` and `scripts/pka_doctor.py` — runtime layer counted as first-class capability

## 0.7.0 - 2026-04-02

Platform maturity: repo boundary fix, production telemetry, session continuity.

### Gap 1: Repo Boundary Fix (CRITICAL SAFETY)
- PKA workspace is now its own standalone git root (`git init` inside `PKA testing/`)
- Remote: `https://github.com/rblake2320/pka-workspace.git` (force-pushed with full history)
- Parent repo index cleaned: `git rm -r --cached "PKA testing/"` (PKA only, council untouched)
- Pre-push bare backup at `C:\Users\techai\pka-workspace-backup.git`
- `.gitignore` updated: added `.claude/worktrees/` and `Team/tasks/RESUME.json`
- `REPO_ALIGNMENT.md` updated to reflect standalone status
- `pka_doctor.py check_git_boundary` passes: toplevel == ROOT (portable, derived from `Path(__file__)`)
- 5 stale Claude Code agent worktrees removed before init

### Gap 2: Production Telemetry
- Added `scripts/pka_telemetry.py` — 8-section trend analysis + anomaly detection:
  score trajectory, check reliability, agent velocity, tool mix, session health,
  guardrail trends, stale task alert, anomaly summary
- Data sufficiency guards: each section prints "Insufficient data" rather than
  misleading trends when record count is below threshold
- Runtime budget: 3s per section, 10s total; slow sections skip with warning
- Agent velocity requires 5+ completed tasks per agent before trend claims
- Exit code always 0 (anomalies are warnings; revisit in v0.8.0)
- Updated `scripts/pka_operator_run.py`: telemetry wired as step 7 (after scorecard,
  before observability)

### Gap 3: Session Continuity
- Upgraded `scripts/pka_session_gate.py start`: scans all non-terminal tasks, flags
  stale (>48h), groups by state, outputs ranked work queue, writes `Team/tasks/RESUME.json`
- Upgraded `scripts/pka_session_gate.py end`: also writes `RESUME.json` after audit
- `parse_task_file()` calls wrapped in try/except — corrupt files skip with warning
- Upgraded `scripts/pka_lib.py FileLock`: writes `{pid}:{timestamp}` on lock creation;
  on contention checks age (>300s) and PID liveness (Windows-safe: ctypes.windll.kernel32.
  OpenProcess, NOT os.kill); stale breaks logged to `logs/guardrail_*.jsonl`
- Added `scripts/pka_doctor.py check_stale_tasks()`: warns on non-terminal tasks with
  updated_at older than 48h (WARNING not FAIL)

## 0.5.1 - 2026-04-02

Agent readiness hardening.

- Added `scripts/pka_machine_health.py` — live Spark/AWS health diagnostics with report output
- Added `Team/AGENT_TOOL_ENTITLEMENTS.json` — explicit per-agent tool entitlement matrix
- Added `scripts/pka_entitlement_check.py` — validates roster coverage and entitlement policy integrity
- Added `scripts/pka_recovery_playbook.py` — generates rollback/recovery playbooks for failed tasks
- Updated `scripts/pka_task_cli.py` — failed verdicts now auto-generate recovery playbooks
- Updated `scripts/pka_operator_run.py` — now includes machine health and entitlement validation
- Updated `scripts/pka_doctor.py` and `scripts/pka_agent_readiness.py` — readiness controls now tracked explicitly

## 0.5.0 - 2026-04-02

Intelligence consolidation and hardening from claude-code-source analysis.

- Added `scripts/pka_dream.py` — 4-phase background intelligence consolidation (orient/gather/consolidate/prune). Reads session logs + task records + agent journals; produces `Owner's Inbox/reports/PKA_DREAM_REPORT.md`. Uses FileLock to prevent concurrent runs.
- Extended `scripts/pka_doctor.py` — added `memory_size` check: warns if MEMORY.md exceeds 200-line or 25 KB dual cap (derived from Claude Code source memdir.ts constants MAX_ENTRYPOINT_LINES=200, MAX_ENTRYPOINT_BYTES=25000)
- Updated `scripts/pka_operator_run.py` — now 9 steps, `dream` inserted before `proof_dashboard`
- Intelligence sourced from: KAIROS daily-log pattern, DreamTask 4-phase structure, memdir.ts dual-cap constants

## 0.4.0 - 2026-04-02

Audit trail, cost tracking, journal compaction, and proof dashboard.

- Added `PostToolUse` hook in `.claude/settings.local.json` — every Bash/Write/Edit/Task call logged to `logs/session_YYYYMMDD.jsonl`
- Added `scripts/pka_post_tool_hook.py` — hook receiver (exits 0 always, never interrupts ops)
- Added `scripts/pka_cost_tracker.py` — aggregates session logs into `PKA_COST_TRACKER_REPORT.md`
- Added `scripts/pka_journal_compact.py` — enforces last-10-entries limit on all agent journals
- Extended `scripts/pka_doctor.py` — added `hooks_configured` check (DeferredInitResult pattern)
- Updated `scripts/pka_operator_run.py` — now 8 steps: doctor → sync → validate → scorecard → observability → journal_compact → cost_tracker → proof_dashboard
- Updated `scripts/pka_proof_dashboard.py` — added Audit Trail section with tool call breakdown and session coverage
- Repo separated to `rblake2320/verified-agent-ops` (origin fixed from council.git)

## 0.3.1 - 2026-04-01

Operator ergonomics hardening.

- Added environment and runtime diagnostics in `scripts/pka_doctor.py`
- Updated `scripts/pka_operator_run.py` to run doctor before validation
- Updated README operator and validation commands to include doctor

## 0.3.0 - 2026-04-01

Validation hardening and observability.

- Fixed task ledger overwrite risk by making task record filenames unique per task id
- Added adversarial live test suite in `scripts/pka_resilience_test.py`
- Added full validation runner in `scripts/pka_full_validation.py`
- Added validation history logging in `logs/pka_validation_history.jsonl`
- Added observability report generator in `scripts/pka_observability.py`
- Added operator entrypoint in `scripts/pka_operator_run.py`
- Updated README and release process to point at the real validation stack
- Verified the workspace with repeated E2E runs plus the resilience suite

## 0.2.0 - 2026-04-01

Automation and evidence layer.

- Added shared process library in `scripts/pka_lib.py`
- Added control-file auto-sync in `scripts/pka_sync.py`
- Added structured message CLI in `scripts/pka_message_cli.py`
- Added process readiness scorecard in `scripts/pka_scorecard.py`
- Added evidence-pack generation in `scripts/pka_evidence_pack.py`
- Updated task CLI to auto-sync status and handoff surfaces
- Verified the expanded process layer with real audit and E2E runs
- Added competitive threat model and anti-slop positioning files

## 0.1.0 - 2026-04-01

Initial hardened operating layer.

- Added canonical process model in `Team/OPERATING_MODEL.md`
- Added consequential task intake template in `Team/TASK_BRIEF_TEMPLATE.md`
- Added delivery ledger in `Owner's Inbox/DELIVERY_MANIFEST.md`
- Added consequential task ledger in `Team/tasks/`
- Added lightweight structured coordination protocol in `Team/MESSAGE_PROTOCOL.md`
- Added process audit in `scripts/pka_process_audit.py`
- Added task ledger CLI in `scripts/pka_task_cli.py`
- Added session gate in `scripts/pka_session_gate.py`
- Added real end-to-end integration test in `scripts/pka_e2e_test.py`
- Added regression protection and manifest integrity checks
