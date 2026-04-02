# MK Copilot SaaS — Revenue Activation Plan
**VENTURE** | 2026-03-30 | Beta Launch: 5 Test Sellers

---

## FATAL FLAW CHECK — READ FIRST

**No fatal flaw found. Green light to proceed.** One meaningful risk exists that requires mitigation
before public launch: Mary Kay corporate's own AI tools (Foundation Finder launched Aug 2025,
agentic AI portfolio announced via CIO Dive 2025) mean their legal team is now watching third-party
AI use of their brand. This is manageable with correct positioning — see Section 7.

---

## 1. Product Definition

### What MK Copilot Does For a Seller

An MK consultant's daily friction points: she forgets exact product ingredients when a customer
asks, stumbles on objections ("I can buy this cheaper at Target"), doesn't know how to follow up
without sounding pushy, and has no one to practice her pitch on at 10pm before a party. MK
Copilot eliminates all four.

Specifically:
- **Product Q&A**: Ask "what's in the TimeWise Repair serum" and get the correct answer instantly,
  formatted as a talking point the seller can speak out loud
- **Objection handling**: "Customer says it's too expensive" → copilot generates a 2-3 sentence
  response the seller can read or adapt
- **Sales script generation**: Input the customer's skin concern → receive a personalized
  recommendation script with product names, benefits, and a close
- **Skin analysis** (vision pipeline, `~/mk-skin-analysis/`): Upload a customer photo → copilot
  recommends foundation shade and skincare regimen with specific MK SKUs
- **Follow-up message drafting**: Tell it what happened in the last interaction → get a follow-up
  text/DM ready to copy-paste

### MVP SaaS Feature Set (Beta — Not Everything Ships Week 1)

**Ships at beta launch:**
- Chat interface (web, mobile-responsive)
- Product Q&A (the core model at :8767)
- Objection handling
- Sales script generation
- Account login (one seller = one account)
- Usage dashboard (how many queries, what topics)

**Ships in Month 2 (post-beta validation):**
- Skin analysis / photo upload (vision pipeline ready, needs API wrapper)
- Follow-up message templates
- Customer CRM notes (basic — "remember Sarah wants the eye cream")

**NOT in MVP:**
- Inventory tracking integration
- Team/downline features
- Mobile native app

### UX: Web-First Chat Interface

The product is a chat window. Think ChatGPT but knowing every MK product and every sales
situation. Mobile-responsive web app — sellers already use their phones but a PWA is faster
to ship than a native app. No desktop app, no Slack bot, no Chrome extension in beta.

URL: `mk.ultrarag.app` (Cloudflare tunnel, add subdomain to existing config)

Login: Email + password. No OAuth in beta — reduces complexity and audit surface.

---

## 2. Pricing Model

### Recommended Structure

**Anchor math**: Average active MK consultant earns $200-$500/month commission. At 5-10% of
that, target price is $10-$50/month. The sweet spot is $29/month — below psychological $30
threshold, leaves room for annual discount, defensible as "less than one party's upsell revenue."

| Tier | Price | What It Includes | Rationale |
|------|-------|-----------------|-----------|
| Free Trial | $0 / 14 days | Full access, 50 queries | Removes sign-up friction for beta |
| Solo | $29/month | Unlimited queries, all chat features | Core tier |
| Solo Annual | $249/year | Same as Solo | $20.75/month effective, saves $99 vs monthly |
| Vision Add-on | +$10/month | Skin photo analysis feature | Upsell after they're hooked |

**No freemium tier.** Freemium works when acquisition cost is zero and viral loops exist.
Beta has neither. Freemium here just creates non-paying users who generate support load.

**Why not $49 or $99?** Because MK consultants are price-sensitive, many are part-time, and
the median consultant earns less than $200/month. $29 is a no-brainer ROI if it helps close
one extra sale per month. $49 requires a harder sell. Start at $29, raise to $39 after
beta validation if retention is strong.

**Trial-to-paid flow:**
1. Seller signs up, enters email, no credit card required for trial
2. Day 1: Onboarding email with 3 specific use cases to try
3. Day 10: Check-in email asking what's working
4. Day 13: Reminder that trial ends tomorrow, one-click to upgrade
5. Day 14: Trial expires. Prompt to add card. No auto-charge without card on file.
6. Month 1 after paying: Ask for testimonial if they've been active

