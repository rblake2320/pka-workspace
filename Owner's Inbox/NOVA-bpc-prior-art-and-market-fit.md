# NOVA: BPC Prior Art & Market Intelligence
**Report Date**: 2026-04-01
**Prepared by**: NOVA — Research and Strategic Intelligence
**For**: Ron Blake / LEGAL review
**Subject**: Bound Pair Credentials (BPC) — Prior Art, Market Signal, and Differentiation Gap Analysis

---

## Objective

Determine whether BPC's 5-layer credential architecture (hardware key + pair registry + user secret + anti-replay + anomaly detection) constitutes novel IP, identify the closest prior art, and assess the market opportunity.

---

## Prior Art Findings

### What Already Exists (Individual Components)

Every one of BPC's five layers exists in isolation. None are novel alone. The question is whether the specific combination is novel.

**Layer 1 — Device-Bound ECDSA P-256 Keys (Hardware)**

Hardware-bound non-extractable keys are well-established:

- **WebAuthn / FIDO2 Passkeys** (W3C WebAuthn Level 2/3 spec): Device-bound credentials using ECDSA P-256 generated inside TPM or Secure Enclave, non-extractable by design. The `extractable: false` flag in Web Crypto API `generateKey()` is a direct precedent. Adopted by Google, Apple, Microsoft. Passkeys now account for 62% of all authentication challenges (2025 data). **However**: passkeys are explicitly designed for human authentication via biometric verification. The FIDO Alliance specification states that AI agents and machines cannot and should not use passkeys directly — this is a deliberate design constraint, not an accident.

- **TPM 2.0 + ECDSA**: DoD, NSA, and TCG (Trusted Computing Group) have published specifications for TPM-bound device identity using ECDSA P-256. NSA's November 2024 guidance (PP-24-4228) covers TPM 2.0 use cases for device authentication.

- **ACME Device Attestation (ACME-DA)**: Hardware-bound certificates at scale — used for device identity, not API authentication specifically.

**Layer 2 — Anti-Replay (Nonce + Timestamp Window)**

Fully covered by existing standards:

- **RFC 9421 — HTTP Message Signatures** (published February 2024): Standardizes signing HTTP requests with ECDSA or HMAC, includes `created` and `expires` timestamp fields, supports nonce-equivalent mechanisms. Directly covers signed requests with timestamp-bounded validity.

- **AWS Signature Version 4 (SigV4)**: Production-grade replay protection using HMAC-SHA256 with timestamp and request-scoped signing. Uses `x-amz-date` header and ±15 minute validity window. SigV4a (multi-region) uses ECDSA P-256 specifically.

- **RFC 9449 — OAuth 2.0 DPoP** (Demonstrating Proof of Possession): Binds OAuth tokens to a specific JWK key pair at the application layer. Client generates a DPoP Proof JWT with method (htm), URI (htu), and a nonce (jti) — directly analogous to BPC's canonical request structure with pair_id, path, method, and nonce. DPoP became a full IETF RFC in 2023 and is in production at Auth0, Okta, and Azure AD.

**Layer 3 — HMAC User Secret Mixed Into Signature**

Covered in practice but less commonly standardized:

- HMAC-based API authentication (Oracle, AWS, many custom implementations) uses a shared secret mixed into request signing. The 2016 arXiv paper "A replay-attack resistant message authentication scheme using time-based keying hash functions and unique message identifiers" (arXiv:1602.02148) covers HMAC + nonce + timestamp as a combined scheme.

- The specific mechanic of mixing a **user-chosen** secret (never stored plaintext, never logged) as a second HMAC factor is not found as a standalone standard. It appears in some 2FA-style API implementations but is not formalized in IETF RFCs.

**Layer 4 — Pair Registry (Explicit Closed Set of Known Callers)**

Partially covered:

- **OAuth 2.0 client registration** and **GNAP (RFC 9635, published October 2024)**: Both require explicit client registration. GNAP in particular handles dynamic client keys without pre-registration — which is actually the inverse of BPC's approach (BPC requires pre-approved pairing; GNAP allows a client to provide a key as part of the first request). So BPC's closed-pair-registry model is stricter than GNAP and is not a match.

- **mTLS client certificate allowlists**: Server-side certificate pinning creates a similar closed set of allowed callers. However, mTLS does not have a "128-bit random pair ID" abstraction or an owner-approval-gated pairing flow.

