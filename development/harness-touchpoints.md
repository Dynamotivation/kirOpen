# Harness Touchpoints

This file is the quick map of what usually needs touching when KirOpen grows to a new harness or when an existing cross-harness concept changes.

## Core Builder

| Area | Files | Why it matters |
|------|-------|----------------|
| Target registration | [assemble_instructions.py](/d:/source/repos/kirOpen/assemble_instructions.py) | Add the new target to `ALL_TARGETS`, CLI validation, and help text |
| Output planning | [assemble_instructions.py](/d:/source/repos/kirOpen/assemble_instructions.py) | Add a planner like the existing Codex and Copilot planners |
| Harness helpers | [assemble_instructions.py](/d:/source/repos/kirOpen/assemble_instructions.py) | Define harness-specific generated files, config, prompts, agents, wrapper files, and special-case logic |

## Vendor Templates

| Area | Files | Why it matters |
|------|-------|----------------|
| Harness folder | `templates/vendor-specifics/<harness>/` | Main template surface for the harness |
| Concept mapping | `templates/vendor-specifics/<harness>/infix-features.md` | Explains how KirOpen concepts map into that harness |
| Tool rules | `templates/vendor-specifics/<harness>/infix-rules-tools.md` | Keeps tool behavior aligned with the real harness |
| Agent support | `templates/vendor-specifics/<harness>/suffix-agents.md` and any agent-frontmatter templates | Needed when the harness supports custom or reusable agents |
| Runtime quirks | `templates/vendor-specifics/<harness>/runtime-guides/*` when used | Captures harness-specific operational guidance |
| Vendor migration helpers | vendor-specific skills or prompts under `templates/vendor-specifics/<harness>/` | Helps port Kiro-era concepts into the harness cleanly |

## Shared Templates And Cross-Harness Concepts

| Area | Files | Why it matters |
|------|-------|----------------|
| Shared skills | `templates/skills/*.SKILL.md` | Shared KirOpen workflows often need to know about every supported harness |
| Steering templates | `templates/steering/*` | Steering output patterns often drive wrapper generation or path rules |
| Kiro source concepts | [templates/vendor-specifics/kiro.md](/d:/source/repos/kirOpen/templates/vendor-specifics/kiro.md) | Preserves the source-side meaning before harness translation |

## Live Skills And Development Copies

| Area | Files | Why it matters |
|------|-------|----------------|
| Shipped repo skill | [.agents/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/.agents/skills/create-steering-documents/SKILL.md) | Cross-harness steering behavior lives here for real runtime use |
| Template copy | [templates/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/templates/skills/create-steering-documents/SKILL.md) | Assembly-side copy must stay aligned with the shipped skill |
| Development copy | [development/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/development/skills/create-steering-documents/SKILL.md) | Easy-to-miss maintainer copy that can drift |

The steering skill is the clearest current example of a cross-harness concept that needs explicit auditing when a new harness is added.

If the new harness also needs migration help, look for or add analogous files to:

- [templates/vendor-specifics/codex/skills/port-kiro-configuration-to-kiropen-on-codex.SKILL.md](/d:/source/repos/kirOpen/templates/vendor-specifics/codex/skills/port-kiro-configuration-to-kiropen-on-codex.SKILL.md)
- [templates/vendor-specifics/copilot/skills/port-kiro-configuration-to-kiropen-on-copilot.SKILL.md](/d:/source/repos/kirOpen/templates/vendor-specifics/copilot/skills/port-kiro-configuration-to-kiropen-on-copilot.SKILL.md)

## README Surfaces

These README sections usually need updates together:

- [README.md](/d:/source/repos/kirOpen/README.md): `Supported Harnesses`
- [README.md](/d:/source/repos/kirOpen/README.md): `Planned Harnesses`
- [README.md](/d:/source/repos/kirOpen/README.md): CLI usage examples near the main entrypoint
- [README.md](/d:/source/repos/kirOpen/README.md): installation into empty repositories
- [README.md](/d:/source/repos/kirOpen/README.md): installation into existing repositories
- [README.md](/d:/source/repos/kirOpen/README.md): merge-review instructions for generated output
- [README.md](/d:/source/repos/kirOpen/README.md): build examples at the end
- [README.md](/d:/source/repos/kirOpen/README.md): any top-level cross-harness behavior notes

## Tests

| Area | Files | Why it matters |
|------|-------|----------------|
| Assembly coverage | [tests/test_assemble_instructions.py](/d:/source/repos/kirOpen/tests/test_assemble_instructions.py) | Main regression surface for target lists, planning, and generated output |

## Maintainer Reference Docs

| Area | Files | Why it matters |
|------|-------|----------------|
| Tool and capability translation | [development/tool-reference-points.md](/d:/source/repos/kirOpen/development/tool-reference-points.md) | Helps maintain consistent cross-harness concept mapping |
| Harness expansion workflow | [development/adding-a-harness.md](/d:/source/repos/kirOpen/development/adding-a-harness.md) | High-level process for future harness additions |
| Reusable maintainer workflow | [.agents/skills/add-harness-support/SKILL.md](/d:/source/repos/kirOpen/.agents/skills/add-harness-support/SKILL.md) | Reusable repo skill that points back to the development docs while doing the work |

## Practical Rule

When a change introduces a new harness or changes a cross-harness behavior, search these folders before you stop:

- `templates/vendor-specifics/`
- `templates/skills/`
- `.agents/skills/`
- `development/`
- `README.md`
- `tests/`
