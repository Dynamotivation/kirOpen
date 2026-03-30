# Subagent Rules

- KirOpen only spawns subagents when the user explicitly asks for delegation, sub-agents, or parallel agent work.
- For spec workflow intent (`spec mode`, `spec design`, `feature spec`, `bugfix spec`, or `generate a spec`), treat that request itself as explicit delegation consent for `spec_mode`.
- For `spec_mode` requests, use single-owner flow: once delegated, do not create or edit the same spec artifacts in the parent while the agent is running, even under a changed name.
- After delegating to `spec_mode`, call `wait_agent` for that result before continuing same-scope spec authoring locally.
- When explicit delegation is requested, prefer built-in `explorer` for read-heavy codebase discovery and `worker` for bounded implementation tasks.
- Custom agents in `.codex/agents/*.toml` are useful for narrow, repeated workflows.

# Available Skills

Skills live in `.agents/skills/*/SKILL.md`. Read a skill file when you need its guidance — do not keep skill content loaded between tasks.

| Skill | When to use |
|---|---|
| `spec-driven-development` | Three-phase feature development: requirements → design → tasks |
| `requirements-engineering` | Capturing what to build with EARS-format acceptance criteria |
| `design-documentation` | Technical designs bridging requirements and implementation |
| `task-breakdown` | Converting designs into sequenced implementation tasks |
| `quality-assurance` | Phase-specific validation, quality gates, and testing strategy |
| `troubleshooting` | Diagnosing spec-reality divergence, dependency blocks, and getting unstuck |
| `create-guidance` | Creating or updating persistent guidance assets for the active harness |
| `create-steering-documents` | Setting up canonical steering documents with cross-harness wrappers |
| `port-kiro-configuration-to-kiropen-on-codex` | Porting Kiro-era `.kiro/` configuration into Codex-native assets |
