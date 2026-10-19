# When something gets stuck

Tell your agent which step is difficult. It should inspect your private run, explain the specific problem and offer the next action, rather than restarting setup.

| What you see | What the agent should do |
| --- | --- |
| “I don't know if I have an ad account” | Offer to inspect business assets in the official Meta UI; don't create duplicates |
| Account creation disabled / verification requested | Record the actual message and guide the legitimate verification/support step; continue research and drafts |
| Meta connected but can't create | Check read versus write permissions and actual tools; offer browser/manual entry of the approved values |
| “Take my browser” but no browser tool exists | Explain the host's supported setup or guide one click at a time; don't claim control is available |
| Agent asks all the questions again | Read `runs/<business>/brief.md`, `state.json` and `NEXT.md`; ask only for missing/changed facts |
| Research tool failed or costs money | Check agreed cost limit; use public web/library or supplied links if no approved paid route |
| Generated image isn't right | Review the mismatch, use approved real media or make an editor brief, then import the finished file |
| Form submitted but no CRM record | Trace the last successful event, check permissions/mapping/integration, fix and retest with controlled details |
| “Ready” but some checklist items are missing | Name the missing evidence; a proposed setup is not a tested one |
| Owner approval became stale | Show what changed and review the current values; don't copy the old digest to bypass review |
| New computer has no progress | Transfer the private run securely or re-establish facts; downloading a public repo doesn't copy private sessions |
| Ads are active but not delivering | Inspect the actual review/delivery/account status; don't report success or increase spend to force delivery |

## If you only have a normal chat window

Ask the assistant to read attached `AGENTS.md`, `playbook/START.md`, `playbook/ROADMAP.md` and the relevant branch files. File editing, browsing and external tool access depend on that app. Without persistent project files, save the brief and continuation note yourself between sessions.
