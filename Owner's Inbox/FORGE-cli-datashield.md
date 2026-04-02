# FORGE Deliverable — datashield-cli Harness

**Build**: CLI-Anything harness for DataShield Data Removal Agent
**Date**: 2026-03-30
**Status**: COMPLETE — 37/37 unit tests passing, entry point verified

---

## Goal

Provide a complete, installable CLI harness that exposes every DataShield
REST API endpoint through a structured, agent-friendly command interface.
Targets `C:\Users\techai\DataShield\` — the automated personal data removal
platform with PII encryption, broker playbooks, and Celery workers.

---

## Architecture

### What I read before writing a line of code

- `src/api/main.py` — all 14 API endpoints, exact routes and parameters
- `src/api/schemas.py` — every request/response shape
- `src/api/pii_vault.py` — AES-256-GCM encryption model (PII is server-side only)
- `src/config/settings.py` — environment variables and port (8000)
- `src/workers/guardrails.py` — safety rules (informed --dry-run placement)
- `src/workers/llm_router.py` — LLM routing (no CLI surface needed here)
- `src/browser/ocr_client.py` — OCR is a toolkit shim, not exposed via REST API
- `src/docker-compose.yml` — confirmed API port 8000
- `D:\memory-web\agent-harness\` — the established pattern this harness follows

### What the actual API surface is

After reading the code: DataShield is a **data removal orchestration system**,
not a generic PII scanner. The API has 14 endpoints across these domains:

| Domain    | Endpoints |
|-----------|-----------|
| Health    | GET /api/health |
| Dashboard | GET /api/dashboard/summary, GET /api/dashboard/kpis |
| Identity  | GET/POST /api/identities, GET/DELETE /api/identities/{id} |
| Broker    | GET/POST /api/brokers |
| Case      | GET /api/cases, POST /api/cases/{id}/action |
| Event     | GET /api/events |
| Scan      | POST /api/scan |
| Breach    | GET /api/breaches |

**Important design decision**: the task spec listed `ocr`, `classify`, `guard`,
and `route` as subcommand groups. These capabilities exist in DataShield's
workers but are NOT exposed as REST endpoints. The OCR client is a toolkit
shim with no HTTP endpoint; guardrails and LLM routing run inside Celery workers,
not via API. Building CLI subcommands for non-existent endpoints would be
"nothing presented as something" — a direct violation of FORGE law. The CLI
exposes only what exists.

### Component layout

```
C:\Users\techai\DataShield\agent-harness\
├── setup.py
├── DATASHIELD.md                            SOP
├── tests\
│   ├── test_core.py                         37 unit tests
│   └── test_full_e2e.py                     E2E tests (server-gated)
└── cli_anything\datashield\
    ├── datashield_cli.py                    Click CLI, all commands
    ├── __main__.py
    ├── core\
    │   └── client.py                        urllib-only HTTP client
    └── utils\
        └── output.py                        human-readable formatters
