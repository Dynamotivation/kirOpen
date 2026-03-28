# Port Kiro Configuration To KirOpen On Copilot

Analyze the repository's `.kiro/` folder and port the useful configuration into Copilot-compatible KirOpen assets.

Inspect and classify the same buckets every time:
- `.kiro/skills/`
- `.kiro/steering/`
- `.kiro/settings/mcp.json`
- other `.kiro/settings/*` files
- hook definitions or Kiro-specific automation config
- vendor-specific Kiro guidance files

Translate them into the closest Copilot-native outputs:
- `.github/agents/*.agent.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.agents/skills/*/SKILL.md`
- `.github/hooks/*.json` for repository hooks where the active Copilot surface supports hooks
- workspace or user MCP configuration where supported by the chosen Copilot surface

Keep the spec-driven workflow outputs alone. Do not rewrite or replace the existing KirOpen spec workflow assets.

When porting:
- preserve intent instead of copying Kiro file formats directly
- keep situational context in `.github/instructions/`
- keep reusable workflows in `.agents/skills/` and use `.github/prompts/` for one-off runs
- port Kiro MCP server intent server-by-server instead of copying `.kiro/settings/mcp.json` verbatim
- port Kiro hook behavior into `.github/hooks/*.json` only when the target Copilot surface supports hooks
- explain any Kiro-only concepts that do not have a clean Copilot equivalent
- note that hook support differs by Copilot surface, so the current GitHub docs for the chosen surface should win

For MCP, use this process:
1. Read each Kiro MCP server entry and extract the server name, transport type, startup command or URL, arguments, environment variables, auth requirements, and any tool allow/deny intent.
2. Choose the correct Copilot surface before writing config:
   - Copilot coding agent repository setup -> use the repository MCP configuration supported by GitHub docs for coding agent
   - Copilot CLI -> use `~/.copilot/mcp-config.json`
   - Custom agents -> use `mcp-servers` frontmatter only where GitHub docs support it
3. Translate each Kiro server into the native Copilot schema for that surface instead of copying Kiro JSON directly.
4. Keep secrets out of committed files unless the user explicitly wants them there.
5. If the active Copilot surface does not support the needed MCP behavior, leave a documented exception instead of inventing portability.

Official docs note:
- GitHub's MCP docs say Copilot coding agent can use local and remote MCP servers configured for the repository.
- GitHub's Copilot CLI docs say CLI MCP details are stored in `mcp-config.json` in `~/.copilot` by default.
- GitHub's custom agents docs document `mcp-servers` frontmatter for supported custom agent surfaces.

For hooks, use this process:
1. Check whether the target Copilot surface actually supports hooks.
2. If yes, translate the hook into `.github/hooks/*.json` with the nearest matching trigger.
3. If no, move the intent into instructions, prompts, MCP-backed validation, or leave it as an unsupported exception.
4. Do not invent agent-scoped hook frontmatter unless the current GitHub docs explicitly support it for the chosen surface.

Official docs note:
- GitHub's hooks docs say Copilot hooks live in `.github/hooks/*.json` in the repository.
- Those same docs say hooks are available for Copilot coding agent on GitHub and GitHub Copilot CLI.

Reference:
- [kiropen agent](../agents/kiropen.agent.md)
- [kiropen-spec agent](../agents/kiropen-spec.agent.md)
