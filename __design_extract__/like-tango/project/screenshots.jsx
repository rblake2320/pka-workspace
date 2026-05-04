// screenshots.jsx — SVG-based fake application screenshots
// Each is a 960x600 viewBox; the editor canvas scales them to fit.
// Style: flat IBM/government Win32-ish, monospace where appropriate.

const SCR_W = 960;
const SCR_H = 600;

// Common chrome bits
function WinTitle({ title, app }) {
  return (
    <g>
      <rect x="0" y="0" width={SCR_W} height="28" fill="var(--scr-titlebar)" />
      <text x="12" y="19" fill="var(--scr-titlebar-fg)" style={{ font: "12px ui-sans-serif, system-ui, sans-serif" }}>
        {app ? `${app} — ` : ""}{title}
      </text>
      <g transform={`translate(${SCR_W - 96}, 4)`}>
        <rect x="0" y="0" width="28" height="20" fill="transparent" />
        <text x="14" y="15" textAnchor="middle" fill="var(--scr-titlebar-fg)" fontSize="13">_</text>
        <rect x="32" y="0" width="28" height="20" fill="transparent" />
        <rect x="38" y="4" width="16" height="12" fill="none" stroke="var(--scr-titlebar-fg)" strokeWidth="1" />
        <rect x="64" y="0" width="28" height="20" fill="#c83838" />
        <text x="78" y="15" textAnchor="middle" fill="#fff" fontSize="13">×</text>
      </g>
    </g>
  );
}

function MenuBar({ items }) {
  return (
    <g>
      <rect x="0" y="28" width={SCR_W} height="22" fill="var(--scr-menubar)" />
      {items.map((it, i) => (
        <text key={i} x={14 + i * 60} y="44" fill="var(--scr-menubar-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>{it}</text>
      ))}
    </g>
  );
}

// ── Screenshot variants ─────────────────────────────────────────────────────

function ScrDesktop() {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="#1a4480" />
      {/* desktop icons */}
      {[
        { x: 60, y: 60, label: "Recycle Bin" },
        { x: 60, y: 160, label: "This PC" },
        { x: 60, y: 260, label: "IMDS Production", highlight: true },
        { x: 60, y: 360, label: "G081 BlueZone" },
        { x: 60, y: 460, label: "ARIS" },
      ].map((ic, i) => (
        <g key={i} transform={`translate(${ic.x}, ${ic.y})`}>
          <rect x="0" y="0" width="64" height="64" fill={ic.highlight ? "rgba(255,255,255,0.15)" : "transparent"} stroke={ic.highlight ? "rgba(255,255,255,0.4)" : "none"} />
          <rect x="14" y="10" width="36" height="44" fill="#e8e8e8" />
          <rect x="18" y="14" width="28" height="3" fill="#1a4480" />
          <rect x="18" y="22" width="20" height="2" fill="#888" />
          <rect x="18" y="28" width="24" height="2" fill="#888" />
          <text x="32" y="84" textAnchor="middle" fill="#fff" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>{ic.label}</text>
        </g>
      ))}
      {/* taskbar */}
      <rect x="0" y={SCR_H - 32} width={SCR_W} height="32" fill="#2a2a2a" />
      <rect x="8" y={SCR_H - 28} width="40" height="24" fill="#1a4480" />
      <text x={SCR_W - 80} y={SCR_H - 12} fill="#ddd" style={{ font: "11px ui-monospace, monospace" }}>14:32</text>
    </g>
  );
}

