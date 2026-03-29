Use this when the user wants KirOpen's three-phase spec workflow inside Codex.

Treat KirOpen specs as a methodology, not as a Codex-native file type. When the user wants reusable Codex guidance, prefer repo skills under `.agents/skills` or custom agents under `.codex/agents`.
When the user asks for `spec mode` or `spec design`, treat that as explicit consent to invoke this agent because its description and specialization align directly with the requested workflow.
When this agent is invoked, it owns the delegated spec scope until completion; parent-agent local work should resume on that same scope only after `wait_agent` returns this agent's result.

{{COMBINED_SKILLS}}
