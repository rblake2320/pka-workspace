"""
NeMo Curator Pipeline — Data Flywheel Step 2
Cleans, deduplicates, and quality-filters the exported JSONL dataset
before fine-tuning on Spark-1/2.

Hardware: RTX 5090 (Windows PC, 32GB VRAM) via SSH tunnel OR
          Spark-1/2 (GB10, 120GB each)

Usage:
    python3 nemo_curator_pipeline.py --input flywheel_data/flywheel_export_*.jsonl
    python3 nemo_curator_pipeline.py --input flywheel_data/ --output clean_data/
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Iterator

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MIN_INPUT_CHARS = 10
MIN_OUTPUT_CHARS = 20
MAX_DUPLICATE_RATIO = 0.8   # Jaccard similarity threshold for near-dedup


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> Iterator[dict]:
    """Load one or more JSONL files (accepts file or directory)."""
    paths = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    for p in paths:
        with open(p, errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


# ---------------------------------------------------------------------------
# Cleaning passes
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Normalize whitespace, remove control chars."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = re.sub(r" {3,}", "  ", text)
    text = text.strip()
    return text


def passes_quality_filter(record: dict) -> bool:
    """Hard-filter: length, non-empty, no obvious errors."""
    inp = record.get("input", "")
    out = record.get("output", "")

    if len(inp) < MIN_INPUT_CHARS or len(out) < MIN_OUTPUT_CHARS:
        return False

    # Filter pure error responses
    error_patterns = [
        r"^traceback \(most recent call last\)",
        r"^(error|exception):\s",
        r"^\s*none\s*$",
        r"^internal server error",
    ]
    out_lower = out.lower().strip()
    for pat in error_patterns:
        if re.match(pat, out_lower):
            return False

    # Filter responses that are just the input repeated
    if out.strip()[:100] == inp.strip()[:100]:
        return False

    return True


def shingle_hash(text: str, k: int = 5) -> set:
    """k-shingle set for Jaccard near-dedup."""
    tokens = text.lower().split()
    return {
        hashlib.md5(" ".join(tokens[i:i+k]).encode()).hexdigest()
        for i in range(max(1, len(tokens) - k + 1))
    }


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(input_path: Path, output_path: Path) -> dict:
    """Run full Curator pipeline. Returns stats dict."""
    stats = {
        "loaded": 0,
        "after_quality_filter": 0,
        "after_dedup": 0,
        "written": 0,
    }

    # Pass 1: load + clean + quality filter
    clean_records: list[dict] = []
    for rec in load_jsonl(input_path):
        stats["loaded"] += 1
        rec["input"] = clean_text(rec.get("input", ""))
        rec["output"] = clean_text(rec.get("output", ""))
        if passes_quality_filter(rec):
            clean_records.append(rec)
    stats["after_quality_filter"] = len(clean_records)
    log.info("Quality filter: %d → %d", stats["loaded"], stats["after_quality_filter"])

    # Pass 2: near-dedup by input shingles
    shingles_seen: list[set] = []
    deduped: list[dict] = []
    for rec in clean_records:
        sh = shingle_hash(rec["input"])
        is_dup = any(jaccard(sh, seen) >= MAX_DUPLICATE_RATIO for seen in shingles_seen)
        if not is_dup:
            shingles_seen.append(sh)
            deduped.append(rec)
    stats["after_dedup"] = len(deduped)
    log.info("Dedup: %d → %d", stats["after_quality_filter"], stats["after_dedup"])

    # Pass 3: sort by quality score descending
    deduped.sort(key=lambda r: r.get("metadata", {}).get("quality_score", 0.5), reverse=True)

    # Write output
    output_path.mkdir(parents=True, exist_ok=True)
    out_file = output_path / "curator_cleaned.jsonl"
    with open(out_file, "w") as f:
        for rec in deduped:
            f.write(json.dumps(rec) + "\n")
            stats["written"] += 1

    log.info("Written %d clean records to %s", stats["written"], out_file)

    # Write summary
    summary = {
        "stats": stats,
        "output_file": str(out_file),
        "next_step": (
            f"python3 /home/rblake2320/data-flywheel/fine_tune_trigger.py "
            f"--input {out_file} --base-model qwen2.5-coder:32b"
        ),
    }
    summary_file = output_path / "curator_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=== NeMo Curator Pipeline Complete ===")
    print(f"  Loaded:          {stats['loaded']:,}")
    print(f"  After quality:   {stats['after_quality_filter']:,}")
    print(f"  After dedup:     {stats['after_dedup']:,}")
    print(f"  Written:         {stats['written']:,}")
    print(f"  Output:          {out_file}")
    print(f"\n  Next: {summary['next_step']}")

    return stats


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="NeMo Curator Pipeline")
    parser.add_argument("--input", required=True, help="Input JSONL file or directory")
    parser.add_argument("--output", default="/home/rblake2320/data-flywheel/clean_data",
                        help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: Input path not found: {input_path}")
        raise SystemExit(1)

    run_pipeline(input_path, output_path)


if __name__ == "__main__":
    main()
