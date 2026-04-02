# EMERGENCY Supply Chain Security Check
**Date**: 2026-04-01
**Executed by**: FORGE
**Nodes checked**: Spark-1 (192.168.12.132), Spark-2 (10.0.0.2)

---

## SUMMARY VERDICT: CLEAN

No compromised packages found. No RAT activity detected. No poisoned LiteLLM versions present.
One Ollama advisory item (below).

---

## CHECK 1: LiteLLM Backdoor (CVE — versions 1.82.7 and 1.82.8)

### Spark-1 — LiteLLM versions found across all venvs

| Environment | Version | Status |
|---|---|---|
| `.pyenv/versions/3.12.4` | 1.75.3 | CLEAN |
| `ai-business/unsloth-env` | 1.80.0 | CLEAN |
| `miniconda3/envs/nat` | 1.82.6 | CLEAN |
| `miniconda3/envs/hipporag` | 1.81.0 | CLEAN |
| `miniconda3` (base 3.13) | 1.80.0 | CLEAN |
| uv cache (archived) | 1.80.5, 1.75.3, 1.82.6 | CLEAN (cache only, not active) |

**Highest version on Spark-1: 1.82.6 — one version below the backdoor threshold (1.82.7).**

### Spark-2 — LiteLLM versions found across all venvs

| Environment | Version | Status |
|---|---|---|
| `ai-business/.venv` | 1.82.6 | CLEAN |
| `miniconda3/envs/nat` | 1.82.6 | CLEAN |
| `miniconda3/envs/hipporag` | 1.81.0 | CLEAN |
| uv cache (archived) | 1.82.6 | CLEAN (cache only) |

**Highest version on Spark-2: 1.82.6 — CLEAN.**

### Backdoor .pth file scan

No suspicious .pth files found that match the LiteLLM backdoor profile. All .pth files found on both nodes are legitimate:
- `_virtualenv.pth` — standard venv scaffolding
- `distutils-precedence.pth` — setuptools shim
- `a1_coverage.pth`, `__editable__.*`, `sphinxcontrib_jsmath*`, `coloredlogs.pth`, `_rapids_dask_dependency.pth`, `_numba_cuda_redirector.pth` — all known legitimate packages

**LiteLLM Result: CLEAN on both nodes. Neither 1.82.7 nor 1.82.8 is present anywhere.**

---

## CHECK 2: Ollama Version and CVE-2025-63389

| Node | Version | Binding | Status |
|---|---|---|---|
| Spark-1 | 0.18.3 | `*:11434` (all interfaces) | PATCHED — well above 0.12.4 threshold |
| Spark-2 | 0.16.2 | `*:11434` (all interfaces) | PATCHED — well above 0.12.4 threshold |

Both Ollama instances are bound to all interfaces (`0.0.0.0`), not just localhost. This is expected given the Cloudflare tunnel and cluster RPC use cases.

**Ollama Result: PATCHED on both nodes. CVE-2025-63389 does not apply.**

Note: The `ollama.ultrarag.app` public tunnel remains active. Since both nodes are patched, no immediate shutdown is required. However, consider restricting this tunnel to authenticated access as a defense-in-depth measure — it is a live attack surface regardless of version.

---

## CHECK 3: Axios RAT (sfrclak.com C2 — /tmp/ld.py persistence)

### Spark-1
- `ss -tnp | grep sfrc`: **no sfrc connections**
- `/var/log/` sfrclak grep: **not found** (auth.log shows a *prior security check* that searched for sfrclak on 2026-03-31 — this is the previous scan, not a sign of infection)
- `/tmp/ld.py`: **NOT FOUND**
- Crontab: Reviewed — all entries are known legitimate services (tunnel keepalive, harvester, AI Army scripts, NLF consumer, patent backup). No anomalous entries.

### Spark-2
- `ss -tnp | grep sfrc`: **no sfrc connections**
- `/var/log/` sfrclak grep: **not found** (same pattern as Spark-1 — the auth.log entry is the prior scan)
- `/tmp/ld.py`: **NOT FOUND**
- Crontab: One entry — `session_guardian.py` every 5 minutes — this is a known AI Army service. CLEAN.

**RAT C2 Result: CLEAN on both nodes.**

---

## CHECK 4: Axios Versions in Node Projects

### Spark-1

| File | Version | Status |
|---|---|---|
| `.npm/_npx/228916dc.../axios` | 1.13.2 | CLEAN |
| `.npm/_npx/12b05d58.../axios` | 1.13.2 | CLEAN |
| `.npm/_npx/75ac80b8.../axios` | 0.21.4 | CLEAN |

### Spark-2

| File | Version | Status |
|---|---|---|
| `.nemoclaw/source/node_modules/axios` | 1.13.6 | CLEAN |
| `ref-tools-mcp/node_modules/axios` | 1.8.4 | CLEAN |

No version 1.14.1 or 0.30.4 found on either node.

**Axios Result: CLEAN on both nodes.**

---

## Final Checklist

| Item | Spark-1 | Spark-2 |
|---|---|---|
| LiteLLM version | 1.82.6 max — NOT INSTALLED (no 1.82.7/1.82.8) | 1.82.6 max — NOT INSTALLED (no 1.82.7/1.82.8) |
| Ollama version | 0.18.3 — PATCHED | 0.16.2 — PATCHED |
| `/tmp/ld.py` | NOT FOUND | NOT FOUND |
| sfrclak.com connections | NONE | NONE |
| Suspicious .pth files | NONE | NONE |
| Poisoned Axios versions | NONE (1.13.2, 0.21.4) | NONE (1.13.6, 1.8.4) |

**OVERALL VERDICT: CLEAN**

---

## Recommendations (non-urgent)

1. **Pin LiteLLM below 1.82.7** in all active venvs until the supply chain incident is fully resolved upstream. The highest currently installed is 1.82.6 — you are one accidental `pip install --upgrade` away from pulling a poisoned version. Add version pins to requirements files where LiteLLM is a dependency.

2. **Consider Ollama tunnel restriction**: `ollama.ultrarag.app` exposes 46 models publicly. Even patched, unauthenticated model inference access is a resource and data exposure risk. Consider adding Cloudflare Access in front of this tunnel.

3. **The auth.log shows a prior security scan was run 2026-03-31** — this confirms someone (likely NemoClaw or Hermes) was already checking for sfrclak before this session. That is normal and expected behavior from the security monitoring scripts.

4. **No action required on crontabs** — all Spark-1 and Spark-2 cron entries match known services documented in CLAUDE.md.
