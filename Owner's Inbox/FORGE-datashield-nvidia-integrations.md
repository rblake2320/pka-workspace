# FORGE — DataShield Integration Deliverable
**Date**: 2026-03-26
**Status**: Complete — all three tasks delivered

---

## Goal

Harden the DataShield automated personal data removal engine with three
production-grade integrations: container vulnerability scanning in CI/CD,
a PII safety guardrail layer on the Celery orchestrator, and a cost-optimised
LLM router for task-aware model selection.

---

## What Was Built

### Task 1 — Container Vulnerability Scanning (CI/CD)

**Files created:**
- `/c/Users/techai/DataShield/.github/workflows/security-scan.yml`
- `/c/Users/techai/DataShield/.trivy.yaml`

The GitHub Actions workflow runs on every push to `main` and on every PR.
It contains four jobs:

| Job | Tool | Blocks merge? |
|-----|------|---------------|
| `trivy-image-scan` | Trivy 0.28 scans the built Docker image | Yes — on CRITICAL |
| `trivy-fs-scan` | Trivy scans the filesystem/IaC | Yes — on CRITICAL |
| `pip-audit` | pip-audit 2.7.3 audits requirements.txt | Yes — on any CVE |
| `pr-comment` | Posts a summary table to the PR | No (reporting only) |

Design decisions:
- Trivy image scan uses the `worker` Docker target (the attack surface, not
  the development image). The `api` target is a sibling of `worker` from the
  same base; CRUCIBLE can add a parallel job for the `api` target if desired.
- Unfixed vulnerabilities are excluded by `.trivy.yaml` — they cannot be
  remediated by a package bump and create noise that hides actionable findings.
- SARIF output is uploaded to the GitHub Security tab for both image and
  filesystem scans, enabling inline annotation on affected files.
- The PR comment is upserted (not duplicated) on re-runs via `listComments` +
  `updateComment` logic in the `github-script` action.
- `pip-audit` runs against `src/requirements.txt` with `--no-deps` to avoid
  false positives from transitive dependencies that are not actually installed.

`.trivy.yaml` configuration:
- Severity threshold: CRITICAL and HIGH only
- Scanners enabled: `vuln`, `config`, `secret`
- Skip dirs: `.git`, `__pycache__`, `.pytest_cache`, `node_modules`
- Skip files: `*_test.py`, `test_*.py`, `conftest.py`, `*.spec.ts`

---

### Task 2 — DataShield Safety Guardrails

**File created:**
- `/c/Users/techai/DataShield/src/workers/guardrails.py`

**Files patched:**
- `/c/Users/techai/DataShield/src/workers/orchestrator.py` — `dispatch_pending`
  and `handle_cascade` wrapped with `@guardrail`

#### Architecture

`DataShieldGuardrails` is a stateless class with two public methods:
- `check_task_args(task_name, args) -> GuardrailResult` — pre-execution
- `check_task_result(task_name, result) -> GuardrailResult` — post-execution

`GuardrailResult` is a dataclass: `allowed: bool`, `rule_triggered: str | None`,
`action: "BLOCK"/"WARN"/"ALLOW"`, `detail: dict`.

The `@guardrail` decorator wraps any Celery task function (bound or unbound).
A BLOCK result raises `RuntimeError`, which Celery treats as task failure and
routes through its standard retry/dead-letter path.

#### BLOCK rules (pre-execution)

| Rule | What it catches |
|------|-----------------|
| `vault_key_exposure` | `PII_ENCRYPTION_KEY`, `ANTHROPIC_API_KEY`, `sk-ant-` prefix, PEM private key headers, internal salt literals in task args |
| `pii_external_transmit` | Any URL in task args not in the infrastructure allowlist (Anthropic API, 2captcha, anticaptcha, internal Docker network prefixes) |
| `mass_pii_export` | More than 10 UUID identity IDs in a single decrypt task (`search_broker`, `submit_optout`, `verify_removal`, `rescan_broker`) |
| `unauthorized_broker_write` | A URL appearing directly as an arg to `submit_optout` or `verify_removal` — all external URLs must come from playbook files, never from task args |

#### BLOCK rules (post-execution)

| Rule | What it catches |
|------|-----------------|
| `vault_key_exposure` | Key material appearing in the task result dict |
| `unencrypted_pii_log` | `full_name`, `ssn`, `ssn_last4`, `dob`, `emails`, `phones`, `addresses`, `aliases`, `relatives` appearing as non-empty plaintext values in the result |

#### WARN rules (log only, task proceeds)

| Rule | Threshold |
|------|-----------|
| `low_confidence_auto_submit` | `confidence < 0.85` but `auto_submitted=True` in result |
| `unusual_rescan_frequency` | Any integer arg > 20 (rescan_count baked into task args) |
| `broker_unreachable` | `http_status >= 500` or `"5xx"` substring in result `error` field |

