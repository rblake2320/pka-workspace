# Approval Automation — Design Brief
**Prepared by:** FORGE/NOVA  
**Date:** 2026-05-04  
**Session:** 12 (post-compaction)

---

## Summary

Three related ideas, researched and designed:

1. **Partner Agent** — a local companion process that watches your Claude Code terminal and auto-approves prompts you would have approved anyway
2. **SaaS Approval Widget** — a standalone product for external users to "walk away all day" (does NOT touch your current setup)
3. **Telegram Bridge** — when Claude needs a yes/no, it pings your phone; you reply; Claude continues

**Your current setup is untouched by all three.** Each is a separate, opt-in tool.

---

## How Claude Code Approvals Actually Work

When a tool is NOT in your `settings.local.json` `permissions.allow` list, Claude Code pauses and prints an interactive prompt in the terminal:

```
Do you want to proceed?
❯ Yes
  No
  Always allow "Bash(curl:*)" for this project
  Never allow
```

Claude Code waits for your keypress (`y`/`n`/arrow keys). This is standard terminal stdin input.

**Key fact:** There is NO `PreToolUse` hook in Claude Code today. Hooks only fire *after* execution. So programmatic approval must come from OUTSIDE the hook system — either via:
- Adding to the `allow` list (static, what your setup does), OR
- Injecting the keypress into the terminal from another process (dynamic, what these tools do)

**SelfConnect's `send_string(hwnd, "y\r")` is exactly the right primitive for this.** PostMessage(WM_CHAR) delivers the keypress directly to Windows Terminal's input buffer without needing focus.

---

## Concept 1: Partner Agent (Local Auto-Approval)

A lightweight Python script you run alongside Claude Code. It monitors the terminal and injects approvals based on configurable rules.

### How It Works

```
Claude Code terminal
      │
      ├── PrintWindow() → PIL image (or UIA text)
      │        every 2 seconds
      │
      ├── Detect approval prompt (regex on text)
      │        "Do you want to proceed?" / "Allow ..." 
      │
      ├── Check rules engine
      │        allow_patterns: ["npm:*", "git:*", "node:*"]
      │        deny_patterns:  ["rm:*", "curl:*"]
      │        default: "ask_telegram" or "approve_all" or "deny"
      │
      └── Inject response
               send_string(hwnd, "y\r")  # approve
               send_string(hwnd, "n\r")  # deny
               → Telegram notification  # ask user
```

### Implementation

```python
# approval_partner.py — ~150 lines
from self_connect import list_windows, get_text_uia, send_string, capture_window
import re, time, fnmatch

APPROVAL_PATTERNS = [
    r"Do you want to proceed",
    r"Allow.*for this project",
    r"Yes.*No.*Always allow",
]

ALLOW_RULES = ["npm:*", "git:*", "node:*", "python:*", "pip:*"]  # always approve
DENY_RULES  = ["rm:*", "rmdir:*", "curl:*"]                       # always deny

def find_claude_terminal():
    for w in list_windows():
        if "claude" in w.title.lower() or "cmd" in w.exe_name.lower():
            return w
    return None

def has_approval_prompt(hwnd):
    text = get_text_uia(hwnd) or ""
    return any(re.search(p, text, re.IGNORECASE) for p in APPROVAL_PATTERNS)

def extract_tool_name(text):
    m = re.search(r'Bash\(([^)]+)\)', text)
    return m.group(0) if m else None

def should_approve(tool_name):
    if any(fnmatch.fnmatch(tool_name, p) for p in DENY_RULES):
        return False
    if any(fnmatch.fnmatch(tool_name, p) for p in ALLOW_RULES):
        return True
    return None  # unknown — escalate

def run():
    print("[partner] Watching for Claude Code approval prompts...")
    while True:
        win = find_claude_terminal()
        if win and has_approval_prompt(win.hwnd):
            text = get_text_uia(win.hwnd)
            tool = extract_tool_name(text)
            decision = should_approve(tool) if tool else None
            
            if decision is True:
                send_string(win, "y\r")
                print(f"[partner] Auto-approved: {tool}")
            elif decision is False:
                send_string(win, "n\r")
                print(f"[partner] Auto-denied: {tool}")
            else:
                # Unknown tool — trigger Telegram escalation
                notify_telegram(text)
                print(f"[partner] Escalated to Telegram: {tool}")
            time.sleep(3)  # cooldown after action
        time.sleep(2)

if __name__ == "__main__":
    run()
```

### What This Costs to Build
- **~150 lines** on top of existing SelfConnect
- No new dependencies beyond `self_connect`
- Runs as a background Python script — start it, minimize it, forget it

### NOT touching your setup
- Zero changes to your `settings.local.json`
- Zero changes to your `permissions.allow` list
- Zero changes to your hooks
- Can be started/stopped independently at any time

---

## Concept 2: SaaS Approval Widget (External Product)

A **standalone Windows installer** that wraps any Claude Code installation with mobile-friendly approvals. Target audience: developers who run long Claude Code sessions and don't want to babysit approvals.

### Product: "ClaudeGo" (working name)

**User story:** Install it once, enter your phone number (or Telegram handle). Walk away. When Claude needs a yes/no, your phone buzzes. Tap Approve or Deny. Claude continues.

### Architecture