---

## 3. Beta Seller Profile

### The 5 Ideal Beta Testers

**Target profile**: Mid-experience consultant, 1-3 years in, doing it seriously part-time
(15-25 hours/week), earning $200-$400/month, frustrated by not being able to answer every
product question and losing customers to indecision. NOT a brand new consultant (no context
for feedback) and NOT a top-100 director (too busy, too opinionated, too entrenched in
their own methods).

**Secondary filter**: Comfortable with technology. Has used ChatGPT or a similar tool at
least once. Owns a smartphone they use for business. Will actually give feedback when asked.

**Geographic preference**: No strong preference, but a regional cluster (e.g., 2-3 in
same metro) creates natural word-of-mouth pressure and makes in-person demos easier if
needed. Dallas-area (Mary Kay HQ region) gives brand-adjacent credibility for later corporate pitch.

### How to Find Them

**Method 1 — Facebook Groups (fastest, this week)**
Search Facebook for: "Mary Kay consultants", "Mary Kay beauty consultant group", "Mary Kay
IBC community". The largest groups have 5,000-50,000 members. Post or DM individually.
Message template is in Section 7.

Specific groups to target:
- "Mary Kay Consultants" (general, multiple large groups)
- State-specific groups (Texas, Florida, California have highest density)
- "Mary Kay New Consultants" groups (recent joiners are most open to tools)

**Method 2 — Personal network**
Does Ron know any MK consultants directly? One warm introduction is worth 50 cold DMs.
Even knowing someone who knows a consultant is a useful entry point.

**Method 3 — MK InTouch consultant directory**
Mary Kay's own website has a "Find a Consultant" locator. Identify local consultants by zip
code and reach out directly via their listed contact info or linked social.

**Outreach message (adapt as needed):**
> "Hi [Name], I'm building an AI sales assistant specifically for Mary Kay consultants —
> it answers product questions, generates sales scripts, and handles objections. I'm looking
> for 5 consultants to test it for free for 30 days in exchange for honest feedback.
> Would you be open to a quick 15-min call to see if it's a fit?"

Do NOT lead with "AI." Lead with the problem it solves. Mention AI in the follow-up.

---

## 4. What's Needed to Take Payments

### Stripe Setup (2-4 hours of work)

1. Create a Stripe account at stripe.com (personal or business — business preferred for
   professional appearance, use existing entity if one exists)
2. Create two products in Stripe:
   - "MK Copilot Solo" at $29/month recurring
   - "MK Copilot Solo Annual" at $249/year recurring
3. Generate payment links (no custom checkout code needed for beta — Stripe-hosted checkout
   is sufficient)
4. Add the payment link to the landing page and the trial expiry email

**No code required for beta.** Stripe payment links work without any integration code.
When beta graduates to full launch, integrate Stripe webhooks with the SaaS backend to
auto-provision accounts.

### Minimum Viable Landing Page

Single page. Required sections:
1. **Headline**: "The AI sales assistant built for Mary Kay consultants"
2. **Three problems** it solves with short copy each
3. **Demo video** or animated GIF showing a real conversation (product Q&A + objection example)
4. **Pricing table** (Free Trial / $29/month)
5. **CTA button**: "Start Free Trial" → goes to signup form
6. **Social proof placeholder** (can be "5 consultants testing now" during beta)

Deploy to: `mk.ultrarag.app` via Cloudflare, pointing to a static page initially.
FORGE can build this in under 2 hours. No CMS needed — static HTML is fine for beta.

### Terms of Service Basics

Three things that must be in the ToS before taking money:
1. You are not affiliated with Mary Kay Inc. (critical — see Section 7)
2. AI responses may be inaccurate; consultant is responsible for verifying product information
3. Subscription terms: monthly billing, cancel anytime, no refunds on partial months

Use a ToS generator (TermsFeed, $10) for the full document. The three items above must be
explicit and prominent — not buried.

### Trial-to-Paid Conversion Flow (technical)

For beta (5 users): manual is fine. When someone's trial expires, manually send the Stripe
payment link. Track in a spreadsheet.

For post-beta scale: integrate Stripe webhooks + email automation (Resend or Postmark).

---

