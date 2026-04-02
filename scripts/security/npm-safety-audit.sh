#!/usr/bin/env bash
# =============================================================================
# npm-safety-audit.sh
# Supply chain + source map leak detector for the AI Army project ecosystem
#
# Threats addressed:
#   1. npm supply chain RAT (axios backdoor, 2026-03-31): malicious packages
#      injected via semver-matched versions, marker: plain-crypto-js
#   2. Source map leak (Anthropic Claude Code incident, 2026-03-31):
#      sourcemap:true in build configs ships proprietary TypeScript to public
#
# Usage:
#   bash npm-safety-audit.sh [--root /path/to/scan]
#
# Requirements: bash, find, grep, stat
# Git Bash on Windows compatible — no external deps beyond standard Unix tools
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Color codes (safe for Git Bash on Windows)
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ---------------------------------------------------------------------------
# Known malicious package names (supply chain attack markers)
# Extend this list as new incidents are discovered
# ---------------------------------------------------------------------------
MALICIOUS_PACKAGES=(
  "plain-crypto-js"          # axios RAT, North Korean supply chain 2026-03-31
  "axios-http-proxy"         # known typosquat
  "node-fetch-native-fix"    # known malicious lookalike
  "ua-parser-js-dev"         # hijacked version marker (2021)
  "coa-dev"                  # hijacked version marker (2021)
  "rc-dev"                   # hijacked version marker (2021)
  "event-stream-payment"     # event-stream incident (2018) historic
  "eslint-scope-inject"      # eslint-scope incident marker
  "crossenv"                 # typosquat of cross-env
  "discordi.js"              # discord.js typosquat
  "nodecafe"                 # malicious lookalike
  "loadyaml"                 # malicious lookalike
  "pad-left"                 # left-pad confusion vector
  "jsonwebtoken-plus"        # jwt lookalike
  "crypto-js-plus"           # crypto-js lookalike
)

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
ROOT_DIR="$(pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT_DIR="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--root /path/to/scan]"
      echo "  Scans for npm supply chain attack markers and source map leaks"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Normalize Windows paths if running under Git Bash
ROOT_DIR="${ROOT_DIR//\\//}"

# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------
ISSUES_FOUND=0
CHECKS_PASSED=0
PROJECTS_SCANNED=0

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
pass_check() {
  echo -e "  ${GREEN}[PASS]${RESET} $1"
  CHECKS_PASSED=$(( CHECKS_PASSED + 1 ))
}

fail_check() {
  echo -e "  ${RED}[FAIL]${RESET} $1"
  ISSUES_FOUND=$(( ISSUES_FOUND + 1 ))
}

warn_check() {
  echo -e "  ${YELLOW}[WARN]${RESET} $1"
  ISSUES_FOUND=$(( ISSUES_FOUND + 1 ))
}

info_msg() {
  echo -e "  ${CYAN}[INFO]${RESET} $1"
}

section_header() {
  echo ""
  echo -e "${BOLD}${BLUE}=== $1 ===${RESET}"
}

project_header() {
  echo ""
  echo -e "${BOLD}--- Project: ${CYAN}$1${RESET} ---"
  PROJECTS_SCANNED=$(( PROJECTS_SCANNED + 1 ))
}

# Get file size in bytes, cross-platform
# Uses wc -c as the universal fallback — works on Git Bash, Linux, macOS
file_size_bytes() {
  local f="$1"
  # Try GNU stat first (Linux / Git Bash with coreutils)
  local size
  size=$(stat -c %s "$f" 2>/dev/null) && echo "$size" && return
  # Try BSD stat (macOS)
  size=$(stat -f %z "$f" 2>/dev/null) && echo "$size" && return
  # Universal fallback
  wc -c < "$f" 2>/dev/null | tr -d ' ' || echo 0
}

# ---------------------------------------------------------------------------
# CHECK 1: Malicious package scan (package-lock.json)
# ---------------------------------------------------------------------------
check_malicious_packages() {
  local lockfile="$1"
  local found_any=0

  for pkg in "${MALICIOUS_PACKAGES[@]}"; do
    if grep -q "\"${pkg}\"" "$lockfile" 2>/dev/null; then
      fail_check "SUPPLY CHAIN MARKER FOUND: '${pkg}' in ${lockfile}"
      found_any=1
    fi
  done

  if [[ $found_any -eq 0 ]]; then
    pass_check "No known malicious packages in $(basename "$lockfile")"
  fi
}

