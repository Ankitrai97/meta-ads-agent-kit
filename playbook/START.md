# Start the conversation

## First turn

If asked what the repo does, answer in a few sentences: it helps the user plan and prepare Meta ads, connect leads to follow-up, and understand the decisions. It remembers the business locally. It needs their own accounts and available tools; it doesn't launch by itself.

Read `runs/*/state.json` and the latest `NEXT.md` if present. If there is one run, summarize its latest step and ask whether to continue. If several, ask which business. Don't expose one business's private details while selecting another. Don't ask for facts already confirmed unless something changed.

With no run, ask: **“What service or product do you want to advertise, and which area do you serve?”** These are one related question. Next ask whether they already have a Facebook business Page and ad account; “not sure” is a valid answer. Account inventory can begin while budget/offer decisions are pending.

Do not send a long intake form. Ask at most two related questions at a time. Explain unfamiliar choices only when they affect the next action. If the user gives a batch of facts, record all of them. When they don't know a marketing answer, recommend a starting choice with a reason and ask them to confirm it. Never guess factual credentials, financing, prices or account ownership.

## Save without asking them to manage files

Create a private run with `python scripts/project.py init <slug>`, or copy `templates/` and create `state.json` using `docs/STATE.md` if Python is unavailable. Don't overwrite another run. The helper creates no account and makes no network calls.

After each useful batch of answers/actions:

- Update `brief.md` and the matching fields in `state.json`. Null means unknown; don't replace it with a plausible value.
- Save research, plans, ad drafts and evidence in that run. Evidence records the observed account/object, relevant saved values, date and tool/UI source. Avoid real lead PII.
- Update `NEXT.md`: done, open decisions, exact next action and any approval scope. Keep it short.
- Mark a check passed only after its actual criterion is met. Explain “proposed,” “saved,” “verified” and “live” accurately.

The user can say “continue” in a later session. Read their run, state the next decision, and continue. Never infer tool/browser authorization still exists after switching accounts/sessions; confirm the actual available access.

## Help modes

Ask once when useful: “Would you prefer that I handle the steps I can, or explain them as we go?” Either way, ask for decisions that affect the business or spending, and reuse authorization within its recorded scope.

When a step feels difficult, offer: **“Would you like me to do this step in your browser, or walk you through it?”** If yes, identify the site, intended account, action and boundary. Start with a reversible task or inspect the page. Use only host-supported controls. Don't describe browser help as installed by this repo.

Let the user type passwords, codes and card details in the official page. Wait for them to finish. If Meta asks for verification, a review or an eligibility step the agent cannot do, give that one action and record the blocker. Continue independent preparation. Do not evade restrictions with fake profiles, borrowed accounts or repeated account creation.

## Keep it moving

Use `ROADMAP.md` to pick the earliest incomplete prerequisite. Don't restart a completed stage or create a new stack when an existing system fits. At each checkpoint, show the actual result, the one thing requiring a decision, and what happens next. A setup can finish at “ready for owner review”; launching is a separate decision.
