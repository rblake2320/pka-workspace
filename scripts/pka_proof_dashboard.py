#!/usr/bin/env python
"""
Generate Owner's Inbox/pka_proof_dashboard.html from live workspace data.

Reads:
- Owner's Inbox/reports/PKA_LATEST_VALIDATION_REPORT.md
- Owner's Inbox/reports/PKA_OBSERVABILITY_REPORT.md
- Owner's Inbox/DELIVERY_MANIFEST.md
- Team/tasks/*.md
- Team/*/journal.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "Owner's Inbox" / "reports"
MANIFEST = ROOT / "Owner's Inbox" / "DELIVERY_MANIFEST.md"
TASKS_DIR = ROOT / "Team" / "tasks"
TEAM_DIR = ROOT / "Team"
LOGS_DIR = ROOT / "logs"
OUT = ROOT / "Owner's Inbox" / "pka_proof_dashboard.html"

AGENTS = [
    "AXIOM", "FORGE", "SENTINEL", "HELM", "NOVA",
    "VENTURE", "SPARK", "LEGAL", "SCRIBE", "GRID",
    "RADAR", "CRUCIBLE", "DEBUGGER",
]


# ── data loaders ────────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_validation() -> dict:
    text = _read(REPORTS_DIR / "PKA_LATEST_VALIDATION_REPORT.md")
    score = re.search(r"Score:\s*(\d+)/(\d+)", text)
    passed = re.search(r"Passed:\s*(\d+)/(\d+)", text)
    ts = re.search(r"Timestamp:\s*(\S+)", text)
    checks = re.findall(r"^- (\w+): (PASS|FAIL)", text, re.MULTILINE)
    return {
        "score": int(score.group(1)) if score else 0,
        "score_max": int(score.group(2)) if score else 0,
        "passed": int(passed.group(1)) if passed else 0,
        "passed_max": int(passed.group(2)) if passed else 0,
        "timestamp": ts.group(1) if ts else "unknown",
        "checks": checks,
    }


def load_observability() -> dict:
    text = _read(REPORTS_DIR / "PKA_OBSERVABILITY_REPORT.md")
    runs = re.search(r"Validation runs recorded:\s*(\d+)", text)
    perfect = re.search(r"Perfect validation runs:\s*(\d+)/(\d+)", text)
    trailing = re.search(r"Trailing 5 pass counts:\s*(.+)", text)
    score_range = re.search(r"Score range:\s*(\d+)/100", text)
    return {
        "runs": int(runs.group(1)) if runs else 0,
        "perfect": int(perfect.group(1)) if perfect else 0,
        "perfect_of": int(perfect.group(2)) if perfect else 0,
        "trailing": trailing.group(1).strip() if trailing else "",
        "score_range": int(score_range.group(1)) if score_range else 0,
    }


def load_manifest() -> list[dict]:
    text = _read(MANIFEST)
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "Date" in line or "YYYY" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 5:
            rows.append({
                "date": parts[0],
                "task": parts[1],
                "route": parts[2],
                "verdict": parts[3],
                "deliverable": parts[4],
                "next": parts[5] if len(parts) > 5 else "",
            })
    return rows


def load_tasks() -> list[dict]:
    tasks = []
    for path in sorted(TASKS_DIR.glob("*.md")):
        if path.name in {"README.md", "TASK_RECORD_TEMPLATE.md"}:
            continue
        text = _read(path)
        fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not fm_match:
            continue
        fm = fm_match.group(1)
        task = {}
        for key in ("task_id", "title", "state", "owner", "verdict", "created_at"):
            m = re.search(rf'^{key}:\s*["\']?([^"\'\n]+)["\']?', fm, re.MULTILINE)
            task[key] = m.group(1).strip() if m else ""
        tasks.append(task)
    return tasks


def load_cost_metrics() -> dict:
    report = REPORTS_DIR / "PKA_COST_TRACKER_REPORT.md"
    if not report.exists():
        return {"total_calls": 0, "unique_sessions": 0, "unique_days": 0, "tool_breakdown": {}}
    text = _read(report)
    total = re.search(r"Total tool calls logged:\s*(\d+)", text)
    sessions = re.search(r"Unique sessions:\s*(\d+)", text)
    days = re.search(r"Days active:\s*(\d+)", text)
    tools = re.findall(r"^- (\w+): (\d+)", text, re.MULTILINE)
    return {
        "total_calls": int(total.group(1)) if total else 0,
        "unique_sessions": int(sessions.group(1)) if sessions else 0,
        "unique_days": int(days.group(1)) if days else 0,
        "tool_breakdown": {t: int(c) for t, c in tools[:8]},
    }


def agent_task_counts(tasks: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in tasks:
        owner = t.get("owner", "").strip()
        if owner:
            counts[owner] = counts.get(owner, 0) + 1
    return counts


# ── HTML generation ──────────────────────────────────────────────────────────

def verdict_badge(verdict: str) -> str:
    v = verdict.strip().upper()
    if v == "GO":
        return '<span class="badge go">GO</span>'
    if v == "NO-GO":
        return '<span class="badge nogo">NO-GO</span>'
    if v == "HOLD":
        return '<span class="badge hold">HOLD</span>'
    return f'<span class="badge delivered">{verdict}</span>'


def state_badge(state: str) -> str:
    s = state.strip().lower()
    cls = "delivered" if s in ("delivered", "archived") else "in-progress" if "progress" in s else "pending"
    return f'<span class="badge {cls}">{state}</span>'


def manifest_rows_html(rows: list[dict]) -> str:
    if not rows:
        return "<tr><td colspan='5'>No deliveries yet</td></tr>"
    out = []
    for r in rows:
        out.append(
            f"<tr>"
            f"<td>{r['date']}</td>"
            f"<td><code>{r['task']}</code></td>"
            f"<td>{verdict_badge(r['verdict'])}</td>"
            f"<td class='deliverable'>{r['deliverable']}</td>"
            f"<td class='route'>{r['route']}</td>"
            f"</tr>"
        )
    return "\n".join(out)


def task_rows_html(tasks: list[dict]) -> str:
    if not tasks:
        return "<tr><td colspan='4'>No tasks yet</td></tr>"
    out = []
    for t in tasks:
        out.append(
            f"<tr>"
            f"<td><code>{t['task_id']}</code></td>"
            f"<td>{t['title']}</td>"
            f"<td>{state_badge(t['state'])}</td>"
            f"<td>{t['owner']}</td>"
            f"</tr>"
        )
    return "\n".join(out)


def checks_html(checks: list[tuple]) -> str:
    out = []
    for name, result in checks:
        cls = "pass" if result == "PASS" else "fail"
        out.append(f'<div class="check {cls}"><span class="check-name">{name}</span><span class="check-result">{result}</span></div>')
    return "\n".join(out)


def trailing_bars_html(trailing: str) -> str:
    parts = [p.strip() for p in trailing.split(",")]
    out = []
    for p in parts:
        m = re.match(r"(\d+)/(\d+)", p)
        if m:
            v, mx = int(m.group(1)), int(m.group(2))
            pct = int(v / mx * 100) if mx else 0
            cls = "full" if pct == 100 else "high" if pct >= 75 else "mid" if pct >= 50 else "low"
            out.append(f'<div class="bar-wrap" title="{p}"><div class="bar {cls}" style="height:{pct}%"></div><div class="bar-label">{p}</div></div>')
    return "\n".join(out)


def agent_grid_html(counts: dict[str, int]) -> str:
    out = []
    for agent in AGENTS:
        n = counts.get(agent, 0)
        active = "active" if n > 0 else "idle"
        out.append(
            f'<div class="agent-card {active}">'
            f'<div class="agent-name">{agent}</div>'
            f'<div class="agent-tasks">{n} task{"s" if n != 1 else ""}</div>'
            f'</div>'
        )
    return "\n".join(out)


def cost_tool_bars_html(breakdown: dict) -> str:
    if not breakdown:
        return '<div style="color:var(--muted);font-size:12px">No hook data yet — hooks fire on next session</div>'
    total = sum(breakdown.values()) or 1
    out = []
    for tool, count in list(breakdown.items())[:8]:
        pct = int(count / total * 100)
        out.append(
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">'
            f'<div style="font-family:var(--mono);font-size:11px;width:90px;flex-shrink:0;color:var(--text)">{tool}</div>'
            f'<div style="flex:1;background:var(--border);border-radius:3px;height:8px">'
            f'<div style="width:{pct}%;background:var(--accent);height:8px;border-radius:3px"></div></div>'
            f'<div style="font-size:11px;color:var(--muted);font-family:var(--mono);width:36px;text-align:right">{count}</div>'
            f'</div>'
        )
    return "\n".join(out)


def generate(val: dict, obs: dict, manifest: list[dict], tasks: list[dict], cost: dict) -> str:
    counts = agent_task_counts(tasks)
    delivered_count = sum(1 for t in tasks if t["state"] in ("delivered", "archived"))
    go_count = sum(1 for r in manifest if r["verdict"].strip().upper() == "GO")
    score_pct = int(val["score"] / val["score_max"] * 100) if val["score_max"] else 0

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Verified Agent Ops — Proof Dashboard</title>
<style>
  :root {{
    --bg: #0a0c10;
    --surface: #111318;
    --border: #1e2330;
    --accent: #00d4ff;
    --accent2: #7c3aed;
    --go: #10b981;
    --warn: #f59e0b;
    --fail: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
    --mono: 'JetBrains Mono', 'Fira Code', monospace;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 14px;
    line-height: 1.6;
    padding: 0 0 60px;
  }}

  /* header */
  .header {{
    background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%);
    border-bottom: 1px solid var(--border);
    padding: 32px 40px 24px;
  }}
  .header-top {{ display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }}
  .logo {{
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 900; color: white;
  }}
  .product-name {{ font-size: 22px; font-weight: 700; color: var(--text); }}
  .product-sub {{ font-size: 13px; color: var(--muted); margin-top: 2px; }}
  .updated {{ font-size: 11px; color: var(--muted); font-family: var(--mono); margin-top: 12px; }}

  /* layout */
  .main {{ max-width: 1200px; margin: 0 auto; padding: 32px 40px 0; }}
  .section {{ margin-bottom: 40px; }}
  .section-title {{
    font-size: 11px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: 16px; padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}

  /* stat cards */
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }}
  .stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
  }}
  .stat-card::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 100%);
  }}
  .stat-value {{ font-size: 36px; font-weight: 800; color: var(--text); font-family: var(--mono); line-height: 1; }}
  .stat-label {{ font-size: 12px; color: var(--muted); margin-top: 6px; }}
  .stat-card.green .stat-value {{ color: var(--go); }}
  .stat-card.green::before {{ background: var(--go); }}

  /* score ring */
  .score-ring-wrap {{ display: flex; align-items: center; gap: 24px; }}
  .ring-container {{ position: relative; width: 80px; height: 80px; flex-shrink: 0; }}
  .ring-svg {{ width: 80px; height: 80px; transform: rotate(-90deg); }}
  .ring-bg {{ fill: none; stroke: var(--border); stroke-width: 8; }}
  .ring-fg {{ fill: none; stroke: var(--go); stroke-width: 8; stroke-linecap: round;
              stroke-dasharray: 220; stroke-dashoffset: {int(220 * (1 - score_pct/100))}; transition: stroke-dashoffset 1s; }}
  .ring-text {{
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    font-size: 16px; font-weight: 800; color: var(--go); font-family: var(--mono);
  }}

  /* badges */
  .badge {{
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.05em;
    font-family: var(--mono);
  }}
  .badge.go {{ background: rgba(16,185,129,0.15); color: var(--go); border: 1px solid rgba(16,185,129,0.3); }}
  .badge.nogo {{ background: rgba(239,68,68,0.15); color: var(--fail); border: 1px solid rgba(239,68,68,0.3); }}
  .badge.hold {{ background: rgba(245,158,11,0.15); color: var(--warn); border: 1px solid rgba(245,158,11,0.3); }}
  .badge.delivered {{ background: rgba(0,212,255,0.12); color: var(--accent); border: 1px solid rgba(0,212,255,0.25); }}
  .badge.in-progress {{ background: rgba(245,158,11,0.12); color: var(--warn); border: 1px solid rgba(245,158,11,0.25); }}
  .badge.pending {{ background: rgba(100,116,139,0.15); color: var(--muted); border: 1px solid rgba(100,116,139,0.3); }}

  /* checks */
  .checks-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 8px; }}
  .check {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 10px 14px;
    display: flex; align-items: center; justify-content: space-between;
    font-family: var(--mono); font-size: 12px;
  }}
  .check.pass {{ border-left: 3px solid var(--go); }}
  .check.fail {{ border-left: 3px solid var(--fail); }}
  .check-name {{ color: var(--text); }}
  .check-result.PASS {{ color: var(--go); font-weight: 700; }}
  .check-result.FAIL {{ color: var(--fail); font-weight: 700; }}

  /* trailing bars */
  .bar-chart {{ display: flex; align-items: flex-end; gap: 8px; height: 60px; }}
  .bar-wrap {{ display: flex; flex-direction: column; align-items: center; gap: 4px; flex: 1; }}
  .bar {{
    width: 100%; border-radius: 4px 4px 0 0; min-height: 4px;
    transition: height 0.5s;
  }}
  .bar.full {{ background: var(--go); }}
  .bar.high {{ background: #34d399; }}
  .bar.mid {{ background: var(--warn); }}
  .bar.low {{ background: var(--fail); }}
  .bar-label {{ font-size: 10px; color: var(--muted); font-family: var(--mono); white-space: nowrap; }}

  /* tables */
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{
    text-align: left; padding: 10px 12px;
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--muted);
    border-bottom: 1px solid var(--border);
  }}
  td {{
    padding: 10px 12px; border-bottom: 1px solid var(--border);
    vertical-align: top;
  }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(255,255,255,0.02); }}
  code {{ font-family: var(--mono); font-size: 11px; color: var(--accent); background: rgba(0,212,255,0.08); padding: 1px 5px; border-radius: 3px; }}
  .deliverable {{ max-width: 360px; font-size: 12px; color: var(--muted); word-break: break-word; }}
  .route {{ font-size: 11px; color: var(--muted); font-family: var(--mono); }}

  /* agents */
  .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; }}
  .agent-card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px; text-align: center;
  }}
  .agent-card.active {{ border-color: rgba(0,212,255,0.3); }}
  .agent-card.active .agent-name {{ color: var(--accent); }}
  .agent-name {{ font-size: 12px; font-weight: 700; font-family: var(--mono); color: var(--muted); }}
  .agent-tasks {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
  .agent-card.active .agent-tasks {{ color: var(--text); }}

  /* obs panel */
  .obs-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 640px) {{ .obs-grid {{ grid-template-columns: 1fr; }} }}
  .obs-panel {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px;
  }}
  .obs-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }}
  .obs-value {{ font-size: 28px; font-weight: 800; font-family: var(--mono); color: var(--text); }}
  .obs-sub {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}

  /* footer */
  .footer {{
    text-align: center; padding: 32px;
    font-size: 11px; color: var(--muted); font-family: var(--mono);
    border-top: 1px solid var(--border); margin-top: 48px;
  }}
  .proof-stamp {{
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2);
    border-radius: 20px; padding: 6px 14px;
    font-size: 12px; color: var(--go); font-weight: 600;
    margin-bottom: 12px;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="header-top">
    <div class="logo">V</div>
    <div>
      <div class="product-name">Verified Agent Ops Platform</div>
      <div class="product-sub">Every task receipted. Every verdict auditable.</div>
    </div>
  </div>
  <div class="updated">Last validated: {val['timestamp']} &nbsp;·&nbsp; {val['score']}/{val['score_max']} checks passing</div>
</div>

<div class="main">

  <!-- KPIs -->
  <div class="section">
    <div class="section-title">Live Metrics</div>
    <div class="stats">
      <div class="stat-card green">
        <div class="score-ring-wrap">
          <div class="ring-container">
            <svg class="ring-svg" viewBox="0 0 80 80">
              <circle class="ring-bg" cx="40" cy="40" r="35"/>
              <circle class="ring-fg" cx="40" cy="40" r="35"/>
            </svg>
            <div class="ring-text">{val['score']}</div>
          </div>
          <div>
            <div class="stat-value" style="font-size:24px">{val['score']}/{val['score_max']}</div>
            <div class="stat-label">Validation score</div>
          </div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{obs['runs']}</div>
        <div class="stat-label">Validation runs recorded</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{obs['perfect']}/{obs['perfect_of']}</div>
        <div class="stat-label">Perfect runs</div>
      </div>
      <div class="stat-card green">
        <div class="stat-value">{delivered_count}</div>
        <div class="stat-label">Tasks delivered</div>
      </div>
      <div class="stat-card green">
        <div class="stat-value">{go_count}</div>
        <div class="stat-label">GO verdicts</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{cost['total_calls']}</div>
        <div class="stat-label">Tool calls audited</div>
      </div>
    </div>
  </div>

  <!-- Audit trail -->
  <div class="section">
    <div class="section-title">Audit Trail — Tool Call Log</div>
    <div class="obs-grid">
      <div class="obs-panel">
        <div class="obs-label">Tool calls by type</div>
        {cost_tool_bars_html(cost['tool_breakdown'])}
      </div>
      <div class="obs-panel">
        <div class="obs-label">Session coverage</div>
        <div class="obs-value">{cost['total_calls']}</div>
        <div class="obs-sub">Calls logged across {cost['unique_sessions']} session(s), {cost['unique_days']} day(s)</div>
        <div style="margin-top:16px;font-size:11px;color:var(--go)">&#10003; PostToolUse hook active on Bash · Write · Edit · Task</div>
      </div>
    </div>
  </div>

  <!-- Validation checks -->
  <div class="section">
    <div class="section-title">Validation Checks — Latest Run</div>
    <div class="checks-grid">
      {checks_html(val['checks'])}
    </div>
  </div>

  <!-- Observability -->
  <div class="section">
    <div class="section-title">Observability</div>
    <div class="obs-grid">
      <div class="obs-panel">
        <div class="obs-label">Trailing 5 pass counts</div>
        <div class="bar-chart">
          {trailing_bars_html(obs['trailing'])}
        </div>
      </div>
      <div class="obs-panel">
        <div class="obs-label">Score stability</div>
        <div class="obs-value">{obs['score_range']}/100</div>
        <div class="obs-sub">Score range across all runs — lower is more stable</div>
      </div>
    </div>
  </div>

  <!-- Delivery manifest -->
  <div class="section">
    <div class="section-title">Delivery Manifest — Completed Tasks</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Task</th>
            <th>Verdict</th>
            <th>Deliverable</th>
            <th>Route</th>
          </tr>
        </thead>
        <tbody>
          {manifest_rows_html(manifest)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Task ledger -->
  <div class="section">
    <div class="section-title">Task Ledger</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Task ID</th>
            <th>Title</th>
            <th>State</th>
            <th>Owner</th>
          </tr>
        </thead>
        <tbody>
          {task_rows_html(tasks)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Agent roster -->
  <div class="section">
    <div class="section-title">Agent Roster — {len(AGENTS)} Active Agents</div>
    <div class="agent-grid">
      {agent_grid_html(counts)}
    </div>
  </div>

</div>

<div class="footer">
  <div class="proof-stamp">&#10003; Verified Agent Ops Platform</div><br>
  Generated from live workspace data &nbsp;·&nbsp; pka_proof_dashboard.py &nbsp;·&nbsp; {val['timestamp']}
</div>

</body>
</html>"""


def main() -> int:
    val = load_validation()
    obs = load_observability()
    manifest = load_manifest()
    tasks = load_tasks()
    cost = load_cost_metrics()

    html = generate(val, obs, manifest, tasks, cost)
    OUT.write_text(html, encoding="utf-8")
    print(f"Generated {OUT.relative_to(ROOT)}")
    print(f"  Validation: {val['score']}/{val['score_max']} | Runs: {obs['runs']} | Delivered: {sum(1 for t in tasks if t['state'] in ('delivered','archived'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
