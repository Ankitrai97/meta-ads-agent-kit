---
name: ads-engine
description: Builds launch-ready Meta ad packages for local service businesses — hooks, copy, creative briefs, Instant Form spec, campaign settings, and an n8n/Marketing-API handoff JSON. Use whenever you need Meta ad copy, ad creative, lead-ad setup, competitor ad research, campaign settings, or anything that will be pushed to Meta.
---

# Ads Engine

Build launch-ready Meta ad packages for local service businesses (high-ticket, appointment
driven: roofing, solar, HVAC, boiler, plumbing, landscaping, windows, pest, pools).

These ads are built to feed a pipeline, not just to win a cheap click: lead submits an
Instant Form, lands in a CRM, and gets called fast. Every choice — form design, qualifying
question, thank-you message — serves that pipeline.

## The workflow

### Step 0 — Intake

Needed before writing: business name and niche, service area (city plus radius), the offer
and rough ticket size, monthly ad spend budget, any differentiators (guarantees, financing,
years in business, reviews), and optional competitor names or pages.

If several are missing, ask for them in one concise message. Never drip questions one at a
time. If told to use defaults, proceed with the niche playbook's standard assumptions and
say which assumptions were made.

### Step 1 — Research

- Read `references/niche-playbooks.md` for the niche: pains, angles, seasonal triggers,
  offers, qualifying question, CPL benchmark.
- Check the **Meta Ad Library** (facebook.com/ads/library — search the advertiser, filter
  Active). The signal that matters: ads running 60+ days are likely paying for themselves.
  Extract the angle, offer, format and hook style. Replicate the *structure* of what works,
  never the words.
- Treat any competitor notes or reference ads supplied in chat as primary research input.

### Step 2 — Build the ad package

Read `references/ad-craft.md` (what makes a winning ad) and `references/campaign-settings.md`
(campaign structure, Instant Form spec, n8n handoff format) before producing output.

Use this exact structure:

```
# Ad Package — [Business] · [Niche] · [Market]
## 1. Strategy snapshot        (angle + offer + why, 4 lines max)
## 2. Campaign settings        (table, per campaign-settings.md)
## 3. Instant Form spec        (fields, ONE qualifying question, thank-you screen)
## 4. Ad concepts              (3–5 conceptually DISTINCT concepts; each: name/angle,
                                hook, primary text, headline, description, CTA button,
                                creative brief)
## 5. n8n handoff JSON         (machine-readable block, per campaign-settings.md)
## 6. Launch checklist + kill/scale rules
```

Concepts must be different *angles* (problem, offer, proof, seasonal, financing), not five
rewrites of one idea. Meta's current delivery engine targets people through creative
differences, so variety is the targeting.

Deliver the package as a markdown file. Keep the chat summary to a few lines.

## Compliance guardrails (never skip)

- **Personal attributes policy:** never imply knowledge of a person's condition or finances.
  Write about the house or the situation, not the person. "Is your AC bill over $300?" is
  fine. "Struggling to pay your bills?" is not.
- **Special Ad Categories:** financing or loan-framed offers can trip the *Credit* category,
  which limits targeting. Prefer "flexible payment options" or "$X/mo" over loan, credit or
  approval language. Housing-adjacent messaging can trip *Housing*.
- No invented reviews, no fake countdown scarcity, no unverifiable claims. Deadlines must be
  real: rebate expiry, storm or insurance windows, seasonal booking cutoffs.
- Every claim must be provable by the business owner. If it cannot be proved, cut it.

## References

- `references/ad-craft.md` — anatomy of a winning ad: hooks, copy frameworks, offer
  engineering, creative briefs. Read before writing any concepts.
- `references/campaign-settings.md` — campaign structure, budgets, bidding, Instant Form
  spec, benchmarks, kill/scale rules, n8n/Marketing-API handoff JSON. Read before writing
  sections 2, 3, 5, 6.
- `references/niche-playbooks.md` — per-niche angles, offers, seasonal triggers, qualifying
  questions, CPL benchmarks. Read the relevant niche every time.

## A note on the benchmarks

The CPL figures in the playbooks are directional, drawn from US local service campaigns.
They are a sanity check, not a promise. Judge against your own niche and market, and track
cost per *booked* job in your CRM rather than cost per lead in Ads Manager.
