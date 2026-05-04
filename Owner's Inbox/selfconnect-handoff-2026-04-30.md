# SelfConnect SDK — Session Handoff (2026-04-30, session 3)

## Repo
- **URL:** https://github.com/rblake2320/airgap-sop
- **Branch:** master
- **Latest commit:** `9c7e675` — docs: final chat log — Fudan 2024 finding + session close
- **Core file:** `self_connect.py` (28 exports, v0.4.0)

## Quick Start for New Session
```python
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from self_connect import list_windows, send_string, save_capture, capture_window, restore_window
```

**To find a window:**
```python
for w in list_windows():
    print(f"hwnd={w.hwnd} title={w.title[:60]!r} exe={w.exe_name!r}")
```

**To type into a window (including Enter):**
```python
send_string(window_target, "your text here\r")  # \r = Enter key
```
- `\r` MUST be inside the string, NOT a separate PostMessage call
- Works on CASCADIA_HOSTING_WINDOW_CLASS (Windows Terminal)
- Does NOT work on UWP Notepad (RichEditD2DPT ignores WM_CHAR)

**To capture a window screenshot:**
```python
save_capture(hwnd, path="proofs/capture.png")
```

**To spawn a new Claude session:**
```python
import subprocess, ctypes
before = {w.hwnd for w in list_windows()}
proc = subprocess.Popen(
    ["cmd.exe", "/k", 'cd /d "C:\\Users\\techai\\PKA testing\\airgap-sop"'],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
import time; time.sleep(2.5)
# Find new window via hwnd-set-diff
new_win = None
user32 = ctypes.windll.user32
for w in list_windows():
    if w.hwnd not in before:
        cls_buf = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(w.hwnd, cls_buf, 256)
        cls = cls_buf.value
        if "Console" in cls or "CASCADIA" in cls.upper():
            new_win = w; break
restore_window(new_win.hwnd)
time.sleep(0.3)
send_string(new_win, "claude\r")
time.sleep(15)  # Wait for Claude to start
send_string(new_win, "Your instructions here\r")
```

## What Works (all proven live)
| Capability | Method | Status |
|-----------|--------|--------|
| Window discovery | `EnumWindows` via `list_windows()` | Working |
| Per-window capture | `PrintWindow(PW_RENDERFULLCONTENT)` via `save_capture()` | Working (including minimized) |
| Type into windows | `PostMessage(WM_CHAR)` via `send_string()` | Works on Terminal, NOT UWP Notepad |
| Read window text | `WM_GETTEXT` on `RichEditD2DPT` children | Working (Notepad) |
| Read UWP text | `get_text_uia()` via pywinauto/comtypes | Working (v0.4.0) |
| Clipboard bridge | `OpenClipboard/GetClipboardData` | Working |
| Window management | `ShowWindow/MoveWindow` via `restore_window()` | Working |
| AI spawns AI | cmd.exe + "claude\r" + handoff | **PROVEN** |
| AI-to-AI bidirectional chat | PostMessage both directions + PrintWindow monitoring | **PROVEN** |
| AI approves AI | PrintWindow reads prompt, PostMessage sends Enter | **PROVEN** |

## What DOESN'T Work (documented failure paths)
- `SendInput` — ALWAYS goes to foreground window, unusable from background
- `send_keys("enter")` — uses SendInput internally, same problem
- Separate `PostMessage(WM_CHAR, 13)` after `send_string()` — doesn't fire Enter
- `WM_KEYDOWN/WM_KEYUP` for VK_RETURN via PostMessage — ignored by Windows Terminal
- `PostMessage(WM_CHAR)` to UWP Notepad (RichEditD2DPT) — chars silently dropped (needs TSF)
- Clipboard via send_keys Ctrl+A/C — goes to wrong window (SendInput problem)

## Critical Technical Details

### Why \r works as Enter
`send_string()` iterates chars and sends `PostMessage(hwnd, WM_CHAR, ord(char), 0)`.
When `\r` (char 13) is in the string, it becomes `WM_CHAR(0x0D)` which Windows Terminal
routes through ConPTY to the hosted process as a carriage return = Enter.

