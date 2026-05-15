# Trust Ledger — PKA Agent Track Record

This file tracks per-agent, per-domain performance history.
AXIOM reads this at routing time to calibrate scrutiny level.
Updated by SENTINEL after every GO/NO-GO verdict.

---

## Schema

Each entry follows this structure:

```
## [AGENT_NAME]

### [DOMAIN] (e.g., auth, database, frontend, API, testing, research)
- Last verdict: GO / NO-GO / CONDITIONAL-GO
- Date: YYYY-MM-DD
- Task: [brief task description]
- Notes: [what passed, what failed, pattern observed]
- Trust score: HIGH / MEDIUM / LOW / PROBATION

### Track Record Summary
- Total tasks: N
- GO: N | NO-GO: N | CONDITIONAL: N
- Domains with LOW trust or PROBATION: [list]
- Last failure pattern: [description]
```

---

## Routing Escalation Rules (AXIOM enforces)

| Trust Score | AXIOM Action |
|-------------|-------------|
| HIGH | Standard routing; normal SENTINEL review |
| MEDIUM | SENTINEL review mandatory (not skippable) |
| LOW | WRAITH red-team mandatory before SENTINEL |
| PROBATION | HELM must approve task assignment; SENTINEL reviews mid-task, not just at end |

---

## Trust Score Update Rules (SENTINEL writes)

- 3 consecutive GOs in a domain → upgrade one level (max HIGH)
- 1 NO-GO in a domain → downgrade one level
- 2 NO-GOs in same domain within 30 days → PROBATION
- PROBATION cleared by: 5 consecutive GOs in that domain

---

## Agent Records

### FORGE

#### workspace-integrity
- Last verdict: CONDITIONAL-GO
- Date: 2026-05-14
- Task: Stale-reference scan — 10 defects found and fixed across v0.9.0 workspace artifacts
- Notes: 9/10 fixes verified correct. 1 partial fix (pka_dream.py: updated display string /13->/14 but did not add WRAITH to AGENTS list — display/data divergence). FORGE correctly identified all 10 defect locations including cross-file references. Strong diagnostic coverage. Weakness: surface-level fix on defect #9 missed the underlying data source.
- Trust score: MEDIUM

### DEBUGGER
*(No entries yet)*

### NOVA
*(No entries yet)*

### SENTINEL
*(Self-review not applicable — SENTINEL's track record tracked by AXIOM directly)*

### CRUCIBLE
*(No entries yet)*

### SCRIBE
*(No entries yet)*

### WRAITH
*(New agent — no entries yet)*

---

*Last updated: 2026-05-14 — SENTINEL (v0.9.0 stale-reference scan verdict)*
