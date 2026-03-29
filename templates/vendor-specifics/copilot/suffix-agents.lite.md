# Custom Agents

- You can hand off tasks to other custom agents using #tool:agent.
- The `kiropen` agent is suitable when the user wants KirOpen selected as the primary Copilot agent.
- The `spec-mode` agent is the preferred path for structured spec workflow sessions.
- For spec workflow intent (`spec mode`, `spec design`, `feature spec`, `bugfix spec`, or `generate a spec`), delegate to `spec-mode` rather than expanding the whole methodology inline.
- Custom agents are defined in `.github/agents/*.agent.md`.
