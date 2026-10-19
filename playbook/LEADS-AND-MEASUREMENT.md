# Lead capture, follow-up, launch and measurement

## Choose one path

Recommend Instant Form → existing CRM for a simple local-service demonstration when it fits. A website/calendar/video page may be better for another offer or existing funnel. Explain that tradeoff, then choose with the user; don't build both paths without a reason.

For an Instant Form, confirm identity, contact fields, useful qualifiers, privacy URL, completion message and follow-up expectation. Ask only questions useful to qualification or the next conversation. For a website, check the exact landing page, mobile experience, form/booking behavior, thank-you event and supported tracking. Validate actual Pixel/CAPI/event setup where used; don't claim conversion tracking is working from a code snippet alone. Inspect current documentation for installation details.

## Connect to what the user already uses

Inspect their CRM and existing automations before creating another system. For a user without a CRM, explain simple choices such as the platform's lead tools or an existing spreadsheet/manual follow-up route; help them choose based on volume/ownership. Don't silently buy a CRM. A reliable manual owner-notification path can be the initial setup if approved, visible and tested.

For n8n or another tool, inspect supported Meta lead triggers/retrieval and actual permissions. A webhook URL alone is not a complete lead integration. Map contact, qualification answers and source/form/campaign IDs; use the lead ID for deduplication when available. Store secrets in the tool's credentials facility. Plan retries/error notifications so failed delivery is visible; avoid duplicate outreach on retry.

Record follow-up owner, response expectation, booking destination and what happens when nobody responds. If an AI caller is chosen, confirm identity/introduction, permission/consent requirements appropriate to the actual deployment, hours/timezone, human handoff and failure route before enabling real outreach. Don't claim the voice is indistinguishable from a person. Don't contact real people during a demo test.

## Prove the handoff

Use the official supported test-lead method or a controlled submission. Don't expose real phone/email data in public artifacts. Trace the event through the integration into the destination and the approved follow-up test. Record the observed IDs/source, mapped fields, deduplication behavior and actual follow-up task/controlled action. If a stage fails, record the last successful step and fix/retest. A diagram or proposed workflow does not pass `lead_test_passed`.

## Final review and owner decision

Read the actual saved account/campaign/ad-set/ad/form values and previews. Compare them to the approved brief, settings and assets. Confirm statuses remain paused, budget type/currency/dates/timezone/exposure, actual service area, identities, claims, destination, tracking and the lead test. Record evidence in `launch-review.md`. Run the optional checker and resolve missing items.

Show the owner a concrete launch packet. Capture their exact approval scope and the current configuration digest in `state.json`; don't fill the approval yourself without their real decision. Changing reviewed settings/assets/lead mapping invalidates the prior digest and requires the applicable updated approval. Local records support review; inspect live objects again before activation.

## After a launch the owner authorized

Activate only those objects and spend values. Read statuses and report whether objects are active, pending review, rejected, or actually delivering. Record actual results in `NEXT.md`; a tool success message isn't evidence of delivery. Don't auto-increase budgets or modify the offer based on one cheap lead.

Join Meta spend/leads/source identifiers to CRM qualified/contacted/booked/won outcomes using documented definitions and date/attribution windows. CPL = spend / leads; booked cost = spend / booked appointments. Return “not enough data” when the denominator/sample is insufficient. Do not manufacture a KPI from test data. Explain gaps in attribution or delayed outcomes. Propose the next test with its data, uncertainty and spend implications; execute budget or outreach changes only within the current explicit authorization.
