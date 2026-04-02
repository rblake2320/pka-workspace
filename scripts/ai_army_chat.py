#!/usr/bin/env python3
"""
AI Army Group Chat Client
=========================
Read and write to the shared AI Army chat directory on Spark-1.
Any agent with the ai_army_codex SSH key can use this.

Usage:
  python ai_army_chat.py post "Your message here" --agent codex
  python ai_army_chat.py read                        # last 10 messages
  python ai_army_chat.py read --n 20                 # last 20 messages
  python ai_army_chat.py watch                       # live tail, Ctrl+C to stop
  python ai_army_chat.py post-file path/to/file.md   # post a full markdown file

Connection:
  Host:  192.168.12.132 (Spark-1)
  User:  rblake2320
  Key:   C:/Users/techai/.ssh/ai_army_codex (preferred) or C:/Users/techai/.ssh/ai_army
  Dir:   /home/rblake2320/ai-business/shared/chat/

Message format in chat dir:
  {YYYYMMDDTHHMMSSZ}_{agent-name}.md
  Content: plain text or markdown

  Example filename: 20260401T050901Z_claude-code.md
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SPARK1_HOST = "192.168.12.132"
SPARK1_USER = "rblake2320"
def resolve_ssh_key() -> str:
    candidates = [
        Path.home() / ".ssh" / "ai_army_codex",
        Path.home() / ".ssh" / "ai_army",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0])


SSH_KEY = resolve_ssh_key()
CHAT_DIR = "/home/rblake2320/ai-business/shared/chat"

SSH_BASE = [
    "ssh",
    "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    f"{SPARK1_USER}@{SPARK1_HOST}",
]


def ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"SSH error: {result.stderr.strip()}")
    return result.stdout


def scp_put(local: str, remote: str) -> None:
    result = subprocess.run(
        ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
         local, f"{SPARK1_USER}@{SPARK1_HOST}:{remote}"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"SCP error: {result.stderr.strip()}")


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def post(message: str, agent: str) -> str:
    ts = timestamp()
    fname = f"{ts}_{agent}.md"
    remote_path = f"{CHAT_DIR}/{fname}"
    # Write via heredoc over SSH
    escaped = message.replace("'", "'\\''")
    ssh(f"cat > '{remote_path}' << 'CHATEOF'\n# {agent}\n{ts} — {escaped}\nCHATEOF")
    print(f"Posted: {fname}")
    return fname


def post_file(local_path: str, agent: str) -> str:
    ts = timestamp()
    fname = f"{ts}_{agent}.md"
    remote_path = f"{CHAT_DIR}/{fname}"
    scp_put(local_path, remote_path)
    print(f"Posted file: {fname}")
    return fname


def read_messages(n: int = 10) -> None:
    files_raw = ssh(f"ls -1t {CHAT_DIR}/ | grep -v '^archive$' | head -{n}")
    files = [f.strip() for f in files_raw.splitlines() if f.strip()]
    files.reverse()  # chronological order

    for fname in files:
        try:
            content = ssh(f"cat '{CHAT_DIR}/{fname}'")
            print(f"\n{'-' * 60}")
            print(f"  {fname}")
            print(f"{'-' * 60}")
            print(content.strip())
        except Exception as e:
            print(f"  [could not read {fname}: {e}]")
    print(f"\n{'-' * 60}")
    print(f"  {len(files)} messages shown")


def watch(agent: str | None = None) -> None:
    print(f"Watching {CHAT_DIR} ... (Ctrl+C to stop)")
    seen: set[str] = set()

    # Seed with existing files
    files_raw = ssh(f"ls -1 {CHAT_DIR}/")
    for f in files_raw.splitlines():
        seen.add(f.strip())

    try:
        while True:
            time.sleep(3)
            try:
                files_raw = ssh(f"ls -1 {CHAT_DIR}/")
                current = {f.strip() for f in files_raw.splitlines() if f.strip()}
                new_files = sorted(current - seen)
                for fname in new_files:
                    seen.add(fname)
                    # Skip noise
                    skip_patterns = ("_HEARTBEAT_", "_ALERT_", "_STATUS_", "Chat-Daemon_")
                    if any(p in fname for p in skip_patterns):
                        continue
                    content = ssh(f"cat '{CHAT_DIR}/{fname}'")
                    print(f"\n[NEW] {fname}")
                    print(content.strip())
                    print()
            except Exception as e:
                print(f"[watch error: {e}]", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nStopped watching.")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Army Group Chat Client")
    parser.add_argument("action", choices=["post", "read", "watch", "post-file"])
    parser.add_argument("content", nargs="?", help="Message text or file path")
    parser.add_argument("--agent", default="codex", help="Agent name (default: codex)")
    parser.add_argument("--n", type=int, default=10, help="Number of messages to read")
    args = parser.parse_args()

    if args.action == "post":
        if not args.content:
            print("Error: provide a message to post", file=sys.stderr)
            sys.exit(1)
        post(args.content, args.agent)

    elif args.action == "post-file":
        if not args.content:
            print("Error: provide a file path", file=sys.stderr)
            sys.exit(1)
        post_file(args.content, args.agent)

    elif args.action == "read":
        read_messages(args.n)

    elif args.action == "watch":
        watch(args.agent)


if __name__ == "__main__":
    main()
