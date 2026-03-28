---
name: port-kiro-configuration-to-kiropen-on-codex
description: Port Kiro workspace configuration into Codex-compatible KirOpen assets without disturbing existing spec-driven workflow outputs.
---

# Port Kiro Configuration To KirOpen On Codex

Use this when a repository still contains Kiro-era configuration and the user wants it migrated into Codex-compatible KirOpen assets.

## Scope

Inspect `.kiro/` and classify the same buckets every time:

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
- `.codex/agents/kiropen_spec.toml`

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
- Convert `.kiro/settings/mcp.json` concepts into Codex MCP entries server-by-server instead of copying Kiro JSON directly.
- Convert Kiro hook concepts into Codex hooks only if the target environment supports them and the user wants that behavior.
- Do not blindly copy Kiro-only frontmatter or JSON structure into Codex files.
- Preserve intent, not file format.

## MCP Porting

Port MCP in the same way every time:

1. Read each Kiro MCP server entry and extract the server name, transport type, startup command or URL, arguments, environment variables, auth requirements, and any tool allow/deny intent.
2. Choose Codex scope:
   - Use `.codex/config.toml` when the repo should carry shared Codex MCP setup.
   - Use `~/.codex/config.toml` only when the user wants a user-level setup and the repo should stay clean.
3. Translate each server into a Codex `[mcp_servers.<name>]` table instead of copying Kiro's JSON schema.
4. Preserve transport details:
   - STDIO server -> `command`, optional `args`, optional `env`, optional `cwd`
   - HTTP server -> `url`, plus auth/header fields when needed
5. Preserve tool restrictions when they exist by mapping them into `enabled_tools` or `disabled_tools`.
6. If the Kiro setup relied on OAuth or tokens, keep the secret in environment variables and wire the config to those variables instead of hardcoding secrets.

Official docs note:
- OpenAI's Codex MCP docs say Codex stores MCP config in `config.toml`, defaulting to `~/.codex/config.toml`, and project-scoped MCP can live in `.codex/config.toml` for trusted projects.
- The same docs say to either run `codex mcp` to add/manage servers or define `[mcp_servers.<name>]` tables directly.
- The CLI and IDE extension share the same MCP configuration, so one Codex MCP setup should be written once and reused.

## Hooks Porting

Port hook intent carefully, not automatically:

1. Check whether the user actually wants Codex hooks.
2. If yes, translate hook behavior into `.codex/hooks.json`.
3. Warn that Codex hooks are experimental, require `[features] codex_hooks = true`, and are currently disabled on Windows.
4. If the original Kiro hook behavior is risky, shell-heavy, or Windows-dependent, document it as a partial or unsupported port instead of forcing a broken Codex hook.

## Process

1. Inventory the existing `.kiro/` files.
2. Analyze the codebase structure to determine where frontend, API, environment, shared library, or other directory-scoped guidance actually belongs.
3. Classify each `.kiro` item as skills, steering, MCP, hooks, settings, or unsupported Kiro-only behavior.
4. Port skills, steering, MCP, and hooks as separate decisions instead of mixing them into one output file.
5. When situational context guidance fits one of the generated placeholder directories, copy the matching `AGENTS.override.md` content from `.codex/copy-me-into-your-...-directories/` into the target project directories that should receive it.
6. If the generated placeholders do not fit the codebase shape, create or adapt more appropriate directory-scoped `AGENTS.override.md` files instead.
7. Leave unsupported concepts as documented exceptions instead of inventing fake Codex behavior.
8. Keep spec workflow assets intact.

## Output Style

- Be explicit about what was ported directly, what was adapted, and what has no Codex equivalent.
- Prefer small targeted assets over one giant catch-all file.
- Include the codebase analysis that led to each target placement decision.
- Execute the fitting copy operations when the user is asking for the migration to be carried out, not just described.
