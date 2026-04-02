# LEGAL: BPC — Bound Pair Credentials Patent Assessment

**Prepared by:** LEGAL Agent, PKA AI Team
**Date:** 2026-04-01
**Classification:** Attorney-Client Privileged Work Product — Draft for Review by Qualified Patent Counsel
**Status:** DRAFT. Not a filed document. Not legal advice.

**FILING WINDOW ALERT — READ FIRST:** If the HTML prototype document has been shared with any person outside Ron's control (email, GitHub, public URL, shared folder), the 12-month AIA grace period clock under 35 U.S.C. § 102(b)(1) has started. A provisional patent application should be filed within 30 days of this assessment to preserve the priority date regardless of disclosure status. The cost of a well-drafted provisional is approximately $1,500–$3,500 with counsel. Missing the window makes the prior disclosure itself prior art against the patent.

---

## Executive Summary

- BPC presents a **genuine multi-claim patent opportunity** with an overall patentability score of **7/10**. The combination claim and the explicit pair registry with approval gate are the strongest positions. The behavioral anomaly engine and secret-mixing technique are commercially valuable but face closer prior art pressure.
- The HTML prototype is implementable evidence of conception and reduction to practice, which is valuable for USPTO and litigation purposes — but it may also constitute a public disclosure if it has been shared. Establish immediately whether the document has left Ron's control. This answer determines whether the filing window is open or already running.
- **Recommended immediate action:** File a provisional patent application covering all six claim clusters within 30 days. Total outlay under $5,000 with a qualified patent prosecution attorney. Failure to file converts BPC's implemented novel architecture into free prior art for any company that reads it.

---

## Patentable Claims Analysis

### Claim 1: The 5-Layer Combined Authentication Method — STRONG

**Issue Identified:** The specific combination of (1) TPM/Secure Enclave non-extractable device binding, (2) explicit closed-set pair registry with owner approval gate, (3) user-secret HMAC injection into every signed payload, (4) nonce + timestamp anti-replay, and (5) per-pair behavioral anomaly detection — operated as a unified API authentication flow — is not replicated in any single prior art reference identified.

**Novelty Assessment:** Each individual element has prior art (discussed in Prior Art Risk Matrix below). What is novel is the specific combination and the particular way they interlock to create the "attacker must possess ALL simultaneously" property. This is a classic "combination patent" scenario. Under KSR Int'l Co. v. Teleflex Inc. (550 U.S. 398, 2007), combination patents face heightened non-obviousness scrutiny — the question is whether a person of ordinary skill in the art would have been motivated to combine these specific elements in this specific way. The argument here is that prior art in each layer addresses different threat models (FIDO2 addresses login, DPoP addresses OAuth token binding, AWS SigV4 addresses API auth without device binding) and that combining them in this configuration to address the API credential threat model specifically is not rendered obvious by any single reference or obvious combination of references.

**Utility:** Clear. The specification calls out npm supply chain attack resistance, social engineering resistance, and progressive friction — all commercially concrete benefits distinguishing from prior art solutions.

**Non-obviousness Argument:** The TPM binding applied specifically to API credentials (not login sessions) + the explicit pair registry as a finite closed set (not RBAC or OAuth scope) + the user-secret HMAC injected per-request (not a session-level secret) + behavioral anomaly at the per-pair level (not per-user or per-IP) is a specific architectural configuration not present in any identified prior art. The combination's purpose — making a stolen credential useless from any device other than the originating TPM — is architecturally novel in the API authentication context.

**Recommended Independent Claim Language (sketch — requires attorney refinement):**

