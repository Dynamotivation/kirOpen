# Port Kiro Configuration To KirOpen On Copilot

Analyze the repository's `.kiro/` folder and port the useful configuration into Copilot-compatible KirOpen assets.

## Cross-Harness Confirmation Gate

If the user is actually targeting a different harness than Copilot, do not proceed immediately.

1. Refuse execution once and ask for explicit confirmation.
2. Tell the user that the target harness may have better aptitude for its own conventions.
3. Continue only if the user explicitly confirms they still want to proceed.
4. If they do not confirm, stop and do not perform migration actions.

Inspect and classify:
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
- `.github/hooks/*.json` for workspace-scoped Copilot hooks in VS Code
- agent-scoped `hooks` frontmatter in `.github/agents/*.agent.md` when appropriate
- workspace MCP configuration where supported by the chosen Copilot surface

Keep the spec-driven workflow outputs alone. Do not rewrite or replace the existing KirOpen spec workflow assets.

When porting:
- preserve intent instead of copying Kiro file formats directly
- keep situational context in `.github/instructions/`
- keep reusable workflows in `.agents/skills/` and use `.github/prompts/` for one-off runs
- port Kiro hook behavior into `.github/hooks/*.json` or agent-scoped hooks when the target Copilot surface supports hooks
- explain any Kiro-only concepts that do not have a clean Copilot equivalent
- note that Copilot hooks are currently preview functionality in VS Code and may not apply to every Copilot surface

Reference:
- [kiropen agent](../agents/kiropen.agent.md)
- [kiropen-spec agent](../agents/kiropen-spec.agent.md)
