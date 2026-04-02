#!/usr/bin/env python
"""
Compact agent journals — keep the last KEEP_ENTRIES Session Log entries.

Entries older than KEEP_ENTRIES are moved into an <!-- ARCHIVED --> block
at the bottom of the Session Log section to keep the file scannable while
preventing unbounded growth.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM_DIR = ROOT / "Team"
KEEP_ENTRIES = 10

AGENTS = [
    "AXIOM", "FORGE", "SENTINEL", "HELM", "NOVA",
    "VENTURE", "SPARK", "LEGAL", "SCRIBE", "GRID",
    "RADAR", "CRUCIBLE", "DEBUGGER",
]

# Matches a session entry: starts at ### YYYY-MM-DD —, ends before next ###, ##, or EOF
_ENTRY_RE = re.compile(
    r"(### \d{4}-\d{2}-\d{2} —.*?)(?=\n### \d{4}-\d{2}-\d{2} —|\n## |\Z)",
    re.DOTALL,
)


def compact_journal(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")

    # Locate ## Session Log
    sl_match = re.search(r"^## Session Log\b", text, re.MULTILINE)
    if not sl_match:
        return False, "no Session Log section"

    # Find the closing --> of the HTML comment block
    comment_end = text.find("-->", sl_match.end())
    if comment_end == -1:
        return False, "no comment block end"
    after_comment_start = comment_end + 3

    # Find the start of the next ## section (e.g. ## Feedback Received)
    next_section = re.search(r"^## \S", text[after_comment_start:], re.MULTILINE)
    if next_section:
        entries_end = after_comment_start + next_section.start()
    else:
        entries_end = len(text)

    entries_block = text[after_comment_start:entries_end]
    tail = text[entries_end:]

    entries = _ENTRY_RE.findall(entries_block)

    if len(entries) <= KEEP_ENTRIES:
        return False, f"{len(entries)} entries — within limit"

    keep = entries[-KEEP_ENTRIES:]
    archive = entries[:-KEEP_ENTRIES]

    archive_block = ""
    if archive:
        archive_block = (
            "\n\n<!-- ARCHIVED ENTRIES\n"
            + "\n\n".join(e.strip() for e in archive)
            + "\n-->\n"
        )

    new_entries_block = "\n\n" + "\n\n".join(e.strip() for e in keep) + "\n"
    new_text = (
        text[:after_comment_start]
        + new_entries_block
        + archive_block
        + tail
    )
    path.write_text(new_text, encoding="utf-8")
    return True, f"compacted {len(entries)} -> {len(keep)}, archived {len(archive)}"


def main() -> int:
    compacted = 0
    for agent in AGENTS:
        journal = TEAM_DIR / agent / "journal.md"
        if not journal.exists():
            continue
        changed, msg = compact_journal(journal)
        if changed:
            compacted += 1
            print(f"  - {agent}: {msg}")

    if compacted == 0:
        print("PKA Journal Compact: all journals within limit")
    else:
        print(f"PKA Journal Compact: compacted {compacted} journal(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
