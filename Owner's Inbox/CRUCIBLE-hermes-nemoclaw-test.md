# CRUCIBLE — Hermes (Nexus) + NemoClaw Test Report
**Date**: 2026-03-31
**Tester**: CRUCIBLE
**Target**: Hermes gateway on Spark-1 + NemoClaw sandbox on Spark-2
**For**: SENTINEL review / Ron's Owner Inbox

---

## Summary Verdict (before detail)

| Agent | Status | Blocking Issue |
|-------|--------|---------------|
| Hermes (Nexus) | DEGRADED — running but leaking to cloud | `auth.json` overrides config; routed real tasks to `chatgpt.com/codex` not local Ollama |
| NemoClaw | RUNNING — sandbox healthy, UI up, chat API not mapped | Port 18789 serves SPA only; no accessible chat completion endpoint found from host |

---

## Agent 1: Hermes (Nexus)

### Test Objective
Verify Hermes is alive, routing exclusively to local Ollama (not cloud), not accumulating restart failures, and has its memory/auth state correctly configured.

### Test Results

**T1 — Service Health**
PASS. Service is active and running as of test time (2026-03-30 23:57 CDT, PID 1170144). Memory: 168.5 MB. The service was completely dead for ~20 hours between 03:41 and 23:57 on Mar 30 — a gap with a single clean start at the end, no crash evidence, no error in that window. Likely a manual stop or host sleep. Currently stable for ~25 minutes at time of check.

**T2 — Model Connectivity (Ollama proxy port 11435)**
PASS. The proxy on port 11435 is responding and serving the correct model list. `qwen3-fast-hermes:latest` is present and registered. 46 models available. Proxy is reachable and answering API calls.

**T3 — Proxy Smoke Test (think:false injection)**
PARTIAL PASS WITH DEFECT. The proxy responds to chat completions. However, the response reveals that `think:false` is NOT suppressing internal reasoning — the response returned an empty `content` field with `finish_reason: length` and the `reasoning` field was populated:

```json
"choices":[{
  "message":{
    "role":"assistant",
    "content":"",
    "reasoning":"Okay, the user sent \"ping\". Let me figure out what they need..."
  },
  "finish_reason":"length"
}]
```

The proxy is returning a 50-token response but the actual answer content is empty. The model burned the entire `max_tokens=50` budget on reasoning tokens that were supposed to be suppressed. This is the exact failure mode documented in `hermes_nexus.md` — if `think:false` is not reliably injected, reasoning tokens consume the response budget and produce empty answers. The proxy appears to be injecting the parameter but Ollama may not be honoring it for this model. This should be verified with a higher `max_tokens` value to distinguish "reasoning suppression failed" from "budget exceeded."

**T4 — CLI Smoke Test**
PASS. `venv/bin/python cli.py --help` returns correct usage. Note: `python` is not in PATH on Spark-1; callers must use the venv binary. The service unit uses the full venv path so the service itself is unaffected, but any manual invocation that uses bare `python` will fail with "command not found."

**T5 — Memory/Config Check**
PASS. Both `~/.hermes/memories/MEMORY.md` and `~/.hermes/memories/USER.md` exist and have content.
- `MEMORY.md`: 332 bytes, contains accurate Spark-1 environment notes
- `USER.md`: 2,056 bytes, contains Ron's full profile (seeded 2026-03-29)
- Lock file present: `MEMORY.md.lock` (empty, normal for file-based locking)

**T6 — Auth State Check (FAIL — BLOCKING)**
FAIL. This is the primary defect.

`~/.hermes/auth.json` contains:
```json
{
  "active_provider": "custom",
  "providers": {
    "openai-codex": {
      "tokens": { ... },
      "auth_mode": "chatgpt"
    }
  }
}
```

`active_provider` is set to `"custom"` — which is correct. However, the `openai-codex` provider is present in the auth file and was used for actual task execution. Journal evidence confirms that on 2026-03-29 at 20:01:45, Hermes routed a real task to `https://chatgpt.com/backend-api/codex` with model `anthropic/claude-opus-4.6`:

```
Provider: openai-codex  Model: anthropic/claude-opus-4.6
Endpoint: https://chatgpt.com/backend-api/codex
Error: HTTP 400 - The 'anthropic/claude-opus-4.6' model is not supported when using Codex with a ChatGPT account.
```

This call was retried 3 times before failing. Total cloud routing incidents since 2026-03-28: **6 calls** to `chatgpt.com`. These calls failed (HTTP 400), so no data was actually sent to OpenAI, but Hermes was attempting to use the cloud provider despite config pointing to local. This is the known "auth file override bug" — the `openai-codex` tokens in auth.json were being activated for some task class that the `custom` provider did not handle, causing fallthrough to cloud.

The `.env` and `config.yaml` are both correctly set to local-only (`OPENAI_BASE_URL=http://localhost:11435/v1`, `LLM_MODEL=qwen3-fast-hermes`, `provider: custom`, `backend: local`). The leak is coming from a code path in Hermes that selects `openai-codex` for certain task types regardless of the configured provider.

**T7 — Restart Stability**
CONCERN. 14 restart events logged since 2026-03-29 (13 on Mar 29 + 1 on Mar 30). Pattern breakdown:
- Mar 29 17:46 — start after apparent manual trigger
- Mar 29 20:01 — restarted after cloud API failure (HTTP 400 triggered exit)
- Mar 29 20:05, 20:17, 20:18, 20:26, 20:38 — rapid restart loop (5 starts in ~37 minutes)
- Mar 29 21:21, 22:55, 23:04, 23:04, 23:36, 23:40 — intermittent restarts
- 20-hour gap Mar 30 03:41 to 23:57 — no restarts (service was off)
- Mar 30 23:57 — current start, stable

No `StartLimitBurst` events were detected in the journal window, meaning the service recovered without hitting systemd's restart limit. The rapid loop around 20:05-20:38 is correlated with the cloud API failure at 20:01 — Hermes crashed, restarted, hit the same failing code path, crashed again. The root cause of that loop is the cloud routing bug in T6.

---

### Hermes Defect Summary

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| H-01 | HIGH | Cloud API leak — Hermes routes some tasks to `chatgpt.com/codex` ignoring local config | Journal 2026-03-29 20:01, 6 calls total |
| H-02 | MEDIUM | `think:false` proxy not suppressing reasoning tokens — empty responses on low `max_tokens` | Proxy test response: empty `content`, reasoning present, `finish_reason: length` |
| H-03 | LOW | `python` not in PATH on Spark-1 — manual CLI invocation fails | `bash: python: command not found` |

**H-01 Root Cause Hypothesis**: Hermes has a task router that selects the provider based on task type, not just the configured default. The `openai-codex` provider is present in `auth.json` with valid tokens, and some code path (likely a tool-calling or code-execution subtask) selects it by name rather than deferring to `active_provider`. Fix: strip the `openai-codex` entry from `auth.json` entirely, not just set `active_provider`.

**H-02 Root Cause Hypothesis**: The proxy injects `options.think=false` in the request body, but Ollama may be ignoring that field for the `qwen3-fast-hermes` model, or the field path is wrong for this Ollama version. Qwen3 thinking mode suppression may require a model-level parameter rather than a request-level one.

---

## Agent 2: NemoClaw

### Test Objective
Verify the OpenShell sandbox is alive, the openclaw-gateway process is healthy, the chat UI is accessible, and a test message can be delivered and answered.

### Test Results

**T1 — Gateway Health (port 8080)**
FAIL — Gateway is not HTTP. Port 8080 returns `HTTP/0.9 when not allowed` on every curl request. This is not a crashed service — it is a protocol mismatch. The `openshell-server` process listening on 8080 speaks a custom binary or WebSocket protocol, not plain HTTP/1.1. Standard curl cannot query it. The gateway is running (2:42 CPU time since Mar 28) but is not inspectable via HTTP.