```

Follows the `cli_anything` namespace package pattern established by
`D:\memory-web\agent-harness\`.

---

## Implementation

### Entry point

```
datashield-cli [OPTIONS] COMMAND [ARGS]
```

### All subcommands

| Command | Description |
|---------|-------------|
| `health` | GET /api/health liveness check |
| `dashboard summary` | Live case status counts |
| `dashboard kpis [--days N]` | KPI history window |
| `identity list` | All identities with decrypted PII |
| `identity get <uuid>` | Full identity detail |
| `identity create --name <n>` | Create identity (--dry-run supported) |
| `identity delete <uuid>` | Delete identity + cascade (--dry-run) |
| `broker list [--all]` | Active brokers with success rates |
| `broker add --name --domain` | Register new broker (--dry-run) |
| `scan start <identity-id>` | Queue broker scans (--dry-run) |
| `case list [filters]` | Cases with status/identity/broker/review filters |
| `case action <id> <action>` | approve/reject/retry/escalate/skip (--dry-run) |
| `event list [filters]` | Audit trail events |
| `breach list [filters]` | HIBP breach alerts |
| `shell` | Interactive REPL (default when no subcommand) |

### Key design decisions

**--dry-run on every write operation**: `identity create`, `identity delete`,
`broker add`, `scan start`, and `case action` all support `--dry-run`.
The flag is enforced client-side — no HTTP call is made, exit 0. This is
critical because DataShield handles real PII and triggers real opt-out
workflows against live broker sites.

**--json everywhere**: Every command accepts `--json`. Outputs to stdout.
Errors produce `{"error": "..."}` and exit 1. Designed for AI agent
consumption and piping to `jq`.

**urllib only**: No `requests` dependency. The client uses only Python
stdlib `urllib.request`, matching the MemoryWeb harness pattern.

**DATASHIELD_URL env var**: Base URL is read from the environment so no
config file is needed. Works with `--base-url` override per-command.

**PII safety**: The CLI never sees raw encrypted PII bytes. The DataShield
server decrypts on read and encrypts on write. The CLI just passes JSON
payloads and receives JSON responses.

---

## Validation

### Unit tests — run without a live server

```
C:\Python312\python.exe -m pytest tests/test_core.py -v
```

**Result: 37/37 PASSED** (verified 2026-03-30)

Test coverage:
- Client `__init__`: default URL, env var override, explicit override, trailing slash
- Client headers: Content-Type and Accept
- HTTP error handling: RuntimeError on 4xx/5xx, ConnectionError on URLError
- health(): calls /api/health with GET, parses response
- initiate_scan(): body construction, broker_ids handling
- case_action(): body construction, URL routing
- list_cases(): query parameter construction
- Output formatters: all 8 formatters including empty-state handling
- CLI structure: help exits 0, version string, all --dry-run paths
- --dry-run JSON mode: produces `{"dry_run": true, "operation": "..."}` with exit 0
- Invalid case action: rejected by Click choice validation

### Entry point verification

```
datashield-cli --help     # Shows all 9 command groups
datashield-cli --version  # datashield-cli, version 1.0.0
```

Confirmed working.

### E2E tests (when server is running)

```
C:\Python312\python.exe -m pytest tests/test_full_e2e.py -v
```

Tests auto-skip if server is unreachable (no false failures). When live:
- Health check
- Dashboard summary and KPIs
- Full identity lifecycle: create → list → get → delete
- Scan lifecycle: create identity → scan → list cases → cleanup
- Broker listing
- Breach listing
- Dry-run safety: verified against port 19999 (no server) — exits 0

---

## Risks

**Risk 1: API not running**
The CLI exits 1 with a clear message: "Cannot connect to DataShield at
http://localhost:8000. Is the server running?" In JSON mode this is
`{"error": "..."}`. E2E tests skip gracefully.

**Risk 2: Identity UUID not known to user**
Users must first run `identity list` to get the UUID before running `scan start`
or `case action`. The REPL and `--json` output make this workflow smooth.
A future enhancement: `scan start --name "Jane Smith"` that resolves by name.

**Risk 3: Case action on wrong case**
All write operations support `--dry-run` for preview. For `case action`, the
action choices are validated by Click — typos fail immediately with a clear
usage error.

**Risk 4: Docker not running**
DataShield's API depends on Postgres 5433 and Redis 6380 (both in Docker).
The `health` command will fail with a connection error if Docker is down.
The error message is clear and actionable.

**Risk 5: PII exposure via CLI history**
`identity create` takes `--name`, `--email`, etc. as command-line arguments,
which may appear in shell history. For production use, consider using the REPL
(which reads from stdin interactively) or piping from a file.

---

## Deployment Notes

### Install

```bash
cd C:\Users\techai\DataShield\agent-harness
C:\Python312\python.exe -m pip install -e .
```

### Start the API (if not already running)

```bash
cd C:\Users\techai\DataShield\src
docker-compose up -d
```

Wait ~10 seconds, then:

```bash
datashield-cli health
```

### Point to a remote instance

```bash
$env:DATASHIELD_URL = "http://192.168.12.132:8000"
datashield-cli health
```

### Agent usage pattern

```bash
# Get all identities as JSON
datashield-cli --json identity list | python -c "import sys,json; [print(x['id']) for x in json.load(sys.stdin)]"

# Start scan for all identities
datashield-cli --json identity list | python -c "
import sys, json, subprocess
for i in json.load(sys.stdin):
    subprocess.run(['datashield-cli', '--json', 'scan', 'start', str(i['id'])])
"

# Review queue: all cases needing human attention
datashield-cli --json case list --review

# Approve a case
datashield-cli --json case action <case-uuid> approve
```

---

## File Locations

| File | Path |
|------|------|
| Entry point script | `C:\Users\techai\DataShield\agent-harness\cli_anything\datashield\datashield_cli.py` |
| HTTP client | `C:\Users\techai\DataShield\agent-harness\cli_anything\datashield\core\client.py` |
| Output formatters | `C:\Users\techai\DataShield\agent-harness\cli_anything\datashield\utils\output.py` |
| Unit tests | `C:\Users\techai\DataShield\agent-harness\tests\test_core.py` |
| E2E tests | `C:\Users\techai\DataShield\agent-harness\tests\test_full_e2e.py` |
| SOP docs | `C:\Users\techai\DataShield\agent-harness\DATASHIELD.md` |
| setup.py | `C:\Users\techai\DataShield\agent-harness\setup.py` |
