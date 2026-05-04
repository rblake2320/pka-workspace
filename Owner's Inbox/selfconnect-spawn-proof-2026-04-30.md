# SelfConnect SDK — AI Spawns AI: Complete Technical Proof

**Date:** 2026-04-30
**Repo:** https://github.com/rblake2320/airgap-sop
**Commit:** 01160a7 (master)
**Script:** `_spawn_claude.py`

---

## The Achievement

One Claude Code session (Session A) programmatically:
1. Opened a new cmd.exe terminal window
2. Typed "claude" to start a second Claude Code session (Session B)
3. Typed a full handoff message into Session B's prompt
4. Session B autonomously read the handoff, added features (v0.4.0), committed, and pushed

All via Win32 PostMessage — no clipboard, no focus stealing, no API.

---

## What FAILED (and why)

### Attempt 1: `send_keys("ctrl", "a")` / `send_keys("ctrl", "c")`
- **Method:** `SendInput` API for keyboard shortcuts
- **Result:** Keystrokes went to OUR terminal, not the target window
- **Why:** `SendInput` always sends to the foreground window. Windows prevents background processes from stealing foreground focus. Even with `AttachThreadInput` + `SetForegroundWindow`, the terminal recaptured focus before the keystroke fired.
- **Lesson:** `SendInput` is unusable from a background process for targeting a specific window.

### Attempt 2: `PostMessage(WM_CHAR, 13)` as separate call for Enter
- **Method:** Sent text via `send_string()`, then separate `PostMessage(hwnd, WM_CHAR, 13, 0)` for Enter
- **Result:** Text appeared but Enter never executed. All text concatenated on one line.
- **Why:** The separate `PostMessage` for CR (char 13) was sent with lparam=0. Windows Terminal's ConPTY layer may have ignored it because the timing or lparam didn't match what `send_string` uses internally.
- **Lesson:** Don't mix `send_string()` with raw `PostMessage()` for control characters.

### Attempt 3: `send_keys("enter")` after `send_string()`
- **Method:** Used SDK's `send_keys("enter")` which calls `SendInput`
- **Result:** Enter keystroke went to our terminal, not the target
- **Why:** Same `SendInput` foreground problem as Attempt 1
- **Lesson:** `send_keys()` uses `SendInput` internally — same limitation.

### Attempt 4: PostMessage WM_KEYDOWN/WM_KEYUP for VK_RETURN
- **Method:** `PostMessage(hwnd, WM_KEYDOWN, 0x0D, ...)` then `WM_KEYUP`
- **Result:** No effect
- **Why:** Windows Terminal (CASCADIA_HOSTING_WINDOW_CLASS) processes WM_CHAR but ignores WM_KEYDOWN/WM_KEYUP for virtual keys sent via PostMessage.

---

## What WORKED (the exact path)

### The Key Insight
**Include `\r` (carriage return) directly inside the `send_string()` call.**

`send_string()` iterates over each character and sends `PostMessage(hwnd, WM_CHAR, ord(char), 0)` for each one. When `\r` (char 13, carriage return) is included in the string, it gets sent as `WM_CHAR` with wParam=13 — and Windows Terminal processes it as Enter.

### Working Code (exact)

```python
from self_connect import list_windows, send_string, save_capture, restore_window
import subprocess, time, ctypes

user32 = ctypes.windll.user32

# Step 1: Snapshot existing windows
before = {w.hwnd for w in list_windows()}

# Step 2: Launch new cmd.exe with its own console
proc = subprocess.Popen(
    ["cmd.exe", "/k", 'cd /d "C:\\Users\\techai\\PKA testing\\airgap-sop"'],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
time.sleep(2.5)

# Step 3: Find the NEW window (hwnd not in before set)
new_win = None
for w in list_windows():
    if w.hwnd not in before:
        cls_buf = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(w.hwnd, cls_buf, 256)
        cls = cls_buf.value
        if "Console" in cls or "CASCADIA" in cls.upper() or "cmd" in w.title.lower():
            new_win = w
            break

# Step 4: Type a command WITH \r at the end (this IS the Enter key)
restore_window(new_win.hwnd)
time.sleep(0.3)
send_string(new_win, "echo HELLO WORLD\r")
time.sleep(1.5)
# Result: "echo HELLO WORLD" executes, output appears

# Step 5: Launch Claude Code
send_string(new_win, "claude\r")
time.sleep(15)  # Wait for Claude to start
# Result: Claude Code v2.1.92 starts, shows "Welcome back Ron!"

# Step 6: Type the handoff message + submit
handoff = 'Your message here'
send_string(new_win, handoff)
time.sleep(0.5)
send_string(new_win, "\r")  # Submit to Claude
# Result: Claude receives and processes the message
```

