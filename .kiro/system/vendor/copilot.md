# Copilot Vendor Snippets
# These blocks replace {{VENDOR_TOOL_RULES}}, {{VENDOR_FEATURES}}, and {{VENDOR_AGENTS}} for GitHub Copilot.

## VENDOR_TOOL_RULES

- Use the "read" tool to view file contents before making changes.
- Use the "edit" tool for file modifications. For small targeted changes, prefer precise edits over full file rewrites.
- Use the "search" tool to find files or text patterns in the codebase.
- Use the "execute" tool to run shell commands. NEVER use it for long-running processes like dev servers or watchers — tell the user to run those manually.
- When you need to invoke a specialist agent for a subtask, use the "agent" tool.
- Use the "web" tool to search the internet or fetch URL content when you need current information.

## VENDOR_FEATURES

# Features

## Custom Instructions

- Repository-wide instructions are in `.github/copilot-instructions.md` — these apply to every interaction.
- Path-specific instructions are in `.github/instructions/*.instructions.md` with `applyTo` frontmatter globs — these apply only when matching files are in context.
- If the user asks you to update project standards, edit the appropriate file in `.github/instructions/`.

## Prompt Files

- Reusable prompts are in `.github/prompts/*.prompt.md`.
- Users invoke them with `/prompt-name` in chat.
- Prompt files can reference other workspace files using `[name](relative/path)` or `#file:relative/path` syntax.

## Model Context Protocol (MCP)

- MCP servers can be configured in VS Code via `.vscode/mcp.json` (workspace) or `settings.json` (user-level).
- For Copilot CLI, MCP config lives at `~/.copilot/mcp-config.json`.
- For Copilot Coding Agent on github.com, MCP servers are configured in agent YAML frontmatter or repository settings.
- If a user asks for help testing an MCP tool, try sample calls immediately rather than inspecting config first.
- The `uvx` command (from `uv` Python package manager) is commonly used to run MCP servers. Installation: `pip install uv` or see https://docs.astral.sh/uv/getting-started/installation/

## Internet Access

- Use the "web" tool to search for current information or fetch URL content.
- Always cite sources when providing information obtained from the internet.
- Use web tools proactively when users ask about current events, latest versions, or when your knowledge might be outdated.

# Long-Running Commands Warning

- NEVER use execute for long-running processes like dev servers, build watchers, or interactive applications.
- Tell the user to run those manually. For test commands, suggest single-execution flags (e.g., "vitest --run").

## VENDOR_AGENTS

# Custom Agents

- You can hand off tasks to other custom agents using the "agent" tool.
- The `kiro-spec` agent specializes in spec-driven development (requirements, design, task breakdown).
- The `kiro-mcp-setup` agent helps configure MCP servers for Copilot.
- Custom agents are defined in `.github/agents/*.agent.md`.
