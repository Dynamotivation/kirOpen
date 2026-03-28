---
name: port-kiro-configuration-to-kiropen-on-antigravity
description: Port Kiro workspace configuration into Antigravity-compatible rules and shared skills, including Model Context Protocol (MCP) server setup.
---

# Port Kiro Configuration To KirOpen On Antigravity

Use this skill when a repository still contains Kiro-era configuration and the user wants it migrated into Antigravity-compatible KirOpen assets.

## Scope

Inspect `.kiro/` and classify the same buckets every time:

- `.kiro/skills/`
- `.kiro/steering/`
- `.kiro/settings/mcp.json`
- other `.kiro/settings/*` files
- hook definitions or Kiro-specific automation config
- vendor-specific Kiro guidance files

## Translation Targets

Prefer these Antigravity-native outputs:

- `.agent/rules/*.md` for persistent behavior and situational context
- `.agents/skills/*/SKILL.md` for reusable repeatable behavior
- active Antigravity MCP configuration for external tools and resource connections

Do not disturb existing generated workflow outputs that already belong to KirOpen's spec workflow.

## Mapping Rules

- Convert reusable Kiro workflow guidance into Antigravity shared skills.
- Convert Kiro steering into Antigravity rule files instead of keeping one giant persistent prompt.
- Convert `.kiro/settings/mcp.json` concepts into the active Antigravity MCP surface server-by-server instead of copying Kiro JSON directly.
- Do not invent a hook file format that Antigravity docs do not document.
- Preserve intent, not file format.

## Rules And Skills

KirOpen uses Antigravity rules for persistent guidance and shared skills for reusable behavior.

- Convert Kiro directory-scoped steering such as `api.md`, `frontend.md`, or environment guidance into `.agent/rules/*.md`.
- Convert task-like or procedure-like Kiro guidance into `.agents/skills/*/SKILL.md`.
- Keep long-running reusable flows in skills instead of stuffing them into a single always-on rule.
- When a Kiro power is really a reusable prompt or checklist, port it as a skill.
- When a Kiro power is really persistent context, port it as one or more rules.

Official docs note:
- Antigravity's docs say Rules guide agent behavior.
- Current Antigravity behavior in KirOpen uses the shared `.agents/skills/*/SKILL.md` setup for reusable skills, with legacy `.agent/skills/*/SKILL.md` compatibility retained by Antigravity.

## MCP Porting

Port MCP in the same way every time:

1. Read each Kiro MCP server entry and extract the server name, transport type, startup command or URL, arguments, environment variables, auth requirements, and any tool allow/deny intent.
2. Do not invent a repo-local Antigravity MCP file schema from Kiro JSON.
3. Recreate each server in the active Antigravity MCP surface the user is actually using.
4. Preserve server intent:
   - local process server -> same command, args, env, and cwd intent where supported
   - remote server -> same URL and auth intent where supported
5. Keep secrets in environment variables or the harness's secure configuration surface instead of committing them into repo markdown.
6. If the docs or current installation do not expose a portable MCP file format, document the server mapping clearly and apply it through the actual Antigravity MCP UI or settings surface instead of fabricating a fake checked-in file.

Official docs note:
- Current Antigravity docs explicitly mention MCP servers as context sources you can reference with `@`.
- The current customization docs focus on Rules and Workflows; they do not document a checked-in workspace MCP file format comparable to Kiro's `.kiro/settings/mcp.json`.

## Hooks Porting

Antigravity currently needs special handling here:

1. Look for Kiro hooks and write down what each hook was trying to accomplish.
2. Check whether the behavior is better expressed as:
   - a persistent rule
   - a reusable skill
   - a safer approval-policy recommendation
   - an MCP-backed tool or context source
3. If the behavior cannot be expressed cleanly in Antigravity, leave it as a documented unsupported exception.
4. Do not create fake Antigravity hook files or frontmatter fields.

Official docs note:
- In the current Antigravity docs reviewed here, Rules, terminal/browser approval policies, and MCP context are documented.
- A hook system equivalent to Kiro hooks is not documented there, so hook behavior should be translated by intent or called out as unsupported.

## Process

1. Inventory the existing `.kiro/` files.
2. Analyze the codebase structure to determine where frontend, API, environment, shared library, or other directory-scoped guidance actually belongs.
3. Classify each `.kiro` item as skills, steering, MCP, hooks, settings, or unsupported Kiro-only behavior.
4. Port skills, steering, MCP, and hooks as separate decisions instead of mixing them into one output file.
5. Leave unsupported concepts as documented exceptions instead of inventing fake Antigravity behavior.
6. Keep existing KirOpen spec workflow assets intact.

## Output Style

- Be explicit about what was ported directly, what was adapted, and what has no Antigravity equivalent.
- Prefer small targeted rules and skills over one giant catch-all file.
- Include the codebase analysis that led to each rule or skill placement.
- Execute the migration when the user is asking for it, not just describe it.