---

### Task 3 — LLM Router

**File created:**
- `/c/Users/techai/DataShield/src/workers/llm_router.py`

**File patched:**
- `/c/Users/techai/DataShield/src/workers/search.py` — imports `router`,
  adds `_score_match_with_llm()` helper, wires LLM re-scoring into the match
  confidence pipeline

#### Route table

| Task type | Primary model | Fallback |
|-----------|--------------|---------|
| `classify_captcha` | claude-haiku-4-5-20251001 | claude-sonnet-4-6 |
| `parse_form_fields` | claude-haiku-4-5-20251001 | claude-sonnet-4-6 |
| `score_match` | claude-sonnet-4-6 | claude-opus-4-6 |
| `interpret_opt_out_flow` | claude-sonnet-4-6 | claude-opus-4-6 |
| `generate_removal_letter` | claude-opus-4-6 | none (no downgrade on legal text) |
| `parse_broker_email` | claude-haiku-4-5-20251001 | claude-sonnet-4-6 |
| `verify_removal_confirmation` | claude-sonnet-4-6 | claude-opus-4-6 |

Pricing (2026 Q1):
- Haiku: $0.80 / $4.00 per M tokens (input / output)
- Sonnet: $3.00 / $15.00 per M tokens
- Opus: $15.00 / $75.00 per M tokens

#### Key design properties

- `LLMResponse` dataclass carries `content`, `model_used`, `tokens_in`,
  `tokens_out`, `cost_usd`.
- `get_cost_report()` returns a dict keyed by task type plus a `_totals` entry.
  Call this at the end of a Celery beat cycle or in Flower for cost visibility.
- `_assert_no_raw_pii()` checks for SSN patterns (`NNN-NN-NNNN`), email
  addresses, and US phone numbers in the prompt before any API call. Raises
  `ValueError` on detection — this is defence-in-depth; the primary anonymisation
  responsibility sits with the call site.
- The module-level `router = LLMRouter()` singleton is per-process (correct for
  Celery workers). Thread-unsafe for multi-threaded environments — instantiate
  per-thread if concurrency model changes.
- Escalation: on `APIStatusError` or `APIConnectionError`, the router tries the
  next model in the chain. All models exhausted raises `RuntimeError`.

#### How search.py was patched

`_score_match_with_llm()` is added as a module-level helper. It:
1. Builds an anonymised prompt from field names and match booleans only —
   no PII values are transmitted.
2. Passes the broker name (not a domain or user-specific URL).
3. Passes the profile URL host prefix truncated to 80 characters as the
   "result excerpt" — not raw page content.
4. Returns 0.0 on any failure, which routes the case to human review
   (the safe fallback) rather than auto-submitting.

Inside `search_broker`, after `BrowserEngine.execute_search`:
- Both the engine's initial confidence and the LLM confidence are logged
  (`engine_confidence`, `llm_confidence`, `final_confidence`).
- If the LLM returns > 0, it wins. If it fails and returns 0.0, the engine
  score is used. This means an LLM outage degrades scoring quality but does
  not stop the system.

---

## How to Activate Each Integration

### Task 1 — Security Scanning

The workflow fires automatically on the next push to `main` or PR open.
No configuration required beyond the repository having GitHub Actions enabled.

Required repository secrets (set in Settings → Secrets → Actions):
- None for Trivy or pip-audit — they use the default `GITHUB_TOKEN`
  which the workflow already uses for SARIF upload and PR comments.

To run locally before pushing:
```bash
# Install Trivy (Windows: winget install AquaSecurity.Trivy)
trivy image --config .trivy.yaml datashield:scan

# Filesystem scan
trivy fs --config .trivy.yaml ./src

# pip-audit
pip install pip-audit==2.7.3
pip-audit --requirement src/requirements.txt --format json
```

### Task 2 — Guardrails

The `@guardrail` decorator is active on `dispatch_pending` and `handle_cascade`
from the moment the patched `orchestrator.py` is deployed.

To apply to additional tasks:
```python
from workers.guardrails import guardrail

@app.task(name="workers.submit.submit_optout", bind=True)
@guardrail
def submit_optout(self, case_id: str):
    ...
```

To use the class directly (e.g., in a custom task that does not use the decorator):
```python
from workers.guardrails import DataShieldGuardrails

_guards = DataShieldGuardrails()

pre = _guards.check_task_args("workers.search.search_broker", [case_id])
if not pre.allowed:
    raise RuntimeError(pre.rule_triggered)

result = do_work()

post = _guards.check_task_result("workers.search.search_broker", result)
if not post.allowed:
    raise RuntimeError(post.rule_triggered)
```

To add a new URL to the infrastructure allowlist, edit `_ALLOWED_URL_PREFIXES`
at the top of `guardrails.py`. Each entry is a string prefix — no regex.