> A computer-implemented method for API authentication comprising: generating an asymmetric key pair on a hardware security module resident on a client device, wherein the private key is designated non-extractable and cannot be exported from the hardware security module; registering a pair identifier with an authorization server via an explicit owner-approval workflow, wherein the set of authorized pair identifiers is a finite closed set requiring affirmative owner action to expand; receiving, from a user, a secret value that is never stored in plaintext and never transmitted outside a local cryptographic operation; for each API request, constructing a canonical signed payload that includes: a hash of the request body, the HTTP method, a cryptographically random nonce, the pair identifier, the request path, an HMAC value derived from the user secret and the nonce combined with a current timestamp, and the timestamp value; signing the canonical payload using the non-extractable private key; transmitting the signed payload and signature in request headers; and at the authorization server, verifying the signature against the registered public key for the pair identifier, validating the nonce has not been previously received within a defined temporal window, validating the timestamp falls within a defined tolerance, and validating behavioral patterns associated with the pair identifier against an established baseline; wherein authentication succeeds only when all verification steps pass.

---

### Claim 2: Secret Mixing Technique (HMAC into Canonical Payload) — MODERATE

**Issue Identified:** The specific technique of computing `HMAC(user_secret, nonce + timestamp)` and injecting the result as a field within the signed payload — so that the user secret is a cryptographic factor bound to every individual request without being transmitted, stored, or loggable — is a distinct technique claim.

**Novelty Assessment:** AWS SigV4 uses HMAC-SHA256 over a canonical request, but the "signing key" is derived from AWS credentials and date, not from a user-chosen secret that is never stored. DPoP uses a key-bound proof but does not mix a user secret into every proof. FIDO2 uses a PIN for device unlock but the PIN is not cryptographically mixed into each individual assertion signature. The specific construction here — user secret as an HMAC input, not as an authentication factor checked separately, but as a binding element baked into the very thing the device key signs — is the novel element.

**Non-obviousness Argument:** Moderate. The individual cryptographic primitives (HMAC, nonce, timestamp) are well-known. The argument must be that the specific construction — injecting a per-request user-secret HMAC into the payload that the hardware-bound key signs, such that neither the hardware key alone nor the user secret alone is sufficient — represents a non-obvious combination that achieves the "two physically separate secrets bound in every signature" property. This is a narrower novelty argument than Claim 1, and the claim must be drafted narrowly enough to avoid reading on prior art while broadly enough to have commercial value.

**Risk:** A patent examiner may argue this is an obvious combination of well-known HMAC techniques. The response argument relies on the specific purpose (binding a user-chosen secret to a hardware-bound key signature without storing or transmitting the secret) and the specific location of the HMAC result (inside the signed canonical request, not as a separate header or separate auth factor).

**Recommended Dependent Claim Language (sketch):**

> The method of Claim 1, wherein constructing the HMAC value comprises: accepting a user-supplied secret value at runtime without persisting the secret value to any storage medium and without transmitting the secret value over any network connection; computing a keyed hash of a concatenation of the nonce and timestamp using the user-supplied secret value as the key; and including the keyed hash result as a field in the canonical payload prior to signing with the non-extractable private key; whereby the authorization server cannot verify authenticity of a request without both the non-extractable private key resident on the client device hardware security module and knowledge of the user-supplied secret value, and neither factor alone is sufficient.

---

### Claim 3: Explicit Pair Registry with Mandatory Owner Approval Gate — STRONG

**Issue Identified:** The model of API credential authorization as a finite closed set of explicitly approved pairs — where each new pairing requires affirmative owner approval and pairing never occurs automatically — is distinct from every identified prior art approach. OAuth scopes, API keys, and certificate-based auth all operate on permission models but none implement a finite closed-set pair registry with an owner approval gate as a structural property of the authentication system.

**Novelty Assessment:** This is the most commercially distinctive element of BPC. The security value proposition — that social engineering attacks fail because an attacker cannot trick the system into creating a new authorized pair without the owner's explicit approval — is directly tied to this architectural choice. No identified prior art implements "finite closed set of callers, new pairings require owner approval, never automatic" as a first-class authentication primitive for APIs.

**Non-obviousness Argument:** Strong. The natural prior art comparison is OAuth client registration — but OAuth client registration does not require owner approval per-pairing, does not create a finite closed set enforced at the crypto layer, and allows automated client credential issuance in many configurations. The difference is structural and purposeful: BPC's pair registry is not an administrative list but a cryptographically enforced boundary. The argument that the social engineering resistance property emerges specifically from the combination of closed-set enforcement and mandatory owner approval is novel.

