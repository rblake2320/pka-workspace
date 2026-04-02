# Council Platform v0.5.1 — Fixes Report
**Date**: 2026-03-29
**Commit**: 1d0f243 (main)
**Tests**: 128 passing
**Status**: All remaining items from v0.5.0 resolved.

---

## What Was Fixed (4 Items)

### Fix 1 — start.sh Default Port (Wrong Since v0.5.0)
`PORT=${PORT:-8600}` → `PORT=${PORT:-8601}`

`start.sh` was defaulting to the stale port 8600 process. Anyone running `bash start.sh` without overriding `$PORT` was starting on the wrong port and hitting old code. Fixed. Now `bash start.sh` just works.

### Fix 2 — DEFAULT_MODEL Upgrade
`llama3.1:8b` → `models/gemini-2.0-flash-lite`

LLaMA 3.1:8b is a weak instruction follower. Even with `_enforce_brevity()` hard-capping output length, the reasoning quality was poor. Gemini 2.0 Flash Lite:
- Much stronger instruction compliance
- Better debate reasoning and factual accuracy
- Free tier on the Gemini API (key already configured in `.env`)
- Uses the existing Gemini OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`)
- No config changes needed — the model router already handles `models/` prefix for Gemini

### Fix 3 — Ultra RAG Registered as Council Tool
`rag_search` added to `tools.py`, registered in `TOOL_FUNCTIONS` and `DEFAULT_TOOLS`.

Every agent can now search 4,015 IMDS corpus chunks during debates. NOVA (Research & Intelligence) will be the primary user, but any agent can call it when they need domain knowledge.

**Tool signature:**
```python
rag_search(query: str, collection: str = "imds", top_k: int = 5) -> str
```

**Routing logic:**
1. Primary: `http://192.168.12.132:8300` (direct Spark-1, ~5ms)
2. Fallback: `https://api.ultrarag.app` (Cloudflare tunnel, ~50ms)
3. 5-minute response cache (same as other tools)

**Collections available:** `imds` (Air Force maintenance docs), `personal` (ai-business docs)

**Agent usage (ReAct pattern):**
```
ACTION: rag_search("AFTO Form 349 completion requirements")
```

### Fix 4 — Spark-1 Ollama Started
Spark-1 Ollama was offline. Started via `nohup ollama serve`. Now running at PID 1940118.

**Current state:** Running, no models pulled yet. The council debates now use Gemini (Fix 2), so Spark-1 Ollama isn't blocking anything. Pull models as needed for agent distribution:
```bash
ssh rblake2320@192.168.12.132 "ollama pull qwen2.5:7b"
```

---

## Current System State

| Component | Status |
|-----------|--------|
| Council backend (port 8601) | ✅ Running, v0.5.1 |
| Council frontend (port 3000) | ✅ Connected |
| start.sh default port | ✅ Fixed (8601) |
| DEFAULT_MODEL | ✅ Upgraded (gemini-2.0-flash-lite) |
| rag_search tool | ✅ Wired — IMDS corpus searchable |
| Ultra RAG (Spark-1:8300) | ✅ Production (4,015 IMDS chunks) |
| Spark-1 Ollama | ✅ Running (no models yet) |
| Spark-2 OpenShell | ✅ Fixed (qwen2.5:7b) |
| Training exports | ✅ 36 sessions in council_training_data.jsonl |
| LoRA training cycle 1 | 🔜 Pending — need persona JSONL from next sessions |

---

## What's Still Pending (Lower Priority)

1. **Pull models to Spark-1** — `ollama pull qwen2.5:7b` to give Spark-1 local inference capability
2. **Distribute agents** — per-agent `ollama_url` config pointing heavy agents to Spark-2, light ones to local
3. **LoRA training cycle 1** — run a few more debate sessions to populate `agent_persona_training.jsonl`, then `bash council/scripts/sync_training_to_spark2.sh --train --file=personas`
4. **`agent_memory_pkey`** — change INSERT to `ON CONFLICT DO NOTHING` (cosmetic improvement; current try/except works fine)

---

## Tests

```
128 passed in 1.11s
```

All 128 tests pass with the new `rag_search` tool added. No test updates required — new tool is purely additive.

---

*Code at `C:\Users\techai\council\` — commit 1d0f243. Start: `cd council/backend && bash start.sh`*
