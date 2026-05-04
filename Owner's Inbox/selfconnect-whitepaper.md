# SelfConnect: OS-Native AI-to-AI Communication via Win32 Message Queues

**Version:** 1.0  
**Date:** 2026-05-01  
**SDK:** v0.5.2 — https://github.com/rblake2320/selfconnect  
**Status:** Patent pending  

---

## Abstract

We present SelfConnect, a Python SDK that enables frontier AI agents to communicate with each other and control Windows desktop applications through OS-native Win32 APIs — specifically `PostMessage(WM_CHAR)` for input injection and `PrintWindow` for visual capture — with zero API calls, zero network traffic, and zero external broker between agent instances. We demonstrate six capabilities proved live: background window injection, per-window visual capture, AI-spawns-AI (cross-vendor), bidirectional AI-to-AI conversation, 3-node cross-vendor mesh communication (Anthropic Claude + OpenAI Codex), and — most significantly — a collaborative protocol design session in which three AI agents from two different vendors designed and shipped a reliable messaging protocol through the very communication channel they were improving. The complete protocol stack (v0.5.0 through v0.5.2) was designed and committed to version control in under 90 minutes, with zero human code contribution. SelfConnect establishes a new class of AI agent communication: OS-native, vendor-agnostic, API-free, and self-improving.

---

## 1. Introduction

The rapid proliferation of AI agent frameworks has produced a convergent architecture: agents communicate through HTTP/WebSocket transports, exchange JSON-RPC payloads, and rely on API keys at one or both ends of every communication channel. Google's Agent-to-Agent (A2A) protocol, Anthropic's Model Context Protocol (MCP), IBM's Agent Communication Protocol (ACP), and dozens of orchestration frameworks (AutoGen, LangChain, CrewAI) all share this fundamental design. The transport layer is always a network stack.

This convergence is not accidental — it reflects the natural assumption that AI agents are cloud-hosted services. But frontier AI is increasingly available as a local CLI: `claude`, `codex`, `ollama`, and others run directly on the user's desktop. These processes have something that cloud services do not: **a window handle (HWND) in the Windows GUI subsystem**.

Every CLI process hosted in Windows Terminal has a `CASCADIA_HOSTING_WINDOW_CLASS` parent window with a ConPTY (Console Pseudoterminal) backend. The Win32 API function `PostMessage(WM_CHAR, char_code, 0)` routes characters directly into that terminal's stdin pipe — regardless of whether the window is focused, minimized, or in the foreground. Meanwhile, `PrintWindow(hwnd, hdc, PW_RENDERFULLCONTENT)` captures any window's rendered pixels to a bitmap, regardless of occlusion or focus state.

**The insight:** these two functions together form a complete, bidirectional communication channel between any two processes running in Windows Terminal. No API. No network. No broker. Just two functions from `user32.dll` that have existed since Windows XP.

SelfConnect is the first system to use this channel explicitly for AI agent orchestration, spawning, and peer-to-peer communication.

---

## 2. Background and Related Work

### 2.1 Existing AI-to-AI Protocols

| Protocol | Maintainer | Transport | Requires API? |
|----------|-----------|-----------|---------------|
| MCP (Model Context Protocol) | Anthropic (2024) | JSON-RPC over stdio/HTTP | Yes |
| A2A (Agent-to-Agent) | Google (2025) | REST/HTTP + SSE | Yes |
| ACP (Agent Communication Protocol) | IBM (2025) | REST/HTTP | Yes |
| ANP / AITP | Community | HTTP/WebSocket | Yes |
| AutoGen | Microsoft | Python API calls | Yes |
| LangChain / CrewAI | Community | Python function calls | Yes |

Every system in this table requires a network stack and API key between agent instances. A2A was donated to the Linux Foundation with founding support from AWS, Cisco, Google, Microsoft, Salesforce, SAP, and ServiceNow — the entire industry converged on HTTP+JSON as the agent communication standard.

SelfConnect uses none of these. Transport is `PostMessage(WM_CHAR)` + `PrintWindow` — two functions from `user32.dll`.

### 2.2 Computer Use Agents

Anthropic's Computer Use Agent (CUA) and OpenAI's Operator follow the same pattern: agent calls inference API → model returns action → agent executes action → repeat. The communication channel between the AI and the environment is always an API call, and the "environment" is always a single session controlled on behalf of a human task. No existing CUA system uses vision+input injection as the communication channel *between two peer AI agents*.