**Recommended Independent Claim Language (sketch):**

> A system for API access control comprising: a pair registry data store maintaining a finite set of authorized pair identifiers, wherein each pair identifier is associated with a public key of a registered client device; an approval workflow module configured to require affirmative authorization from a designated owner before any new pair identifier is added to the finite set, and wherein the approval workflow cannot be bypassed by automated processes or by client-side requests; and an authentication module configured to reject any API request from a client presenting a pair identifier not present in the finite set, regardless of cryptographic signature validity; wherein the system enforces that the total number of authorized callers is bounded by explicit human approval actions and cannot grow through automated credential issuance.

---

### Claim 4: Step-Up Approval with Timed Modal for Sensitive Operations — MODERATE

**Issue Identified:** The design-time classification of API operations into sensitivity tiers, combined with a runtime timed approval modal (30-second countdown) and an out-of-band confirmation option, applied specifically to API credential authentication (not user login), constitutes a potentially patentable UI/UX + method combination.

**Novelty Assessment:** Step-up authentication exists broadly (banking OTP, Google Workspace step-up, etc.). The novel elements here are: (1) the application to API-level credentials rather than user login flows, (2) the timed modal with explicit countdown creating a defined approval window, (3) the out-of-band confirmation channel as an alternative to the modal, and (4) the separation between dev/prod modes where the step-up requirement is configurable per environment. The combination in the API credential context is distinctive.

**Risk:** Moderate-High. Step-up authentication is a well-traveled space. The claim must be scoped specifically to the API credential context and the specific modal + countdown + out-of-band combination to avoid reading on existing patents from Duo Security (Cisco), Okta, or similar MFA vendors. An exhaustive freedom-to-operate search (FTO) against Cisco/Duo and Okta patent portfolios is required before any independent claim on this element. This is the one element where LEGAL recommends an FTO search before committing attorney time to prosecution.

**Non-obviousness Argument:** The argument is that step-up authentication in the user login context is known, but applying it to API-level credential authorization — where the "user" approving is the API owner, not the end user — in combination with a bounded countdown timer and alternative confirmation channel is not rendered obvious by existing step-up MFA patents because those patents address user authentication, not API credential authorization.

**Recommended Dependent Claim Language (sketch):**

> The system of Claim 3, further comprising: an operation sensitivity classifier configured to assign a sensitivity tier to each API operation at design time; a step-up authorization module configured, upon receiving a request for a high-sensitivity operation, to initiate an approval workflow comprising: presenting a time-bounded approval interface displaying the requested operation, the requesting pair identifier, and a countdown timer of a defined duration; accepting an approval or denial input within the countdown timer duration; and providing an alternative out-of-band confirmation channel as an alternative to the approval interface; and wherein the step-up authorization module denies the high-sensitivity request if no approval is received within the countdown timer duration.

---

### Claim 5: Behavioral Anomaly Engine for Per-Pair API Authentication — MODERATE

**Issue Identified:** A behavioral anomaly detection system that establishes a per-pair-identifier baseline (not per-IP, not per-user, not per-account) and flags anomalies including unknown pair attempts, signature failure patterns, and traffic pattern deviations — integrated directly into the API authentication layer rather than as a separate network security layer — is a distinct system claim.

**Novelty Assessment:** Behavioral anomaly detection for API security exists broadly (Cloudflare Bot Management, Akamai, Apigee, AWS WAF, Darktrace, etc.). The novel element is the scope of the baseline: per-pair-identifier. Because BPC's pair IDs are device-and-key-bound, a per-pair baseline tracks the behavioral profile of a specific device-key-user combination, not just an IP address or account. This is a narrower and more precise behavioral unit than existing approaches.

**Risk:** The prior art in behavioral API security is dense. The claim must be scoped precisely to the per-pair-identifier baseline as the novel element. If drafted broadly as "behavioral anomaly detection for APIs," it will be rejected immediately on prior art. The defensible position is the specific choice of pair identifier as the behavioral unit and the integration of anomaly detection into the authentication decision (not as a separate alerting layer).

