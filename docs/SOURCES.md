# Maintained source references

Reviewed 19 October 2026. Interfaces, eligibility and available tools can change; confirm the current official docs/UI when actually setting up. These links support setup routes; they don't establish that a particular user's account or connector works.

## Agent entry points and tools

- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md): repository instructions.
- [Codex skills](https://learn.chatgpt.com/docs/build-skills): discoverable reusable instructions. This kit has a repository skill under `.agents/skills/`.
- [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp): host connection setup; check installed CLI help before editing configuration.
- [Claude Code memory](https://code.claude.com/docs/en/memory): project guidance through CLAUDE.md/AGENTS.md. The small CLAUDE.md here imports the shared entry point.
- [Claude Code skills](https://code.claude.com/docs/en/skills): the `.claude/skills/` entry point points to the shared playbook.
- [Claude Code MCP](https://code.claude.com/docs/en/mcp): authentication and scope choices for the selected connection.
- [Apify MCP](https://docs.apify.com/mcp): documented remote endpoint and Actor discovery/results. Choose/check the actual Actor and pricing; don't assume a generic connection includes a specific working scraper.

## Meta and lead routing

- [Meta Business Suite](https://business.facebook.com/) and [Ads Manager](https://adsmanager.facebook.com/): inspect the actual user's account and UI; login may be required.
- [Meta Blueprint: setting up a business portfolio](https://www.facebookblueprint.com/student/path/219702-set-up-business-portfolio-meta-business-suite): official portfolio setup education.
- [Meta Ad Library](https://www.facebook.com/ads/library/): public ad research. Visible dates/content alone don't reveal a local competitor's profitability; treat that as a limit of the evidence.
- [Meta ads and Pages transparency](https://about.fb.com/news/2018/06/transparency-for-ads-and-pages/): background on public visibility, not a current targeting/performance manual.
- [Meta lead retrieval developer guide](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/retrieving/): verify current requirements when integrating directly. Automated fetch was unavailable during this build; use the authenticated official guide/current UI rather than relying on unverified API specifics here.
- [n8n Facebook Lead Ads trigger](https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.facebookleadadstrigger/): verify current trigger/credential setup when this is the selected route. Existing workflow access and a real controlled test are still required.

No third-party Meta MCP provider has been selected or endorsed by this kit. It deliberately does not ship a guessed Meta endpoint, bearer token, personal connector configuration or production automation. A new user chooses available tools and proves their capabilities in their own account.
