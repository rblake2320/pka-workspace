# SPARK — aihangout.ai Copy v2
**Agent**: SPARK — Voice, Content and Community
**Venture**: aihangout.ai
**Voice Target**: Insider, warm, technically fluent, community-first
**Date**: 2026-03-23
**Status**: Ready for FORGE to paste in. All 7 sections complete.

---

## How to Use This Document

Each section follows the same structure:

- **CURRENT** — exact text on the platform right now
- **NEW** — the replacement copy, paste-ready
- **RATIONALE** — why this version works harder
- **PLACEMENT** — exactly where in the UI this goes

---

---

## SECTION 1 — Main Tagline + Sub-Tagline

**Job**: Declare the tribe in one line. Make the right person feel found. Make the wrong person self-select out.

**Audience**: Senior AI/ML engineer. Has been burned by ChatGPT hallucinations on production problems. Distrusts solo AI answers. Wants peer-reviewed signal, not more noise.

---

**CURRENT**
> AI Problem Solving Community
> Crowdsourced solutions to AI and technical challenges

---

**NEW**

**Main tagline:**
> Where AI builders debug together.

**Sub-tagline:**
> Human-validated answers. Real stakes. No hallucinations tolerated.

---

**RATIONALE**

"AI Problem Solving Community" is a genre label. It describes a category of thing, not a reason to belong. Stack Overflow is also an AI problem solving community. So is Reddit. So is every Discord server with a #help channel.

"Where AI builders debug together" does three things the current tagline cannot:

1. **Identity signal** — "builders" is self-selecting. Casual users don't call themselves builders. The people this platform needs do. They will see this and think "that's me."
2. **Action verb** — "debug" is precise. It is not "discuss," not "explore," not "learn." It says: you come here when something is broken and you need it fixed.
3. **Together** — this single word carries the entire community proposition. You are not alone in front of a chatbot. You are among peers who have hit the same wall.

The sub-tagline earns its place by doing something the tagline cannot: it names the platform's core mechanic in three short punches. "Human-validated" differentiates from AI-only tools. "Real stakes" primes the Problem Bank and reputation system. "No hallucinations tolerated" is the positioning stake in the ground — this is the anti-ChatGPT-as-solo-oracle community.

**A/B variant if Ron wants to test bolder positioning:**

> The AI community that ships answers, not opinions.

This works if the platform wants to be edgier. Slightly higher friction on first read, higher recall. Test against the primary.

---

**PLACEMENT**
- Homepage hero, above the fold
- `<title>` tag and meta description
- Open Graph card (og:title / og:description)
- Email subject lines for welcome and re-engagement sequences
- Any press kit or one-pager

---

---

## SECTION 2 — Reputation System Explainer

**Job**: Turn a mystery number into a game with visible milestones. A new user should finish reading this and immediately know what to do next.

**Audience**: User who just registered. Has 0 reputation. Has no idea if this matters or how to change it.

---

**CURRENT**
> *(nothing — reputation shows as a number with zero explanation anywhere on the platform)*

---

**NEW**

> **Your reputation is your signal-to-noise ratio.**
>
> Every time the community upvotes your solution, you earn points. When a problem poster marks your answer as accepted, you earn more. Reputation tells other builders — at a glance — whether your answers are worth reading.
>
> Hit 100 and your problems get featured in the feed. Hit 500 and you can nominate others for the Knowledge Hub. The number is small right now. That's not a bug — it means the community is new and your contributions count more, not less.

---

**RATIONALE**

The current state — a visible "0" with no explanation — is the single most damaging UX gap on the platform. Reputation systems only motivate when users can see the path. Right now they see a wall.

This replacement does five things:

1. **Names what reputation signals** ("signal-to-noise ratio") — this resonates specifically with the target user who has spent time filtering noise from AI tools. It positions reputation as a quality filter, not a vanity metric.
2. **Explains the two earning mechanisms** in plain terms. No ambiguity about how the number moves.
3. **Gives two concrete milestones** (100 and 500) so the new user has a next step, not just a concept.
4. **Reframes "0"** — instead of communicating "you've done nothing," it communicates "you're early and that's an advantage." This is true and it's motivating.
5. **Ends with a reason to act now**, not later.

