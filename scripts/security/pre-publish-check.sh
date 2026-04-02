#!/usr/bin/env bash
# =============================================================================
# pre-publish-check.sh
# Pre-publish safety gate for npm packages
#
# Blocks publication if any of the following are true:
#   - .map files are in the publish file list
#   - node_modules would ship
#   - .env files would ship
#   - package.json is missing a "files" field (means everything ships)
#
# Root cause of the Anthropic Claude Code source map incident (2026-03-31):
#   Bun generates source maps by default. The built package included a 59.8MB
#   .map file exposing 512,000 lines of proprietary TypeScript source code.
#   This check would have caught it before publish.
#
# Usage:
#   bash pre-publish-check.sh [/path/to/package/dir]
#   (defaults to current directory if no arg given)
#
# Install as pre-publish hook:
#   Add to package.json scripts: "prepublishOnly": "bash scripts/security/pre-publish-check.sh"
#
# Requirements: bash, node, npm
# Git Bash on Windows compatible
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
PACKAGE_DIR="${1:-$(pwd)}"
PACKAGE_DIR="${PACKAGE_DIR//\\//}"

BLOCKED=0
WARNINGS=0
BLOCK_REASONS=()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
blocked() {
  echo -e "  ${RED}[BLOCKED]${RESET} $1"
  BLOCK_REASONS+=("$1")
  BLOCKED=$(( BLOCKED + 1 ))
}

warning() {
  echo -e "  ${YELLOW}[WARNING]${RESET} $1"
  WARNINGS=$(( WARNINGS + 1 ))
}

ok() {
  echo -e "  ${GREEN}[OK]${RESET} $1"
}

info_msg() {
  echo -e "  ${CYAN}[INFO]${RESET} $1"
}

# ---------------------------------------------------------------------------
# Validate directory
# ---------------------------------------------------------------------------
if [[ ! -f "${PACKAGE_DIR}/package.json" ]]; then
  echo -e "${RED}ERROR: No package.json found in ${PACKAGE_DIR}${RESET}"
  exit 1
fi

echo -e "${BOLD}${BLUE}"
echo "============================================================"
echo " pre-publish-check.sh"
echo " Pre-Publish Safety Gate"
echo " Package: $PACKAGE_DIR"
echo " Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo -e "${RESET}"

# ---------------------------------------------------------------------------
# CHECK 1: "files" field in package.json
# A missing "files" field means npm will publish everything not in .gitignore
# or .npmignore — the most common way source maps accidentally ship.
# ---------------------------------------------------------------------------
echo -e "${BOLD}[1] Checking package.json 'files' field...${RESET}"

if ! node -e "
  const pkg = require('${PACKAGE_DIR}/package.json');
  if (!pkg.files) process.exit(1);
  process.exit(0);
" 2>/dev/null; then
  warning "'files' field missing from package.json — npm will publish everything not excluded by .npmignore"
  warning "Recommendation: add 'files': ['dist'] to package.json to whitelist only build output"
else
  ok "'files' field present in package.json"
  # Show what files will ship
  FILES_LIST=$(node -e "
    const pkg = require('${PACKAGE_DIR}/package.json');
    console.log(pkg.files.join(', '));
  " 2>/dev/null || echo "unknown")
  info_msg "Declared files: $FILES_LIST"
fi

# ---------------------------------------------------------------------------
# CHECK 2: Run npm pack --dry-run and capture the file list
# This is the ground truth — it shows exactly what would be published.
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}[2] Running npm pack --dry-run to get publish file list...${RESET}"

cd "$PACKAGE_DIR"

# Capture output; handle npm versions that write to stderr vs stdout
PACK_OUTPUT=$(npm pack --dry-run 2>&1) || {
  echo -e "${YELLOW}  WARNING: npm pack --dry-run failed — skipping file list checks${RESET}"
  echo -e "${YELLOW}  Output: $PACK_OUTPUT${RESET}"
  PACK_OUTPUT=""
}

