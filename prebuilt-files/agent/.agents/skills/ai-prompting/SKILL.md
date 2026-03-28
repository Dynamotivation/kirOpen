---
name: ai-prompting
description: How to communicate effectively with KirOpen and other AI coding assistants. Context-first prompting, phased interactions, iterative refinement, and validation techniques for better results.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, KirOpen
metadata:
  category: methodology
  complexity: beginner
  author: KirOpen Team
  version: "1.0.0"
---

# AI Prompting Strategies

This is how to get the best results out of me. Not generic "prompt engineering" but specific patterns that work well with KirOpen-style coding assistance.

## Why This Matters

I produce better output when I have:

- clear context about what you're working on
- explicit constraints such as stack, performance, or security needs
- a defined scope
- examples of what good looks like

I produce worse output when:

- context is missing and I have to guess
- everything is requested at once in a wall of text
- constraints are implicit
- there is no feedback loop

## Core Strategies

### 1. Context First, Request Second

Give me the situation before the ask.

**Weak:**

```text
Create requirements for a user profile feature.
```

**Strong:**

```text
I'm building a fitness tracking web app with React and Node.js. We need user profiles
where people manage their info and fitness goals. It must comply with GDPR for EU users
and integrate with our existing auth system.

Help me create requirements for the user profile feature using EARS format.
```

### 2. Work In Phases

Do not jump from vague idea to implementation in one prompt if you want high-quality output.

Use the three phases:

1. Requirements
2. Design
3. Tasks

Each phase should build on the previous one.

### 3. Iterate On The Draft

My first answer should be treated as a draft. Improve it by giving targeted feedback.

```text
Good start. Improve these areas:
1. Add a daily digest option
2. Cover what happens when preferences change while notifications are queued
3. Add GDPR details to unsubscribe handling
```

### 4. Show The Desired Shape

Examples help a lot. If you want EARS, decision tables, concise task lists, or design sections in a specific shape, show one example.

### 5. Make Constraints Explicit

Spell out what is fixed and what is flexible.

```text
Design a caching strategy for product catalog data.

Constraints:
- AWS with Redis and PostgreSQL
- API response under 200ms for cached data
- 10,000 products
- 1,000 concurrent users
- cache budget under $100 per month

Flexible:
- invalidation approach
- key structure
- failover strategy
```

### 6. Ask For Validation

Explicit review prompts improve quality:

```text
Review these requirements and check:
1. Are they testable?
2. Are edge cases covered?
3. Do any requirements conflict?
4. Are there missing user journey steps?
```

## Phase-Specific Patterns

### For Requirements

```text
I have this user story: [story]

Help me:
1. Expand it with EARS acceptance criteria
2. Identify edge cases and error scenarios
3. Add non-functional requirements
4. Flag ambiguity
```

### For Design

```text
Given these requirements: [summary]

Propose:
1. Architecture and component breakdown
2. Data models
3. Key interfaces
4. Error handling strategy

Our stack is [stack]. Key constraint: [constraint].
```

### For Tasks

```text
Based on this design: [summary]

Create implementation tasks that:
1. Respect dependencies
2. Are 2-4 hours each
3. Include testing
4. Reference requirements
```

## What Does Not Work Well

- asking for everything at once
- saying "make it better" without criteria
- assuming I remember old conversations
- skipping repo or product context
- accepting the first draft without challenge

## Harness-Specific Tips

### In KirOpen-like IDEs

- attach relevant files or folders to ground the request
- include diagnostics, terminal output, or diffs when asking for debugging help
- use steering documents for persistent standards
- use spec workflows for larger features

### In Codex

- point me to the repo paths that matter
- ask for a review pass before implementation if risk is high
- name whether you want direct edits, a plan, or an investigation

### In Copilot

- keep the requested output shape explicit
- use custom agents and reusable prompts when you want repeatable workflows
- keep project-wide standards in instructions only when you intentionally want default behavior changed