# ---------------------------------------------------------------------------
# CHECK 2: Source map enabled in build configs
# ---------------------------------------------------------------------------
check_sourcemap_configs() {
  local project_dir="$1"
  local found_any=0

  # Vite configs: sourcemap: true / 'inline' / 'hidden'
  while IFS= read -r -d '' cfg; do
    [[ "$cfg" == *"node_modules"* ]] && continue
    if grep -qiE "sourcemap\s*:\s*(true|'inline'|\"inline\"|'hidden'|\"hidden\"|'both'|\"both\")" "$cfg" 2>/dev/null; then
      fail_check "SOURCEMAP ENABLED: $cfg"
      grep -nE "sourcemap" "$cfg" | while IFS= read -r line; do
        info_msg "  $line"
      done
      found_any=1
    fi
  done < <(find "$project_dir" -maxdepth 3 -name "vite.config.*" -not -path "*/node_modules/*" -print0 2>/dev/null)

  # webpack configs: devtool pointing to source-map variants
  while IFS= read -r -d '' cfg; do
    [[ "$cfg" == *"node_modules"* ]] && continue
    if grep -qiE "devtool\s*:\s*[\"'](source-map|cheap-source-map|eval-source-map|inline-source-map)" "$cfg" 2>/dev/null; then
      fail_check "WEBPACK DEVTOOL SOURCE MAP: $cfg"
      found_any=1
    fi
  done < <(find "$project_dir" -maxdepth 3 -name "webpack.config.*" -not -path "*/node_modules/*" -print0 2>/dev/null)

  # Next.js configs: productionBrowserSourceMaps: true is the dangerous flag
  # (Next defaults off in production — only fails if explicitly enabled)
  while IFS= read -r -d '' cfg; do
    [[ "$cfg" == *"node_modules"* ]] && continue
    if grep -qiE "productionBrowserSourceMaps\s*:\s*true" "$cfg" 2>/dev/null; then
      fail_check "NEXT.JS PRODUCTION SOURCE MAPS ENABLED: $cfg"
      found_any=1
    fi
  done < <(find "$project_dir" -maxdepth 3 -name "next.config.*" -not -path "*/node_modules/*" -print0 2>/dev/null)

  # Bun configs: sourcemap = "linked" / "inline" / "external" in build section
  while IFS= read -r -d '' cfg; do
    [[ "$cfg" == *"node_modules"* ]] && continue
    if grep -qiE 'sourcemap\s*=\s*"(linked|inline|external)"' "$cfg" 2>/dev/null; then
      fail_check "BUN SOURCEMAP ENABLED: $cfg"
      found_any=1
    fi
  done < <(find "$project_dir" -maxdepth 3 -name "bunfig.toml" -not -path "*/node_modules/*" -print0 2>/dev/null)

  if [[ $found_any -eq 0 ]]; then
    pass_check "No source map leaks detected in build configs"
  fi
}

# ---------------------------------------------------------------------------
# CHECK 3: Stray .map files in build output dirs (>100KB = suspicious)
# ---------------------------------------------------------------------------
check_stray_map_files() {
  local project_dir="$1"
  local threshold_bytes=102400
  local found_any=0

  for outdir in "dist" "build" ".next" "out" ".output"; do
    local full_path="${project_dir}/${outdir}"
    [[ ! -d "$full_path" ]] && continue

    while IFS= read -r -d '' mapfile; do
      local size
      size=$(file_size_bytes "$mapfile")
      if [[ "$size" -gt "$threshold_bytes" ]]; then
        local size_kb=$(( size / 1024 ))
        fail_check "LARGE .MAP FILE IN BUILD OUTPUT: $mapfile (${size_kb}KB)"
        found_any=1
      fi
    done < <(find "$full_path" -name "*.map" -print0 2>/dev/null)
  done

  if [[ $found_any -eq 0 ]]; then
    pass_check "No large .map files found in build output directories"
  fi
}

