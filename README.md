# PKA — Personal Knowledge Agents

A structured AI team workspace that runs inside Claude Code.
Drop a task in. Get a finished deliverable out. Every time.

---

## What This Is

PKA is an orchestrated multi-agent workspace built on Claude Code's subagent system.
Instead of prompting one AI, you work with a **named team of specialists** — each with
a defined mission, non-negotiable standards, and a specific place in the workflow.

**AXIOM** is the orchestrator. You never route tasks yourself. You drop work in the
Team Inbox, AXIOM reads it, routes to the right agent(s), and completed work lands
in your Owner's Inbox ready to act on.

---

## The Team

| Agent | Role |
|-------|------|
| **AXIOM** | Orchestrator — routes everything, never executes |
| **NOVA** | Research & Strategic Intelligence |
| **FORGE** | Builder & Technical Architect |
| **SENTINEL** | QA, Validation & Risk Control |
| **HELM** | Operator, Planner & Execution Coordinator |
| **VENTURE** | Product & Business Innovation |
| **SPARK** | Voice, Content & Community |
| **LEGAL** | IP Strategy, Patents & Legal Risk |
| **SCRIBE** | Autonomous Skill Writer |
| **GRID** | Scale & Architecture Integrity |
| **RADAR** | Opportunity Detection & Use Case Scout |
| **CRUCIBLE** | Master Test Engineer |
| **DEBUGGER** | Ultra Master Debugger |

---

## The Workflow

```
You drop a file or task → Team Inbox/
        ↓
    AXIOM reads it at session start
        ↓
    Routes to the right agent(s)
        ↓
    Work gets done — reviewed — validated
        ↓
Finished deliverable → Owner's Inbox/
        ↓
    You review and act
```

---

## Folder Structure

```
PKA/
├── VERSION                ← Workspace version
├── CHANGELOG.md           ← Version history
├── RELEASE_PROCESS.md     ← Release and validation rules
├── CLAUDE.md              ← Workspace config: who you are, what you're building,
│                            operating rules, agent roster, design principles
├── Team/OPERATING_MODEL.md ← Canonical task lifecycle and operating controls
├── Team/tasks/             ← Consequential task ledger and task records
│
├── Team Inbox/            ← Drop tasks, files, images, hire requests here
│   └── processed/         ← Completed tasks archived here
│
├── Owner's Inbox/         ← All completed deliverables land here
│   └── owner.md           ← Your profile — agents read this before every task
│   └── DELIVERY_MANIFEST.md ← Index of completed deliverables and next actions
│
├── Team/
│   ├── roster.md          ← Active agent list with missions
│   ├── CORE_RULES.md      ← Non-negotiable rules all agents follow
│   ├── hiring/
│   │   └── process.md     ← How to hire a new agent in 5 steps
│   └── [AGENT]/
│       └── readme.md      ← Per-agent working directory
│
├── logs/                  ← Validation history and runtime audit logs
└── scripts/               ← Automation scripts, validation, observability, and operator entrypoints
```

---

## How to Hire a New Agent

Drop this in `Team Inbox/`:

```
HIRE REQUEST
Role needed: [what this agent does]
Trigger: [when should AXIOM route to this agent]
Key outputs: [what this agent delivers]
Named: [optional name]
```

AXIOM validates the gap, HELM creates the agent file, the agent is active next session.
Full process in `Team/hiring/process.md`.

---

## Core Operating Principles

All agents follow these without exception:

1. **Answer first** — every response leads with the answer, then reasoning, then risks, then action
2. **Honesty over impressiveness** — weak sources get flagged, not hidden
3. **Nothing generic** — no padding, no boilerplate, no "it depends" without specifics
4. **No circular validation** — agents don't review their own consequential work
5. **Inbox protocol is absolute** — Owner's Inbox is the only delivery path to you
6. **Defined lifecycle** — meaningful tasks move through a tracked state model in `Team/OPERATING_MODEL.md`
7. **Real validation** — nothing is green without a real supporting test

## Validation Commands

Run these before calling the workspace healthy:

```powershell
python scripts\pka_doctor.py
python scripts\pka_process_audit.py
python scripts\pka_e2e_test.py
python scripts\pka_resilience_test.py
python scripts\pka_full_validation.py
python scripts\pka_scorecard.py
python scripts\pka_observability.py
python scripts\pka_agent_readiness.py
python scripts\pka_runtime_check.py
```

## Operator Commands

Useful day-to-day control commands:

```powershell
python scripts\pka_task_cli.py --help
python scripts\pka_message_cli.py --help
python scripts\pka_doctor.py
python scripts\pka_machine_health.py
python scripts\pka_sync.py
python scripts\pka_entitlement_check.py
python scripts\pka_runtime.py --help
python scripts\pka_operator_run.py
python scripts\pka_evidence_pack.py --task-id TASK-YYYYMMDD-001
python scripts\pka_recovery_playbook.py --task-id TASK-YYYYMMDD-001
```

## Repository Note

This workspace is its own standalone git repository. `scripts/pka_doctor.py`
checks that the git top-level matches this folder before the workspace is
called healthy.

---

## Setting Up Your Own Workspace

1. **Fork this repo**
2. **Edit `CLAUDE.md`** — replace the owner context, active projects, and design principles with your own
3. **Edit `Owner's Inbox/owner.md`** — your profile: role, communication style, priorities
4. **Open the folder in Claude Code** — AXIOM activates automatically on session start
5. **Drop your first task in `Team Inbox/`** and tell AXIOM what you want done

The agents are built into Claude Code's subagent system. No additional setup required.

---

## What Makes This Different

Most AI workflows are one prompt → one response. PKA is a **team with memory**:

- Agents have defined missions and non-negotiables — they don't drift
- AXIOM enforces routing — the right specialist handles every task
- SENTINEL reviews consequential work before it reaches you — no rubber stamps
- The Owner's Inbox builds a permanent record of every decision and deliverable
- New agents can be hired for gaps — the team grows with your needs

---

## SaaS / Commercial Use

This workspace pattern is designed to be deployed for others. If you're building
AI-assisted workflows for clients or teams, the full hiring pipeline, agent template,
and inbox protocol are designed to be white-labeled and customized per deployment.

See `Team/hiring/process.md` for the agent creation template.

---

*Built with Claude Code. Runs on any machine with Claude Code installed.*
