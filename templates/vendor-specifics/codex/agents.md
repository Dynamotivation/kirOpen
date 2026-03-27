# Subagent Rules

- KirOpen only spawns subagents when the user explicitly asks for delegation, sub-agents, or parallel agent work.
- When explicit delegation is requested, prefer built-in `explorer` for read-heavy codebase discovery and `worker` for bounded implementation tasks.
- Custom agents in `.codex/agents/*.toml` are useful for narrow, repeated workflows.
