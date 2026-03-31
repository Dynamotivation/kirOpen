# Copilot Profile Notes

- This Always-on profile does not emit `.github/agents/*.agent.md`.
- Keep KirOpen behavior in `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, and the reusable skills on disk.
- For spec workflow requests in this profile, execute the requirements -> design -> tasks flow inline instead of delegating to a generated Copilot agent.

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
| `port-kiro-configuration-to-kiropen-on-copilot` | Porting Kiro-era `.kiro/` configuration into Copilot-native assets |
