# Workspace Memory Index

This is the canonical startup index for cross-session memory in
`C:\Users\techai\PKA testing`.

## What This Workspace Is
- Personal AI orchestration workspace for Ron
- AXIOM-centered multi-agent operating model
- `Team Inbox/` is intake
- `Owner's Inbox/` is delivery

## Canonical Memory Stack

### Identity And Rules
- `VERSION` — current workspace release number
- `CHANGELOG.md` — latest implemented changes by version
- `CLAUDE.md` — workspace identity, agent roster, startup and shutdown rules
- `README.md` — repo overview and operator commands
- `Team/CORE_RULES.md` — team-wide non-negotiables
- `Team/OPERATING_MODEL.md` — canonical lifecycle and process rules
- `Team/roster.md` — active agent roster and responsibilities

### Current Session State
- `Owner's Inbox/owner.md` — Ron's profile, priorities, and working style
- `Team/handoff.md` — latest session summary and next attention items
- `Team/status.md` — active work and session-start checklist
- `Team Inbox/` — unprocessed user input for the team

### Completed Work History
- `Owner's Inbox/DELIVERY_MANIFEST.md` — indexed history of consequential deliverables
- `Owner's Inbox/` — completed reports, verdicts, plans, and evidence packs
- `Team/tasks/` — task records, definitions of done, operational history

### Agent Memory
- `Team/AXIOM/journal.md`
- `Team/CRUCIBLE/journal.md`
- `Team/DEBUGGER/journal.md`
- `Team/FORGE/journal.md`
- `Team/GRID/journal.md`
- `Team/HELM/journal.md`
- `Team/LEGAL/journal.md`
- `Team/NOVA/journal.md`
- `Team/RADAR/journal.md`
- `Team/SCRIBE/journal.md`
- `Team/SENTINEL/journal.md`
- `Team/SPARK/journal.md`
- `Team/VENTURE/journal.md`

## Retrieval Protocol
- For `what version are we on` or `what is this folder doing now`, start with `VERSION`, then `CHANGELOG.md`, then the latest implementation report in `Owner's Inbox/`.
- For `what were we last working on`, start with `Team/handoff.md`, then `Team/status.md`, then `Owner's Inbox/DELIVERY_MANIFEST.md`.
- For `what changed`, inspect the relevant task record, deliverable, and current file state.
- For agent-specific history, read that agent's journal before answering.
- For ambiguous prior-work questions, search the workspace instead of guessing.

## Current High-Signal State
- Current workspace version is `0.8.0`.
- `0.8.0` added a durable runtime layer: `scripts/pka_runtime.py`, `scripts/pka_runtime_check.py`, runtime-aware session gate output, runtime auditing, and runtime readiness coverage.
- `0.7.0` established repo-boundary correction, production telemetry, and stronger session continuity.
- Latest handoff/status files may lag behind versioned reality and should not override `VERSION` plus `CHANGELOG.md` when summarizing the current state of the folder.
- Delivery manifest is the best compact index of what has already been completed.

## Guardrail
New chats in this folder should treat these files as persistent memory and should not answer prior-work questions from model memory alone.
