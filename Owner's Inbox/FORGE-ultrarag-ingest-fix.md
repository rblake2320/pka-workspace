# FORGE — Ultra RAG Ingest Fix: Silent Dict-Path Failure

**Date**: 2026-03-23
**Agent**: FORGE
**Status**: FIXED AND VERIFIED

---

## The Bug

**File**: `/home/rblake2320/ultra-rag/rag_ingest.py`
**Line**: 156 (original)

When `config.yaml` configures a collection path as a dict (with `path` + `max_depth` keys), the original code passed the entire dict object to `Path()`:

```python
# BEFORE (broken)
paths = [Path(p) for p in coll_cfg.get("paths", [])]
```

This raises `TypeError: argument should be a str or an os.PathLike object` when `p` is `{'path': '/some/dir', 'max_depth': 0}`. The exception was silently swallowed by calling code, which returned HTTP 200 with 0 chunks — a classic silent failure.

**Affected paths in the personal collection** (all were silently skipped):

| Config entry | Type |
|---|---|
| `{'path': 'C:\Users\techai', 'max_depth': 0}` | dict |
| `{'path': 'D:\patent-readiness-master\01_evidence_raw\dgx_spark_1\patent_evidence', 'max_depth': 0}` | dict |
| `{'path': 'D:\patent-readiness-master\01_evidence_raw\rtx_5090\downloads', 'max_depth': 0}` | dict |
| `{'path': 'D:\acq-copilot-v2', 'max_depth': 0}` | dict |
| `{'path': 'D:\memory-web', 'max_depth': 0}` | dict |
| `{'path': 'D:\memory-pulse', 'max_depth': 0}` | dict |

---

## The Fix

**Lines 156-175 of `rag_ingest.py`** on Spark-1 (`/home/rblake2320/ultra-rag/rag_ingest.py`)

```python
# BEFORE — line 156 (broken)
paths      = [Path(p) for p in coll_cfg.get("paths", [])]
excl_dirs  = set(coll_cfg.get("exclude_dirs", []))
skip_files = set(coll_cfg.get("skip_files", []))

# Collect files
files = []
for base in paths:
    if not base.exists():
        log.warning(f"Path not found: {base}")
        continue
    for fpath in sorted(base.rglob("*")):
        if not fpath.is_file():
            continue
        rel = fpath.relative_to(base)
        if any(d in excl_dirs for d in rel.parts):
            continue
        if fpath.name in skip_files:
            continue
        if fpath.suffix.lower() in PARSERS:
            files.append(fpath)
```

```python
# AFTER — fixed (handles both plain string and dict-style path entries)
# Each entry in paths may be a plain string or a dict with path + optional max_depth
raw_paths  = coll_cfg.get("paths", [])
path_specs = [
    {"path": Path(p["path"] if isinstance(p, dict) else p),
     "max_depth": p.get("max_depth") if isinstance(p, dict) else None}
    for p in raw_paths
]
excl_dirs  = set(coll_cfg.get("exclude_dirs", []))
skip_files = set(coll_cfg.get("skip_files", []))

# Collect files
files = []
for spec in path_specs:
    base      = spec["path"]
    max_depth = spec["max_depth"]  # None = unlimited
    if not base.exists():
        log.warning(f"Path not found: {base}")
        continue
    for fpath in sorted(base.rglob("*")):
        if not fpath.is_file():
            continue
        rel = fpath.relative_to(base)
        # Honour max_depth: len(rel.parts)-1 = directory depth of file
        if max_depth is not None and len(rel.parts) - 1 > max_depth:
            continue
        if any(d in excl_dirs for d in rel.parts):
            continue
        if fpath.name in skip_files:
            continue
        if fpath.suffix.lower() in PARSERS:
            files.append(fpath)
```

**Two bugs fixed in one change:**
1. `Path(p)` on a dict → `Path(p["path"] if isinstance(p, dict) else p)` — the primary silent failure
2. `max_depth` was stored in config but completely ignored in the rglob walk — now enforced

---

## Live Proof

Test script ran `ingest_collection("personal", conn)` with the personal collection paths replaced by a single dict-style entry `{"path": tmpdir, "max_depth": 0}`, containing one 1,656-byte `.md` file.

**Before fix would have done**: raised `TypeError`, returned summary with 0 files found, 0 chunks.

**After fix result**:

```
Collection 'personal': 1 files found
[1/1] forge_fix_verification_full.md
  Parsing: forge_fix_verification_full.md
  OK 3 chunks, 345 tokens (0.1s)

Ingest summary: {
  'collection': 'personal', 'files': 1, 'ingested': 1,
  'skipped': 0, 'errors': 0, 'chunks': 3, 'tokens': 345
}

Before: 2143 docs, 23379 chunks
After:  2144 docs, 23382 chunks
New chunks: 3

Document row: (2282, 'forge_fix_verification_full.md', 3)
  Chunk 0: 'The Ultra RAG ingest pipeline had a silent failure bug. When a collection path i'
  Chunk 1: 'Line 156 of rag_ingest.py was changed from:\n\n```python\npaths = [Path(p) for p in'
  Chunk 2: 'The personal collection in config.yaml has multiple dict-style path entries:\n\n- '

PASS: dict-style path entry correctly ingested, chunks in DB
```

**DB verification**: `rag.documents` row id=2282, chunk_count=3. `rag.chunks` count went from 23,379 to 23,382. Three real rows in the database — not just a 200 response.

---

## Notes

- Both `/api/ingest` and `/api/upload` endpoints call `_run_parse` → `ingest_collection` — both are covered by this fix.
- The `/api/upload` endpoint copies files to `data/<collection>/` — that directory is not listed in config.yaml paths, so upload-then-parse only works if `data/<collection>/` is added to the collection config (separate issue, pre-existing).
- No restart of the gunicorn server required — `rag_ingest.py` is imported fresh per request via `importlib` lazy imports inside the endpoint handlers.