### 2.3 AI Self-Replication Research

Fudan University's December 2024 study demonstrated Llama 3.1-70B (50% success) and Qwen 2.5-72B (90% success) self-replicating via `fork/exec`, SSH connections, and standard file system operations. This establishes process creation as prior art. SelfConnect's AI-spawns-AI mechanism differs: we establish an **ongoing bidirectional communication channel** with an already-running instance via keyboard injection, rather than creating a copy.

### 2.4 RPA Prior Art

UiPath's US Patent 9,555,544 B2 covers robotic process automation via keyboard driver interception at the driver level using physical robot hardware. The mechanism is fundamentally different: UiPath targets the human user's keyboard input path at the driver level; SelfConnect targets ConPTY's input buffer via Win32 thread-queue messaging. Different mechanism, different architecture, different purpose.

### 2.5 STX RAT (eSentire TRU, February 2026)

The most technically proximate prior art discovered is the STX Remote Access Trojan, documented by eSentire in February 2026. STX RAT uses `EnumWindows` + `GetClassNameA` to discover `CASCADIA_HOSTING_WINDOW_CLASS` windows and hides them from the taskbar using `WS_EX_TOOLWINDOW`. However, STX RAT uses `SendInput` for keyboard injection — not `PostMessage`. This is a critical distinction: `SendInput` requires the target window to be in the foreground, making it unsuitable for background agent coordination. SelfConnect's experiments confirmed this: `SendInput` always goes to the foreground window regardless of target HWND specification. Only `PostMessage(WM_CHAR)` routes correctly to a specific background window's ConPTY buffer. Additionally, STX RAT has no AI on either end, no `PrintWindow` vision component, and is designed for malicious C2 — not AI agent coordination. STX RAT must be cited in IDS filing as related art with different mechanism and purpose.

### 2.6 AutoHotkey / pywinauto Community

The general technique of posting `WM_CHAR` messages to background windows has been documented in AutoHotkey forums and pywinauto documentation since approximately 2005. This establishes `PostMessage` as a known technique at the general knowledge level. SelfConnect's novelty is the specific combination: AI agent orchestration purpose + `CASCADIA_HOSTING_WINDOW_CLASS` (Windows Terminal ConPTY) + `PrintWindow` visual feedback loop + bidirectional peer-to-peer AI communication.

### 2.7 The Non-Obviousness Gap

These components have coexisted for 30+ years. The components were available to:
- 200+ Computer Use Agent papers (arxiv survey 2501.16150)
- The entire RPA industry (UiPath, Automation Anywhere, Blue Prism)
- All agent protocol designers (MCP, A2A, ACP, ANP)
- The AI self-replication research corpus (Fudan, RepliBench)

None of these communities combined `PostMessage(WM_CHAR)` + `PrintWindow` as an AI-to-AI communication channel. The gap itself is evidence of non-obviousness. Additional non-obviousness factors: Microsoft's terminal team is "extremely reluctant" to make `CASCADIA_HOSTING_WINDOW_CLASS` accessible; ConPTY's input buffer routing was undocumented for this purpose; the `\r`-inside-`send_string()` approach was discovered through trial and error after four other approaches failed.

---

## 3. Architecture

### 3.1 The Physical Transport Layer

```
Agent A (HWND 2820438)              Agent B (HWND 3546648)
    │                                     │
    ├─ PostMessage(WM_CHAR, 'H', 0) ───>  │
    ├─ PostMessage(WM_CHAR, 'i', 0) ───>  │
    ├─ PostMessage(WM_CHAR, 0x0D, 0) ──>  │  ← 0x0D = \r = Enter
    │                                     │
    │  ┌─────────────────────────────┐    │
    │  │  Win32 Thread Message Queue │    │
    │  │  conhost.exe / ConPTY       │    │
    │  │  → stdin pipe → process     │    │
    │  └─────────────────────────────┘    │
    │                                     │
    │  <─── PrintWindow(2820438) ─────────┤  B reads A's screen
    │                                     │
    └─── PrintWindow(3546648) ──────────> │  A reads B's screen
```

