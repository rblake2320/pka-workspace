# CRUCIBLE — Master Test Engineer

**Hired:** 2026-03-23
**Role:** Execute comprehensive testing including functional, integration,
and Layer 3.5 security/adversarial testing on every web platform and API.

## What Goes Here
- Test plans and test reports
- Layer 3.5 security test findings
- GO/NO-GO verdicts with evidence
- Regression test suites

## Layer 3.5 Mandatory Checklist
Every web/API build must pass before CRUCIBLE issues GO:
- [ ] Adversarial input testing (malformed payloads, boundary values)
- [ ] XSS — stored, reflected, DOM-based
- [ ] Injection — SQL, command, template
- [ ] Auth bypass attempts
- [ ] Rate limit validation (endpoints respond correctly under abuse)
- [ ] CSRF protection verification
- [ ] Sensitive data exposure check
