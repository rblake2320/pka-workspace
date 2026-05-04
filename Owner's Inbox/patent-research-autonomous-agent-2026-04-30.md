# Patent Research: Autonomous Self-Sustaining AI Agent
## Prepared 2026-04-30 for Ron Blake

---

## Ron's Concept (demonstrated with "Droid" months ago)

A closed-loop autonomous AI agent that operates a desktop computer without human intervention:

1. **SEE** — OCR/computer vision reads what's on screen
2. **DECIDE** — AI determines what to click, type, or command based on what it sees
3. **ACT** — OS-level automation (SendInput, mouse clicks, keyboard injection, window focus)
4. **SELF-APPROVE** — AI monitors for permission/confirmation dialogs and clicks through them to keep itself running
5. **CONTINUOUS LOOP** — AI keeps operating indefinitely, writing new commands, reading results, responding to whatever the OS puts in front of it

The Droid proof-of-concept used OCR and computer vision to find a command line, send itself a command, and reply to it. Ron then extended the concept to have the AI handle approval dialogs automatically — recognizing when something needs to be clicked and clicking it to maintain continuous operation.

---

## What Exists in airgap-sop Today (Built 2026-04-30)

The airgap-sop codebase at https://github.com/rblake2320/airgap-sop already contains the primitives:

| Primitive | Implementation | File |
|-----------|---------------|------|
| Window finding | `_find_hwnd(title)` — EnumWindows to locate any window by title | `backend/playback.py` |
| Window focusing | `_focus_window(hwnd)` — AttachThreadInput + SetForegroundWindow | `backend/playback.py` |
| Mouse clicking | `_mouse_click(x, y)` — SendInput with absolute virtual screen coords | `backend/playback.py` |
| Keystroke injection | `_send_string(text)` — SendInput per-character with delay | `backend/playback.py` |
| Screen capture | `_capture_screenshot()` — PrintWindow or full-screen with auto-crop | `backend/recorder.py` |
| OCR | Tesseract OCR on captured screenshots | `backend/recorder.py` |
| UIA element inspection | pywinauto `from_point()` — gets control type, automation ID, name | `backend/recorder.py` |
| Correction override | `user_text` field — AI/human can set what gets typed (decoupled from original capture) | `backend/playback.py` |

The missing piece for full autonomy: a **monitor loop** that continuously captures the screen, feeds it to a local LLM for decision-making, and dispatches actions based on what the model sees.

---

## Prior Art Landscape

### Core concept "AI operates computer via screen + input" — HEAVILY PRIOR-ARTED

| Project | Who | First Date | What It Does |
|---------|-----|-----------|--------------|
| ACT-1 | Adept AI | **Sep 2022** | Action Transformer watching browser, clicking/typing. Raised $350M. |
| AutoGPT / BabyAGI | Open source | **Mar-Apr 2023** | Autonomous task loops, code execution, self-sustaining iteration |
| Self-Operating Computer | OthersideAI | **Nov 2023** | Multimodal model views screen, decides mouse/keyboard actions. Open source. |
| UFO | Microsoft Research | **Feb 2024** | Windows-specific UI agent using UIA APIs + visual grounding. Now at UFO3. |
| Agent S | Simular AI | **Oct 2024** | Open framework, hierarchical planning, experience-augmented |
| Claude Computer Use | Anthropic | **Oct 22, 2024** | First frontier model with native computer use API |
| OpenAI Operator/CUA | OpenAI | **Jan 23, 2025** | GPT-4o vision + reinforcement learning for GUI interaction |
| Agent S2 | Simular AI | **Mar 2025** | State-of-the-art, outperformed Operator and Claude on benchmarks |
| PyWinAssistant | a-real-ai | 2024-2025 | Windows-specific, uses SendInput (OS-native) |
| Windows-Use | CursorTouch | 2025 | Windows UI Automation API + LLM decision-making |
| Open Computer Use | Coasty AI | 2025-2026 | 82% OSWorld score, open source |
| Project Mariner | Google DeepMind | **Dec 2024** | Chrome extension, Gemini 2.5 Pro, browser-only |
| UI Automata | VisionCortex | **Apr 2026** | Windows desktop automation with semantic selectors, demonstrated UAC dialog handling |

### OS-level vs browser-based automation

- **Browser-based** (Playwright/Puppeteer/CDP): Project Mariner, Adept ACT-1. Uses DOM access, not pixel-level.
- **OS-level native** (SendInput, ctypes, UIA): PyWinAssistant, Microsoft UFO, UiPath AI CV, PyAutoGUI (2014+).
- OS-level + AI decision-making is newer but PyWinAssistant and UFO have both done it.

### Key patents in the space

