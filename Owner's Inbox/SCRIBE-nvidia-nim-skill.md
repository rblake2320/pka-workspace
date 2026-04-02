# SCRIBE — nvidia-nim Skill Delivery
**Date**: 2026-03-26
**Status**: Delivered — PENDING (requires 3 confirmed successful uses to promote to ACTIVE)

---

## Gap Report

**What was missing**: No skill existed for NVIDIA NIM integration. The same
patterns (credential loading, endpoint URLs, tiling logic, docker run commands)
were being reconstructed in each new project that touched a NIM. DataShield,
Ultra RAG, and AI Army OS all use NIMs but none of their patterns were
codified as a reusable skill.

**What was searched**:
- All 24+ skills in `~/.claude/skills/` — no nvidia-nim, no nim-inference match above 50% relevance
- MCP catalog (docker unavailable at scan time) — no NIM-specific MCP
- Installed CLIs — `nvidia-smi` detected but that covers GPU status, not NIM API patterns
- pip packages — `nvidia-cuda-runtime`, `nvidia-ml-py` present but unrelated to NIM client patterns
- Self-learning KB — 0 entries on this domain

**What was found**: The real production source code in:
- `C:\Users\techai\DataShield\src\browser\ocr_client.py` — NeMo OCR client
- `C:\Users\techai\DataShield\src\config\settings.py` — pydantic-settings env_file tuple pattern
- `C:\Users\techai\toolkit\toolkit\vision\ocr\nemo.py` — shared toolkit wrapper
- `C:\Users\techai\.nvidia.env` — actual credential file structure and comments

---

## Coverage Scan Result

| Source | Coverage | Decision |
|--------|----------|----------|
| Existing skills | 0% — nothing within 80% threshold | CREATE new |
| MCP catalog | Not accessible at scan time | Not applicable |
| `nvidia-smi` CLI | Covers GPU monitoring only | Not applicable |
| DataShield source | 100% of OCR client pattern | Grounded the skill in this |
| toolkit source | 100% of shared wrapper | Grounded the skill in this |

**Decision: CREATE new skill from scratch.**

No existing skill came within 80% of the NIM integration domain. The source
code that existed was buried in project-specific directories, not in a form
Claude could apply to a new project. The skill codifies those patterns once.

---

## What Was Built

### Primary skill file
**Location**: `C:\Users\techai\claude-skills\nvidia-nim\skill.md`

Covers 8 sections:

| Section | What it gives you |
|---------|-------------------|
| 1. Credential Setup | The exact `~/.nvidia.env` structure, pydantic-settings tuple pattern, PowerShell/bash loading, docker-compose wiring, NGC registry login |
| 2. Cloud API Pattern | Base URLs, auth headers, retry with backoff, size limits (175 KB safe margin) |
| 3. Key Available NIMs | Exact endpoints, docker images, VRAM requirements, and request/response patterns for: NeMo OCR, NV-EmbedQA, Llama 3.1 70B, Nemotron 70B, Grounding DINO, YOLOX |
| 4. Local NIM Docker | Standard `docker run` template, NIM-specific commands, cloud-to-local switching, health check |
| 5. Python Client Pattern | Minimal standalone client, toolkit import, large file tiling (2x2 quadrant), batch API call |
| 6. Toolkit Integration | `from toolkit.vision.ocr.nemo import NeMoOCR` — the shared wrapper and when to use it vs project-scoped clients |
| 7. RTX 5090 Decision Tree | Cloud vs local criteria, VRAM budget table for all relevant NIMs, Spark-1 deployment for 70B models |
| 8. build.nvidia.com Reference | Catalog URLs, how to find new NIMs, getting API keys, checking quotas |

### References file
**Location**: `C:\Users\techai\claude-skills\nvidia-nim\references\nim-catalog.md`

Full NIM table across 5 categories:
- CV / Vision NIMs (OCR, Grounding DINO, YOLOX, VISTA)
- Embedding NIMs (NV-EmbedQA-E5-v5, NV-Embed-v2, Llama-3.2-EmbedQA)
- LLM NIMs (Llama 3.1/3.3 70B, Nemotron, Mistral, Qwen2.5-Coder, DeepSeek-R1)
- Reranking NIMs (NV-RerankQA, Llama-3.2-RerankQA)
- Multimodal / VLM NIMs (Llama Vision, NVLM-D, Florence-2)

Also includes:
- Deployment topology map (cloud → RTX 5090 → Spark-1 → Spark-2)
- Local cache strategy (D: drive path for Windows, expected cache sizes)
- Image tag pinning pattern for reproducible production deployments

---

## Validation Plan

The skill reaches ACTIVE after 3 confirmed successful uses. Suggested test
scenarios that cover the most-used paths:

**Use 1 — Credential loading in a new project**
- Copy the pydantic-settings pattern from Section 1 into a new project
- Confirm `NVIDIA_API_KEY` loads from `~/.nvidia.env` without a project `.env`
- Pass criterion: `get_settings().nvidia_api_key` starts with `nvapi-`

**Use 2 — Cloud OCR call**
- Use the standalone client in Section 5 on a real screenshot PNG
- Pass criterion: response contains non-empty `predictions[0].text`

**Use 3 — Toolkit import in a new project**
- `from toolkit.vision.ocr.nemo import NeMoOCR` + `ocr.extract_text(path)`
- Pass criterion: `result.success == True` and `result.full_text` is non-empty

When each use succeeds, increment `use_count` in the skill frontmatter.
At `use_count: 3`, change `status: PENDING` to `status: ACTIVE`.

---

## Risks

| Risk | Severity | Notes |
|------|----------|-------|
| NVIDIA endpoint URLs change without notice when NIM versions update | Medium | The catalog at `build.nvidia.com/nim` is the authoritative source. The OCR and embedding endpoints have been stable across multiple releases; YOLOX and Grounding DINO slugs are more likely to shift. |
| NGC_API_KEY same as NVIDIA_API_KEY is underdocumented by NVIDIA | Low | Confirmed in `~/.nvidia.env` and NVIDIA docs. Will cause confused NGC login failures if someone sets them to different values. |
| Local NIM first-start latency (~60-120s model load) surprises developers | Low | Documented in Section 4. Health check endpoint is the right way to poll readiness. |
| 70B LLM NIMs exceed RTX 5090 VRAM | Low | Documented in decision tree. Route to Spark-1. |
| `.nvidia.env` must never be committed to public repos | High | The file is in the home directory (`~`), not a project directory, so it won't be accidentally `git add`-ed. CI/CD must use repository secrets instead. |

---

## Files Delivered

| File | Purpose |
|------|---------|
| `C:\Users\techai\claude-skills\nvidia-nim\skill.md` | Primary skill — all 8 sections |
| `C:\Users\techai\claude-skills\nvidia-nim\references\nim-catalog.md` | Full NIM catalog table |
| `C:\Users\techai\PKA testing\Owner's Inbox\SCRIBE-nvidia-nim-skill.md` | This summary |
