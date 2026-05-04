// app.jsx — main shell, navigation, state, banner, editor host

const { Library, Settings, RecorderHUD, ExportModal } = window.AGSOP_SCREENS;
const { StepList, Canvas, FallbackPanel, Inspector } = window.AGSOP_EDITOR;
const { SESSIONS, STEPS } = window.AGSOP_DATA;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "theme": "dark",
  "accent": "#ff7a1a",
  "bannerLevel": "CUI",
  "density": "comfortable",
  "showOcrFallback": true
}/*EDITMODE-END*/;

const BANNER_PRESETS = {
  CUI: { text: "CUI", color: "#5b21b6", fg: "#fff" },
  SECRET: { text: "SECRET", color: "#b91c1c", fg: "#fff" },
};

function NavItem({ id, label, badge, active, onClick }) {
  return (
    <button className={`nav-item ${active ? "active" : ""}`} onClick={onClick}>
      <span className="nav-item-label">{label}</span>
      {badge != null && <span className="nav-item-badge mono">{badge}</span>}
    </button>
  );
}

function ClassificationBar({ position, text, color, fg }) {
  return (
    <div className={`cui-bar cui-bar-${position}`} style={{ background: color, color: fg }}>
      <span className="cui-bar-text mono">{text}</span>
      <span className="cui-bar-text mono">{text}</span>
      <span className="cui-bar-text mono">{text}</span>
    </div>
  );
}

function CosmeticDisclaimer() {
  const [open, setOpen] = React.useState(false);
  return (
    <div className={`cosmetic-disclaimer ${open ? "open" : ""}`}>
      <button className="cosmetic-trigger mono" onClick={() => setOpen(o => !o)}>
        ⓘ PROTOTYPE — banner is cosmetic
      </button>
      {open && (
        <div className="cosmetic-body">
          The classification banner shown in this prototype is <b>visual only</b>.
          Real CUI / classified handling on a deployed system requires document-handling
          controls (storage, transmission, access, marking compliance per DoDM 5200.01)
          that are not implemented by CSS. Do not screenshot this prototype to claim
          ATO readiness.
        </div>
      )}
    </div>
  );
}

