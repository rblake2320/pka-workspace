# v0.9.0 Pipeline Test Verdict — SENTINEL Final Verification
**Date**: 2026-05-14
**Reviewer**: SENTINEL
**Scope**: 10 defects found and fixed by FORGE during stale-reference scan
**Verdict**: GO — updated 2026-05-14 after pka_dream.py AGENTS list fix + WhyCase generated

---

## Stage 1: CRUCIBLE Verification (10 items)

| # | Defect | Severity | File | Verdict | Evidence |
|---|--------|----------|------|---------|----------|
| 1 | CHANGELOG.md — no v0.9.0 entry + merge conflict | Critical | CHANGELOG.md | VERIFIED | Lines 7-19: v0.9.0 entry present with full change list. Grep for `<<<<<<<`, `=======`, `>>>>>>>` returned zero matches. |
| 2 | VERSION — still read 0.8.0 | Critical | VERSION | VERIFIED | File content is exactly `0.9.0` followed by newline. No trailing garbage. |
| 3 | Team/roster.md — WRAITH missing | Critical | Team/roster.md | VERIFIED | Lines 114-118: WRAITH entry present with mission, activation date, and correct position description. Format matches other agents. |
| 4 | Team/CORE_RULES.md — Build route missing WRAITH | High | Team/CORE_RULES.md | VERIFIED | Line 137: Build route reads `FORGE -> CRUCIBLE (functional + Layer 3.5 security) -> WRAITH (adversarial red-team) -> SENTINEL`. WRAITH correctly positioned after CRUCIBLE, before SENTINEL. |
| 5 | governance/policy_cards/WRAITH.yaml — didn't exist | High | governance/policy_cards/WRAITH.yaml | VERIFIED | File exists, 41 lines. Schema matches FORGE.yaml structure. |
| 6 | Team/AGENT_TOOL_ENTITLEMENTS.json — WRAITH block missing | High | Team/AGENT_TOOL_ENTITLEMENTS.json | VERIFIED | Lines 219-239: WRAITH block present with risk_tier, allowed_actions, blocked_actions, escalation_required. JSON parses cleanly (validated via `python -c "import json; json.load(...)"`). |
| 7 | AGENTS.md — Maintenance section missing references | High | AGENTS.md | VERIFIED | Lines 44-47: trust_ledger, evidence, and CONFIDENCE_VOCABULARY references all present in Maintenance section. |
| 8 | Team/status.md — no v0.9.0 context or WRAITH note | High | Team/status.md | VERIFIED | Line 12: Workspace version shown as 0.9.0. Line 15: WRAITH activation noted with build route. |
| 9 | scripts/pka_dream.py — hardcoded /13 journal count | Medium | scripts/pka_dream.py | PARTIAL | Line 141: Display string now reads `/14`. However, the `AGENTS` list on lines 37-41 still contains only 13 entries — WRAITH is NOT in the list. The display says /14 but only 13 journals are actually scanned. See Stage 2 for details. |
| 10 | Team/hiring/process.md — no WRAITH hire log entry | Medium | Team/hiring/process.md | VERIFIED | Line 156: WRAITH hire log entry present with date, agent name, hired-by, and notes. |

