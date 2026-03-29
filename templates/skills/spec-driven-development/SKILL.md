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

<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WHEN_TO_USE -->

## The Three Phases

### Phase 1: Requirements

I start by figuring out what we're actually building. Not how — what.

<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_1 -->

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

<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_2 -->
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

<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_3 -->

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

<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WORKFLOW -->

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

<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_LIGHTWEIGHT -->

- Brief requirements (key user stories and acceptance criteria only)
- High-level design (architecture sketch, key decisions, no exhaustive data models)
- Flat task list (no two-level hierarchy, just sequenced steps)

Use this when you need some structure but the full process would be overkill.

## What Makes This Different From Generic Planning

- It's designed for AI collaboration. Clear, structured input produces better AI output.
- It separates thinking modes. Requirements thinking, design thinking, and implementation thinking are different cognitive tasks. Mixing them produces worse results.
- It creates traceability. Every line of code traces back through tasks → design → requirements. Nothing gets built without a reason.
- It catches problems early. A bad requirement caught in phase 1 costs minutes to fix. The same bad requirement caught in phase 3 costs hours.
