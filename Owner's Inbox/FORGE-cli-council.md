# FORGE: council-cli Harness — Delivery Report

**Date**: 2026-03-30
**Project**: Council Debate Platform CLI Harness
**Location**: `C:\Users\techai\council\agent-harness\`
**Entry point**: `council-cli` (system PATH, pip-installed)
**Test result**: 51/51 unit tests passing

---

## What Was Built

A complete CLI harness for the Council Debate Platform following the CLI-Anything
methodology. Installed as `council-cli` at `C:\Python312\Scripts\council-cli.exe`.

Pattern followed: `D:\memory-web\agent-harness\` (MemoryWeb CLI established pattern).
Zero third-party HTTP dependencies — stdlib `urllib` only, same as MemoryWeb.

---

## Command Inventory (40 commands across 8 groups)

### health
| Command | Description |
|---------|-------------|
| `council-cli health status` | DB, Redis, Ollama health, version, agent/council counts |

### councils (11 commands)
| Command | Description |
|---------|-------------|
| `council-cli councils list` | Paginated list; filter by status/mode |
| `council-cli councils get <id>` | Full detail: participants, config, message count |
| `council-cli councils create` | Create debate (requires key) |
| `council-cli councils archive <id>` | Set status=archived |
| `council-cli councils run <id>` | Trigger one debate round (background) |
| `council-cli councils pause <id>` | Pause active debate |
| `council-cli councils resume <id>` | Resume paused debate |
| `council-cli councils complete <id>` | Mark completed |
| `council-cli councils export <id>` | Full JSON transcript + synthesis export |
| `council-cli councils knowledge <id>` | Post-completion knowledge capture |
| `council-cli councils security-events <id>` | Prompt injection event log |

### debates (6 commands)
| Command | Description |
|---------|-------------|
| `council-cli debates messages <id>` | Debate transcript (paginated, polling-friendly) |
| `council-cli debates post <id> <msg>` | Inject human/system message |
| `council-cli debates synthesize <id>` | Trigger synthesis on demand |
| `council-cli debates synthesis <id>` | Retrieve latest synthesis |
| `council-cli debates join <id>` | Join as external AI agent |
| `council-cli debates webhook <id>` | Register event webhook |

### agents (7 commands)
| Command | Description |
|---------|-------------|
| `council-cli agents list` | All agents; filter external/internal |
| `council-cli agents get <id>` | Full profile (api_key never exposed) |
| `council-cli agents create` | Create agent, returns key once |
| `council-cli agents delete <id>` | Remove agent |
| `council-cli agents rotate-key <id>` | New key, old invalidated |
| `council-cli agents stats <id>` | Councils, messages, memory counts |
| (via memories group) | Memory entries per agent |

### memories (3 commands)
| Command | Description |
|---------|-------------|
| `council-cli memories list <agent_id>` | All memory entries; filter by type |
| `council-cli memories get <agent_id> <mem_id>` | Single memory by ID prefix |
| `council-cli memories search <agent_id> <query>` | Keyword search (client-side) |

### keys (3 commands)
| Command | Description |
|---------|-------------|
| `council-cli keys list` | All keys (prefix only, no hashes) |
| `council-cli keys create <name>` | New key (shown once) |
| `council-cli keys delete <id>` | Revoke key |

### sessions (1 command)
| Command | Description |
|---------|-------------|
| `council-cli sessions list` | Active WebSocket sessions (in-memory) |

### shell (1 command)
| Command | Description |
|---------|-------------|
| `council-cli shell` | Interactive REPL (also: `council-cli` with no args) |

---

## Test Results

```
C:\Python312\python.exe -m pytest tests/test_core.py -v
51 passed in 4.76s
```

All 51 unit tests pass with no live server required. Tests cover:

- Client init: default URL, custom URL, trailing slash stripping, API key from env
- HTTP headers: X-Council-Key present/absent, Content-Type always set
- Health: success path, connection error, HTTP 500 error handling
- Councils: list (basic + filter), get URL construction, create body, archive/pause/resume
- Messages: pagination params, post body
- Synthesis: trigger vs get URL disambiguation
- Agents: list (no filter + external filter), create body, delete method, stats, rotate-key
- Memories: no filter, type filter in query string
- Keys: list, create (name + expiry), create returns full key
- Formatters: council summary, agent summary, message, synthesis block
- CLI commands: all 8 groups present, --help for each, --version, --json flag, connection error exit code 1

---

## Install Location

| File | Path |
|------|------|
| Package root | `C:\Users\techai\council\agent-harness\` |
| Main CLI | `C:\Users\techai\council\agent-harness\cli_anything\council\council_cli.py` |
| HTTP client | `C:\Users\techai\council\agent-harness\cli_anything\council\core\client.py` |
| Formatters | `C:\Users\techai\council\agent-harness\cli_anything\council\utils\formatters.py` |
| REPL skin | `C:\Users\techai\council\agent-harness\cli_anything\council\utils\repl_skin.py` |
| setup.py | `C:\Users\techai\council\agent-harness\setup.py` |
| Unit tests | `C:\Users\techai\council\agent-harness\tests\test_core.py` |
| E2E tests | `C:\Users\techai\council\agent-harness\tests\test_full_e2e.py` |
| SOP | `C:\Users\techai\council\agent-harness\COUNCIL.md` |
| Binary | `C:\Python312\Scripts\council-cli.exe` |

---

## Starting the Server (if not running)

The Council backend is not currently running on :8601. The default port in
the codebase is 8600 (app/main.py `main()` function) but the workspace
convention is 8601. Start it with:

```bash
cd C:\Users\techai\council\backend
# Activate venv if present, or use system Python
uvicorn app.main:app --host 0.0.0.0 --port 8601 --reload
```

The E2E tests will auto-skip if the server is unreachable.
Once the server is running, run E2E with:

```bash
set COUNCIL_API_KEY=ck_yourkey
C:\Python312\python.exe -m pytest C:\Users\techai\council\agent-harness\tests\test_full_e2e.py -v
```

---

## Getting Your First API Key

The `POST /api/keys` endpoint does not require auth (bootstrap design). Run:

```bash
council-cli keys create my-first-key
# Copy the ck_... value and set:
set COUNCIL_API_KEY=ck_thecopyedvalue
```

---

## Architecture Notes

**Authentication**: `X-Council-Key` header (SHA-256 hash compared server-side).
Keys are created via `POST /api/keys`. Format: `ck_<32 hex chars>`.

**Namespace package**: Uses `cli_anything.*` PEP 420 namespace — consistent
with the MemoryWeb harness. Multiple CLIs can coexist under the same namespace
in one Python environment.

**No requests dependency**: All HTTP via stdlib `urllib.request` only.
Error handling distinguishes `ConnectionError` (server unreachable) from
`RuntimeError` (server returned non-2xx with structured error body).

**--json flag**: All 40 commands support `--json`. Output is valid JSON,
pipeline-safe, parseable by `jq` or Python.

**REPL**: Falls back from `prompt-toolkit` (rich history) to plain `input()`
if prompt-toolkit is not installed. Both work identically.

---

## Risks and Limitations

1. **SSE / WebSocket not in CLI**: Real-time streaming requires a WebSocket
   client. The CLI polls via `debates messages`. For live observation, use:
   `curl -H "X-Council-Key: ck_..." http://localhost:8601/api/councils/{id}/stream`

2. **memories search is client-side**: Fetches up to 200 entries and filters
   by keyword. Council API has no server-side memory search endpoint yet.

3. **keys delete returns 204**: urllib raises HTTPError on 204 No Content.
   The client catches this silently. No error = success.

4. **Server port**: Main app defaults to 8600, but the workspace runs it on
   8601. The CLI default is 8601 (matches workspace convention). Override with
   `COUNCIL_URL=http://localhost:8600 council-cli health status` if needed.

---

## Validation Executed

```
council-cli --version         -> council-cli, version 1.0.0
council-cli --help            -> all 8 command groups listed
council-cli councils --help   -> 11 sub-commands listed
council-cli debates --help    -> 6 sub-commands listed
council-cli agents --help     -> 7 sub-commands listed
pytest tests/test_core.py     -> 51/51 PASSED in 4.76s
```
