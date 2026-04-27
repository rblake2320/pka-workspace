#!/usr/bin/env python3
"""
AI Army Telegram Bridge -- bidirectional relay
~/ai-business/shared/chat/ <-> Telegram group

Chat -> Telegram: New .md files appear in chat dir -> parsed -> posted to group
Telegram -> Chat: Group messages -> written as .md files -> agents see them

Setup:
    1. Copy .env.example -> .env and fill in real values
    2. pip install python-telegram-bot watchdog python-dotenv
    3. python bridge.py
    4. Or: systemctl --user start ai-army-telegram-bridge
"""

import asyncio
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GROUP_ID_RAW = os.getenv("TELEGRAM_GROUP_ID", "")
CHAT_DIR = Path(os.getenv("CHAT_DIR", "/home/rblake2320/ai-business/shared/chat"))

# Files the bridge itself writes -- don't echo back to Telegram
BRIDGE_PREFIX = "_tg_"

# Filename patterns that are agent-internal noise -- don't relay to Ron's phone
NOISE_PATTERNS = (
    "_ALERT_",      # system threshold alerts (handled by monitor, not for Ron)
    "_HEARTBEAT_",  # status pings
    "_STATUS_",     # routine status posts
    "_DEBATE_",     # autonomous agent debates
    "_RESPONSE_",   # automated responses
    "Chat-Daemon_",
    "Spark1-Daemon_",
    "Spark2-Daemon_",
)

# Track filenames already seen so we never double-process
seen_files: set = set()

# Set once the event loop is running
_app = None
_loop = None


def _parse_group_id() -> int:
    raw = GROUP_ID_RAW.strip()
    if not raw or raw == "REPLACE_WITH_GROUP_CHAT_ID":
        raise ValueError("TELEGRAM_GROUP_ID not configured in .env")
    return int(raw)


def parse_chat_file(filepath: Path) -> dict:
    """Parse a .md chat file and return metadata dict, or None on failure."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    # Extract FROM field -- handles [FROM: X] and # [FROM: X] formats
    from_match = re.search(r'\[FROM:\s*([^\]]+)\]', content, re.IGNORECASE)
    from_agent = from_match.group(1).strip() if from_match else filepath.stem

    # Extract Subject line
    subject_match = re.search(r'\*\*Subject:\*\*\s*(.+)', content)
    subject = subject_match.group(1).strip() if subject_match else ""

    # Build body: skip header lines
    lines = content.split('\n')
    body_lines = []
    for line in lines:
        stripped = line.strip()
        if (stripped.startswith('#') or
                stripped.startswith('[FROM:') or
                stripped.startswith('[TO:') or
                stripped.startswith('**Time:') or
                stripped.startswith('**Subject:')):
            continue
        body_lines.append(line)

    body = '\n'.join(body_lines).strip()
    if len(body) > 800:
        body = body[:797] + "..."

    return {
        "from": from_agent,
        "subject": subject,
        "body": body,
        "filename": filepath.name,
    }


def write_chat_file(sender_name: str, message_text: str) -> Path:
    """Write an incoming Telegram message as a properly-formatted .md chat file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{BRIDGE_PREFIX}{timestamp}_ron-telegram.md"
    filepath = CHAT_DIR / filename

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")
    content = (
        f"# [FROM: Ron-Telegram] [TO: ALL]\n"
        f"**Time:** {now_str}\n"
        f"**Subject:** Message from Ron via Telegram\n\n"
        f"{message_text}\n"
    )
    filepath.write_text(content, encoding="utf-8")
    # Pre-register so the watcher does not echo it back
    seen_files.add(filename)
    return filepath


