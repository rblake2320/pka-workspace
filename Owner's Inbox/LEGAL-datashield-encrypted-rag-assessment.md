# LEGAL Assessment: DataShield — Encrypted RAG Architecture
# CCPA / GDPR Compliance for PII Search Under NVIDIA Cyborg RAG Blueprint

**Prepared by**: LEGAL Agent
**Date**: 2026-03-26
**Classification**: Attorney-Client Privileged Work Product (Retain counsel before filing or publishing)
**Urgency**: High — architecture decisions being made now will lock compliance posture at launch

---

## VERDICT FIRST

**Safest architecture for DataShield's RAG knowledge layer, compliant today without a legal opinion before shipping:**

> Run all embedding models on-premises (RTX 5090 or Spark-1 GB10). Store embedding vectors in a local pgvector instance with AES-256-GCM encryption at the column level. Do NOT embed raw PII fields — embed only de-identified case summaries, outcome patterns, and procedural metadata. Treat any vector derived from PII as personal data under both CCPA and GDPR until regulatory guidance explicitly says otherwise.

This path eliminates the third-party disclosure problem, eliminates the GDPR Article 28 processor trigger, keeps you inside your existing AES-256-GCM envelope, and survives the strictest state floor (Washington My Health MY Data Act). You can ship it now. NVIDIA cloud APIs can be added later once a DPA is executed and the embedding-vector-as-PII question gets regulatory clarification (expected 2026-2027 from EDPB).

What the "encryption in use" / TEE path gives you: better search performance and the ability to embed actual PII fields. What it costs: regulatory uncertainty, a vendor DPA requirement, and a defensibility argument you would have to win in court rather than point to a safe harbor. DataShield is a PII-handling platform — you do not want to test novel legal theories on your own product.

---

## SECTION 1 — CCPA: Do Embedding Vectors Trigger Notification Requirements?

### 1.1 Are Embedding Vectors "Personal Information" Under CCPA?

**Answer: Yes, with high confidence. Treat them as personal information.**

Cal. Civ. Code § 1798.140(v)(1) defines "personal information" as information that "identifies, relates to, describes, is reasonably capable of being associated with, or could reasonably be linked, directly or indirectly, with a particular consumer or household."

The phrase "reasonably capable of being associated with" is the operative clause. Dense embedding vectors (768-dim or larger) generated from PII text — names, addresses, dates of birth — encode semantic features of that PII. Multiple published research papers (Carlini et al. 2021, 2022; Song & Raghunathan 2020) demonstrate that training data and input text can be recovered from model embeddings with non-trivial success rates. A vector generated from "John Smith, DOB 1985-04-12, 4521 Oak Ave" is "reasonably capable of being associated with" John Smith.

CPRA (effective January 2023) reinforced this by adding Cal. Civ. Code § 1798.140(ae) defining "sensitive personal information" — a subset that includes SSNs, precise geolocation, and contents of communications. The CPRA also added a new consumer right to limit the use of sensitive personal information (§ 1798.121). SSN last-4 digits stored in DataShield almost certainly qualify as sensitive personal information.

**The embedding of sensitive personal information creates a new category of regulated data the moment the vector is persisted.** There is no CCPA provision that treats the output of an embedding function as anonymized data by operation of law.

### 1.2 Does the CCPA Encryption Safe Harbor Apply to Embedding Vectors?

**Answer: No, with high confidence.**

Cal. Civ. Code § 1798.150(a)(1) provides that a business is not liable for a data breach notification if the personal information was "encrypted." The safe harbor is specifically a breach notification exception — it does not make encrypted data exempt from all CCPA obligations. It only means a breach of encrypted data that does not also expose the decryption key does not trigger § 1798.150(a) civil liability.

But the deeper problem: embedding vectors are not encrypted data in the sense the statute means. An embedding vector is a derived artifact — it is a transformation of decrypted PII into a float vector. If the vector database is breached, the safe harbor does not apply because the vectors were never "encrypted" in the statutory sense. They were computed in cleartext (even if briefly in a TEE) and stored as float arrays. Storing those floats under AES-256-GCM encryption at rest means the stored form is encrypted — but the vector itself is still a decryption-derived artifact. A breach that exposes the vector store encryption key exposes recoverable-PII-adjacent data.

