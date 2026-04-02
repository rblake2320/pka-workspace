# Task Ledger

This folder is the canonical ledger for consequential work.
Use one task record per meaningful task that needs continuity, validation, or a final deliverable.

## When To Create A Task Record
Create a record when the work is:
- strategic
- technical
- legal
- multi-step
- likely to produce a file in `Owner's Inbox/`
- likely to span sessions

Do not create records for trivial one-turn requests unless they become consequential.

## Rules
- One file per task
- Use `TASK_RECORD_TEMPLATE.md`
- Keep frontmatter accurate
- Update the record when the lifecycle state changes
- If the task is delivered, update `Owner's Inbox/DELIVERY_MANIFEST.md`
- You may use `python scripts/pka_task_cli.py` to create and update records consistently

## Filename Convention
`YYYYMMDD-short-task-name.md`

Example:
`20260331-profilepays-billing-model.md`
