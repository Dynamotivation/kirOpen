---
name: create-steering-documents
description: Create canonical steering documents in `.kiro/steering/` and create staged companion wrapper files for supported non-Kiro harnesses such as Codex and GitHub Copilot. Use when KirOpen needs to set up project standards, conditional steering, or persistent guidance while keeping `.kiro/steering/` as the source of truth.
version: 1.1.0
license: MIT
compatibility:
  - Claude Code
  - Cursor
  - VS Code Copilot
  - Windsurf
  - KirOpen
metadata:
  category: project-setup
  complexity: intermediate
  author: KirOpen Team
  triggers:
    - create steering documents
    - setup project standards
    - initialize KirOpen steering
    - project guidelines
---

# Create Steering Documents

Create canonical steering documents in `.kiro/steering/` first. Then create staged wrapper files for every supported non-Kiro harness so those harnesses can be pointed back to the canonical steering files instead of carrying their own divergent copies.

## What Steering Documents Are

Treat `.kiro/steering/*.md` as the source of truth. These files contain the real project-specific standards, conventions, and workflows that KirOpen should follow.

When you create harness wrapper files for Codex or Copilot, keep them thin. Their job is to tell the target harness to read the matching `.kiro/steering/<topic>.md` file, not to replace it.

## How Inclusion Works

Three modes, controlled by front-matter:

**Always included** (no front-matter needed):
```markdown
# Project Standards
Your standards here...
```

**Conditionally included** when specific files are in context:
```yaml
---
inclusion: fileMatch
fileMatchPattern: '*.tsx|*.jsx'
---
# Frontend Standards
Your frontend rules here...
```

**Manually included** when you reference them with `#` in chat:
```yaml
---
inclusion: manual
---
# API Design Guidelines
Your API rules here...
```

Inclusion is rule-based. There is no relevance ranking or recency prioritization. If the rule matches, the full document is included.

## Cross-Harness Output Model

Always use this two-layer model:

1. Create the canonical steering document in `.kiro/steering/`
2. Create staged companion wrapper files for each supported non-Kiro harness

Today that means:
- Codex wrapper files under `.codex/copy-me-to-...`
- GitHub Copilot wrapper files under `.github/copy-me-to-...`

Do not auto-place wrapper files into guessed target folders. Stage them in copy-me locations and tell the user where they are.

## File References

Steering docs can reference other files in your project:
```markdown
#[[file:openapi.yml]]
#[[file:schema.graphql]]
```

This means your API spec or database schema can influence my behavior without copy-pasting content into the steering doc.

Wrapper files can also point back to the canonical steering file:

```markdown
Read `.kiro/steering/frontend-standards.md` and follow it as the source of truth for this directory.
```

## What to Put in Steering Documents

### Always-included docs (use sparingly)
- Project-wide coding standards
- Git workflow and commit conventions
- Security practices
- Testing requirements

These apply to every interaction, so keep them focused. Do not dump everything here.

### File-match docs (most useful)
- Frontend standards (triggered by .tsx, .jsx, .vue files)
- API design guidelines (triggered by route/controller files)
- Database conventions (triggered by migration/schema files)
- Environment setup (triggered by package.json, Dockerfile)

These only appear when relevant, keeping context lean.

### Manual docs (for specialized topics)
- API design deep-dives
- Architecture decision records
- Deployment procedures
- Domain-specific business rules

These are available when you need them but do not clutter every conversation.

## My Process for Creating Them

### 1. Analyze the Project

I look at:
- What languages and frameworks are used
- What the directory structure looks like
- What existing conventions are in place
- What config files exist (linters, formatters, CI)

### 2. Determine Which Documents to Create

**Frontend projects:** project-standards, git-workflow, frontend-standards, dev-environment
**Backend/API projects:** project-standards, git-workflow, api-design, dev-environment
**Full-stack:** All of the above
**Libraries:** project-standards, git-workflow, documentation-standards

### 3. Create Canonical `.kiro/steering` Files

Write the real guidance into `.kiro/steering/*.md`. Every guideline should be specific enough to follow. Not "write good code" but "use functional components with hooks, keep components under 200 lines, define props with TypeScript interfaces."

### 4. Set Appropriate Inclusion Rules

- Standards that apply everywhere: no front-matter (always included)
- Standards for specific file types: fileMatch with appropriate patterns
- Reference material: manual inclusion

### 5. Create Companion Wrapper Files For Every Supported Non-Kiro Harness

For every canonical steering file you create, also create a staged wrapper for each supported non-Kiro harness.

Current harness wrappers:
- Codex: staged `AGENTS.override.md` files
- GitHub Copilot: staged `.instructions.md` files

Keep wrapper files short and referential. They should tell the harness to read the matching `.kiro/steering/<topic>.md` file.

## Output Structure

```
.kiro/steering/
  project-standards.md      (always included)
  git-workflow.md            (always included)
  frontend-standards.md      (fileMatch: *.tsx|*.jsx)
  api-design.md              (manual)
  development-environment.md (fileMatch: package.json|Dockerfile)

.codex/
  copy-me-to-your-frontend-directories/
    AGENTS.override.md
  copy-me-to-your-api-directories/
    AGENTS.override.md
  copy-me-to-your-environment-directories/
    AGENTS.override.md

.github/
  copy-me-to-your-instructions-directory/
    frontend-standards.instructions.md
    api-design.instructions.md
    development-environment.instructions.md
```

## Wrapper File Formats

### Codex Wrapper Files

Use staged placeholder paths under `.codex/copy-me-to-your-...-directories/`.

Example:

```markdown
<!-- Move this file into the directory whose files should receive this guidance. -->
<!-- Canonical steering source: .kiro/steering/frontend-standards.md -->

Read `.kiro/steering/frontend-standards.md` and follow it as the source of truth for frontend guidance in this directory.
```

Do not paste the full steering document body into the Codex wrapper unless the user explicitly asks for that duplication.

### GitHub Copilot Wrapper Files

Use staged placeholder paths under `.github/copy-me-to-your-instructions-directory/`.

Example:

```markdown
---
name: 'Frontend Standards Wrapper'
description: 'Scoped wrapper that points Copilot to the canonical KirOpen steering file'
applyTo: "**/*.tsx,**/*.jsx,**/*.vue,**/*.svelte"
---

Read `.kiro/steering/frontend-standards.md` and apply it as the source of truth for files matched by this instruction.
```

Keep Copilot frontmatter valid, but keep the body minimal and referential.

## Final Response Requirements

When you finish creating these files:
- List the canonical `.kiro/steering/*.md` files you created
- List the staged wrapper files you created under `.codex` and `.github`
- Explicitly remind the user that the wrapper files are in copy-me locations and still need to be moved into the directories where they want that scoped guidance to apply

## Guidelines

Do:
- Keep documents focused on one topic each
- Use specific, actionable language
- Include code examples for complex conventions
- Reference external files with #[[file:path]] syntax
- Use fileMatch for context-specific standards
- Keep `.kiro/steering` as the only source of truth
- Create wrapper files for all supported non-Kiro harnesses, not just one
- Keep wrapper files short and point them back to the matching `.kiro/steering` file
- Stage wrapper files under `.codex` and `.github` copy-me paths instead of guessing final placement

Do not:
- Create overly broad documents that apply to everything
- Duplicate information across multiple documents
- Include secrets or credentials
- Create conflicting standards between documents
- Make documents so long they consume excessive context
- Auto-place wrapper files into guessed project folders
- Treat Codex or Copilot wrapper files as the canonical version of the guidance
