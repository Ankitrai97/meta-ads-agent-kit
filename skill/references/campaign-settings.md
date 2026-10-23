# Campaign Settings — 2026 structure, Instant Forms, and the n8n handoff

## Default campaign structure (local lead gen, 2026)

One campaign per client per offer. Simple beats clever — Andromeda does the segmentation.

| Setting | Default | Why |
|---|---|---|
| Objective | Leads (`OUTCOME_LEADS`) | Optimizes for form submits |
| Type | Advantage+ Leads campaign where available | ~10% lower cost per qualified lead in Meta's testing |
| Budget | CBO, campaign level | Let the algorithm allocate |
| Daily budget | ad-spend/mo ÷ 30 (a $1.5k–$3k/mo budget lands at $50–$100/day) | Below ~$50/day learning is slow |
| Ad sets | ONE, broad | Creative is the targeting |
| Location | Radius around service area, 15–50 mi (1 mi min, 50 max in US) | Only pay for people the client can serve; tighter radius = cheaper leads |
| Age | 28–65+ | Homeowner skew without strangling delivery |
| Detailed targeting | None (broad) | Andromeda-era default |
| Placements | Advantage+ (all) | Let Meta allocate |
| Bidding | Highest volume (default) | Cost cap only later, at scale, to defend CPA |
| Conversion location | Instant Forms | Feeds CRM → AI dialer |
| Special Ad Category | Declare ONLY if genuinely credit/housing | Wrongly triggering it kneecaps delivery; financing-worded ads risk forced Credit categorization |

**Learning phase:** ~50 conversions/week per ad set is the ideal; local budgets rarely hit it — expect 1–2 weeks of noise. Do not edit budget/creative for the first 7 days unless spend is clearly burning (see kill rules).

## Instant Form spec

Always **Higher Intent** form type (adds a review screen — slightly higher CPL, meaningfully better lead quality for the AI dialer).

1. **Intro card**: restate the offer in one line + one qualifying expectation ("Serving [area] homeowners").
2. **Prefill fields**: full name, phone, email. Phone is the money field — the AI voice agent dials it.
3. **Exactly ONE custom qualifying question** (multiple choice). More questions raise CPL; zero questions flood the dialer with browsers. Pick from the niche playbook (e.g., "Do you own your home?" / "Is your roof over 10 years old?" / timeline question).
4. **Review screen**: on (that's the Higher Intent part).
5. **Thank-you screen**: set the callback expectation explicitly — *"Keep your phone handy — you'll get a call from our team in the next minute."* This turns the 60-second AI call into a promise kept, and lifts answer rates.

**Lead delivery:** leads must NOT sit in Meta. Wire the form to the CRM instantly: Meta webhook (`leadgen` field on the Page subscription) → n8n → CRM → AI dialer trigger. CSV download is a failure mode.

## Benchmarks (US local services, directional)

| Niche | CPL target | Notes |
|---|---|---|
| HVAC / plumbing | $35–55 | Emergency angles run cheaper |
| Roofing | $25–50 | Storm windows can hit single digits |
| Solar | $40–80 | Qualify hard; junk lead risk highest |
| Boiler/heating | $30–55 | Strongly seasonal |
| Landscaping/hedge | $15–35 | Lower ticket end |
| Windows/remodel | $40–70 | Longer cycles |

Cross-industry lead-campaign averages: CPC ≈ $1.9, CPL ≈ $28. Judge against niche, not average. What actually matters downstream: **cost per BOOKED appointment** — track it in the CRM, not Ads Manager.

## Kill / scale rules

- **Kill an ad**: spend ≥ 3× target CPL with zero leads, or CPL ≥ 2× target after ≥ $100 spend post-learning.
- **Scale**: raise budget +20% at a time, max every 3–4 days (bigger jumps reset learning).
- **Refresh**: rotate new concepts every 3–4 weeks; frequency > 3 on a small radius = fatigue, refresh sooner.
- **Lead quality veto**: if the AI dialer reports garbage contacts, fix the qualifying question/form type before touching budgets — cheap bad leads are expensive.

## n8n / Marketing API handoff JSON

Every ad package ends with this machine-readable block so your n8n workflow (or a Meta MCP) can create objects via the Marketing API without a human re-typing settings. Field names mirror the API's.

```json
{
  "client": "Client Name",
  "meta": {
    "ad_account_id": "act_XXXX",
    "page_id": "PAGE_ID",
    "instagram_actor_id": null
  },
  "campaign": {
    "name": "{brand}-{niche}-Leads-{YYYYMM}",
    "objective": "OUTCOME_LEADS",
    "buying_type": "AUCTION",
    "special_ad_categories": [],
    "daily_budget_cents": 7500,
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    "status": "PAUSED"
  },
  "adset": {
    "name": "Broad-{radius}mi",
    "optimization_goal": "LEAD_GENERATION",
    "billing_event": "IMPRESSIONS",
    "destination_type": "ON_AD",
    "targeting": {
      "geo_locations": {
        "custom_locations": [
          {"latitude": 0.0, "longitude": 0.0, "radius": 25, "distance_unit": "mile"}
        ]
      },
      "age_min": 28,
      "age_max": 65
    },
    "status": "PAUSED"
  },
  "lead_form": {
    "name": "{client}-higher-intent-v1",
    "follow_up_action_url": null,
    "question_page_custom_headline": "…",
    "questions": [
      {"type": "FULL_NAME"},
      {"type": "PHONE"},
      {"type": "EMAIL"},
      {"type": "CUSTOM", "label": "…", "options": ["…", "…"]}
    ],
    "higher_intent": true,
    "thank_you_page": {"title": "…", "body": "Keep your phone handy — you'll get a call in the next minute."}
  },
  "ads": [
    {
      "concept": "concept-name",
      "creative": {
        "format": "VIDEO_9_16 | IMAGE | CAROUSEL",
        "primary_text": "…",
        "headline": "…",
        "description": "…",
        "call_to_action_type": "LEARN_MORE | GET_QUOTE | APPLY_NOW",
        "asset_brief": "what to shoot/build — the media itself is produced separately"
      },
      "status": "PAUSED"
    }
  ],
  "lead_routing": {
    "delivery": "webhook",
    "flow": "meta leadgen webhook -> n8n -> CRM -> AI dialer (call within 60s)",
    "crm_pipeline_stage": "New Lead"
  }
}
```

Notes for the n8n build (context, not tasks for this skill):
- Everything created `PAUSED`; you flip live after review in Ads Manager.
- Lead retrieval: subscribe the Page to `leadgen` webhooks; on event, GET `/{leadgen_id}` with the Page token, map fields, push to CRM, trigger dialer.
- Reporting pull for dashboards: `/{ad_account}/insights` with `spend, impressions, ctr, cpm, actions(lead)`, daily, then join with CRM booked-appointment data for cost-per-booked-job.
