# PKA Operating Model

This file is the canonical process for how work moves through the PKA workspace.
If any other document conflicts with this file, this file wins unless Ron overrides it.

## Core Principle
Every meaningful task must move through a defined lifecycle with a named owner,
clear evidence requirements, and a final deliverable in `Owner's Inbox/`.

Consequential tasks must also have a record in `Team/tasks/`.

## Task Lifecycle
Every consequential task moves through these states in order:

| State | Owner | Entry Criteria | Exit Criteria |
|------|------|------|------|
| `new` | Ron / AXIOM | Item appears in `Team Inbox/` | AXIOM has reviewed the item |
| `classified` | AXIOM | Task type, route, and urgency are identified | Execution contract is written |
| `assigned` | AXIOM / HELM | Responsible agent or chain is named | First working agent has accepted scope |
| `in_progress` | Working agent | Work has started | Deliverable or artifact is ready for handoff |
| `under_test` | CRUCIBLE | Build or executable artifact exists | Test report is complete |
| `under_audit` | SENTINEL | Test evidence or audit scope exists | GO / HOLD / NO-GO is issued |
| `delivered` | AXIOM | Final deliverable is placed in `Owner's Inbox/` | Manifest entry is recorded |
| `archived` | AXIOM | Follow-up completed or no action pending | Item moved to historical record if needed |

Notes:
- Tiny low-risk requests do not need every state, but they still require classification and delivery.
- Web/API builds cannot skip `under_test` or `under_audit`.
- A task may return to `assigned` or `in_progress` after a HOLD or NO-GO.

## Execution Contract
Before meaningful work begins, AXIOM or HELM must define:
- Objective
- Route
- Deliverable expected
- Definition of done
- Evidence required
- Known constraints
- Known risks
- Out of scope — what this task explicitly does NOT cover
- Abort conditions — specific signals that mean stop work and escalate (e.g., "if FORGE hits the same blocker twice," "if SENTINEL issues NO-GO after second iteration")
- Falsifiability — what evidence would prove this approach is wrong? What does failure-disguised-as-success look like? (e.g., "tests pass but only test the mock," "all research sources trace to same origin")

If these are not clear, the task is not ready for execution.

## Definition Of Done
A task is done only when all of the following are true:
- The output answers the actual request
- The right agent chain handled it
- Required validation has been completed
- The final artifact is in `Owner's Inbox/`
- The delivery manifest has been updated
- `Team/status.md` and `Team/handoff.md` reflect reality

## Validation Gates
- Research or decision support with material business impact: SENTINEL review required
- Technical build or code change: CRUCIBLE then SENTINEL required
- Web/API work: CRUCIBLE Layer 3.5 is mandatory
- Security-sensitive work: explicit data isolation review required

## Escalation Protocol
Escalate immediately when:
- Requirements conflict
- Required context is missing
- A live/security/data isolation risk is detected
- The same failed approach has been tried twice

Severity model:
- `Critical`: stop work now, escalate same session
- `High`: do not deliver, escalate in current task cycle
- `Medium`: continue only if assumption is logged explicitly
- `Low`: log as debt or cleanup item

## Inbox Rules
- `Team Inbox/` is the intake surface
- `Owner's Inbox/` is the only delivery surface to Ron
- `Owner's Inbox/DELIVERY_MANIFEST.md` is the index of what was delivered and why it matters
- `Team/tasks/` is the lifecycle ledger for consequential work

## Operational Hygiene
- Temp artifacts belong in a temp folder, not the workspace root
- Session-start and session-end checklists are mandatory
- Agent journals are memory, not decoration; update them after consequential work
- `python scripts/pka_session_gate.py start` and `python scripts/pka_session_gate.py end` are the default lightweight session gates

## What This Process Optimizes For
- Correct routing
- Real validation
- Low ambiguity
- High continuity between sessions
- Minimal process overhead outside high-value controls
