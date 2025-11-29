---
name: SpecPulse: Task Breakdown
description: Break down plans into actionable tasks without SpecPulse CLI
category: SpecPulse
tags: [specpulse, task, breakdown]
---

# SpecPulse Task Management

Break down implementation plans into actionable tasks without requiring SpecPulse CLI installation.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to task creation and updates
- Only edit files in tasks/ and memory/ directories
- Favor straightforward, minimal implementations first

**Steps**
Track these steps as TODOs and complete them one by one.
1. Check .specpulse/memory/context.md for active feature
2. Locate current implementation plan in .specpulse/plans/[feature]/
3. Read and analyze plan content and phases
4. Extract work items and deliverables from plan
5. Break down deliverables into individual tasks
6. Define task dependencies and sequence
7. Estimate task complexity and effort
8. Generate comprehensive task breakdown
9. Create task file: .specpulse/tasks/[feature]/tasks-[id].md
10. Update feature context with task breakdown
11. Provide task summary and execution guidance

**Reference**
- Use Universal ID System for unique task numbering
- Check implementation plans for work item extraction
- Refer to memory/context.md for feature context
- Follow task template for consistency and tracking

**Usage**
Arguments should be provided as: `[--template <template-name>] [--priority <priority-level>]`

**Task Template Structure:**
```markdown
# Task Breakdown: [Feature Name]

## Overview
### Total Tasks: [count]
### Estimated Effort: [time]
### Priority Level: [high/medium/low]

## Task Categories
### Backend Development
### Frontend Development
### Database Setup
### Integration Development
### Testing and QA
### Documentation

## Task List

### Phase 1: Foundation Tasks

#### T001: Environment Setup
**Priority:** High
**Estimated Time:** 2-4 hours
**Dependencies:** None
**Status:** Pending

**Description:**
- Set up development environment
- Install required dependencies
- Configure development tools

**Acceptance Criteria:**
- Development environment is fully configured
- All dependencies are installed and tested
- Team can start development work

**Subtasks:**
- [ ] Install development dependencies
- [ ] Configure development database
- [ ] Set up version control
- [ ] Verify environment setup

---

#### T002: Database Design Implementation
**Priority:** High
**Estimated Time:** 8-12 hours
**Dependencies:** T001
**Status:** Pending

**Description:**
- Implement database schema
- Create database migrations
- Set up seed data

**Acceptance Criteria:**
- Database schema matches specification
- All migrations are tested
- Seed data is properly populated

**Subtasks:**
- [ ] Create database schema
- [ ] Write database migrations
- [ ] Create seed data scripts
- [ ] Test database setup

## Task Dependencies
### Critical Path
1. T001 → T002 → T005 → T008 → T012
2. T001 → T003 → T006 → T009 → T013

### Parallel Work Streams
- Backend: T002, T005, T008, T012
- Frontend: T004, T007, T010, T014
- Testing: T003, T006, T009, T011

## Progress Tracking
### Overall Progress: 0%
### Completed Tasks: 0/[total]
### In Progress: 0
### Blocked: 0

## Next Steps
1. Start with T001: Environment Setup
2. Begin parallel work on T002 and T004
3. Schedule regular progress reviews
```

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Automatic task extraction from implementation plans
- Dependency management and critical path analysis
- Progress tracking and milestone management

**Advanced Features:**
- **Dependency Analysis**: Automatic task dependency detection
- **Critical Path**: Identify longest task sequence
- **Parallel Streams**: Enable concurrent development
- **Progress Tracking**: Real-time task completion monitoring
<!-- SPECPULSE:END -->