## 5. Infrastructure Checklist

### Current State Assessment

The model is live at Spark-1:8767. For external users, the following gaps exist:

| Item | Status | Action Required |
|------|--------|----------------|
| HTTPS | Not exposed | Cloudflare tunnel (30 min) |
| Authentication | None | Add API key or session auth to SaaS app |
| Rate limiting | Unknown | Add per-user query limits |
| Uptime monitoring | None | Add UptimeRobot (free tier) |
| Multi-tenancy | Beta mode | SaaS app at `~/ai-business/mk-copilot-saas/` handles this |
| Error handling | Unknown | Test with bad inputs before launch |
| Logging | Unknown | Add structured query logging for debugging |

### Cloudflare Tunnel — Yes, Use It (30-Minute Setup)

The Cloudflare tunnel already runs on Spark-1 for ultrarag.app. Add a new route:

```yaml
# Add to /etc/cloudflared/config.yml on Spark-1
- hostname: mk.ultrarag.app
  service: http://localhost:8767
```

Then in Cloudflare DNS: add CNAME `mk` pointing to the tunnel endpoint.
Domain: ultrarag.app already owned. This costs $0 additional.

**Note**: The memoryweb.ultrarag.app tunnel is currently broken (MW is on Spark-2, not Spark-1).
Do not repeat this mistake — verify mk.ultrarag.app routes to :8767 on Spark-1, which is correct.

### Rate Limiting

For 5 beta users: 100 queries/day per user is more than sufficient. Implement at the
SaaS app layer, not the model layer. Log every query with timestamp and user ID.

### Auth

The SaaS app at `~/ai-business/mk-copilot-saas/` should have session-based auth already
partially built (beta state). Verify it works before giving credentials to testers.
At minimum: email + password, server-side sessions, no shared API keys.

### Uptime Monitoring

Register mk.ultrarag.app on UptimeRobot (free). Get notified by email if the service
goes down. Takes 5 minutes. A seller hitting a 502 with no context will churn immediately.

### Capacity Sanity Check

Spark-1 is running the MK model at :8767 alongside Ultra RAG (:8300), IMDS RAG (:8301),
AI Army OS (:8500), and 8 other services. 5 beta users with 100 queries/day = ~500 queries.
At Spark-1's capacity, this is negligible. No scaling concern for beta.

---

## 6. 30-Day Launch Timeline

### Week 1 — Infrastructure and Payments (Days 1-7)
- [ ] Set up Stripe account and create two products (Solo + Annual)
- [ ] Add Cloudflare route for mk.ultrarag.app → Spark-1:8767
- [ ] Verify SaaS app auth works end-to-end (login → query → response)
- [ ] Add rate limiting (100 queries/day/user)
- [ ] Register mk.ultrarag.app on UptimeRobot
- [ ] Purchase ToS template from TermsFeed, customize with the three mandatory items
- [ ] Build landing page (FORGE: 2-hour task — static HTML, 5 sections, deploy to mk.ultrarag.app)

**End of Week 1 deliverable**: A working URL with auth, a landing page, ToS, and Stripe
payment link. Fully functional before first tester touches it.

### Week 2 — Find and Onboard Beta Testers (Days 8-14)
- [ ] Post/DM in 3 MK Facebook groups (50 DMs minimum to get 5 responses)
- [ ] Schedule 15-min onboarding calls with each confirmed tester
- [ ] Give each tester login credentials and a "quick start" guide (1 page, 3 use cases)
- [ ] Send tester #1-5 trial confirmation emails with Stripe link for when trial ends
- [ ] Monitor Spark-1 logs for errors during first live user sessions

**End of Week 2 deliverable**: 5 testers active, using the product, with a feedback mechanism.

### Week 3 — Feedback Loop and Fixes (Days 15-21)
- [ ] Conduct 15-min check-in call with each tester (what's working, what's broken)
- [ ] Identify top 3 complaints and fix at least 2
- [ ] Test vision/skin analysis feature with 2 willing testers (upsell validation)
- [ ] Collect usage data: query volume, topics, drop-off points
- [ ] Decide whether to open a 6th-10th beta slot based on demand signals

**End of Week 3 deliverable**: Known bugs fixed, real usage data in hand, first honest
signal on whether testers would pay.

