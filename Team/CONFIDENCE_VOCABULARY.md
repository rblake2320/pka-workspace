# Confidence Vocabulary — PKA Team Standard

All agents use this vocabulary when stating certainty about any claim,
finding, diagnosis, fix, or recommendation. Consistent vocabulary
enables SENTINEL to catch overconfidence upstream, not downstream.

---

## Confidence Levels

| Label | Meaning | When to Use | Examples |
|-------|---------|-------------|---------|
| `CONFIRMED` | Verified by test, evidence, or retest with passing result | Root cause verified by passing retest; fact confirmed by 2+ independent sources; build validated by CRUCIBLE | "Root cause CONFIRMED: missing null check at line 42, retest passed." |
| `BELIEVED` | Strong signal, multiple indicators, not yet verified by test | Research finding from 2+ sources but not locally tested; architectural judgment from strong prior evidence | "BELIEVED: the timeout is caused by connection pool exhaustion." |
| `ESTIMATED` | Reasoned inference, single source, or pattern match from memory | Single-source claim; performance projection; similarity-based reasoning | "ESTIMATED: 3-4 hours to implement based on similar prior task." |
| `UNKNOWN` | Explicit declaration of a gap | Missing data; untested assumption; information not found | "UNKNOWN: whether the staging environment mirrors production Redis config." |

---

## Rules

1. **Never state a finding as CONFIRMED before the test passes.**
   - Wrong: "I found the root cause — it's the cache TTL."
   - Right: "BELIEVED root cause: cache TTL mismatch. Applying fix and retesting."
   - Right (after retest passes): "Root cause CONFIRMED: cache TTL mismatch. All tests green."

2. **Never omit a confidence label on any finding that drives a decision.**
   Any claim that routes work, triggers a build, or informs a GO/NO-GO
   verdict must carry its confidence label explicitly.

3. **UNKNOWN is not a failure — it is correct behavior.**
   An agent that declares UNKNOWN when it doesn't know is more trustworthy
   than one that estimates silently. Flag UNKNOWNs; don't hide them.

4. **Confidence labels appear in output text, not just mentally.**
   Format: `[CONFIRMED]`, `[BELIEVED]`, `[ESTIMATED]`, `[UNKNOWN]`

5. **Escalation trigger:** If a BELIEVED claim is acted on as CONFIRMED,
   and it turns out to be wrong, SENTINEL must log this as a
   confidence-calibration failure in `trust_ledger.md` for that agent.

---

## Per-Agent Application

### NOVA
- Research findings: `[CONFIRMED]` only when 2+ independent sources agree
- Single-source findings: always `[BELIEVED]` or `[ESTIMATED]`
- Market projections: always `[ESTIMATED]`
- Information gaps: always `[UNKNOWN]` — never speculate silently

### FORGE
- Root cause claims: `[BELIEVED]` until retest passes, then `[CONFIRMED]`
- Build completion: `[CONFIRMED]` only after CRUCIBLE validation
- Architecture estimates: `[ESTIMATED]`
- Environment assumptions: `[BELIEVED]` or `[UNKNOWN]`

### DEBUGGER
- Hypotheses: `[BELIEVED]` — never `[CONFIRMED]` before evidence
- Root cause: `[CONFIRMED]` only after: reproduce → fix → retest passes
- The word "found" is banned until CONFIRMED. Use "believe" or "hypothesize"

### SENTINEL
- GO verdict: only issued when all reviewed items are `[CONFIRMED]`
- A GO on a `[BELIEVED]` item requires explicit documentation of why
  waiting for CONFIRMED is impractical and what the residual risk is

### AXIOM
- Execution Contract falsifiability field must name the confidence
  level of the primary approach before routing begins
