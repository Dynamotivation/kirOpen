# Subagent Rules

- KirOpen only spawns subagents when the user explicitly asks for delegation, sub-agents, or parallel agent work.
- For spec workflow intent (`spec mode`, `spec design`, `feature spec`, `bugfix spec`, or `generate a spec`), treat that request itself as explicit delegation consent for `spec_mode`.
- When explicit delegation is requested, prefer built-in `explorer` for read-heavy codebase discovery and `worker` for bounded implementation tasks.
- Custom agents in `.codex/agents/*.toml` are useful for narrow, repeated workflows.
