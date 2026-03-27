---
name: task-breakdown
description: Kiro's approach to converting technical designs into sequenced, actionable implementation tasks. Creates clear coding tasks that respect dependencies, enable incremental progress, and maintain traceability to requirements.
license: MIT
compatibility: Claude Code, Cursor, VS Code, Windsurf, Kiro
metadata:
  category: methodology
  complexity: intermediate
  author: Kiro Team
  version: "1.0.0"
---

# Task Breakdown

Phase 3 of spec-driven development. The design tells me how to build it. Tasks tell me in what order, one step at a time.

## When to Use This

- Design phase is complete and approved
- Ready to start implementation
- Need to track incremental progress
- Want to coordinate work across developers

## Task Structure

I use a two-level hierarchy:

```markdown
- [ ] 1. [Major component/epic]
- [ ] 1.1 [Specific implementation task]
  - [What to implement]
  - [Files to create/modify]
  - _Requirements: [Req-1, Req-2]_
- [ ] 1.2 [Next task]
  - [Details]
  - _Requirements: [Req-3]_
```

Each task includes:
- A clear objective (what specific code to write or modify)
- Implementation details (files, components, functions)
- Requirements reference (which requirements this satisfies)
- Implicit completion criteria (tests pass, requirement met)

## How I Sequence Tasks

### My Default Approach: Hybrid

I don't rigidly follow one strategy. I combine them based on the project:

1. Minimal foundation first (core interfaces, project structure)
2. High-risk or uncertain parts early (external integrations, complex logic)
3. Feature slices where possible (end-to-end for early validation)
4. Polish and optimization last

### When I Use Foundation-First

For new projects or major new subsystems:
```
1. Project setup and core interfaces
2. Data models and validation
3. Data access layer
4. Business logic
5. API endpoints
6. Integration wiring
```

### When I Use Feature-Slice

For MVP development or when early validation matters:
```
1. User registration (complete flow)
2. User login (complete flow)
3. Profile management (complete flow)
```

### When I Use Risk-First

For high-uncertainty work:
```
1. Most complex/uncertain component
2. External integrations
3. Core business logic
4. Everything else
```

## Task Sizing

Each task should be roughly 2-4 hours of focused work.

Too large: "Implement complete user management system"
Too small: "Add semicolon to line 42"
Right: "Create User model with validation methods and unit tests"

If I can't describe what a task produces in one sentence, it's too big. If it doesn't produce something testable, it's too small or needs to be merged with the next task.

## Dependency Management

I map dependencies explicitly. A task that depends on another task must come after it in the sequence.

```markdown
- [ ] 1.1 Create database schema and migrations
- [ ] 2.1 Create User model ← depends on 1.1
- [ ] 3.1 Create UserService ← depends on 2.1
- [ ] 4.1 Create API endpoints ← depends on 3.1
```

When I hit circular dependencies (ServiceA needs ServiceB, ServiceB needs ServiceA), I extract interfaces:
```markdown
- [ ] 1.1 Define IServiceA and IServiceB interfaces
- [ ] 1.2 Implement ServiceA using IServiceB
- [ ] 1.3 Implement ServiceB using IServiceA
- [ ] 1.4 Wire up dependency injection
```

## Requirements Traceability

Every task references the requirements it satisfies. This serves two purposes:
1. I can verify every requirement has at least one task implementing it
2. During implementation, I can check my work against the original requirement

If a task doesn't map to any requirement, either:
- A requirement is missing (go back and add it)
- The task is unnecessary (remove it)

## Quality Checklist

Before starting implementation:
- [ ] Every design component has implementation tasks
- [ ] Every requirement is referenced by at least one task
- [ ] Tasks are sequenced to respect dependencies
- [ ] Each task produces something testable
- [ ] Tasks are sized at 2-4 hours each
- [ ] No task has unresolved external blockers

## During Implementation

When I execute tasks:
- I mark a task in-progress when I start it
- I write tests alongside code, not after
- I mark a task complete when tests pass and the requirement is met
- If implementation reveals a gap in the spec, I update the spec first, then continue

I don't skip ahead. I don't "just quickly do" a later task because it seems easy. The sequence exists for a reason.

## What Comes Next

After task breakdown is complete:
1. Review the task list (does it cover everything? is the sequence right?)
2. Begin implementation following the sequence
3. Track progress by checking off tasks
4. Update tasks if implementation reveals gaps
5. Validate completed work against requirements
