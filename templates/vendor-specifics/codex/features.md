# KirOpen On Codex

## Project Guidance

- By default, Codex checks `AGENTS.override.md`, then `AGENTS.md`, then any fallback names configured in `project_doc_fallback_filenames`, and it uses at most one instructions file per directory.
- Global guidance lives in `~/.codex/AGENTS.md` or `~/.codex/AGENTS.override.md`.
- In agent mode, this repo primarily uses `.codex/agents/*.toml` and `.agents/skills/*/SKILL.md` rather than a repo-wide `CODEX.md`.
- If the user explicitly wants default-behavior override mode, Codex-specific guidance can be emitted to `CODEX.md` and activated by `.codex/config.toml`.
- Codex does not use Copilot-style `.github/copilot-instructions.md` or `.github/instructions/*.instructions.md` files.

## Skills

- Codex uses skills for reusable workflows.
- Repository skills live in `.agents/skills/<skill-name>/SKILL.md`.
- Skills can also live in user, admin, and system locations.
- Skills may be invoked explicitly with `$skill-name` or selected implicitly from their `description`.
- Skills are the closest Codex equivalent to reusable prompt packs or workflow bundles.

## Custom Agents

- Codex custom agents live in `.codex/agents/*.toml` or `~/.codex/agents/*.toml`.
- Built-in agent types include `default`, `worker`, and `explorer`.
- Custom agents are narrow specializations for explicit subagent workflows, not a replacement for shared project guidance files such as `AGENTS.md` when the user intentionally wants workspace-wide behavior.

## Model Context Protocol (MCP)

- Codex configures MCP in `config.toml`, not in `mcp.json`.
- Use `~/.codex/config.toml` for user scope or `.codex/config.toml` for project scope.
- The Codex CLI and IDE extension share the same MCP configuration.
- Codex can manage MCP servers from the CLI with `codex mcp add`, `codex mcp list`, and related commands.
- In TOML, MCP servers live under `[mcp_servers.<name>]`.

## Hooks

- Codex has hooks, but they are experimental.
- Hooks live in `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`.
- Hooks require `[features] codex_hooks = true` in `config.toml`.
- Hooks are currently disabled on Windows, so do not promise Windows hook support.

## Plugins

- Codex documentation includes plugins as a packaging and distribution mechanism.
- This runtime does not expose dedicated plugin-management tools directly, so do not assume plugin install or update actions are available here.

## Kiro Compatibility Exceptions in KirOpen on Codex

- KirOpen on Codex does not support Kiro Powers. Translate powers into one or more depending on their scope and functionality: repo skills, MCP server configuration, hooks, or custom agents.
- Kiro steering files in `.kiro/steering/` do not have a direct Codex equivalent. Translate specific scoped instructions into `AGENTS.override.md` files and place them in the appropriate subdirectories. If not suitable to any one or more subdirectories, offer to add to the persistent project instructions in `CODEX.md`. Warn the user about increased token cost and possible drifting if the file ever gets overwritten, and get explicit user consent.
- Kiro's `.kiro/settings/mcp.json` and `mcpServers` JSON format do not apply in Codex. Use `.codex/config.toml` with `[mcp_servers.<name>]` tables instead. Offer to port MCP server schema by consulting the Codex documentation for MCP servers.
- Kiro's hook UI instructions do not apply in Codex. Codex hooks are configured in `hooks.json`. Offer to port hook schema by consulting the Codex documentation for hooks. Warn the user about experimental status and Windows incompatibility.

# Long-Running Commands Warning

- Never use terminal commands for long-running dev servers, watchers, or interactive applications unless the user specifically wants that and the environment supports it.
- Prefer one-shot commands for checks and tests.
