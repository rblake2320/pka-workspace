# HELM: Council + AgentForge Integration Plan
*Agent: HELM | Task: TASK-20260402-010 | Date: 2026-04-02*
*Route: AXIOM -> HELM -> FORGE*

---

## 1. Feasibility Verdict

RADAR's "zero new engineering" claim is **partially accurate and partially wrong.**

The accurate part: no new services, no new infrastructure, no database changes, and no new
dependencies are required. The data already exists as flat files on disk.

The inaccurate part: pka_dream.py does require new code. The current `orient()` and `gather()`
functions are hardcoded to read exactly three data sources — PKA session logs in `logs/`,
PKA task records in `Team/tasks/`, and PKA agent journals in `Team/AGENT/journal.md`. None of
those paths point at Council or AgentForge. Reading external project data requires new logic
in both phases plus a new config structure. The work is small (one sitting, ~120 lines of
additions), but it is new engineering, not just config extension.

Corrected framing: "Low engineering cost — one focused session for an experienced builder,
no new dependencies, no new infrastructure."

---

## 2. Data Sources

### Council (`C:\Users\techai\council\`)

| File | What it contains | Maps to dream phase |
|------|-----------------|---------------------|
| `backend/exports/agent_self_model_evolution.jsonl` | 12 records. Each record: `agent_name`, `council_topic`, `council_title`, `observed_patterns`, `record_type`, `metadata` (with `council_id`, `exported_at`). Records are agent pattern observations from debate runs. | Gather — agent activity signal |
| `backend/exports/council_training_data.jsonl` | 39 multi-turn debate records. Each record: list of messages with `role` and `name` (agent name) and `content`. Represents completed debate sessions. | Gather — completed work count, active agent count |
| `backend/exports/agent_persona_training.jsonl` | 282 records. Each record: `messages` list + `metadata`. Training pairs generated from Council operation. | Gather — volume/activity signal |
| `backend/coverage.json` | Coverage.py output. Keys: `meta` (format, version, timestamp), `files` (per-file coverage), `totals` (covered_lines: 745, num_statements: 2751, percent_covered: 27.08%). Last run: 2026-03-29. | Gather — test coverage signal |
| `backend/tests/test_adversarial.py`, `test_debate_fixes.py`, `test_tools_and_loop.py` | Test file count only (no JUnit XML generated at rest). Dream reads presence + file count, not test results. | Orient — test file count |

**What Council does NOT have at rest:** JUnit XML test results, a pytest-generated report,
or any structured pass/fail file unless tests are actively run. Test count (128) is from
prior manual runs and is not persisted to disk in machine-readable form. Dream must read
what is actually on disk: export record counts and coverage.json, not test pass counts.

**Council agent count signal:** The `council_training_data.jsonl` records contain
`role`/`name` fields. Unique agent names can be extracted by scanning message names across
all records — this yields the set of active Council debate agents.

### AgentForge (`D:\agentvault\`)

| File | What it contains | Maps to dream phase |
|------|-----------------|---------------------|
| `flywheel_logs/*.jsonl` | 18 files, 19 total records (one agent has 2 entries). Each record: `ts` (ISO timestamp), `agent_id` (UUID), `intent` (task complexity label), `model`, `runtime`, `latency_ms`, `prompt_tokens`, `completion_tokens`. One record per agent invocation. | Gather — agent activity, runtime stats, latency |
| `backend/tests/*.py` (8 files) | Test files: `test_crypto.py`, `test_identity.py`, `test_marketplace.py`, `test_portability.py`, `test_rls.py`, `test_runtime.py`, `test_trust.py`, `test_wallet_tamper.py`. No JUnit XML at rest. | Orient — test file count |
| `pytest.ini` | Config: `testpaths = backend/tests`, `asyncio_mode = auto`. No `addopts` generating JUnit XML. | Meta context only |

**What AgentForge does NOT have at rest:** No JUnit XML, no coverage.json, no structured
test result file. The 34/34 pass count is from prior manual test runs. Dream reads what is
on disk: flywheel log records and test file presence.

**AgentForge agent count signal:** Each flywheel log file is named by `agent_id` (UUID).
Unique file count = registered agent count. At inspection: 18 unique agent IDs, 19 log
records.

---

## 3. The Change

### What changes in pka_dream.py

No changes to `pka_process_audit.py`. All changes are confined to `pka_dream.py`.

#### Step A: Add a config block at the top of pka_dream.py

Insert after the existing constants (`AGENTS`, `RETENTION_DAYS`, etc.):

```python
# --- External project integrations ---
# Each entry: display name, project root path, gather function name
# Set to empty list to disable all external project scanning.

EXTERNAL_PROJECTS: list[dict] = [
    {
        "name": "Council",
        "root": Path(r"C:\Users\techai\council"),
        "type": "council",
    },
    {
        "name": "AgentForge",
        "root": Path(r"D:\agentvault"),
        "type": "agentforge",
    },
]
```

