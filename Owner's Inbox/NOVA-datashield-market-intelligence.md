# DataShield Market Intelligence Report
**Author**: NOVA — Research and Strategic Intelligence
**Audience**: Ron (decision), FORGE (roadmap input), LEGAL (regulatory flag)
**Date**: 2026-03-26
**Status**: Research complete. Action items identified.

---

## Objective

Current-state intelligence on data broker regulation, competitor landscape, market sizing,
and technology signals for DataShield — the automated personal data removal engine. Goal:
identify what changes roadmap priority and what creates an immediate opportunity.

---

## Key Findings (ranked by decision impact)

### 1. California's DROP Is a Direct Integration Opportunity — Deadline August 1, 2026

California's Delete Request and Opt-Out Platform (DROP) went live January 1, 2026. Starting
August 1, 2026, ALL registered data brokers must retrieve and process consumer deletion
requests from DROP every 45 days. Penalties are $200 per request per day for non-compliance,
no cure period.

**The opportunity for DataShield**: DROP is a single API endpoint that, when hit, triggers
deletion at every registered California data broker simultaneously. DataShield does not need
to maintain individual playbooks for each California-registered broker. One integration covers
all of them. CalPrivacy opens the API for automated request retrieval in Spring 2026.

This is the highest-ROI integration available right now. It is legally mandated, technically
standardized, and no competitor has publicly claimed to have fully integrated it.

