# Conversational prompt pack

You normally only need the starter message in the README. The agent uses these stages for you. For the accompanying video, prompts **1, 1B, 2, 3, 4 and 5** keep the same references as the v5 script. Account/connection help comes first when needed. Fill business-specific details through conversation; you don't need to paste a completed form.

## Start / continue

```text
Read AGENTS.md and playbook/START.md. Explain this repo, then help me run Facebook ads for my business. Ask one or two questions at a time and save my answers privately. First check whether we already have a run to continue. If I need help, offer browser assistance for the steps your tools support. Don't launch anything until I approve the exact setup and spend.
```

## Account setup — I don't have an account

```text
I don't have a Meta ad account, or I'm not sure what's already set up. Follow playbook/ACCOUNT-SETUP.md. Help me identify my existing Page/business assets before creating anything. Explain the next choice in plain English and offer browser help. Show me the proposed name, owner, currency and timezone before creating an ad account. I'll handle login, codes, payment entry and identity checks directly.
```

## Connections — help me choose and test access

```text
Follow playbook/CONNECTIONS.md. Check which tools are actually available in this session. Help me choose between my existing connector, browser help and guided manual steps. Don't assume a Meta MCP URL or install an unreviewed connector. Test the intended account read and save the capability results. Use paid tools only within a cost limit I approve.
```

## Prompt 1 — Business brief, market research and campaign plan

```text
Use my current private business run. If details are missing, collect them conversationally: business, one campaign service/product, service area, customer, approved offer, budget/currency/dates, capacity, destination, proof, Page identity and follow-up owner. Unknown facts stay unknown. Ask me for decisions that affect spend or what we can promise.

Research relevant competitors and their service areas, public customer reviews/questions, and context for my intended campaign dates. Save source URLs/access dates. Separate observations, inferences and test hypotheses; don't invent results or profitable competitor ads.

Inspect the actual connected account and available tools. Propose campaign/ad-set/ad settings, with reasons and plain-English explanations. Match the actual service area, available targeting controls, budget type/amount/currency, dates, destination, identities and tracking. Explain spend exposure and the difference between a daily budget and an actual total limit. Identify applicable platform category requirements for the offer.

Define a good outcome and how we'd track it. For a local service, distinguish leads, qualified leads and booked appointments. If a target is unknown, explain how we'd set a starting target and its assumptions. Save the plan and missing decisions. Don't create objects or activate anything yet.
```

## Prompt 1B — Apply the approved settings

```text
Use only the exact campaign plan and spend values I approved. Create the campaign and ad set PAUSED through supported tools. Return actual IDs, read back saved values, and compare with the plan. Before retrying a write, check whether it already created the object. If a capability is missing, use the agreed browser/manual route. Don't create unfinished ad objects, change unrelated campaigns, change spend or activate anything. Save what actually happened and the next step.
```

## Prompt 2 — Ad Library research through Apify or the browser

```text
Follow playbook/RESEARCH-AND-CREATIVE.md. Research a few relevant advertisers with the approved public-research route. Verify their service areas separately. If using Apify, inspect the Actor, actual fields, pricing and the agreed result/cost cap first. Otherwise use public web/browser research or ask me for sources.

Record source links/access dates, visible start/status, offer, opening message, creative format, CTA and destination. Include older ads where visible dates support it, but don't infer profit, continuous delivery, conversions or exact targeting from duration.

Use the research, my customer knowledge and approved proof to create original concepts. For each give primary text, headline, CTA, visual brief, proof/claim check and a hypothesis. Recommend a test size that fits my budget; three concepts are a useful example, not a requirement. Don't copy competitors or use another company's reviews/credentials. Save the drafts for my review.
```

## Prompt 3 — Creative, files and placements

```text
Use the concepts, copy and files approved in my run. Ask for missing actual file locations. Match assets to concepts; explain mismatches. Prefer approved real business media. If image generation is available and we choose it, make concepts that represent the business honestly. If it isn't useful, help me import a file made by me or an editor.

Prepare supported feed/vertical crops and actual previews. Check readable text, captions, claims, identity, CTA and destination. Show me the mapping and get the needed creative decision before assembling ads. Upload through supported tools or the agreed browser/manual route. Keep everything paused, preserve originals, return actual saved ad IDs/previews and save the asset/version references.
```

## Prompt 4 — Instant Form, CRM and follow-up test

```text
Follow playbook/LEADS-AND-MEASUREMENT.md. Use the destination and follow-up approach we chose. Inspect my existing form/website, lead access, CRM and automations before changing them. If I don't have a CRM, explain an appropriate simple route and let me choose; don't buy a new service automatically.

Propose field/source mappings, deduplication and visible failure handling. Ask who follows up, when, and how booking/handoff works. If we choose an AI caller, confirm its actual setup and contact boundaries before any real outreach. Store credentials only in the appropriate secret/credential service.

After the scoped changes are approved, use controlled demo details to trace a labeled test lead into the destination and approved follow-up test. Report actual successes and the last successful step if it fails. Don't simulate a successful connection or contact real leads during the test. Save evidence without real lead contact data and tell me what needs fixing.
```

## Prompt 5 — Review now; measurement later

```text
Compare my approved brief and plan with the actual saved account, campaign, ad set, ads, previews, form/website, tracking and lead route. Check geography, identity, budget/type/currency/dates/spend exposure, claims, destination and actual test evidence. Keep everything paused. Show mismatches and unresolved items, fix those within the approved scope, and save the final review packet.

Run the optional local readiness checker if available. Explain its limits: it checks saved records, not Meta itself. Show me the exact proposed activation scope and spend when the setup is ready. Record a launch decision only if I actually give it; configuration changes invalidate the prior review approval. A generic setup request isn't launch authorization.

Outline reporting that joins platform spend/leads to qualified/booked/won outcomes with source IDs and clear attribution windows. With no live data, give the measurement plan only. Later, show the period, spend, sample size, uncertainty and actual outcomes before recommending changes. Don't autonomously scale budgets or contact leads.
```
