#!/usr/bin/env bash
# Data Flywheel setup on Spark-1
# Run as: bash /tmp/data_flywheel_setup.sh
set -euo pipefail

FLYWHEEL_DIR="/home/rblake2320/data-flywheel"
VENV_DIR="$FLYWHEEL_DIR/.venv"

echo "=== Data Flywheel Setup ==="
echo "Target: $FLYWHEEL_DIR"

# 1. Clone the blueprint
if [ -d "$FLYWHEEL_DIR" ]; then
    echo "[SKIP] Already cloned at $FLYWHEEL_DIR"
else
    git clone https://github.com/NVIDIA-AI-Blueprints/data-flywheel "$FLYWHEEL_DIR"
    echo "[OK] Cloned data-flywheel"
fi

# 2. Python venv
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "[OK] venv created"
fi

source "$VENV_DIR/bin/activate"

# 3. Install deps (skip GPU-heavy ones for now, just wiring layer)
pip install --quiet psycopg2-binary pandas numpy tqdm pyyaml requests 2>&1 | tail -3
echo "[OK] base deps installed"

echo ""
echo "=== Setup complete ==="
echo "Next: python3 $FLYWHEEL_DIR/army_os_wiring.py --dry-run"
