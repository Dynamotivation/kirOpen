---
name: requirements-engineering
description: KirOpen's approach to capturing what needs to be built before diving into how. Uses EARS format for clear, testable requirements with user stories, acceptance criteria, and edge case coverage.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, KirOpen
metadata:
  category: methodology
  complexity: beginner
  author: KirOpen Team
  version: "1.0.0"
---

# Requirements Engineering

This is how I handle the first phase of spec-driven development. The goal: turn a vague idea into something specific enough to design and build against.

## When to Use This

- Starting any new feature or project
- Clarifying ambiguous requests
- Creating acceptance criteria for user stories
- Ensuring everyone agrees on what "done" looks like

## The EARS Format

I use EARS (Easy Approach to Requirements Syntax) because it forces precision. Every requirement follows a pattern that makes it testable.

### Core Patterns

**Event-Response** (most common):
```
WHEN [triggering event] THEN [system] SHALL [required response]
```

**Conditional:**
```
IF [precondition] THEN [system] SHALL [required response]
```

**Combined:**
```
WHEN [event] AND [condition] THEN [system] SHALL [response]
```

### Why EARS Works

- "SHALL" makes requirements mandatory and unambiguous
- The pattern forces you to specify the trigger, not just the behavior
- Every requirement written this way is inherently testable
- It eliminates weasel words like "should," "might," "ideally"

## My Process

### Step 1: Capture User Stories

Format: **As a [role], I want [feature], so that [benefit]**

I focus on three things:
- Who is the user? (not "the system" — an actual human role)
- What do they want to accomplish?
- Why does it matter? (this prevents building features nobody needs)

### Step 2: Write Acceptance Criteria

For each user story, I define specific criteria using EARS:

```markdown
**User Story:** As a returning customer, I want to save payment methods, so that checkout is faster.

**Acceptance Criteria:**
1. WHEN user adds a valid credit card THEN system SHALL securely store card details
2. WHEN user adds a card with invalid number THEN system SHALL display validation error
3. WHEN user has saved cards THEN system SHALL display them during checkout
4. WHEN user selects a saved card THEN system SHALL pre-fill the payment form
5. WHEN user deletes a saved card THEN system SHALL remove it permanently
6. IF user is not authenticated THEN system SHALL redirect to login before saving
7. WHEN user adds a card THEN system SHALL mask all but last 4 digits in display
```

### Step 3: Hunt for Edge Cases

For every requirement, I ask:
- What if the input is empty or null?
- What if we're at boundary values (max length, zero, negative)?
- What if the operation fails (network, database, external service)?
- What if the user isn't authorized?
- What if two users do this simultaneously?
- What happens on the first use (empty state)?

### Step 4: Validate

Before moving to design, I check:
- [ ] All user roles identified and addressed
- [ ] Happy path covered for each story
- [ ] Edge cases and error cases documented
- [ ] Every requirement uses EARS format consistently
- [ ] No two requirements contradict each other
- [ ] Each requirement is testable (I can write a test for it)
- [ ] No implementation details leaked in (requirements say what, not how)
- [ ] Non-functional requirements captured (performance, security, accessibility)

## Common Mistakes I Watch For

**Vague requirements:**
Bad: "System should be user-friendly"
Good: "WHEN new user completes onboarding THEN system SHALL require no more than 3 steps to reach the main dashboard"

**Implementation leaking into requirements:**
Bad: "System shall use Redis for caching"
Good: "WHEN user requests frequently accessed data THEN system SHALL return cached results within 200ms"

**Missing error cases:**
If you only document the happy path, you'll discover the sad paths during implementation when they're expensive to handle.

**Untestable requirements:**
If you can't write a test for it, it's not a requirement — it's a wish.

## Requirements Document Template

```markdown
# Requirements Document: [Feature Name]

## Overview
[Brief description of the feature and its purpose]

## User Roles
- [Role 1]: [Description]
- [Role 2]: [Description]

## Requirements

### Requirement 1: [Name]
**User Story:** As a [role], I want [feature], so that [benefit]

**Acceptance Criteria:**
1. WHEN [event] THEN system SHALL [response]
2. IF [condition] THEN system SHALL [response]

**Edge Cases:**
- [Edge case and how it's handled]

### Requirement 2: [Name]
[Continue pattern...]

## Non-Functional Requirements
- **Performance:** [Specific metrics]
- **Security:** [Security requirements]
- **Accessibility:** [Standards to meet]

## Out of Scope
- [Items explicitly excluded]

## Open Questions
- [Things that need stakeholder input]
```

## What Comes Next

Once requirements are validated:
1. Get explicit approval before proceeding
2. Move to Design Phase — create the technical architecture
3. Requirements become the foundation for acceptance testing later
