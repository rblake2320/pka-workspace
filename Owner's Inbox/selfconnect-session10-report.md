# SelfConnect Session 10 Report
**Date:** 2026-05-02  
**Commit:** `6458650` → https://github.com/rblake2320/selfconnect

---

## What Was Proved

### Browser Automation via SelfConnect — Zero External Dependencies

Conducted a full live test against Perplexity AI using nothing but Win32 primitives:

| Step | Method | Notes |
|------|--------|-------|
| Screen capture | `PIL.ImageGrab.grab(bbox=window_rect, all_screens=True)` | Only method that works on Chrome — GPU compositing blocks both `BitBlt` and `PrintWindow(PW_RENDERFULLCONTENT)` |
| Click | `ctypes SetCursorPos() + mouse_event(MOUSEEVENTF_LEFTDOWN/UP)` | Raw Win32, no WebDriver, no CDP |
| Text input | Write → temp file → PowerShell `Set-Clipboard` → `keybd_event(Ctrl+V)` | Avoids `WM_CHAR` Unicode encoding issues |
| Submit | `keybd_event(VK_RETURN)` | |

**No Playwright. No Selenium. No browser extension. No MCP. No API calls. No WebDriver.**

### CAPTCHA Test Results

| Test | Correct Answer | Session A Answer | Score |
|------|---------------|-----------------|-------|
| CAPTCHA 1 | R7X4P2 | Skipped (answer visible in Perplexity message) | N/A |
| CAPTCHA 2 | 9KMBW3 | 9KMBW | 5/6 (6th char cut off in frame) |
| CAPTCHA 3 | J4NQ8 | J4NQ8 | **100% — Perfect** |

Perplexity's verdict on CAPTCHA 3: **"Perfect — 100% correct. J4NQ8 is exactly right."**

---

## Other Wins

### Watchdog Interleaving Bug — Fixed
- Root cause: 6+ duplicate `game_watchdog.py` processes all running concurrently, each sending `WM_CHAR` one character at a time → characters from different processes interleaved into gibberish
- Fix: lockfile singleton (`C:/Users/techai/tmp/watchdog.lock`) — startup checks if previous PID is alive, exits if so
- Also: interval increased 30s → 60s so Sonnet has time to think before next nudge

### F2 Model Switch — Haiku → Sonnet
- `/model claude-sonnet-4-6` injected via `send_string(F2_win)`
- Confirmed "Set model to Sonnet 4.6" in terminal capture

### Game Status
- **ON HOLD per Ron** — Dark War Survival paused, all watchdogs stopped

---

## Files Changed

| File | Change |
|------|--------|
| `selfconnect/game_watchdog.py` | Lockfile singleton, interval 30→60s, atexit cleanup |
| `selfconnect/proofs/checkpoint_A_s10_browser_automation.json` | Session 10 checkpoint |

---

## New Patent Claim

**GPU-compositing-aware screen capture for browser automation** — `PIL.ImageGrab` as the only viable capture path when the target window uses hardware acceleration (Chrome, Edge, most modern browsers). Neither `BitBlt` nor `PrintWindow(PW_RENDERFULLCONTENT)` returns non-zero pixels for these windows. `ImageGrab` works by reading from the desktop compositor directly.

This extends the SelfConnect patent claim from "Win32 terminal window automation" to **"any visible window including GPU-composited browser windows."**

---

## Session 11 Queue

1. `v0.9.1`: PEER_FROZEN detection in WatchdogLoop (detect accept-edits TUI deadlock)
2. Full live MigrationCoordinator proof from Spark-2 side (trigger via Hub CMD)
3. C restart with `codex --full-auto`
4. Resume game with Sonnet when Ron says go