function ScrCacPin({ pinEntered = "" }) {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="#1a4480" opacity="0.4" />
      {/* dialog */}
      <g transform="translate(280, 200)">
        <rect width="400" height="220" fill="var(--scr-bg)" stroke="#2a2a2a" />
        <WinTitle title="ActivClient — PIN Required" />
        <text x="20" y="68" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>Smart Card</text>
        <rect x="20" y="76" width="360" height="22" fill="var(--scr-input)" stroke="#888" />
        <text x="28" y="92" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>SMITH.JOHN.A.1234567890</text>

        <text x="20" y="124" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>PIN</text>
        <rect x="20" y="132" width="360" height="22" fill="var(--scr-input)" stroke="#444" strokeWidth="1.5" />
        <text x="28" y="148" fill="var(--scr-fg)" style={{ font: "13px ui-monospace, monospace", letterSpacing: "3px" }}>{pinEntered || "••••••"}</text>

        <rect x="220" y="174" width="76" height="26" fill="#e0e0e0" stroke="#888" />
        <text x="258" y="191" textAnchor="middle" fill="#000" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>OK</text>
        <rect x="304" y="174" width="76" height="26" fill="#e0e0e0" stroke="#888" />
        <text x="342" y="191" textAnchor="middle" fill="#000" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>Cancel</text>
      </g>
    </g>
  );
}

function ScrImdsMenu() {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="var(--scr-bg)" />
      <WinTitle title="IMDS — Main Menu" />
      <MenuBar items={["File", "Edit", "View", "Tools", "Help"]} />

      <rect x="0" y="50" width={SCR_W} height="32" fill="#1a4480" />
      <text x="20" y="71" fill="#fff" style={{ font: "bold 14px ui-sans-serif, system-ui, sans-serif" }}>INTEGRATED MAINTENANCE DATA SYSTEM</text>
      <text x={SCR_W - 20} y="71" textAnchor="end" fill="#fff" style={{ font: "11px ui-monospace, monospace" }}>SMITH.JOHN.A.1234567890 | 1FW/MXG</text>

      {/* Menu grid */}
      <g transform="translate(80, 120)">
        {[
          { label: "Work Orders", desc: "Create / view WOs", highlight: true },
          { label: "Inspections", desc: "Daily / phase / TCTO" },
          { label: "Discrepancies", desc: "Open / closed" },
          { label: "Parts Lookup", desc: "NSN / part number" },
          { label: "Time Compliance", desc: "TCTO tracking" },
          { label: "Reports", desc: "Maintenance summaries" },
        ].map((it, i) => {
          const col = i % 3, row = Math.floor(i / 3);
          return (
            <g key={i} transform={`translate(${col * 260}, ${row * 140})`}>
              <rect width="240" height="120" fill={it.highlight ? "#e8eef7" : "var(--scr-card)"} stroke={it.highlight ? "#1a4480" : "#bbb"} strokeWidth={it.highlight ? "2" : "1"} />
              <rect x="16" y="16" width="32" height="32" fill="#1a4480" />
              <text x="16" y="76" fill="var(--scr-fg)" style={{ font: "bold 13px ui-sans-serif, system-ui, sans-serif" }}>{it.label}</text>
              <text x="16" y="96" fill="var(--scr-fg-dim)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>{it.desc}</text>
            </g>
          );
        })}
      </g>
    </g>
  );
}

function ScrImdsWoList() {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="var(--scr-bg)" />
      <WinTitle title="IMDS — Work Orders" />
      <MenuBar items={["File", "Edit", "View", "Actions", "Help"]} />

      {/* toolbar */}
      <rect x="0" y="50" width={SCR_W} height="44" fill="var(--scr-toolbar)" />
      <rect x="12" y="60" width="120" height="24" fill="#1a4480" stroke="#0d3060" />
      <text x="72" y="76" textAnchor="middle" fill="#fff" style={{ font: "bold 11px ui-sans-serif, system-ui, sans-serif" }}>+ New Work Order</text>
      <rect x="140" y="60" width="80" height="24" fill="var(--scr-card)" stroke="#888" />
      <text x="180" y="76" textAnchor="middle" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>Refresh</text>
      <rect x="228" y="60" width="80" height="24" fill="var(--scr-card)" stroke="#888" />
      <text x="268" y="76" textAnchor="middle" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>Filter</text>

      {/* table header */}
      <rect x="0" y="100" width={SCR_W} height="28" fill="var(--scr-tablehdr)" />
      {["WO Number", "Tail #", "WUC", "Status", "Assigned", "Opened"].map((h, i) => (
        <text key={i} x={20 + i * 150} y="118" fill="var(--scr-fg)" style={{ font: "bold 11px ui-sans-serif, system-ui, sans-serif" }}>{h}</text>
      ))}

      {/* rows */}
      {[
        ["WO-89231", "TN-12345", "14000", "Open", "SMITH.J", "04/27/26"],
        ["WO-89232", "TN-67890", "11000", "In Work", "LOPEZ.R", "04/27/26"],
        ["WO-89233", "TN-12345", "23000", "Closed", "PARK.H", "04/26/26"],
        ["WO-89234", "TN-44556", "14000", "Open", "SMITH.J", "04/26/26"],
        ["WO-89235", "TN-99887", "75000", "Open", "PARK.H", "04/25/26"],
      ].map((row, ri) => (
        <g key={ri}>
          <rect x="0" y={128 + ri * 26} width={SCR_W} height="26" fill={ri % 2 ? "var(--scr-row-alt)" : "var(--scr-bg)"} />
          {row.map((cell, ci) => (
            <text key={ci} x={20 + ci * 150} y={146 + ri * 26} fill="var(--scr-fg)" style={{ font: "11px ui-monospace, monospace" }}>{cell}</text>
          ))}
        </g>
      ))}
    </g>
  );
}

