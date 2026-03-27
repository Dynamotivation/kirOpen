---
inclusion: manual
---

# Steering Document Creation and Usage Guide

## What Are Steering Documents?

Steering documents are contextual guidelines that influence how I approach development tasks. They contain project-specific standards, conventions, and best practices that help me provide more relevant and consistent assistance.

## How Steering Documents Work

### Inclusion Mechanisms

1. **Always included**: documents without front-matter are included in every interaction
2. **File match conditional**: documents with `inclusion: fileMatch` and `fileMatchPattern` are included when matching files are in context
3. **Manual inclusion**: documents with `inclusion: manual` are included only when explicitly referenced

### Context Integration

- steering content is injected before request handling
- multiple steering documents can be active simultaneously
- file references using `#[[file:path]]` syntax can be resolved and included

## What Goes Into Steering Documents

### Common Categories

1. Development environment standards
2. Code quality guidelines
3. Git workflow standards
4. Technology-specific standards
5. Security and performance guidance

### Content Structure

```markdown
---
inclusion: always|fileMatch|manual
fileMatchPattern: 'pattern'
---

# Clear Title

## Actionable Guidance
- concrete rules
- examples
- references to project files using #[[file:path]]
```

## How I Build Steering Documents

### Assessment Process

1. analyze the project structure and technologies
2. identify high-value standardization gaps
3. prioritize security, quality, and workflow guidance
4. choose document shapes and inclusion rules that keep context lean

### Quality Checks

1. ensure the guidance is actionable
2. avoid conflicts across steering files
3. keep documents scoped and maintainable
4. update them as the project evolves

## Best Practices

Do:

- keep each document focused on one concern
- use concrete, testable language
- include examples where ambiguity is likely
- use `fileMatch` for context-sensitive guidance
- use manual docs for deeper reference material

Do not:

- make every document always included
- duplicate the same guidance in multiple files
- store secrets
- create conflicting rules
- let steering become a dumping ground

## Suggested Structure

```text
templates/steering/
  project-standards.md
  git-workflow.md
  frontend-standards.md
  api-design.md
  development-environment.md
```

## Harness Note

Steering is a KirOpen-native concept. In other harnesses, use this guide as source material and translate it into the nearest equivalent:

- Copilot: `.github/instructions/` and reusable prompts
- Codex: repo skills, custom agents, and optional project instruction files when intentionally overriding default behavior
