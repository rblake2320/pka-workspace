#!/usr/bin/env python
from __future__ import annotations

import json
import re
import sys

from pka_lib import REPORTS_DIR, ROOT, TEAM_DIR

ROSTER = TEAM_DIR / "roster.md"
MATRIX = TEAM_DIR / "AGENT_TOOL_ENTITLEMENTS.json"
OUT = REPORTS_DIR / "PKA_AGENT_ENTITLEMENTS_REPORT.md"
REQUIRED_KEYS = {"risk_tier", "allowed_actions", "blocked_actions", "escalation_required"}
NON_AGENT_HEADINGS = {
    "Team Operating Rules",
    "Inbox Protocol",
    "Bench Agents",
    "Core Rules",
    "Hiring Pipeline",
}


def roster_agents() -> list[str]:
    names: list[str] = []
    pattern = re.compile(r"^##\s+([A-Z]+)\s+[—-]\s+")
    for line in ROSTER.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        name = match.group(1)
        if name not in NON_AGENT_HEADINGS:
            names.append(name)
    return names


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    roster = roster_agents()
    issues: list[str] = []

    for agent in roster:
        if agent not in data:
            issues.append(f"Missing entitlement entry for {agent}")
            continue
        entry = data[agent]
        missing = sorted(REQUIRED_KEYS - set(entry))
        if missing:
            issues.append(f"{agent}: missing keys {', '.join(missing)}")
            continue
        for key in ("allowed_actions", "blocked_actions", "escalation_required"):
            if not isinstance(entry[key], list) or not entry[key]:
                issues.append(f"{agent}: {key} must be a non-empty list")
        if not entry.get("risk_tier"):
            issues.append(f"{agent}: risk_tier must be non-empty")

    extra = sorted(set(data) - set(roster))
    for agent in extra:
        issues.append(f"Entitlement entry has no matching roster agent: {agent}")

    lines = [
        "# PKA Agent Entitlements Report",
        "",
        f"- Roster agents: {len(roster)}",
        f"- Entitlement entries: {len(data)}",
        f"- Overall: {'PASS' if not issues else 'FAIL'}",
        "",
        "## Agent Coverage",
    ]
    for agent in roster:
        lines.append(f"- {agent}: {'PASS' if agent in data else 'FAIL'}")
    if issues:
        lines += [
            "",
            "## Issues",
        ]
        lines.extend(f"- {issue}" for issue in issues)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if issues:
        print("PKA Entitlement Check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PKA Entitlement Check: PASS")
    print(f"- Roster agents: {len(roster)}")
    print(f"- Report: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
