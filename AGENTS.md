# Workspace Memory Bootstrap

This folder has persistent local memory. New chats opened in this workspace
must load that memory before answering questions about prior work.

## Required Startup Read Order
Read these files at the start of every new chat in this folder:

1. `MEMORY.md`
2. `VERSION`
3. `CHANGELOG.md`
4. `CLAUDE.md`
5. `Owner's Inbox/owner.md`
6. `Team/handoff.md`
7. `Team/status.md`

## When The User Asks About Prior Work
Before saying you do not remember, inspect the local memory stack in this order:

1. `VERSION` and `CHANGELOG.md` for the current release and latest implemented capabilities
2. `Team/handoff.md` for the latest session state
3. `Team/status.md` for active and pending work
4. `Owner's Inbox/DELIVERY_MANIFEST.md` for completed deliverables
5. Relevant files in `Team/tasks/` for task history and definitions of done
6. Relevant agent journals in `Team/*/journal.md`
7. Relevant deliverables in `Owner's Inbox/`

## Memory Rules
- Treat local workspace files as the source of truth for prior work in this folder.
- Do not claim lack of memory until you have checked the files above.
- For current-version questions, prefer `VERSION` and `CHANGELOG.md` over `Team/handoff.md` and `Team/status.md`.
- If memory files conflict, prefer the most specific and operational source in this order:
  `VERSION`/`CHANGELOG.md` -> `Team/tasks/` -> `Owner's Inbox/DELIVERY_MANIFEST.md` -> `Team/handoff.md` -> `Team/status.md` -> agent journals.
- For code-specific history, also inspect current files and `git diff` after reading the memory files.

## Maintenance
When consequential work changes the workspace state, keep memory current by updating the relevant local artifacts:

- `Team/handoff.md`
- `Team/status.md`
- `Owner's Inbox/DELIVERY_MANIFEST.md`
- the relevant task record in `Team/tasks/`
- the relevant agent journal in `Team/*/journal.md`
- `Team/trust_ledger.md` — update after every SENTINEL GO/NO-GO verdict
- `Owner's Inbox/evidence/` — WhyCases from Why Engine are stored here; do not delete

When using confidence language, all agents must follow `Team/CONFIDENCE_VOCABULARY.md`.

## Scope
This file exists to make future chats in `C:\Users\techai\PKA testing` start with folder memory, not a blank slate.
