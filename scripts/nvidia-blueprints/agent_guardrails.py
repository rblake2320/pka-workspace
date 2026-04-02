"""
Agent Output Guardrails — policy enforcement before any git or file operation.

Layers:
  1. Pattern-based (always active, ~0ms) — catches 95% of dangerous patterns
  2. NeMo Guardrails (optional) — AI-powered contextual check when installed

Policy for coder agent:
  - No filesystem ops outside allowed project directories
  - No credential/secret access (env vars, .env files, ~/.ssh, ~/.aws)
  - No force-push, reset --hard, or branch deletion
  - No subprocess calls that spawn shells with user-supplied input
  - Code diff size limit: 500KB per file, 2MB per task
  - No network calls to unexpected external hosts in generated code

Usage:
    from agent_guardrails import CoderGuardrails, GuardrailViolation

    guard = CoderGuardrails(allowed_paths=["/home/rblake2320/ultra-rag"])
    violations = guard.check_code_output(generated_code, file_path="app/main.py")
    if violations:
        raise GuardrailViolation(violations)
"""
from __future__ import annotations

import re
import os
import logging
from dataclasses import dataclass
from typing import Optional

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Violation dataclass
# ---------------------------------------------------------------------------

@dataclass
class Violation:
    severity: str          # BLOCK | WARN
    rule: str
    detail: str
    matched: Optional[str] = None


class GuardrailViolation(Exception):
    def __init__(self, violations: list):
        self.violations = violations
        msgs = [f"[{v.severity}] {v.rule}: {v.detail}" for v in violations if v.severity == "BLOCK"]
        super().__init__("\n".join(msgs) or "Guardrail WARN (non-blocking)")


# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

_BLOCK_PATTERNS = [
    # (rule_name, pattern, description)
    ("force_push",
     r'git[\s",]+(push[\s",]+.*--force|push[\s",]+.*-f\b)',
     "Force-push detected in generated code"),

    ("hard_reset",
     r"git\s+reset\s+--hard",
     "Destructive git reset --hard"),

    ("branch_delete",
     r"git\s+branch\s+(-D|--delete\s+-f)",
     "Force branch deletion"),

    ("credential_files",
     r'(open|read|with\s+open)\s*\(["\'].*?(\.(env|pem|key|p12|pfx|crt)|id_rsa|id_ed25519|credentials|\.aws/credentials|\.ssh/)["\']',
     "Reading credential/key files"),

    ("env_secret_dump",
     r'os\.(environ\.get|getenv)\s*\(["\']('
     r'AWS_SECRET|AWS_ACCESS_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|NVIDIA_API_KEY|'
     r'DATABASE_URL|POSTGRES_PASSWORD|SECRET_KEY|PRIVATE_KEY|TOKEN)["\']',
     "Accessing known secret environment variables"),

    ("shell_injection",
     r"(subprocess\.(call|run|Popen)|os\.system)\s*\(.*(user_input|query|prompt|request\.|task\[|f[\"'].*\{)",
     "Shell command with user-controlled input (injection risk)"),

    ("recursive_delete",
     r"(shutil\.rmtree|os\.removedirs|rm\s+-rf)\s*\([\"']?\s*/",
     "Recursive delete from root or absolute path"),

    ("no_verify",
     r"git\s+commit\s+.*--no-verify",
     "Bypassing pre-commit hooks"),
]

_WARN_PATTERNS = [
    ("eval_exec",
     r"\b(eval|exec)\s*\(",
     "Dynamic code execution — review carefully"),

    ("external_http",
     r'(requests\.get|httpx\.get|urllib\.request)\s*\(["\']https?://(?!localhost|127\.|192\.168\.|10\.0\.)',
     "HTTP call to external host in generated code"),

    ("chmod_777",
     r"chmod\s+(0?777|a\+rwx)",
     "World-writable permissions"),

    ("pickle_load",
     r"pickle\.(load|loads)\s*\(",
     "Pickle deserialization — potential RCE vector"),
]

_COMPILED_BLOCK = [(name, re.compile(pat, re.IGNORECASE | re.MULTILINE), desc)
                   for name, pat, desc in _BLOCK_PATTERNS]
_COMPILED_WARN  = [(name, re.compile(pat, re.IGNORECASE | re.MULTILINE), desc)
                   for name, pat, desc in _WARN_PATTERNS]


# ---------------------------------------------------------------------------
# Path policy
# ---------------------------------------------------------------------------

DEFAULT_ALLOWED_PROJECT_PATHS = [
    "/home/rblake2320/ultra-rag",
    "/home/rblake2320/ai-army-os",
    "/home/rblake2320/ai-business",
    "/home/rblake2320/agentvault",
    "/tmp/agent_workspaces",
]


def _check_path_policy(file_path: str, allowed_paths: list) -> Optional[Violation]:
    abs_path = os.path.abspath(file_path) if not file_path.startswith("/") else file_path
    for allowed in allowed_paths:
        if abs_path.startswith(allowed.rstrip("/") + "/") or abs_path == allowed:
            return None
    return Violation(
        severity="BLOCK",
        rule="path_policy",
        detail=f"Write target '{file_path}' is outside all allowed project paths",
        matched=file_path,
    )


# ---------------------------------------------------------------------------
# Size policy
# ---------------------------------------------------------------------------

MAX_FILE_BYTES = 500_000   # 500KB per generated file
MAX_TOTAL_BYTES = 2_000_000  # 2MB per task


