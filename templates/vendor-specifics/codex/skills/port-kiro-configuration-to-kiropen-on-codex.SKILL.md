---
name: port-kiro-configuration-to-kiropen-on-codex
description: Port Kiro workspace configuration into Codex-compatible KirOpen assets without disturbing existing spec-driven workflow outputs.
---

# Port Kiro Configuration To KirOpen On Codex

Use this when a repository still contains Kiro-era configuration and the user wants it migrated into Codex-compatible KirOpen assets.

## Cross-Harness Confirmation Gate

If the user is actually targeting a different harness than Codex, do not proceed immediately.

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
- `.codex/agents/spec_mode.toml`

## Translation Targets

Prefer these Codex-native outputs:

- `.agents/skills/*/SKILL.md` for reusable workflows
- `.codex/agents/*.toml` for explicit custom agents
- `.codex/config.toml` for MCP configuration when the user explicitly wants project-level Codex config
- directory-scoped `AGENTS.override.md` files for situational context

Prefer these generated situational-context stubs when they fit:

- `.codex/copy-me-into-your-frontend-directories/AGENTS.override.md`
- `.codex/copy-me-into-your-api-directories/AGENTS.override.md`
- `.codex/copy-me-into-your-environment-directories/AGENTS.override.md`

## Mapping Rules

- Convert reusable Kiro workflow guidance into Codex skills.
- Convert Kiro steering into directory-scoped `AGENTS.override.md` files or other local Codex guidance surfaces.
- Convert `.kiro/settings/mcp.json` concepts into `.codex/config.toml` only when the user wants Codex MCP configured.
- Convert Kiro hook concepts into Codex hooks only if the target environment supports them and the user wants that behavior.
- Do not blindly copy Kiro-only frontmatter or JSON structure into Codex files.
- Preserve intent, not file format.

## Process

1. Inventory the existing `.kiro/` files.
2. Analyze the codebase structure to determine where frontend, API, environment, shared library, or other directory-scoped guidance actually belongs.
3. Classify each `.kiro` item as skills, steering, MCP, hooks, settings, or unsupported Kiro-only behavior.
4. Propose or create the closest Codex-native equivalent.
5. When situational context guidance fits one of the generated placeholder directories, copy the matching `AGENTS.override.md` content from `.codex/copy-me-into-your-...-directories/` into the target project directories that should receive it.
6. If the generated placeholders do not fit the codebase shape, create or adapt more appropriate directory-scoped `AGENTS.override.md` files instead.
7. Leave unsupported concepts as documented exceptions instead of inventing fake Codex behavior.
8. Keep spec workflow assets intact.

## Output Style

- Be explicit about what was ported directly, what was adapted, and what has no Codex equivalent.
- Prefer small targeted assets over one giant catch-all file.
- Include the codebase analysis that led to each target placement decision.
- Execute the fitting copy operations when the user is asking for the migration to be carried out, not just described.