- **Cloudflare Access / AWS IAM / HashiCorp Vault**: Support allowlisting of service accounts and IAM principals. Vault's AWS auth method supports `bound_iam_principal_arns`, which is analogous to a caller allowlist. These are infrastructure-level controls, not embedded protocol primitives.

**Layer 5 — Behavioral Anomaly Engine**

Exists as an add-on layer in commercial products, not embedded in auth protocols:

- **Akamai API Security** (acquired Noname Security for $450M in June 2024): ML-based behavioral anomaly detection, establishes traffic baselines, detects credential abuse, rate anomalies, and suspicious data access patterns. 200+ dynamic CI/CD security tests. Industry-leading but operates as a gateway/proxy layer, not as a credential primitive.

- **Salt Security, Wallarm**: Similar behavioral analytics products. None embed anomaly detection into the credential structure itself.

- **Okta Behavior Detection**: Behavioral authentication flagging for geographic anomalies and off-hours usage.

The critical distinction: every existing anomaly detection system operates **outside** the credential — as a network-level or gateway-level observer. BPC embeds anomaly-response capability as a property of the credential contract itself (probe attempts against the pair registry trigger the engine).

---

### Closest Existing Technologies

Ranked by total overlap with BPC's combined 5-layer design:

**1. OAuth 2.0 DPoP (RFC 9449) + mTLS**
- Covers: hardware-ish binding (key pair at application layer, not necessarily TPM), anti-replay (nonce/jti), request signing
- Missing: pair registry, user secret, anomaly engine, TPM/hardware enforcement
- Overlap score: ~2.5/5 layers

**2. AWS Signature Version 4 (SigV4)**
- Covers: HMAC request signing, timestamp/replay protection, method + path + body hash in canonical request
- Missing: hardware binding, pair registry, user secret as separate HMAC factor, anomaly engine
- Overlap score: ~2/5 layers (BPC's canonical request structure is structurally similar to SigV4's string-to-sign)
- **This is the most legally significant prior art for the signing mechanism specifically**

**3. RFC 9421 — HTTP Message Signatures**
- Covers: ECDSA or HMAC signing of HTTP components (method, path, headers), timestamp bounds
- Missing: hardware binding, pair registry, user secret, anomaly engine
- Overlap score: ~2/5 layers

**4. WebAuthn/FIDO2 Device-Bound Credentials**
- Covers: Hardware-bound ECDSA P-256, non-extractable keys, anti-replay (challenge/response)
- Missing: pair registry, user secret as HMAC factor, anomaly engine, machine-to-machine use case
- Overlap score: ~2/5 layers
- **Key gap**: FIDO2 is explicitly not designed for machine-to-machine API auth. BPC fills this specific gap.

**5. mTLS + API Gateway**
- Covers: client certificate auth (hardware-ish), server-side caller allowlist (CA-level)
- Missing: user secret, anti-replay at application layer, pair registry as protocol primitive, anomaly engine
- Overlap score: ~1.5/5 layers

---

### The Gap — What Doesn't Exist

After surveying IETF RFCs (9449/DPoP, 9421/HTTP Signatures, 9635/GNAP), WebAuthn Level 3, AWS SigV4, mTLS standards, and commercial products (Cloudflare Access, HashiCorp Vault, Akamai, Salt Security):

**No existing protocol, RFC, or commercial product combines all five of:**
1. Hardware-bound non-extractable key (TPM/Secure Enclave) for machine-to-machine API calls
2. Explicit owner-approved pair registry (closed set with approval gate, not open registration)
3. User-chosen secret mixed as a second HMAC factor into every signature
4. Application-layer nonce + timestamp anti-replay
5. Behavioral anomaly engine embedded as a credential-level primitive

The closest conceptual ancestor is DPoP + SigV4 combined, but even that pairing omits the pair registry, user secret, and anomaly integration. No academic paper or standard found that combines all five.

The Web Crypto API implementation detail — running real ECDSA P-256 signing inside the browser using `crypto.subtle` with `extractable: false` — is technically established, but applying it to machine-to-machine API authentication (as opposed to user login) is not addressed by any existing standard.

---

## Market Signal

### API Key Leak Problem (Data)

The scale of the problem is extreme and accelerating:

