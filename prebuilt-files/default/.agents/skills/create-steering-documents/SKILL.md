---
name: create-steering-documents
description: Create project-specific steering documents that give KirOpen persistent context about project standards, conventions, and workflows. Steering docs live in `.kiro/steering/` and are included based on configurable rules.
version: 1.0.0
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

Steering documents give me persistent context about your project. Instead of repeating your standards and conventions every conversation, you write them once in `.kiro/steering/` and I pick them up automatically.

## What Steering Documents Are

They are markdown files in `.kiro/steering/` that get injected into my context before I process your requests. They contain project-specific standards, conventions, and guidelines that help me produce consistent, relevant output.

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

## File References

Steering docs can reference other files in your project:
```markdown
#[[file:openapi.yml]]
#[[file:schema.graphql]]
```

This means your API spec or database schema can influence my behavior without copy-pasting content into the steering doc.

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

### 3. Write Actionable Content

Every guideline should be specific enough to follow. Not "write good code" but "use functional components with hooks, keep components under 200 lines, define props with TypeScript interfaces."

### 4. Set Appropriate Inclusion Rules

- Standards that apply everywhere: no front-matter (always included)
- Standards for specific file types: fileMatch with appropriate patterns
- Reference material: manual inclusion

## Output Structure

```
.kiro/steering/
  project-standards.md      (always included)
  git-workflow.md            (always included)
  frontend-standards.md      (fileMatch: *.tsx|*.jsx)
  api-design.md              (manual)
  development-environment.md (fileMatch: package.json|Dockerfile)
```

## Guidelines

Do:
- Keep documents focused on one topic each
- Use specific, actionable language
- Include code examples for complex conventions
- Reference external files with #[[file:path]] syntax
- Use fileMatch for context-specific standards

Do not:
- Create overly broad documents that apply to everything
- Duplicate information across multiple documents
- Include secrets or credentials
- Create conflicting standards between documents
- Make documents so long they consume excessive context
