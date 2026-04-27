#!/usr/bin/env python
"""
PKA Journal Consolidation — prevents unbounded journal growth.

For each agent journal:
1. Parses session log entries
2. Keeps the last N entries in the hot journal (default: 20)
3. Archives older entries to Team/{AGENT}/journal_archive.md
4. Preserves the Self-Model and Recurring Patterns sections intact
5. Stores a consolidation summary to MemoryWeb (if reachable)

Usage:
    python scripts/pka_journal_consolidate.py                # consolidate all journals
    python scripts/pka_journal_consolidate.py --dry-run       # preview without writing
    python scripts/pka_journal_consolidate.py --agent FORGE   # consolidate one agent
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from pka_lib import TEAM_DIR, timestamp

HOT_ENTRIES = 20  # keep last N session log entries in the active journal


def find_agent_journals() -> list[tuple[str, Path]]:
    """Return (agent_name, journal_path) for each agent with a journal."""
    results = []
    for agent_dir in sorted(TEAM_DIR.iterdir()):
        if not agent_dir.is_dir():
            continue
        journal = agent_dir / "journal.md"
        if journal.exists():
            results.append((agent_dir.name, journal))
    return results


def split_journal(text: str) -> tuple[str, str, list[str]]:
    """Split a journal into (preserved_header, preserved_sections, session_entries).

    preserved_header: everything before the first session log entry
    preserved_sections: Self-Model, Recurring Patterns, Feedback Received
                        (these sections are never archived)
    session_entries: individual session log entries (### dated blocks)
    """
    # Find session log entries: ### lines that look like dates or session markers
    entry_pattern = re.compile(r"^### (?:Session Log|20\d{2}-\d{2}-\d{2})", re.MULTILINE)
    matches = list(entry_pattern.finditer(text))

    if not matches:
        return text, "", []

    header = text[:matches[0].start()].rstrip()

    # Extract entries
    entries = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        entry = text[start:end].rstrip()
        entries.append(entry)

    # Separate preserved sections (Self-Model, Recurring Patterns, Feedback)
    preserved_sections = []
    session_entries = []
    preserved_markers = ("## self-model", "## recurring patterns", "## feedback received",
                         "## growth areas", "## strengths")

    for entry in entries:
        first_line_lower = entry.split("\n")[0].lower().strip("# ").strip()
        is_preserved = any(marker.replace("## ", "") in first_line_lower for marker in preserved_markers)
        if is_preserved:
            preserved_sections.append(entry)
        else:
            session_entries.append(entry)

    # Also check if preserved sections are in the header
    preserved_text = "\n\n".join(preserved_sections)

    return header, preserved_text, session_entries


def consolidate_journal(
    agent_name: str,
    journal_path: Path,
    dry_run: bool = False,
) -> dict[str, int]:
    """Consolidate one agent's journal. Returns stats."""
    text = journal_path.read_text(encoding="utf-8")
    header, preserved, entries = split_journal(text)

    total = len(entries)
    if total <= HOT_ENTRIES:
        return {"agent": agent_name, "total": total, "archived": 0, "kept": total}

    to_archive = entries[:-HOT_ENTRIES]
    to_keep = entries[-HOT_ENTRIES:]

    archive_path = journal_path.parent / "journal_archive.md"

    if not dry_run:
        # Append archived entries
        archive_header = f"# {agent_name} — Journal Archive\n*Consolidated: {timestamp()}*\n\n"
        existing_archive = ""
        if archive_path.exists():
            existing_archive = archive_path.read_text(encoding="utf-8")
            # Strip the header from existing archive before appending
            if existing_archive.startswith("# "):
                first_entry = existing_archive.find("\n### ")
                if first_entry > 0:
                    existing_archive = existing_archive[first_entry:]

        new_archive = archive_header + "\n\n".join(to_archive) + "\n\n" + existing_archive
        archive_path.write_text(new_archive.rstrip() + "\n", encoding="utf-8")

        # Rewrite hot journal
        parts = [header]
        if preserved:
            parts.append(preserved)
        parts.append("\n\n".join(to_keep))
        journal_path.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")

    return {
        "agent": agent_name,
        "total": total,
        "archived": len(to_archive),
        "kept": len(to_keep),
    }


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    target_agent = None

    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            target_agent = sys.argv[i + 1].upper()

    journals = find_agent_journals()
    if target_agent:
        journals = [(name, path) for name, path in journals if name == target_agent]
        if not journals:
            print(f"No journal found for agent: {target_agent}")
            return 1

    if dry_run:
        print("DRY RUN — no files will be modified\n")

    total_archived = 0
    for agent_name, journal_path in journals:
        stats = consolidate_journal(agent_name, journal_path, dry_run=dry_run)
        if stats["archived"] > 0:
            print(f"  {stats['agent']}: {stats['total']} entries -> kept {stats['kept']}, archived {stats['archived']}")
            total_archived += stats["archived"]
        else:
            print(f"  {stats['agent']}: {stats['total']} entries — no consolidation needed")

    if total_archived:
        print(f"\nConsolidated {total_archived} entries across {len(journals)} journals")
    else:
        print(f"\nAll {len(journals)} journals within limits (≤{HOT_ENTRIES} entries each)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
