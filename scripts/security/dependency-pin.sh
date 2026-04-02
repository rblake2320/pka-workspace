#!/usr/bin/env bash
# =============================================================================
# dependency-pin.sh
# Dependency range auditor and exact-version pinning assistant
#
# Problem: semver ranges (^, ~, *) allow npm to silently upgrade to a
# backdoored version during `npm install`. The axios supply chain attack
# (2026-03-31) worked because packages using "^1.x" automatically pulled
# in the backdoored 1.14.1 during the 3-hour window.
#
# Pinning to exact versions from a known-good package-lock.json prevents
# automatic pickup of newly-published malicious versions.
#
# Usage:
#   bash dependency-pin.sh [--pin] [/path/to/package/dir]
#
# Without --pin: audit only, print range vs pinned summary
# With --pin:    generate package.pinned.json with exact versions
#                from the current package-lock.json
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
# Argument parsing
# ---------------------------------------------------------------------------
PACKAGE_DIR="$(pwd)"
DO_PIN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pin)
      DO_PIN=1
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--pin] [/path/to/package/dir]"
      echo ""
      echo "  Audit mode (default): reports semver ranges vs pinned packages"
      echo "  Pin mode (--pin):     generates package.pinned.json with exact"
      echo "                        versions from the current package-lock.json"
      exit 0
      ;;
    *)
      # Treat as directory path
      PACKAGE_DIR="$1"
      shift
      ;;
  esac
done

PACKAGE_DIR="${PACKAGE_DIR//\\//}"

# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------
if [[ ! -f "${PACKAGE_DIR}/package.json" ]]; then
  echo -e "${RED}ERROR: No package.json found in ${PACKAGE_DIR}${RESET}"
  exit 1
fi

if [[ ! -f "${PACKAGE_DIR}/package-lock.json" ]]; then
  echo -e "${YELLOW}WARNING: No package-lock.json found — pinned version lookup will be unavailable${RESET}"
fi

echo -e "${BOLD}${BLUE}"
echo "============================================================"
echo " dependency-pin.sh"
echo " Dependency Range Auditor"
echo " Package: $PACKAGE_DIR"
echo " Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo -e "${RESET}"

# ---------------------------------------------------------------------------
# Node script: analyze package.json ranges and optionally emit pinned version
# ---------------------------------------------------------------------------
node - <<'NODESCRIPT'
const fs = require('fs');
const path = require('path');

// Read args passed via environment (bash exports them before calling node -)
const packageDir = process.env.PACKAGE_DIR_ARG;
const doPin = process.env.DO_PIN_ARG === '1';

const packageJsonPath = path.join(packageDir, 'package.json');
const lockJsonPath = path.join(packageDir, 'package-lock.json');

const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

// Collect all deps
const depSections = ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'];
const allDeps = {};
for (const section of depSections) {
  if (pkg[section]) {
    for (const [name, ver] of Object.entries(pkg[section])) {
      allDeps[name] = { version: ver, section };
    }
  }
}

// Categorize
const ranged = [];
const pinned = [];
const wildcard = [];

for (const [name, { version, section }] of Object.entries(allDeps)) {
  const v = String(version);
  if (v === '*' || v === 'x' || v === '') {
    wildcard.push({ name, version: v, section });
  } else if (v.startsWith('^') || v.startsWith('~') || v.includes('>=') || v.includes('>') || v.includes('<')) {
    ranged.push({ name, version: v, section });
  } else {
    pinned.push({ name, version: v, section });
  }
}

// Print report
const total = Object.keys(allDeps).length;

console.log('\x1b[1m\x1b[34m=== DEPENDENCY RANGE AUDIT ===\x1b[0m');
console.log(`\n  Total packages : ${total}`);
console.log(`  Pinned (safe)  : \x1b[32m${pinned.length}\x1b[0m`);
console.log(`  Ranged (^/~/>= ): \x1b[33m${ranged.length}\x1b[0m`);
console.log(`  Wildcard (* )  : \x1b[31m${wildcard.length}\x1b[0m`);

const supplyChainRisk = ranged.length + wildcard.length;
const riskPct = total > 0 ? Math.round((supplyChainRisk / total) * 100) : 0;

