> **DRAFT — For Ron's review before publishing to rblake2320/verified-agent-ops**

---

# verified-agent-ops

A structured multi-agent workspace that runs inside Claude Code. Thirteen named agents. A defined task lifecycle. Every deliverable validated before it reaches you.

---

## What it is

PKA (Personal Knowledge Agents) is an orchestrated workspace built on Claude Code's subagent system. Instead of prompting a single AI, you work with a fixed team of specialists — each with a defined mission, a scope they do not exceed, and a specific position in the task chain. Work goes in through one inbox. Completed, validated deliverables come out through another. The orchestrator (AXIOM) handles routing. You never do that yourself.

The repo is named `verified-agent-ops` because the design guarantee is verification, not just generation: nothing reaches the owner until SENTINEL has audited it, and no build goes to production until CRUCIBLE has tested it.

---

## The 13-agent roster

| Agent | Role |
|-------|------|
| **AXIOM** | Orchestrator — reads every task, routes to the right agent(s), synthesizes final output. Never executes tasks directly. |
| **NOVA** | Research and strategic intelligence — market analysis, technical landscape, decision support. |
| **FORGE** | Builder and technical architect — code, systems, infrastructure, integrations. |
| **SENTINEL** | QA, validation, and risk control — audits outputs, issues GO / NO-GO verdicts, blocks bad work from reaching the owner. |
| **HELM** | Operator and execution coordinator — plans multi-step work, manages sequencing across agents. |
| **VENTURE** | Product and business innovation — strategy, positioning, feature decisions, market fit. |
| **SPARK** | Voice, content, and community — copy, brand narrative, launch messaging. |
| **LEGAL** | IP strategy, patents, and legal risk — patent assessment, contract review, compliance flags. |
| **SCRIBE** | Autonomous skill writer — documents processes, writes reusable skills, maintains the knowledge layer. |
| **GRID** | Scale and architecture integrity — reviews systems for load ceiling, failure modes, and structural debt. |
| **RADAR** | Opportunity detection and use case scout — spots cross-domain opportunities across the portfolio. |
| **CRUCIBLE** | Master test engineer — functional testing, security/adversarial testing (Layer 3.5), regression coverage. |
| **DEBUGGER** | Ultra master debugger — root cause analysis on unknown failures before FORGE attempts a fix. |

---

## The 9-step operator pipeline

Run this at the start of any session to verify workspace health and sync all state surfaces:

```bash
python scripts/pka_operator_run.py
```

| Step | Script | What it does |
|------|--------|--------------|
| 1 | `pka_doctor.py` | Environment and config diagnostics — checks Python, file structure, hooks, memory size cap |
| 2 | `pka_sync.py` | Syncs control files: task ledger, status board, handoff, manifest |
| 3 | `pka_full_validation.py` | Runs the complete validation stack end-to-end |
| 4 | `pka_scorecard.py` | Process readiness scorecard — surfaces gaps in coverage or hygiene |
| 5 | `pka_observability.py` | Generates an observability report from session logs |
| 6 | `pka_journal_compact.py` | Enforces the last-10-entries limit on all agent journals |
| 7 | `pka_cost_tracker.py` | Aggregates tool call logs into a cost and usage report |
| 8 | `pka_dream.py` | 4-phase background intelligence consolidation (orient / gather / consolidate / prune) across session logs, task records, and journals |
| 9 | `pka_proof_dashboard.py` | Generates the proof dashboard — audit trail, task history, session coverage |

---

## Task lifecycle

Every consequential task moves through these states in order. AXIOM enforces transitions. Tasks cannot skip validation gates.

```
classified → assigned → in_progress → under_test → under_audit → delivered → archived
```

| State | Owner | What happens |
|-------|-------|-------------|
| `classified` | AXIOM | Task type, route, and urgency identified. Execution contract written. |
| `assigned` | AXIOM / HELM | Agent chain named. First working agent has accepted scope. |
| `in_progress` | Working agent | Work is being executed. |
| `under_test` | CRUCIBLE | Functional tests run. Layer 3.5 security testing run on any web or API work. |
| `under_audit` | SENTINEL | GO / HOLD / NO-GO issued against CRUCIBLE's test evidence. |
| `delivered` | AXIOM | Final artifact placed in `Owner's Inbox/`. Manifest entry recorded. |
| `archived` | AXIOM | Follow-up complete or no further action pending. |

Web and API builds cannot skip `under_test` or `under_audit`. A SENTINEL GO without CRUCIBLE's Layer 3.5 report is invalid.

---

## How to run it

**Requirements:** Claude Code installed. Python 3.10+. No other dependencies for the operator layer.

```bash
# Clone
git clone https://github.com/rblake2320/verified-agent-ops.git
cd verified-agent-ops

# Open in Claude Code
# (Claude Code reads CLAUDE.md and activates AXIOM automatically)

# Verify workspace health
python scripts/pka_doctor.py

# Start a session
python scripts/pka_session_gate.py start

# Drop your first task
# Edit Team Inbox/README.md or drop a file directly into Team Inbox/
# Tell AXIOM what you want done.

# Run the full operator pipeline
python scripts/pka_operator_run.py
```

To make it yours: edit `CLAUDE.md` with your own context, projects, and design principles. Edit `Owner's Inbox/owner.md` with your profile. The agents read both before every task.

---

## What makes it different from generic multi-agent frameworks

- **Audit trail by default.** Every tool call (Bash, Write, Edit, Task) is logged to `logs/session_YYYYMMDD.jsonl` via a `PostToolUse` hook. The proof dashboard surfaces coverage per session. You can verify exactly what ran and when.

- **Persistent agent journals, not stateless prompts.** Each agent maintains a journal with a Self-Model, recurring patterns, and feedback received from SENTINEL and CRUCIBLE. Agents read their journal before starting a task. Over time, the team calibrates.

- **Formal verdicts, not vibes.** SENTINEL issues GO / NO-GO / HOLD against a defined checklist — not a general impression. A NO-GO names the exact defect category and required fix. CRUCIBLE's Layer 3.5 adversarial testing is a hard gate on any web or API build, not an optional step.

---

## Repository structure

```
verified-agent-ops/
├── CLAUDE.md                   # Workspace config: owner context, agent roster, design rules
├── CHANGELOG.md                # Version history
├── Team/
│   ├── OPERATING_MODEL.md      # Canonical task lifecycle and validation gates
│   ├── CORE_RULES.md           # Non-negotiable rules all agents follow
│   ├── tasks/                  # Consequential task ledger
│   └── [AGENT]/journal.md      # Per-agent persistent memory
├── Team Inbox/                 # Drop tasks, files, and hire requests here
├── Owner's Inbox/              # All completed deliverables land here
│   ├── owner.md                # Owner profile — agents read this before every task
│   └── DELIVERY_MANIFEST.md    # Index of what was delivered and why it matters
├── scripts/                    # Operator entrypoints, validation, observability
└── logs/                       # Session audit logs and validation history
```

---

*Runs on any machine with Claude Code installed. Current version: 0.5.0.*