class ChatDirHandler(FileSystemEventHandler):
    """watchdog handler: fires when a new .md file appears in the chat dir."""

    def _handle(self, filepath: Path):
        if filepath.suffix != '.md':
            return
        if filepath.name in seen_files:
            return
        if filepath.name.startswith(BRIDGE_PREFIX):
            return  # Do not relay files the bridge itself created
        name_upper = filepath.name.upper()
        if any(pat.upper() in name_upper for pat in NOISE_PATTERNS):
            seen_files.add(filepath.name)  # mark seen so we don't recheck
            return  # agent-internal noise, not for Telegram

        seen_files.add(filepath.name)

        # Schedule async send on the running event loop (watchdog runs in a thread)
        if _loop is not None and _loop.is_running():
            asyncio.run_coroutine_threadsafe(
                _relay_to_telegram(filepath), _loop
            )

    def on_created(self, event):
        if event.is_directory:
            return
        self._handle(Path(event.src_path))

    def on_moved(self, event):
        # rsync renames temp files into place — triggers moved_to not created
        if event.is_directory:
            return
        self._handle(Path(event.dest_path))


async def _relay_to_telegram(filepath: Path) -> None:
    """Parse a chat file and post it to the Telegram group."""
    global _app
    if _app is None:
        return

    # Brief delay -- ensure file is fully written before we read it
    await asyncio.sleep(0.5)

    parsed = parse_chat_file(filepath)
    if not parsed:
        return

    from_agent = parsed["from"]
    subject = parsed["subject"]
    body = parsed["body"]

    # Build the Telegram message (plain text -- avoids MarkdownV2 escaping issues)
    if subject and body:
        msg = f"[{from_agent}] {subject}\n\n{body}"
    elif subject:
        msg = f"[{from_agent}] {subject}"
    elif body:
        msg = f"[{from_agent}]\n\n{body}"
    else:
        return  # Nothing useful to send

    if len(msg) > 4000:
        msg = msg[:3997] + "..."

    try:
        group_id = _parse_group_id()
        await _app.bot.send_message(chat_id=group_id, text=msg)
        print(f"[bridge] -> Telegram: [{from_agent}] {subject or '(no subject)'}")
    except Exception as e:
        print(f"[bridge] Failed to send to Telegram: {e}")


async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Incoming Telegram group message -> write to chat dir."""
    msg = update.message
    if not msg or not msg.text:
        return

    try:
        group_id = _parse_group_id()
    except ValueError:
        return
    if msg.chat.id != group_id:
        return

    # Ignore bot messages
    if msg.from_user and msg.from_user.is_bot:
        return

    sender = msg.from_user.first_name if msg.from_user else "Telegram"
    filepath = write_chat_file(sender, msg.text)
    print(f"[bridge] Telegram -> chat: {filepath.name}")


async def _preseed_seen_files() -> None:
    """Pre-populate seen_files with all existing .md files so we only relay NEW ones."""
    if CHAT_DIR.exists():
        count = 0
        for f in CHAT_DIR.iterdir():
            if f.suffix == '.md':
                seen_files.add(f.name)
                count += 1
        print(f"[bridge] Pre-seeded {count} existing files -- watching for NEW files only")


async def main() -> None:
    global _app, _loop

    if not BOT_TOKEN or BOT_TOKEN == "REPLACE_WITH_BOT_TOKEN":
        print("[bridge] ERROR: TELEGRAM_BOT_TOKEN not set in .env -- exiting")
        return

    try:
        group_id = _parse_group_id()
    except ValueError as e:
        print(f"[bridge] ERROR: {e} -- exiting")
        return

    print("[bridge] Starting AI Army Telegram Bridge")
    print(f"[bridge] Chat dir : {CHAT_DIR}")
    print(f"[bridge] Group ID : {group_id}")

    await _preseed_seen_files()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message)
    )
    _app = app
    _loop = asyncio.get_running_loop()

    observer = Observer()
    observer.schedule(ChatDirHandler(), str(CHAT_DIR), recursive=False)
    observer.start()
    print(f"[bridge] Watching {CHAT_DIR} for new .md files")

    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        print("[bridge] Telegram polling active -- bridge is live")

        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print("[bridge] Shutting down...")

        await app.updater.stop()
        await app.stop()
        await app.shutdown()

    observer.stop()
    observer.join()
    print("[bridge] Stopped")


if __name__ == "__main__":
    asyncio.run(main())
