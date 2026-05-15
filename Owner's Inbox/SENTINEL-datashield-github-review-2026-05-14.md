# SENTINEL Review - DataShield GitHub

Date: 2026-05-14  
Repo: `https://github.com/rblake2320/DataShield.git`  
Commit reviewed: `f1ee431a00fe604db1041a675f38881a08002ec0` on `main`  
Verdict: HOLD for production or real customer PII. GO only as a prototype/security-hardening baseline.

## Executive Take

DataShield has a credible shape: FastAPI, Postgres, Celery, Playwright, encrypted PII fields, playbook validation, and a useful CLI harness. The core `src` test suite is broad for playbook/schema behavior and currently passes.

It is not production-ready for a privacy product handling PII. The biggest blockers are deployment schema drift, ineffective tenant isolation, production-unsafe defaults, broken harness auth integration, and dependency vulnerabilities that the GitHub Actions audit likely does not enforce correctly.

## Verification Run

- `git clone https://github.com/rblake2320/DataShield.git _reviews/DataShield` - clean clone.
- `git rev-parse HEAD` - `f1ee431a00fe604db1041a675f38881a08002ec0`.
- `python -m pytest tests -q` from `src/` - `399 passed, 27 skipped`.
- `python -m compileall api browser workers config scripts tests` from `src/` - pass.
- `python -m pytest tests -q` from `agent-harness/` - `12 failed, 44 passed, 6 skipped`.
- `python -m ruff check src agent-harness` - fail, `215 errors`.
- `python -m bandit -r src/api src/browser src/workers src/config -q` - 22 low-severity findings, no medium/high.
- `python -m pip_audit -r src/requirements.txt` - fail, 34 known vulnerabilities in 7 packages.

## P0 Findings

### 1. Fresh Docker deployments do not apply the schema the app expects

`src/docker-compose.yml:13-14` mounts only `migrations/001_init.sql` into Postgres init. But later code depends on migrations 003-006: `tenants`, `tenant_id` columns, `guided_actions`, `dark_web_alerts`, and `webhook_endpoints`.

Evidence:
- `src/migrations/001_init.sql:72-92` creates `identities` without `tenant_id`.
- `src/api/models.py:64-67` maps `Identity.tenant_id`.
- `src/migrations/003_multi_tenant.sql:9-32` creates `tenants` and adds tenant columns.
- `src/migrations/006_webhook_endpoints.sql:4-13` creates `webhook_endpoints`.
- `src/migrations/alembic/` has `env.py` and `script.py.mako`, but no versioned Alembic migration files.

Impact: a clean `docker compose up` can produce a database that passes health checks but fails as soon as tenant-aware API paths insert/query ORM fields not present in the database. This is a launch blocker.

Fix: replace one-off mounted SQL with a real migration runner at startup, or mount/apply all ordered SQL migrations in a deterministic init path. Add a smoke test that starts a fresh DB and performs create identity, scan, public API create/list/status, and webhook registration.

### 2. Tenant isolation is caller-controlled, not auth-controlled

The public API uses one global API key set and lets the request body/header select `tenant_id`. It also allows omission of `X-Tenant-Id` for list calls, which returns all identities.

Evidence:
- `src/api/public_api.py:41-45` validates only membership in `settings.api_key_set`, not tenant ownership.
- `src/api/public_api.py:100` accepts `x_tenant_id` directly from request headers.
- `src/api/public_api.py:143-155` writes whichever tenant UUID the caller supplies.
- `src/api/public_api.py:240-265` lists all removals if `X-Tenant-Id` is omitted.
- `src/api/public_api.py:192-235` returns removal status by raw `removal_id` without tenant scoping.
- `src/api/public_api.py:108-114` deduplicates by global `identity_hash`, so the same person across tenants collides.
- `src/api/models.py:64` makes `identity_hash` globally unique.

Impact: any valid API key can create, enumerate, or inspect data across tenants by choosing or omitting tenant headers. For a PII product, this is a hard HOLD.

Fix: bind API keys to tenant IDs server-side, derive tenant context from authenticated credentials, remove user-supplied tenant selection except for privileged admin paths, and make identity dedup unique per tenant.

### 3. Production-unsafe secrets are accepted silently

The app still has usable dev defaults for the PII key and API key, and Docker Compose defaults to them.

Evidence:
- `src/config/settings.py:20` defaults `pii_encryption_key` to the base64 encoding of 32 null bytes.
- `src/config/settings.py:90` defaults `api_keys` to `dev-api-key-change-in-production`.
- `src/docker-compose.yml:47`, `74`, `100`, `129`, `154` default `PII_ENCRYPTION_KEY` to the null key.
- `src/docker-compose.yml:49` defaults `API_KEYS` to the dev key.
- `src/docker-compose.yml:9` defaults the Postgres password to `dra_dev_2026`.

Impact: a misconfigured deployment encrypts all PII with a public key and exposes protected endpoints to a public dev API key.

Fix: fail startup unless explicit non-dev secrets are set outside a declared local/dev environment. Add a boot-time settings validator and tests for rejected defaults.

## P1 Findings

### 4. GitHub dependency audit likely false-passes while vulnerable dependencies are present

