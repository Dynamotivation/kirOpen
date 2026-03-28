---
name: port-kiro-configuration-to-kiropen-on-antigravity
description: Port Kiro workspace configuration into Antigravity-compatible rules and workflows, including Model Context Protocol (MCP) server setup.
---

# Port Kiro Configuration To KirOpen On Antigravity

Use this skill when migrating from a Kiro-era repository to the **Antigravity** framework.

## Scope

Inspect `.kiro/` and translate compatible configurations:
- `.kiro/skills/` -> `.agent/workflows/`
- `.kiro/steering/` -> `.agent/rules/`
- `.kiro/settings/mcp.json` -> Antigravity's MCP configuration surface for the active installation

## Translation Targets

Prefer these Antigravity-native outputs:
- **Workspace Rules** (`.agent/rules/*.md`): For persistent behavior and situational context.
- **Workflows** (`.agent/workflows/*.md`): For reusable repeatable tasks that are invoked intentionally.
- **MCP Configuration**: For external tool and resource connections, using the active Antigravity MCP surface instead of copying Kiro JSON directly.

## Mapping Rules

### Situational Context and Steering

Antigravity uses separate rule files for context and behavior.
- Convert Kiro directory-scoped steering (e.g., `api.md`, `frontend.md`) into Antigravity Rules with corresponding **Glob** patterns (e.g., `api/**`, `src/ui/**`).
- Convert Kiro powers or specialized personas into targeted rules or workflows only when Antigravity really needs a separate reusable surface.

### Workflow Translation

- Convert `.kiro/tasks/` or procedure-based steering into **Workflows** in `.agent/workflows/`.
- Workflows should use the standard Markdown structure: Title, Description, and a numbered list of Steps.
- Use slash commands (e.g., `/deploy`) to trigger these in the Antigravity interface.

### Model Context Protocol (MCP)
(Detailed MCP section follows...)