| Patent | Assignee | What It Claims |
|--------|----------|---------------|
| **US 12,387,036 B1** (234 pages) | Anthropic PBC | Intermediary intercepts user-actuated actions on interfaces, preserves state, translates to machine-actuated commands. **VERY BROAD — needs attorney review.** |
| **US 12,437,238** | Anthropic PBC | Client-side interface automation language, agent specification logic |
| **WO2021084510A1** | Enterprise AI | Executing AI agents with workflow editor, multi-agent coordination |
| **US 12,111,859** | Agentic system | Orchestrator supervising subordinate agents, multimodal processing |
| Multiple patents | UiPath Inc. | AI computer vision for RPA, neural network UI element recognition |

---

## WHAT IS POTENTIALLY NOVEL (Best Patent Angles)

### 1. Self-Approval Loop (STRONGEST angle)

No existing project explicitly demonstrates or patents an AI that detects and handles **its own framework's** permission/approval dialogs via computer vision to maintain continuous autonomous operation.

- Claude Code uses `--dangerously-skip-permissions` — this is **flag-based suppression**, not the AI visually recognizing and clicking through dialogs
- UI Automata handles UAC dialogs, but those are OS dialogs during software installation — not the agent's OWN permission system
- The distinction: Ron's concept has the AI **see** the dialog, **recognize** it needs to be approved, and **click** it — using the same see/decide/act loop it uses for everything else

### 2. Air-Gapped Closed Loop

No project found that combines ALL of these in a single system:
- Local LLM (no cloud API)
- OCR/computer vision for screen reading
- OS-level SendInput for automation
- Self-approval of own dialogs
- Running on a disconnected/air-gapped machine

### 3. OS-Native + Local LLM in Single Process

Using ctypes/SendInput (not browser DOM automation) combined with local model inference (Ollama/local LLM) in a closed-loop process — with the AI composing text that gets injected at the OS level.

---

## RISKS

1. **Anthropic's US 12,387,036 is extremely broad** (234 pages). The "intermediary that intercepts user-actuated actions and translates them to machine-actuated commands" language could potentially overlap. Full claims need line-by-line attorney review.

2. **"Self-approval" could be rejected as obvious combination** under 35 USC 103 — combining "agent that clicks buttons" with "dialog box is a button" might not meet non-obviousness threshold.

3. **Safety/ethical framing** — USPTO may resist a patent that claims "AI bypasses its own safety dialogs." Framing matters — focus on "continuous autonomous operation in disconnected environments" rather than "bypassing safety."

4. **Timing risk** — UI Automata (April 2026) demonstrated UAC dialog handling. The field is accelerating. Every month that passes means more prior art.

---

## RECOMMENDED ACTIONS (in priority order)

### 1. Document earliest provable date — IMMEDIATELY
Find timestamped evidence from the original Droid work:
- Git commits (any repo with the Droid code)
- Screenshots with EXIF dates
- Emails discussing the concept
- Chat logs, notes, anything with a date
- This establishes prior art defense even if you don't file a patent

### 2. File a provisional patent application — WITHIN 2 WEEKS
- Cost: ~$320 for a small entity
- Buys 12 months of priority date protection
- Does NOT require final claims — just a description of the invention
- Can be written by you (not ideal) or by an attorney ($1,500-3,000)
- Focus claims on: self-approval via computer vision + air-gapped closed loop

### 3. Engage a patent attorney
- Request a formal prior art search focused on "self-approval of own framework dialogs via computer vision"
- Review Anthropic's US 12,387,036 for claim overlap
- Patent classification codes to search: G06F 3/04842, G06F 9/4881, G06N 3/08
- Budget: $500-1,500 for prior art search; $5,000-15,000 for full utility patent filing

### 4. Consider trade secret as alternative
- If the code won't be open-sourced, trade secret protection may be more practical
- No disclosure required, no expiration
- But no exclusivity against independent discovery
- Can file patent later if you decide to go that route (as long as no public disclosure)

### 5. Review Anthropic's patent portfolio
- US 12,387,036 B1 — 234 pages, very broad
- US 12,437,238 — interface automation
- Both assigned to Anthropic PBC
- Available at https://patents.justia.com/assignee/anthropic-pbc

---

## KEY REFERENCES

- Anthropic Computer Use: https://www.anthropic.com/news/3-5-models-and-computer-use
- Self-Operating Computer: https://github.com/OthersideAI/self-operating-computer
- OpenAI Operator: https://openai.com/index/introducing-operator/
- Microsoft UFO: https://github.com/microsoft/UFO
- Agent S2: https://github.com/simular-ai/Agent-S
- PyWinAssistant: https://github.com/a-real-ai/pywinassistant
- UI Automata: https://automata.visioncortex.org/blog/introducing-ui-automata/
- Anthropic Patents: https://patents.justia.com/assignee/anthropic-pbc
- OSWorld Benchmark: https://arxiv.org/abs/2404.07972
- Patenting Agentic AI (Mintz, Mar 2025): https://www.mintz.com/insights-center/viewpoints/2231/2025-03-19-understanding-how-patent-agentic-ai-systems

---

*Research conducted by NOVA agent, 2026-04-30. This is a web-based landscape assessment, not a formal freedom-to-operate analysis. Consult a patent attorney before making filing decisions.*
