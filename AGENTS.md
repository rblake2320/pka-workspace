# Workspace Memory Bootstrap

This folder has persistent local memory. New chats opened in this workspace
must load that memory before answering questions about prior work.

## Required Startup Read Order
Read these files at the start of every new chat in this folder:

1. `MEMORY.md`
2. `CLAUDE.md`
3. `Owner's Inbox/owner.md`
4. `Team/handoff.md`
5. `Team/status.md`

## When The User Asks About Prior Work
Before saying you do not remember, inspect the local memory stack in this order:

1. `Team/handoff.md` for the latest session state
2. `Team/status.md` for active and pending work
3. `Owner's Inbox/DELIVERY_MANIFEST.md` for completed deliverables
4. Relevant files in `Team/tasks/` for task history and definitions of done
5. Relevant agent journals in `Team/*/journal.md`
6. Relevant deliverables in `Owner's Inbox/`

## Memory Rules
- Treat local workspace files as the source of truth for prior work in this folder.
- Do not claim lack of memory until you have checked the files above.
- If memory files conflict, prefer the most specific and operational source in this order:
  `Team/tasks/` -> `Owner's Inbox/DELIVERY_MANIFEST.md` -> `Team/handoff.md` -> `Team/status.md` -> agent journals.
- For code-specific history, also inspect current files and `git diff` after reading the memory files.

## Maintenance
When consequential work changes the workspace state, keep memory current by updating the relevant local artifacts:

- `Team/handoff.md`
- `Team/status.md`
- `Owner's Inbox/DELIVERY_MANIFEST.md`
- the relevant task record in `Team/tasks/`
- the relevant agent journal in `Team/*/journal.md`

## Scope
This file exists to make future chats in `C:\Users\techai\PKA testing` start with folder memory, not a blank slate.