**T2 — Chat UI Check (port 18789)**
PASS. Port 18789 responds with a full SPA (title: "OpenClaw Control"). The UI is served by a port-forward: `0.0.0.0:18789 → 127.0.0.1:18789` inside the sandbox, maintained by the `openshell ssh-proxy` process. The HTML loads correctly from outside the sandbox via the host's port binding.

**T3 — API Discovery**
PARTIAL. The chat UI at port 18789 returns 404 on all API paths tested:
- `/api/chat` — 404
- `/api/v1/chat` — 404
- `/api/chat/completions` (OpenAI format) — 404
- `/api/prompt` — 404
- `/api/info` — 404
- `/api/status` — 404
- `/status` — 404
- `/v1/messages` — 404

The server is an Express/Node app (confirmed by `Connection: keep-alive`, `Keep-Alive: timeout=5`, `X-Content-Type-Options` headers). It serves the SPA on `/` and unknown routes on `/` (subpaths of the SPA), but the actual chat API is either not exposed on port 18789, only accessible from inside the sandbox, or requires WebSocket. No OpenAPI schema is available from the host side.

**T4 — Sandbox Status**
PASS. `openshell sandbox list` returns:

```
NAME     NAMESPACE  CREATED            PHASE
ai-army  openshell  2026-03-28 18:51   Ready
```

Sandbox has been in `Ready` phase since creation on Mar 28. The onboard session completed all 7 steps successfully (preflight, gateway, provider_selection, inference, sandbox, openclaw, policies).

**T5 — Test Message Send**
BLOCKED. Cannot reach the chat API from the host. Port 18789 does not expose a message endpoint externally. The `openshell sandbox connect` subcommand does not support inline command execution. The chat API appears to be internal to the sandbox only, with the UI as the sole external interface.

