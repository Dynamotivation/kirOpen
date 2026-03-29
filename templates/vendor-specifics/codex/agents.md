# Subagent Rules

- KirOpen only spawns subagents when the user explicitly asks for delegation, sub-agents, or parallel agent work.
- For spec workflow intent (`spec mode`, `spec design`, `feature spec`, `bugfix spec`, or `generate a spec`), treat that request itself as explicit delegation consent for `spec_mode`.
- For `spec_mode` requests, use single-owner flow: once delegated, do not create or edit the same spec artifacts in the parent while the agent is running, even under a changed name.
- After delegating to `spec_mode`, call `wait_agent` for that result before continuing same-scope spec authoring locally.
- When explicit delegation is requested, prefer built-in `explorer` for read-heavy codebase discovery and `worker` for bounded implementation tasks.
- Custom agents in `.codex/agents/*.toml` are useful for narrow, repeated workflows.