**Conclusion**: The § 1798.150 safe harbor applies to DataShield's existing AES-256-GCM field encryption. It does not extend to embedding vectors derived from that PII, even if those vectors are themselves stored encrypted.

### 1.3 Does Using NVIDIA Cloud APIs Constitute a "Disclosure" Under CCPA?

**Answer: Yes, under the service provider exception only — which requires a written contract.**

CCPA § 1798.140(ag) defines "service provider" as a business that processes personal information on behalf of a business pursuant to a written contract that prohibits the service provider from retaining, using, or disclosing personal information for any purpose other than performing the services. If DataShield sends PII (or PII-derived embeddings) to NVIDIA NIM endpoints without that contract, NVIDIA is not a "service provider" — it is a "third party" under § 1798.140(ah), and the disclosure is a "sale" or "sharing" of personal information triggering consumer opt-out rights under § 1798.120.

**Sending PII to NVIDIA NIM without a written service provider agreement is a CCPA violation.** Sending embedding vectors to NVIDIA NIM without a written agreement may also be a violation, depending on whether those vectors are classified as personal information (see 1.1 above — LEGAL's position is that they should be treated as personal information).

---

## SECTION 2 — GDPR: Pseudonymization vs. Anonymization of Embedding Vectors

### 2.1 Are Embedding Vectors Personal Data Under GDPR Article 4(1)?

**Answer: Almost certainly yes — treat them as personal data.**

GDPR Article 4(1) defines personal data as "any information relating to an identified or identifiable natural person." Recital 26 explains that to determine identifiability, account should be taken of "all the means reasonably likely to be used" including "singling out." Recital 26 also states that anonymization requires that re-identification be "reasonably" impossible.

The current state of embedding inversion research does not permit the claim that 768-dim dense vectors from PII text are anonymized under Recital 26. Membership inference attacks and embedding inversion attacks are published, reproducible, and improving. The EDPB's Opinion 5/2019 on the interplay between the ePrivacy Directive and GDPR, and the WP29 Opinion 05/2014 on anonymization techniques, both establish that for data to be truly anonymous, it must be "irreversibly" de-identified such that re-identification is not "reasonably likely." Dense PII embeddings do not meet this bar.

### 2.2 Are Embedding Vectors Pseudonymized or Anonymized?

**Answer: Pseudonymized. They remain regulated personal data under GDPR.**

GDPR Article 4(5) defines pseudonymization as processing that renders data not directly attributable to a specific person "without the use of additional information." Embedding vectors require the embedding model's weights and the original PII corpus as "additional information" to invert — but that additional information exists, is accessible, and the process is not irreversible.

Under WP29 Opinion 05/2014, pseudonymization techniques include tokenization, hashing, and — relevantly — "noise addition" and "aggregation." Dense embeddings are closest to a transformation/encoding — they are not listed as anonymization-achieving techniques. They retain residual information about the original input.

**Operational consequence**: GDPR's full regulatory framework applies to stored embedding vectors. The data minimization principle (Article 5(1)(c)), storage limitation (Article 5(1)(e)), and integrity and confidentiality (Article 5(1)(f)) all apply.

### 2.3 Right to Erasure (Article 17) and Embedding Vectors

**Answer: This is an open legal question. The minimum defensible position is: deletion of an embedding means deletion of every vector derived from that person's data, plus any model checkpoints fine-tuned on that data.**

Article 17(1) requires erasure of personal data where the original purpose has elapsed or consent is withdrawn. For DataShield — which is literally a data removal platform — this creates a circular obligation: the system that removes people's PII from the web must also be able to remove their PII from its own knowledge layer.

If DataShield embeds PII into vectors and a data subject exercises their Article 17 right, DataShield must:
1. Delete the vector(s) associated with that person from pgvector.
2. Delete any embedding model that was fine-tuned on that person's data (model unlearning is an open research problem — not a production-ready capability as of 2026-03-26).
3. Regenerate any downstream aggregations that included that person's data.

This is operationally complex and becomes a compliance liability at scale. **The cleanest mitigation is to never embed raw PII fields** — only embed de-identified case-level summaries where the link to a specific natural person is broken before embedding.

### 2.4 Article 9 — Special Categories

SSN last-4 digits do not cleanly map to Article 9 special categories (health, race, biometrics, etc.), but they are treated as sensitive data under Article 9 equivalent provisions in many EU member state implementations. More importantly, if DataShield's case records include any health-adjacent removal requests (e.g., medical record removal, disability-related record removal), those records are directly within Article 9 scope. Any embedding of Article 9 data requires an explicit legal basis under Article 9(2) — most commonly explicit consent (Article 9(2)(a)) or substantial public interest under EU/member state law (Article 9(2)(g)).

**Recommendation**: Before embedding any DataShield case history, categorize whether it contains Article 9 data and confirm you have an Article 9 legal basis. This requires legal counsel — do not assume your general legitimate interests basis under Article 6(1)(f) covers Article 9 data.

---

## SECTION 3 — Data Processing Agreements: NVIDIA as Processor

### 3.1 Is NVIDIA a "Processor" Under GDPR Article 28?

**Answer: Yes, if DataShield sends personal data (including PII embeddings) to NVIDIA cloud APIs.**

GDPR Article 4(8) defines "processor" as a natural or legal person that processes personal data on behalf of the controller. Article 28(1) requires that controllers "use only processors providing sufficient guarantees to implement appropriate technical and organisational measures." Article 28(3) requires a binding contract (DPA) with specific mandatory clauses.

NVIDIA maintains a general Privacy Policy and has enterprise DPA templates. However, NVIDIA's standard NIM API terms (as of knowledge cutoff August 2025) are consumer/developer terms, not a GDPR Article 28-compliant DPA. Enterprise DPA terms require explicit negotiation or acceptance through NVIDIA's enterprise agreement program.

**Operating NVIDIA NIM for PII embedding without an executed Article 28 DPA is a GDPR violation.** Maximum fine: €20 million or 4% of global annual turnover under Article 83(4), whichever is higher.

### 3.2 Is NVIDIA a "Service Provider" Under CCPA?

**Answer: Only if the written contract meets § 1798.140(ag) requirements.**

NVIDIA's standard API terms as provided to developers do not constitute a CCPA service provider agreement — they are general terms of service. To qualify for the service provider carve-out, the contract must explicitly:
- Prohibit NVIDIA from retaining, using, or disclosing DataShield's personal information for any commercial purpose other than providing the embedding service.
- Prohibit NVIDIA from selling or sharing DataShield's personal information.
- Grant DataShield the right to audit compliance.

NVIDIA does offer enterprise agreements that can include these terms. Without one, every transmission of personal data to NVIDIA NIM is a third-party disclosure triggering CCPA's sale/sharing opt-out obligations.

### 3.3 Can DataShield Use NVIDIA NIM Without a DPA?

**Answer: No, not if any personal data or PII-derived embedding is transmitted.**

Legal exposure without a DPA:
- GDPR: Direct violation of Article 28(1). Supervisory authority enforcement risk. Individual data subject claims under Article 82.
- CCPA: Disclosure to a third party without opt-out mechanism. CPPA enforcement authority (effective July 2023 under CPRA). Per-violation civil penalties of $2,500 (unintentional) or $7,500 (intentional) per record per violation. At DataShield's scale (automated removal engine handling many subjects), aggregate exposure is substantial.
- Contractual: DataShield's own privacy policy likely represents to users that their PII is not shared with third parties for processing. Using NVIDIA cloud APIs without a DPA would breach that representation.

**Timeline**: Engage NVIDIA's enterprise sales channel before sending any data to NIM endpoints. This is not a "do later" item — it is a prerequisite.

---

## SECTION 4 — On-Premises vs. Cloud Embedding: Legal Impact

### 4.1 Does On-Prem Embedding Eliminate the Third-Party Disclosure Problem Under CCPA?

**Answer: Yes, completely.**

If DataShield runs the embedding model locally on the RTX 5090 or Spark-1 GB10, no personal data leaves the controller's environment. There is no disclosure to a third party. The CCPA third-party disclosure framework does not apply. The service provider DPA requirement does not apply. Consumer opt-out rights are not triggered.

The RTX 5090 (32GB VRAM) can run embedding models up to approximately 7B parameters comfortably. Spark-1 GB10 (120GB unified memory) can run models up to 70B parameters. Models appropriate for on-prem PII embedding at this scale: `nomic-embed-text`, `mxbai-embed-large`, `bge-large-en-v1.5`, `e5-large-v2`. All are available through Ollama and HuggingFace and can be deployed without any cloud API call.

### 4.2 Does On-Prem Embedding Eliminate the GDPR Article 28 Processor Relationship?

**Answer: Yes, completely.**

When DataShield processes personal data using its own infrastructure (on-prem GPU), NVIDIA is not involved in the data processing. There is no processor relationship. GDPR Article 28 does not apply. The controller (DataShield) processes data on its own equipment — this is the most legally clean configuration possible under GDPR.

Note: If DataShield uses Ollama on Spark-1, and Spark-1 is rented infrastructure (not owned), the hosting provider may qualify as a processor for infrastructure purposes. Confirm Spark-1 is owned equipment, not a cloud-rented VM, to avoid reintroducing a processor relationship.

### 4.3 Minimum Legal Risk Path

In order from lowest to highest legal risk for DataShield's RAG knowledge layer:

1. **On-prem embedding + no PII in what gets embedded** (embed only de-identified summaries) — Near-zero regulatory exposure. Compliant under all applicable laws with no DPA required. No "encryption in use" dependency. Ships today.

2. **On-prem embedding + PII in what gets embedded + AES-256-GCM vector store encryption** — CCPA and GDPR controller-only processing, no disclosure, no third-party trigger. Vectors stored encrypted. Article 17 deletion complexity remains. Manageable with proper data mapping.

3. **Cloud embedding (NVIDIA NIM) + executed DPA + PII flagged + opt-out mechanism** — Legally compliant path for cloud embedding, but operationally complex and slower to ship. Requires NVIDIA enterprise agreement.

4. **Cloud embedding without DPA** — Do not ship. Clear violation.

---

## SECTION 5 — Encryption in Use: Legal Sufficiency

### 5.1 Do CCPA/GDPR Explicitly Recognize "Encryption in Use" as a Technical Safeguard?

**Answer: No explicit recognition exists. "Encryption in use" (TEE / confidential computing) is ahead of the regulatory framework as of 2026-03-26.**

GDPR Article 32(1)(a) requires "encryption of personal data" as one example of an appropriate technical measure — but does not define what stage of the data lifecycle must be encrypted. Article 32 is principle-based (appropriate to the risk), not prescriptive. "Encryption in use" via TEE could qualify as meeting Article 32 in a risk-based analysis — but no EDPB guidance document, adequacy decision, or supervisory authority binding opinion has explicitly held that TEE processing satisfies Article 32.

CCPA does not define "encrypted" by reference to a specific standard. Cal. Civ. Code § 1798.81.5 requires "reasonable security procedures" — the California AG's guidance references NIST standards generally. NIST SP 800-175B Rev. 1 (2020) defines encryption comprehensively but does not yet have a formal category for "encryption in use" / confidential computing as a recognized security tier.

**EDPB and CISA Guidance**:
- EDPB Recommendations 01/2020 on supplementary measures for data transfers address pseudonymization and encryption but do not specifically address TEE-based processing.
- CISA's Secure by Design guidance (2023-2024) encourages hardware-based isolation but does not create a regulatory safe harbor.
- NIST NCCoE is actively working on confidential computing guidance (project page active as of 2025), but no finalized publication exists that creates a recognized legal standard.

### 5.2 Is "Encryption in Use" a Defensible Position Today?

**Answer: Defensible as part of a defense-in-depth argument, but not as a stand-alone compliance basis.**

If DataShield were audited or facing enforcement, "we used Intel TDX / NVIDIA Hopper TEE for in-use encryption" would be received as a sophisticated security measure that demonstrates seriousness about data protection — it would weigh positively in an Article 32 proportionality analysis. It would not, however, automatically satisfy the legal standard because no regulatory body has issued an opinion that TEE = compliance checkmark.

**The strategic bet**: Regulatory guidance on confidential computing will emerge in the 2026-2028 window as TEE adoption grows. If DataShield ships with on-prem TEE-based embedding now, it will be positioned to claim first-mover compliance status when that guidance arrives. But it cannot rely on that guidance today.

**Recommendation**: If DataShield intends to use NVIDIA Hopper TEE / confidential computing, document the architectural decision in a Data Protection Impact Assessment (DPIA) under GDPR Article 35. A DPIA is required when processing is "likely to result in a high risk" to natural persons — PII search over a removal engine's case history qualifies. The DPIA process creates a documented, defensible record of risk analysis even when the legal standard is unsettled.

---

## SECTION 6 — State Law Survey: The Strictest Floor

DataShield serves users in all 50 states. The following survey identifies the strictest applicable standards.

### Active Comprehensive Privacy Laws (as of 2026-03-26)

| State | Law | Encryption Requirement | Notes |
|-------|-----|----------------------|-------|
| California | CCPA/CPRA | Reasonable security (§ 1798.81.5); encryption referenced in breach safe harbor (§ 1798.150) | Strictest enforcement apparatus (CPPA active) |
| Virginia | CDPA (effective Jan 2023) | "Reasonable administrative, technical, and physical data security practices" (§ 59.1-578) | No explicit encryption mandate; risk-based |
| Colorado | CPA (effective Jul 2023) | "Reasonable security practices" | AG enforcement |
| Connecticut | CTDPA (effective Jul 2023) | "Reasonable security practices" | Similar to Virginia |
| Texas | TDPSA (effective Jul 2024) | "Reasonable security measures" | No explicit encryption requirement |
| Oregon | OCPA (effective Jul 2024) | "Appropriate technical and organizational measures" | GDPR-influenced language |
| Montana | MCDPA (effective Oct 2024) | "Reasonable administrative, technical, and physical data security practices" | — |
| Iowa | ICDPA (effective Jan 2025) | "Reasonable administrative, technical, and physical measures" | — |

### Special Category Laws Relevant to DataShield

**Washington My Health MY Data Act (effective Mar 2024 for large entities)**:
This is the strictest applicable standard DataShield must comply with if it processes health-related personal data for Washington residents. The MHMD Act:
- Applies to "consumer health data" broadly defined to include data that could "identify a consumer's past, present, or future physical or mental health status."
- If DataShield handles removal requests for medical record exposure, health data leaks, or disability-related data — MHMD applies.
- Requires "separate, valid authorization" for collection and sharing of consumer health data.
- Prohibits geofencing health facilities.
- Requires a signed consent for any health data processing beyond the primary purpose.

**The MHMD Act creates a stricter-than-CCPA standard for health-adjacent PII.** DataShield must determine whether any case records involve health data. If yes, treat MHMD as the floor for Washington residents' data.

**Illinois BIPA (Biometric Information Privacy Act)**:
If DataShield ever processes facial recognition data, fingerprints, or voiceprints in connection with identity verification for removal requests — BIPA applies to Illinois residents with a private right of action of $1,000-$5,000 per violation. This is a pre-existing liability trap. If DataShield's roadmap includes biometric verification, engage Illinois counsel before building.

### The Compliance Floor

The strictest standard DataShield must comply with across all 50 states is:

1. **For health-adjacent PII**: Washington MHMD Act — explicit separate authorization required.
2. **For all other PII**: CCPA/CPRA — strongest enforcement apparatus, explicit sensitive personal information category (SSN adjacent), strongest consumer rights framework.
3. **For biometric data (if applicable)**: Illinois BIPA — private right of action, no cure period for first violations.

**No state law currently imposes a stricter encryption-at-rest standard than CCPA's "reasonable security" + encryption safe harbor for breach notification. GDPR Article 32's risk-based approach is equivalent in rigor.** The gap is enforcement severity: CPPA (California) is the most aggressive enforcer in the US. GDPR enforcement for US companies serving EU subjects is handled by the relevant EU member state DPA (likely Irish DPC or German state DPAs depending on DataShield's EU user base).

---

## SECTION 7 — Risk Matrix

| Scenario | Legal Risk | Risk Level | Mitigation |
|----------|-----------|------------|------------|
| Cloud embedding (NVIDIA NIM API) without DPA | GDPR Article 28 violation; CCPA third-party disclosure without opt-out mechanism; potential "sale" classification triggering § 1798.120 | CRITICAL | Do not proceed. Execute DPA before any PII transmission to NVIDIA cloud. |
| Cloud embedding with executed NVIDIA DPA | GDPR Article 28 compliant; CCPA service provider relationship compliant. Residual risk: embedding vectors still classified as personal data; Article 17 deletion complexity; data transfer mechanism if NVIDIA servers are outside EEA | HIGH | Execute DPA. Confirm NVIDIA's Standard Contractual Clauses (SCCs) for EU data transfers. Implement vector-level deletion protocol. Conduct DPIA before launch. |
| On-prem embedding (RTX 5090 / Spark-1), raw PII embedded, vectors in pgvector | No third-party disclosure. CCPA and GDPR controller-only processing. Vectors are personal data — Article 17 deletion obligation. Storage encrypted under AES-256-GCM | MEDIUM | Document data mapping of which vectors link to which data subjects. Implement deletion-by-subject capability in pgvector. Conduct DPIA. |
| On-prem embedding, de-identified summaries only embedded (no raw PII fields), vectors in pgvector with AES-256-GCM | Lowest feasible risk. No third-party disclosure. Vectors may not qualify as personal data if de-identification is robust. DPIA recommended but risk is low | LOW | Define and document de-identification standard before embedding (pseudonymization of names/DOB/addresses before text enters embedding model). Validate de-identification is irreversible with technical review. |
| On-prem TEE (NVIDIA Hopper confidential computing) + raw PII embedding | Same as on-prem above for disclosure risk. TEE adds technical security layer but does not create regulatory safe harbor. Article 17 deletion complexity remains | MEDIUM | Document TEE architecture in DPIA as risk mitigation measure. Does not change legal classification of vectors as personal data. Strong engineering position, weak regulatory certainty position. |
| No RAG over PII at all | Near-zero regulatory risk for the knowledge layer. RAG functionality restricted to non-PII operational data (workflow metadata, removal source patterns, service statistics) | MINIMAL | Implement RAG only over operational/procedural data. Maintain separate, encrypted case records outside the RAG index. Accept the product limitation. |

---

## SECTION 8 — Final Recommendation

### The Architecture

**Ship with this stack. It is compliant today under CCPA, GDPR, and all applicable state laws.**

**Embedding model**: Run `bge-large-en-v1.5` or `nomic-embed-text` via Ollama on Spark-1 GB10. These models are free, open-weight, and run entirely on your hardware. No NVIDIA cloud API call for embeddings.

**What gets embedded**: De-identified case summaries only. The embedding pipeline must strip all PII fields before generating the summary text sent to the embedding model. The summary contains only: removal category (data broker, court record, social profile, etc.), outcome (removed, pending, failed), timeframe (week of removal, not date of birth), and procedural notes (no personal identifiers). This de-identification step is the legal linchpin — document it.

**Vector storage**: pgvector on Spark-1, encrypted at rest using your existing AES-256-GCM envelope (PIIVault). The vector store should be logically separated from the case record store. Access to the vector store requires the same encryption key management as the PII fields.

**Deletion protocol**: When a data subject's case record is deleted, the deletion workflow must also delete their associated vectors. Because the summaries are de-identified, linking vectors back to data subjects requires a mapping table (case_id → vector_id). Maintain that mapping inside the encrypted PIIVault, not in the vector store. This gives you an Article 17-compliant deletion path without exposing who a vector "belongs to."

**NVIDIA Cyborg RAG / TEE path**: Defer. It is the right long-term direction — especially for enabling search over encrypted PII fields, which would unlock significantly more powerful case pattern analysis. But deploy it after: (a) a DPIA is completed, (b) an NVIDIA enterprise DPA is executed if using cloud APIs, and (c) EDPB or NIST issues guidance on TEE-based processing that you can cite. That guidance is 12-24 months away.

**DPIA**: Conduct a GDPR Article 35 Data Protection Impact Assessment for the RAG layer regardless of which path you choose. Given DataShield processes PII at scale for removal purposes, a DPIA is likely mandatory (Article 35(3)(b) — large-scale processing of special category data is explicitly listed). This requires legal counsel engagement.

### Where Real Legal Counsel Is Required

LEGAL identifies issues and recommends action. The following items require engagement of qualified privacy/IP counsel before acting:

1. **GDPR Article 9 determination**: Whether DataShield's case histories include special category data (health, biometric, etc.) and whether your legal basis covers it. This is a factual-legal determination that requires counsel review of your data categories.

2. **DPIA drafting and review**: GDPR Article 35 DPIA for DataShield's RAG layer. Required before processing high-risk data. Must be documented by qualified DPO or privacy counsel.

3. **Washington MHMD Act compliance**: If DataShield handles health-related removal requests (medical records, health data exposure), you need Washington-admitted counsel to review MHMD exposure before serving Washington residents.

4. **NVIDIA enterprise DPA negotiation**: If the cloud embedding path is pursued, NVIDIA's enterprise legal team must be engaged. Do not attempt to self-negotiate a GDPR Article 28 DPA — the mandatory clauses are prescribed by the European Commission and require counsel to verify compliance.

5. **Illinois BIPA exposure analysis**: If DataShield's product roadmap includes biometric identity verification at any point. The private right of action creates significant class action exposure.

### What You Can Ship Without Counsel Review

The on-prem, de-identified-summary-only RAG architecture described above. The legal basis is clear, the risk is low, and there are no unresolved questions that require legal interpretation. It is the only architecture in the risk matrix with that status.

---

## APPENDIX — Statutory Citations

| Citation | Provision | Relevance |
|----------|-----------|-----------|
| Cal. Civ. Code § 1798.140(v)(1) | CCPA definition of personal information | Embedding vectors likely qualify |
| Cal. Civ. Code § 1798.140(ae) | CPRA sensitive personal information definition | SSN last-4 qualifies |
| Cal. Civ. Code § 1798.140(ag) | Service provider definition | Requires written contract before using NVIDIA NIM |
| Cal. Civ. Code § 1798.140(ah) | Third party definition | NVIDIA without DPA = third party |
| Cal. Civ. Code § 1798.120 | Right to opt-out of sale/sharing | Triggered by disclosure to NVIDIA without service provider agreement |
| Cal. Civ. Code § 1798.121 | Right to limit use of sensitive personal information | Applies to SSN-adjacent data |
| Cal. Civ. Code § 1798.150(a)(1) | Encryption safe harbor — breach notification only | Does NOT exempt embeddings from CCPA obligations |
| Cal. Civ. Code § 1798.81.5 | Reasonable security requirement | Baseline data security obligation |
| GDPR Article 4(1) | Personal data definition | Embedding vectors qualify |
| GDPR Article 4(5) | Pseudonymization definition | Embeddings = pseudonymized, not anonymous |
| GDPR Article 4(8) | Processor definition | NVIDIA = processor if cloud APIs used with personal data |
| GDPR Article 5(1)(c) | Data minimization | Embed only what is necessary |
| GDPR Article 5(1)(e) | Storage limitation | Delete vectors when case record deleted |
| GDPR Article 5(1)(f) | Integrity and confidentiality | AES-256-GCM vector store encryption required |
| GDPR Article 9 | Special categories | Health-adjacent removal cases require explicit legal basis |
| GDPR Article 17 | Right to erasure | Deletion must include associated vectors |
| GDPR Article 25 | Data protection by design | Embed de-identified summaries by design, not as afterthought |
| GDPR Article 28 | Processor contract requirement | Article 28-compliant DPA required before any NVIDIA NIM use with personal data |
| GDPR Article 32 | Technical security measures | AES-256-GCM at rest + TLS in transit = baseline. TEE is additive |
| GDPR Article 35 | Data Protection Impact Assessment | Required before high-risk processing |
| GDPR Article 83 | Administrative fines | Up to €20M or 4% global turnover for Article 28 violations |
| GDPR Recital 26 | Anonymization standard | Dense PII embeddings do not meet this standard |
| WP29 Opinion 05/2014 | Anonymization techniques | Embeddings are not listed as anonymization-achieving |
| Washington MHMD Act (RCW 70.372) | Consumer health data | Strictest US standard for health-adjacent PII |
| Illinois BIPA (740 ILCS 14) | Biometric data | Private right of action — most dangerous liability exposure |
| NIST SP 800-175B Rev. 1 | Encryption guidance | Referenced by California AG; does not create TEE safe harbor |

---

*LEGAL does not practice law. This document identifies issues, assesses risk levels, and recommends engagement of qualified legal counsel where noted. Nothing in this document constitutes legal advice. Engage qualified privacy counsel for DPIA drafting, GDPR Article 9 classification, Washington MHMD analysis, and NVIDIA DPA negotiation before those decisions are finalized.*