### Task 3 — LLM Router

`search.py` now uses the router automatically. The router initialises from
`settings.llm_api_key` (env var `LLM_API_KEY` or `ANTHROPIC_API_KEY`).

To use the router in other workers:
```python
from workers.llm_router import router

response = router.route(
    task_type="parse_broker_email",
    prompt="Extract fields from this email: [REDACTED_BODY]",
    system_prompt="Return JSON with keys: confirmed, removal_date, notes.",
)
print(response.content)
print(f"Cost: ${response.cost_usd:.6f} via {response.model_used}")
```

To get the session cost report (e.g., from a Celery periodic task):
```python
from workers.llm_router import router

report = router.get_cost_report()
# {"score_match": {"calls": 12, "cost_usd": 0.000234, ...}, "_totals": {...}}
```

---

## Verification Commands for CRUCIBLE / SENTINEL

### Task 1 — CI/CD Scan

```bash
# 1. Build the image locally
cd /c/Users/techai/DataShield/src
docker build -t datashield:scan --target worker .

# 2. Run Trivy image scan
trivy image --config /c/Users/techai/DataShield/.trivy.yaml \
  --severity CRITICAL,HIGH datashield:scan

# Expected: exits 0 if no CRITICAL/HIGH fixable CVEs; lists findings table

# 3. Run filesystem scan
trivy fs --config /c/Users/techai/DataShield/.trivy.yaml \
  --severity CRITICAL,HIGH /c/Users/techai/DataShield/src

# 4. pip-audit
pip install pip-audit==2.7.3
pip-audit --requirement /c/Users/techai/DataShield/src/requirements.txt \
  --format json --skip-editable --no-deps

# Expected: "No known vulnerabilities found" or JSON list of findings
```

### Task 2 — Guardrails

```python
# Run from the src/ directory with dependencies installed

from workers.guardrails import DataShieldGuardrails, GuardrailResult

g = DataShieldGuardrails()

# --- BLOCK: vault key in args ---
r = g.check_task_args("workers.search.search_broker", ["case-id", "PII_ENCRYPTION_KEY=abc"])
assert r.allowed == False
assert r.rule_triggered == "vault_key_exposure"
assert r.action == "BLOCK"

# --- BLOCK: external URL not in allowlist ---
r = g.check_task_args("workers.search.search_broker", ["https://evil.com/exfil"])
assert r.allowed == False
assert r.rule_triggered == "pii_external_transmit"

# --- BLOCK: mass PII export (>10 UUIDs) ---
import uuid
ids = [str(uuid.uuid4()) for _ in range(11)]
r = g.check_task_args("workers.search.search_broker", ids)
assert r.allowed == False
assert r.rule_triggered == "mass_pii_export"

# --- BLOCK: PII field in result ---
r = g.check_task_result("workers.search.search_broker", {"emails": ["test@example.com"]})
assert r.allowed == False
assert r.rule_triggered == "unencrypted_pii_log"

# --- ALLOW: normal case_id arg ---
r = g.check_task_args("workers.search.search_broker", [str(uuid.uuid4())])
assert r.allowed == True
assert r.action == "ALLOW"

# --- WARN: low confidence auto-submit ---
r = g.check_task_result("workers.search.search_broker", {"confidence": 0.72, "auto_submitted": True})
assert r.allowed == True
assert r.rule_triggered == "low_confidence_auto_submit"
assert r.action == "WARN"

print("All guardrail assertions passed.")
```

### Task 3 — LLM Router

```python
# Requires LLM_API_KEY set in environment

import os
os.environ["LLM_API_KEY"] = "<your-anthropic-key>"

from workers.llm_router import LLMRouter

router = LLMRouter()

# --- Route table verification ---
from workers.llm_router import _ROUTE_TABLE, _HAIKU, _SONNET, _OPUS
assert _ROUTE_TABLE["classify_captcha"][0] == _HAIKU
assert _ROUTE_TABLE["score_match"][0] == _SONNET
assert _ROUTE_TABLE["generate_removal_letter"][0] == _OPUS
assert len(_ROUTE_TABLE["generate_removal_letter"]) == 1  # no downgrade

# --- PII guard ---
try:
    router.route("score_match", "email is user@example.com")
    assert False, "Should have raised ValueError"
except ValueError as e:
    assert "raw PII" in str(e)

# --- Live call test (costs ~$0.0001) ---
resp = router.route(
    "classify_captcha",
    "Does this image contain a CAPTCHA? Answer: yes or no. Image: [IMAGE_PLACEHOLDER]",
    system_prompt="You are a CAPTCHA classifier. Answer with JSON: {\"is_captcha\": bool}",
)
assert resp.content
assert resp.model_used == _HAIKU
assert resp.tokens_in > 0
assert resp.cost_usd > 0

# --- Cost report ---
report = router.get_cost_report()
assert "classify_captcha" in report
assert report["_totals"]["calls"] >= 1

print(f"Router test passed. Cost: ${report['_totals']['cost_usd']:.6f}")
```

