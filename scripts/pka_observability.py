#!/usr/bin/env python
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from pka_lib import LOGS_DIR, REPORTS_DIR

HISTORY_FILE = LOGS_DIR / "pka_validation_history.jsonl"
OUTPUT_PATH = REPORTS_DIR / "PKA_OBSERVABILITY_REPORT.md"


def load_history() -> list[dict[str, object]]:
    if not HISTORY_FILE.exists():
        return []
    rows: list[dict[str, object]] = []
    for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def main() -> int:
    history = load_history()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if not history:
        text = "# PKA Observability Report\n\n- No validation history recorded yet.\n"
        OUTPUT_PATH.write_text(text, encoding="utf-8")
        print(text.strip())
        return 0

    latest = history[-1]
    scores = [int(item.get("score", 0)) for item in history]
    pass_rates = [
        f"{item.get('passed', 0)}/{item.get('total', 0)}"
        for item in history[-5:]
    ]
    perfect_runs = sum(1 for score in scores if score == 100)
    latest_checks = latest.get("checks", [])

    lines = [
        "# PKA Observability Report",
        "",
        f"- Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"- Validation runs recorded: {len(history)}",
        f"- Latest validation score: {latest.get('score', 0)}/100",
        f"- Latest validation pass count: {latest.get('passed', 0)}/{latest.get('total', 0)}",
        f"- Perfect validation runs: {perfect_runs}/{len(history)}",
        f"- Trailing 5 pass counts: {', '.join(pass_rates)}",
        f"- Score range: {min(scores)}/{max(scores)}",
        "",
        "## Latest Checks",
    ]
    for check in latest_checks:
        lines.append(
            f"- {check.get('name','')}: {'PASS' if check.get('ok') else 'FAIL'} | {check.get('summary','')}"
        )

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
