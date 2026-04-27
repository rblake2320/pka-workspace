# SENTINEL: PKA Setup And Code Review

**Date:** 2026-04-25  
**Scope:** PKA workspace setup, validation stack, and new `scripts/agent_brain` runtime  
**Verdict:** GO for core PKA workspace; HOLD for live Agent Brain LLM execution until Ollama connectivity is restored

## What Was Verified

- `python scripts\pka_doctor.py` — PASS
- `python scripts\pka_process_audit.py` — PASS
- `python scripts\pka_runtime_check.py` — PASS, 0 active jobs and 0 pending approvals
- `python scripts\pka_e2e_test.py` — PASS
- `python scripts\pka_resilience_test.py` — PASS, 100/100 and 9/9 checks
- `python scripts\pka_full_validation.py` — PASS, 100/100 and 8/8 checks
- `python scripts\pka_agent_readiness.py` — PASS, 100/100
- `python scripts\pka_scorecard.py` — PASS, 93/100 strong readiness
- `python scripts\pka_observability.py` — PASS, latest validation 100/100
- `python -m compileall scripts\agent_brain` — PASS
- `python -m scripts.agent_brain --help` — PASS
- Agent Brain worker job-id and heartbeat unit checks — PASS

## Fixes Applied

- Fixed `scripts/agent_brain/worker.py` to read runtime jobs from `job_id`, matching `scripts/pka_runtime.py`.
- Fixed Agent Brain heartbeat calls to include the required `--note` argument.
- Corrected Agent Brain docs so the `gemma3` alias accurately maps to `qwen3:latest`.
- Corrected file-write safety docs to match behavior: `CLAUDE.md`, root `MEMORY.md`, and `owner.md` are read-only; `Owner's Inbox` is writable for deliverables.
- Updated root README repository note to match the v0.7.0 standalone git-root reality.
- Added `.gitignore` coverage for Agent Brain runtime logs, sessions, sandbox, and bytecode cache.
- Converted `scripts/agent_brain/` from an embedded git repository into a normal tracked workspace package.
- Preserved the prior Agent Brain repo history in `backups/agent_brain/agent_brain-history-20260425.bundle`.
- Added provider-aware model profiles so Agent Brain can use local Ollama SLMs, Spark/Tunnel Ollama models, or cloud OpenAI-compatible LLMs through the same loop.
- Confirmed local Ollama is live through `--model local` using `imds-v2:latest`.
- Confirmed cloud OpenAI-compatible routing reaches the API, but the configured key returns `401 Unauthorized`.

## Remaining Blockers

1. Cloud OpenAI-compatible execution is configured but currently blocked by auth: the configured API key returns `401 Unauthorized`.
2. Default Spark/Tunnel Ollama execution may still be offline if those remote endpoints are unreachable or missing the configured models.
2. Existing uncommitted workspace state includes the deleted `Team Inbox/bpc-protocol.html`; this was not changed during this review.

## Action

- Local SLM is already live:
  `python -m scripts.agent_brain status --model local`
- Restore/replace the cloud API key, then rerun:
  `python -m scripts.agent_brain status --model cloud`
- For task execution, use:
  `python -m scripts.agent_brain run "What version is this workspace?" --model qwen3-8b --verbose`
  `python -m scripts.agent_brain run "What version is this workspace?" --model local --verbose`
  `python -m scripts.agent_brain run "What version is this workspace?" --model cloud --verbose`
- Use the tracked bundle if the old embedded Agent Brain git history ever needs to be restored or inspected.