This is the "configurable project list" RADAR described. Adding or removing a project
requires only editing this list — FORGE does not need to change any function signatures.

#### Step B: Add gather functions for each project type

Add two new functions to pka_dream.py:

**`gather_council(root: Path) -> dict`**

Reads from `root / "backend" / "exports"` and `root / "backend" / "coverage.json"`.

Returns:
```python
{
    "name": "Council",
    "available": True,         # False if root doesn't exist
    "debate_records": int,     # line count of council_training_data.jsonl
    "agent_observations": int, # line count of agent_self_model_evolution.jsonl
    "training_pairs": int,     # line count of agent_persona_training.jsonl
    "coverage_pct": float,     # from coverage.json totals.percent_covered (or None)
    "coverage_ts": str,        # from coverage.json meta.timestamp (or None)
    "test_files": int,         # count of test_*.py in backend/tests/
    "active_agents": int,      # unique agent names in council_training_data.jsonl messages
}
```

Logic: count lines in each JSONL file (skip blank lines). Extract unique agent names from
`council_training_data.jsonl` by parsing message `name` fields. Read `coverage.json` with
`json.loads`. If any file is missing, set its value to 0 or None and continue — never raise.

**`gather_agentforge(root: Path) -> dict`**

Reads from `root / "flywheel_logs"` and `root / "backend" / "tests"`.

Returns:
```python
{
    "name": "AgentForge",
    "available": True,          # False if root doesn't exist
    "registered_agents": int,   # count of *.jsonl files in flywheel_logs/
    "flywheel_records": int,    # total line count across all flywheel JSONL files
    "avg_latency_ms": float,    # mean latency_ms across all records (or None if 0 records)
    "intents": dict,            # Counter of intent values (e.g. {"complex": 18, "simple": 1})
    "test_files": int,          # count of test_*.py in backend/tests/
}
```

Logic: glob `flywheel_logs/*.jsonl`, parse each record's `latency_ms` and `intent` fields,
aggregate. If a field is missing in a record, skip that field contribution silently.

#### Step C: Wire into orient()

Add to the return dict of `orient()`:

```python
"external_projects": [
    {"name": p["name"], "available": p["root"].exists()}
    for p in EXTERNAL_PROJECTS
]
```

This gives the Orient phase a count of configured vs available external projects.

#### Step D: Wire into gather()

At the end of `gather()`, before the return statement, add:

```python
ext_data = []
for proj in EXTERNAL_PROJECTS:
    if not proj["root"].exists():
        ext_data.append({"name": proj["name"], "available": False})
        continue
    if proj["type"] == "council":
        ext_data.append(gather_council(proj["root"]))
    elif proj["type"] == "agentforge":
        ext_data.append(gather_agentforge(proj["root"]))
```

Add `"external_projects": ext_data` to the gather return dict.

#### Step E: Wire into consolidate()

Add a new section in the consolidate report string between Phase 2 and Phase 3:

```
## External Projects

### Council
- Debate records: {n}
- Agent observations: {n}
- Training pairs: {n}
- Test files: {n}
- Active agents in debates: {n}
- Code coverage: {pct}% (as of {ts})

### AgentForge
- Registered agents: {n}
- Flywheel log records: {n}
- Test files: {n}
- Intent distribution: {intents}
- Avg agent latency: {ms}ms
```

If `available` is False for a project, output: `- {name}: NOT AVAILABLE (root path missing)`.

### Total scope of change
- ~120 lines added to pka_dream.py
- No changes to any other PKA script
- No new imports beyond what is already in pka_dream.py (pathlib, json, re, Counter are
  all already imported)
- No new config files required (config block lives in pka_dream.py itself)

---

## 4. Process Audit Impact

`pka_process_audit.py` is **not at risk.** Here is why:

The audit script operates on exactly these paths:
- `Team/tasks/*.md` — task record frontmatter
- `Team/status.md` — status board
- `Team/handoff.md` — session handoff
- `Owner's Inbox/DELIVERY_MANIFEST.md` — delivery table
- `Team/AGENT/journal.md` — agent journals (for delivered task cross-reference)