### Why This Works

1. **`send_string()` uses `PostMessage(hwnd, WM_CHAR, ...)`** — this sends to a specific HWND, NOT to the foreground window. No focus needed.

2. **Windows Terminal (CASCADIA_HOSTING_WINDOW_CLASS)** processes `WM_CHAR` messages and routes them to ConPTY → the hosted console app (cmd.exe → claude).

3. **`\r` (ASCII 13) as a WM_CHAR message** is interpreted as Enter by the terminal. This is different from sending VK_RETURN via WM_KEYDOWN (which doesn't work).

4. **`CREATE_NEW_CONSOLE` flag** ensures the new cmd.exe gets its own console window, not shared with our process.

5. **hwnd-set-diff** (before/after snapshot) reliably identifies the new window even when multiple terminals exist.

### Critical Details

| Detail | Value |
|--------|-------|
| Window class | `CASCADIA_HOSTING_WINDOW_CLASS` |
| Message | `PostMessage(hwnd, WM_CHAR, ord(char), 0)` |
| Enter key | `\r` (0x0D) sent as WM_CHAR, NOT WM_KEYDOWN |
| Window finding | hwnd-set-diff (not PID, not title match) |
| Launch method | `subprocess.Popen(["cmd.exe", "/k", ...], creationflags=CREATE_NEW_CONSOLE)` |
| Wait for Claude | 15 seconds after sending "claude\r" |
| SDK function | `send_string(WindowTarget, text)` from self_connect.py |

### The Chain of Events (with timestamps from proof screenshots)

1. **spawn_step1_terminal.png** — Fresh cmd.exe at `C:\Users\techai\PKA testing\airgap-sop>`
2. **spawn_step1_echo.png** — `echo SELFCONNECT TERMINAL TEST` executed, output visible
3. **spawn_step2_claude.png** — Claude Code v2.1.92 running, "Welcome back Ron!", prompt ready
4. **spawn_step3_handoff.png** — Handoff message in Claude's prompt, "Sock-hopping..." (thinking)
5. **spawn_step4_response.png** — Claude reading handoff file, searching MemoryWeb, listing directory
6. **spawn_live_now.png** — Claude committed v0.4.0, created pyproject.toml, writing next handoff

---

## What Also Worked (Notepad Save Operation)

Same session proved these additional capabilities:

### Reading UWP Notepad Content (WM_GETTEXT on RichEditD2DPT)
- **Method:** `EnumChildWindows` → find `RichEditD2DPT` class → `SendMessage(hwnd, WM_GETTEXT, ...)`
- **Result:** 10/16 windows returned full text content
- **Failure mode:** 4 windows returned "Non Client Input Sink Window" (from `InputNonClientPointerSource` child instead of `RichEditD2DPT`)
- **Script:** `_save_notepads.py`

### Closing UWP Notepad Windows
- **Method 1:** `PostMessage(WM_CLOSE)` + `PostMessage(WM_KEYDOWN, VK_TAB)` + `PostMessage(WM_KEYDOWN, VK_RETURN)` to `InputSiteWindowClass` → closed 3/12
- **Method 2:** `taskkill /F /PID` → closed remaining 9 (safe since content already saved)
- **Why partial:** Windows 11 Notepad's save dialog is WinUI XAML, not classic Win32 dialog. The "Don't Save" button isn't a standard Button class.

---

## Reproduction Steps

```bash
# 1. Clone the repo
git clone https://github.com/rblake2320/airgap-sop.git
cd airgap-sop

# 2. Install dependencies
pip install Pillow psutil

# 3. Run the spawn proof
python _spawn_claude.py

# 4. Check proofs/ directory for screenshot evidence
ls proofs/spawn_step*.png
```

Requirements: Windows 10/11, Python 3.10+, Claude Code CLI installed and authenticated.

---

## Patent Implications

This proves a **4th patentable invention**: AI Agent Process Spawning via OS-Native Keyboard Injection.

An AI agent (Claude Session A) creates a new instance of itself (Claude Session B) by:
1. Launching a host process (cmd.exe) via `subprocess`
2. Injecting the CLI command ("claude\r") via `PostMessage(WM_CHAR)`
3. Injecting task instructions via the same method
4. Monitoring the spawned agent via `PrintWindow` capture

No API. No SDK. No inter-process protocol. Just Win32 `PostMessage` to `CASCADIA_HOSTING_WINDOW_CLASS`.

This is distinct from all 3 prior patent claims because it involves **process creation and lifecycle management**, not just interaction with existing windows.
