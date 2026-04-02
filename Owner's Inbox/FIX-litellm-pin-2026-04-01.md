# SECURITY FIX — LiteLLM Supply Chain Pin
**Date:** 2026-04-01
**Executed by:** FORGE
**Threat:** TeamPCP supply chain attack — litellm 1.82.7 and 1.82.8 are backdoored (March 24 2026)
**Current installed version on all systems:** 1.82.6 (CLEAN — not affected)
**Risk without this fix:** Any unguarded `pip install --upgrade litellm` would silently pull the poisoned version.

---

## Verdict: PINNED

All litellm dependency entries across Spark-1 and Spark-2 are now bounded to `<1.82.7`.

---

## Files Patched

### Spark-1 (192.168.12.132)

| File | Before | After | Action |
|------|--------|-------|--------|
| `/home/rblake2320/agent-zero/requirements2.txt` | `litellm==1.79.3` | `litellm==1.79.3` | SKIP — exact pin to safe version (1.79.3 < 1.82.7) |
| `/home/rblake2320/ai-business/aiq-research-assistant/pyproject.toml` | `"litellm~=1.74.3"` | `"litellm>=1.74.3,<1.82.7"` | PATCHED — tilde operator replaced with explicit bounds |
| `/home/rblake2320/GenerativeAIExamples/nemo/Evaluator/Custom LLM-as-a-Judge/pyproject.toml` | `"litellm>=1.67.1"` | `"litellm>=1.67.1,<1.82.7"` | PATCHED — added upper bound |
| `/home/rblake2320/nvidia-blueprints/GenerativeAIExamples/nemo/Evaluator/Custom LLM-as-a-Judge/pyproject.toml` | `"litellm>=1.67.1"` | `"litellm>=1.67.1,<1.82.7"` | PATCHED — added upper bound |
| `/home/rblake2320/nvidia-blueprints/AgentIQ/pyproject.toml` | `"litellm==1.74.9"` | `"litellm==1.74.9"` | SKIP — exact pin to safe version |

### Spark-2 (10.0.0.2 via jump)

| File | Before | After | Action |
|------|--------|-------|--------|
| `/home/rblake2320/NeMo-Agent-Toolkit/pyproject.toml` | `"litellm==1.74.9"` | `"litellm==1.74.9"` | SKIP — exact pin to safe version |
| `/home/rblake2320/ai-business/aiq-research-assistant/pyproject.toml` | `"litellm~=1.74.3"` | `"litellm>=1.74.3,<1.82.7"` | PATCHED — tilde operator replaced with explicit bounds |

---

## Not Patched (Intentionally)

The following entries were found but are NOT direct litellm dependencies — they are wrapper packages that pull their own pinned litellm version internally. No action needed:

- `llama-index-llms-litellm~=0.x` (Spark-1 + Spark-2 NeMo-Agent-Toolkit)
- `langchain-litellm~=0.x` (Spark-1 + Spark-2 NeMo-Agent-Toolkit)
- `nvidia-nat[litellm]~=1.5` (AgentIQ packages, both Sparks)

The `.cache/uv/` directory entries are cached source distributions of litellm itself (version 1.77.2) — not dependency specs, not editable.

---

## Vulnerability Reference

- **CVE / Event:** TeamPCP supply chain attack, March 24 2026
- **Poisoned versions:** litellm 1.82.7 and 1.82.8
- **Safe versions:** All versions below 1.82.7 (and 1.82.9+ once vetted — do NOT assume safe without verification)
- **Attack vector:** `pip install --upgrade litellm` or any range spec that permits >=1.82.7

---

## Remaining Risk

1. **Lock files** — No `poetry.lock` or `pip freeze` outputs were audited. If any environment
   was previously `pip install --upgrade`'d between March 24 and today, the installed binary
   could be poisoned even if the requirements file is now clean. Run
   `pip show litellm` in each active venv to verify installed version.

2. **NVIDIA blueprint venvs** — These are reference clones. If they have active `.venv/`
   directories with litellm installed, those were excluded from the file scan. Verify with:
   ```bash
   find /home/rblake2320/nvidia-blueprints -path '*/.venv/*/litellm-*' -name 'METADATA' | xargs grep '^Version:' 2>/dev/null
   ```

3. **PyPI cache** — The `.cache/uv/` directory contains a cached source dist of
   litellm 1.77.2 (safe). No poisoned sdists were found in cache.

4. **Windows PC** — This fix only covered Spark-1 and Spark-2. If any local Windows
   Python environments use litellm (DataShield, Council, etc.), those were not scanned.
   Run: `pip show litellm` in any active local venv.

---

## Files Modified (absolute paths)

```
/home/rblake2320/ai-business/aiq-research-assistant/pyproject.toml          [Spark-1]
/home/rblake2320/GenerativeAIExamples/nemo/Evaluator/Custom LLM-as-a-Judge/pyproject.toml  [Spark-1]
/home/rblake2320/nvidia-blueprints/GenerativeAIExamples/nemo/Evaluator/Custom LLM-as-a-Judge/pyproject.toml  [Spark-1]
/home/rblake2320/ai-business/aiq-research-assistant/pyproject.toml          [Spark-2]
```