None of those paths overlap with Council or AgentForge. The audit script has no awareness
of `EXTERNAL_PROJECTS` and will never read anything from `C:\Users\techai\council\` or
`D:\agentvault\`.

The one indirect risk: if FORGE introduces a syntax error into pka_dream.py that also breaks
pka_lib.py (which both scripts import), pka_process_audit.py would fail on import. This is
prevented by the acceptance criterion below: pka_process_audit.py must pass before and after
the change.

**Prevention:** FORGE runs `python scripts/pka_process_audit.py` both before making any
changes (to confirm baseline is clean) and after making all changes (to confirm no
regression). This is a mandatory step in the task brief.

---

## 5. Sequencing

**Integrate both projects in a single session, not sequentially.**

Reasoning:

1. The config block, the orient() extension, the gather() extension, and the consolidate()
   extension are all single-function changes in one file. The plumbing is identical for both
   projects. Writing it once for Council and then again for AgentForge in a second session
   doubles the risk of inconsistency between the two implementations.

2. The `gather_council` and `gather_agentforge` functions are independent of each other.
   Neither calls the other. There is no dependency that would require one to be validated
   before the other is written.

3. The risk of doing both simultaneously is low because both projects are read-only from
   dream's perspective. A bug in `gather_agentforge` cannot corrupt Council data and vice
   versa. If one gather function errors, wrapping it in a try/except that sets
   `available: False` isolates the failure.

4. Splitting across two sessions creates a half-integrated state where the dream report
   mentions Council but not AgentForge — this would require FORGE to touch pka_dream.py
   twice and run the full validation pass twice.

---

## 6. Handoff to FORGE

**Task: Extend pka_dream.py with Council and AgentForge gather support**

### Inputs
- `C:\Users\techai\PKA testing\scripts\pka_dream.py` — the file to modify
- `C:\Users\techai\council\` — Council project root (read-only)
- `D:\agentvault\` — AgentForge project root (read-only)
- This plan document (reference for exact field names and logic)

### What to build

1. Add the `EXTERNAL_PROJECTS` config list (Section 3, Step A) after the `AGENTS` constant
   in pka_dream.py. Use verbatim paths from this plan.

2. Add `gather_council(root: Path) -> dict` (Section 3, Step B). The function must:
   - Return `{"name": "Council", "available": False}` immediately if `root` does not exist
   - Count lines in `backend/exports/council_training_data.jsonl` (skip blank lines)
   - Count lines in `backend/exports/agent_self_model_evolution.jsonl`
   - Count lines in `backend/exports/agent_persona_training.jsonl`
   - Count `test_*.py` files in `backend/tests/`
   - Read `backend/coverage.json` and extract `totals.percent_covered` and `meta.timestamp`
   - Count unique agent names from `council_training_data.jsonl` message `name` fields
   - Wrap all file reads in try/except — missing file yields 0 or None, never raises

3. Add `gather_agentforge(root: Path) -> dict` (Section 3, Step B). The function must:
   - Return `{"name": "AgentForge", "available": False}` immediately if `root` does not exist
   - Count `*.jsonl` files in `flywheel_logs/` (= registered agent count)
   - Count total lines across all flywheel JSONL files (= record count)
   - Compute mean `latency_ms` across all parsed records
   - Build a Counter of `intent` field values
   - Count `test_*.py` files in `backend/tests/`
   - Wrap all file reads in try/except

4. Extend `orient()` to include external project availability (Section 3, Step C).

5. Extend `gather()` to call the two new functions and include results under
   `"external_projects"` key (Section 3, Step D).

6. Extend `consolidate()` to render the External Projects section in the report output
   (Section 3, Step E). It must render gracefully when `available` is False.

### Acceptance criteria

1. `python scripts/pka_process_audit.py` exits 0 before the change is made (FORGE verifies
   current baseline).
2. `python scripts/pka_dream.py` runs to completion without error after the change.
3. `Owner's Inbox/reports/PKA_DREAM_REPORT.md` contains an "External Projects" section
   with non-zero values for at least one field in both Council and AgentForge blocks.
4. `python scripts/pka_process_audit.py` exits 0 after the change (no regression).
5. If either project root is temporarily renamed/missing, pka_dream.py still completes and
   reports `NOT AVAILABLE` rather than raising an exception.

### What FORGE must NOT do
- Do not modify pka_process_audit.py, pka_lib.py, or any other PKA script
- Do not run pytest against Council or AgentForge — dream is read-only
- Do not add any new pip dependencies; all needed imports (json, pathlib, Counter, re) are
  already present in pka_dream.py

### Deliverable
Updated `C:\Users\techai\PKA testing\scripts\pka_dream.py` with the integration in place,
plus a brief verification note (10 lines max) confirming all 5 acceptance criteria passed,
delivered to `Owner's Inbox\`.

---

## Open Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Council or AgentForge root path changes in future | Low | EXTERNAL_PROJECTS config block is at the top of the file — one-line update |
| flywheel_logs grows to thousands of files, slowing gather | Low (currently 18 files, 19 records) | Add a `MAX_FLYWHEEL_FILES = 500` cap in gather_agentforge with a truncation note |
| council_training_data.jsonl has malformed JSON lines | Low (generated by Council backend) | Line-level try/except in the agent name extraction loop |
| pka_dream.py lock file left behind from crashed run blocks next run | Pre-existing risk, not introduced here | No change to lock behavior required |
| FORGE interprets "configurable project list" as requiring a separate .json config file | Medium — RADAR's wording is ambiguous | This plan specifies the config block lives in pka_dream.py itself as a Python list |

---

*HELM out. Routing to FORGE for execution.*