function ScrImdsWoEntry({ wo = "", tail = "", wuc = "", showRef = false }) {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="var(--scr-bg)" />
      <WinTitle title="IMDS — Work Order Entry" />
      <MenuBar items={["File", "Edit", "View", "Actions", "Help"]} />

      <rect x="0" y="50" width={SCR_W} height="32" fill="#1a4480" />
      <text x="20" y="71" fill="#fff" style={{ font: "bold 13px ui-sans-serif, system-ui, sans-serif" }}>NEW WORK ORDER</text>

      {/* form */}
      <g transform="translate(60, 120)">
        {[
          ["Work Order Number", wo, true],
          ["Tail Number", tail, true],
          ["Work Unit Code (WUC)", wuc, true],
          ["Discrepancy Description", "", false],
          ["Priority", "Routine ▾", false],
          ["Reference T.O.", showRef ? "1F-16C-2-29" : "", false],
        ].map(([label, val, focus], i) => (
          <g key={i} transform={`translate(0, ${i * 56})`}>
            <text x="0" y="14" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>{label}</text>
            <rect x="0" y="22" width="380" height="24" fill="var(--scr-input)" stroke={focus ? "#1a4480" : "#888"} strokeWidth={focus ? "1.5" : "1"} />
            <text x="8" y="38" fill="var(--scr-fg)" style={{ font: "12px ui-monospace, monospace" }}>{val}</text>
          </g>
        ))}
      </g>

      {/* right panel — recent activity */}
      <g transform="translate(500, 120)">
        <rect width="400" height="380" fill="var(--scr-card)" stroke="#bbb" />
        <text x="16" y="24" fill="var(--scr-fg)" style={{ font: "bold 12px ui-sans-serif, system-ui, sans-serif" }}>Aircraft History — TN-12345</text>
        <line x1="0" y1="36" x2="400" y2="36" stroke="#bbb" />
        {[
          ["04/27/26", "Hydraulic line replacement", "CLOSED"],
          ["04/12/26", "Phase inspection — 200hr", "CLOSED"],
          ["03/28/26", "Avionics BIT failure", "CLOSED"],
          ["03/15/26", "Brake assembly R&R", "CLOSED"],
          ["02/29/26", "Engine borescope", "CLOSED"],
        ].map(([d, desc, st], i) => (
          <g key={i} transform={`translate(0, ${48 + i * 28})`}>
            <text x="16" y="14" fill="var(--scr-fg)" style={{ font: "10px ui-monospace, monospace" }}>{d}</text>
            <text x="92" y="14" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>{desc}</text>
            <text x="380" y="14" textAnchor="end" fill="#5a8a3a" style={{ font: "bold 9px ui-monospace, monospace" }}>{st}</text>
          </g>
        ))}
      </g>

      {/* buttons */}
      <g transform={`translate(${SCR_W - 280}, ${SCR_H - 60})`}>
        <rect x="0" y="0" width="120" height="30" fill="var(--scr-card)" stroke="#888" />
        <text x="60" y="20" textAnchor="middle" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>Attach Reference</text>
        <rect x="132" y="0" width="120" height="30" fill="#1a4480" stroke="#0d3060" />
        <text x="192" y="20" textAnchor="middle" fill="#fff" style={{ font: "bold 11px ui-sans-serif, system-ui, sans-serif" }}>Submit</text>
      </g>
    </g>
  );
}

