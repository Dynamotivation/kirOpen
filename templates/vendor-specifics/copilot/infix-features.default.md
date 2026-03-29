# Features

## User Question Tools

- In VS Code, use `vscode_askQuestions` to present structured questions to the user.
- In Copilot CLI, use `ask_user` to present structured questions to the user.
- Use whichever is available in the current surface. If neither is available, fall back to asking in the chat response.

## Custom Instructions

- Repository-wide instructions live in `.github/copilot-instructions.md`.
- Copilot custom agents live in `.github/agents/*.agent.md` and can be selected as primary agents.
- Path-specific instructions live in `.github/instructions/*.instructions.md` with `applyTo` frontmatter globs.
- If the user asks you to update project standards, edit the appropriate file in `.github/instructions/` when those files exist.
- When the user wants to create new project guidance or standards from scratch, read and follow the `create-guidance` skill at `.agents/skills/create-guidance/SKILL.md`.
- When the user wants structured steering documents with cross-harness support, read and follow the `create-steering-documents` skill at `.agents/skills/create-steering-documents/SKILL.md`.

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
- Kiro steering files in `.kiro/steering/` do not have a direct Copilot equivalent. Translate reusable, path-scoped guidance into `.github/instructions/*.instructions.md`. If the user wants broader persistent behavior, offer `.github/copilot-instructions.md` and explain that it affects the whole workspace. When creating new steering, read and follow the `create-steering-documents` skill at `.agents/skills/create-steering-documents/SKILL.md`.
- Kiro's `.kiro/settings/mcp.json` format does not directly apply across all Copilot surfaces. Use the documented Copilot MCP location for the active surface instead, such as `.vscode/mcp.json`, `settings.json`, `~/.copilot/mcp-config.json`, or agent/frontmatter-based configuration where supported.
- Kiro hook UI instructions do not apply in Copilot. Prefer `.github/hooks/*.json` for workspace hooks in VS Code, `~/.copilot/hooks` for user scope, or agent-scoped `hooks` frontmatter when supported. Warn the user that hooks are currently preview functionality in VS Code and may not apply to every Copilot surface.
- Kiro's spec workflow remains valid as a methodology, but Copilot does not have Kiro-native spec artifacts. Keep the workflow and document structure while mapping reusable behavior into skills, prompts, agents, and instructions.
- When the user wants the structured spec workflow, prefer delegating to the `spec-mode` agent so the heavyweight workflow steering stays out of the main context. Use the reusable skills directly only when the agent path is unavailable or the user explicitly asks for inline handling.
- When the user wants to port existing `.kiro/` configuration into Copilot-native assets, read and follow the `port-kiro-configuration-to-kiropen-on-copilot` skill at `.agents/skills/port-kiro-configuration-to-kiropen-on-copilot/SKILL.md`.
- Kiro chat-context features such as `#File`, `#Folder`, `#Problems`, and `#Git Diff` are not portable as literal syntax. Translate them into the closest Copilot context and tool surfaces instead of copying the Kiro syntax verbatim.

## Diagnostics

- In VS Code, Copilot can access the Problems panel via `#problems` or `#read/problems`. Use this as the diagnostic tool when checking for compile, lint, type, and other semantic issues after editing files.
- Prefer `#problems` over running lint or type-check commands in the terminal. It surfaces the same squiggles the developer sees in the editor without spawning a separate process.
- On GitHub.com coding agent there is no live Problems panel. Instead, replicate diagnostic checks by running the project's lint and type-check commands (e.g. `npm run lint`, `tsc --noEmit`, `mypy .`) via `#tool:execute` and inspecting the output.
- On Copilot CLI, use `#tool:execute` to run lint and type-check commands the same way.
- When implementation problems are hard to diagnose, read and follow the `troubleshooting` skill at `.agents/skills/troubleshooting/SKILL.md`.

## Internet Access

- Use #tool:web/search or #tool:web/fetch to search for current information or fetch URL content.
- Always cite sources when providing information obtained from the internet.
- Use web tools proactively when users ask about current events, latest versions, or when your knowledge might be outdated.

# Long-Running Commands Warning

- NEVER use #tool:execute for long-running processes like dev servers, build watchers, or interactive applications.
- Tell the user to run those manually. For test commands, suggest single-execution flags such as `vitest --run`.