Source: [Clark Hill — California's DROP Goes Live](https://www.clarkhill.com/news-events/news/is-your-business-a-data-broker-californias-drop-goes-live-and-calprivacy-continues-to-enforce-delete-act/),
[Transcend DROP Compliance Guide](https://transcend.io/blog/calprivacy-drop-compliance-guide),
[DataGrail DROP Analysis](https://www.datagrail.io/blog/regulations/the-delete-act-and-drop-what-you-need-to-know/)

---

### 2. Cloaked Just Raised $375M — The Market Is Validating at Scale

Cloaked (privacy identity + data removal + VPN) closed $375M Series B on March 19, 2026.
Led by General Catalyst and Liberty City Ventures. 350,000 paying customers, 10x YoY growth,
1 billion records cleaned. Moving into enterprise — CISOs can now view employee risk
aggregates. Investors include DuckDuckGo, LG Technology Ventures, Assurant Ventures.

**Signal**: This is the largest privacy consumer raise in history. It proves institutional
capital has conviction in this market. It also defines what DataShield is NOT — Cloaked is
building a full identity stack (identity masking + removal + insurance + VPN + enterprise).
DataShield's lane is surgical automation of opt-out mechanics, not a lifestyle privacy suite.
The two are not in direct conflict today. They will be if DataShield does not move fast.

Source: [TechCrunch — Cloaked raises $375M](https://techcrunch.com/2026/03/19/consumer-focused-privacy-company-cloaked-raises-375m-as-it-expands-to-enterprise/),
[BusinessWire](https://www.businesswire.com/news/home/20260319361833/en/Cloaked-Raises-$375-Million-to-Fight-for-Privacy-in-the-Age-of-AI)

---

### 3. Global Privacy Control (GPC) Is Now Legally Enforceable in 12 States — DataShield Is Missing This

As of January 1, 2026, twelve states require businesses to honor GPC opt-out preference
signals: California, Colorado, Connecticut, Montana, Nebraska, New Hampshire, New Jersey,
Minnesota, Maryland, Delaware, Oregon, and Texas.

California's Opt Me Out Act (AB 566, signed October 2025) requires all browsers to have
built-in GPC functionality by January 1, 2027. 40 million consumers already use GPC-enabled
browsers.

**The gap**: GPC is a browser signal that automatically triggers opt-outs when a consumer
visits a site. DataShield's current architecture uses Playwright-driven active opt-outs
(go-to-broker, fill form, submit). GPC is passive and continuous — the browser declares
opt-out status on every site visit. DataShield has no GPC emission capability.

**The opportunity**: DataShield can add a GPC header layer to its browser automation stack.
Any broker that honors GPC gets an instant, legally-enforceable opt-out without running the
full Playwright playbook. This is a force multiplier, not a replacement. Estimated dev effort:
low. Compliance upside: high.

Source: [Didomi — GPC in 2026](https://www.didomi.io/blog/global-privacy-control-gpc-2026),
[Pandectes — GPC vs Do Not Track](https://pandectes.io/blog/global-privacy-control-vs-do-not-track-whats-legally-enforceable-in-2026/),
[California AG GPC page](https://oag.ca.gov/privacy/ccpa/gpc)

---

### 4. Government Buying Broker Data Without Warrants — Active Political Story Creating Urgency

NPR broke a story March 25, 2026 (one day ago): ICE and other federal agencies are purchasing
bulk data from commercial data brokers — location data, identity records — without warrants.
130 civil society organizations signed a letter urging Congress to close the "data broker
loophole" in FISA 702 reauthorization (deadline: April 20, 2026). Bipartisan legislation
introduced by Reps. Davidson, Lofgren, and Sens. Lee and Wyden.

**Signal**: This story is top-of-press. Privacy concern is acute and bipartisan right now.
DataShield has a marketing window that expires in weeks if the FISA vote doesn't pass. The
frame to use: "Your data is being bought and used — removal is not optional."

Source: [NPR — Your data is everywhere](https://www.npr.org/2026/03/25/nx-s1-5752369/ice-surveillance-data-brokers-congress-anthropic)

---

### 5. Regulatory Coverage Is Expanding Fast — 20 State Privacy Laws Active in 2026

New comprehensive privacy laws active in 2026: Indiana, Kentucky, Rhode Island (plus
California, Colorado, Connecticut, Montana, Nebraska, New Hampshire, New Jersey, Minnesota,
Maryland, Delaware, Oregon, Texas already in effect). Rhode Island's threshold is
exceptionally low: 35,000 consumers or 10,000 consumers if 20%+ revenue from data sales.

State-specific data broker registration now mandatory in 4 states:
- **California**: $6,000/year, DROP integration required by August 2026
- **Vermont**: Registration by January 31 annually, robust security requirements
- **Texas**: $300/year, WISP mandatory, $100/day up to $10,000/year penalties
- **Oregon**: Recently added

**Signal for DataShield**: The regulatory map creates a natural upsell. Users who remove
their data from California-registered brokers via DROP still need active Playwright-based
removal for non-California brokers, Vermont-registered brokers, and the long tail not covered
by any registry. DataShield's full automation stack remains essential.

Source: [MultiState — 20 State Privacy Laws 2026](https://www.multistate.us/insider/2026/2/4/all-of-the-comprehensive-privacy-laws-that-take-effect-in-2026),
[SecurePrivacy — Data Broker Registration](https://secureprivacy.ai/blog/data-broker-registration),
[Davis+Gilbert — Texas and Oregon](https://www.dglaw.com/u-s-data-broker-legislation-expands-to-include-texas-and-oregon/)

---

### 6. FTC Actively Enforcing PADFAA — Foreign Adversary Data Sales Banned

February 2026: FTC sent warning letters to 13 data brokers for potential PADFAA violations.
PADFAA (Protecting Americans' Data from Foreign Adversaries Act, 2024) bans data brokers from
selling health, financial, genetic, biometric, geolocation, SSN, or credential data to
entities linked to China, Russia, Iran, or North Korea. Civil penalties: up to $53,088 per
violation. CFPB withdrew its broader proposed Regulation V data broker rule in May 2025.

**Signal**: Federal enforcement is active but narrowly targeted (foreign adversary angle, not
broad consumer protection). The CFPB rule withdrawal means federal baseline protection for
consumers is weaker than expected. State laws and services like DataShield fill the gap.

Source: [FTC — PADFAA reminder Feb 2026](https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-reminds-data-brokers-their-obligations-comply-padfaa),
[Alston & Bird — PADFAA letters](https://www.alstonprivacy.com/ftc-sends-letters-reminding-data-brokers-of-their-obligations-under-padfaa/)

---

## Competitor Intelligence

### Pricing Map (current as of March 2026)

| Service | Entry Price | Coverage | Differentiator |
|---------|-------------|----------|----------------|
| **DeleteMe** | $129/yr individual | ~950 sites claimed; 181 auto-removed in practice | Human-verified removals, quarterly reports, brand recognition |
| **Incogni** (Surfshark) | $6.49/mo ($77.88/yr) | 420+ brokers automated; 3,000+ custom domains | Deloitte-audited, 245M removals, fastest growth |
| **Optery** | $3.25–$24.99/mo | 130–640 sites by tier | Free tier, screenshot proof of removal, transparency |
| **EasyOptOuts** | $19.99/yr | ~100 people-search sites | Wirecutter budget pick, repeats every 4 months |
| **Kanary** | $9.99/mo (mobile app) | 300+ people-search sites | Pivot to mobile app (Kanary Copilot), free basic tier |
| **Privacy Bee** | $18/mo | Broad + facial recognition removal | Premium positioning, dark web + social + real estate photos |
| **Cloaked** | Unknown (consumer) | 1B+ records cleaned | Full identity stack, $375M raise, enterprise play |
| **OneRep** | ~$100/yr | 310 sites | Controversy: founder linked to data broker industry |

### Key Competitor Weaknesses (from Reddit and review sites)

**DeleteMe**: Reddit consensus has shifted against it. "DeleteMe claims 850 brokers but 569
require custom requests — effective coverage is 181." Users complain about vague status
updates ("monitoring") rather than specific removal confirmations. Its 10-year head start is
no longer a moat.

**Incogni**: Strongest automated performer. Independent Deloitte audit is a credibility
differentiator no one else has. 420+ brokers, recurring removals every 60–90 days, 245M
successful removals. This is DataShield's primary benchmark.

**Optery**: Best transparency (before/after screenshots). Free tier creates top-of-funnel.
Price range is widest in the market — something for every budget. Weaker on automation depth.

**EasyOptOuts**: Budget-only play. $19.99/year. No custom requests. ~100 sites. Low threat.

**Kanary**: Pivoted fully to mobile app. This is a strategic retreat, not an advance. Web
users abandoned. Narrowed to people-search sites only. Low threat to DataShield.

**OneRep**: Founder credibility issue (linked to operating data broker sites). This is a
marketing vulnerability DataShield can use.

**Cloaked**: Biggest long-term threat. $375M, enterprise expansion, full stack. But their
moat is identity masking (create fake identities), not surgical broker opt-outs. Different
architecture, different customer behavior. Watch closely.

Source: [Security.org DeleteMe Review](https://www.security.org/data-removal/deleteme/),
[CyberInsider Incogni Review](https://cyberinsider.com/data-removal/incogni-review/),
[VPN Tier Lists — Reddit Optery vs DeleteMe](https://vpntierlists.com/blog/optery-vs-deleteme-what-reddit-really-says-in-2026),
[Cloudwards Kanary Review](https://www.cloudwards.net/kanary-review/)

---

## Market Size

**The data broker industry** (companies selling data) is valued at $315–465B in 2026 (wide
range, methodology-dependent). Growing at 7–10% CAGR. This is the industry DataShield
removes data from — not DataShield's market, but its reason for existing.

**Identity theft protection services** (the adjacent revenue category DataShield competes in):
- US market: $5.7B in 2026
- Global: $19B in 2025, growing to $38.7B by 2032 at 10.59% CAGR
- DataShield's TAM sits at the intersection of this category and privacy software

**Privacy removal services specifically** (DataShield's direct market): No clean third-party
TAM figure. Proxy: Incogni has 245M+ removals and is privately held; DeleteMe has 50M
removals in 10 years; Cloaked has 1B records cleaned. The subscription pricing range is
$20–$216/year. This is a high-growth emerging category, not a mature market — the
opportunity to establish position is now, not in 3 years.

Source: [Mordor Intelligence Data Broker Market](https://www.mordorintelligence.com/industry-reports/data-broker-market),
[Fortune Business Insights Identity Theft Protection](https://www.fortunebusinessinsights.com/identity-theft-protection-services-market-105125),
[Cloaked data broker economy post](https://www.cloaked.com/post/the-data-broker-economy-will-hit-561-b-by-2029--why-personalized-risk-reports-are-now-the-first-line-of-defense)

---

## Technology Signals

### DSAR Automation (B2B Adjacent)

Enterprise DSAR tools (DataGrail, OneTrust, Osano, Sentra) handle Data Subject Access
Requests for businesses that receive deletion requests. This is the compliance side of the
same regulatory world. DataShield is the consumer-facing mirror. No direct competitor overlap,
but worth knowing: DataGrail and OneTrust are well-funded and could expand consumer-facing.

### Data Broker Opt-Out Barriers — What's Changed Recently

California's DROP standardizes the matching format (dates as 8-digit strings, phone as last
10 digits without dashes). This eliminates the "doesn't match our records" dodge that brokers
have used for years. For non-DROP states, barriers remain variable: Spokeo retains removed
information for paid accounts even if it disappears from free searches. Intelius requires
email, phone, or mailing address confirmation. Individual playbook maintenance remains
essential for the long tail.

**No major broker has added new automated barriers in the past cycle.** The direction is
toward standardization (DROP), not increased friction.

Source: [Freedom of the Press Foundation — DROP tool](https://freedom.press/digisec/blog/californians-get-new-data-broker-opt-out-tool/),
[Cybernews Opt-Out Guide 2026](https://cybernews.com/privacy-tools/data-broker-opt-out/)

---

## Evidence Quality Assessment

| Finding | Source Quality | Confidence |
|---------|---------------|------------|
| DROP API opens Spring 2026, August 1 mandate | CPPA official + multiple law firm advisories | High |
| Cloaked $375M raise | TechCrunch, BusinessWire (press release) | High — confirmed |
| GPC enforceable in 12 states | California AG, multiple compliance firms | High |
| Government buying broker data (NPR story) | NPR + 8 public radio stations | High — current news |
| Competitor pricing | Vendor sites + independent review aggregators | High for top players |
| Market size figures | Multiple research firms with conflicting methodology | Medium — directional only |
| Reddit complaint summary | Aggregated via review sites, not direct Reddit scrape | Medium |

---

## Risks

1. **DROP API scope unknown**: CalPrivacy's DROP only covers California-registered brokers.
   That registry has enforcement gaps — CPPA has fined 8 brokers so far but hundreds may be
   unregistered. DROP integration does not eliminate the need for individual playbooks.

2. **Cloaked trajectory**: At $375M with 10x growth, Cloaked could absorb a pure-play removal
   engine via acquisition within 18 months. DataShield should have a considered position on
   whether to build toward acqui-hire positioning or independent defensibility.

3. **CFPB rule withdrawal**: The death of Regulation V means no federal floor on data broker
   behavior outside PADFAA's narrow foreign adversary scope. Future administration changes
   could reverse state-level momentum. Regulatory tailwinds are real but not guaranteed.

4. **Incogni's Deloitte audit**: This is a hard credibility differentiator. DataShield will
   need a comparable third-party validation story before it can compete at Incogni's price
   point.

5. **OneRep controversy**: Founder's data broker ties created a trust crisis. DataShield must
   ensure its own supply chain is clean — no contractors, tools, or APIs with data broker
   affiliations.

---

## Recommendation

Single priority order for DataShield roadmap changes based on this research:

**1. Integrate California DROP API (ship before August 1, 2026).**
This is free regulatory leverage — mandatory for all California-registered brokers. One
integration replaces dozens of individual playbooks for California coverage. Spring 2026 is
when the API opens. This is a hard deadline with a hard penalty structure.

**2. Add GPC emission to the Playwright stack (low effort, high upside).**
Set `Sec-GPC: 1` header in all browser sessions. Any broker honoring GPC gets an automatic,
legally-enforceable opt-out without running the full playbook. 12 states enforcing now. 40M
consumers already using it. This is a force multiplier on existing automation.

**3. Use the NPR/ICE story as a marketing moment now.**
This week's news cycle is maximally favorable. Government surveillance via data brokers is a
bipartisan concern with a Congressional vote imminent. DataShield's messaging should hit
urgency, not just privacy preference. Window: 2–4 weeks until FISA vote resolves.

**4. Build a third-party audit narrative (medium term).**
Incogni's Deloitte audit is their strongest sales tool. DataShield needs a comparable trust
signal — an independent verification of broker coverage, removal success rate, and data
handling practices — before competing on credibility with enterprise or high-paying consumers.

**5. Watch Cloaked's enterprise moves.** They are moving up-market. Their consumer product
could commoditize the low end. DataShield's defensible position is automation depth and
playbook accuracy, not price competition.

---

## Next Actions

| Action | Owner | When |
|--------|-------|------|
| Validate CalPrivacy DROP API access requirements and Spring 2026 opening date | FORGE | This week |
| Add GPC header to Playwright session config | FORGE | This sprint |
| Draft a marketing brief using the NPR/ICE story angle | SPARK | This week |
| Audit DataShield's contractor and API supply chain for data broker ties | LEGAL | Before any public launch |
| Identify a third-party auditor for removal accuracy validation | Ron + VENTURE | 60-day horizon |
| Monitor Cloaked enterprise product launch terms for direct overlap with DataShield | NOVA | Monthly |

---

*Sources compiled March 26, 2026. All URLs verified current at time of research.*

### Primary Sources Used

- [CPPA — Information for Data Brokers](https://cppa.ca.gov/data_brokers/)
- [Clark Hill — DROP Goes Live](https://www.clarkhill.com/news-events/news/is-your-business-a-data-broker-californias-drop-goes-live-and-calprivacy-continues-to-enforce-delete-act/)
- [Transcend — DROP Compliance Guide](https://transcend.io/blog/calprivacy-drop-compliance-guide)
- [DataGrail — DELETE Act and DROP](https://www.datagrail.io/blog/regulations/the-delete-act-and-drop-what-you-need-to-know/)
- [California Privacy Protection Agency](https://privacy.ca.gov/data-brokers/)
- [IAPP — New year, new rules 2026](https://iapp.org/news/a/new-year-new-rules-us-state-privacy-requirements-coming-online-as-2026-begins/)
- [MultiState — 20 State Privacy Laws 2026](https://www.multistate.us/insider/2026/2/4/all-of-the-comprehensive-privacy-laws-that-take-effect-in-2026)
- [FTC — PADFAA reminder](https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-reminds-data-brokers-their-obligations-comply-padfaa)
- [Alston & Bird — PADFAA letters](https://www.alstonprivacy.com/ftc-sends-letters-reminding-data-brokers-of-their-obligations-under-padfaa/)
- [Davis+Gilbert — Texas and Oregon](https://www.dglaw.com/u-s-data-broker-legislation-expands-to-include-texas-and-oregon/)
- [SecurePrivacy — Data Broker Registration](https://secureprivacy.ai/blog/data-broker-registration)
- [NPR — Government buying data without warrants](https://www.npr.org/2026/03/25/nx-s1-5752369/ice-surveillance-data-brokers-congress-anthropic)
- [TechCrunch — Cloaked raises $375M](https://techcrunch.com/2026/03/19/consumer-focused-privacy-company-cloaked-raises-375m-as-it-expands-to-enterprise/)
- [BusinessWire — Cloaked announcement](https://www.businesswire.com/news/home/20260319361833/en/Cloaked-Raises-$375-Million-to-Fight-for-Privacy-in-the-Age-of-AI)
- [Didomi — GPC in 2026](https://www.didomi.io/blog/global-privacy-control-gpc-2026)
- [California AG — GPC](https://oag.ca.gov/privacy/ccpa/gpc)
- [Pandectes — GPC vs Do Not Track](https://pandectes.io/blog/global-privacy-control-vs-do-not-track-whats-legally-enforceable-in-2026/)
- [Security.org — DeleteMe Review](https://www.security.org/data-removal/deleteme/)
- [Security.org — Best Data Removal 2026](https://www.security.org/data-removal/best/)
- [CyberInsider — Incogni Review](https://cyberinsider.com/data-removal/incogni-review/)
- [Cloudwards — Kanary Review](https://www.cloudwards.net/kanary-review/)
- [AllAboutCookies — Privacy Bee Review](https://allaboutcookies.org/privacy-bee-review)
- [Onerep — Best Data Removal Services](https://onerep.com/blog/best-data-removal-service)
- [VPN Tier Lists — Reddit Optery vs DeleteMe](https://vpntierlists.com/blog/optery-vs-deleteme-what-reddit-really-says-in-2026)
- [Freedom of the Press Foundation — DROP](https://freedom.press/digisec/blog/californians-get-new-data-broker-opt-out-tool/)
- [Cybernews — Opt-Out Guide 2026](https://cybernews.com/privacy-tools/data-broker-opt-out/)
- [Fortune Business Insights — Identity Theft Protection](https://www.fortunebusinessinsights.com/identity-theft-protection-services-market-105125)
- [Mordor Intelligence — Data Broker Market](https://www.mordorintelligence.com/industry-reports/data-broker-market)
- [Cloaked — Data Broker Economy](https://www.cloaked.com/post/the-data-broker-economy-will-hit-561-b-by-2029--why-personalized-risk-reports-are-now-the-first-line-of-defense)