```
[ClaudeGo Tray App]
      │
      ├── Terminal Monitor Thread
      │        SelfConnect scan → detect approval prompt
      │
      ├── Rule Engine (configurable via settings UI)
      │        Always approve: npm, git, python...
      │        Always deny: rm, curl to external URLs...
      │        Ask phone: everything else
      │
      ├── Mobile Notification Gateway
      │        Option A: Telegram bot (user connects their own bot)
      │        Option B: ClaudeGo cloud relay (managed SaaS)
      │        Option C: ntfy.sh / Pushover webhook (open-source)
      │
      └── Response Handler
               Poll for reply → inject into terminal
```

### Business Model
- **Free tier:** 20 approvals/day, basic rules engine
- **Pro ($9/mo):** Unlimited approvals, mobile app, audit log
- **Team ($29/mo):** Multiple developers, shared rule sets, approval history

### What Makes This Distinct (vs just editing `settings.local.json`)
1. **Dynamic rules** — not just allow/deny lists, but conditional logic ("approve git push only if no --force flag")
2. **Audit trail** — every auto-approval logged with timestamp, tool, args
3. **Mobile UI** — you see WHAT was approved, not just a notification
4. **Works with any Claude Code project** — no per-project config changes
5. **Team-aware** — know what your team's Claude agents are doing

### What Needs to Be Built
| Component | Effort |
|-----------|--------|
| Terminal monitor (SelfConnect-based) | 1 day |
| Rules engine + settings UI | 2 days |
| Telegram integration (see Concept 3) | 1 day |
| System tray app (Windows) | 1 day |
| Installer (NSIS or WiX) | 1 day |
| Cloud relay (optional for managed tier) | 1 week |

**MVP = 5 days. Ship the terminal monitor + Telegram integration first.**

---

## Concept 3: Telegram Bridge (Approval via Phone)

The existing `scripts/ai-army-telegram-bridge/bridge.py` is a **file watcher for a Linux chat directory** — it won't work for Windows terminal injection. But the Telegram Bot API code in it is reusable.

### What's Already Built
- ✅ Bot token + group ID config pattern (`.env.example`)
- ✅ `python-telegram-bot` integration
- ✅ Bidirectional: files → Telegram AND Telegram → files
- ✅ Noise filtering (ignore heartbeats, status pings)

### What's Missing for Approval Use Case
- ❌ Windows terminal monitoring (no file watcher equivalent)
- ❌ Prompt detection (no approval pattern matching)
- ❌ Terminal injection on response (no `send_string` usage)
- ❌ Structured approve/deny UI (just plain text messages now)

### Approval-Specific Telegram Bridge Design

```python
# claude_approval_telegram.py — new file, ~200 lines

# ON APPROVAL PROMPT DETECTED:
# → Send to Telegram:
"""
⚠️ Claude Code needs approval

Tool: Bash(npm install react)
Project: C:/Users/techai/my-project
Time: 2026-05-04 14:32:11

Reply:
  ✅ yes — approve
  ❌ no  — deny
  🔁 always — add to allow list
"""

# ON TELEGRAM REPLY:
# → Parse response text ("yes", "y", "✅")
# → inject: send_string(claude_hwnd, "y\r")
# → Confirm: send back "✅ Approved — Claude is continuing"
```

### Bot Setup (One-Time)
1. Message @BotFather on Telegram → `/newbot` → copy token
2. Add bot to a private channel (just you)
3. Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
4. `python claude_approval_telegram.py` — runs in background

### Message Flow

```
Claude pauses for approval
        ↓
claude_approval_telegram.py detects prompt
        ↓
Sends Telegram message to your phone
        ↓
You reply "yes" from anywhere in the world
        ↓
Script polls Telegram API (every 2s), gets "yes"
        ↓
send_string(claude_hwnd, "y\r")
        ↓
Claude continues working
        ↓
Telegram confirmation: "✅ Approved — Claude continuing"
```

**Latency: 5-15 seconds** (Telegram poll interval + your response time)

---

## Recommendation: Build Order

**Week 1 — Build the core (for us, then productize)**
1. `selfconnect/approval_partner.py` — terminal monitor + local rule engine
2. `selfconnect/approval_telegram.py` — Telegram notification + response handler
3. Test: start both, walk away, watch Claude work unattended

**Week 2 — Package as SaaS**
1. Windows tray app wrapping both scripts
2. Web-based settings UI (FastAPI + simple HTML)
3. Telegram bot setup wizard (guided, no manual `.env` editing)

**This is buildable NOW.** Every piece exists:
- Terminal monitoring: `get_text_uia(hwnd)` (SelfConnect)
- Prompt detection: regex on UIA text
- Terminal injection: `send_string(hwnd, "y\r")` (SelfConnect)
- Telegram: `bridge.py` has working bot integration code
- Zero changes to your current setup required

---

## Files That Would Be Created (None Touch Your Config)

```
selfconnect/
  approval_partner.py      — local auto-approval daemon
  approval_telegram.py     — Telegram escalation bridge
  tests/
    test_approval_partner.py

Owner's Inbox/
  approval-automation-design-brief.md   ← this file
```

**Your `settings.local.json`, `permissions.allow`, and hooks are not touched.**

---

## One Sentence Per Concept

| Concept | One Sentence |
|---------|-------------|
| Partner Agent | A Python script that reads your Claude terminal every 2 seconds and types "y" for tools you'd always approve anyway |
| SaaS Widget | A system tray app that routes Claude's approval prompts to your phone, lets you tap Approve/Deny, and injects the answer back |
| Telegram Bridge | An adaptation of the existing `bridge.py` — detects approval prompts, sends them to Telegram, waits for your reply, injects it |
