---
name: port-kiro-configuration-to-kiropen-on-copilot
description: Port Kiro workspace configuration into Copilot-compatible KirOpen assets without disturbing existing spec-driven workflow outputs.
---

# Port Kiro Configuration To KirOpen On Copilot

Use this when a repository still contains Kiro-era configuration and the user wants it migrated into Copilot-compatible KirOpen assets.

## Cross-Harness Confirmation Gate

If the user is actually targeting a different harness than Copilot, do not proceed immediately.

1. Refuse execution once and ask for explicit confirmation.
2. Tell the user that the target harness may have better aptitude for its own conventions.
3. Continue only if the user explicitly confirms they still want to proceed.
4. If they do not confirm, stop and do not perform migration actions.

## Scope

Inspect `.kiro/` and translate only the compatible configuration areas:

- `.kiro/skills/`
- `.kiro/steering/`
- `.kiro/settings/mcp.json`
- other `.kiro/settings/*` files
- hook definitions or Kiro-specific automation config
- vendor-specific Kiro guidance files

Do not disturb existing spec-driven workflow outputs such as:

- `.agents/skills/spec-driven-development/`
- `.agents/skills/requirements-engineering/`
- `.agents/skills/design-documentation/`
- `.agents/skills/task-breakdown/`
- `.agents/skills/quality-assurance/`
- `.agents/skills/troubleshooting/`
- `.github/agents/kiropen.agent.md`
- `.github/agents/spec-mode.agent.md`

## Translation Targets

Prefer these Copilot-native outputs:

- `.agents/skills/*/SKILL.md` for reusable workflows
- `.github/agents/*.agent.md` for specialist custom agents
- `.github/instructions/*.instructions.md` for path-scoped situational context
- `.github/prompts/*.prompt.md` for one-off runnable prompts
- `.github/hooks/*.json` for workspace-scoped Copilot hooks in VS Code
- agent-scoped `hooks` frontmatter in `.github/agents/*.agent.md` when appropriate
- workspace MCP configuration where supported by the chosen Copilot surface (`.vscode/mcp.json`, `settings.json`, or `~/.copilot/mcp-config.json`)

## Mapping Rules

- Convert reusable Kiro workflow guidance into skills under `.agents/skills/`.
- Convert Kiro steering into `.github/instructions/*.instructions.md` with appropriate `applyTo` globs.
- Convert `.kiro/settings/mcp.json` concepts into the documented Copilot MCP location for the active surface.
- Convert Kiro hook concepts into `.github/hooks/*.json` or agent-scoped hooks when the target Copilot surface supports them. Note that hooks are currently preview functionality in VS Code and may not apply to every surface.
- Do not blindly copy Kiro-only frontmatter or JSON structure into Copilot files.
- Preserve intent, not file format.

## Process

1. Inventory the existing `.kiro/` files.
2. Analyze the codebase structure to determine where frontend, API, environment, shared library, or other path-scoped guidance actually belongs.
3. Classify each `.kiro` item as skills, steering, MCP, hooks, settings, or unsupported Kiro-only behavior.
4. Propose or create the closest Copilot-native equivalent.
5. Leave unsupported concepts as documented exceptions instead of inventing fake Copilot behavior.
6. Keep spec workflow assets intact.

## Output Style

- Be explicit about what was ported directly, what was adapted, and what has no Copilot equivalent.
- Prefer small targeted assets over one giant catch-all file.
- Include the codebase analysis that led to each target placement decision.
- Execute the fitting operations when the user is asking for the migration to be carried out, not just described.