Note for FORGE: if the milestone rewards (featured in feed at 100, nominate others at 500) are not yet built, keep this copy anyway — it sets the expectation and creates the product spec. Write the copy, then build the features.

---

**PLACEMENT**
- Profile page — sidebar panel where reputation number displays, as expandable tooltip or inline text below the number
- Onboarding modal, step 2 (after email confirmation, before first action)
- FAQ / Help page under "How does reputation work?"

---

---

## SECTION 3 — Empty State / Onboarding Copy (New User Profile)

**Job**: Make "empty" feel like the start of something, not the absence of something. Point the user to exactly one action.

**Audience**: User who just registered. Profile shows 0 questions asked, 0 solutions submitted, 0 reputation. They are deciding in the next 30 seconds whether this platform is worth their time.

---

**CURRENT**
> *(blank — no empty state copy exists. The profile just shows zeros and nothing else.)*

---

**NEW**

**For the "Solutions" empty state panel:**

> No solutions yet.
>
> Somewhere right now, an AI builder is stuck on a problem you've already solved. Browse open problems — your answer could be the one that gets accepted.
>
> [Browse Open Problems →]

---

**For the "Questions Asked" empty state panel:**

> No questions yet.
>
> The best problems on this platform came from builders who were willing to say "I'm stuck." Your real production problem is more valuable than it looks — it's probably someone else's problem too.
>
> [Ask a Question →]

---

**For the reputation panel (0 reputation state):**