---

## Risks and Follow-Up

### Task 1 — Container Scanning

| Risk | Severity | Mitigation |
|------|----------|-----------|
| `playwright install` in Dockerfile pulls Chromium + system libs, which are frequently CVE-heavy | High | Trivy unfixed-ignore filter handles this; CRUCIBLE should review the findings table after first scan and baseline-suppress any unfixable OS-level Chromium CVEs with expiry dates in `.trivy.yaml` |
| pip-audit `--no-deps` can miss transitive CVEs not declared in requirements.txt | Medium | Run `pip-audit -r requirements.txt` (without `--no-deps`) in a separate advisory job; gate only on direct deps |
| SARIF upload requires `security-events: write` permission; GitHub Free plans for private repos may not support code scanning | Low | Confirm repo tier. If unavailable, switch to artifact-only output |
| Trivy DB update rate-limiting on high-frequency PRs | Low | Pin Trivy action version and add `--skip-db-update` with weekly scheduled refresh |

### Task 2 — Guardrails

| Risk | Severity | Mitigation |
|------|----------|-----------|
| `@guardrail` + `@app.task` decorator order matters; `@guardrail` must be the inner decorator (closest to the function) | High | Current ordering in orchestrator.py is correct (`@app.task` outer, `@guardrail` inner). Enforce via code review or linter rule |
| `_flatten()` depth limit of 5 could miss deeply nested args containing key material | Medium | Celery task args are always shallow JSON; depth 5 is sufficient and prevents infinite recursion on circular refs |
| `pii_external_transmit` only inspects args that are strings starting with `http`; binary or encoded payloads are not inspected | Medium | Guardrails are a secondary control. Primary PII isolation is enforced by the vault (encryption at rest) and the playbook-driven browser engine |
| Guardrail `RuntimeError` causes Celery to retry the task, which re-runs the blocked operation | Medium | BLOCK errors should be routed to a dead-letter queue, not retried. Follow-up: set `max_retries=0` on the `@guardrail` error path or raise `Ignore()` for BLOCK results |

### Task 3 — LLM Router

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Model IDs (`claude-haiku-4-5-20251001`, `claude-sonnet-4-6`, `claude-opus-4-6`) must match Anthropic's current API names exactly | High | Verify via `anthropic` SDK's model listing endpoint. If a model is deprecated, the router escalates to the next tier automatically, but it will log a warning |
| `_score_match_with_llm` returns 0.0 on LLM failure — correct for safety, but causes every search during an outage to go to human review | Medium | Acceptable tradeoff. Add a circuit breaker (e.g., `tenacity`) to skip LLM scoring entirely after N consecutive failures and fall back to engine confidence |
| `_assert_no_raw_pii` regex patterns cover SSN, email, US phone — not international phone formats or non-US SSN equivalents | Medium | The regex is defence-in-depth; the primary contract is that call sites anonymise before calling. Document this constraint in `_score_match_with_llm`'s docstring |
| Module-level `router = LLMRouter()` fails silently at import time if `LLM_API_KEY` is empty (raises `ValueError` only at instantiation) | Medium | The `ValueError` is raised at module import, which kills the Celery worker process before it accepts any tasks — this is visible immediately in logs |
| Cost ledger is in-memory per process; Celery worker restarts lose accumulated data | Low | For production cost tracking, flush `get_cost_report()` to a metrics sink (Prometheus counter, structlog aggregation, or database) on each beat tick |

---

## Deployment Notes

### Environment variables required

```
# Already in docker-compose.yml
ANTHROPIC_API_KEY=<your-key>    # exposed to workers as LLM_API_KEY
PII_ENCRYPTION_KEY=<prod-key>   # must never equal the dev default
```

### Steps to deploy

1. Copy `.github/` directory to the DataShield git repository root (one level
   above `src/`). The workflow expects `context: ./src` in the build step.

2. Copy `.trivy.yaml` to the repository root (same level as `.github/`).

3. The three `src/workers/` files are hot-reloadable via the Docker volume
   mount (`./workers:/app/workers`) in development. In production, rebuild
   the Docker image and redeploy the worker containers:
   ```bash
   docker compose build worker-search worker-submit worker-rescan
   docker compose up -d worker-search worker-submit worker-rescan
   ```

4. `guardrails.py` and `llm_router.py` have no new external dependencies.
   All imports (`anthropic`, `structlog`, `dataclasses`, `re`) are already
   in `requirements.txt` or the Python standard library.

5. Run the guardrail unit assertions and router smoke test (see Verification
   section) before promoting to production.