| Year | Leaked Secrets (GitHub) | Source |
|------|------------------------|--------|
| 2022 | ~9.0 million | GitGuardian baseline |
| 2023 | 12.8 million | GitGuardian State of Secrets Sprawl 2024 |
| 2024 | 39 million | GitHub Blog (April 2025 announcement) |
| 2025 | 28.65 million new additions | Snyk / GitGuardian 2026 report |

The 2024 spike to 39M is particularly significant — a 3x jump year-over-year. AI service credentials are the fastest-growing category, with 81% YoY increase in 2025 (Wiz/GitGuardian data). Wiz found that 65% of the Forbes AI 50 had leaked verified secrets on GitHub.

Real-world supply chain incidents directly validating BPC's threat model:
- **Axios npm compromise (March 2026)**: Malicious dependency injected into Axios 1.14.1 and 0.30.4 — any installed instance assumed to have all credentials stolen including API keys
- **Shai-Hulud Worm (September 2025)**: Self-replicating malware that stole npm tokens, used them to compromise 180+ packages, infected 25,000+ GitHub repositories; specifically targeted API keys and cloud credentials
- **UNC6426 nx npm attack (March 2026)**: Compromised four major open-source projects in 8 days, harvested cloud credentials, SSH keys, and CI/CD secrets — gained AWS admin access within 72 hours
- **xAI API key leak (July 2025)**: Developer at DOGE accidentally published private xAI API keys to GitHub

Every one of these attacks would have been neutralized by BPC's Layer 1 (non-extractable key) + Layer 3 (user secret never in env/logs) combination. Stolen `.env` files and `npm` supply chain exfiltration are the two top attack vectors — BPC's architecture directly defeats both.

### Developer Pain Points

Developer sentiment data:
- **Authorization issues now rank #1** on OWASP's API Security Top 10 (2025 report)
- **67% of organizations** consider generative AI applications a severe threat to API security (Curity 2025 survey)
- **60% believe** API integration for AI apps increases their attack surface
- Organizations losing **$94-186 billion annually** to vulnerable or insecure APIs (Akamai 2025 data)
- The **average breach cost $4.88 million** in 2024, with the majority involving compromised credentials (IBM/FIDO Alliance data)

The developer community has not found a satisfying solution: OAuth adds overhead and requires an auth server; mTLS requires certificate infrastructure most teams lack; static API keys are the path of least resistance despite being the most dangerous. BPC targets exactly this gap — harder than a static key to set up, but dramatically easier than mTLS, with security properties that exceed both.

### Enterprise Demand

Market scale signals:
- **API Security market**: Projected $10.89B in 2025 → $41.66B by 2034 (17.17% CAGR) (Precedence Research)
- **Zero Trust API Security market**: $4.05B in 2024 → $35.35B by 2032 (31.10% CAGR) (Data Bridge)
- **Large enterprises**: 60% of API security market share in 2024; BFSI sector holds 40% of that
- **Akamai's $450M acquisition of Noname** (June 2024) signals that behavioral API security is viewed as strategic enterprise infrastructure

Enterprise procurement focus: Zero-trust API auth, sender-constrained tokens, non-human identity management. BPC is positioned at the intersection of all three trends.

The emerging "non-human identity" (NHI) security category is particularly relevant — AI agents, CI/CD pipelines, and microservices are generating massive volumes of machine-to-machine API calls. No existing standard adequately addresses this with hardware-level credential binding. BPC is purpose-built for this.

---

## Competitive Analysis

### BPC vs Closest Competitors

| Property | Static API Key | OAuth 2.0 + DPoP | mTLS | AWS SigV4 | HTTP Signatures (RFC 9421) | BPC |
|----------|---------------|-------------------|------|-----------|---------------------------|-----|
| Hardware-bound key (TPM/Enclave) | No | No (software key) | Partial (can use HSM, not required) | No | No | Yes |
| Non-extractable private key | No | No | Partial | No | No | Yes |
| Explicit pair registry (owner-approved, closed set) | No | No (open client registration) | No (CA-based) | No | No | Yes |
| User-chosen secret as 2nd HMAC factor | No | No | No | No | No | Yes |
| Application-layer anti-replay (nonce + timestamp) | No | Yes (jti) | No | Yes | Yes | Yes |
| Body hash in signed payload | No | No | No | Yes | Yes | Yes |
| Behavioral anomaly engine as credential primitive | No | No | No | No | No | Yes |
| Machine-to-machine by design | Yes | Partial | Yes | Yes | Yes | Yes |
| Works in browser (Web Crypto API) | Yes | Partial | No | Partial | Partial | Yes |
| Defeats stolen env/log credential | No | No | Partial | No | No | Yes |
| Defeats npm supply-chain exfiltration | No | No | No | No | No | Yes |
| Dev setup complexity | Low | High | Very High | Medium | Medium | Medium |

