# /task

Generate task breakdowns using SpecPulse structure.

## Usage
```
/task breakdown
/task update
/task status
```

## Commands

### breakdown
Generate tasks from plan:
1. Create task categories:
   - Critical Path (Phase 0)
   - Phase 1: Foundation
   - Phase 2: Core Features
   - Phase 3: Polish
   - Phase 4: Testing

2. For each task:
   - Use T[XXX] format (T001, T002)
   - Include clear description
   - Mark dependencies
   - Estimate complexity (S/M/L/XL)
   - Assign priority

3. Write to tasks/[feature]/tasks.md

### update
Update task status:
1. Mark tasks as completed
2. Add new discovered tasks
3. Update dependencies
4. Track blockers

### status
Show task progress:
1. Count completed vs total
2. Show current phase
3. List blockers
4. Estimate remaining work

## Task Format
```markdown
- [ ] T001: [S] Set up project structure
- [ ] T002: [M] Create database schema
- [x] T003: [L] Implement authentication
```

## Example
```
/task breakdown
```