console.log(`\n  Supply chain exposure: ${supplyChainRisk}/${total} packages (${riskPct}%) use ranges`);

// Show wildcards (highest risk — any version accepted)
if (wildcard.length > 0) {
  console.log('\n\x1b[1m\x1b[31m  WILDCARD PACKAGES (accept ANY version — highest risk):\x1b[0m');
  for (const { name, version, section } of wildcard) {
    console.log(`    \x1b[31m${name}\x1b[0m  ${version}  [${section}]`);
  }
}

// Show ranged packages
if (ranged.length > 0) {
  console.log('\n\x1b[1m\x1b[33m  RANGED PACKAGES (semver range — supply chain risk):\x1b[0m');
  for (const { name, version, section } of ranged) {
    console.log(`    \x1b[33m${name}\x1b[0m  ${version}  [${section}]`);
  }
}

// Highlight high-value targets (commonly hijacked packages)
const highValueTargets = [
  'axios', 'lodash', 'moment', 'express', 'react', 'next', 'webpack',
  'babel', 'eslint', 'prettier', 'typescript', 'vite', 'rollup',
  'cross-env', 'dotenv', 'jsonwebtoken', 'bcrypt', 'crypto-js'
];
const rangedHighValue = ranged.filter(d => highValueTargets.some(t => d.name === t || d.name.startsWith(`@${t}/`)));

if (rangedHighValue.length > 0) {
  console.log('\n\x1b[1m\x1b[31m  HIGH-VALUE TARGETS using ranges (commonly hijacked):\x1b[0m');
  for (const { name, version, section } of rangedHighValue) {
    console.log(`    \x1b[31m${name}\x1b[0m  ${version}  [${section}]  <-- PIN THIS`);
  }
}

