---
name: troubleshooting
description: How KirOpen diagnoses and resolves common issues during spec-driven development and implementation. Covers spec-reality divergence, dependency blocks, unclear requirements, and getting unstuck.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, KirOpen
metadata:
  category: methodology
  complexity: intermediate
  author: KirOpen Team
  version: "1.0.0"
---

# Troubleshooting

Things go wrong during development. Here is how I handle the common problems that come up during spec-driven work.

## Issue 1: Spec and Reality Diverge

This is the most common problem. You start implementing and discover the design assumed something that is not true.

### What I Do

1. Stop implementing. Do not hack around it.
2. Document exactly what is different from what the spec assumed.
3. Assess the impact: is this a minor detail or a fundamental problem?

**Minor deviation** (API returns slightly different format, field name differs):
- Update the design doc with the actual approach
- Adjust affected tasks
- Note why the change was needed
- Continue implementation

**Major deviation** (core assumption is wrong, technology cannot do what we planned):
- Go back to design phase
- Redesign with the new understanding
- Re-validate against requirements
- Create new task breakdown

**Fundamental issue** (requirements cannot be met as stated):
- Document why the requirements are not achievable
- Propose alternatives
- Get user approval before proceeding
- Update the entire spec chain

### Prevention
- Validate assumptions with actual code exploration during design
- Prototype risky integrations before finalizing the spec
- Include technical spike tasks for uncertain areas

## Issue 2: Tasks Are Blocked by Dependencies

A task cannot be completed because it needs something that does not exist yet.

### What I Do

**Reorder:** If the dependency was missed in planning, complete the prerequisite first, then return to the blocked task.

**Split:** If the task is too large, break it into parts. Complete the unblocked parts now, queue the rest.

**Stub:** If the dependency is complex, create a minimal stub/mock. Implement against the stub. Replace it when the real dependency is ready.

**Interface-first:** Define the contract between components. Implement against the interface. Integrate when both sides are ready.

### Prevention
- Map dependencies explicitly during task planning
- Order tasks to minimize blocking
- Identify parallelizable work upfront

## Issue 3: Requirements Are Unclear During Implementation

You hit a point where the requirement could mean two different things, or an edge case was never addressed.

### What I Do

1. Identify exactly what is ambiguous
2. List the possible interpretations
3. Pick the one most consistent with existing requirements and user needs
4. Propose it to the user with my rationale
5. Update the requirements with the clarification
6. Continue implementation

I do not guess silently. If something is ambiguous, I surface it.

## Issue 4: Technical Debt Creates Friction

The existing code makes the new feature harder to implement than the spec anticipated.

### What I Do

**If refactoring is bounded and low-risk:** Create separate refactoring tasks before the feature tasks. Complete them first.

**If refactoring is extensive:** Implement the feature with reasonable workarounds. Document the technical debt created. Plan cleanup separately.

**If refactoring can be incremental:** Refactor only what I touch. Leave code better than I found it. Do not go on a refactoring spree.

### Prevention
- Assess existing code quality during design phase
- Include refactoring tasks in the plan when needed
- Set realistic timelines that account for debt

## Issue 5: Scope Creep During Implementation

The classic "while I am here, I should also..." problem.

### How I Recognize It
- Working on something not in the task list
- Adding features nobody asked for
- Refactoring beyond what the task requires
- Tasks taking much longer than estimated

### What I Do

**Is it required for the current requirement?** Add it to the current work, update the spec.

**Is it nice to have?** Document it as a future enhancement. Finish the current spec first.

**Is it out of scope?** Note it explicitly. Create a separate spec later if valuable.

I do not gold-plate. The goal is to satisfy the requirements, not to build the perfect system.

## Issue 6: Performance Problems

Implementation works but does not meet performance requirements.

### What I Do

1. Measure first. Profile the code. Identify the actual bottleneck.
2. Target the biggest bottleneck. Do not optimize everything.
3. Make one change at a time. Measure after each change.
4. Verify the requirement is met. Stop optimizing once it is.

Common fixes:
- Database: add indexes, optimize queries, implement caching
- Algorithm: better data structures, reduce complexity
- Network: batch requests, reduce payload size, compress

### Prevention
- Include performance requirements in the spec with specific numbers
- Design with performance in mind (caching strategy, query patterns)
- Profile early, not just at the end

## Getting Unstuck

When truly blocked:

1. Re-read the spec. The answer might already be there.
2. Simplify. Solve a simpler version of the problem first.
3. Go back a phase. Maybe the design needs work, not the code.
4. Ask for help. Explain the problem clearly and what you have tried.
5. Take a break. Solutions often come when you step away.

## When to Update the Spec

Always update when:
- Design assumptions were wrong
- Requirements need clarification
- Tasks need reordering
- New edge cases are discovered
- Technical approach changes

Document what changed, why, and the impact. The spec should always reflect the current understanding, not the original plan.