**Prior Art to Search Before Filing:** Cloudflare's patent portfolio on bot behavioral detection, Akamai's API security patents, and Darktrace's pattern of life analysis patents. Any overlap requires claim differentiation. LEGAL recommends a targeted prior art search on these specific entities before committing to this as an independent claim. Budget $1,500–$2,500 for a professional prior art search.

**Recommended Dependent Claim Language (sketch):**

> The system of Claim 1, further comprising: a behavioral analysis module configured to maintain, for each pair identifier in the pair registry, a behavioral baseline comprising: a temporal distribution of request arrival times, a distribution of API operations requested, and a historical count of signature verification failures; and to flag, as anomalous, any of: a request from a pair identifier not present in the pair registry; a rate of signature verification failures exceeding a defined threshold for a given pair identifier; a traffic pattern for a given pair identifier deviating from the established behavioral baseline by a defined statistical threshold; and wherein the authentication module incorporates anomaly flags from the behavioral analysis module into the authentication decision for each request.

---

### Claim 6: Dev/Prod Mode Credential Separation with Configurable Enforcement Tiers — WEAK (as independent claim) / MODERATE (as dependent claim)

**Issue Identified:** The same credential architecture operating under different enforcement tiers (dev = permissive limits, no approval prompts; prod = step-up required, strict limits) with explicit mode separation is a system design claim.

**Novelty Assessment:** Environment-tiered security configurations are extremely common in software development (development vs. production environments, feature flags, environment variables controlling auth behavior). This is the weakest of the six claim clusters as an independent patent claim because the concept of configuring different security enforcement levels per environment is well-established.

**Non-obviousness Problem:** The argument that applying dev/prod mode separation to API credential enforcement tiers is non-obvious is difficult to sustain against the enormous prior art body of environment-aware configuration systems. This is unlikely to survive as an independent claim.

**Recommendation:** Do not pursue as an independent claim. Include as a dependent claim attached to Claim 1 or Claim 3 to add breadth to the patent family without creating a standalone weak claim that could be used to invalidate other claims.

**Recommended Dependent Claim Language (sketch):**

> The system of Claim 1, wherein the authentication module operates in a first enforcement mode and a second enforcement mode, wherein the first enforcement mode applies relaxed rate limits and suppresses step-up authorization requirements, and the second enforcement mode enforces rate limits and requires step-up authorization for operations classified as high-sensitivity, and wherein the active enforcement mode is determined by a configuration setting that is not modifiable by a requesting client.

---

## Prior Art Risk Matrix