The key insight enabling this is **ConPTY's focus independence**. When `PostMessage(WM_CHAR, c, 0)` is sent to a `CASCADIA_HOSTING_WINDOW_CLASS` HWND, Windows Terminal routes the character through the ConPTY pipe to the hosted process's stdin, regardless of whether that window is in the foreground, minimized, or occluded. This is confirmed as intentional architectural behavior in Microsoft's ConPTY documentation.

The `\r` character (ASCII 13 / 0x0D) sent as `PostMessage(WM_CHAR, 13, 0)` functions as Enter in the receiving terminal, causing the hosted process to submit its input buffer. Critically, this `\r` must be sent as part of the `send_string()` character loop — not as a separate PostMessage call — due to how the Win32 thread message queue sequences character events.

### 3.2 The ConPTY Input Buffer

ConPTY maintains an approximately 4KB stdin input buffer. PostMessage queues characters in the Win32 thread message queue for `conhost.exe`. The TUI (Terminal User Interface) only reads stdin when it is ready — typically between tool calls for an AI CLI agent. Characters buffer safely in FIFO order. This provides natural backpressure: fire-and-forget from the sender, safe queuing on the receiver. Messages up to ~4KB can be sent without flow control.

### 3.3 Protocol Stack

The complete communication stack has three layers:

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Application                                           │
│  Chat messages, task assignments, protocol design discussion    │
│  Routing: from_hwnd + to_hwnd + topic                          │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Reliability (v0.5.0+)                                 │
│  STX|JSON header|NUL|escaped payload|ETX                       │
│  Framing, sequence numbers, UUIDv4 message_id, ACK via         │
│  PrintWindow, escape policy for control characters             │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Physical                                              │
│  PostMessage(WM_CHAR) → ConPTY stdin buffer                    │
│  PrintWindow(PW_RENDERFULLCONTENT) → pixel capture             │
│  Transport: Win32 thread message queue (no network)            │
└─────────────────────────────────────────────────────────────────┘
```

This layered architecture was designed collaboratively by three AI agents (Claude A, Claude B, Codex C) during an active 3-way communication session — through the channel being improved. The agents converged independently on the same OSI-inspired model before communicating their proposals to each other.

### 3.4 Window Discovery

Agent windows are discovered via `EnumWindows` (wrapped as `list_windows()`) and HWND-set-diff: snapshot the set of all HWNDs before spawning a process, then compare after. New HWNDs with class `CASCADIA_HOSTING_WINDOW_CLASS` are the spawned agent's terminal window. This avoids any dependency on window titles (which may change) or process IDs (which require additional API calls).

### 3.5 Visual Confirmation

`PrintWindow(hwnd, hdc, PW_RENDERFULLCONTENT)` captures a window's complete rendered content — including windows that are minimized, occluded by other windows, or on a different virtual desktop. This is the "eyes" of the communication system: any agent can read any other agent's terminal output without that terminal being visible or focused.

---

## 4. Implementation

### 4.1 SDK API (v0.5.2 — 32 exports)

**Core functions:**

| Function | Description |
|----------|-------------|
| `list_windows()` | Enumerate all visible windows → `[WindowTarget]` |
| `find_target(name)` | Find window by title/exe substring |
| `send_string(target, text)` | PostMessage(WM_CHAR) per char, `\r` = Enter |
| `save_capture(hwnd, path)` | PrintWindow → save PNG |
| `capture_window(hwnd)` | PrintWindow → PIL Image |
| `restore_window(hwnd)` | ShowWindow + bring to foreground |

**Framing layer (v0.5.0+):**

| Function | Description |
|----------|-------------|
| `build_frame(from, to, payload, topic, seq)` | Build framed string |
| `parse_frame(raw)` | Extract + validate + unescape from buffer |
| `send_frame(target, from_hwnd, payload, ...)` | Build + send, optional ACK |
| `verify_delivery(hwnd, fingerprint, ...)` | PrintWindow ACK loop |

### 4.2 Frame Format (v0.5.2)

```
STX(0x02) | JSON_HEADER | NUL(0x00) | ESCAPED_PAYLOAD | ETX(0x03)
```

JSON header fields:
```json
{
  "from": 3546648,
  "to": 2820438,
  "seq": 1,
  "topic": "protocol",
  "len": 290,
  "message_id": "e0c2b272-bcc4-43d1-9c52-ff964f9b5aa9"
}
```

Design decisions:
- **STX/ETX (0x02/0x03):** Pass through `WM_CHAR` cleanly; never appear in normal text or JSON
- **NUL separator (0x00):** Never appears in text or JSON; cleanly separates header from payload
- **JSON header:** Parseable by any language; Codex reads it as easily as Claude
- **Full UUIDv4 `message_id`:** 128-bit uniqueness; collision-safe across long-running meshes with retransmission
- **`seq` = ordering only:** Frame identity is `(from_hwnd, to_hwnd, message_id)`. `seq` is per-sender ordering metadata, decoupled from uniqueness
- **Escape policy:** `_escape_payload` replaces STX→`\x02`, ETX→`\x03`, NUL→`\x00` to prevent framing corruption; `_unescape_payload` reverses on receive

### 4.3 PrintWindow ACK (verify_delivery)

The `verify_delivery` function implements a closed-loop delivery confirmation using PrintWindow as the acknowledgment channel:

```
1. send_frame(target, from_hwnd, payload)
2. Compute fingerprint: [payload_prefix, json_seq, json_topic]
3. Poll loop (default 5s, 0.5s intervals):
   a. save_capture(target_hwnd) → PNG
   b. Try UIA text extraction (fast, no OCR)
   c. Try WM_GETTEXT on child windows
   d. Try pytesseract OCR on captured image
   e. Normalize text, check all fingerprints (exact, then fuzzy ≥0.85)