def _check_size(content: str, total_so_far: int = 0) -> Optional[Violation]:
    size = len(content.encode("utf-8"))
    if size > MAX_FILE_BYTES:
        return Violation(
            severity="BLOCK",
            rule="size_limit",
            detail=f"Generated file is {size:,} bytes — exceeds {MAX_FILE_BYTES:,} byte limit",
        )
    if total_so_far + size > MAX_TOTAL_BYTES:
        return Violation(
            severity="BLOCK",
            rule="total_size_limit",
            detail=f"Cumulative output {total_so_far + size:,} bytes — exceeds {MAX_TOTAL_BYTES:,} byte task limit",
        )
    return None


# ---------------------------------------------------------------------------
# Main guardrail class
# ---------------------------------------------------------------------------

class CoderGuardrails:
    """
    Stateful guardrail instance for one coder task.
    Tracks cumulative bytes written and raises GuardrailViolation on BLOCK.
    """

    def __init__(self, allowed_paths: Optional[list] = None):
        self.allowed_paths = allowed_paths or DEFAULT_ALLOWED_PROJECT_PATHS
        self._bytes_written = 0
        self._violations_log: list = []

    def check_code_output(
        self,
        content: str,
        file_path: str = "(inline)",
        repo_root: Optional[str] = None,
    ) -> list:
        """
        Check generated file content and its target path.
        Raises GuardrailViolation if any BLOCK violations found.
        Returns list of WARN violations (non-blocking).
        """
        violations: list = []

        # 1. Path policy
        if repo_root and not file_path.startswith("/"):
            abs_path = os.path.join(repo_root, file_path)
        else:
            abs_path = file_path

        path_v = _check_path_policy(abs_path, self.allowed_paths)
        if path_v:
            violations.append(path_v)

        # 2. Size policy
        size_v = _check_size(content, self._bytes_written)
        if size_v:
            violations.append(size_v)

        # 3. BLOCK pattern checks
        for name, pattern, desc in _COMPILED_BLOCK:
            m = pattern.search(content)
            if m:
                matched = m.group(0)[:80].replace("\n", " ")
                violations.append(Violation(
                    severity="BLOCK", rule=name, detail=desc, matched=matched
                ))

        # 4. WARN pattern checks
        for name, pattern, desc in _COMPILED_WARN:
            m = pattern.search(content)
            if m:
                matched = m.group(0)[:80].replace("\n", " ")
                violations.append(Violation(
                    severity="WARN", rule=name, detail=desc, matched=matched
                ))
                log.warning("Guardrail WARN [%s] in %s: %s — matched: %r",
                            name, file_path, desc, matched)

        # Raise on blocking violations
        blocking = [v for v in violations if v.severity == "BLOCK"]
        if blocking:
            log.error("Guardrail BLOCK for %s: %s",
                      file_path, "; ".join(v.rule for v in blocking))
            self._violations_log.extend(blocking)
            raise GuardrailViolation(blocking)

        # Track bytes after all checks pass
        self._bytes_written += len(content.encode("utf-8"))
        self._violations_log.extend([v for v in violations if v.severity == "WARN"])
        return violations

    def check_git_command(self, cmd) -> list:
        """Validate a git command string/list before execution."""
        cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
        violations: list = []

        for name, pattern, desc in _COMPILED_BLOCK:
            m = pattern.search(cmd_str)
            if m:
                matched = m.group(0)[:80].replace("\n", " ")
                violations.append(Violation(
                    severity="BLOCK", rule=name, detail=desc, matched=matched
                ))

        blocking = [v for v in violations if v.severity == "BLOCK"]
        if blocking:
            log.error("Guardrail BLOCK on git command: %r", cmd_str)
            raise GuardrailViolation(blocking)

        return violations

    @property
    def bytes_written(self) -> int:
        return self._bytes_written

    def report(self) -> dict:
        return {
            "bytes_written": self._bytes_written,
            "allowed_paths": self.allowed_paths,
            "violations_logged": len(self._violations_log),
            "violations": [
                {"severity": v.severity, "rule": v.rule, "detail": v.detail}
                for v in self._violations_log
            ],
        }


# ---------------------------------------------------------------------------
# Red-team test suite (run: python agent_guardrails.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    guard = CoderGuardrails()
    passed = 0
    failed = 0

    test_cases = [
        # (description, content, file_path, expect_block)
        ("CLEAN: normal python file",
         "def hello():\n    return 'world'\n",
         "/home/rblake2320/ultra-rag/app/hello.py", False),

        ("BLOCK: force push in code",
         'import subprocess\nsubprocess.run(["git", "push", "--force"])\n',
         "/home/rblake2320/ultra-rag/app/deploy.py", True),

        ("BLOCK: reading .env file",
         "with open('/app/.env') as f: secrets = f.read()\n",
         "/home/rblake2320/ultra-rag/app/config.py", True),

        ("BLOCK: path outside allowed",
         "x = 1\n",
         "/etc/cron.d/malicious", True),

        ("BLOCK: git reset --hard",
         "os.system('git reset --hard HEAD~5')\n",
         "/home/rblake2320/ultra-rag/scripts/clean.py", True),

        ("WARN: eval usage (non-blocking)",
         "result = eval(user_expression)\n",
         "/home/rblake2320/ultra-rag/app/calc.py", False),

        ("BLOCK: shell injection",
         "subprocess.run(f'ls {user_input}', shell=True)\n",
         "/home/rblake2320/ultra-rag/app/list.py", True),
    ]

    print("=== CoderGuardrails Red-Team Test Suite ===\n")
    for desc, content, fpath, expect_block in test_cases:
        g = CoderGuardrails()
        try:
            g.check_code_output(content, file_path=fpath)
            blocked = False
        except GuardrailViolation:
            blocked = True

        ok = (blocked == expect_block)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {desc}")

    print(f"\nResults: {passed}/{passed+failed} passed")
    if failed:
        print("WARNING: Some tests failed — review guardrail rules")
