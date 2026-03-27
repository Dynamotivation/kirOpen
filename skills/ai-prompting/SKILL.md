---
name: ai-prompting
description: How to communicate effectively with Kiro and other AI coding assistants. Context-first prompting, phased interactions, iterative refinement, and validation techniques for better results.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, Kiro
metadata:
  category: methodology
  complexity: beginner
  author: Kiro Team
  version: "1.0.0"
---

# AI Prompting Strategies

This is how to get the best results out of me. Not generic "prompt engineering" — specific patterns that work with how I actually process requests.

## Why This Matters

I produce better output when I have:
- Clear context about what you're working on
- Explicit constraints (tech stack, performance, security)
- A defined scope (what's in, what's out)
- Examples of what good looks like

I produce worse output when:
- Context is missing and I have to guess
- Everything is requested at once in a wall of text
- Constraints are implicit ("you should know this")
- There's no feedback loop

## Core Strategies

### 1. Context First, Request Second

I can't read your mind. Give me the situation before the ask.

**Weak:**
```
Create requirements for a user profile feature.
```

**Strong:**
```
I'm building a fitness tracking web app (React + Node.js). We need user profiles 
where people manage their info and fitness goals. Must comply with GDPR for EU users. 
Integrates with our existing auth system.

Help me create requirements for the user profile feature using EARS format.
```

The second version gives me domain, tech stack, constraints, and integration context. I'll produce something relevant instead of generic.

### 2. Work in Phases, Not All at Once

Don't ask me to go from idea to implementation plan in one message. The spec-driven workflow exists for a reason — each phase builds on the previous one.

**Phase 1:** "Help me develop requirements for [feature]. Here's the context: [context]"
→ We iterate until requirements are solid.

**Phase 2:** "Requirements are approved. Let's design the technical approach. Here's our stack: [stack]"
→ We iterate until design is solid.

**Phase 3:** "Design is approved. Break this into implementation tasks."
→ We iterate until the task list is complete.

Trying to do all three at once produces shallow results across the board.

### 3. Iterate, Don't Accept First Draft

My first response is a starting point, not a final answer. Push back. Ask questions. Refine.

```
Good start. A few things to improve:
1. The notification frequency should include a daily digest option
2. What happens if preferences change while notifications are pending?
3. The unsubscribe flow needs GDPR compliance details
```

This kind of specific feedback produces much better second drafts than "make it better."

### 4. Show Me What Good Looks Like

If you have examples of the output format you want, share them.

```
Write acceptance criteria for file upload. Use EARS format like this:

"WHEN user enters valid credentials THEN system SHALL authenticate within 2 seconds"

Not like this:
"System should handle file uploads efficiently"
```

### 5. Make Constraints Explicit

Don't assume I know your limitations. Spell them out.

```
Design a caching strategy for product catalog data.

Constraints:
- AWS with Redis and PostgreSQL
- API response < 200ms for cached data
- 10,000 products, 1,000 concurrent users
- Cache budget < $100/month
- Updates visible within 5 minutes

Flexible:
- Cache invalidation approach
- Key structure
- Failover strategy
```

### 6. Validate, Don't Just Accept

Build quality checks into your workflow:

```
Review these requirements and check:
1. Are all requirements testable?
2. Have we covered error cases?
3. Do any requirements conflict?
4. Are there gaps in the user journey?
```

I'm good at self-review when you ask me to do it explicitly. I won't always do it unprompted.

## Phase-Specific Patterns

### For Requirements

```
I have this user story: [story]

Help me:
1. Expand with EARS acceptance criteria
2. Identify edge cases and error scenarios
3. Add non-functional requirements
4. Flag anything ambiguous
```

### For Design

```
Given these requirements: [summary]

Propose the technical approach:
1. Architecture and component breakdown
2. Data models
3. Key interfaces
4. Error handling strategy

Our stack is [stack]. Key constraint: [constraint].
```

### For Tasks

```
Based on this design: [summary]

Create implementation tasks that:
1. Respect dependencies
2. Are 2-4 hours each
3. Include testing
4. Reference requirements
```

## What Doesn't Work

- **Giant prompts with everything at once.** I'll produce shallow results. Break it up.
- **"Make it good."** Good by what criteria? Be specific about what you want improved.
- **Assuming I remember previous conversations.** Each conversation starts fresh. Provide context.
- **Skipping context because "it's obvious."** It's not obvious to me. I don't have your codebase memorized unless you show it to me.
- **Never pushing back.** If my first answer isn't right, tell me why. I learn from feedback within the conversation.

## Kiro-Specific Tips

- Use `#File` and `#Folder` to pull specific files into context
- Use `#Problems` to show me current diagnostics
- Use `#Terminal` to share terminal output
- Use `#Git Diff` to show me what changed
- Drag images or documents (PDF, DOCX) directly into chat
- Use steering documents (`.kiro/steering/`) to set persistent project context
- Use specs (`.kiro/specs/`) for structured feature development