| Prior Art | Overlap Area | BPC Differentiation | Risk Level |
|-----------|-------------|--------------------|-|
| FIDO2 / WebAuthn (W3C Recommendation) | Device-bound asymmetric key; TPM/Secure Enclave; non-extractable private key; nonce-based replay prevention | FIDO2 is for user authentication (login), not API credential authorization. FIDO2 does not implement a pair registry, does not inject user secrets into assertion signatures, and does not include per-pair behavioral monitoring. The threat model is different: FIDO2 solves "prove you are the account owner at login"; BPC solves "prove this specific device-key-user combination is an authorized API caller on every request." | MEDIUM — Claims must be explicitly scoped to API credential context, not login authentication. Examiner will cite FIDO2 for device binding. Response argument is application domain and architectural combination. |
| RFC 9421 (HTTP Message Signatures, formerly draft-ietf-httpbis-message-signatures) | Signing HTTP requests with asymmetric keys; canonical request format; signature components | RFC 9421 defines a signing format but does not specify device binding, does not define a pair registry, does not require a user secret factor, and does not include behavioral anomaly detection. BPC's canonical request structure is inspired by this space but the authentication system built around it is distinct. | LOW-MEDIUM — The canonical request format is similar in concept to HTTP Signatures. Claims must focus on the system and method, not the wire format alone. The wire format alone is not patentable; the system that uses it is. |
| RFC 9449 (DPoP — Demonstrating Proof of Possession) | Key-bound OAuth tokens; proof-of-possession JWTs per request; nonce | DPoP binds an OAuth access token to a key pair to prevent token theft. DPoP does not require TPM/hardware binding (software keys are permitted), does not implement a pair registry with owner approval, does not inject a user secret, and does not include behavioral monitoring. DPoP is OAuth-layer; BPC is application-layer API auth. | MEDIUM — DPoP is the closest prior art to BPC's key-binding concept. Independent claim must clearly differentiate on: (1) hardware binding requirement (not just software key), (2) pair registry with owner approval, (3) user secret HMAC, (4) behavioral monitoring. All four differentiate BPC from DPoP. |
| AWS SigV4 | HMAC-based request signing; canonical request format; timestamp + nonce anti-replay; per-request signature | AWS SigV4 uses HMAC of a canonical request. The "signing key" is derived from AWS credentials (access key, secret key, date, region, service) — not from a hardware-bound asymmetric key and not from a user-chosen runtime secret. SigV4 has no pair registry, no device binding, and no behavioral anomaly layer. | LOW — SigV4 demonstrates that per-request HMAC signing of canonical requests is known. Claim 2's secret-mixing technique must clearly differentiate by specifying the hardware-bound key signature over the HMAC result (not HMAC alone) and the user-secret-never-stored construction. |
| Google Service Account / JSON Key auth | Asymmetric key pairs for service authentication; service account registration | Google service accounts use RSA/EC key pairs but keys are software-stored JSON files (extractable). There is no pair registry with owner approval gate, no user secret factor, no anti-replay nonce system, and no behavioral monitoring. | LOW — Useful to distinguish in the specification. Does not pose prior art rejection risk for the combination claim. |
| GNAP (Group Needs Access Protocol, draft-ietf-gnap-core-protocol) | Next-generation OAuth; explicit user approval for access grants; key binding | GNAP includes a concept of explicit interaction patterns for access grant approval. GNAP's key binding is conceptually related to BPC's pair registry concept. However, GNAP operates at the OAuth/delegation layer, not at the per-request API authentication layer, and does not include user-secret HMAC injection or behavioral monitoring. | MEDIUM — The Examiner may cite GNAP for the approval-gate concept. Response argument: GNAP's grant approval is for OAuth scopes at the application level, not for registering a specific device-key binding into a finite closed set at the API authentication layer. |
| Behavioral API Security (Cloudflare Bot Management, Akamai, Imperva, Darktrace) | Behavioral baseline for API traffic; anomaly detection; per-entity profiling | These systems establish behavioral baselines at the IP, ASN, user-agent, or account level — not at the pair-identifier level. The pair identifier in BPC is a unique primitive that does not exist in these systems because those systems do not implement a pair registry. The per-pair behavioral baseline is only possible because the pair ID is a stable, hardware-bound, owner-approved entity — which these systems do not have. | MEDIUM — Claim 5 faces the densest prior art. Must be drafted to claim the per-pair-identifier behavioral unit as the novel element, not behavioral anomaly detection generally. Professional prior art search strongly recommended before committing to Claim 5 as an independent claim. |
| Duo Security / Okta step-up authentication patents | Step-up authentication triggers; risk-based auth; time-bounded approval windows | These patents address user authentication step-up (MFA prompts during user login/session elevation). BPC applies step-up to API credential authorization — a different actor (the API owner, not the end user) approving a different action (a specific API operation, not a login session). Domain distinction is the primary differentiation argument. | MEDIUM — FTO search against Cisco (Duo) and Okta patent portfolios required before prosecuting Claim 4 as an independent claim. This is a blocking research task before filing the non-provisional. |

---

## Filing Strategy

### Recommended Approach

File a provisional patent application within 30 days covering all six claim clusters. A well-drafted provisional establishes the priority date without requiring claims in final form, gives 12 months to refine the non-provisional, and costs significantly less than a full utility application. The priority date established by the provisional is the date that matters for prior art cutoffs — every day of delay increases the window in which a competitor could independently file and establish an earlier priority date.