function EditorScreen({ steps, setSteps, session, accent, density, showOcrFallback, onExport }) {
  const [activeIdx, setActiveIdx] = React.useState(0);
  const [savingState, setSavingState] = React.useState("idle");
  const saveTimer = React.useRef(null);

  // Filter out OCR steps if hidden via tweak
  const visibleSteps = React.useMemo(() => {
    if (showOcrFallback) return steps;
    return steps.filter(s => s.kind !== "tn3270");
  }, [steps, showOcrFallback]);

  const safeIdx = Math.min(activeIdx, visibleSteps.length - 1);
  const active = visibleSteps[safeIdx];
  const activeRealIdx = active ? steps.findIndex(s => s.id === active.id) : -1;

  const triggerSave = () => {
    setSavingState("saving");
    if (saveTimer.current) clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(() => {
      setSavingState("saved");
      setTimeout(() => setSavingState("idle"), 1400);
    }, 450);
  };

  const updateStep = React.useCallback((idxOrNull, patch) => {
    // Special: reorder via _move
    if (patch && patch._move) {
      const { from, to } = patch._move;
      if (to < 0 || to >= steps.length) return;
      const next = steps.slice();
      const [moved] = next.splice(from, 1);
      next.splice(to, 0, moved);
      // resequence
      next.forEach((s, i) => s.seq = i + 1);
      setSteps(next);
      triggerSave();
      return;
    }
    const idx = idxOrNull == null ? activeRealIdx : idxOrNull;
    if (idx < 0) return;
    const next = steps.slice();
    const target = { ...next[idx] };
    if (patch._removeRedaction != null) {
      target.redactions = target.redactions.filter((_, i) => i !== patch._removeRedaction);
    } else {
      Object.assign(target, patch);
    }
    next[idx] = target;
    setSteps(next);
    triggerSave();
  }, [steps, activeRealIdx]);

  const addRedaction = (r) => {
    if (activeRealIdx < 0) return;
    const next = steps.slice();
    next[activeRealIdx] = { ...next[activeRealIdx], redactions: [...next[activeRealIdx].redactions, r] };
    setSteps(next);
    triggerSave();
  };

  if (!active) {
    return <div className="screen empty"><div className="empty-msg">No steps to show. Toggle on the OCR fallback in Tweaks to restore TN3270 steps.</div></div>;
  }

  return (
    <div className="screen editor">
      <div className="editor-header">
        <div>
          <div className="screen-title">{session.name}</div>
          <div className="screen-sub mono">
            {session.id} · {session.event_count} events · captured {session.captured_at.slice(0, 10)} by {session.captured_by}
          </div>
        </div>
        <div className="screen-actions">
          <button className="btn btn-secondary" onClick={() => alert("Preview rendered in a separate tab.")}>Preview</button>
          <button className="btn btn-primary" onClick={onExport}>Export…</button>
        </div>
      </div>

      <div className="editor-body">
        <StepList
          steps={visibleSteps}
          activeIdx={safeIdx}
          setActiveIdx={setActiveIdx}
          onUpdate={(i, patch) => {
            // i is index within visible; map to real
            if (patch && patch._move) {
              const realFrom = steps.findIndex(s => s.id === visibleSteps[patch._move.from].id);
              const realTo = steps.findIndex(s => s.id === visibleSteps[patch._move.to].id);
              updateStep(null, { _move: { from: realFrom, to: realTo } });
              return;
            }
            const realIdx = i == null ? activeRealIdx : steps.findIndex(s => s.id === visibleSteps[i].id);
            updateStep(realIdx, patch);
          }}
          density={density}
        />

        <div className="editor-main">
          <Canvas
            step={active}
            onAddRedaction={addRedaction}
            onRemoveRedaction={(i) => updateStep(activeRealIdx, { _removeRedaction: i })}
            showClick={true}
            accent={accent}
          />
          {active.kind === "tn3270" && <FallbackPanel step={active} />}
          <Inspector
            step={active}
            onChange={(patch) => updateStep(activeRealIdx, patch)}
            savingState={savingState}
          />
        </div>
      </div>
    </div>
  );
}

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [route, setRoute] = React.useState("editor");
  const [activeSessionId, setActiveSessionId] = React.useState(SESSIONS[0].id);
  const [steps, setSteps] = React.useState(STEPS);
  const [exportOpen, setExportOpen] = React.useState(false);
  const [patterns, setPatterns] = React.useState([
    { glob: "*SSN*", enabled: true },
    { glob: "*DODID*", enabled: true },
    { glob: "*CAC*Pin*", enabled: true },
    { glob: "txtPin*", enabled: true },
    { glob: "*Password*", enabled: true },
    { glob: "*Birthdate*", enabled: false },
  ]);

  const banner = BANNER_PRESETS[t.bannerLevel] || BANNER_PRESETS.CUI;
  const [bannerOverride, setBannerOverride] = React.useState({ text: banner.text, color: banner.color });

  // when tweak banner level changes, snap override to match
  React.useEffect(() => {
    setBannerOverride({ text: banner.text, color: banner.color });
  }, [t.bannerLevel]);

  const session = SESSIONS.find(s => s.id === activeSessionId) || SESSIONS[0];

  const themeClass = `theme-${t.theme}`;
  const densityClass = `density-${t.density}`;

  // Apply CSS variables for theme + accent
  React.useEffect(() => {
    document.documentElement.style.setProperty("--accent", t.accent);
  }, [t.accent]);

  return (
    <div className={`app ${themeClass} ${densityClass}`}>
      <ClassificationBar position="top" text={bannerOverride.text} color={bannerOverride.color} fg="#fff" />

      <div className="shell">
        <aside className="sidebar">
          <div className="brand">
            <div className="brand-mark mono">▮</div>
            <div className="brand-text">
              <div className="brand-name mono">airgap-sop</div>
              <div className="brand-version mono dim">v0.1.0+demo</div>
            </div>
          </div>

          <div className="sidebar-section">
            <div className="sidebar-section-label mono">studio</div>
            <NavItem label="Library" badge={SESSIONS.length} active={route === "library"} onClick={() => setRoute("library")} />
            <NavItem label="Editor" badge={steps.filter(s => s.enabled).length} active={route === "editor"} onClick={() => setRoute("editor")} />
            <NavItem label="Settings" active={route === "settings"} onClick={() => setRoute("settings")} />
          </div>

          <div className="sidebar-section">
            <div className="sidebar-section-label mono">recorder</div>
            <NavItem label="HUD &amp; tray" active={route === "hud"} onClick={() => setRoute("hud")} />
          </div>

          <div className="sidebar-foot">
            <div className="loopback-pill">
              <span className="loopback-dot" />
              <span className="mono">127.0.0.1:7714</span>
            </div>
            <div className="loopback-sub mono dim">loopback-only · no egress</div>
          </div>
        </aside>

        <main className="main">
          {route === "library" && (
            <Library sessions={SESSIONS} activeSessionId={activeSessionId} onSelect={(id) => { setActiveSessionId(id); setRoute("editor"); }} />
          )}
          {route === "editor" && (
            <EditorScreen
              steps={steps}
              setSteps={setSteps}
              session={session}
              accent={t.accent}
              density={t.density}
              showOcrFallback={t.showOcrFallback}
              onExport={() => setExportOpen(true)}
            />
          )}
          {route === "settings" && (
            <Settings
              patterns={patterns}
              setPatterns={setPatterns}
              banner={bannerOverride}
              setBanner={setBannerOverride}
            />
          )}
          {route === "hud" && <RecorderHUD />}
        </main>
      </div>

      <ClassificationBar position="bottom" text={bannerOverride.text} color={bannerOverride.color} fg="#fff" />

      <CosmeticDisclaimer />

      {exportOpen && (
        <ExportModal
          steps={steps}
          session={session}
          banner={bannerOverride}
          onClose={() => setExportOpen(false)}
          onConfirm={() => {
            setExportOpen(false);
            window.__lastExport = { at: new Date(), format: "html" };
          }}
        />
      )}

      <TweaksPanel title="Tweaks">
        <TweakSection label="Theme" />
        <TweakRadio label="Mode" value={t.theme}
                    options={[{ value: "dark", label: "Dark" }, { value: "darker", label: "Darker" }, { value: "hc", label: "HC" }]}
                    onChange={(v) => setTweak("theme", v)} />
        <TweakColor label="Accent" value={t.accent} onChange={(v) => setTweak("accent", v)} />
        <TweakRadio label="Density" value={t.density}
                    options={["comfortable", "compact"]}
                    onChange={(v) => setTweak("density", v)} />

        <TweakSection label="Banner (cosmetic)" />
        <TweakRadio label="Level" value={t.bannerLevel}
                    options={["CUI", "SECRET"]}
                    onChange={(v) => setTweak("bannerLevel", v)} />

        <TweakSection label="Editor" />
        <TweakToggle label="Show OCR fallback steps" value={t.showOcrFallback} onChange={(v) => setTweak("showOcrFallback", v)} />
      </TweaksPanel>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
