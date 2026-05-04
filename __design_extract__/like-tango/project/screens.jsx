// screens.jsx — Library, Settings, Recorder HUD, Export modal

const { Screenshot } = window.AGSOP_SCR;

// ── Library ────────────────────────────────────────────────────────────────

function Library({ sessions, activeSessionId, onSelect }) {
  const [filter, setFilter] = React.useState("all");
  const filtered = sessions.filter(s => filter === "all" ? true : s.status === filter);

  return (
    <div className="screen library">
      <div className="screen-header">
        <div>
          <div className="screen-title">Library</div>
          <div className="screen-sub mono">{sessions.length} sessions · all stored locally · no upload</div>
        </div>
        <div className="screen-actions">
          <div className="filter-group">
            {[
              ["all", "All"],
              ["draft", "Draft"],
              ["exported", "Exported"],
              ["archived", "Archived"],
            ].map(([k, l]) => (
              <button key={k} className={`filter-btn ${filter === k ? "active" : ""}`} onClick={() => setFilter(k)}>
                {l}
              </button>
            ))}
          </div>
          <button className="btn btn-secondary" disabled>+ Import bundle</button>
        </div>
      </div>

      <div className="lib-grid">
        {filtered.map(s => {
          const dt = new Date(s.captured_at);
          const date = dt.toISOString().slice(0, 10);
          const time = dt.toISOString().slice(11, 16);
          const dur = `${Math.floor(s.duration_s / 60)}m ${s.duration_s % 60}s`;
          return (
            <div
              key={s.id}
              className={`lib-card ${activeSessionId === s.id ? "active" : ""}`}
              onClick={() => onSelect(s.id)}
            >
              <div className="lib-card-header">
                <span className={`status-pill status-${s.status}`}>{s.status}</span>
                <span className="cui-pill mono">{s.classification}</span>
              </div>
              <div className="lib-card-name">{s.name}</div>
              <div className="lib-card-grid mono">
                <div><span className="dim">user</span> {s.captured_by}</div>
                <div><span className="dim">date</span> {date} {time}Z</div>
                <div><span className="dim">steps</span> {s.event_count}</div>
                <div><span className="dim">dur</span> {dur}</div>
                <div><span className="dim">size</span> {s.bundle_size}</div>
                <div className="lib-card-id"><span className="dim">id</span> {s.id.slice(0, 16)}…</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Settings ───────────────────────────────────────────────────────────────

function Settings({ patterns, setPatterns, banner, setBanner }) {
  const [draftPattern, setDraftPattern] = React.useState("");

  const addPattern = () => {
    if (!draftPattern.trim()) return;
    setPatterns([...patterns, { glob: draftPattern.trim(), enabled: true }]);
    setDraftPattern("");
  };

  return (
    <div className="screen settings">
      <div className="screen-header">
        <div>
          <div className="screen-title">Settings</div>
          <div className="screen-sub mono">stored at <span className="hl">~/.airgap-sop/config.toml</span> · never transmitted</div>
        </div>
      </div>

      <div className="settings-grid">

        <section className="settings-section">
          <div className="settings-section-title">Network posture</div>
          <div className="settings-section-sub">Enforced by Studio at startup. Cannot be overridden from this UI.</div>
          <div className="kv-list">
            <div className="kv-row"><span className="kv-key mono">bind</span><span className="kv-val mono hl">127.0.0.1:7714</span></div>
            <div className="kv-row"><span className="kv-key mono">non-loopback</span><span className="kv-val mono err">refused</span></div>
            <div className="kv-row"><span className="kv-key mono">outbound</span><span className="kv-val mono err">none</span></div>
            <div className="kv-row"><span className="kv-key mono">telemetry</span><span className="kv-val mono err">disabled</span></div>
            <div className="kv-row"><span className="kv-key mono">auto-update</span><span className="kv-val mono err">disabled</span></div>
            <div className="kv-row"><span className="kv-key mono">cdn</span><span className="kv-val mono err">none — htmx vendored</span></div>
          </div>
        </section>

        <section className="settings-section">
          <div className="settings-section-title">Classification banner</div>
          <div className="settings-section-sub">Top + bottom marking applied to Studio and to exported documents. Cosmetic.</div>
          <div className="form-row">
            <label className="form-label">Marking text</label>
            <input className="form-input mono" value={banner.text} onChange={e => setBanner({ ...banner, text: e.target.value })} />
          </div>
          <div className="form-row">
            <label className="form-label">Color</label>
            <div className="color-row">
              {[
                ["#5b21b6", "CUI"],
                ["#b45309", "CUI//SP-PRVCY"],
                ["#b91c1c", "SECRET"],
                ["#15803d", "UNCLASSIFIED"],
              ].map(([c, lbl]) => (
                <button key={c} className={`swatch-btn ${banner.color === c ? "active" : ""}`} onClick={() => setBanner({ ...banner, color: c, text: lbl })}>
                  <span className="swatch-chip" style={{ background: c }} />
                  <span className="mono">{lbl}</span>
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="settings-section settings-section-wide">
          <div className="settings-section-title">Auto-redaction patterns</div>
          <div className="settings-section-sub">When a captured control's automation_id matches one of these globs, the screenshot region of that control's bounding rect is auto-blacked. Patterns are applied at capture time, not at export — the SME can still adjust per-step.</div>
          <div className="patterns-list">
            {patterns.map((p, i) => (
              <div key={i} className="pattern-row">
                <button
                  className={`toggle-btn ${p.enabled ? "on" : "off"}`}
                  onClick={() => setPatterns(patterns.map((x, j) => j === i ? { ...x, enabled: !x.enabled } : x))}
                >{p.enabled ? "ON" : "OFF"}</button>
                <span className="pattern-glob mono">{p.glob}</span>
                <button className="iconbtn" onClick={() => setPatterns(patterns.filter((_, j) => j !== i))}>×</button>
              </div>
            ))}
          </div>
          <div className="pattern-add">
            <input
              className="form-input mono"
              placeholder="e.g. *SSN* or txt*Pin* or *DODID*"
              value={draftPattern}
              onChange={e => setDraftPattern(e.target.value)}
              onKeyDown={e => e.key === "Enter" && addPattern()}
            />
            <button className="btn btn-secondary" onClick={addPattern}>Add pattern</button>
          </div>
        </section>

        <section className="settings-section">
          <div className="settings-section-title">Recorder</div>
          <div className="settings-section-sub">Hotkeys and capture behavior.</div>
          <div className="kv-list">
            <div className="kv-row"><span className="kv-key">Toggle recording</span><span className="kv-val"><span className="kbd">Ctrl</span>+<span className="kbd">Shift</span>+<span className="kbd">R</span></span></div>
            <div className="kv-row"><span className="kv-key">Quit recorder</span><span className="kv-val"><span className="kbd">Ctrl</span>+<span className="kbd">Shift</span>+<span className="kbd">Q</span></span></div>
            <div className="kv-row"><span className="kv-key mono">--ocr</span><span className="kv-val mono">enabled (tesseract 5.3.3)</span></div>
            <div className="kv-row"><span className="kv-key mono">key buffer flush</span><span className="kv-val mono">800 ms idle</span></div>
            <div className="kv-row"><span className="kv-key mono">click highlight</span><span className="kv-val mono">orange · 32px ring · 600 ms</span></div>
          </div>
        </section>

        <section className="settings-section">
          <div className="settings-section-title">About</div>
          <div className="kv-list">
            <div className="kv-row"><span className="kv-key">Version</span><span className="kv-val mono">0.1.0+demo</span></div>
            <div className="kv-row"><span className="kv-key">License</span><span className="kv-val mono">Apache-2.0</span></div>
            <div className="kv-row"><span className="kv-key">Copyright</span><span className="kv-val mono">© Ron, 2026</span></div>
            <div className="kv-row"><span className="kv-key">Build</span><span className="kv-val mono">offline · pyinstaller · UPX off</span></div>
          </div>
        </section>

      </div>
    </div>
  );
}

// ── Recorder HUD ───────────────────────────────────────────────────────────

function RecorderHUD() {
  const [state, setState] = React.useState("recording"); // idle / recording / paused / flushing

  return (
    <div className="screen hud">
      <div className="screen-header">
        <div>
          <div className="screen-title">Recorder HUD</div>
          <div className="screen-sub mono">windows · pynput global hooks · pywinauto UIA · mss capture</div>
        </div>
        <div className="screen-actions">
          <span className="dim">simulate state:</span>
          <div className="filter-group">
            {["idle", "recording", "paused", "flushing"].map(s => (
              <button key={s} className={`filter-btn ${state === s ? "active" : ""}`} onClick={() => setState(s)}>{s}</button>
            ))}
          </div>
        </div>
      </div>

      <div className="hud-stage">
        {/* fake desktop */}
        <div className="hud-desktop">
          <div className="hud-desktop-grid">
            {Array.from({ length: 24 }).map((_, i) => <div key={i} className="hud-desktop-cell" />)}
          </div>

          {/* taskbar with tray */}
          <div className="hud-taskbar">
            <div className="hud-taskbar-start">⊞</div>
            <div className="hud-taskbar-icons">
              <div className="hud-taskbar-app" />
              <div className="hud-taskbar-app" />
              <div className="hud-taskbar-app active" />
            </div>
            <div className="hud-tray">
              <div className="hud-tray-icon" title="Network">⚡</div>
              <div className="hud-tray-icon" title="Audio">🔈</div>
              <div className={`hud-tray-icon airgap ${state}`} title={`airgap-sop · ${state}`}>
                <span className="airgap-dot" />
                <span className="airgap-mark mono">a</span>
              </div>
              <div className="hud-tray-time mono">14:32</div>
            </div>
          </div>

          {/* recording badge */}
          {state === "recording" && (
            <div className="hud-rec-badge">
              <span className="rec-dot" />
              <span className="mono">REC</span>
              <span className="dim mono">02:47 · 11 events</span>
            </div>
          )}
          {state === "paused" && (
            <div className="hud-rec-badge paused">
              <span className="mono">▌▌ PAUSED</span>
              <span className="dim mono">02:47 · resume <span className="kbd">Ctrl</span>+<span className="kbd">Shift</span>+<span className="kbd">R</span></span>
            </div>
          )}
          {state === "flushing" && (
            <div className="hud-rec-badge flushing">
              <span className="mono">⟳ FLUSHING BUFFER</span>
              <span className="dim mono">writing 11 events to sqlite…</span>
            </div>
          )}

          {/* hotkey toast on idle */}
          {state === "idle" && (
            <div className="hud-toast">
              <div className="hud-toast-title mono">airgap-sop · idle</div>
              <div className="hud-toast-body">
                Press <span className="kbd">Ctrl</span>+<span className="kbd">Shift</span>+<span className="kbd">R</span> to start recording.
              </div>
            </div>
          )}

          {/* tray menu (always visible to show what right-click looks like) */}
          <div className="hud-tray-menu">
            <div className="hud-tray-menu-header mono">airgap-sop · {state}</div>
            <div className="hud-tray-menu-row"><span>Start recording</span><span className="kbd-row"><span className="kbd">⌃</span><span className="kbd">⇧</span><span className="kbd">R</span></span></div>
            <div className="hud-tray-menu-row"><span>Pause</span><span className="dim mono">{state === "recording" ? "available" : "—"}</span></div>
            <div className="hud-tray-menu-row"><span>Open last bundle in Studio…</span></div>
            <div className="hud-tray-menu-sep" />
            <div className="hud-tray-menu-row"><span className="dim">Output:</span><span className="mono dim">~/sessions/</span></div>
            <div className="hud-tray-menu-row"><span className="dim">OCR:</span><span className="mono dim">tesseract 5.3.3</span></div>
            <div className="hud-tray-menu-sep" />
            <div className="hud-tray-menu-row"><span>Quit</span><span className="kbd-row"><span className="kbd">⌃</span><span className="kbd">⇧</span><span className="kbd">Q</span></span></div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Export modal ───────────────────────────────────────────────────────────

function ExportModal({ steps, session, onClose, onConfirm, banner }) {
  const [format, setFormat] = React.useState("html");
  const [includeMeta, setIncludeMeta] = React.useState(true);
  const [confirmed, setConfirmed] = React.useState(false);

  const enabled = steps.filter(s => s.enabled);
  const totalRedactions = steps.reduce((n, s) => n + s.redactions.length, 0);
  const sensitiveSteps = steps.filter(s => s.sensitive);
  const unredactedSensitive = sensitiveSteps.filter(s => s.enabled && s.redactions.length === 0);
  const blocked = unredactedSensitive.length > 0 || !confirmed;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <div className="modal-title">Export SOP</div>
            <div className="modal-sub mono dim">{session.name}</div>
          </div>
          <button className="iconbtn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">

          <div className="modal-section">
            <div className="modal-section-label">Format</div>
            <div className="format-row">
              {[
                ["html", "HTML", "Jinja2 · single file · standalone"],
                ["pdf", "PDF", "WeasyPrint · A4 · embeds banners"],
                ["docx", "DOCX", "python-docx · for AFI/T.O. mirrors"],
              ].map(([k, l, d]) => (
                <button key={k} className={`format-btn ${format === k ? "active" : ""}`} onClick={() => setFormat(k)}>
                  <div className="format-name">{l}</div>
                  <div className="format-desc mono dim">{d}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="modal-section">
            <div className="modal-section-label">Include</div>
            <label className="check-row">
              <input type="checkbox" checked={includeMeta} onChange={e => setIncludeMeta(e.target.checked)} />
              <span>Include capture metadata (window class, automation ID, timestamps)</span>
            </label>
            <label className="check-row">
              <input type="checkbox" checked={true} disabled />
              <span>Apply classification banner: <span className="mono hl">{banner.text}</span></span>
            </label>
          </div>

          <div className="modal-section">
            <div className="modal-section-label">Redaction summary</div>
            <div className="redact-summary">
              <div className="redact-summary-row">
                <span className="dim">Steps included:</span>
                <span className="mono">{enabled.length} of {steps.length}</span>
              </div>
              <div className="redact-summary-row">
                <span className="dim">Total redactions baked:</span>
                <span className="mono">{totalRedactions}</span>
              </div>
              <div className="redact-summary-row">
                <span className="dim">Sensitive steps:</span>
                <span className="mono">{sensitiveSteps.length}</span>
              </div>
            </div>

            {unredactedSensitive.length > 0 ? (
              <div className="alert alert-blocking">
                <div className="alert-title mono">⚠ EXPORT BLOCKED</div>
                <div>
                  {unredactedSensitive.length} sensitive step{unredactedSensitive.length > 1 ? "s have" : " has"} no redactions applied:
                </div>
                <ul className="alert-list">
                  {unredactedSensitive.map(s => (
                    <li key={s.id} className="mono">step {s.seq} · {s.name}</li>
                  ))}
                </ul>
                <div className="dim">Either redact the sensitive region on the canvas, or disable the step.</div>
              </div>
            ) : (
              <label className="confirm-row">
                <input type="checkbox" checked={confirmed} onChange={e => setConfirmed(e.target.checked)} />
                <span>
                  I have reviewed every screenshot and confirm no CUI, PII, or otherwise sensitive content is visible in any unredacted area. Once exported, redactions are baked into the image and cannot be reversed from the document.
                </span>
              </label>
            )}
          </div>

        </div>

        <div className="modal-footer">
          <span className="dim mono">output: ~/exports/{session.id}.{format}</span>
          <div className="modal-footer-actions">
            <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button className="btn btn-primary" disabled={blocked} onClick={onConfirm}>
              Export {format.toUpperCase()}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

window.AGSOP_SCREENS = { Library, Settings, RecorderHUD, ExportModal };