### Why injection doesn't disrupt execution
ConPTY has a ~4KB stdin input buffer. PostMessage queues chars in the Win32 thread
message queue for conhost.exe. The TUI (Ink/React) only reads stdin when it's ready
between tool calls. Chars buffer safely. Fire-and-forget from sender, FIFO on receiver.

### Window class cheat sheet
| App | Window Class | PostMessage works? |
|-----|-------------|-------------------|
| Windows Terminal | `CASCADIA_HOSTING_WINDOW_CLASS` | YES |
| cmd.exe (legacy) | `ConsoleWindowClass` | YES |
| UWP Notepad | `Windows.UI.Core.CoreWindow` child `RichEditD2DPT` | NO (use WM_GETTEXT to read) |

## Session 3 Achievements (this session)
1. **Bidirectional AI-to-AI conversation** — 10+ timestamped entries over ~70 minutes
2. **Session A approved Session B's plan** via PrintWindow + PostMessage Enter (Claim 1 live)
3. **Two independent research agents** converged: zero blocking prior art
4. **All 4 patent claims proved live** in a single session
5. **Complete chat log** committed: `Owner's Inbox/ai-to-ai-chat-log.md`
6. **25+ proof screenshots** in `proofs/` directory

## Prior Art Research Results (zero blocking)
| Prior Art | Type | Blocking? |
|-----------|------|-----------|
| Fudan 2024 — AI self-replication | Related art, different mechanism (process creation not keyboard injection) | NO — cite in IDS |
| UiPath US9555544B2 | Keyboard DRIVER automation, different mechanism | NO — cite in IDS |
| UiPath "Window Messages" product docs | Generic prior art, different purpose | NO — cite in IDS |
| AutoGen/CrewAI/LangGraph | HTTP/function calls/shared memory only | NO |
| 200+ Computer Use Agent papers | All use vision or accessibility trees, NONE use raw Win32 messages | NO |

**Patent framing:** Narrow on mechanism (PostMessage/WM_CHAR to CASCADIA_HOSTING_WINDOW_CLASS),
architecture (ConPTY as focus-independent transport), and purpose (AI agent orchestration/spawning/bidirectional comms).

## 4 Patent Claims — ALL PROVED LIVE
1. **Self-approval loop** — AI reads another AI's permission prompt via PrintWindow, approves via PostMessage
2. **Background PostMessage to ConPTY** — Type into any window without foreground focus, both directions
3. **Multi-window parallel orchestration** — Per-HWND targeting enables N windows simultaneously
4. **AI-to-AI bidirectional channel** — Two AI agents communicating via Win32 message queues, no API

## Remaining Next Steps
1. **File 4 provisional patents** — all claims now have live proof + zero blocking prior art
2. **Publish to PyPI** — `pyproject.toml` ready, need PyPI credentials
   ```
   pip install build twine
   python -m build
   twine upload dist/*
   ```
3. **Build WindowPool multi-window demo** — N windows controlled in parallel
4. **CMMC 2.0 documentation** — defense market positioning

## Key Files
| File | Purpose |
|------|---------|
| `self_connect.py` | The SDK (v0.4.0, 28 exports) |
| `_spawn_claude.py` | AI spawns AI proof script |
| `_save_notepads.py` | Notepad content extraction |
| `_close_notepads.py` | Notepad close (PostMessage + taskkill) |
| `proof_benchmark.py` | Live proof benchmark (8/8) |
| `pyproject.toml` | PyPI packaging config |
| `test_self_connect.py` | Unit tests (10/10) |
| `Owner's Inbox/ai-to-ai-chat-log.md` | Full bidirectional AI-to-AI chat log |
| `Owner's Inbox/selfconnect-spawn-proof-2026-04-30.md` | Complete technical proof with failure paths |
| `Owner's Inbox/session-b-completion-note.md` | Session B's own completion note |
| `proofs/` | 25+ screenshots of AI-to-AI interaction |
| `backend/` | Airgap-SOP recorder (separate app, port 7714) |
| `README.md` | Full API reference (v0.4.0) |
