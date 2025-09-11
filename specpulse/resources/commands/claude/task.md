# /task

Create task breakdown from implementation plan.

## Usage
```
/task breakdown
```

## Description
Generates a detailed task list from the implementation plan with dependencies and time estimates.

## Process
1. Reads the implementation plan
2. Breaks down each phase into tasks
3. Identifies dependencies
4. Marks parallel tasks with [P]
5. Estimates time for each task
6. Creates critical path
7. Generates execution schedule

## Task Structure
Each task includes:
- ID (T001, T002, etc.)
- Type (setup/development/testing/documentation)
- Priority (HIGH/MEDIUM/LOW)
- Estimate (hours)
- Dependencies
- Description
- Acceptance criteria
- Files affected
- Assignable role

## Organization
- **Parallel Groups**: Tasks that can run simultaneously
- **Sequential Tasks**: Tasks with dependencies
- **Critical Path**: Longest dependency chain

## Example
```
/task breakdown
```

Reads: `plans/001-user-auth/implementation.md`
Creates: `tasks/001-user-auth/tasks.md`