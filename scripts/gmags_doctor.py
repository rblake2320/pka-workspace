#!/usr/bin/env python3
"""
gmags_doctor.py — PKA Workspace Health Check
Checks real workspace state: agent/roster sync, entitlement coverage,
stale deliverables, orphaned files, and governance tool availability.

USAGE:
  python scripts/gmags_doctor.py                  # full check
  python scripts/gmags_doctor.py --check agents   # agents only
  python scripts/gmags_doctor.py --check roster   # roster sync only
  python scripts/gmags_doctor.py --check inbox    # Owner's Inbox staleness
  python scripts/gmags_doctor.py --check tools    # governance tools

WHAT THIS ACTUALLY CHECKS (not YAML field counting):
  1. Agent/roster sync    — every .claude/agents/*.md has a roster entry and vice versa
  2. AXIOM routing sync   — every agent in AXIOM's routing table has an agent file
  3. Entitlement coverage — AGENT_TOOL_ENTITLEMENTS.json covers all active agents
  4. Orphaned agents      — agent files with no roster entry
  5. Inbox staleness      — Owner's Inbox files older than 30 days with no archival
  6. Handoff freshness    — Team/handoff.md and status.md updated recently
  7. Governance tools     — the 3 CLI tools in governance/tools/ exist and are runnable
  8. Task audit log       — logs/task_audit.jsonl exists and recent entries look healthy
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path(__file__).parent.parent

results = {
    "run_id": f"doctor-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
    "run_at": datetime.now(timezone.utc).isoformat(),
    "checks": {},
    "failures": [],
    "warnings": [],
}


def check(name, passed, detail="", warning=False):
    results["checks"][name] = {"passed": passed, "detail": detail}
    sym = "PASS" if passed else ("WARN" if warning else "FAIL")
    print(f"  [{sym}] {name}" + (f" — {detail}" if detail else ""))
    if not passed:
        if warning:
            results["warnings"].append(f"{name}: {detail}")
        else:
            results["failures"].append(f"{name}: {detail}")
    return passed


# ── 1. Agent / Roster Sync ────────────────────────────────────────────────────
def check_agent_roster_sync():
    print("\n[1] Agent <-> Roster sync")
    agents_dir = BASE / ".claude" / "agents"
    roster_path = BASE / "Team" / "roster.md"

    if not agents_dir.exists():
        check("agents_dir_exists", False, str(agents_dir))
        return
    if not roster_path.exists():
        check("roster_exists", False, str(roster_path))
        return

    agent_files = {p.stem.upper() for p in agents_dir.glob("*.md")}
    roster_text = roster_path.read_text(encoding="utf-8", errors="replace")

    orphaned = []
    for agent in sorted(agent_files):
        in_roster = agent in roster_text.upper()
        if not in_roster:
            orphaned.append(agent)

    check(
        "all_agents_in_roster",
        len(orphaned) == 0,
        f"Orphaned (in .claude/agents/ but not roster.md): {orphaned}" if orphaned else
        f"{len(agent_files)} agents, all in roster"
    )

    # Reverse: find roster mentions not backed by agent files
    roster_lines = [l for l in roster_text.splitlines() if l.strip().startswith("##")]
    roster_names = set()
    for line in roster_lines:
        m = re.search(r'##\s+([A-Z][A-Z0-9_]+)', line)
        if m:
            roster_names.add(m.group(1))

    unlaunched = [n for n in roster_names if n not in agent_files]
    check(
        "roster_agents_have_files",
        len(unlaunched) == 0,
        f"In roster but no agent file: {unlaunched}" if unlaunched else
        f"All {len(roster_names)} roster entries have agent files",
        warning=True  # might be bench agents
    )


# ── 2. AXIOM Routing Sync ─────────────────────────────────────────────────────
def check_axiom_routing():
    print("\n[2] AXIOM routing table sync")
    axiom_path = BASE / ".claude" / "agents" / "AXIOM.md"
    agents_dir = BASE / ".claude" / "agents"

    if not axiom_path.exists():
        check("axiom_exists", False)
        return

    axiom_text = axiom_path.read_text(encoding="utf-8", errors="replace")
    agent_files = {p.stem.upper() for p in agents_dir.glob("*.md") if p.stem.upper() != "AXIOM"}

    # Find agent names mentioned in routing table lines
    routing_section = False
    routed_agents = set()
    for line in axiom_text.splitlines():
        if "Routing Modes" in line:
            routing_section = True
        if routing_section and "|" in line:
            for name in agent_files:
                if name in line.upper():
                    routed_agents.add(name)

    unrouted = agent_files - routed_agents
    check(
        "agents_in_axiom_routing",
        len(unrouted) == 0,
        f"Not mentioned in AXIOM routing: {sorted(unrouted)}" if unrouted else
        f"{len(routed_agents)}/{len(agent_files)} agents covered in routing",
        warning=True  # some agents like SCRIBE may only be called directly
    )


# ── 3. Entitlement Coverage ───────────────────────────────────────────────────
def check_entitlements():
    print("\n[3] AGENT_TOOL_ENTITLEMENTS.json coverage")
    entitlements_path = BASE / "Team" / "AGENT_TOOL_ENTITLEMENTS.json"
    agents_dir = BASE / ".claude" / "agents"

    if not entitlements_path.exists():
        check("entitlements_file_exists", False, str(entitlements_path))
        return

    try:
        with open(entitlements_path, encoding="utf-8") as f:
            entitlements = json.load(f)
    except Exception as e:
        check("entitlements_parseable", False, str(e))
        return

    check("entitlements_parseable", True)

    agent_files = {p.stem.upper() for p in agents_dir.glob("*.md")}
    # Entitlements may use lowercase agent names
    covered = {k.upper() for k in entitlements.keys()}
    uncovered = agent_files - covered

    check(
        "all_agents_have_entitlements",
        len(uncovered) == 0,
        f"No entitlement entry for: {sorted(uncovered)}" if uncovered else
        f"All {len(agent_files)} agents covered",
        warning=True
    )


# ── 4. Owner's Inbox Staleness ────────────────────────────────────────────────
def check_inbox_staleness():
    print("\n[4] Owner's Inbox staleness (>30 days without archival)")
    inbox_path = BASE / "Owner's Inbox"
    if not inbox_path.exists():
        check("inbox_exists", False)
        return

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30)
    stale = []

    for f in inbox_path.glob("*.md"):
        if f.name in ("owner.md", "DELIVERY_MANIFEST.md", "README.md"):
            continue
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            age_days = (now - mtime).days
            stale.append(f"{f.name} ({age_days}d old)")

    check(
        "inbox_no_stale_deliverables",
        len(stale) == 0,
        f"{len(stale)} files older than 30 days: {stale[:3]}{'...' if len(stale)>3 else ''}"
        if stale else f"{len(list(inbox_path.glob('*.md')))} files, none stale",
        warning=True
    )


# ── 5. Handoff / Status Freshness ─────────────────────────────────────────────
def check_handoff_freshness():
    print("\n[5] Team/handoff.md and status.md freshness")
    now = datetime.now(timezone.utc)
    cutoff_hours = 72  # warn if not updated in 3 days

    for fname in ("handoff.md", "status.md"):
        fpath = BASE / "Team" / fname
        if not fpath.exists():
            check(f"team_{fname}_exists", False, str(fpath))
            continue
        mtime = datetime.fromtimestamp(fpath.stat().st_mtime, tz=timezone.utc)
        age_hours = (now - mtime).total_seconds() / 3600
        check(
            f"team_{fname}_fresh",
            age_hours < cutoff_hours,
            f"Last updated {age_hours:.0f}h ago" + (" — may be stale" if age_hours >= cutoff_hours else ""),
            warning=(age_hours >= cutoff_hours)
        )


# ── 6. Governance Tools Available ─────────────────────────────────────────────
def check_governance_tools():
    print("\n[6] Governance tools (governance/tools/)")
    tools = [
        ("audit_logger.py", "Post-task output verifier"),
        ("policy_check.py", "Policy card compliance checker"),
        ("status_check.py", "Status claim verifier"),
    ]
    for fname, purpose in tools:
        fpath = BASE / "governance" / "tools" / fname
        if fpath.exists():
            size = fpath.stat().st_size
            check(f"tool_exists:{fname}", True, f"{purpose} ({size:,} bytes)")
        else:
            check(f"tool_exists:{fname}", False, f"Missing: {fpath.relative_to(BASE)}")

    # Policy cards dir (reference only — not enforced at runtime, but useful docs)
    cards_dir = BASE / "governance" / "policy_cards"
    if cards_dir.exists():
        card_count = len(list(cards_dir.glob("*.yaml")))
        check("policy_cards_present", card_count > 0,
              f"{card_count} policy cards (reference docs — not runtime-enforced)",
              warning=False)
    else:
        check("policy_cards_present", False, "governance/policy_cards/ missing", warning=True)


# ── 7. Task Audit Log Health ───────────────────────────────────────────────────
def check_audit_log():
    print("\n[7] Task audit log health (logs/task_audit.jsonl)")
    audit_path = BASE / "logs" / "task_audit.jsonl"

    if not audit_path.exists():
        check("audit_log_exists", False,
              "logs/task_audit.jsonl missing — run audit_logger.py after tasks to create it",
              warning=True)
        return

    check("audit_log_exists", True, str(audit_path.relative_to(BASE)))

    try:
        with open(audit_path, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception as e:
        check("audit_log_parseable", False, str(e))
        return

    check("audit_log_not_empty", len(lines) > 0, f"{len(lines)} entries", warning=len(lines) == 0)

    if lines:
        try:
            last = json.loads(lines[-1])
            ts = last.get("timestamp", "")[:19]
            verdict = last.get("verdict", "?")
            task = last.get("task", "?")[:50]
            all_present = last.get("summary", {}).get("all_present", None)
            check(
                "last_audit_entry_valid",
                True,
                f"Last: '{task}' @ {ts} — verdict={verdict}, all_outputs_present={all_present}"
            )
            if all_present is False:
                missing_count = last.get("summary", {}).get("missing", "?")
                check(
                    "last_audit_no_missing_outputs",
                    False,
                    f"Last task had {missing_count} missing output(s) — agent may have claimed work without delivering",
                    warning=True
                )
        except Exception as e:
            check("last_audit_entry_valid", False, f"Parse error: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────
def print_summary():
    total = len(results["checks"])
    passed = sum(1 for v in results["checks"].values() if v["passed"])
    failed = len(results["failures"])
    warned = len(results["warnings"])

    print("\n" + "=" * 60)
    print("PKA WORKSPACE HEALTH — RESULTS")
    print("=" * 60)
    print(f"  Total checks : {total}")
    print(f"  Passed       : {passed}")
    print(f"  Failed       : {failed}")
    print(f"  Warnings     : {warned}")
    print(f"  Overall      : {'PASS' if failed == 0 else 'FAIL'}")

    if results["failures"]:
        print("\nFAILURES (need fixing):")
        for f in results["failures"]:
            print(f"  - {f}")

    if results["warnings"]:
        print("\nWARNINGS (review recommended):")
        for w in results["warnings"]:
            print(f"  - {w}")

    # Write log
    log_dir = BASE / "logs"
    log_dir.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    log_path = log_dir / f"verify.gmags.doctor.{ts}.json"
    results["summary"] = {
        "total": total, "passed": passed,
        "failed": failed, "warnings": warned,
        "overall": "PASS" if failed == 0 else "FAIL"
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nLog: {log_path.relative_to(BASE)}")


def main():
    parser = argparse.ArgumentParser(description="PKA Workspace Health Check")
    parser.add_argument("--check",
                        choices=["all", "agents", "roster", "routing", "entitlements",
                                 "inbox", "handoff", "tools", "audit"],
                        default="all")
    args = parser.parse_args()

    print("PKA Workspace Doctor")
    print(f"Base: {BASE}")

    run_all = args.check == "all"
    if run_all or args.check in ("agents", "roster"):
        check_agent_roster_sync()
    if run_all or args.check in ("agents", "routing"):
        check_axiom_routing()
    if run_all or args.check == "entitlements":
        check_entitlements()
    if run_all or args.check == "inbox":
        check_inbox_staleness()
    if run_all or args.check == "handoff":
        check_handoff_freshness()
    if run_all or args.check == "tools":
        check_governance_tools()
    if run_all or args.check == "audit":
        check_audit_log()

    print_summary()
    sys.exit(0 if not results["failures"] else 1)


if __name__ == "__main__":
    main()