Engage a qualified patent prosecution attorney with software and cryptographic system experience. LEGAL identifies issues and recommends action — prosecution of a patent application requires a registered USPTO practitioner (patent attorney or patent agent). Budget guidance: $1,500–$3,500 for a well-drafted provisional; $8,000–$18,000 for the subsequent non-provisional with full claim prosecution.

### Filing Window

**Status: Unknown — must be determined immediately.**

The filing window question turns on a single factual issue: has the HTML prototype document, or any written description enabling a person skilled in the art to practice BPC, been shared outside Ron's direct control? This includes:
- Any email to a collaborator, developer, or advisor that includes or describes the protocol
- Any GitHub repository (public or private with third-party access) containing the prototype or specification
- Any public post, forum discussion, or technical writeup describing the protocol
- Any demo to a third party that was accompanied by written materials

If the answer is NO — the document has never left Ron's control: the 12-month AIA clock has not started. File the provisional and the priority date will be the filing date.

If the answer is YES — and the disclosure occurred less than 12 months ago: the grace period under 35 U.S.C. § 102(b)(1) is running. The provisional must be filed before the 12-month anniversary of the first enabling disclosure. Determine the earliest disclosure date and subtract from today (2026-04-01) to determine remaining runway.

If the answer is YES — and the disclosure occurred more than 12 months ago: US patent rights may be lost. PCT (international) filing under EPC Article 54(2) also bars post-disclosure filing. This would be a critical finding requiring immediate counsel engagement to determine any remaining path.

**Action required: Audit all communications and repositories for BPC-enabling disclosures within the next 72 hours. Report the earliest disclosure date to patent counsel before any other filing step.**

### Claim Hierarchy (Independent to Dependent)

**Patent Application 1 (Core System — recommended as primary application):**

Independent Claim 1: The 5-layer combined authentication method (Claim 1 above — the broadest claim, most defensible combination)

Dependent on Claim 1:
- Claim 2: The secret-mixing technique (HMAC user secret into signed payload)
- Claim 3: The explicit pair registry with owner approval gate
- Claim 4 (dependent on Claim 3): Step-up approval with timed modal for sensitive operations
- Claim 5 (dependent on Claim 1): Behavioral anomaly engine scoped to per-pair identifier baseline
- Claim 6 (dependent on Claim 1): Dev/prod mode enforcement tier separation

**Patent Application 2 (Pair Registry System — recommended as continuation application after provisional):**

File as a continuation-in-part (CIP) or divisional after the non-provisional prosecution begins if the pair registry (Claim 3) gets narrowed during prosecution. A standalone system claim on the pair registry with owner approval gate has independent commercial value (licensing to API gateway vendors, identity providers) and should be protected with its own independent claim if the primary application's independent claim is narrowed in prosecution.

### Split vs. Unified Filing

File unified in the provisional. The provisional does not require formal claims — it requires an enabling description. One provisional filing covering all six claim clusters costs the same as one provisional and starts one priority date. Splitting into separate applications is a decision for the non-provisional stage, after claim examination begins and any restriction requirements from the USPTO examiner identify which claims may be forced into separate applications by the examiner anyway.

Recommended split for the non-provisional stage (file 12 months after provisional):

**Application A — Apparatus and Method:** Claims 1, 2, 3, 6 (core authentication system and method)
**Application B — Behavioral Security System:** Claim 5 (if Claim 5 survives the professional prior art search as independently defensible)
**Application C — User Interaction Method for API Authorization:** Claim 4 (if the FTO search against Duo/Okta clears)

This split maximizes examination success probability by keeping each application focused, and creates a patent family that is harder to design around than a single broad patent.

### International Filing Consideration (PCT)

PCT filing is warranted if BPC is intended for commercial licensing or product integration at international scale. The PCT application must be filed within 12 months of the provisional (or 18 months for Chapter II examination). Budget $5,000–$12,000 in additional fees for PCT filing. The commercial justification: API authentication protocols are global in application. A granted US patent without PCT protection can be designed around by non-US implementations. If BPC is licensed to API gateway vendors, authentication platforms, or enterprise security vendors — any of which operate globally — PCT protection is commercially justified.

