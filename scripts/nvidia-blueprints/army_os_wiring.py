"""
Data Flywheel — AI Army OS Wiring Layer
Connects production query logs to the NVIDIA Data Flywheel pipeline.

Data sources:
  - PostgreSQL memoryweb DB: rag.query_log (Ultra RAG queries + responses)
  - PostgreSQL memoryweb DB: army_os call log (ai-army llm_calls table)
  - Flat log files: ~/ai-army-os/server.log (JSONL entries)

Output: Cleaned JSONL dataset ready for NeMo Curator → fine-tune cycle

Usage:
    python3 army_os_wiring.py --dry-run        # count records, no export
    python3 army_os_wiring.py --export         # export to flywheel_data/
    python3 army_os_wiring.py --since 7d       # last 7 days only
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from collections.abc import Iterator
from datetime import datetime, timedelta
from pathlib import Path

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PG_DSN = os.getenv(
    "FLYWHEEL_PG_DSN",
    "postgresql://memoryweb:memoryweb@localhost:5432/memoryweb"
)

ARMY_LOG = Path("/home/rblake2320/ai-army-os/server.log")
EXPORT_DIR = Path("/home/rblake2320/data-flywheel/flywheel_data")

# Quality thresholds — only keep examples above these scores
MIN_RESPONSE_TOKENS = 20    # Filter one-word / error responses
MAX_RESPONSE_TOKENS = 2000  # Filter runaway/corrupted completions
MIN_QUALITY_SCORE = 0.5     # Placeholder: 0.0–1.0 from heuristics


# ---------------------------------------------------------------------------
# Source 1: Ultra RAG query log (PostgreSQL)
# ---------------------------------------------------------------------------

def iter_rag_queries(since: datetime | None = None) -> Iterator[dict]:
    """Yield {prompt, response, model, latency_ms, score} from rag query log."""
    try:
        import psycopg2
        conn = psycopg2.connect(PG_DSN)
        cur = conn.cursor()

        # Ultra RAG: query_log with chunk summaries as context
        # Note: answer_text in provenance_chains is not yet populated.
        # We pull queries that have high quality_score and join the top
        # retrieved chunk as the expected response (for weak supervision).
        query = """
            SELECT q.query_text, q.quality_score,
                   q.collection, q.latency_ms, q.created_at,
                   (SELECT c.content FROM rag.chunks c
                    JOIN rag.chunk_utility cu ON cu.chunk_id = c.id
                    WHERE c.collection = q.collection
                    ORDER BY cu.use_count DESC LIMIT 1) AS top_chunk
            FROM rag.query_log q
            WHERE q.quality_score >= 0.7
              AND length(q.query_text) > 20
        """
        if since:
            query += " AND q.created_at >= %s"
            cur.execute(query, (since,))
        else:
            cur.execute(query)

        for row in cur.fetchall():
            prompt, quality_score, model, latency, ts, top_chunk = row
            if not top_chunk or len(top_chunk) < 50:
                continue
            score = quality_score if quality_score else 0.7
            yield {
                "source": "ultra_rag",
                "prompt": prompt,
                "response": top_chunk[:2000],
                "model": model or "unknown",
                "latency_ms": latency or 0,
                "quality_score": round(score * 0.85, 3),  # Discount: weak supervision
                "timestamp": ts.isoformat() if ts else None,
            }
        conn.close()
    except Exception as e:
        log.warning("RAG query log unavailable: %s", e)
        return


# ---------------------------------------------------------------------------
# Source 2: AI Army OS tasks table (PostgreSQL — real prompt→response pairs)
# ---------------------------------------------------------------------------

def iter_army_log(since: datetime | None = None) -> Iterator[dict]:
    """Pull completed tasks from Army OS tasks table (real training pairs)."""
    try:
        import psycopg2
        conn = psycopg2.connect(PG_DSN)
        cur = conn.cursor()

        query = """
            SELECT title, description, spec, result, model_used,
                   tokens_used, cost_usd, completed_at
            FROM army_os.tasks
            WHERE status = 'completed'
              AND result IS NOT NULL
              AND length(result) > 50
              AND title IS NOT NULL
        """
        if since:
            query += " AND completed_at >= %s"
            cur.execute(query, (since,))
        else:
            cur.execute(query)

        for row in cur.fetchall():
            title, desc, spec, result, model, tokens, cost, ts = row
            # Build prompt from task fields
            prompt_parts = [p for p in [title, desc, spec] if p and len(p.strip()) > 3]
            prompt = "\n\n".join(prompt_parts[:2000])
            if not prompt.strip():
                continue

            yield {
                "source": "army_os_tasks",
                "prompt": prompt,
                "response": result[:4000],
                "model": model or "unknown",
                "latency_ms": 0,
                "quality_score": 0.75,  # Completed tasks are generally high quality
                "timestamp": ts.isoformat() if ts else None,
            }
        conn.close()
    except Exception as e:
        log.warning("Army OS tasks table unavailable: %s", e)
        return


# ---------------------------------------------------------------------------
# Quality filtering heuristics
# ---------------------------------------------------------------------------

def score_example(ex: dict) -> float:
    """Heuristic quality score 0.0–1.0 for a prompt/response pair."""
    score = ex.get("quality_score", 0.7)

    response = ex.get("response", "")
    token_count = len(response.split())

    # Penalize very short or very long responses
    if token_count < MIN_RESPONSE_TOKENS:
        score *= 0.3
    elif token_count > MAX_RESPONSE_TOKENS:
        score *= 0.6

    # Reward voted helpful responses
    if ex.get("quality_score", 0) >= 0.8:
        score = min(1.0, score * 1.2)

    # Penalize error/exception responses
    error_phrases = ["error:", "exception:", "traceback (most", "404", "500 internal"]
    if any(p in response.lower() for p in error_phrases):
        score *= 0.4

    return round(min(1.0, max(0.0, score)), 3)


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_dataset(records: list[dict], output_dir: Path) -> Path:
    """Write cleaned JSONL ready for NeMo Curator."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"flywheel_export_{ts}.jsonl"

    with open(out_path, "w") as f:
        for rec in records:
            # NeMo Curator SFT format: {"input": "...", "output": "..."}
            curator_rec = {
                "input": rec["prompt"],
                "output": rec["response"],
                "metadata": {
                    "source": rec["source"],
                    "model": rec["model"],
                    "quality_score": rec["quality_score"],
                    "timestamp": rec.get("timestamp"),
                }
            }
            f.write(json.dumps(curator_rec) + "\n")

    log.info("Exported %d records to %s", len(records), out_path)
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_since(s: str) -> datetime | None:
    if not s:
        return None
    if s.endswith("d"):
        return datetime.now() - timedelta(days=int(s[:-1]))
    if s.endswith("h"):
        return datetime.now() - timedelta(hours=int(s[:-1]))
    return None


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="Data Flywheel — Army OS wiring")
    parser.add_argument("--dry-run", action="store_true", help="Count records, no export")
    parser.add_argument("--export", action="store_true", help="Export JSONL dataset")
    parser.add_argument("--since", default="", help="Time filter e.g. 7d, 24h")
    parser.add_argument("--min-score", type=float, default=MIN_QUALITY_SCORE)
    args = parser.parse_args()

    since = parse_since(args.since)
    if since:
        log.info("Filtering records since %s", since.isoformat())

    # Collect from all sources
    all_records: list[dict] = []

    log.info("Source 1: Ultra RAG query log...")
    rag_count = 0
    for ex in iter_rag_queries(since=since):
        ex["quality_score"] = score_example(ex)
        if ex["quality_score"] >= args.min_score:
            all_records.append(ex)
            rag_count += 1
    log.info("  RAG: %d qualifying examples", rag_count)

    log.info("Source 2: AI Army OS task log...")
    army_count = 0
    for ex in iter_army_log(since=since):
        ex["quality_score"] = score_example(ex)
        if ex["quality_score"] >= args.min_score:
            all_records.append(ex)
            army_count += 1
    log.info("  Army OS: %d qualifying examples", army_count)

    total = len(all_records)
    log.info("Total qualifying examples: %d", total)

    if args.dry_run:
        print(f"\nDRY RUN — {total} records would be exported")
        print(f"  From Ultra RAG:  {rag_count}")
        print(f"  From Army OS:    {army_count}")
        print(f"  Min score:       {args.min_score}")
        if total > 0:
            avg_score = sum(r["quality_score"] for r in all_records) / total
            print(f"  Avg quality:     {avg_score:.3f}")
        return

    if args.export:
        if total == 0:
            print("No qualifying records found — nothing to export")
            sys.exit(1)
        out = export_dataset(all_records, EXPORT_DIR)
        print(f"\nExported {total} records to: {out}")
        print(f"Next step: python3 /home/rblake2320/data-flywheel/nemo_curator_pipeline.py --input {out}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
