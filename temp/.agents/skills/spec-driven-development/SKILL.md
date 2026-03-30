---
name: spec-driven-development
description: KirOpen's three-phase approach to feature development — Requirements, Design, Tasks. Transforms vague ideas into implementable solutions through structured planning that reduces ambiguity and enables effective AI collaboration.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, KirOpen
metadata:
  category: methodology
  complexity: intermediate
  author: KirOpen Team
  version: "1.0.0"
---

# Spec-Driven Development

This is how I approach feature development. Not a generic methodology guide — this is the actual workflow I use when someone says "build me X."

## Intake Triage

When a user asks for help, I ALWAYS ask whether this is a feature or a bug fix. The only exception is when the user has explicitly used the word "feature" or "bug" (or "bugfix") in their request. Do not infer or deduce the answer from context, project structure, or the nature of the request. If in doubt, ask.

If a tool is available to present structured questions to the user (see the tools section of your harness configuration), use it for the feature vs bug fix triage and for the workflow mode selection. Ask one question per interaction — do not combine multiple questions into a single prompt.

The format I use:

> **Is this a new feature or a bugfix?**
>
> **Build a Feature**
> Implement new functionality or capabilities that don't exist yet
>
> **Fix a Bug**
> Fix something that's broken, crashing, or not working correctly

Only skip this question when the user literally said "feature", "bug", "bugfix", or "fix" in their message. Do not skip it because the request "sounds like" one or the other.

The answer determines the workflow:

- **Build a Feature**: Proceed to the workflow mode selection (see below).
- **Fix a Bug**: I ask for reproduction steps, expected vs actual behavior, and which part of the system is affected. If the fix is straightforward, I skip the full spec and go straight to implementation. If it's complex (touches multiple components, unclear root cause), I do a lightweight spec.

## Workflow Mode Selection

After confirming this is a feature, I ask which workflow to use:

> **What do you want to start with?**
>
> **Requirements** *(Recommended)*
> Begin by gathering and documenting requirements
>
> **Technical Design**
> Begin with the technical design, then derive requirements from that design

If the user picks **Technical Design**, I also ask which artifacts to include in the design doc:

> **Select the artifacts you want included in the Design doc:**
>
> - **High-Level Design** — System diagrams, components, and data models
> - **Low-Level Design** — Code/pseudocode, algorithms, and function signatures

Both can be selected. The default recommendation is Requirements-first with both design artifacts enabled.

### Requirements-First Workflow (Recommended)

This is the standard three-phase flow:
1. Requirements (user stories + EARS acceptance criteria)
2. Design (architecture, components, data models, interfaces, error handling)
3. Tasks (sequenced implementation plan)

Each phase completes and is validated before moving to the next.

### Technical Design-First Workflow

This reverses the first two phases:
1. Design first — I create the technical design based on the user's description, including whichever artifacts they selected (high-level, low-level, or both)
2. Requirements derived — I backfill requirements from the design, ensuring every design element has a corresponding testable requirement
3. Tasks — same as the standard flow, sequenced from the design

Use this when the user already has a clear technical vision and wants to start from architecture rather than user stories. The requirements still get written — they're just derived from the design rather than driving it.

#### Artifact Selection (Design-First Only)

When the user picks Technical Design, I ask which artifacts to include:

- **High-Level Design**: System diagrams, components, and data models. This covers architecture, component responsibilities, interfaces between components, data models with validation rules, and error handling strategy.
- **Low-Level Design**: Code/pseudocode, algorithms, and function signatures. This covers core interfaces/types as actual code, key function signatures with formal specs, algorithmic pseudocode, and example usage.
- **Both**: Comprehensive design covering all of the above.

#### Requirements Derivation Process (Design-First Only)

After the design is complete, I derive requirements by walking through each design element:

1. **Components → Behavioral requirements**: Each component responsibility becomes a WHEN/THEN requirement.
2. **Data models → Validation requirements**: Each validation rule becomes an IF/THEN requirement.
3. **Error handling → Error requirements**: Each error scenario becomes a WHEN/THEN requirement covering the failure mode and recovery.
4. **Traceability check**: Every design element must map to at least one requirement. If a design element has no corresponding requirement, either the requirement is missing or the design element is unnecessary.

#### When to Recommend Each Mode

I recommend **Requirements-First** (the default) when:
- The feature is user-facing and needs stakeholder alignment
- The scope is unclear and needs to be defined through requirements
- Multiple stakeholders need to agree on what's being built
- The "what" is more important than the "how" at this stage

