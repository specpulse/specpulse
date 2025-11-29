---
name: SpecPulse: Task Execute
description: Execute tasks continuously without SpecPulse CLI
category: SpecPulse
tags: [specpulse, task, execute]
---

# SpecPulse Task Execution

Execute tasks continuously without requiring SpecPulse CLI installation.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to task execution and updates
- Only edit files in tasks/, memory/, and project code directories
- Favor straightforward, minimal implementations first

**Steps**
Track these steps as TODOs and complete them one by one.
1. Check .specpulse/memory/context.md for active feature
2. Locate current task breakdown in .specpulse/tasks/[feature]/
3. Parse execution arguments (task-id or "all")
4. Load task details and dependencies
5. Verify prerequisites are completed
6. Execute task implementation step by step
7. Update task status and progress in real-time
8. Validate task completion against acceptance criteria
9. Update feature context and memory with decisions
10. Move to next available task if dependencies allow

**Reference**
- Check task breakdown files for task details and dependencies
- Refer to memory/context.md for feature context and decisions
- Follow project code structure and conventions
- Validate against acceptance criteria in task definitions

**Usage**
Arguments should be provided as: `[task-id | all] [--force] [--validate]`

**Task Execution Process:**

### Single Task Execution
When specific task-id provided:
1. Load task T[xxx] details
2. Check all dependencies are completed
3. Execute task implementation
4. Validate against acceptance criteria
5. Update task status to completed
6. Update dependent tasks availability

### All Tasks Execution
When "all" provided:
1. Find all available tasks (dependencies satisfied)
2. Execute tasks in priority order
3. Continue until no more tasks available
4. Report progress and blockers

**Task Implementation Template:**
```markdown
# Executing Task T[xxx]: [Task Title]

## Task Details
**Priority:** [High/Medium/Low]
**Estimated Time:** [time]
**Dependencies:** [task-list]
**Status:** In Progress → Completed

## Implementation Steps
1. [ ] Step 1 description
2. [ ] Step 2 description
3. [ ] Step 3 description

## Acceptance Criteria Validation
- [ ] Criterion 1 met
- [ ] Criterion 2 met
- [ ] Criterion 3 met

## Implementation Notes and Decisions
- Decision 1: [description and rationale]
- Decision 2: [description and rationale]

## Files Modified/Created
- `path/to/file1.ext` - [description of changes]
- `path/to/file2.ext` - [description of changes]

## Next Steps
- Ready for dependent tasks: [task-list]
- Review and validation required
```

**Progress Tracking:**
```markdown
## Execution Progress Update
### Current Task: T[xxx] - [Task Title]
### Overall Feature Progress: [xx]%
### Completed Tasks: [count]/[total]
### Current Session Tasks: [count] completed

### Recent Completions
- ✅ T[xxx]: [Task Title] - completed at [timestamp]
- ✅ T[yyy]: [Task Title] - completed at [timestamp]

### Next Available Tasks
- 🔄 T[aaa]: [Task Title] - dependencies satisfied
- 🔄 T[bbb]: [Task Title] - dependencies satisfied

### Blockers
- ❌ T[ccc]: [Task Title] - blocked by [dependency]
```

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Continuous task execution with automatic dependency checking
- Real-time progress tracking and status updates
- Comprehensive validation against acceptance criteria

**Advanced Features:**
- **Dependency Management**: Automatic prerequisite checking
- **Continuous Execution**: Execute multiple tasks in sequence
- **Progress Tracking**: Real-time status and completion monitoring
- **Validation**: Comprehensive acceptance criteria validation
- **Decision Logging**: Track implementation decisions and rationale

**Error Handling:**
- Task not found: List available tasks
- Dependencies not satisfied: Identify missing prerequisites
- Validation failures: Report specific acceptance criteria not met
- Permission issues: Guide through file access problems
<!-- SPECPULSE:END -->