**Key takeaway**: BPC is the only entry in this table with all three of: hardware binding, user secret factor, and pair registry. The combination of these three with anti-replay and anomaly detection is not covered by any single existing solution.

---

## NOVA Assessment

### Novelty Score: 7/10

**Rationale**: Each individual component scores 1-2/10 for novelty (all are established). The combination scores 7/10. The scoring is conservative because:
- The canonical request structure resembles SigV4 closely enough that a patent examiner will require careful claim differentiation
- DPoP (RFC 9449) covers key-bound token + nonce + method + URI signing — the overlap is real
- The "user secret HMAC" concept is the most original single element; closest prior art is 2FA schemes applied to API calls, not a direct match
- The pair registry with owner-approval gate is novel as a protocol primitive

What pushes the score above 5: No single protocol or commercial product combines all five layers. The machine-to-machine application of hardware-bound credentials is a genuine gap in FIDO2/WebAuthn. The explicit pair registry as a first-class credential property is not found in any standard reviewed.

### Strongest Differentiator

**The pair registry + user secret combination is the strongest patentable core.**

Specifically: a credential architecture where (a) every caller is pre-registered with a 128-bit pair ID requiring explicit owner approval, AND (b) a user-known secret is mixed via HMAC into every signature but never stored or transmitted in plaintext, AND (c) the server can detect probe attempts against unregistered pair IDs as a security signal.

This combination defeats the two most common real-world API credential attacks (stolen env/logs and supply chain exfiltration) simultaneously, in a way that no existing standard does.

Secondary differentiator: Dev/prod mode separation with step-up auth (30-second approval window) is a practical UX innovation not found in any existing protocol. It addresses the real developer behavior of using weak credentials in development and forgetting to harden for production.

### Risk of Prior Art Blocking

**Moderate risk on the signing mechanism. Low risk on the full 5-layer combination.**

Specific risks:
1. **SigV4 overlap**: BPC's canonical request (body_hash + method + nonce + pair_id + path + secret_hmac + timestamp) structurally mirrors SigV4's string-to-sign. Claims must be differentiated by the pair_id primitive and the hardware binding, not just the signing structure.
2. **DPoP overlap**: RFC 9449's DPoP Proof JWT (htm + htu + jti + public key) covers request-scoped key-bound token proof. Claims must be differentiated by the non-OAuth context, the pair registry, and the user secret.
3. **Web Crypto API**: The browser-based ECDSA P-256 implementation is a valid implementation detail but is not patentable on its own — it must be claimed as part of the system architecture.

Mitigation: Independent claims should center on the pair registry + user secret HMAC combination as the core novel architecture, with dependent claims on hardware binding, anomaly engine integration, and dev/prod mode separation.

### Market Opportunity Signal: STRONG

Three converging factors make this a strong commercial opportunity:
1. **Volume**: 39M leaked credentials in 2024 on GitHub alone — the problem is demonstrably massive and accelerating
2. **Timing**: AI-driven machine-to-machine API calls are exploding; no hardware-binding standard exists for this use case; FIDO explicitly excludes it
3. **Market**: $10.89B API security market in 2025 growing at 17-31% CAGR; enterprise buyers actively spending; Akamai's $450M Noname acquisition validates strategic value of behavioral API security

BPC's architecture is most defensible in the enterprise and high-security developer segments where the pain of static API keys is actively being felt. The npm supply chain attack pattern (Shai-Hulud, UNC6426, Axios) provides ready-made case studies that make the sales narrative concrete.

---

## Recommended Next Steps for LEGAL

**Priority 1 — Provisional Patent Filing (recommended within 30 days)**

File a provisional covering:
- The 5-layer credential architecture as a complete system claim
- The pair registry with owner-approval gate as a standalone claim
- The user-secret-HMAC-into-every-signature mechanism as a standalone claim
- The behavioral anomaly engine embedded as a credential-level primitive (vs. gateway-level observer)
- The dev/prod mode separation with step-up auth window

This establishes a priority date before further public disclosure (spec doc, demos, any GitHub publishing).

