#!/usr/bin/env python
"""
PKA Production Telemetry  |  trend analysis and anomaly detection.

Reads all existing log sources and produces actionable intelligence.
Exit code is always 0  |  anomalies are warnings only.
Revisit exit-code policy in v0.8.0 when data volume supports real thresholds.
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs"
TASKS_DIR = ROOT / "Team" / "tasks"

TERMINAL_STATES = {"delivered", "archived"}
NON_TERMINAL_STATES = {"new", "classified", "assigned", "in_progress", "under_test", "under_audit"}

SECTION_BUDGET_S = 3.0   # max seconds per section before skip warning
MIN_VALIDATION_RUNS = 3  # minimum validation runs for trajectory
MIN_SESSION_DAYS = 2     # minimum session days for drift
MIN_TASKS_PER_AGENT = 5  # minimum completed tasks before velocity trend claims
RELIABILITY_WINDOW_H = 24  # hours to look back for reliability and anomaly metrics


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(s: str) -> datetime | None:
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


# ── Data loaders ──────────────────────────────────────────────────────────────

def load_validation_runs() -> list[dict]:
    path = LOGS_DIR / "pka_validation_history.jsonl"
    if not path.exists():
        return []
    runs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                runs.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return runs


def load_session_logs() -> list[dict]:
    entries = []
    for path in sorted(LOGS_DIR.glob("session_*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def load_guardrail_logs() -> list[dict]:
    entries = []
    for path in sorted(LOGS_DIR.glob("guardrail_*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def load_task_records() -> list[dict]:
    records = []
    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            parts = text.split("---\n", 2)
            if len(parts) < 3:
                continue
            block = parts[1]
            data: dict = {}
            for raw_line in block.splitlines():
                if ":" not in raw_line or raw_line.startswith("  -"):
                    continue
                key, value = raw_line.split(":", 1)
                data[key.strip()] = value.strip().strip('"')
            records.append(data)
        except Exception:
            pass
    return records


# ── Windowing helper ──────────────────────────────────────────────────────────

def recent_runs(runs: list[dict], hours: int = RELIABILITY_WINDOW_H) -> list[dict]:
    """Return only validation runs from the last ``hours`` hours."""
    cutoff = utc_now() - timedelta(hours=hours)
    result = []
    for r in runs:
        ts = parse_iso(r.get("timestamp", "") or "")
        if ts is not None and ts > cutoff:
            result.append(r)
    return result


def current_health_runs(runs: list[dict]) -> list[dict]:
    """Return the latest consecutive all-pass validation streak."""
    streak: list[dict] = []
    for run in reversed(runs):
        checks = run.get("checks", [])
        is_clean = bool(checks) and all(bool(check.get("ok")) for check in checks)
        if not is_clean:
            break
        streak.append(run)
    streak.reverse()
    return streak


# ── Section 1: Score Trajectory ───────────────────────────────────────────────

def section_score_trajectory(runs: list[dict]) -> list[str]:
    lines = ["## 1. Score Trajectory"]
    if len(runs) < MIN_VALIDATION_RUNS:
        lines.append(
            f"  Insufficient data ({len(runs)} records)  |  "
            f"need at least {MIN_VALIDATION_RUNS} for meaningful analysis"
        )
        return lines

    streak = current_health_runs(runs)
    recent = recent_runs(runs)
    window = streak or recent or runs
    scores = [(r.get("timestamp", ""), int(r.get("score", 0))) for r in window]
    anomalies = []
    for i in range(1, len(scores)):
        drop = scores[i - 1][1] - scores[i][1]
        if drop > 25:
            anomalies.append(
                f"  [ANOMALY] Score dropped {drop} points: "
                f"window run {i} ({scores[i-1][0]}) -> window run {i+1} ({scores[i][0]})"
            )

    current = scores[-1][1]
    prev = scores[-2][1] if len(scores) >= 2 else current
    trend = "(up)" if current > prev else ("(down)" if current < prev else "(stable)")
    min_s = min(s for _, s in scores)
    max_s = max(s for _, s in scores)
    lines.append(
        f"  Latest: {current}/100 {trend}  |  Current-health window: {len(window)} run(s)"
        f"  |  Min: {min_s}  |  Max: {max_s}"
    )
    lines.extend(anomalies) if anomalies else lines.append("  No current-health score regressions detected")
    if streak:
        lines.append(f"  Current healthy streak: {len(streak)} consecutive clean validation run(s)")
    if recent and len(recent) > len(window):
        lines.append(
            f"  Historical context: {len(recent) - len(window)} additional recent run(s) exist outside the healthy streak"
        )
    return lines


# ── Section 2: Check Reliability ─────────────────────────────────────────────

def section_check_reliability(runs: list[dict]) -> list[str]:
    streak = current_health_runs(runs)
    windowed = streak or recent_runs(runs)
    label = (
        f"current clean streak ({len(streak)} run(s))"
        if streak
        else f"last {RELIABILITY_WINDOW_H}h"
    )
    lines = [f"## 2. Check Reliability ({label})"]
    if len(windowed) < MIN_VALIDATION_RUNS:
        lines.append(
            f"  Insufficient recent data ({len(windowed)} records in last {RELIABILITY_WINDOW_H}h)  |  "
            f"need at least {MIN_VALIDATION_RUNS} for meaningful analysis"
        )
        return lines

    check_counts: dict[str, list[bool]] = defaultdict(list)
    for run in windowed:
        for check in run.get("checks", []):
            check_counts[check["name"]].append(bool(check.get("ok")))

    for name, results in sorted(check_counts.items()):
        pass_rate = sum(results) / len(results) * 100
        marker = "[FLAKY] " if pass_rate < 80 else "        "
        lines.append(f"  {marker}{name}: {pass_rate:.0f}% pass ({sum(results)}/{len(results)})")
    return lines


# ── Section 3: Agent Velocity ─────────────────────────────────────────────────

def section_agent_velocity(tasks: list[dict]) -> list[str]:
    lines = ["## 3. Agent Velocity"]
    if not tasks:
        lines.append("  Insufficient data (0 records)  |  need tasks for meaningful analysis")
        return lines

    by_agent: dict[str, list[dict]] = defaultdict(list)
    for t in tasks:
        by_agent[t.get("owner", "unknown")].append(t)

    for agent, agent_tasks in sorted(by_agent.items()):
        completed = [t for t in agent_tasks if t.get("state") in TERMINAL_STATES]
        total = len(agent_tasks)
        n_done = len(completed)
        if n_done < MIN_TASKS_PER_AGENT:
            lines.append(
                f"  {agent}: {n_done}/{total} completed "
                f"(low sample  |  trend needs {MIN_TASKS_PER_AGENT}+ completed)"
            )
        else:
            verdicts = [t.get("verdict") or "" for t in completed]
            go_rate = sum(1 for v in verdicts if "go" in v.lower()) / n_done * 100
            lines.append(
                f"  {agent}: {n_done}/{total} completed | GO rate: {go_rate:.0f}%"
            )
    return lines


# ── Section 4: Tool Mix ───────────────────────────────────────────────────────

def section_tool_mix(entries: list[dict]) -> list[str]:
    lines = ["## 4. Tool Mix"]
    if len(entries) < 10:
        lines.append(
            f"  Insufficient data ({len(entries)} records)  |  "
            "need at least 10 for meaningful analysis"
        )
        return lines

    by_day: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for e in entries:
        ts = e.get("ts", "")
        day = ts[:10] if ts else "unknown"
        tool = e.get("tool", "unknown")
        by_day[day][tool] += 1

    for day in sorted(by_day.keys()):
        counts = by_day[day]
        total = sum(counts.values())
        breakdown = " | ".join(
            f"{k}:{v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])[:5]
        )
        lines.append(f"  {day}: {total} calls  |  {breakdown}")
    return lines


# ── Section 5: Session Health ─────────────────────────────────────────────────

def section_session_health(entries: list[dict]) -> list[str]:
    lines = ["## 5. Session Health"]
    if len(entries) < 5:
        lines.append(
            f"  Insufficient data ({len(entries)} records)  |  "
            "need at least 5 for meaningful analysis"
        )
        return lines

    by_session: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_session[e.get("session_id", "unknown")].append(e)

    anomalies = []
    for sid, calls in by_session.items():
        if len(calls) > 100:
            anomalies.append(f"  [ANOMALY] Runaway session: {sid} ({len(calls)} calls)")

    lines.append(f"  Sessions tracked: {len(by_session)} | Total calls: {len(entries)}")
    lines.extend(anomalies) if anomalies else lines.append("  No runaway sessions detected")
    return lines


# ── Section 6: Guardrail Trends ───────────────────────────────────────────────

def section_guardrail_trends(entries: list[dict]) -> list[str]:
    lines = ["## 6. Guardrail Trends"]
    if not entries:
        lines.append("  No guardrail events recorded")
        return lines

    by_day: dict[str, int] = defaultdict(int)
    by_type: dict[str, int] = defaultdict(int)
    for e in entries:
        ts = e.get("ts", "")
        day = ts[:10] if ts else "unknown"
        by_day[day] += 1
        for v in e.get("violations", []):
            vtype = v[:50]
            by_type[vtype] += 1

    lines.append(f"  Total violations: {sum(by_day.values())} across {len(by_day)} day(s)")
    for day in sorted(by_day.keys()):
        lines.append(f"  {day}: {by_day[day]} violation(s)")
    return lines


# ── Section 7: Stale Task Alert ───────────────────────────────────────────────

def section_stale_tasks(tasks: list[dict]) -> list[str]:
    lines = ["## 7. Stale Task Alert"]
    now = utc_now()
    threshold = now - timedelta(hours=48)
    stale = []
    for t in tasks:
        if t.get("state", "") in TERMINAL_STATES:
            continue
        updated = parse_iso(t.get("updated_at", ""))
        if updated and updated < threshold:
            age_h = (now - updated).total_seconds() / 3600
            stale.append(
                (t.get("task_id", "?"), t.get("owner", "?"), t.get("state", "?"), age_h)
            )

    if stale:
        for task_id, owner, state, age_h in sorted(stale, key=lambda x: -x[3]):
            lines.append(
                f"  [STALE] {task_id} | owner={owner} | state={state} | {age_h:.0f}h since update"
            )
    else:
        lines.append("  No stale tasks detected")
    return lines


# ── Section 8: Anomaly Summary ────────────────────────────────────────────────

def section_anomaly_summary(
    runs: list[dict],
    entries: list[dict],
    tasks: list[dict],
    guardrail: list[dict],
) -> list[str]:
    lines = ["## 8. Anomaly Summary"]
    anomalies = []

    # Score drops — use only the latest health window so resolved regressions do
    # not remain active anomalies after the platform is stable again.
    windowed = current_health_runs(runs) or recent_runs(runs)
    if len(windowed) >= 2:
        scores = [int(r.get("score", 0)) for r in windowed]
        for i in range(1, len(scores)):
            drop = scores[i - 1] - scores[i]
            if drop > 25:
                anomalies.append(
                    f"  [HIGH] Score dropped {drop} points in consecutive current-health validation runs"
                )

    # Runaway sessions
    by_session: dict[str, int] = defaultdict(int)
    for e in entries:
        by_session[e.get("session_id", "?")] += 1
    for sid, count in by_session.items():
        if count > 100:
            anomalies.append(f"  [MEDIUM] Runaway session {sid} ({count} calls)")

    # Stale tasks
    now = utc_now()
    threshold = now - timedelta(hours=48)
    for t in tasks:
        if t.get("state", "") in TERMINAL_STATES:
            continue
        updated = parse_iso(t.get("updated_at", ""))
        if updated and updated < threshold:
            age_h = (now - updated).total_seconds() / 3600
            anomalies.append(
                f"  [LOW] Stale task {t.get('task_id','?')} "
                f"({age_h:.0f}h, state={t.get('state','?')}, owner={t.get('owner','?')})"
            )

    # High guardrail rate (>5 violations in any single day)
    by_day: dict[str, int] = defaultdict(int)
    for e in guardrail:
        day = e.get("ts", "")[:10]
        if day:
            by_day[day] += 1
    for day, count in by_day.items():
        if count > 5:
            anomalies.append(f"  [MEDIUM] High guardrail rate: {count} violations on {day}")

    lines.extend(anomalies) if anomalies else lines.append("  No anomalies detected")
    return lines


# ── Section 9: Historical Context ────────────────────────────────────────────

def section_historical_context(runs: list[dict]) -> list[str]:
    lines = ["## 9. Historical Context (all-time)"]
    recent = recent_runs(runs)
    lines.append(f"  Total runs: {len(runs)} | Recent (last {RELIABILITY_WINDOW_H}h): {len(recent)}")
    if len(runs) < MIN_VALIDATION_RUNS:
        return lines

    check_counts: dict[str, list[bool]] = defaultdict(list)
    for run in runs:
        for check in run.get("checks", []):
            check_counts[check["name"]].append(bool(check.get("ok")))

    for name, results in sorted(check_counts.items()):
        pass_rate = sum(results) / len(results) * 100
        lines.append(f"  {name}: {pass_rate:.0f}% all-time ({sum(results)}/{len(results)})")
    return lines


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    print("PKA Telemetry Report")
    print(f"- Generated: {utc_now().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print()

    t_load = time.time()
    runs = load_validation_runs()
    entries = load_session_logs()
    guardrail = load_guardrail_logs()
    tasks = load_task_records()
    load_elapsed = time.time() - t_load

    print(
        f"Data: {len(runs)} validation runs | {len(entries)} session calls | "
        f"{len(guardrail)} guardrail events | {len(tasks)} tasks"
        f"  (loaded in {load_elapsed:.2f}s)"
    )
    print()

    sections = [
        ("score_trajectory", lambda: section_score_trajectory(runs)),
        ("check_reliability", lambda: section_check_reliability(runs)),
        ("agent_velocity", lambda: section_agent_velocity(tasks)),
        ("tool_mix", lambda: section_tool_mix(entries)),
        ("session_health", lambda: section_session_health(entries)),
        ("guardrail_trends", lambda: section_guardrail_trends(guardrail)),
        ("stale_tasks", lambda: section_stale_tasks(tasks)),
        (
            "anomaly_summary",
            lambda: section_anomaly_summary(runs, entries, tasks, guardrail),
        ),
        ("historical_context", lambda: section_historical_context(runs)),
    ]

    for name, fn in sections:
        t0 = time.time()
        try:
            output_lines = fn()
        except Exception as exc:
            output_lines = [f"## {name}", f"  [ERROR] Section failed: {exc}"]
        elapsed = time.time() - t0
        if elapsed > SECTION_BUDGET_S:
            output_lines = output_lines[:1] + [
                f"  [TIMING] Skipped  |  took {elapsed:.1f}s, budget is {SECTION_BUDGET_S}s"
            ]
        for line in output_lines:
            print(line)
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