// G081 / TN3270 green-screen — the demo moment
function ScrG081({ typed = false }) {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="#0a0a0a" />
      <WinTitle title="G081 Reference Lookup — BlueZone Mainframe" />
      {/* terminal area */}
      <rect x="0" y="28" width={SCR_W} height={SCR_H - 28} fill="#000" />
      {(() => {
        const lines = [
          "G081 REFERENCE PUBLICATION LOOKUP                              SCRN: REF01",
          "================================================================================",
          "",
          "  COMMAND ===>",
          "",
          "  ENTER REF T.O. NUMBER:  " + (typed ? "1F-16C-2-29_" : "____________"),
          "",
          "  AVAILABLE PUBLICATIONS FOR TAIL: TN-12345",
          "  --------------------------------------------------------------------",
          "  1F-16C-1     FLIGHT MANUAL                              REV 47   ACTIVE",
          "  1F-16C-2-1   GENERAL MAINTENANCE                        REV 31   ACTIVE",
          "  1F-16C-2-29  HYDRAULIC PRESSURE TEST PROCEDURE          REV 12   ACTIVE",
          "  1F-16C-2-94  EGRESS SYSTEM SAFE/ARM                     REV 08   ACTIVE",
          "  1F-16C-6     INSPECTION REQUIREMENTS                    REV 22   ACTIVE",
          "  1F-16C-23    NON-DESTRUCTIVE INSPECTION                 REV 14   ACTIVE",
          "",
          "",
          "  PF1=HELP  PF2=NEXT  PF3=EXIT  PF7=UP  PF8=DOWN  ENTER=SELECT",
        ];
        return lines.map((ln, i) => (
          <text key={i} x="20" y={56 + i * 18} fill="#33ff33" style={{ font: "13px ui-monospace, Consolas, monospace", whiteSpace: "pre" }}>{ln.replace(/ /g, "\u00a0")}</text>
        ));
      })()}
      {/* status bar */}
      <rect x="0" y={SCR_H - 24} width={SCR_W} height="24" fill="#1a4480" />
      <text x="12" y={SCR_H - 8} fill="#fff" style={{ font: "11px ui-monospace, monospace" }}>BlueZone — SESSION A — CONNECTED — 24x80</text>
      <text x={SCR_W - 12} y={SCR_H - 8} textAnchor="end" fill="#fff" style={{ font: "11px ui-monospace, monospace" }}>{typed ? "06/16" : "06/24"}</text>
    </g>
  );
}