// Pinning mode: generate package.pinned.json
if (doPin) {
  console.log('\n\x1b[1m\x1b[34m=== GENERATING PINNED package.json ===\x1b[0m');

  if (!fs.existsSync(lockJsonPath)) {
    console.log('\x1b[31m  ERROR: package-lock.json not found — cannot resolve exact versions\x1b[0m');
    console.log('  Run `npm install` first to generate a lock file, then re-run with --pin');
    process.exit(1);
  }

  const lock = JSON.parse(fs.readFileSync(lockJsonPath, 'utf8'));

  // Build exact version map from lock file
  // package-lock v2/v3 uses "packages" key with "node_modules/pkgname" keys
  const exactVersions = {};
  const lockPackages = lock.packages || {};
  for (const [lockKey, lockData] of Object.entries(lockPackages)) {
    if (!lockKey || lockKey === '') continue; // root entry
    const pkgName = lockKey.replace(/^node_modules\//, '').replace(/\/node_modules\/[^/]+$/, match => match);
    // Handle scoped packages like node_modules/@scope/pkg
    const cleanName = lockKey.startsWith('node_modules/')
      ? lockKey.slice('node_modules/'.length)
      : lockKey;
    if (lockData.version && !exactVersions[cleanName]) {
      exactVersions[cleanName] = lockData.version;
    }
  }

  // Build pinned package.json
  const pinnedPkg = JSON.parse(JSON.stringify(pkg));
  let pinCount = 0;
  let missCount = 0;

  for (const section of depSections) {
    if (!pinnedPkg[section]) continue;
    for (const name of Object.keys(pinnedPkg[section])) {
      const resolved = exactVersions[name];
      if (resolved) {
        pinnedPkg[section][name] = resolved;
        pinCount++;
      } else {
        console.log(`  \x1b[33m[WARN]\x1b[0m Could not resolve exact version for: ${name} — keeping original`);
        missCount++;
      }
    }
  }

  const outputPath = path.join(packageDir, 'package.pinned.json');
  fs.writeFileSync(outputPath, JSON.stringify(pinnedPkg, null, 2) + '\n');

  console.log(`\n  Pinned ${pinCount} packages`);
  if (missCount > 0) {
    console.log(`  \x1b[33mCould not resolve ${missCount} packages (kept original range)\x1b[0m`);
  }
  console.log(`\n  \x1b[32mWrote: ${outputPath}\x1b[0m`);
  console.log('\n  To apply:');
  console.log('    cp package.json package.json.backup');
  console.log('    cp package.pinned.json package.json');
  console.log('    npm install');
  console.log('    # Verify everything works, then commit');
  console.log('\n  NOTE: Pinned versions still require package-lock.json for full integrity.');
  console.log('  Use `npm ci` instead of `npm install` in CI/CD to enforce the lock file.');
}

// Final advice
console.log('\n\x1b[1m\x1b[34m=== RECOMMENDATIONS ===\x1b[0m');
if (supplyChainRisk > 0 && !doPin) {
  console.log(`  ${supplyChainRisk} packages use ranges. Run with --pin to generate package.pinned.json`);
}
console.log('  1. Use `npm ci` in CI/CD (enforces exact lock file, no upgrades)');
console.log('  2. Enable Dependabot or Renovate for controlled dependency updates');
console.log('  3. Run `npm audit` weekly — catches known CVEs');
console.log('  4. Consider using `npm install --ignore-scripts` for untrusted packages');
console.log('  5. Pin axios and other high-value targets immediately');
NODESCRIPT

# ---------------------------------------------------------------------------
# Pass variables to the Node script
# ---------------------------------------------------------------------------
export PACKAGE_DIR_ARG="$PACKAGE_DIR"
export DO_PIN_ARG="$DO_PIN"

# Re-run the script now that exports are set
# (The heredoc above already ran without them — we need to re-run it properly)
# We re-implement as a temp file approach for variable passing

TMP_SCRIPT=$(mktemp /tmp/dep_pin_XXXXXX.js)

cat > "$TMP_SCRIPT" << 'ENDNODESCRIPT'
const fs = require('fs');
const path = require('path');

const packageDir = process.env.PACKAGE_DIR_ARG;
const doPin = process.env.DO_PIN_ARG === '1';

const packageJsonPath = path.join(packageDir, 'package.json');
const lockJsonPath = path.join(packageDir, 'package-lock.json');

if (!fs.existsSync(packageJsonPath)) {
  console.error('ERROR: package.json not found at ' + packageJsonPath);
  process.exit(1);
}

const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

const depSections = ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'];
const allDeps = {};
for (const section of depSections) {
  if (pkg[section]) {
    for (const [name, ver] of Object.entries(pkg[section])) {
      allDeps[name] = { version: ver, section };
    }
  }
}

const ranged = [];
const pinned = [];
const wildcard = [];

for (const [name, { version, section }] of Object.entries(allDeps)) {
  const v = String(version);
  if (v === '*' || v === 'x' || v === '') {
    wildcard.push({ name, version: v, section });
  } else if (v.startsWith('^') || v.startsWith('~') || v.includes('>=') || v.includes('>') || v.includes('<')) {
    ranged.push({ name, version: v, section });
  } else {
    pinned.push({ name, version: v, section });
  }
}

const total = Object.keys(allDeps).length;

console.log('\x1b[1m\x1b[34m=== DEPENDENCY RANGE AUDIT ===\x1b[0m');
console.log('\n  Total packages  : ' + total);
console.log('  Pinned (safe)   : \x1b[32m' + pinned.length + '\x1b[0m');
console.log('  Ranged (^/~/>=) : \x1b[33m' + ranged.length + '\x1b[0m');
console.log('  Wildcard (*)    : \x1b[31m' + wildcard.length + '\x1b[0m');

const supplyChainRisk = ranged.length + wildcard.length;
const riskPct = total > 0 ? Math.round((supplyChainRisk / total) * 100) : 0;

console.log('\n  Supply chain exposure: ' + supplyChainRisk + '/' + total + ' packages (' + riskPct + '%) use ranges');

if (wildcard.length > 0) {
  console.log('\n\x1b[1m\x1b[31m  WILDCARD PACKAGES (accept ANY version — critical risk):\x1b[0m');
  for (const { name, version, section } of wildcard) {
    console.log('    \x1b[31m' + name + '\x1b[0m  ' + version + '  [' + section + ']');
  }
}

if (ranged.length > 0) {
  console.log('\n\x1b[1m\x1b[33m  RANGED PACKAGES (semver range — supply chain risk):\x1b[0m');
  for (const { name, version, section } of ranged) {
    console.log('    \x1b[33m' + name + '\x1b[0m  ' + version + '  [' + section + ']');
  }
}

const highValueTargets = [
  'axios', 'lodash', 'moment', 'express', 'react', 'next', 'webpack',
  'babel', 'eslint', 'prettier', 'typescript', 'vite', 'rollup',
  'cross-env', 'dotenv', 'jsonwebtoken', 'bcrypt', 'crypto-js', 'socket.io'
];
const rangedHighValue = ranged.filter(d =>
  highValueTargets.some(t => d.name === t || d.name.startsWith('@' + t + '/'))
);

if (rangedHighValue.length > 0) {
  console.log('\n\x1b[1m\x1b[31m  HIGH-VALUE TARGETS using ranges (commonly hijacked):\x1b[0m');
  for (const { name, version, section } of rangedHighValue) {
    console.log('    \x1b[31m' + name + '\x1b[0m  ' + version + '  [' + section + ']  <-- PIN THIS');
  }
}

if (doPin) {
  console.log('\n\x1b[1m\x1b[34m=== GENERATING PINNED package.json ===\x1b[0m');

  if (!fs.existsSync(lockJsonPath)) {
    console.log('\x1b[31m  ERROR: package-lock.json not found\x1b[0m');
    console.log('  Run `npm install` first to generate a lock file, then re-run with --pin');
    process.exit(1);
  }

  const lock = JSON.parse(fs.readFileSync(lockJsonPath, 'utf8'));
  const exactVersions = {};
  const lockPackages = lock.packages || {};

  for (const [lockKey, lockData] of Object.entries(lockPackages)) {
    if (!lockKey) continue;
    const cleanName = lockKey.startsWith('node_modules/')
      ? lockKey.slice('node_modules/'.length)
      : lockKey;
    if (lockData.version && !exactVersions[cleanName]) {
      exactVersions[cleanName] = lockData.version;
    }
  }

  const pinnedPkg = JSON.parse(JSON.stringify(pkg));
  let pinCount = 0;
  let missCount = 0;

  for (const section of depSections) {
    if (!pinnedPkg[section]) continue;
    for (const name of Object.keys(pinnedPkg[section])) {
      const resolved = exactVersions[name];
      if (resolved) {
        pinnedPkg[section][name] = resolved;
        pinCount++;
      } else {
        console.log('  \x1b[33m[WARN]\x1b[0m Could not resolve: ' + name + ' — keeping original');
        missCount++;
      }
    }
  }

  const outputPath = path.join(packageDir, 'package.pinned.json');
  fs.writeFileSync(outputPath, JSON.stringify(pinnedPkg, null, 2) + '\n');

  console.log('\n  Pinned ' + pinCount + ' packages');
  if (missCount > 0) {
    console.log('  \x1b[33mCould not resolve ' + missCount + ' packages (kept original range)\x1b[0m');
  }
  console.log('\n  \x1b[32mWrote: ' + outputPath + '\x1b[0m');
  console.log('\n  To apply:');
  console.log('    cp package.json package.json.backup');
  console.log('    cp package.pinned.json package.json');
  console.log('    npm install');
  console.log('    # Verify, then commit both package.json and package-lock.json');
}

console.log('\n\x1b[1m\x1b[34m=== RECOMMENDATIONS ===\x1b[0m');
if (supplyChainRisk > 0 && !doPin) {
  console.log('  ' + supplyChainRisk + ' packages use ranges — run with --pin to generate pinned version');
}
console.log('  1. Use `npm ci` in CI/CD (enforces exact lock file, no silent upgrades)');
console.log('  2. Enable Dependabot or Renovate for controlled, reviewed dependency updates');
console.log('  3. Run `npm audit` weekly to catch known CVEs');
console.log('  4. Consider `npm install --ignore-scripts` for untrusted transitive deps');
console.log('  5. Commit package-lock.json — it is your dependency manifest, not just a cache');
ENDNODESCRIPT

# Run the real script with environment variables set
node "$TMP_SCRIPT"
rm -f "$TMP_SCRIPT"
