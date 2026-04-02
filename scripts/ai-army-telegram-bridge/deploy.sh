#!/bin/bash
# deploy.sh -- Run this on Spark-1 after filling in .env
# Usage: bash deploy.sh

set -e

BRIDGE_DIR="$HOME/ai-army-telegram-bridge"
cd "$BRIDGE_DIR"

echo "=== AI Army Telegram Bridge Deploy ==="

# 1. Create virtualenv if missing
if [ ! -d "venv" ]; then
    echo "Creating virtualenv..."
    python3 -m venv venv
fi

# 2. Install dependencies
echo "Installing dependencies..."
venv/bin/pip install -q --upgrade pip
venv/bin/pip install -q "python-telegram-bot>=21.0" watchdog python-dotenv

# 3. Verify .env exists and has real values
if [ ! -f ".env" ]; then
    echo "ERROR: .env not found. Copy .env.example to .env and fill in values."
    exit 1
fi
if grep -q "REPLACE_WITH_BOT_TOKEN" .env; then
    echo "ERROR: TELEGRAM_BOT_TOKEN still has placeholder value in .env"
    exit 1
fi
if grep -q "REPLACE_WITH_GROUP_CHAT_ID" .env; then
    echo "ERROR: TELEGRAM_GROUP_ID still has placeholder value in .env"
    exit 1
fi

# 4. Install systemd service
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"
cp ai-army-telegram-bridge.service "$SERVICE_DIR/"
systemctl --user daemon-reload
systemctl --user enable ai-army-telegram-bridge.service
systemctl --user start ai-army-telegram-bridge.service

echo ""
echo "=== Deploy complete ==="
echo "Check status: systemctl --user status ai-army-telegram-bridge"
echo "Watch logs:   journalctl --user -u ai-army-telegram-bridge -f"
