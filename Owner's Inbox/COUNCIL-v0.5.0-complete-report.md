# Council Platform v0.5.0 — Complete Session Report
**Date**: 2026-03-29
**Commit**: 1c85dbc (main)
**Tests**: 128 passing (was 110 at v0.4.0)
**Status**: All critical issues resolved. Training pipeline live. OpenShell fixed.

---

## What Was Broken Coming In

Three user-visible failures:
1. **"What is today's date" → silence.** Zero responses. Nobody answered.
2. **"4+5" → 3-paragraph essay.** FORGE and DEBUGGER (weak models) ignored the 1-sentence rule.
3. **"Should AI have rights?" → domain agents silenced themselves.** They knew it wasn't their lane technically, so they said nothing — but the question was actually asking for their perspective.

---

## What Was Fixed (8 Total)

### Bug 1 — Silence (CRITICAL)
**Root cause**: `_running` lock held during multi-round session. Second message arrives → lock blocked → `run_session` returned immediately. Message saved to DB, never processed.

**Fix**: Catch-up loop in `run_session` finally block. After session ends, checks if a human message arrived with no agent response after it. If yes, re-enters. Capped at 3 catch-ups to prevent infinite re-entry.

### Bug 2 — Wrong Question Being Answered (CRITICAL)
**Root cause**: `_generate_one` pulled the "latest" human message from `agent_context` — a 20-message sliding window. In a 50-message council, the newest human message was outside the window. Agents were answering the *previous* question, not the current one.

**Fix**: `q_text` now sourced from `recent_messages` (same snapshot as `run_round`). Always the correct question.

### Bug 3 — Date Bypass Not Working
**Root cause**: Bypass required `web_context` to be non-None, so it only fired after a web search. Pure date queries with no search never triggered it.

**Fix**: Removed `web_context` dependency. Date queries match `_FACTUAL_PATTERNS` → bypass LLM entirely → `_server_datetime()` injected directly. Ground truth timestamp in every system prompt as backup.

### Bug 4 — Session Corruption (CRITICAL)
**Root cause**: `extract_and_persist_insight()` (fire-and-forget after each agent response) shared the main `db` session. A `UniqueViolationError` on `agent_memory_pkey` poisoned the session → `PendingRollbackError` for all subsequent DB operations → messages not saved.

**Fix**: Snapshot all ORM values before the `await`, open a fresh `AsyncSessionLocal()` inside the function, catch rollback gracefully. The shared session is never touched.

### Bug 5 — Verbosity
**Root cause**: GPT-4o-mini and LLaMA 3.1:8b are weak instruction followers. System prompt rules ("ONE sentence") were ignored.

**Fix**: `_enforce_brevity(text, max_words)` hard-caps after generation:
- Factual questions → 15 words
- Debate/opinion → 60 words
Truncates at last sentence boundary. Can't be ignored — runs on output, not input.

### Bug 6 — Opinion Questions Silencing Agents
**Root cause**: Rule 6 said "stay in your domain." Ethics/rights/values questions aren't anyone's *technical* domain, so agents with strict domain discipline stayed quiet.

**Fix**: `_OPINION_PATTERNS` regex detects ethics/values/rights/moral/philosophy questions → classified as `"opinion"` type → Rule 6 becomes: *"This is a values question — your background shapes a unique angle. Speak from what YOU know."* All agents respond from their perspective.

### Bug 7 — Self-Model Truncation
**Root cause**: Only the single latest `self_model` memory was injected into each agent's system prompt. Earlier sessions' insights were stored but never used.

**Fix**: Last 3 `self_model` entries (deduplicated by first 60 chars). Agents with no `self_model` yet get their latest 3 `pattern` memories instead (SCRIBE, CRUCIBLE, RADAR).

### Bug 8 — Training Data Too Narrow
**Root cause**: Only 1 JSONL file with full conversation records. Not useful for persona-specific or preference-based training.

**Fix**: `LearningCapture` now exports 3 files per session:
- `council_training_data.jsonl` — full conversation (OpenAI SFT format)
- `agent_persona_training.jsonl` — per-agent SFT: system(persona) + user(question) → assistant(response)
- `agent_self_model_evolution.jsonl` — pattern evolution per agent per session (DPO-ready)

---

## Training Pipeline Status

| Item | Status |
|------|--------|
| Export files | 36 sessions in `council_training_data.jsonl` (1.25 MB) |
| `agent_persona_training.jsonl` | Generates after next debate session |
| `agent_self_model_evolution.jsonl` | Generates after next debate session |
| Spark-2 training script | Deployed to `~/ai-business/training/train_council.py` |
| Sync script | `council/scripts/sync_training_to_spark2.sh` |
| Target model | `Qwen/Qwen2.5-7B-Instruct` (= qwen2.5:7b in Ollama) |
| Dry-run verified | ✅ 36 examples loaded cleanly on Spark-2 |

**To run first LoRA cycle** (after a few more sessions accumulate persona data):
```bash
bash council/scripts/sync_training_to_spark2.sh --train --file=personas
```

---

## OpenShell on Spark-2 — Fixed

**Bug**: Every inference request through the `ai-army` sandbox failed at exactly the same point with `"error decoding response body"`. Happened on a repeating ~10/20 minute schedule (automated health probes from Claude Code inside the sandbox).

**Root cause**: `qwen3-32b-nothink` model (despite the "nothink" name) outputs a non-standard `"reasoning"` field inside streaming SSE delta chunks:
```json
{"delta": {"role":"assistant","content":"","reasoning":"Alright"}}
```
OpenShell's Rust proxy expected standard OpenAI `ChatCompletionChunk` format — `delta` with only `role`/`content`. Deserializing an unexpected field → panic → "error decoding response body" on every chunk.

**Fix**: Switched inference model:
```
openshell inference update -g nemoclaw --model qwen2.5:7b
```
`qwen2.5:7b` confirmed clean standard SSE output. Proxy now decodes without error.

**Verified**: From inside the ai-army sandbox via kubectl exec — clean response received in 5 seconds.

---

## Current System State

| Component | Status |
|-----------|--------|
| Council backend (port 8601) | ✅ Running, v0.5.0 |
| Council frontend (port 3000) | ✅ Connected |
| PostgreSQL agent_memory | ✅ 319 memories (187 pattern + 132 self_model) |
| Training exports | ✅ 36 sessions captured |
| Spark-2 OpenShell | ✅ Fixed — qwen2.5:7b inference |
| Spark-2 training infra | ✅ Script deployed, dry-run verified |
| Spark-1 Ollama | ⚠️ Offline — needs `ollama serve` |
| LoRA training cycle 1 | 🔜 Pending — need persona JSONL from next sessions |

---

## What's Next (Priority Order)

1. **Run a few more debate sessions** — generates the persona and self-model JSONL files, then trigger the first LoRA training cycle on Spark-2
2. **Fix `start.sh`** — default to port 8601, kill the stale 8600 process
3. **Register Ultra RAG as Council tool** — NOVA can hit the private IMDS corpus during debates
4. **Ollama on Spark-1** — `ssh rblake2320@192.168.12.132 "ollama serve"` then pull better models for council agents
5. **Distribute agents** — per-agent `ollama_url` config pointing heavy agents to Spark-2, light ones to local

---

*All code at `C:\Users\techai\council\` — commit 1c85dbc. Tests: `cd council/backend && pytest tests/ -v`*