**Priority 2 — Prior Art Differentiation**

LEGAL must explicitly distinguish BPC from:
- RFC 9449 (DPoP): BPC is not OAuth-dependent; adds hardware binding and pair registry that DPoP lacks
- AWS SigV4: BPC adds hardware binding, pair registry, and user secret; SigV4 has no concept of any of these
- RFC 9421: HTTP Message Signatures cover the signing structure but not hardware binding, pair registry, or user secret

The safest claim framing: "A credential system for machine-to-machine API authentication comprising a hardware-bound non-extractable key, an owner-approved pair registry, and a user-derived HMAC factor combined in a single verifiable request signature" — this combination is not found in any reviewed prior art.

**Priority 3 — Trademark**

Register "BPC" and "Bound Pair Credentials" before any public launch. The protocol name is marketable and the category (hardware-bound API credentials for M2M) is currently unnamed in the market.

**Flag for LEGAL**: The spec doc footer says "Conceived by R. Blake" — ensure the working prototype and any related code commits are timestamped and preserved as evidence of conception date.

---

## Sources

- [RFC 9449 — OAuth 2.0 DPoP](https://datatracker.ietf.org/doc/html/rfc9449)
- [RFC 9421 — HTTP Message Signatures](https://datatracker.ietf.org/doc/rfc9421/)
- [RFC 9635 — GNAP (Grant Negotiation and Authorization Protocol)](https://datatracker.ietf.org/doc/rfc9635/)
- [W3C WebAuthn Level 2](https://www.w3.org/TR/webauthn-2/)
- [FIDO Alliance — Device-Bound Passkeys](https://fidoalliance.org/passkeys/)
- [Corbado — Device-Bound vs Synced Passkeys](https://www.corbado.com/blog/device-bound-synced-passkeys)
- [Corbado — AI Agents and Passkeys (machines cannot use passkeys)](https://www.corbado.com/blog/ai-agents-passkeys)
- [NSA/DoD TPM 2.0 Use Cases Guidance, November 2024](https://media.defense.gov/2024/Nov/06/2003579882/-1/-1/0/CSI-TPM-USE-CASES.PDF)
- [GitHub Blog — 39M Secret Leaks in 2024](https://github.blog/security/application-security/next-evolution-github-advanced-security/)
- [Snyk — 28M Credentials Leaked on GitHub in 2025](https://snyk.io/articles/state-of-secrets/")
- [GitGuardian State of Secrets Sprawl 2024](https://www.gitguardian.com/state-of-secrets-sprawl-report-2024)
- [Palo Alto Unit 42 — Shai-Hulud npm Worm](https://unit42.paloaltonetworks.com/npm-supply-chain-attack/)
- [The Hacker News — UNC6426 nx npm Supply Chain Attack, AWS Admin Access](https://thehackernews.com/2026/03/unc6426-exploits-nx-npm-supply-chain.html)
- [Wiz — Axios npm Compromise](https://wiz.io/blog/axios-npm-compromised-in-supply-chain-attack)
- [arXiv:1602.02148 — Replay-Attack Resistant HMAC with nonce + timestamp](https://arxiv.org/abs/1602.02148)
- [AWS SigV4 Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html)
- [Precedence Research — API Security Market $10.89B → $41.66B](https://www.precedenceresearch.com/api-security-and-management-market)
- [Data Bridge — API Zero Security Market $4.05B → $35.35B](https://www.databridgemarketresearch.com/reports/global-application-program-interfaces-api-zero-security-market)
- [Akamai — Noname Acquisition and Anomaly Detection](https://www.akamai.com/site/en/documents/white-paper/2024/anomaly-detection-in-akamai-api-security.pdf)
- [MDN Web Docs — SubtleCrypto sign() and generateKey()](https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/sign)
- [OpenBotAuth — RFC 9421 HTTP Message Signatures for Bot Auth](https://openbotauth.com/blog/http-message-signatures-rfc-9421-guide)
- [Auth0 — DPoP Implementation Guide](https://auth0.com/blog/protect-your-access-tokens-with-dpop/)
- [Akamai — API Security Trends 2025](https://www.akamai.com/blog/security/2025/jul/the-price-poor-cybersecurity-2024-31-billion)
- [Aembit — Anomaly Detection for Non-Human Identities](https://aembit.io/blog/anomaly-detection-non-human-identities/)
