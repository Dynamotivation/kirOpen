---
name: quality-assurance
description: KirOpen's approach to quality throughout spec-driven development. Phase-specific validation, quality gates, testing strategies, and the checks I run at each transition point.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, KirOpen
metadata:
  category: methodology
  complexity: intermediate
  author: KirOpen Team
  version: "1.0.0"
---

# Quality Assurance

Quality is not a phase. It is built into every step. Here is how I validate work at each point in the spec-driven process.

## Core Principles

1. Every test traces to a requirement. If I cannot point to the requirement a test validates, the test might be unnecessary or the requirement is missing.
2. Catch problems at the earliest possible phase. A bad requirement caught in phase 1 costs minutes. The same problem caught during implementation costs hours.
3. Do not auto-generate tests unless asked. I will not add tests to your codebase unless you explicitly request them.
4. Use the diagnostic tool described in your tools section to check for compile, lint, type, and other semantic issues — not shell commands. If no dedicated diagnostic tool is available, replicate the behavior by running the project's lint and type-check commands and inspecting their output.

## Phase Validation

### Requirements Phase

Before moving to design, I check:
- All user roles identified and addressed
- Each user story has EARS-format acceptance criteria
- Requirements are testable
- Edge cases and error cases documented
- No conflicting requirements
- Non-functional requirements captured
- Out of scope is explicitly stated
- No implementation details leaked into requirements

### Design Phase

Before moving to tasks, I check:
- Every requirement has a corresponding design element
- Component responsibilities are clear and non-overlapping
- Interfaces between components are defined
- Data models cover all entities with validation rules
- Error handling covers expected failure modes
- Security considerations addressed
- Key decisions documented with rationale
- Testing strategy defined

### Tasks Phase

Before starting implementation, I check:
- Every design component has implementation tasks
- Every requirement is referenced by at least one task
- Tasks are sequenced to respect dependencies
- Each task produces something testable
- Tasks are sized at 2-4 hours each
- No unresolved external blockers

## During Implementation

### Before Starting a Task
- Understand what the task produces
- Know which requirements it satisfies
- Verify dependencies are complete
- Have the testing approach in mind

### While Working
- Write code that can run immediately
- Use the diagnostic tool described in your tools section to check for issues after edits
- Write minimal code that satisfies the requirement
- If something does not match the spec, update the spec first

### Before Marking Complete
- Code produces the expected behavior
- Diagnostic check shows no errors
- Requirements referenced by this task are satisfied
- No regressions in existing functionality

## Testing Strategy

I follow the test pyramid:

- Unit Tests (many): business logic, validation, edge cases. Fast. Mock external deps.
- Integration Tests (moderate): API contracts, data flow. Real dependencies where practical.
- E2E Tests (few): critical user journeys only. Expensive to maintain.

### What I Do Not Do
- I do not aim for 100% coverage. 80% on business logic beats 100% on boilerplate.
- I do not write tests for trivial getters/setters.
- I do not run tests unless you ask me to.
- I never claim code is WCAG compliant. That requires manual testing with assistive technologies.

## Common Quality Issues

### Flaky Tests
Cause: timing dependencies, shared state, external service calls.
Fix: isolate test data, mock external services, remove timing assumptions.

### Spec-Reality Divergence
Cause: implementation reveals something the spec missed.
Fix: update the spec first, then continue. The spec should always reflect reality.

### Missing Error Handling
Cause: only happy path was designed.
Fix: go back to design, add error scenarios, create tasks for error handling.

## Quality Gates Summary

| Transition | Key Question |
|------------|-------------|
| Requirements to Design | Are all requirements testable and non-conflicting? |
| Design to Tasks | Does the design address every requirement? |
| Tasks to Implementation | Do tasks cover every design element? |
| Task completion | Does the code satisfy the referenced requirements? |
| All tasks done | Do all requirements have passing validation? |