I recommend **Technical Design-First** when:
- The user has a clear technical vision or architecture in mind
- The feature is driven by technical constraints (performance, infrastructure)
- There are existing patterns to follow and the approach is obvious
- The user explicitly says they want to start from the technical side

## When to Use This

Use it when:
- The feature has multiple moving parts (components, integrations, user flows)
- Getting it wrong would be expensive to fix
- Multiple people need to understand what's being built
- You want me to produce high-quality, well-structured output
- The work will be maintained long-term

Skip it when:
- It's a simple bug fix with an obvious solution
- You're prototyping something throwaway
- It's a critical hotfix that needs to ship now
- The pattern is well-established and there's nothing to figure out

## The Three Phases

### Phase 1: Requirements

I start by figuring out what we're actually building. Not how — what.

The output is a `.kiro/specs/<feature>/requirements.md` with:
- User stories expressing who wants what and why
- Acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
- Edge cases and constraints
- What's explicitly out of scope

EARS patterns I use:
```
WHEN [event] THEN [system] SHALL [response]
IF [precondition] THEN [system] SHALL [response]  
WHEN [event] AND [condition] THEN [system] SHALL [response]
```

I write requirements that are testable and specific. "System should be fast" is not a requirement. "WHEN user submits search THEN system SHALL return results within 2 seconds" is.

I don't put implementation details in requirements. Requirements describe behavior, not technology choices.

### Phase 2: Design

Once requirements are solid, I create a `.kiro/specs/<feature>/design.md` covering:

- Overview of the approach
- Architecture and component interactions
- Data models with field types and validation rules
- Component interfaces (what goes in, what comes out)
- Error handling strategy
- Testing strategy

I document key decisions with context:
```markdown
### Decision: [Title]
**Context:** [Why this decision matters]
**Options:** [What I considered]
**Decision:** [What I chose]
**Rationale:** [Why]
```

I design for current requirements, not hypothetical futures. Over-engineering is a bigger risk than under-engineering — you can always extend later.

### Phase 3: Tasks

Design gets broken into a `.kiro/specs/<feature>/tasks.md` — a sequenced implementation plan:

```markdown
- [ ] 1. [Major component/epic]
- [ ] 1.1 [Specific coding task]
  - [What to implement]
  - [Files to create/modify]
  - _Requirements: [which requirements this satisfies]_
```

Each task should be roughly 2-4 hours of focused work. If it's bigger, break it down. If it's smaller, merge it.

I sequence tasks to:
- Respect dependencies (models before services, services before API)
- Enable incremental testing (each task produces something verifiable)
- Tackle risky/uncertain parts early
- Maintain traceability back to requirements

## How I Actually Work Through This

1. I don't skip phases. Requirements before design, design before tasks. Shortcuts here create problems later.

2. I iterate within phases. First pass doesn't need to be perfect — I refine based on questions and feedback.

3. I validate at transitions. Before moving from requirements to design, I check: are all user roles covered? Are requirements testable? Any conflicts? Same at design-to-tasks.

4. I keep specs as living documents. If implementation reveals something the spec got wrong, I update the spec. The spec should always reflect reality.

5. I reference requirements from tasks. Every task traces back to a requirement. If a task doesn't map to a requirement, either the requirement is missing or the task shouldn't exist.

## Spec Files Support References

Spec files can include references to other files:
```markdown
#[[file:openapi.yml]]
#[[file:schema.graphql]]
```

This means external specs, schemas, or documentation can influence the implementation without copy-pasting content.

## Lightweight Variant

For medium-complexity work that doesn't warrant a full spec:

- Brief requirements (key user stories and acceptance criteria only)
- High-level design (architecture sketch, key decisions, no exhaustive data models)
- Flat task list (no two-level hierarchy, just sequenced steps)

Use this when you need some structure but the full process would be overkill.

## What Makes This Different From Generic Planning

- It's designed for AI collaboration. Clear, structured input produces better AI output.
- It separates thinking modes. Requirements thinking, design thinking, and implementation thinking are different cognitive tasks. Mixing them produces worse results.
- It creates traceability. Every line of code traces back through tasks → design → requirements. Nothing gets built without a reason.
- It catches problems early. A bad requirement caught in phase 1 costs minutes to fix. The same bad requirement caught in phase 3 costs hours.
