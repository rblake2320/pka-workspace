#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from pka_lib import REPORTS_DIR, ROOT

OUT = REPORTS_DIR / "PKA_MACHINE_HEALTH_REPORT.md"
SPARK_HOST = "192.168.12.132"
SPARK_USER = "rblake2320"


def resolve_spark_key() -> Path:
    for name in ("ai_army_codex", "ai_army"):
        candidate = Path.home() / ".ssh" / name
        if candidate.exists():
            return candidate
    return Path.home() / ".ssh" / "ai_army_codex"


def run_command(command: list[str], timeout: int = 15) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except Exception as exc:
        return False, str(exc)
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    spark_key = resolve_spark_key()
    checks: list[tuple[str, bool, str]] = []
    checks.append(("chat_script", (ROOT / "scripts" / "ai_army_chat.py").exists(), "AI Army chat client present"))
    checks.append(("spark_key_present", spark_key.exists(), f"Spark key path: {spark_key}"))

    ssh_ok = False
    ssh_note = "Spark key missing; live SSH skipped"
    if spark_key.exists():
        ssh_ok, ssh_output = run_command(
            [
                "ssh",
                "-i",
                str(spark_key),
                "-o",
                "BatchMode=yes",
                "-o",
                "StrictHostKeyChecking=no",
                "-o",
                "UserKnownHostsFile=NUL",
                "-o",
                "ConnectTimeout=8",
                f"{SPARK_USER}@{SPARK_HOST}",
                "echo spark-ok",
            ],
        )
        ssh_note = ssh_output or "Spark SSH reachable"
    checks.append(("spark_ssh", ssh_ok, ssh_note))

    aws_ok, aws_output = run_command(
        ["cmd", "/c", "aws sts get-caller-identity --output json"],
    )
    if aws_ok:
        try:
            identity = json.loads(aws_output)
            aws_note = identity.get("Arn", "AWS identity verified")
        except json.JSONDecodeError:
            aws_note = "AWS identity verified"
    else:
        aws_note = aws_output or "AWS identity unavailable"
    checks.append(("aws_identity", aws_ok, aws_note))

    warnings = [name for name, ok, _ in checks if not ok]
    lines = [
        "# PKA Machine Health Report",
        "",
        f"- Timestamp: {timestamp}",
        f"- Overall: {'healthy' if not warnings else 'warnings present'}",
        "",
        "## Checks",
    ]
    lines.extend(f"- {name}: {'PASS' if ok else 'WARN'} | {note}" for name, ok, note in checks)
    lines += [
        "",
        "## Notes",
        "- This is a live environment diagnostic, not a release verdict.",
        "- Spark SSH warnings usually indicate key ACL, host trust, or network reachability issues outside the workspace code.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("PKA Machine Health")
    for name, ok, note in checks:
        print(f"- {name}: {'PASS' if ok else 'WARN'} | {note}")
    print(f"- Report: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
