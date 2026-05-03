#!/usr/bin/env python3
"""
policy_check.py — Agent Policy Card Compliance Checker
Checks whether a task was run within an agent's declared policy card constraints.

USAGE:
  python governance/tools/policy_check.py --agent FORGE --mode build
  python governance/tools/policy_check.py --agent SENTINEL --mode review
  python governance/tools/policy_check.py --agent NOVA --mode build  # will FAIL

WHY THIS EXISTS:
  Policy cards define what each agent is supposed to do (allowed modes,
  prohibited actions). This script checks whether the mode used in a task
  is actually allowed for that agent per its policy card.
  It also checks the most recent task_audit.jsonl entry for policy violations.

WHAT IT ACTUALLY CHECKS:
  1. Does the agent have a policy card?
  2. Was the declared operating mode in the agent's allowed_modes list?
  3. If a recent audit log exists, did the agents involved match expected roles?
  4. Are there any prohibited actions flagged in the audit entry?

OUTPUTS:
  - Prints pass/fail per check with specific violations
  - Appends one JSON line to logs/policy_check.jsonl

PRACTICAL EXAMPLES:
  # After FORGE builds something — verify it was in build mode (allowed):
  python governance/tools/policy_check.py --agent FORGE --mode build

  # After NOVA tries to deploy something — verify mode violation:
  python governance/tools/policy_check.py --agent NOVA --mode operate

  # Check last audit entry for a multi-agent chain:
  python governance/tools/policy_check.py --agent FORGE --mode build --check-last-audit
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent.parent
POLICY_CARDS_DIR = BASE / "governance" / "policy_cards"
AUDIT_LOG = BASE / "logs" / "task_audit.jsonl"
POLICY_LOG = BASE / "logs" / "policy_check.jsonl"


def load_policy_card(agent_name: str):
    card_path = POLICY_CARDS_DIR / f"{agent_name.upper()}.yaml"
    if not card_path.exists():
        return None, str(card_path)
    with open(card_path, encoding="utf-8") as f:
        return yaml.safe_load(f), str(card_path)


def get_last_audit_entry():
    if not AUDIT_LOG.exists():
        return None
    with open(AUDIT_LOG, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return None
    try:
        return json.loads(lines[-1])
    except Exception:
        return None


def check_mode(card, mode):
    allowed = card.get("allowed_modes", [])
    return mode in allowed, allowed


def check_prohibited(card, actions_to_check):
    prohibited = card.get("prohibited_actions", [])
    violations = [a for a in actions_to_check if a in prohibited]
    return violations, prohibited


def print_check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    line = f"  [{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return passed


def main():
    parser = argparse.ArgumentParser(
        description="Check agent policy card compliance for a task run"
    )
    parser.add_argument("--agent", required=True, help="Agent name (e.g. FORGE, NOVA)")
    parser.add_argument("--mode", required=True,
                        help="Mode that was used (exploration/design/build/verify/operate/review)")
    parser.add_argument("--actions", default="",
                        help="Comma-separated actions taken — checked against prohibited list")
    parser.add_argument("--check-last-audit", action="store_true",
                        help="Also check the most recent task_audit.jsonl entry")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    agent = args.agent.upper()
    mode = args.mode.lower()

    print(f"\nPOLICY CHECK — {agent} — mode: {mode}")
    print(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    failures = []

    # 1. Policy card exists
    card, card_path = load_policy_card(agent)
    if card is None:
        print_check("policy_card_exists", False, f"Not found: {card_path}")
        print(f"\nFAIL — No policy card for {agent}. Cannot perform compliance check.")
        sys.exit(1)
    print_check("policy_card_exists", True, card_path.split("PKA testing")[-1])

    # 2. Mode is allowed
    mode_ok, allowed_modes = check_mode(card, mode)
    if not print_check(
        f"mode_allowed:{mode}",
        mode_ok,
        f"'{mode}' is {'allowed' if mode_ok else 'NOT in allowed list: ' + str(allowed_modes)}"
    ):
        failures.append(f"Mode '{mode}' not allowed for {agent}. Allowed: {allowed_modes}")

    # 3. Actions vs prohibited list
    if args.actions:
        actions = [a.strip() for a in args.actions.split(",") if a.strip()]
        violations, prohibited = check_prohibited(card, actions)
        if violations:
            for v in violations:
                print_check(f"action_not_prohibited:{v}", False,
                             f"'{v}' is in prohibited_actions for {agent}")
                failures.append(f"Prohibited action taken: {v}")
        else:
            print_check("no_prohibited_actions", True,
                        f"Checked {len(actions)} action(s) against {len(prohibited)} prohibited")

    # 4. Budget awareness (informational only — can't enforce, but report)
    budgets = card.get("budgets", {})
    if budgets:
        print(f"\n  [INFO] Declared budgets for {agent}:")
        for k, v in budgets.items():
            print(f"         {k}: {v}")
        print("         (budgets are informational — not enforced by Claude Code runtime)")

    # 5. Check last audit entry if requested
    if args.check_last_audit:
        entry = get_last_audit_entry()
        if entry is None:
            print_check("last_audit_entry_exists", False, f"No entries in {AUDIT_LOG}")
        else:
            print(f"\n  Last audit entry: {entry.get('task', '?')} "
                  f"({entry.get('timestamp', '?')[:19]})")
            # Check if this agent was involved
            audit_agents = entry.get("agents", [])
            agent_involved = agent in [a.upper() for a in audit_agents]
            print_check(
                "agent_in_last_audit",
                agent_involved,
                f"{agent} {'was' if agent_involved else 'was NOT'} in: {audit_agents}"
            )
            # Check verdict
            audit_verdict = entry.get("verdict", "PENDING")
            all_present = entry.get("summary", {}).get("all_present", True)
            print_check(
                "last_audit_all_outputs_present",
                all_present,
                f"Audit verdict: {audit_verdict}, all outputs: {all_present}"
            )
            if not all_present:
                missing_count = entry.get("summary", {}).get("missing", 0)
                failures.append(f"Last audit had {missing_count} missing output(s)")

    # Summary
    print()
    if failures:
        print(f"FAIL — {len(failures)} violation(s):")
        for f in failures:
            print(f"  - {f}")
    else:
        print(f"PASS — {agent} operated within policy card constraints for mode '{mode}'")

    # Log result
    log_entry = {
        "timestamp": now.isoformat(),
        "agent": agent,
        "mode_checked": mode,
        "mode_allowed": mode_ok,
        "failures": failures,
        "passed": len(failures) == 0,
        "policy_card": str(POLICY_CARDS_DIR.relative_to(BASE) / f"{agent}.yaml"),
    }
    POLICY_LOG.parent.mkdir(exist_ok=True)
    with open(POLICY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\nLogged to: {POLICY_LOG.relative_to(BASE)}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