### Week 4 — First Revenue and Verdict (Days 22-30)
- [ ] Send trial expiry emails to testers whose 14-day trial ends
- [ ] Convert at least 2/5 to paid (40% trial-to-paid = viable; 20% = needs product work)
- [ ] Document conversion rate, most-used features, verbatim feedback
- [ ] Make Go/No-Go decision on full launch (criteria below)
- [ ] If Go: plan 50-user cohort, set up Stripe webhooks, begin email automation
- [ ] If No-Go: identify the specific failure point and define what would change the verdict

**Launch day checklist** (Day 30 if Go):
- Model is running and health-checked
- Auth working, rate limits active
- Payment link live and tested with a real card
- ToS visible on landing page
- Uptime monitoring active
- At least 1 testimonial from a paying beta tester

**Go criteria for full launch**:
- 2+ beta testers convert to paid
- No critical bugs in production
- At least 3/5 testers say they would recommend it to another consultant
- Model accuracy: <5% hallucination rate on product facts (spot-check 20 queries)

---

## 7. Risk Factors

### Risk 1: Mary Kay Corporate IP/Trademark (HIGH — Mitigatable)

**The actual threat**: Mary Kay Inc. launched its own AI tools in 2025 (Foundation Finder,
agentic AI portfolio per CIO Dive). They have a legal team watching third-party uses of
their brand. A product called "MK Copilot" using their product names in an AI model could
draw a cease-and-desist or trademark claim.

**Mitigation** (required before launch, not after):
- ToS must state: "Not affiliated with, endorsed by, or sponsored by Mary Kay Inc."
- Do NOT use Mary Kay's pink logo, trade dress, or official branding in the product UI
- Rebrand consideration: "Beauty Seller Copilot" or "Consultant AI" is safer than "MK Copilot"
  as the public-facing name. Keep MK branding internal/informal only.
- The model itself using product knowledge is different from trademark infringement —
  knowing facts about products is not infringement. Impersonating the company is.
