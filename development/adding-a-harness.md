# Adding A New Harness

This is a maintainer-facing checklist for expanding KirOpen to a new harness without leaving the repo half-updated.

## Goal

When a new harness is added, keep three things in sync:

1. The builder can emit the harness correctly
2. The templates and cross-harness concepts describe the harness correctly
3. The repo docs explain the harness correctly

If only one of those moves, drift shows up fast.

## Recommended Order

### 1. Wire the builder first

Start in [assemble_instructions.py](/d:/source/repos/kirOpen/assemble_instructions.py).

At minimum, review:

- `ALL_TARGETS`
- CLI help text and target validation
- target-specific output planners such as `plan_codex_outputs()` and `plan_copilot_outputs()`
- any target-specific helper functions that define generated files, wrapper files, agents, prompts, config, or trust/setup behavior

The builder is the source of truth for what gets emitted. If the harness is not represented here, the rest of the repo is just documentation.

### 2. Add the vendor template surface

Create or update `templates/vendor-specifics/<harness>/`.

Typical template touchpoints:

- `features.md`
- `tool-rules.md`
- `agents.md`
- `parallel-hint.md`
- harness-specific agent frontmatter or templates if that harness supports agents
- harness-specific prompts or skills when the harness needs dedicated migration or setup help
- runtime guide files when the harness has quirks worth documenting

Keep these templates about the real harness surface. Do not copy Codex or Copilot behavior blindly.

### 3. Audit shared templates

A new harness is not only a new vendor folder. If a shared KirOpen concept needs a new cross-harness explanation, update the shared templates too.

Common shared touchpoints:

- `templates/skills/*.SKILL.md`
- `templates/steering/*`
- `templates/vendor-specifics/kiro.md`

The main example right now is [templates/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/templates/skills/create-steering-documents/SKILL.md), because steering now creates canonical `.kiro/steering` files plus harness wrapper files. If a new harness participates in that model, this shared skill needs to know about it.

### 4. Audit live repo skills and development copies

When a shared behavior changes, check both the shipped skill and any maintainer copy in `development/`.

Current example:

- [.agents/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/.agents/skills/create-steering-documents/SKILL.md)
- [templates/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/templates/skills/create-steering-documents/SKILL.md)
- [development/skills/create-steering-documents/SKILL.md](/d:/source/repos/kirOpen/development/skills/create-steering-documents/SKILL.md)

If only one of these is updated, maintainers lose track of the intended cross-harness behavior.

Also review any harness-specific migration assets. Right now Codex and Copilot already have vendor-specific porting helpers:

- [templates/vendor-specifics/codex/skills/port-kiro-configuration-to-kiropen-on-codex.SKILL.md](/d:/source/repos/kirOpen/templates/vendor-specifics/codex/skills/port-kiro-configuration-to-kiropen-on-codex.SKILL.md)
- [templates/vendor-specifics/copilot/port-kiro-configuration-to-kiropen-on-copilot.prompt.md](/d:/source/repos/kirOpen/templates/vendor-specifics/copilot/port-kiro-configuration-to-kiropen-on-copilot.prompt.md)

If the new harness needs equivalent onboarding or migration help, add it here too.

### 5. Update README in every harness-facing section

Do not treat README as one edit. It usually needs changes in several places.

Review at least:

- supported and planned harness lists
- CLI usage examples
- installation into empty repositories
- installation into existing repositories
- merge-review instructions for generated output
- build examples near the bottom
- any top-level explanation that names current harnesses or cross-harness behavior

README drift is the easiest way to make the builder and docs disagree.

### 6. Update maintainer docs when mappings change

If the new harness changes how KirOpen concepts map to runtime features, review:

- [development/tool-reference-points.md](/d:/source/repos/kirOpen/development/tool-reference-points.md)
- any harness-maintenance documents in `development/`

This is where maintainers should be able to see how the harness fits into the bigger cross-harness model.

### 7. Add or update tests

Review [tests/test_assemble_instructions.py](/d:/source/repos/kirOpen/tests/test_assemble_instructions.py).

At minimum, add coverage for:

- target selection and validation
- output planning for the new harness
- representative generated files
- any harness-specific branching or regression-prone behavior

## Common Drift Traps

- Adding a new folder under `templates/vendor-specifics/` but forgetting `assemble_instructions.py`
- Updating README examples in one section but not the installation and merge sections
- Updating only the template copy of a shared skill and not the live `.agents/skills/` copy
- Forgetting the `development/skills/` copy for cross-harness skills such as `create-steering-documents`
- Treating steering, hooks, MCP, or agents as portable formats instead of harness translations

## Minimum Review Before Calling It Done

Before considering a new harness integrated, confirm:

- the builder can plan outputs for it
- the vendor template folder exists and is actually used
- README mentions it in every relevant section
- shared cross-harness skills have been audited
- tests cover the new target