**Summary**: 9/10 VERIFIED. 1/10 PARTIAL (defect #9 — incomplete fix).

---

## Stage 2: WRAITH Adversarial Pass

### Attack 1: CHANGELOG.md merge conflict residue
**Vector**: Search for git merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
**Result**: HELD. Grep returned zero matches across entire file. Conflict fully resolved.

### Attack 2: WRAITH.yaml schema conformance
**Vector**: Compare WRAITH.yaml field-by-field against FORGE.yaml reference.
**Result**: HELD. Both files share identical top-level schema:
- `agent_id`, `agent_version`, `owner`, `purpose`, `allowed_modes`, `prohibited_actions`, `permissions`, `data_classes_allowed`, `change_control`, `budgets`, `status_ttl` — all present in both.
- WRAITH has `fix_findings_directly` and `route_findings_to_forge_directly` in prohibited_actions — appropriate for a red-team agent that must route through SENTINEL.
- WRAITH includes `routes_findings_through: [SENTINEL]` under change_control — correct per routing table.
- WRAITH has `WebFetch` and `Task` in tools.allowed that FORGE does not — reasonable for an adversarial agent needing endpoint verification and task tracking.
- Budget is higher (150 calls / 45 min / $20 vs 100 / 30 / $15) — reasonable for adversarial work which is exploratory by nature.
**Severity**: N/A — no break found.

### Attack 3: AGENT_TOOL_ENTITLEMENTS.json syntax and permissions
**Vector**: Parse JSON programmatically; verify WRAITH permissions are appropriate for red-team role.
**Result**: HELD. JSON parses cleanly. WRAITH block contains:
- `risk_tier: "red_team"` — correct.
- `allowed_actions`: adversarial_attack, attack_surface_mapping, finding_documentation, test_suite_integrity_check, ai_specific_attack — all appropriate for red-team.
- `blocked_actions`: fix_findings_directly, route_to_forge_without_sentinel, self_issue_go_decision, skip_attack_surface_documentation — correct constraints.
- `escalation_required`: critical_finding, data_isolation_breach, prompt_injection_confirmed — appropriate escalation triggers.

### Attack 4: VERSION file content
**Vector**: Check for trailing whitespace, BOM, or extra characters.
**Result**: HELD. File is exactly `0.9.0\n` (6 bytes + newline). Clean.

### Attack 5: Team/roster.md WRAITH entry format
**Vector**: Compare WRAITH entry structure against other agent entries.
**Result**: HELD. WRAITH entry (lines 114-118) follows the same pattern as all other agents: `## NAME — Role *(activation context)*` followed by `**Mission:**` paragraph. The activation context uses `*(activated PKA Gap-Fill 2026-05-14)*` rather than `*(hired YYYY-MM-DD)*` — this is intentional and appropriate since WRAITH was activated as part of a gap-fill, not a standard hire.

### Attack 6: pka_dream.py — display vs. reality mismatch (BROKE)
**Vector**: The `/13` was changed to `/14` on line 141, but does the AGENTS list actually contain 14 agents?
**Result**: BROKE. The `AGENTS` list on lines 37-41 contains exactly 13 entries:
```python
AGENTS = [
    "AXIOM", "FORGE", "SENTINEL", "HELM", "NOVA",
    "VENTURE", "SPARK", "LEGAL", "SCRIBE", "GRID",
    "RADAR", "CRUCIBLE", "DEBUGGER",
]
```
WRAITH is missing. This means:
1. The orient phase will report `X/14` but only check 13 journals
2. WRAITH's journal will never be scanned for entries
3. WRAITH's journal health will never be reported
4. The dream report will silently under-count agent activity

**Severity**: Medium. This is a functional defect that will produce incorrect operational intelligence. It will not cause a crash or security issue, but it means WRAITH is invisible to the dream consolidation pipeline — a monitoring blind spot for the newest and most critical-path agent.

### Attack 7: Cross-file consistency — did fixes introduce new inconsistencies?
**Vector**: Check that CLAUDE.md agent count, roster count, and all `/14` references are consistent.
**Result**: HELD with one note.
- CLAUDE.md lists 14 agents (13 in Active Roster + WRAITH added as line 48). Consistent.
- Team/roster.md lists 14 agents. Consistent.
- HELM.md references "all 14 agents". Consistent.
- CHANGELOG.md says "14th agent". Consistent.
- The ONLY inconsistency is pka_dream.py as documented in Attack 6.

---

## Stage 3: SENTINEL Verdict

### Evidence Provenance

| Claim | Evidence Class | Source |
|-------|---------------|--------|
| CHANGELOG.md fixed | Tool receipt | Read file (lines 1-19) + Grep for conflict markers (0 matches) |
| VERSION is 0.9.0 | Tool receipt | Read file (line 1: `0.9.0`) |
| WRAITH in roster | Tool receipt | Read Team/roster.md (lines 114-118) |
| WRAITH in CORE_RULES routing | Tool receipt | Grep WRAITH in CORE_RULES.md (line 137) |
| WRAITH.yaml valid schema | Tool receipt | Read file (41 lines) + schema comparison with FORGE.yaml |
| WRAITH in entitlements JSON | Tool receipt | Read file (lines 219-239) + `python -c "import json"` parse (success) |
| AGENTS.md references present | Tool receipt | Grep trust_ledger/evidence/vocabulary in AGENTS.md (3 matches, lines 44-47) |
| status.md updated | Tool receipt | Read file (lines 12, 15) |
| pka_dream.py AGENTS list missing WRAITH | Tool receipt | Read file (lines 37-41: 13 entries, no WRAITH) + Grep WRAITH in file (0 matches) |
| hiring/process.md entry present | Tool receipt | Read file (line 156) |

### Decision Matrix Check

- Critical issues: 0 (all three Critical defects verified fixed)
- High issues: 0 (all five High defects verified fixed)
- Medium issues: 1 (pka_dream.py AGENTS list incomplete — display says /14 but only 13 agents scanned)
- Low issues: 0

Per the GO/NO-GO matrix: Zero Critical, Zero High, 1 Medium. This qualifies for GO if the Medium is either fixed or logged as accepted debt with timeline.

### Verdict: CONDITIONAL GO

**Condition**: The pka_dream.py defect (AGENTS list missing WRAITH) must be either:
- (a) Fixed before the next dream run, OR
- (b) Explicitly accepted by Ron as known debt with a fix ticket

This is not a blocker for the v0.9.0 workspace upgrade itself — all structural files (CHANGELOG, VERSION, roster, routing table, policy card, entitlements, status) are correct. The defect is in an operational intelligence script that will produce a cosmetically misleading but not harmful report.

If Ron accepts this as known debt: GO.
If Ron wants it fixed first: the fix is adding `"WRAITH"` to the AGENTS list on line 40 of `scripts/pka_dream.py`.

---

## Stage 4: WhyCase Recommendation

### Best WhyCase Candidate: Defect #9 — pka_dream.py incomplete fix

**Why this one qualifies best:**

**Root cause**: FORGE updated the display string (`/13` to `/14`) but did not update the data source (the `AGENTS` list) that drives the actual computation. The display and the logic diverged. This is a classic "fix the symptom, not the cause" pattern.

**whyNotCaught**: The original v0.9.0 installation process focused on adding new files (WRAITH.md, WRAITH.yaml, trust_ledger.md, etc.) and updating configuration files. It did not include a scan for hardcoded agent lists in Python scripts. The stale-reference scan that FORGE ran caught the `/13` string but treated it as a display-only fix rather than tracing the dependency chain to the `AGENTS` list that populates the `/N` denominator.

**preventNextTime**: Any agent list change must include a workspace-wide grep for the canonical agent name list pattern (`AGENTS = [`) and all files containing the old agent count as a literal. The fix checklist for "add new agent" should include:
1. Grep for the old count (e.g., `/13`, `13 agent`) across all files
2. Grep for agent list arrays in Python/JSON files
3. Verify that every list containing agent names includes the new agent
4. Run the affected script and verify the output matches the expected agent count

**Why not the other defects?** Defects 1-8 had straightforward root causes ("file X was not updated during installation") with obvious prevention ("add file X to the installation checklist"). Defect #9 is more instructive because it reveals a pattern where a surface-level fix masks a deeper structural gap — the display was fixed but the underlying data was not. This class of error recurs whenever a fix targets the visible output rather than the data flow.

---

*Report generated: 2026-05-14 by SENTINEL*
*Evidence: All claims backed by tool receipts (Read/Grep/Bash). No ungrounded claims.*