function ScrImdsSubmit() {
  return (
    <g>
      <rect width={SCR_W} height={SCR_H} fill="var(--scr-bg)" />
      <WinTitle title="IMDS — Work Order Entry" />
      <MenuBar items={["File", "Edit", "View", "Actions", "Help"]} />

      {/* confirm dialog */}
      <rect x="0" y="50" width={SCR_W} height={SCR_H - 50} fill="rgba(0,0,0,0.3)" />
      <g transform="translate(280, 180)">
        <rect width="400" height="240" fill="var(--scr-bg)" stroke="#2a2a2a" />
        <rect x="0" y="0" width="400" height="28" fill="var(--scr-titlebar)" />
        <text x="12" y="19" fill="var(--scr-titlebar-fg)" style={{ font: "12px ui-sans-serif, system-ui, sans-serif" }}>Submit Work Order</text>

        <text x="20" y="70" fill="var(--scr-fg)" style={{ font: "12px ui-sans-serif, system-ui, sans-serif" }}>Submit work order WO-99999?</text>

        <g transform="translate(20, 90)">
          {[
            ["Work Order:", "WO-99999"],
            ["Tail Number:", "TN-12345"],
            ["WUC:", "14000 — Hydraulic"],
            ["T.O. Reference:", "1F-16C-2-29"],
            ["Priority:", "Routine"],
          ].map(([k, v], i) => (
            <g key={i} transform={`translate(0, ${i * 18})`}>
              <text x="0" y="12" fill="var(--scr-fg-dim)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>{k}</text>
              <text x="120" y="12" fill="var(--scr-fg)" style={{ font: "11px ui-monospace, monospace" }}>{v}</text>
            </g>
          ))}
        </g>

        <rect x="220" y="194" width="76" height="28" fill="var(--scr-card)" stroke="#888" />
        <text x="258" y="212" textAnchor="middle" fill="var(--scr-fg)" style={{ font: "11px ui-sans-serif, system-ui, sans-serif" }}>Cancel</text>
        <rect x="304" y="194" width="76" height="28" fill="#1a4480" stroke="#0d3060" strokeWidth="2" />
        <text x="342" y="212" textAnchor="middle" fill="#fff" style={{ font: "bold 11px ui-sans-serif, system-ui, sans-serif" }}>Submit</text>
      </g>
    </g>
  );
}

// Click highlight — draws an orange ring at the click coordinates
function ClickHighlight({ x, y }) {
  return (
    <g>
      <circle cx={x} cy={y} r="20" fill="none" stroke="var(--accent)" strokeWidth="3" opacity="0.85" />
      <circle cx={x} cy={y} r="32" fill="none" stroke="var(--accent)" strokeWidth="2" opacity="0.5" />
      <circle cx={x} cy={y} r="6" fill="var(--accent)" />
    </g>
  );
}

// Renders a screenshot by id, with optional click + redactions
function Screenshot({ step, redactions = [], showClick = true }) {
  if (!step) return null;
  const id = step.screenshot;
  let content;
  switch (id) {
    case "desktop": content = <ScrDesktop />; break;
    case "cac_pin": content = <ScrCacPin />; break;
    case "imds_menu": content = <ScrImdsMenu />; break;
    case "imds_wo_list": content = <ScrImdsWoList />; break;
    case "imds_wo_entry":
      content = <ScrImdsWoEntry wo={step.seq >= 5 ? "WO-99999" : ""} tail={step.seq >= 6 ? "TN-12345" : ""} wuc={step.seq >= 7 ? "14000 — Hydraulic System" : ""} />;
      break;
    case "imds_wo_entry_full":
      content = <ScrImdsWoEntry wo="WO-99999" tail="TN-12345" wuc="14000 — Hydraulic System" showRef />;
      break;
    case "g081_terminal": content = <ScrG081 typed={false} />; break;
    case "g081_terminal_typed": content = <ScrG081 typed={true} />; break;
    case "imds_wo_submit": content = <ScrImdsSubmit />; break;
    default:
      content = <rect width={SCR_W} height={SCR_H} fill="#222" />;
  }
  return (
    <svg viewBox={`0 0 ${SCR_W} ${SCR_H}`} preserveAspectRatio="xMidYMid meet" style={{ width: "100%", height: "100%", display: "block" }}>
      {content}
      {showClick && step.click && <ClickHighlight x={step.click.x} y={step.click.y} />}
      {redactions.map((r, i) => (
        <g key={i}>
          <rect x={r.x * SCR_W} y={r.y * SCR_H} width={r.w * SCR_W} height={r.h * SCR_H} fill="#000" />
          <text
            x={r.x * SCR_W + (r.w * SCR_W) / 2}
            y={r.y * SCR_H + (r.h * SCR_H) / 2 + 4}
            textAnchor="middle"
            fill="var(--accent)"
            style={{ font: "bold 11px ui-monospace, monospace", letterSpacing: "1px" }}
          >REDACTED{r.label ? ` · ${r.label}` : ""}</text>
        </g>
      ))}
    </svg>
  );
}

window.AGSOP_SCR = { Screenshot, SCR_W, SCR_H };
