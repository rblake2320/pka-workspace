---
task_id: "TASK-20260401-006"
title: "Rebuild PKA scorecard with real task history metrics"
state: "delivered"
priority: "high"
owner: "FORGE"
route:
  - "AXIOM"
  - "FORGE"
  - "SENTINEL"
intake_file: ""
deliverable_file: "scripts/pka_scorecard.py"
verdict: "GO"
created_at: "2026-04-01"
updated_at: "2026-04-01"
definition_of_done: "python scripts/pka_scorecard.py outputs score based only on delivered operational tasks, process/meta tasks excluded, manifest lookup by task_id not title, evidence section checked for non-placeholder content"
blockers: []
---

# Task Summary

## Objective
Eliminate circular/self-referential scoring in pka_scorecard.py. Scorecard must derive all scores from real operational task history in Team/tasks/, never from process meta-tasks or its own existence.

## Context
Original scorecard (pka_competitive_eval.py) scored itself and used process tasks to inflate metrics. Codex rebuilt as pka_scorecard.py: filters via is_operational_task(), indexes DELIVERY_MANIFEST.md by task_id, scores throughput/evidence/verdict/defects from real delivered work only. Zero operational tasks = zero score by design.

## Evidence Required
- `scripts/pka_scorecard.py` exists, replaces `pka_competitive_eval.py` (deleted)
- `is_operational_task()` excludes process/hardening/scorecard/manifest/session-gate/operating-model/task-ledger/audit-script/control-layer tasks
- `manifest_task_ids()` reads DELIVERY_MANIFEST.md and indexes by task_id column (parts[1]), not title
- `has_non_placeholder_evidence()` returns False for "[Add evidence requirements]" placeholder lines
- `python scripts/pka_scorecard.py` output: 85/100 with 2 operational tasks before this session's additions
- Circular scoring eliminated: zero real tasks → zero score by design

## Notes
- Delivered by Codex (codex-agent) on Spark-1, 2026-04-01
- Verified by Claude Code (PKA orchestrator): E2E test pass, manifest ID lookup bug found and fixed post-delivery