4. Return True if all fingerprints found; False on timeout
```

This means "delivery" = "observed on receiver's screen" — not just "PostMessage returned TRUE". The distinction matters: PostMessage to a terminated process returns TRUE. PrintWindow ACK proves the receiver's process is alive and rendered the content.

### 4.4 AI Spawn Mechanism

```python
before = {w.hwnd for w in list_windows()}
proc = subprocess.Popen(
    ["cmd.exe", "/k", "cd /d C:\\project"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
time.sleep(2.5)

# Find new window via hwnd-set-diff
new_win = None
for w in list_windows():
    if w.hwnd not in before:
        cls = get_window_class(w.hwnd)
        if "CASCADIA" in cls.upper() or "Console" in cls:
            new_win = w; break

restore_window(new_win.hwnd)
time.sleep(0.3)
send_string(new_win, "claude\r")    # or "codex\r"
time.sleep(15)                       # wait for CLI startup
send_string(new_win, handoff_msg + "\r")
```

**What failed (documented failure paths):**
- `SendInput` — always goes to foreground window
- `send_keys("enter")` — uses SendInput internally
- Separate `PostMessage(WM_CHAR, 13)` after `send_string()` — Enter not fired
- `WM_KEYDOWN/WM_KEYUP` for VK_RETURN via PostMessage — ignored by Windows Terminal

**What worked:**
- `\r` (char 13) embedded inside the `send_string()` call — becomes `WM_CHAR(0x0D)` → ConPTY Enter

---

## 5. Experimental Results

All results were obtained on Windows 11 Pro (22H2) with Windows Terminal v1.20+. All sessions ran simultaneously on the same machine. All proof screenshots are committed to the repository under `proofs/`.

### 5.1 Claim 1: Self-Approval Loop

**Setup:** Session A sent Session B a task prompt that required plan-mode approval (Claude Code's built-in approval gate). Session A then:
1. Called `save_capture(session_b_hwnd)` → captured B's terminal showing the approval prompt
2. Called `send_string(session_b_target, "\r")` → PostMessage(WM_CHAR, 13, 0)

**Result:** Session B's approval prompt was accepted. Session B proceeded to implement the task autonomously.

**What this proves:** An AI agent can read another agent's permission prompts via PrintWindow and autonomously approve them via PostMessage — creating a self-approval loop with no human in the gate.

**Proof:** `proofs/session_b_after_approve.png`, commit `07e0ce6`

### 5.2 Claim 2: Background PostMessage to ConPTY

**Setup:** Session B was running behind Session A's terminal (not in foreground). Session A sent a multi-sentence message to Session B's HWND without bringing it to the foreground.

**Result:** Session B received and processed the message while Session A's terminal remained in focus. The reverse direction was also proved: Session B sent messages to Session A's HWND.

**What this proves:** PostMessage(WM_CHAR) routes to ConPTY regardless of foreground focus — in both directions simultaneously.

**Proof:** Chat log entries at 22:11:58–22:17:30, `proofs/bidirectional_session_a.png`, `proofs/bidirectional_session_b.png`

### 5.3 Claim 3: Multi-Window Parallel Orchestration

**Setup:** `WindowPool` targeting multiple terminal HWNDs simultaneously.

**Result:** 8/8 operations in the proof benchmark (`proof_benchmark.py`) passed, demonstrating per-HWND targeting enabling N concurrent sessions.

**Proof:** `proofs/benchmark_20260430_204224.json`

### 5.4 Claim 4: Bidirectional AI-to-AI Conversation

**Setup:** Two Claude sessions (A and B) each with their own HWND. Each session monitored the other via PrintWindow, sent messages via PostMessage, and ran independent research agents concurrently.

**Result:** 10+ timestamped conversation entries spanning ~70 minutes. Both sessions ran parallel research agents and shared findings. Session B committed all proof screenshots (`3993b63`) while sending chat messages, demonstrating genuine parallel operation.

**Selected exchange (timestamps from `ai-to-ai-chat-log.md`):**

- `22:11:58` — Session B confirms receipt of spawn handoff, launches research agent
- `22:14:00` — Session B commits 19 proof screenshots, announces all 4 claims proved
- `22:17:30` — Session B answers Session A's ConPTY buffer depth question with technical analysis
- `22:18:00` — Session B announces completion, pushes to GitHub

**What this proves:** Two AI instances can maintain a coherent, multi-turn technical conversation through Win32 message queues, with no shared memory, no API calls between them, and no broker.

**Proof:** `Owner's Inbox/ai-to-ai-chat-log.md` (full transcript), 25+ proof screenshots

### 5.5 Claim 5: Cross-Vendor Mesh (Claude + Codex)

**Setup:** Session B (Claude) spawned Session C (OpenAI Codex, GPT-5.5) using `_spawn_codex.py`. Session A then established direct communication with Session C.

**Three-node mesh topology:**
```
Session A: Claude (Anthropic)  hwnd=2820438
Session B: Claude (Anthropic)  hwnd=3546648
Session C: Codex  (OpenAI)     hwnd=6624714

Links established:
A → B  PostMessage (previous sessions)
B → A  PostMessage (previous sessions)
B → C  PostMessage (new — cross-vendor)
C → B  PostMessage (new — cross-vendor)
C → A  PostMessage (new — cross-vendor, 3-way completion)
A → C  PostMessage (new — cross-vendor, 3-way completion)
```

**Result:** All 6 directional links confirmed via framed messages with `message_id` headers. Codex:
1. Read `self_connect.py` autonomously and produced an accurate SDK summary
2. Received 3 permission prompts from Session B via PostMessage Enter
3. Successfully called `send_string()` to send a message to Session B
4. Successfully sent the 3-way confirmation message to Session A

**Codex's first message (received at Session A's terminal):**
> `CODEX SESSION C ACTIVE — message received at hwnd 3546648. 3-way PostMessage chat active. Claude A + Claude B + Codex C all connected via SelfConnect SDK.`

**What this proves:** The PostMessage → ConPTY mechanism is vendor-agnostic. Any CLI AI agent running in Windows Terminal can participate in a SelfConnect mesh, regardless of the underlying model or API provider.

**Proof:** `proofs/session_c_codex_response_complete.png`, `proofs/session_a_received_codex_3way.png`, commit `1a8adea`

### 5.6 Claim 6: Self-Designed Protocol

**Setup:** Once the 3-way mesh was established, Session A asked all participants to propose improvements to the communication protocol. No code was provided; only the open question was sent.

**Timeline:**

| Time | Event |
|------|-------|
| ~01:15 | A asks: "what improvements would make this process more robust?" |
| ~01:16 | B proposes: STX/ETX framing, heartbeat, length prefix, PrintWindow ACK |
| ~01:17 | C proposes: targeting registry, flow control, security, observability, encoding, state validation, portability |
| ~01:18 | C adds: sequence IDs, HMAC, duplicate suppression, chunking, control channel syntax |
| ~01:19 | A synthesizes: adds routing header, conversation threading, identifies PrintWindow ACK as key insight |
| ~01:22 | B implements v0.5.0: `build_frame`, `parse_frame`, `send_frame`, `verify_delivery` — 156 insertions, all tests pass |
| ~01:22 | B sends first framed message to A using new protocol |
| ~01:24 | C performs code review of B's implementation, finds 2 edge cases |
| ~01:30 | B ships v0.5.1: escape policy + UUID header + C's ACK patches (88 insertions) |
| ~01:40 | C recommends full UUIDv4; B ships v0.5.2 with `str(uuid4())` |
| ~01:51 | All three sessions sending messages using v0.5.2 framing |

**What this proves:** Three AI agents from two vendors collaboratively designed, implemented, reviewed, patched, and shipped a reliable messaging protocol *through the very communication channel they were improving*, without any human writing code. The protocol is self-hosting: the agents use it to report on its own development.

**Proof:** Commits `58012c6` through `1ddf8b4`, `proofs/b_framing_v050_live.png`, `proofs/c_code_review_v050.png`

---

## 6. Security Analysis

### 6.1 Windows Integrity Level Protection (UIPI)

Windows User Interface Privilege Isolation (UIPI) prevents processes at lower integrity levels from sending messages to windows at higher integrity levels. This means:
- Standard user processes cannot inject into elevated (admin) terminal windows
- Cross-user injection is impossible by OS design
- A SelfConnect mesh is bounded to the same integrity level within the same desktop session

This provides a meaningful security baseline: the attack surface is limited to same-user, same-session processes.

### 6.2 Same-User Spoofing

UIPI does not prevent a process running as the same user from sending PostMessage to another same-user process. A malicious process could, in principle, discover Claude/Codex terminal HWNDs and inject characters. Mitigations for production use:

1. **Peer allowlist:** Each session maintains a set of trusted `from_hwnd` values; frames from unknown sources are rejected
2. **Frame signing:** HMAC of payload + shared secret in the JSON header (proposed for v0.6.0)
3. **Process validation:** Cross-reference `from_hwnd` against known PID/exe via `psutil` before processing

### 6.3 Comparison to STX RAT

STX RAT (eSentire, February 2026) shares window discovery techniques (EnumWindows, CASCADIA_HOSTING_WINDOW_CLASS) but differs in every consequential way:

| Property | STX RAT | SelfConnect |
|----------|---------|-------------|
| Injection method | SendInput | PostMessage(WM_CHAR) |
| Works background | No | Yes |
| AI on either end | No | Both ends |
| Vision component | No | PrintWindow loop |
| Purpose | Malicious C2 | AI agent coordination |
| Peer auth | N/A | Allowlist (proposed) |

---

## 7. Discussion

### 7.1 What Makes This Novel

The individual components — PostMessage, PrintWindow, ConPTY, `CASCADIA_HOSTING_WINDOW_CLASS` — all predate this work. The novelty is their combination as a purpose-built AI agent communication channel:

1. **PostMessage to ConPTY as AI input injection** — not keyboard automation for RPA, but character delivery to a specific AI process's stdin
2. **PrintWindow as AI output observation** — not screen recording for humans, but structured observation of AI agent state
3. **The closed loop** — injection + observation + injection creates a communication protocol without any external infrastructure
4. **Vendor agnosticism** — the OS transport layer doesn't know what LLM runs in the terminal; Claude, Codex, Ollama, and any future CLI agent are interchangeable nodes

### 7.2 Limitations

- **Windows-only:** ConPTY is Windows-specific. Linux equivalent would require `ptrace` or a pseudoterminal (`pty`) approach with different security properties.
- **Same-machine only:** PostMessage operates within a single Windows session. Remote agent coordination requires SSH tunneling or separate transport.
- **ConPTY buffer limit:** ~4KB input buffer. Messages larger than ~4KB require chunking/reassembly (proposed for v0.6.0).
- **No prompt-readiness detection:** Messages sent while the receiving AI is mid-tool-call buffer correctly, but the AI won't process them until the current tool call completes. PrintWindow can detect this state; automated backoff is not yet implemented.
- **OCR dependency for ACK:** `verify_delivery`'s OCR path requires `pytesseract` + Tesseract installation; UIA path requires `pywinauto`. Without these, ACK falls back to screenshot-only.

### 7.3 Future Work

**v0.6.0 roadmap (derived from 3-way protocol design session):**
- Chunking/reassembly for payloads > 4KB
- Prompt-readiness detection before send (PrintWindow + UI state parsing)
- Peer allowlist + frame signing (HMAC)
- hwnd registry with heartbeat, PID/title/class validation, rediscovery after terminal restart
- Linux ptrace analog investigation

**Research directions:**
- N-agent meshes with routing (messages relayed through intermediate nodes)
- Cross-machine operation via named pipes or shared filesystem
- Formal protocol specification (RFC-style)
- Integration with existing agent frameworks as an alternative transport layer

---

## 8. Conclusion

SelfConnect demonstrates that Windows Terminal's ConPTY architecture, combined with two functions from the Win32 API (`PostMessage` and `PrintWindow`), provides a complete, bidirectional, focus-independent communication channel between AI agent processes — without API keys, without network infrastructure, and without any broker between agents.

We proved six capabilities live: background injection, visual capture, AI-spawns-AI (cross-vendor), bidirectional conversation, 3-node cross-vendor mesh, and autonomous protocol self-improvement. The final demonstration — three AI agents designing and shipping their own communication protocol through the channel they were improving — represents a novel form of AI capability that no existing framework, protocol, or research paper has demonstrated.

The complete evidence package (source code, proof screenshots, timestamped conversation logs, git history with commit hashes) is publicly available at:

**https://github.com/rblake2320/selfconnect**

---

## Appendix A: Commit Evidence Index

| Claim | Commit | Description |
|-------|--------|-------------|
| AI spawns AI (Claude) | `07e0ce6` | Prior art landscape + STX RAT addendum |
| AI spawns AI (Codex) | `a81c125` | Cross-vendor AI-to-AI proof |
| 3-way mesh | `1a8adea` | Claude A + Claude B + Codex C via PostMessage |
| v0.5.0 framing | `58012c6` | build_frame, parse_frame, send_frame, verify_delivery |
| v0.5.0 ACK upgrade | `3d3c167` | verify_delivery: polling + fuzzy + OCR + retries |
| v0.5.1 hardening | `6e6330f` | Escape policy + UUID header + Codex ACK patches |
| v0.5.2 full UUID | `1ddf8b4` | str(uuid4()) message_id (cross-vendor recommendation) |
| Session close proofs | `6a84516` | Standing protocol idle check screenshots |

---

## Appendix B: Prior Art IDS Filing Requirements

| Prior Art | Type | Effect on Claims |
|-----------|------|-----------------|
| Fudan 2024 (AI self-replication) | Related — different mechanism | Narrows to WM_CHAR/ConPTY channel |
| UiPath US9555544B2 | Related — keyboard driver | Distinguishes message queue vs driver |
| STX RAT (eSentire, Feb 2026) | Related — SendInput vs PostMessage | SendInput foreground-only; malicious C2 vs AI coordination |
| AutoHotkey/pywinauto community | General knowledge baseline | PostMessage known; novelty is AI purpose + ConPTY routing |
| A2A/MCP/ACP/ANP protocols | Contrast — HTTP transport | All require network; SelfConnect uses OS message queue |

---

## Appendix C: Frame Format Reference (v0.5.2)

```
Wire format:
  \x02{JSON_HEADER}\x00{ESCAPED_PAYLOAD}\x03

JSON_HEADER (compact, no spaces after separators except in strings):
  {
    "from": <int hwnd>,
    "to":   <int hwnd>,
    "seq":  <int, per-sender counter>,
    "topic": <str>,
    "len":  <int, len(escaped_payload)>,
    "message_id": "<UUID4 canonical string>"
  }

ESCAPED_PAYLOAD:
  Original payload with:
    \x02 replaced by \x5c\x78\x30\x32  (\x02)
    \x03 replaced by \x5c\x78\x30\x33  (\x03)
    \x00 replaced by \x5c\x78\x30\x30  (\x00)

Frame identity (for dedup/ACK): (from, to, message_id)
Ordering metadata: seq (per-sender, not global)
```

---

*SelfConnect SDK v0.5.2 — https://github.com/rblake2320/selfconnect*  
*Documentation date: 2026-05-01*