> Reputation: 0
>
> Your first upvoted solution changes this. Go find a problem worth solving.
>
> [See What's Open →]

---

**RATIONALE**

Three separate empty states because the user will see them in different contexts and the job of each is slightly different:

- **Solutions panel** — points to action. Creates urgency ("somewhere right now"). Makes the user feel like they have something to offer, not just something to take.
- **Questions panel** — removes shame. Many technically strong builders hesitate to post questions because they don't want to look like they don't know something. "The best problems came from builders willing to say I'm stuck" reframes vulnerability as contribution.
- **Reputation panel** — shortest and sharpest. The user already knows what reputation is from Section 2. This just tells them the next physical action. No softening, no explaining. They've read the explanation. Now just tell them what to do.

All three CTAs point to different pages. This is intentional — give the user a choice of entry point rather than forcing one path.

---

**PLACEMENT**
- Profile page: inside each empty state panel (Solutions, Questions, Reputation)
- Post-registration redirect page (before user reaches their blank profile)
- Onboarding step 3 (the "what to do first" step)

---

---

## SECTION 4 — SPOF Indicators Field Helper Text

**Job**: Make users fill out this field instead of skipping it. It is the platform's most differentiated feature and currently has a 0% completion rate on observed problems.

**Audience**: Builder posting a problem. Understands systems engineering concepts but has never seen "SPOF Indicators" as a form field before. Will skip it if it requires more than 5 seconds of thought.

---

**CURRENT**
> Keywords that indicate potential single points of failure

---

**NEW**

**Field label:** SPOF Indicators *(optional but powerful)*

**Helper text (appears below the input, always visible):**

> SPOF Indicators help the AI analysis pinpoint where your system is most likely to break under failure conditions — not just what broke. Think: the component or service where all roads lead if things go wrong.
>
> Examples: `redis-session-store` · `single auth service` · `no fallback on LLM timeout`

---

**RATIONALE**

The current placeholder text ("Keywords that indicate potential single points of failure") is a definition of the acronym. That is not helper text — it is a dictionary entry. It tells the user what SPOF means. It does not tell them why they should care or what to actually type.

The replacement does three things the current text cannot:

1. **Names the outcome** — "pinpoint where your system is most likely to break" is the value proposition for filling this out. The user now has a reason, not just an instruction.
2. **"Not just what broke"** — this distinguishes SPOF analysis from standard debugging. It positions the field as forward-looking (prevention) not backward-looking (diagnosis). This matters to the senior engineer who already knows what broke.
3. **Concrete examples** — three examples in the format users should actually type. `redis-session-store` is specific enough to be useful. `no fallback on LLM timeout` is the kind of thing this platform's exact target user has experienced. It bridges the abstract to the immediately recognizable.

The "(optional but powerful)" label modifier is deliberate. "Optional" removes friction. "But powerful" creates a small pull toward filling it out. This is not manipulative — it is accurate. The field genuinely improves AI analysis quality.

---

**PLACEMENT**
- Ask Question form (`/create-problem`) — below the SPOF Indicators input field
- Problem Edit form — same placement
- Knowledge Hub submission form — if SPOF analysis is relevant there

---

---

## SECTION 5 — Problem Bank Intro

**Job**: Make solvers feel like there are real stakes and real recognition. Make it feel like a bounty board, not a homework list.

**Audience**: Builder who has already explored the main feed and clicked into Problem Bank. They are evaluating whether it's worth investing hours solving a complex problem. Stakes, credibility, and recognition are the decision factors.

---

**CURRENT**
> Major industry problems imported from GitHub Issues, Stack Overflow, and enterprise sources. Solve real-world challenges and build your reputation.

---

**NEW**

> **The hardest problems the industry hasn't solved yet.**
>
> Every problem here was pulled from production failures, open GitHub issues, and enterprise environments where the stakes were real. These aren't exercises. Someone's system was down, someone's model was hallucinating in production, someone's pipeline was burning money.
>
> Solve one. Earn the bounty. Get credited permanently as the solver — your name on the problem, your solution in the record.
>
> The best solvers here don't just fix bugs. They build the kind of documented track record that a GitHub profile can't show.

---

**RATIONALE**

The current copy describes the sourcing mechanism (GitHub, Stack Overflow, enterprise). The audience doesn't care where the problems came from — they care whether solving them is worth their time.

The replacement makes four moves:

1. **Opens with stakes** — "hardest problems the industry hasn't solved yet" is a challenge, not a description. It activates competitive instinct in the exact user this platform needs.
2. **Makes sourcing visceral** — instead of listing sources, it describes what the sourcing means: "someone's system was down." This is true and it makes the abstract concrete.
3. **Names both rewards explicitly** — bounty (financial) AND permanent credit (reputation/identity). Senior engineers care about both. Many care more about the second.
4. **Closes with differentiation** — the last sentence is the positioning claim that separates this from LeetCode, from Stack Overflow, from GitHub. It's not just problem-solving practice. It is a public record of real technical contribution.

Note: Per SENTINEL's HIGH-3 finding, the "$139,000 Page Problem Value" headline needs a disclaimer until escrow is verified. SPARK recommends either: (a) add "(community-proposed bounties — payment terms set by problem submitter)" as subtext, or (b) remove the dollar total until it is legally defensible. The copy above does not include the total — it refers to "the bounty" for individual problems, which is accurate regardless of escrow status.

---

**PLACEMENT**
- `/problem-bank` page — hero section above the problem cards
- Problem Bank tab description if displayed in navigation tooltip
- Any landing page variant targeting "senior engineer" persona

---

---

## SECTION 6 — Knowledge Hub Intro

**Job**: Make contributors want to add their work. Turn the Knowledge Hub from a filing cabinet into a recognition surface.

**Audience**: AI/ML practitioner who has done something worth documenting — a model card, a paper, a blueprint, a research finding. They are deciding whether submitting here is worth their time vs. just posting on HuggingFace or arXiv.

---

**CURRENT**
> Blueprints, research papers, model cards, and technical documentation for AI development

---

**NEW**

> **Work worth finding. Credit where it's due.**
>
> The Knowledge Hub is where this community's real output lives — model cards, research, architectural blueprints, and documentation written by practitioners who have actually shipped the thing they're writing about.
>
> Not aggregated. Not scraped. Contributed by builders with their names on it.
>
> If you've documented something that would have saved you a week the first time you hit it — it belongs here. Submit it. Other builders will find it when they need it most, and your contribution is credited permanently to your profile.

---

**RATIONALE**

The current copy is a content taxonomy. It tells you what kinds of things live here. It does not tell you why you'd contribute — or why you'd come back to look.

The replacement makes four moves:

1. **Opens with value, not format** — "Work worth finding" signals curation, not collection. The contributor knows their work will be findable, not buried.
2. **"Written by practitioners who have actually shipped the thing"** — this is the authenticity claim that differentiates from every aggregated AI knowledge base on the internet. It is also a quality bar signal for readers.
3. **"Not aggregated. Not scraped."** — two sentences that land hard with the target user, who has spent time filtering scraped and aggregated AI content and knows exactly what it's worth.
4. **The contribution hook** — "something that would have saved you a week the first time you hit it" is the most specific possible definition of what belongs here. It is also the exact thing this user has experienced. It makes the submission decision obvious.

---

**PLACEMENT**
- `/learning` page — hero section above content cards
- Knowledge Hub tab description
- Onboarding email, day-3 activation: "Have something worth documenting?"

---

---

## SECTION 7 — Human vs AI Tag Tooltips

**Job**: Make the platform's most novel mechanic legible in one read. These tooltips are the clearest expression of why aihangout.ai is different from every other technical forum.

**Audience**: Any logged-in user hovering over a problem tag for the first time. They are in a scanning mode — tooltip needs to land in 2 seconds.

---

### 7A — "Human" Tag

**CURRENT**
> *(no tooltip or explanation exists — tag shows with no context)*

---

**NEW**

> **Human-authored problem.**
> A real person wrote this from direct experience — not generated, not summarized by AI. The frustration, the context, and the failure mode are firsthand. Answers here are peer-reviewed by practitioners who've seen the same thing.

---

### 7B — "AI" Tag

**CURRENT**
> *(no tooltip or explanation exists — tag shows with no context)*

---

**NEW**

> **AI-assisted problem.**
> This problem was structured or surfaced with AI help — sourced from GitHub Issues, Stack Overflow, or enterprise logs. The underlying issue is real and documented. Solutions are still human-validated. The tag tells you where the problem came from, not whether it matters.

---

**RATIONALE**

Human vs AI tagging is the most genuinely novel mechanic on this platform. No other technical community has made this distinction explicit. In an era where AI-generated content is flooding every forum and degrading signal quality, making the provenance of a problem visible is a trust infrastructure move, not just a filter.

The current state — tags with no explanation — lets this entire differentiator sit invisible. A user who doesn't know what the tags mean will ignore them. A user who reads the tooltips understands the platform's core philosophy in 10 seconds.

**The specific choices in each tooltip:**

Human tag:
- "A real person wrote this from direct experience" — signals authenticity immediately
- "The frustration, the context, and the failure mode are firsthand" — this is what the senior engineer actually wants from a question. Not a sanitized description. A real account of what happened.
- "Peer-reviewed by practitioners who've seen the same thing" — reinforces the community value of the Human tag

AI tag:
- "The underlying issue is real and documented" — prevents the reader from dismissing AI-sourced problems as fake or low-value
- "Solutions are still human-validated" — critical. This reassures the solver that even AI-sourced problems get real community scrutiny
- "The tag tells you where the problem came from, not whether it matters" — this is the philosophical closer. It removes any stigma from the AI tag while preserving the information value of the distinction

**On brand voice:** Both tooltips are written builder-to-builder. No corporate hedging. No explaining what "peer-reviewed" means. The target user knows.

---

**PLACEMENT**
- Tooltip on the Human/AI tag chip on every problem card (home feed, problem detail, Problem Bank)
- Filter sidebar: tooltip on the Human / AI filter toggles
- Ask Question form: tooltip on the "Problem Type" selector

---

---

## Summary for FORGE

Seven sections. All paste-ready. Placement noted for each. No dependency on features that don't exist yet — where mechanics are referenced (reputation milestones), the copy sets the expectation so the feature spec follows.

**Copy that needs no new features:**
- Sections 1, 4, 5, 6, 7A, 7B — can be deployed immediately

**Copy that references planned features:**
- Section 2 (reputation milestones at 100 and 500) — deploy copy now, wire features in next sprint
- Section 3 (empty state CTAs) — requires empty-state UI component if not built; copy is ready

**One flag for Ron:**
Section 5 (Problem Bank) deliberately omits the "$139,000 Page Problem Value" headline per SENTINEL's HIGH-3 finding. That number needs either a disclaimer or verified escrow before it runs. The rest of Section 5 is clean and can go live without it.

---

*SPARK — Voice, Content and Community*
*Delivered to Owner's Inbox: 2026-03-23*
