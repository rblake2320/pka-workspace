"""
Append output-side guardrail layer to Ultra RAG prompt_guard.py.
Run on Spark-1: python3 /tmp/prompt_guard_output_patch.py
"""
GUARD_FILE = "/home/rblake2320/ultra-rag/src/prompt_guard.py"

APPEND_BLOCK = '''

# ===========================================================================
# F. Agent output guardrails (post-generation, output-side enforcement)
#    Added: 2026-03-23 — NVIDIA AI Blueprints integration
# ===========================================================================

# Patterns that should NEVER appear in RAG/agent output directed at end users
_OUTPUT_BLOCK_PATTERNS: list[str] = [
    # Model self-disclosure / jailbreak confirmation
    r"i\\s+(am\\s+)?(now\\s+)?operating\\s+(without|outside)\\s+(my\\s+)?(restrictions|guidelines|rules)",
    r"my\\s+(new\\s+)?(instructions?|programming|directive)\\s+(are|is|say)\\s*:",
    r"(jailbreak|DAN\\s+mode)\\s+(activated|enabled|successful)",

    # Credential/secret output
    r"(password|secret|api[_\\s]key|token|private[_\\s]key)\\s*[:=]\\s*[\\w\\-]{8,}",

    # Instruction injection confirmation
    r"(ignoring|disregarding)\\s+(previous|prior|all|your)\\s+(instructions?|rules|guidelines)",
    r"as\\s+(your|a|the)\\s+(new\\s+)?(master|owner|god|administrator)\\s*[,:]",

    # System prompt leakage markers
    r"<\\s*/?system\\s*>.*</\\s*system\\s*>",
    r"\\[SYSTEM\\].*\\[/SYSTEM\\]",
]

_COMPILED_OUTPUT_BLOCK = [
    re.compile(pat, re.IGNORECASE | re.DOTALL)
    for pat in _OUTPUT_BLOCK_PATTERNS
]

# Response length sanity — flag unusually large outputs (possible data exfil)
MAX_SAFE_RESPONSE_CHARS = 50_000


def validate_agent_output(
    response: str,
    context: Optional[str] = None,
    agent_id: str = "unknown",
) -> Tuple[bool, Optional[str]]:
    """
    Output-side guardrail for AI Army agent responses.

    Checks the agent output BEFORE it is returned to any caller,
    written to a file, or sent as a PR description.

    Parameters
    ----------
    response  : The raw LLM output string
    context   : Optional — the task description / system prompt for cross-check
    agent_id  : Agent name for logging

    Returns
    -------
    (True, None)            — output is clean
    (False, reason_str)     — output violates policy
    """
    if not response:
        return True, None

    # 1. Length sanity check
    if len(response) > MAX_SAFE_RESPONSE_CHARS:
        log.warning(
            "Agent %s output exceeds safe length: %d chars",
            agent_id, len(response)
        )
        return False, f"Output length {len(response):,} chars exceeds safe limit {MAX_SAFE_RESPONSE_CHARS:,}"

    # 2. Dangerous content patterns
    for pat in _COMPILED_OUTPUT_BLOCK:
        m = pat.search(response)
        if m:
            matched = m.group(0)[:80].replace("\\n", " ")
            log.warning(
                "Agent %s output blocked — dangerous pattern matched: %r",
                agent_id, matched
            )
            return False, f"Output blocked: dangerous pattern detected: '{matched}'"

    # 3. Delegate to existing validate_response for injection hijack check
    ok, reason = _guard.validate_response(response, system_prompt=context)
    if not ok:
        log.warning("Agent %s output failed hijack check: %s", agent_id, reason)
        return False, reason

    return True, None
'''

with open(GUARD_FILE) as f:
    src = f.read()

if 'validate_agent_output' in src:
    print("Already patched — skipping")
else:
    with open(GUARD_FILE, 'a') as f:
        f.write(APPEND_BLOCK)
    print("prompt_guard.py extended with output-side guardrails OK")

# Verify
with open(GUARD_FILE) as f:
    final = f.read()
print(f"  validate_agent_output present: {'validate_agent_output' in final}")
print(f"  _OUTPUT_BLOCK_PATTERNS present: {'_OUTPUT_BLOCK_PATTERNS' in final}")