if [[ -n "$PACK_OUTPUT" ]]; then
  info_msg "Pack output captured (${#PACK_OUTPUT} bytes)"

  # --- CHECK 2a: .map files ---
  echo ""
  echo -e "${BOLD}[2a] Checking for .map files in publish list...${RESET}"
  MAP_FILES=$(echo "$PACK_OUTPUT" | grep -iE '\.map$' || true)
  if [[ -n "$MAP_FILES" ]]; then
    blocked ".MAP FILES WOULD BE PUBLISHED — source code exposure risk"
    echo "$MAP_FILES" | while IFS= read -r line; do
      info_msg "  $line"
    done
    info_msg "Fix: set 'sourcemap: false' in vite.config/webpack.config/bunfig.toml"
    info_msg "     and/or add '*.map' to .npmignore"
  else
    ok "No .map files in publish list"
  fi

  # --- CHECK 2b: node_modules ---
  echo ""
  echo -e "${BOLD}[2b] Checking for node_modules in publish list...${RESET}"
  NM_FILES=$(echo "$PACK_OUTPUT" | grep -i "node_modules" || true)
  if [[ -n "$NM_FILES" ]]; then
    blocked "node_modules WOULD BE PUBLISHED — massive bloat and security risk"
    info_msg "Fix: add 'node_modules' to .npmignore"
  else
    ok "node_modules not in publish list"
  fi

  # --- CHECK 2c: .env files ---
  echo ""
  echo -e "${BOLD}[2c] Checking for .env files in publish list...${RESET}"
  ENV_FILES=$(echo "$PACK_OUTPUT" | grep -iE '\.env' || true)
  if [[ -n "$ENV_FILES" ]]; then
    blocked ".ENV FILES WOULD BE PUBLISHED — credential exposure risk"
    echo "$ENV_FILES" | while IFS= read -r line; do
      info_msg "  $line"
    done
    info_msg "Fix: add '.env*' to .npmignore"
  else
    ok "No .env files in publish list"
  fi

  # --- CHECK 2d: TypeScript source files ---
  echo ""
  echo -e "${BOLD}[2d] Checking for raw TypeScript source in publish list...${RESET}"
  TS_SOURCE=$(echo "$PACK_OUTPUT" | grep -iE 'src/.*\.tsx?$' || true)
  if [[ -n "$TS_SOURCE" ]]; then
    warning "TypeScript source files found in publish list — may expose proprietary logic"
    echo "$TS_SOURCE" | head -10 | while IFS= read -r line; do
      info_msg "  $line"
    done
    info_msg "Fix: add 'src/' to .npmignore (keep types/ if you ship type definitions)"
  else
    ok "No TypeScript source files (src/*.ts/tsx) in publish list"
  fi

  # --- CHECK 2e: Config files that expose infra details ---
  echo ""
  echo -e "${BOLD}[2e] Checking for config files in publish list...${RESET}"
  CONFIG_FILES=$(echo "$PACK_OUTPUT" | grep -iE '\.(config\.(ts|js|mjs)|yml|yaml)$' | grep -v "node_modules" || true)
  if [[ -n "$CONFIG_FILES" ]]; then
    warning "Config files found in publish list — may expose infrastructure details"
    echo "$CONFIG_FILES" | while IFS= read -r line; do
      info_msg "  $line"
    done
  else
    ok "No config files in publish list"
  fi
fi

# ---------------------------------------------------------------------------
# FINAL VERDICT
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}${BLUE}============================================================"
echo " VERDICT"
echo "============================================================${RESET}"

if [[ "$BLOCKED" -gt 0 ]]; then
  echo ""
  echo -e "${RED}${BOLD}  BLOCKED: DO NOT PUBLISH${RESET}"
  echo ""
  echo -e "${RED}  Blocking reasons:${RESET}"
  for reason in "${BLOCK_REASONS[@]}"; do
    echo -e "  ${RED}- $reason${RESET}"
  done
  echo ""
  if [[ "$WARNINGS" -gt 0 ]]; then
    echo -e "${YELLOW}  Additionally, $WARNINGS warning(s) need attention before publish${RESET}"
  fi
  exit 1
elif [[ "$WARNINGS" -gt 0 ]]; then
  echo ""
  echo -e "${YELLOW}${BOLD}  CONDITIONALLY SAFE TO PUBLISH${RESET}"
  echo -e "${YELLOW}  $WARNINGS warning(s) found — review above before proceeding${RESET}"
  echo ""
  echo -e "${GREEN}  No hard blockers found. Proceed with caution.${RESET}"
  exit 0
else
  echo ""
  echo -e "${GREEN}${BOLD}  SAFE TO PUBLISH${RESET}"
  echo -e "${GREEN}  All checks passed. No blockers or warnings.${RESET}"
  exit 0
fi
