# Meta Ads Agent Kit

**Open this folder in Codex, Claude Code, or another AI agent with file access. Tell it: “Help me set up my Facebook ads.”**

It walks you from your first questions to an inspected campaign, creative, lead capture, follow-up and reporting. You can start without a Meta ad account. Your agent asks for the details it needs, offers browser help, and remembers your answers locally.

Built by [Rapple AI](https://rappleai.com) for business owners who want to understand and run their own campaigns. The default examples use local service businesses; your actual business details drive the work.

## Start here — no coding required

1. [Download the kit](https://github.com/Ankitrai97/meta-ads-agent-kit/archive/refs/heads/main.zip) and unzip it, or clone this repository.
2. Open the **unzipped folder** as a project in your AI coding agent. Use your normal permissions; don't enable bypass modes.
3. Paste this:

   > Read AGENTS.md and playbook/START.md. Explain what this repo does in plain English, then help me set up my Facebook ads. Ask me one or two questions at a time. Save my answers so we can continue later. If something is difficult, offer to do that step in my browser.

4. Answer the questions. You can say “I don't know,” “I don't have an account,” or “Can you do that part for me?”

If your agent didn't load the instructions automatically, the starter message above tells it exactly what to read. An ordinary chat without project-file access needs the files attached or pasted; downloading the folder alone doesn't install tools in a chat app.

## What the conversation covers

| Step | What you get |
| --- | --- |
| Business | One service, service area, offer, budget and a clear definition of a good lead |
| Account | Existing-account check or guided Page, business portfolio and ad-account setup |
| Connections | Tested tool access, browser assistance, or a guided manual route |
| Research | Local market/customer research and competitor-ad observations with sources |
| Campaign | A proposed plan, then a paused campaign with saved settings checked |
| Creative | Different messages to test, copy, images/video and placement previews |
| Leads | Form or website, CRM routing, follow-up owner and a test lead |
| Launch | A short review of the exact campaign and spend before activation |
| Improve | Reporting that connects spend to qualified leads and booked appointments |

The agent offers: **“Would you like me to do this step in your browser, or walk you through it?”** It can act only when your agent supports browser control and you enable the relevant access. You handle passwords, verification codes, payment entry and identity checks in the official service.

## Use it again

Say “Continue my campaign,” “Explain this setting,” “Review these ads,” or “Help me connect my leads.” Answers and work live in `runs/<business-name>/`, excluded from Git. The agent resumes from there instead of interviewing you again. Use a separate run for each business. To switch computers, transfer that private run folder securely; a public GitHub fork is not your campaign backup.

## Tools and costs

The kit is free, open-source instructions and local helpers. It does **not** bundle a Meta connector, browser controller, CRM, image service, or AI subscription. Your agent uses your available tools and helps connect the ones you choose. Ad spend, AI subscriptions and optional third-party services have their own costs. There is no required paid research tool: public sources/manual research are supported.

There is no universal Meta MCP URL in this repo. Choose and verify an actual connector, its publisher, permissions and capabilities. Read-only access cannot create campaigns. The agent should say what it can do and use the browser/manual route where needed. See [connection options](playbook/CONNECTIONS.md).

## What gets approved

Research and local drafting proceed as part of the task. The agent checks the concrete plan before creating ad-account resources or a paused campaign. Spending, publication/activation, contacting real leads, paid tool runs and material budget changes need the relevant exact approval. Existing authorization is reused within its scope. You can finish the entire preparation without launching.

These files guide your agent; they aren't a technical lock on its external tools. Keep your normal tool approval controls enabled. The optional readiness checker checks local records; it cannot prove what is saved in Meta or authorize spending.

## Optional local helper

You don't have to type these yourself. Your agent can run them if Python 3.10+ is installed. Otherwise it can create the same files from the templates.

```sh
python scripts/project.py init my-business
python scripts/project.py status my-business
python scripts/project.py check my-business
python scripts/project.py check my-business --launch
```

`init` creates private working files without connecting to any service. `check` reports missing facts and evidence; `--launch` additionally checks the approval for the current settings. Neither command runs an ad. Read [the full roadmap](playbook/ROADMAP.md), [the conversational prompt pack](prompts/PROMPT-PACK.md), or [the fictional HVAC example](examples/dallas-hvac.md).

Stuck on a connection or setup step? See [common problems and the next action](docs/TROUBLESHOOTING.md).

## For contributors

Keep the experience conversational. Fix the canonical playbook rather than adding duplicated agent-specific workflows. Run `python -m unittest discover -s tests -v`. Current official references and verification limits are listed in [sources](docs/SOURCES.md). Contributions and reuse are covered by the [MIT license](LICENSE).