Priority national phase entries recommended: United States (already covered), European Patent Office (covers 38 member states), United Kingdom (post-Brexit separate filing), Japan, Canada, and Australia. Total budget for national phase entry across these jurisdictions: $25,000–$50,000 over 30 months. This is a later decision but must be budgeted now.

---

## Risk Factors

### Alice/Mayo Abstract Idea Rejection Risk

**Risk Level: High — must be addressed in claim drafting.**

35 U.S.C. § 101 under Alice Corp. v. CLS Bank Int'l (573 U.S. 208, 2014) requires that software patent claims not be directed to an abstract idea without an "inventive concept" that transforms the claim into patent-eligible subject matter. The USPTO has applied Alice aggressively to cryptographic and authentication software claims.

The Alice risk for BPC is real. A claim drafted as "a method for authenticating an API request using multiple security factors" is likely abstract. The mitigation strategy is to draft claims that anchor every element to a specific physical or technical implementation:

1. "Non-extractable private key generated in a hardware security module" — the TPM/Secure Enclave specificity grounds the claim in a specific machine component, not an abstract cryptographic concept.
2. "Finite closed set enforced at the authentication module" — the structural property (finiteness, closure) is a concrete system constraint, not an abstract access control concept.
3. "HMAC value computed from user-supplied runtime secret without persisting the secret" — the "without persisting" constraint is a concrete technical limitation on system behavior, not an abstract idea.
4. "Behavioral baseline maintained per pair identifier in the pair registry" — the per-pair-ID scope is a concrete data structure and measurement unit, not an abstract monitoring concept.

Every claim must begin from the hardware (TPM) and proceed to the system consequences of that hardware binding. Claims that can be practiced purely in software without a TPM are at higher Alice risk. Claims that require a hardware security module as a structural element are at lower Alice risk because the hardware module is a specific machine, not an abstract concept.

**Claim drafting instruction for counsel:** Draft all independent claims to require a hardware security module as a structural component. This is both technically accurate (BPC requires a TPM or Secure Enclave) and strategically sound for Alice avoidance.

### How to Structure Claims for Maximum USPTO Approval Probability

1. Lead with apparatus claims (a system comprising...) before method claims where the apparatus grounding is strongest. Apparatus claims are somewhat more robust to Alice rejections than pure method claims.
2. Include a Beauregard claim (computer-readable medium storing instructions) as a dependent or parallel claim, but do not lead with it — it is the weakest form for Alice purposes.
3. Each claim element must have a concrete technical function, not a functional result description. "An authentication module configured to verify a cryptographic signature" is stronger than "means for authenticating."
4. Keep independent claims as broad as the differentiation from prior art allows, then add the specific novel elements as dependent claims. This preserves the broadest possible protection while ensuring at least the dependent claims survive prosecution.
5. Anticipate the FIDO2 and DPoP rejections in the response strategy before they arrive. Prepare a claim chart showing element-by-element why FIDO2 and DPoP do not anticipate or render obvious the combination.

### Licensing Value if Granted

A granted BPC patent family has meaningful licensing value in the following addressable markets:

**API Gateway Vendors:** AWS API Gateway, Azure API Management, Google Apigee, Kong, Traefik. Any of these vendors adding device-bound API credentials as a feature would read on the Claim 3 pair registry patent. Licensing royalty basis: per-API-call or per-enterprise-customer.

**Identity and Access Management Platforms:** Okta, Auth0 (Okta), Ping Identity, ForgeRock, CyberArk. The step-up approval claim (Claim 4, after FTO clearance) and the pair registry claim (Claim 3) have licensing relevance to IAM vendors building API security features.

**Zero-Trust Security Vendors:** Cloudflare Access, Zscaler, Palo Alto Prisma Access. The behavioral anomaly engine (Claim 5) and the device-bound API credential system (Claim 1) have licensing relevance to zero-trust vendors who are extending device trust to API-level authorization.

