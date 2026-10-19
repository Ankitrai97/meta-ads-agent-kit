# Private run records

`runs/<slug>/state.json` is a local progress record. The agent maintains it from actual user answers and observed results. It is ignored by Git. Do not put passwords, tokens, cookies, card details or real lead PII in it or its evidence files. Screenshots/exports need the same care.

Start with `templates/state.json`. `schema_version` is 1. `mode` starts as `demo`; use `live` only when the owner wants a real campaign. Live mode alone never authorizes activation. `stage` is a short human-readable progress label used with `NEXT.md`.

## Configuration

`configuration` contains the facts, settings and approved asset/lead mapping that define the review. Unknown fields stay null. Explicitly record “No special offer” or “None applies, checked against …” when that is the verified decision; don't use unknown/null to mean approved omission. Capacity is a positive number; record its unit/time period in `brief.md`. For a non-appointment campaign, use an appropriate outcome/capacity definition.

- `business`: name, one service/product, service_area list, customer, offer, capacity.
- `account`: actual ad-account ID, Page ID, currency and timezone. These are private working identifiers, not credentials.
- `budget`: amount, type (`daily`/`lifetime`), uppercase currency, start/end ISO timestamps **with UTC offsets**, maximum total the owner authorizes for the test. Record account timezone separately. This local maximum does not itself create a platform spending limit.
- `settings`: objective, geography list, audience, placements, optimization, category decision. Include additional exact reviewed settings as needed; they also enter the digest.
- `destination`: `instant_form` or `website`, actual form ID/URL reference, HTTPS privacy URL.
- `ads`: list of actual saved ad mappings: `id`, `concept`, approved `copy`, approved `asset` reference, `destination`. Preserve the approved file or its content hash in the private run; changing an asset under the same filename still needs review and a refreshed reference/hash. Record previews in evidence.
- `objects`: saved records with `kind` (`campaign`/`ad_set`/`ad`), `id`, `status`. All reviewed objects must be `PAUSED` before launch. Include the exact critical saved values here or elsewhere in configuration so changes affect the review digest.
- `lead_route`: owner, method (including an approved manual route), destination, response_expectation. Add actual field mapping, workflow version and caller/permission configuration when used; don't hide material changes outside the reviewed configuration.

## Checks and evidence

Each check has `passed: true/false` and a run-relative evidence filepath. A passed check requires a real nonempty evidence file under that run. The helper rejects missing, empty and outside-run evidence. It does not judge whether a file tells the truth; the agent must inspect actual external state.

| Check | Required observed criterion |
| --- | --- |
| brief_confirmed | User confirmed service, offer, geography, budget and outcome |
| account_ready | Correct account/Page identity, access, currency/timezone and visible readiness checked |
| research_done | Sources and useful distinctions saved, hypotheses labeled |
| settings_verified | Actual saved settings/object IDs compared with approved plan |
| creative_approved | Owner-approved copy/media mapping plus actual previews |
| lead_test_passed | Controlled test reached the intended destination and approved follow-up test |
| review_complete | Final packet compared to actual paused setup, blockers resolved |

Evidence should name source/tool, observed object ID/values, timestamp and result. A tool response or screenshot may be referenced without copying private contact/payment information. Don't mark “not applicable” checks passed to bypass the campaign's essential lead path; record the approved manual path and its test instead.

## Current owner approval

Run `python scripts/project.py status <slug>` or `check` to get the configuration SHA-256. After the owner actually approves the exact launch packet, record:

```json
{
  "decision": "activate",
  "by": "actual owner name or role",
  "at": "2026-10-19T10:00:00-05:00",
  "source": "reference to the actual user approval message",
  "config_sha256": "the digest printed for the approved configuration"
}
```

These example values are not an approval. The agent records the real decision; the helper never creates it. Any configuration change changes the digest and invalidates the old local approval. Review live values again because Meta can change outside these files. `check --launch` requires live mode, all readiness checks/evidence, paused reviewed objects and a current approval record. Even a passing result isn't authorization by itself.

After actual activation, update recorded statuses and `NEXT.md`. The prelaunch checker will then report non-paused objects; that is expected. It is a prelaunch readiness tool, not a campaign manager or delivery monitor.
