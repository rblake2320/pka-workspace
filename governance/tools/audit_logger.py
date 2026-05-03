#!/usr/bin/env python3
"""
audit_logger.py — Post-Task Audit Logger
Verifies claimed output files actually exist, records evidence, appends to audit log.

USAGE (call this after any agent chain completes):
  python governance/tools/audit_logger.py \
    --task "Build X" \
    --agents "FORGE,CRUCIBLE,SENTINEL" \
    --outputs "path/to/file1.py,path/to/file2.md" \
    --verdict "GO" \
    --note "Optional context"

WHY THIS EXISTS:
  Agents claim to build things. Sometimes the file doesn't exist.
  Sometimes it exists but is empty. Sometimes it's a stub.
  This script checks the actual filesystem — not the agent's claim — and
  records what was really there at the time of delivery.

OUTPUTS:
  - Prints a table: each output file, whether it exists, its size
  - Appends one JSON line to logs/task_audit.jsonl
  - Exits 0 if all outputs exist, exits 1 if any are missing

PRACTICAL EXAMPLES:
  # After FORGE builds a script:
  python governance/tools/audit_logger.py \
    --task "Add user auth to API" --agents "FORGE,CRUCIBLE" \
    --outputs "src/auth.py,tests/test_auth.py" --verdict "GO"

  # After NOVA delivers research:
  python governance/tools/audit_logger.py \
    --task "Market research: AI agent governance" --agents "NOVA" \
    --outputs "Owner's Inbox/nova-governance-research.md" --verdict "GO"

  # Check without logging (dry run):
  python governance/tools/audit_logger.py \
    --outputs "some/file.py,another/file.md" --dry-run
"""
import argparse
import glob as glob_module
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent.parent.parent  # PKA testing root
LOG_FILE = BASE / "logs" / "task_audit.jsonl"


def resolve_outputs(output_args):
    """Expand glob patterns and resolve paths relative to BASE."""
    resolved = []
    for pattern in output_args:
        pattern = pattern.strip()
        # Try as glob relative to BASE
        matches = sorted(glob_module.glob(str(BASE / pattern)))
        if matches:
            for m in matches:
                resolved.append(Path(m))
        else:
            # Treat as literal path
            p = BASE / pattern if not Path(pattern).is_absolute() else Path(pattern)
            resolved.append(p)
    return resolved


def check_file(path: Path):
    """Return dict with existence, size, mtime for a file path."""
    if path.exists() and path.is_file():
        stat = path.stat()
        return {
            "exists": True,
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "empty": stat.st_size == 0,
        }
    elif path.exists() and path.is_dir():
        files = list(path.rglob("*"))
        return {
            "exists": True,
            "is_dir": True,
            "file_count": len([f for f in files if f.is_file()]),
        }
    else:
        return {"exists": False}


def print_table(output_checks):
    """Print a clean summary table."""
    col_w = max(len(str(p)) for p, _ in output_checks) + 2
    print(f"\n{'Output':<{col_w}} {'Status':<12} {'Size':>10}  {'Modified'}")
    print("-" * (col_w + 40))
    for path, info in output_checks:
        try:
            rel = str(path.relative_to(BASE))
        except ValueError:
            rel = str(path)
        if info["exists"]:
            if info.get("is_dir"):
                status = "EXISTS (dir)"
                size = f"{info.get('file_count', 0)} files"
                mtime = ""
            elif info.get("empty"):
                status = "EMPTY FILE"
                size = "0 bytes"
                mtime = info.get("modified", "")[:19]
            else:
                status = "OK"
                sz = info["size_bytes"]
                size = f"{sz:,} bytes" if sz < 1024 else f"{sz/1024:.1f} KB"
                mtime = info.get("modified", "")[:19]
        else:
            status = "MISSING"
            size = ""
            mtime = ""
        print(f"{rel:<{col_w}} {status:<12} {size:>10}  {mtime}")


def main():
    parser = argparse.ArgumentParser(
        description="Post-task audit logger — verify outputs exist, record evidence"
    )
    parser.add_argument("--task", default="(unnamed task)", help="Task description")
    parser.add_argument("--agents", default="", help="Comma-separated agent names that ran")
    parser.add_argument("--outputs", required=True,
                        help="Comma-separated output file paths or glob patterns to verify")
    parser.add_argument("--verdict", choices=["GO", "HOLD", "NO-GO", "PENDING"],
                        default="PENDING", help="Task verdict")
    parser.add_argument("--note", default="", help="Optional context note")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check files and print results without writing to log")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    output_paths = resolve_outputs([o for o in args.outputs.split(",") if o.strip()])

    if not output_paths:
        print("ERROR: No output paths provided or resolved.", file=sys.stderr)
        sys.exit(1)

    # Check each output
    output_checks = [(p, check_file(p)) for p in output_paths]
    missing = [p for p, info in output_checks if not info["exists"]]
    empty = [p for p, info in output_checks if info.get("exists") and info.get("empty")]

    # Print header
    print(f"\nAUDIT LOG — {args.task}")
    print(f"Agents : {args.agents or '(not specified)'}")
    print(f"Verdict: {args.verdict}")
    print(f"Time   : {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # Print table
    print_table(output_checks)

    # Summary
    total = len(output_checks)
    ok = total - len(missing)
    print(f"\nSummary: {ok}/{total} outputs verified")
    if missing:
        print(f"MISSING ({len(missing)}):")
        for p in missing:
            rel = str(p.relative_to(BASE)) if BASE in p.parents or p.is_absolute() else str(p)
            print(f"  - {rel}")
    if empty:
        print(f"WARNING — empty files ({len(empty)}):")
        for p in empty:
            rel = str(p.relative_to(BASE)) if BASE in p.parents or p.is_absolute() else str(p)
            print(f"  - {rel}")

    if args.dry_run:
        print("\n(dry-run — not written to log)")
        sys.exit(1 if missing else 0)

    # Build log entry
    entry = {
        "timestamp": now.isoformat(),
        "task": args.task,
        "agents": [a.strip() for a in args.agents.split(",") if a.strip()],
        "verdict": args.verdict,
        "note": args.note,
        "outputs": {
            str(p.relative_to(BASE) if BASE in p.parents else p): info
            for p, info in output_checks
        },
        "summary": {
            "total": total,
            "verified": ok,
            "missing": len(missing),
            "empty": len(empty),
            "all_present": len(missing) == 0,
        }
    }

    # Append to log
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"\nLogged to: {LOG_FILE.relative_to(BASE)}")

    if missing:
        print(f"\nFAIL — {len(missing)} declared output(s) missing. Agent claimed work that doesn't exist.")
        sys.exit(1)
    else:
        print("PASS — all declared outputs verified on disk.")
        sys.exit(0)


if __name__ == "__main__":
    main()
