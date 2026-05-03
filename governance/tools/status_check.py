#!/usr/bin/env python3
"""
status_check.py — Artifact Status Verifier
Checks whether a claimed task status is supported by actual evidence.

USAGE:
  python governance/tools/status_check.py \
    --claimed-status tested \
    --outputs "scripts/new_feature.py,tests/test_new_feature.py" \
    --test-log "logs/verify.*.json"

  python governance/tools/status_check.py \
    --claimed-status implemented \
    --outputs "Owner's Inbox/my-deliverable.md"

WHY THIS EXISTS:
  Agents say things like "done", "tested", "deployed". This script
  checks whether the evidence on disk actually supports that claim.
  It computes the highest status the evidence supports and tells you
  if the claimed status is too optimistic.

STATUS LADDER (in order):
  draft             → artifact path provided (doesn't need to exist yet)
  implemented       → all declared output files exist and are non-empty
  ready_for_verify  → outputs exist + at least one test/verifier is defined
  tested            → outputs exist + a passing test log exists
  validated         → tested + a SENTINEL GO verdict exists in task_audit.jsonl
  production_ready  → validated + explicit human GO recorded in audit log

OUTPUTS:
  - Prints: claimed status, actual status, pass/fail, what's missing to promote
  - Exits 0 if evidence supports the claimed status, 1 if it doesn't

PRACTICAL EXAMPLES:
  # Agent claims code is "tested" — verify:
  python governance/tools/status_check.py \\
    --claimed-status tested \\
    --outputs "src/feature.py" \\
    --test-log "logs/verify.feature.*.json"

  # Quick check that a deliverable file exists (claimed: implemented):
  python governance/tools/status_check.py \\
    --claimed-status implemented \\
    --outputs "Owner's Inbox/nova-research.md"

  # Check if anything is actually production_ready:
  python governance/tools/status_check.py \\
    --claimed-status production_ready \\
    --outputs "src/auth.py,tests/test_auth.py" \\
    --test-log "logs/verify.auth.json" \\
    --require-human-go
"""
import argparse
import glob as glob_module
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent.parent.parent
AUDIT_LOG = BASE / "logs" / "task_audit.jsonl"

STATUS_LADDER = [
    "draft",
    "implemented",
    "ready_for_verify",
    "tested",
    "validated",
    "production_ready",
]


def resolve_paths(patterns):
    resolved = []
    for pat in patterns:
        pat = pat.strip()
        matches = sorted(glob_module.glob(str(BASE / pat)))
        if matches:
            for m in matches:
                resolved.append(Path(m))
        else:
            resolved.append(BASE / pat)
    return resolved


def files_ok(paths):
    """All paths exist and are non-empty."""
    for p in paths:
        if not p.exists():
            return False, f"Missing: {p.relative_to(BASE) if BASE in p.parents else p}"
        if p.is_file() and p.stat().st_size == 0:
            return False, f"Empty: {p.relative_to(BASE) if BASE in p.parents else p}"
    return True, None


def find_test_logs(patterns):
    logs = []
    for pat in patterns:
        matches = sorted(glob_module.glob(str(BASE / pat.strip())))
        logs.extend([Path(m) for m in matches])
    return logs


def test_log_passes(log_paths):
    """Return True if any test log shows a passing result."""
    for lp in log_paths:
        try:
            with open(lp, encoding="utf-8") as f:
                data = json.load(f)
            # Various test log formats
            summary = data.get("summary", {})
            overall = summary.get("overall", data.get("overall", ""))
            if overall.upper() in ("PASS", "PASSING", "SUCCESS"):
                return True, str(lp.relative_to(BASE))
            # pka-style: check for zero failures
            if summary.get("failed", 1) == 0 and summary.get("passed", 0) > 0:
                return True, str(lp.relative_to(BASE))
        except Exception:
            continue
    return False, None