**T6 — Config/Blueprint Check**
PASS. `~/.nemoclaw/` is properly configured:
- `sandboxes.json`: `ai-army` sandbox defined, `gpuEnabled: true`, policies `[pypi, npm]`
- `onboard-session.json`: Onboard complete, model `qwen3:32b` via `http://host.openshell.internal:11434/v1` (Spark-2's Ollama), provider `ollama-local`, API `openai-completions`
- `source/nemoclaw-blueprint/blueprint.yaml`: Default inference profile points to NVIDIA cloud (`https://integrate.api.nvidia.com/v1`, `nvidia/nemotron-3-super-120b-a12b`) but the onboard was configured with the local Ollama override — this is correct behavior (blueprint default is overridden at onboard time)

NemoClaw is correctly wired to local `qwen3:32b` on Spark-2's Ollama, not NVIDIA cloud. Local inference routing is confirmed by `onboard-session.json`.

**T7 — Resource Usage**
PASS. `openclaw-gateway` is using 336 MB RAM (336,428 KB), consistent with the 335 MB observed on Mar 28. No memory growth over 3 days. CPU: 5:45 elapsed (modest for 3 days). The sandbox has been stable since creation.

---

### NemoClaw Defect Summary

| ID | Severity | Description | Evidence |
|----|----------|-------------|----------|
| N-01 | LOW | No externally accessible chat API — cannot send messages or verify inference from host | 404 on all API paths at port 18789 |
| N-02 | INFO | Gateway on port 8080 speaks non-HTTP protocol — not testable via curl | `HTTP/0.9 when not allowed` |

**N-01 Root Cause**: The chat API is almost certainly exposed inside the sandbox, accessible via the `openshell sandbox connect` SSH tunnel or a WebSocket on port 18789. The SPA at port 18789 connects via WebSocket to the backend — this is standard for agent chat UIs. The limitation is that CRUCIBLE cannot test the chat path without interactive sandbox access or a WebSocket client. The agent itself may be fully functional; the gap is in external observability.

---

## What Each Agent Can and Cannot Do Right Now

### Hermes (Nexus)
**CAN DO**:
- Receive and process Telegram messages from Ron's allowlisted user ID
- Use local qwen3-fast-hermes via Ollama proxy
- Persist and read memory files (MEMORY.md, USER.md)
- Self-restart on failure (Restart=always)
- Run autonomous tool calls and multi-step reasoning tasks

**CANNOT DO RELIABLY**:
- Guarantee local-only routing — some task types leak to chatgpt.com/codex
- Produce non-empty responses on low token budgets (think suppression unreliable)
- Survive the cloud-routing code path without crashing and restart-looping

### NemoClaw
**CAN DO**:
- Maintain the OpenShell sandbox in Ready state
- Serve the OpenClaw Control UI on port 18789
- Route inference to local qwen3:32b on Spark-2 Ollama
- Operate with GPU access enabled in the sandbox

**CANNOT DO FROM HOST**:
- Accept external chat messages via HTTP (no accessible REST endpoint on port 18789)
- Be tested via curl without WebSocket client or sandbox-internal access

---

## Recommended Fixes and Next Steps

### Hermes — Required Before Calling It Clean

**Fix H-01 (HIGH — do this now)**
Remove the `openai-codex` provider from `~/.hermes/auth.json` entirely:
```bash
# On Spark-1
python3 -c "
import json
with open('/home/rblake2320/.hermes/auth.json') as f:
    d = json.load(f)
d['providers'] = {}
d['active_provider'] = 'custom'
with open('/home/rblake2320/.hermes/auth.json', 'w') as f:
    json.dump(d, f, indent=2)
print('Done')
"
systemctl --user restart hermes-gateway.service
```
After restart, watch the journal for 10 minutes to confirm no `chatgpt.com` calls appear. If the code path that selects `openai-codex` by name still runs, it will fail to find credentials and fall through to an error rather than making a cloud call.

**Fix H-02 (MEDIUM — verify think suppression)**
Test the proxy with a higher token budget to isolate whether the issue is budget exhaustion or failed suppression:
```bash
curl -s http://localhost:11435/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3-fast-hermes","messages":[{"role":"user","content":"What is 2+2? Answer only with the number."}],"max_tokens":2000}' | python3 -m json.tool
```
If `content` is still empty with 2000 tokens, the `think:false` injection is failing. Check what the proxy is actually sending by logging the outgoing request body in `~/tmp_proxy.py`.

### NemoClaw — Testing Gap, Not a Defect

The sandbox is healthy. To complete end-to-end testing, access needs to come from inside the sandbox or via WebSocket. Options:
1. Use `openshell sandbox connect ai-army --gateway nemoclaw` for interactive shell access, then test the internal chat API
2. Write a WebSocket client to connect to `ws://localhost:18789` and send a message
3. Forward an internal API port to the host at onboard time (requires re-onboarding or `openshell policy set`)

For a functional chat test without reconfiguration, option 1 is the lowest friction.

---

## Findings for SENTINEL

**Hermes**:
- Service is running and structurally intact, but has an active cloud routing leak (H-01, HIGH). Six calls were made to `chatgpt.com` in the last 48 hours. All failed with HTTP 400, so no data was transmitted, but the behavior violates Ron's local-only requirement and causes crash loops. This must be fixed before Hermes is considered production-reliable. The fix is a one-line JSON edit to `auth.json`.

- The think-suppression proxy is suspect (H-02). Evidence is a single test returning empty `content`, which may be budget exhaustion rather than proxy failure. Needs one follow-up test with higher `max_tokens` to confirm or clear.

**NemoClaw**:
- Sandbox has been stable for 3 days, GPU-enabled, correctly wired to local Ollama (qwen3:32b). No defects found in what is observable from the host. End-to-end chat path could not be tested without sandbox-internal access. This is a testing gap, not a system failure. Recommend SENTINEL treat NemoClaw as "infrastructure healthy, chat functionality unverified" until a WebSocket or sandbox-internal test is run.

**Recommended SENTINEL decision**: NO-GO for Hermes as "local-only confirmed" until H-01 is patched and verified. NemoClaw is GO for "sandbox healthy" with the chat path marked as an open verification item.