Local `pip-audit` found 34 known vulnerabilities in `python-multipart`, `cryptography`, `aiohttp`, `Pillow`, `python-dotenv`, `pytest`, and transitive `starlette`.

The GitHub workflow tries to capture the pip-audit exit code after piping to `tee`, but without `set -o pipefail`, `$?` is the `tee` exit code, not the audit exit code.

Evidence:
- `.github/workflows/security-scan.yml:147-158` runs `pip-audit ... 2>&1 | tee ...` then writes `PIP_AUDIT_EXIT=$?`.
- `.github/workflows/security-scan.yml:170-174` only fails if that env var is nonzero.

Impact: dependency vulnerabilities can appear as passing CI.

Fix: add `set -o pipefail` before the command or avoid the pipe. Also add normal test/lint jobs; the current workflow is security-only.

### 5. CLI harness is out of sync with API authentication

The API now requires `X-API-Key` on protected endpoints, but the harness client never sends it.

Evidence:
- `src/api/main.py:54-58` enforces `X-API-Key`.
- `agent-harness/cli_anything/datashield/core/client.py:31-32` sends only `Content-Type` and `Accept`.
- `agent-harness/tests/test_full_e2e.py:28-37` considers the server reachable via unauthenticated `/api/health`, then exercises protected endpoints unauthenticated.

Observed result: `agent-harness` E2E run failed with 12 auth failures against `localhost:8000`.

Fix: support `DATASHIELD_API_KEY` and `--api-key`, send `X-API-Key`, and make the E2E reachability check verify an authenticated endpoint or skip with a clear missing-key reason.

### 6. Billing endpoints are not authenticated or tenant-bound

`/billing/checkout` and `/billing/status` are included in the app without API key dependency. The checkout request accepts an arbitrary `tenant_id`, and status returns subscription data for any supplied tenant UUID.

Evidence:
- `src/api/main.py:120` includes `billing_router`.
- `src/api/billing.py:42-45` accepts `tenant_id` in request body.
- `src/api/billing.py:50` creates checkout without auth.
- `src/api/billing.py:189-209` returns billing status by raw query param.

Impact: tenant billing metadata can be enumerated, and checkout sessions can be initiated for tenants the caller does not own.

Fix: require tenant-bound auth for billing routes. Treat Stripe webhooks as the only unauthenticated billing path, protected by Stripe signature verification.

### 7. Webhook registration accepts insecure URLs and stores secrets plaintext

Webhook registration allows `http://` destinations and stores the provided signing secret directly.

Evidence:
- `src/api/public_api.py:339` accepts both `http://` and `https://`.
- `src/api/public_api.py:345-350` stores `secret=req.secret`.
- `src/api/models.py:395-396` notes the secret should be hashed in prod, but the model stores plaintext.

Impact: if event delivery is added or already exists elsewhere, this becomes SSRF/data-exfiltration surface and leaks signing secrets to DB readers/backups.

Fix: require HTTPS, block private/link-local metadata networks, verify endpoint ownership, generate server-side signing secrets, and store only hashed/derivable forms when possible.

## P2 Findings

### 8. Lint posture is not clean and is not enforced

`python -m ruff check src agent-harness` found 215 issues, mostly import ordering, unused imports, modern typing, and style correctness. Many are fixable automatically, but the signal matters because CI does not run ruff.

Fix: add `ruff check` and `ruff format --check` to CI, then fix or explicitly configure the rule set.

### 9. Test coverage is skewed toward schema/playbook checks

The passing `src` suite is valuable, but it is mostly playbook validation. It does not currently prove a clean Docker deployment, migration application, tenant isolation, auth enforcement, billing ownership, webhook safety, or worker happy paths.

Fix: add integration tests around a fresh Postgres service and API lifecycle, plus negative security tests for cross-tenant access and default-secret startup rejection.

### 10. Product/docs overstate implementation maturity

The README says React dashboard and 200+ broker coverage. The repo has static HTML dashboards and 47-ish broker playbooks, plus platform/registry/group playbooks. That is not fatal, but it will create operator and investor trust issues.

Fix: tighten docs to current reality: "static monitoring dashboard" unless React is actually introduced, and publish exact broker/playbook counts generated from the repo.

## Strengths

- PII vault uses AES-GCM with random nonces and validates key length.
- Protected endpoints now require API keys in the main API.
- Playbook schema tests are substantial and passing.
- Worker architecture is separated by search, submit, verify, rescan, supporting monitors.
- There is a serious attempt at guardrails around PII and LLM prompts.

## Recommended Fix Order

1. Fix migrations/deployment first: all SQL migrations must apply in clean Docker and CI.
2. Replace global API keys with tenant-bound auth and server-derived tenant context.
3. Add production startup checks that reject dev API keys, null PII keys, and default DB passwords.
4. Fix billing route auth and public API cross-tenant reads.
5. Repair CI: `pipefail`, dependency updates, pytest, ruff, and a Docker smoke test.
6. Update the CLI harness to send API keys and restore E2E pass.
7. Harden webhook registration before enabling event delivery.

## Final Verdict

HOLD for production/customer PII. The concept and codebase are salvageable, and the core suite passing is a good base. The current repo should be treated as a prototype until schema deployment, tenant isolation, secret validation, and CI enforcement are corrected and retested end to end.
