---
name: add-harness-support
description: Add or extend KirOpen support for a harness while keeping the builder, templates, README, tests, and cross-harness skills in sync. Use when KirOpen needs to add a new harness, audit all repo touchpoints for a harness change, or update shared cross-harness behavior such as steering.
license: MIT
compatibility: Claude Code, Codex, Cursor, GitHub Copilot, VS Code, Windsurf, KirOpen
metadata:
  category: workflow
  complexity: intermediate
  author: KirOpen Team
  version: "1.0.0"
---

# Add Harness Support

Use this when KirOpen is adding a new harness or when an existing cross-harness concept changes in a way that forces multiple repo surfaces to stay in sync.

## Read First

Before making changes, read:

- `development/adding-a-harness.md`
- `development/harness-touchpoints.md`
- `development/tool-reference-points.md` when the harness changes concept mapping, tools, agents, steering, hooks, or MCP behavior

Those files are the maintainer-facing source material for this workflow.

## Core Workflow

### 1. Update the builder

Start in `assemble_instructions.py`.

Audit:

- `ALL_TARGETS`
- CLI target parsing and validation
- target-specific output planners
- target-specific helper functions for generated files, prompts, skills, agents, wrapper files, config, and setup logic

If the harness is not wired here, the repo does not really support it yet.

### 2. Add the vendor template surface

Audit `templates/vendor-specifics/<harness>/`.

Common touchpoints:

- `features.md`
- `tool-rules.md`
- `agents.md`
- `parallel-hint.md`
- harness-specific prompt, skill, runtime-guide, or agent-frontmatter files

Only describe capabilities the real harness actually supports.

### 3. Audit shared cross-harness templates

A new harness often changes shared files too.

Check:

- `templates/skills/*.SKILL.md`
- `templates/steering/*`
- `templates/vendor-specifics/kiro.md`

Important current example:

- `templates/skills/create-steering-documents/SKILL.md`

If the new harness participates in the canonical `.kiro/steering` plus wrapper-file model, update that skill.

### 4. Audit live skills and development copies

When a shared behavior changes, keep these aligned:

- `.agents/skills/...`
- `templates/skills/...`
- `development/skills/...` when a maintainer copy exists

Important current example:

- `.agents/skills/create-steering-documents/SKILL.md`
- `templates/skills/create-steering-documents/SKILL.md`
- `development/skills/create-steering-documents/SKILL.md`

### 5. Update README in every affected section

Do not stop after one README edit.

Review:

- supported harnesses
- planned harnesses
- CLI usage examples
- installation into empty repositories
- installation into existing repositories
- merge-review instructions
- build examples
- top-level cross-harness behavior notes

### 6. Update maintainer docs if mappings changed

When the harness changes the translation of KirOpen concepts, update:

- `development/tool-reference-points.md`
- `development/adding-a-harness.md`
- `development/harness-touchpoints.md`

### 7. Update tests

Audit `tests/test_assemble_instructions.py`.

At minimum, add or update coverage for:

- target selection
- output planning
- representative generated files
- harness-specific regression risks

## Output Expectations

When doing this work:

- name the exact files that were changed
- call out any cross-harness skills that were audited
- say explicitly if README or tests were left for follow-up

## Rule Of Thumb

Before you stop, search these areas:

- `assemble_instructions.py`
- `templates/vendor-specifics/`
- `templates/skills/`
- `.agents/skills/`
- `development/`
- `README.md`
- `tests/`