- If Mary Kay corporate reaches out, this is actually a sales opportunity for an enterprise
  deal (the memory file lists this as revenue path #2). Do not panic — engage.

### Risk 2: Model Hallucination on Product Details (HIGH — Manageable)

The model answers questions about specific MK products. If it confidently gives a wrong
ingredient list or a discontinued product recommendation, the seller damages a customer
relationship and blames the tool.

**Mitigation**:
- Disclaimer in the UI on every response: "Always verify product details at marykay.com"
- ToS explicitly states AI output is for sales assistance only, not authoritative product specs
- During beta, monitor queries manually. Flag any hallucination reports immediately.
- Add a "thumbs down" feedback button to every response so testers can flag bad answers
- Before launch, run a known-answer test: 20 specific product questions with verified answers.
  Current 26/26 test pass rate is promising but those may be scripted tests, not edge cases.

### Risk 3: Spark-1 Service Conflicts (MEDIUM)

Spark-1 is running 12+ services. Several are already broken (ai-army-responder crash loop,
s3-state-backup failed, spark-cluster.service dead). Adding production user traffic to a
machine with known instability is a risk.

**Mitigation**: The MK model (:8767) is its own process. The other broken services do not
affect it directly. However, a Spark-1 reboot or OOM event affects everyone. For beta (5 users)
this is acceptable risk. For 50+ users, evaluate moving MK Copilot to a dedicated Docker
container or VPS instance.

### Risk 4: Consultant Churn Before Conversion (MEDIUM)

MK consultant turnover is 68.6% annually (FTC data). Many start, struggle to earn, and quit.
If beta testers churn from MK before the trial ends, they won't convert.

**Mitigation**: Screen beta testers for minimum 1 year tenure and active business. Exclude
brand-new consultants. The target profile in Section 3 is designed to filter this.

### Risk 5: Low Query Volume / Wrong Use Case (MEDIUM)

If testers log in once and never return, the product is solving the wrong problem or has
UX friction. This would be visible in usage logs by Day 10.

**Mitigation**: Onboarding call is mandatory. Do not just hand testers a login. Walk them
through 3 specific scenarios on the call. Usage below 5 queries/day by Day 7 is a warning
signal — do an emergency check-in call.

---

## 8. Revenue Projection

### Beta: 5 Sellers

- 5 testers, 14-day trial, target 40% conversion = 2 paying users
- 2 users at $29/month = **$58/month**
- Not meaningful revenue — this is a validation exercise, not a revenue event

### Signal Scenario: 20 Paying Users (Month 2-3)

- If beta validates and 20 consultants convert: $580/month
- Annual revenue: ~$7,000
- Still not a business, but proves the model converts

### Viable Business: 200 Paying Users

- $29/month x 200 = $5,800/month = **$69,600/year ARR**
- This is the first threshold where this is a real business worth investing in
- Achievable in 6-12 months if word-of-mouth works in MK communities

### Market Sizing: 1% Penetration of One City

Mary Kay has approximately 500,000-600,000 active US consultants (3M global, US is
largest market, estimated 17-20% of global total; 68.6% annual turnover means active base
is roughly that range at any given time). In a major metro (Dallas, Houston, Atlanta) there
are likely 5,000-15,000 active consultants.

1% penetration of Dallas metro (10,000 active consultants) = **100 paying users**
at $29/month = $2,900/month = **$34,800/year**.

1% penetration of the US active base (~600,000 consultants) = 6,000 users
at $29/month = $174,000/month = **$2.1M ARR**.

**Reality check**: 1% national penetration requires distribution, marketing, and brand
awareness that does not exist today. 1% in a single city is achievable through active
Facebook group outreach within 90 days. The $34,800/year single-city target is the
realistic 12-month anchor.

### White-Label Path (Bigger Number)

The memory file notes white-label for Avon, Herbalife as revenue path #3. These companies
have hundreds of thousands of consultants each. A white-label deal at $5/user/month with
Avon's 200,000 US reps = $1M/month. This is a 2-3 year play, not a beta play, but the
technology being built now is the proof of concept for that pitch.

### Competitive Pricing Context

General AI sales tools (Salesforce Einstein, Outreach) price at $100-$220/month for
enterprise. There is no known Mary Kay-specific AI assistant product available to
independent consultants as of March 2026. Mary Kay's own AI Foundation Finder is
consumer-facing (helps customers find shades), not a consultant productivity tool. This
is a clear gap in the market with no direct competitor identified.

---

## Recommendation: GO — With One Pre-Condition

**GO on beta launch.** The model works, the infrastructure is there, the market gap is real,
and there are no fatal flaws that should kill this before testing.

**Pre-condition**: Before the first tester logs in, add the disclaimer language to the ToS
and UI disavowing Mary Kay Inc. affiliation. This is a 30-minute legal task that eliminates
the highest-risk exposure. Do not skip it.

**First Move**: This week, create the Stripe account and add the Cloudflare route for
mk.ultrarag.app. These two steps take under 2 hours and make everything else possible.
The landing page and tester outreach follow in Week 2. Revenue is possible by Day 28.

---

## Cross-Domain Flags

1. **DataShield + Skin Analysis**: The vision pipeline (`~/mk-skin-analysis/`) uses the
   NVIDIA vision stack also used in DataShield. If OCR/vision accuracy becomes a product
   issue for skin analysis recommendations, DataShield's guardrails work applies directly.

2. **aihangout.ai**: If MK Copilot gains traction, a "direct sales consultant" vertical on
   aihangout.ai (where consultants share tips, AI-assisted content, etc.) is a natural
   cross-platform play. Not for now — flag for Month 3.

3. **White-label path**: A validated MK SaaS product is the prototype for the AI
   Infrastructure Benefit Plan (AIIBP) concept — AI tools sold as a benefit through
   employer/MLM company channels. This beta is the first proof of that model.

---

*Sources consulted: [Mary Kay AI strategy via CIO Dive](https://www.ciodive.com/news/mary-kay-AI-strategy-agentic-generative/806209/), [Mary Kay Foundation Finder](https://www.beautypackaging.com/breaking-news/mary-kay-introduces-ai-foundation-finder-tool/), [Rallyware consultant platform data](https://www.rallyware.com/case-study/modern-beauty-how-mary-kay-transformed-consultant-experience), [AI sales agent market sizing](https://www.lindy.ai/blog/ai-agents-sales), [DSA turnover data via Wikipedia](https://en.wikipedia.org/wiki/Mary_Kay)*
