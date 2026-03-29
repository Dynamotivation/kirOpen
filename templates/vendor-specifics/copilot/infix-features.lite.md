# Features

## Custom Instructions

- Repository-wide instructions live in `.github/copilot-instructions.md`.
- Copilot custom agents live in `.github/agents/*.agent.md` and can be selected as primary agents.
- In Lite mode, keep this file lean and route heavyweight workflows into custom agents instead of expanding them inline.

## Spec Workflow

- KirOpen keeps Kiro-style spec artifacts under `.kiro/specs/<feature>/requirements.md`, `design.md`, and `tasks.md`.
- When the user wants the structured spec workflow, delegate to the `spec-mode` agent so the main context stays small.
- `spec-mode` owns requirements, design, and task breakdown once delegated.

## Diagnostics

- In VS Code, prefer `#problems` or `#read/problems` for compile, lint, and type issues.
- When that surface is unavailable, fall back to `#tool:execute` for one-shot lint or type-check commands.

## Internet Access

- Use #tool:web/search or #tool:web/fetch when the task depends on current information or URL content.
- Cite sources when information comes from the internet.
