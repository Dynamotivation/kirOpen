---
name: create-guidance
description: Create or update the smallest useful persistent guidance assets for the active harness and repository layout.
license: MIT
compatibility: Claude Code, Codex, Cursor, GitHub Copilot, VS Code, Windsurf, KirOpen
metadata:
  category: workflow
  complexity: intermediate
  author: KirOpen Team
  version: "1.0.0"
---

# Create Guidance

Use this when the user wants reusable project guidance, not just a one-off answer.

## Goal

Create or update the smallest useful persistent guidance surface for the active harness and repository.

## Look At

- Languages and frameworks in use
- Directory structure and team conventions
- Existing config files, linters, formatters, and CI
- Build tools and package managers
- Whether the user wants global behavior, scoped behavior, reusable workflows, or one-off prompts

## Preferred Outputs

- Reusable repo skills when the workflow should be invoked repeatedly
- Scoped instruction files when guidance should apply only to certain paths or contexts
- Custom agents when a narrow specialist persona or repeated delegated workflow is useful
- Prompt files only when the workflow is intentionally one-off
- Hook or MCP configuration only when the user explicitly wants automation or external tool integration

## Rules

- Prefer the smallest surface that solves the user's problem cleanly
- Reuse existing guidance files instead of creating duplicates
- Do not generate repo-wide default instruction files unless the user explicitly wants workspace-wide assistant behavior
- Keep tool-calling details aligned with the active harness instead of hardcoding another harness's syntax

## Output Style

- Explain what guidance surface you chose and why
- Prefer small targeted assets over one giant catch-all file
- Keep the guidance specific to the project rather than generic best-practice filler
