# Features

## Custom Instructions

- In agent mode, Copilot behavior is primarily carried by `.github/agents/*.agent.md`.
- If the user explicitly wants default workspace behavior, repository-wide instructions can live in `.github/copilot-instructions.md`.
- Path-specific instructions live in `.github/instructions/*.instructions.md` with `applyTo` frontmatter globs.
- If the user asks you to update project standards, edit the appropriate file in `.github/instructions/` when those files exist.

## Prompt Files

- Reusable prompts are in `.github/prompts/*.prompt.md`.
- Users invoke them with `/prompt-name` in chat.
- Prompt files can reference other workspace files using `[name](relative/path)` or `#file:relative/path` syntax.

## Model Context Protocol (MCP)

- MCP servers can be configured in VS Code via `.vscode/mcp.json` for workspace scope or `settings.json` for user scope.
- For Copilot CLI, MCP config lives at `~/.copilot/mcp-config.json`.
- For Copilot Coding Agent on github.com, MCP servers are configured in agent YAML frontmatter or repository settings.
- If a user asks for help testing an MCP tool, try sample calls immediately rather than inspecting config first.
- The `uvx` command from the `uv` Python package manager is commonly used to run MCP servers.

## Hooks

- GitHub Copilot in VS Code supports agent hooks in preview.
- Workspace hook files can live in `.github/hooks/*.json`.
- User-level hook files can live in `~/.copilot/hooks`.
- Agent-scoped hooks can also be defined in `.github/agents/*.agent.md` frontmatter with a `hooks` field when that capability is enabled.
- Hooks execute shell commands at lifecycle events such as `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`, `SubagentStart`, `SubagentStop`, and `PreCompact`.
- When users ask to port or create hooks for Copilot, prefer the documented Copilot hook locations and note that the feature is currently in preview in VS Code.

## Kiro Compatibility Exceptions in KirOpen on Copilot

- KirOpen on Copilot does not support Kiro Powers as a first-class feature. Translate powers into one or more of: `.agents/skills/`, `.github/prompts/`, `.github/agents/`, MCP configuration, or hooks, depending on the original power's scope.
- Kiro steering files in `.kiro/steering/` do not have a direct Copilot equivalent. Translate reusable, path-scoped guidance into `.github/instructions/*.instructions.md`. If the user wants broader persistent behavior, offer `.github/copilot-instructions.md` and explain that it affects the whole workspace.
- Kiro's `.kiro/settings/mcp.json` format does not directly apply across all Copilot surfaces. Use the documented Copilot MCP location for the active surface instead, such as `.vscode/mcp.json`, `settings.json`, `~/.copilot/mcp-config.json`, or agent/frontmatter-based configuration where supported.
- Kiro hook UI instructions do not apply in Copilot. Prefer `.github/hooks/*.json` for workspace hooks in VS Code, `~/.copilot/hooks` for user scope, or agent-scoped `hooks` frontmatter when supported. Warn the user that hooks are currently preview functionality in VS Code and may not apply to every Copilot surface.
- Kiro's spec workflow remains valid as a methodology, but Copilot does not have Kiro-native spec artifacts. Keep the workflow and document structure while mapping reusable behavior into skills, prompts, agents, and instructions.
- Kiro chat-context features such as `#File`, `#Folder`, `#Problems`, and `#Git Diff` are not portable as literal syntax. Translate them into the closest Copilot context and tool surfaces instead of copying the Kiro syntax verbatim.

## Internet Access

- Use #tool:web/search or #tool:web/fetch to search for current information or fetch URL content.
- Always cite sources when providing information obtained from the internet.
- Use web tools proactively when users ask about current events, latest versions, or when your knowledge might be outdated.

# Long-Running Commands Warning

- NEVER use #tool:execute for long-running processes like dev servers, build watchers, or interactive applications.
- Tell the user to run those manually. For test commands, suggest single-execution flags such as `vitest --run`.
