#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys

from pka_lib import MANIFEST, ROOT, find_task_path, parse_task_file, read_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a task evidence pack")
    parser.add_argument("--task-id", required=True)
    args = parser.parse_args()

    task_path = find_task_path(args.task_id)
    data, body = parse_task_file(task_path)

    manifest_matches = []
    for line in read_text(MANIFEST).splitlines():
        if data.get("title", "") in line or args.task_id in line:
            manifest_matches.append(line)

    output_dir = ROOT / "Owner's Inbox" / "evidence"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.task_id}-evidence-pack.md"

    content = "\n".join(
        [
            f"# Evidence Pack - {args.task_id}",
            "",
            f"- **Title**: {data.get('title','')}",
            f"- **State**: {data.get('state','')}",
            f"- **Owner**: {data.get('owner','')}",
            f"- **Route**: {data.get('route','').replace('|',' -> ')}",
            f"- **Verdict**: {data.get('verdict','')}",
            f"- **Deliverable File**: {data.get('deliverable_file','')}",
            "",
            "## Task Record",
            f"`{task_path.relative_to(ROOT)}`",
            "",
            "```md",
            read_text(task_path).rstrip(),
            "```",
            "",
            "## Manifest Entries",
            *(manifest_matches or ["- No manifest match found"]),
            "",
            "## Summary",
            body.strip(),
            "",
        ]
    )
    output_path.write_text(content, encoding="utf-8")
    print(f"Created {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