**Enterprise Developer Security Tools:** Snyk, GitHub Advanced Security, Veracode. The npm supply chain attack resistance angle (device-bound keys that are useless when stolen from another device) has commercial relevance to supply chain security vendors.

Conservative licensing value estimate for a granted US patent family on Claims 1 and 3: $500,000–$5,000,000 NPV over a 15-year patent life, assuming a 0.5%–2% royalty rate on addressable implementation revenues across the top-5 API gateway vendors. This is a rough estimate only — a qualified IP valuation firm is required for investor or licensing-negotiation purposes.

---

## LEGAL Verdict

**Overall Patentability Score: 7/10**

BPC is a genuinely novel architecture with real commercial protection value. The explicit pair registry with owner approval (Claim 3) and the full 5-layer combined system (Claim 1) are the strongest independent claims. The secret-mixing technique (Claim 2) and behavioral engine (Claim 5) have value as dependent claims. The step-up modal (Claim 4) requires an FTO search before committing to as an independent claim. Dev/Prod mode separation (Claim 6) is a dependent claim only.

**Recommended Immediate Action (ordered by priority):**

1. **Within 72 hours:** Audit all prior disclosures of BPC. Determine whether the HTML prototype or any enabling description has been shared with any third party. Report the earliest disclosure date to patent counsel. This single determination governs all subsequent filing decisions.

2. **Within 30 days:** Engage a qualified patent prosecution attorney with software and cryptographic system experience. File a provisional patent application covering all six claim clusters. The provisional must include: the full BPC specification, the canonical request structure, the Web Crypto API implementation details, the pair registry data model, the behavioral anomaly engine specification, and the dev/prod mode design. Budget $1,500–$3,500 for attorney fees.

3. **Within 60 days:** Commission a professional prior art search targeting Claim 5 (behavioral anomaly engine) and Claim 4 (step-up approval modal), specifically against Cloudflare, Duo Security (Cisco), Okta, Akamai, and Darktrace patent portfolios. Budget $3,000–$5,000. Results determine whether Claims 4 and 5 are filed as independent claims in the non-provisional.

4. **Within 12 months of provisional filing:** File the non-provisional patent application with full claim sets. Split into Application A (Claims 1, 2, 3, 6) and Application B (Claim 5, if prior art search clears) per the strategy above. Evaluate Claim 4 filing after FTO results.

5. **Within 12 months of provisional filing:** Make the PCT filing decision based on commercialization progress. If BPC is being licensed or integrated into a commercial product with international customers, file PCT simultaneously with the non-provisional.

**Red Flags:**

- **Disclosure audit is the single highest-priority action.** If the HTML prototype was committed to a public GitHub repository at any time, or shared in any public forum, the patent window may already be running or closed. This is not hypothetical risk — it is a dispositive factual question.
- **Do not publish BPC publicly** (blog post, conference talk, GitHub publication, open-source release) until the provisional is filed. Any such publication before filing irrevocably starts the 12-month AIA clock and may eliminate international rights under EPC, which has no grace period.
- **No attorney has reviewed this document.** LEGAL identifies issues and recommends engagement of qualified legal counsel. Nothing in this assessment constitutes legal advice or establishes an attorney-client relationship. All filing decisions, claim language, and prosecution strategy must be reviewed and executed by a registered USPTO practitioner before any document is filed.
- **The NLF/DMS provisional filing window is also running (see LEGAL-patent-provisionals-NLF-DMS.md).** BPC adds a third urgent filing to the queue. Ron should confirm with patent counsel that NLF, DMS, and BPC can be filed within a coordinated 30-day window to avoid any one filing crowding out another.

---

*LEGAL does not practice law. This document identifies issues, assesses risk levels, and recommends engagement of qualified legal counsel. Engage a registered USPTO patent practitioner before any filing action. Do not publicly disclose BPC before a provisional application is filed.*

*LEGAL — IP Strategy, Patents and Legal Risk*
*PKA AI Team — 2026-04-01*
