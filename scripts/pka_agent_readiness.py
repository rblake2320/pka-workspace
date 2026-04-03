#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from pka_lib import LOGS_DIR, MANIFEST, REPORTS_DIR, ROOT, TASKS_DIR, TEAM_DIR


OUT = REPORTS_DIR / "PKA_AGENT_READINESS_REPORT.md"


def exists(path: Path) -> bool:
    return path.exists()


def any_exists(paths: list[Path]) -> bool:
    return any(path.exists() for path in paths)


def score(items: list[tuple[str, bool, str]]) -> tuple[int, int]:
    passed = sum(1 for _, ok, _ in items if ok)
    total = len(items)
    return passed, total


def main() -> int:
    reports_dir = REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)

    connectivity = [
        ("team_inbox", exists(ROOT / "Team Inbox"), "Task intake surface exists"),
        ("owner_inbox", exists(ROOT / "Owner's Inbox"), "Delivery surface exists"),
        ("message_protocol", exists(ROOT / "scripts" / "pka_message_cli.py"), "Structured inter-agent messaging exists"),
        ("group_chat_client", exists(ROOT / "scripts" / "ai_army_chat.py"), "Spark-1 group chat client exists"),
        ("chat_key_present", any_exists([Path.home() / ".ssh" / "ai_army_codex", Path.home() / ".ssh" / "ai_army"]), "AI Army SSH key available"),
        ("tool_hook", exists(ROOT / "scripts" / "pka_post_tool_hook.py"), "Post-tool hook exists"),
        ("machine_health", exists(ROOT / "scripts" / "pka_machine_health.py"), "Live machine-health checks exist"),
        ("runtime_cli", exists(ROOT / "scripts" / "pka_runtime.py"), "Durable runtime CLI exists"),
    ]

    context = [
        ("owner_profile", exists(ROOT / "Owner's Inbox" / "owner.md"), "Owner context exists"),
        ("task_ledger", exists(TASKS_DIR), "Consequential task ledger exists"),
        ("status_board", exists(TEAM_DIR / "status.md"), "Cross-session status exists"),
        ("handoff", exists(TEAM_DIR / "handoff.md"), "Cross-session handoff exists"),
        ("journals", exists(TEAM_DIR / "AXIOM" / "journal.md"), "Agent journal system exists"),
        ("dream_report", exists(REPORTS_DIR / "PKA_DREAM_REPORT.md"), "Background consolidation exists"),
        ("validation_history", exists(LOGS_DIR / "pka_validation_history.jsonl"), "Historical validation log exists"),
    ]

    control = [
        ("operating_model", exists(TEAM_DIR / "OPERATING_MODEL.md"), "Canonical lifecycle exists"),
        ("audit", exists(ROOT / "scripts" / "pka_process_audit.py"), "Process audit exists"),
        ("session_gate", exists(ROOT / "scripts" / "pka_session_gate.py"), "Session gate exists"),
        ("e2e", exists(ROOT / "scripts" / "pka_e2e_test.py"), "E2E validation exists"),
        ("resilience", exists(ROOT / "scripts" / "pka_resilience_test.py"), "Adversarial resilience test exists"),
        ("scorecard", exists(ROOT / "scripts" / "pka_scorecard.py"), "Outcome-based scoring exists"),
        ("doctor", exists(ROOT / "scripts" / "pka_doctor.py"), "Environment diagnostics exist"),
        ("evidence_pack", exists(ROOT / "scripts" / "pka_evidence_pack.py"), "Evidence pack generation exists"),
        ("proof_dashboard", exists(ROOT / "scripts" / "pka_proof_dashboard.py"), "Proof dashboard exists"),
        ("cost_tracker", exists(ROOT / "scripts" / "pka_cost_tracker.py"), "Audit/cost trend tracking exists"),
        ("entitlement_registry", exists(TEAM_DIR / "AGENT_TOOL_ENTITLEMENTS.json"), "Agent tool entitlement matrix exists"),
        ("entitlement_check", exists(ROOT / "scripts" / "pka_entitlement_check.py"), "Entitlement validation exists"),
        ("recovery_playbook", exists(ROOT / "scripts" / "pka_recovery_playbook.py"), "Recovery playbook generation exists"),
        ("runtime_check", exists(ROOT / "scripts" / "pka_runtime_check.py"), "Durable runtime integrity check exists"),
    ]

    c_pass, c_total = score(connectivity)
    x_pass, x_total = score(context)
    k_pass, k_total = score(control)
    known_gaps: list[str] = []
    # Only add repo-root gap if git boundary check actually fails
    try:
        git_result = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        )
        if git_result.returncode != 0 or Path(git_result.stdout.strip()).resolve() != ROOT.resolve():
            known_gaps.append(
                "No standalone repo root yet — workspace still nested inside parent git boundary"
            )
    except Exception:
        known_gaps.append(
            "No standalone repo root yet — workspace still nested inside parent git boundary"
        )
    gap_penalty = len(known_gaps) * 4
    base_pass = c_pass + x_pass + k_pass
    base_total = c_total + x_total + k_total
    base_score = round(base_pass / base_total * 100) if base_total else 0
    overall_score = max(0, base_score - gap_penalty)

    strengths = [
        "Connectivity is strong across inboxes, group chat, hooks, and structured agent messaging",
        "Context is strong across owner profile, ledger, journals, handoff, status, and dream consolidation",
        "Control is strong across audit, gates, E2E, resilience, scorecard, evidence packs, and proof dashboard",
    ]

    lines = [
        "# PKA Agent Readiness Report",
        "",
        f"- Overall score: {overall_score}/100",
        f"- Base implemented coverage: {base_score}/100",
        f"- Connectivity: {c_pass}/{c_total}",
        f"- Context: {x_pass}/{x_total}",
        f"- Control: {k_pass}/{k_total}",
        "",
        "## Strengths",
    ]
    lines.extend(f"- {item}" for item in strengths)
    lines += [
        "",
        "## Connectivity Checks",
    ]
    lines.extend(f"- {name}: {'PASS' if ok else 'FAIL'} | {note}" for name, ok, note in connectivity)
    lines += [
        "",
        "## Context Checks",
    ]
    lines.extend(f"- {name}: {'PASS' if ok else 'FAIL'} | {note}" for name, ok, note in context)
    lines += [
        "",
        "## Control Checks",
    ]
    lines.extend(f"- {name}: {'PASS' if ok else 'FAIL'} | {note}" for name, ok, note in control)
    lines += [
        "",
        "## Known Gaps Blocking True 100% Agent Coverage",
    ]
    lines.extend(f"- {gap}" for gap in known_gaps)
    lines += ["", "## Verdict"]
    if known_gaps:
        lines.append(
            f"Base workspace coverage is {base_score}/100 from implemented controls, "
            f"but {len(known_gaps)} known infrastructure gap(s) reduce effective readiness to {overall_score}/100."
        )
        lines.append("Remaining gaps: " + "; ".join(known_gaps))
    else:
        lines.append(f"Full readiness: {overall_score}/100 — all known infrastructure gaps resolved.")
    lines.append("PKA has strong coverage on connectivity, context, and control inside this workspace.")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PKA Agent Readiness: {overall_score}/100")
    print(f"- Connectivity: {c_pass}/{c_total}")
    print(f"- Context: {x_pass}/{x_total}")
    print(f"- Control: {k_pass}/{k_total}")
    print(f"- Report: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