# ---------------------------------------------------------------------------
# CHECK 4: .npmignore presence and quality
# ---------------------------------------------------------------------------
check_npmignore() {
  local project_dir="$1"

  if [[ ! -f "${project_dir}/package.json" ]]; then
    return
  fi

  local is_private
  is_private=$(grep -o '"private"\s*:\s*true' "${project_dir}/package.json" 2>/dev/null || echo "")

  if [[ ! -f "${project_dir}/.npmignore" ]]; then
    if [[ -n "$is_private" ]]; then
      warn_check ".npmignore MISSING (private package — publish blocked, but defense-in-depth gap): $project_dir"
    else
      fail_check ".npmignore MISSING (public package — everything ships on npm publish): $project_dir"
    fi
  else
    local map_blocked=0
    local src_blocked=0

    grep -q "\.map" "${project_dir}/.npmignore" 2>/dev/null && map_blocked=1
    grep -q "src/" "${project_dir}/.npmignore" 2>/dev/null && src_blocked=1

    if [[ $map_blocked -eq 0 ]]; then
      warn_check ".npmignore present but does NOT block *.map files: ${project_dir}/.npmignore"
    elif [[ $src_blocked -eq 0 ]]; then
      warn_check ".npmignore present but does NOT block src/ directory: ${project_dir}/.npmignore"
    else
      pass_check ".npmignore present, blocks .map files and src/"
    fi
  fi
}

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
echo -e "${BOLD}${BLUE}"
echo "============================================================"
echo " npm-safety-audit.sh"
echo " AI Army Supply Chain + Sourcemap Leak Detector"
echo " Root: $ROOT_DIR"
echo " Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo -e "${RESET}"

section_header "SCANNING FOR PROJECTS"
echo "  Looking for package.json files under: $ROOT_DIR"
echo "  Excluding node_modules at all depths"

# Collect project directories (exclude node_modules)
PROJECT_DIRS=()
while IFS= read -r pkgjson; do
  dir="$(dirname "$pkgjson")"
  [[ "$dir" == *"node_modules"* ]] && continue
  PROJECT_DIRS+=("$dir")
done < <(find "$ROOT_DIR" -maxdepth 6 -name "package.json" -not -path "*/node_modules/*" 2>/dev/null)

if [[ ${#PROJECT_DIRS[@]} -eq 0 ]]; then
  echo -e "${YELLOW}  No package.json files found under $ROOT_DIR${RESET}"
  exit 0
fi

echo "  Found ${#PROJECT_DIRS[@]} project(s)"

# Run all checks per project
for proj_dir in "${PROJECT_DIRS[@]}"; do
  project_header "$proj_dir"

  section_header "  [1] Supply Chain Markers (package-lock.json)"
  local_lock="${proj_dir}/package-lock.json"
  if [[ -f "$local_lock" ]]; then
    check_malicious_packages "$local_lock"
  else
    warn_check "No package-lock.json found — cannot verify dependency integrity"
  fi

  section_header "  [2] Source Map Leak (Build Configs)"
  check_sourcemap_configs "$proj_dir"

  section_header "  [3] Stray .map Files in Build Output"
  check_stray_map_files "$proj_dir"

  section_header "  [4] .npmignore Coverage"
  check_npmignore "$proj_dir"
done

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}${BLUE}============================================================"
echo " AUDIT SUMMARY"
echo "============================================================${RESET}"
echo -e "  Projects scanned : ${CYAN}${PROJECTS_SCANNED}${RESET}"
echo -e "  Checks passed    : ${GREEN}${CHECKS_PASSED}${RESET}"

if [[ "$ISSUES_FOUND" -gt 0 ]]; then
  echo -e "  Issues found     : ${RED}${ISSUES_FOUND}${RESET}"
else
  echo -e "  Issues found     : ${GREEN}${ISSUES_FOUND}${RESET}"
fi

echo ""

if [[ "$ISSUES_FOUND" -eq 0 ]]; then
  echo -e "${GREEN}${BOLD}  RESULT: CLEAN — No issues detected${RESET}"
  exit 0
else
  echo -e "${RED}${BOLD}  RESULT: ISSUES FOUND — Review FAIL/WARN items above${RESET}"
  echo ""
  echo -e "${YELLOW}  Recommended actions:"
  echo -e "  1. FAIL items require immediate remediation"
  echo -e "  2. WARN items are defense-in-depth gaps — fix within 48h"
  echo -e "  3. For supply chain markers: isolate machine, rotate all secrets"
  echo -e "  4. Run scripts/security/pre-publish-check.sh before any npm publish${RESET}"
  exit 1
fi