def get_sentinel_go_from_audit():
    """Check if any recent audit entry has a GO verdict from SENTINEL."""
    if not AUDIT_LOG.exists():
        return False, None
    with open(AUDIT_LOG, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    for line in reversed(lines[-10:]):  # Check last 10 entries
        try:
            entry = json.loads(line)
            if entry.get("verdict") == "GO" and "SENTINEL" in [
                a.upper() for a in entry.get("agents", [])
            ]:
                return True, entry.get("timestamp", "")[:19]
        except Exception:
            continue
    return False, None


def compute_actual_status(output_paths, test_log_paths, require_human_go):
    """Compute the highest status the evidence actually supports."""
    status = "draft"
    reason = None

    # implemented: all outputs exist and non-empty
    ok, msg = files_ok(output_paths)
    if not ok:
        return "draft", f"Cannot reach 'implemented': {msg}"
    status = "implemented"

    # ready_for_verify: outputs exist + test log paths are defined
    if test_log_paths is not None:
        status = "ready_for_verify"
        if not test_log_paths:
            return status, "Cannot reach 'tested': no test logs found matching pattern"

        # tested: a passing test log exists
        passed, log_used = test_log_passes(test_log_paths)
        if not passed:
            return status, f"Cannot reach 'tested': no passing test log found among {len(test_log_paths)} log(s)"
        status = "tested"

        # validated: SENTINEL GO in audit log
        go, ts = get_sentinel_go_from_audit()
        if not go:
            return status, "Cannot reach 'validated': no SENTINEL GO verdict in task_audit.jsonl"
        status = "validated"

        # production_ready: requires explicit human GO
        if require_human_go:
            # We can't auto-detect a human GO — this must be asserted by the caller
            return status, "Cannot reach 'production_ready': requires explicit human GO (pass --human-go-confirmed)"
    else:
        # No test log provided — cap at ready_for_verify
        status = "ready_for_verify"
        reason = "No --test-log provided. Pass a test log pattern to check for 'tested' or higher."

    return status, reason


def ladder_index(s):
    try:
        return STATUS_LADDER.index(s.lower().replace("-", "_"))
    except ValueError:
        return -1


def main():
    parser = argparse.ArgumentParser(
        description="Verify whether a claimed status is supported by evidence"
    )
    parser.add_argument("--claimed-status", required=True,
                        help="Status the agent claims (draft/implemented/tested/validated/production_ready)")
    parser.add_argument("--outputs", default="",
                        help="Comma-separated output files to verify exist")
    parser.add_argument("--test-log", default="",
                        help="Comma-separated glob patterns for test log files")
    parser.add_argument("--require-human-go", action="store_true",
                        help="Check for production_ready (always blocked without explicit GO)")
    parser.add_argument("--human-go-confirmed", action="store_true",
                        help="Assert that human GO was given (allows production_ready)")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    claimed = args.claimed_status.lower().replace("-", "_")

    print("\nSTATUS CHECK")
    print(f"Claimed status : {claimed}")
    print(f"Time           : {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    # Resolve outputs
    output_paths = resolve_paths([o for o in args.outputs.split(",") if o.strip()]) if args.outputs else []
    if not output_paths:
        print("  [FAIL] No --outputs provided. Cannot verify any status above 'draft'.")
        sys.exit(1)

    # Resolve test logs
    test_log_paths = None
    if args.test_log:
        test_log_paths = find_test_logs([t for t in args.test_log.split(",") if t.strip()])

    # Handle human GO
    require_human_go = args.require_human_go or (claimed == "production_ready")

    # Compute actual status
    actual, reason = compute_actual_status(output_paths, test_log_paths, require_human_go)

    # Handle human GO override
    if args.human_go_confirmed and actual == "validated":
        actual = "production_ready"
        reason = None

    # Print output details
    print(f"  Outputs checked ({len(output_paths)}):")
    for p in output_paths:
        rel = str(p.relative_to(BASE)) if BASE in p.parents or p.is_absolute() else str(p)
        exists = p.exists()
        size = f"{p.stat().st_size:,}b" if exists and p.is_file() else ("dir" if p.is_dir() else "MISSING")
        status_sym = "OK" if exists else "MISSING"
        print(f"    [{status_sym}] {rel} ({size})")

    if test_log_paths is not None:
        print(f"\n  Test logs found: {len(test_log_paths)}")
        for lp in test_log_paths[:3]:
            print(f"    {lp.relative_to(BASE)}")

    # Verdict
    print()
    claimed_idx = ladder_index(claimed)
    actual_idx = ladder_index(actual)
    supported = actual_idx >= claimed_idx

    print(f"  Claimed status : {claimed}")
    print(f"  Actual status  : {actual}")
    print()

    if supported:
        print(f"PASS — Evidence supports claimed status '{claimed}'")
        if reason:
            print(f"       Note: {reason}")
    else:
        print(f"FAIL — Evidence only supports '{actual}', not '{claimed}'")
        if reason:
            print(f"       Reason: {reason}")
        print(f"\n  To reach '{claimed}', you need:")
        for level in STATUS_LADDER[actual_idx + 1:claimed_idx + 1]:
            if level == "implemented":
                print("    - All declared output files must exist and be non-empty")
            elif level == "ready_for_verify":
                print("    - Pass --test-log with a path to a test log file")
            elif level == "tested":
                print("    - Test log must exist and show passing results (summary.overall=PASS)")
            elif level == "validated":
                print("    - A SENTINEL GO verdict must exist in logs/task_audit.jsonl")
            elif level == "production_ready":
                print("    - Explicit human GO (pass --human-go-confirmed)")

    sys.exit(0 if supported else 1)


if __name__ == "__main__":
    main()
