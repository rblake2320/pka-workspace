# PKA Message Protocol

This is the lightweight structured protocol for agent-to-agent coordination inside PKA.
Use it only when the message needs to preserve state or trigger action across turns or sessions.

## Goals
- Standardize assignment, blocker, approval, and completion signals
- Keep coordination machine-readable
- Avoid freeform "status-ish" messages that get lost

## Storage
- Active messages live in `Team/messages/active/`
- Completed or consumed messages move to `Team/messages/archive/`
- One message per file

## Filename Convention
`YYYYMMDD-HHMMSS-message-type-short-name.json`

Example:
`20260331-223500-task-assignment-profilepays.json`

## Required Envelope
```json
{
  "type": "task_assignment",
  "timestamp": "2026-03-31T22:35:00Z",
  "from": "AXIOM",
  "to": "NOVA",
  "task_id": "TASK-20260331-001"
}
```

## Supported Message Types

### `task_assignment`
Use when AXIOM or HELM assigns meaningful work.

Required fields:
- `task_id`
- `summary`
- `expected_state`

### `blocker`
Use when work cannot proceed without intervention.

Required fields:
- `task_id`
- `severity`
- `reason`
- `requested_action`

Severity:
- `critical`
- `high`
- `medium`
- `low`

### `approval_request`
Use when a plan, deliverable, or task transition needs explicit review.

Required fields:
- `task_id`
- `approval_type`
- `artifact`

### `completion_notice`
Use when an agent has finished its step and is handing off.

Required fields:
- `task_id`
- `artifact`
- `next_owner`
- `next_state`

## Rules
- If the message changes task state, update the task record too
- If the message results in a final deliverable, update the delivery manifest too
- Do not use messages for trivial conversation
- Do not store secrets or owner-private context in protocol messages
