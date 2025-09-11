---
name: task
description: Generate and manage task breakdowns
allowed_tools:
  - Read
  - Write  
  - Edit
  - Bash
---

# /task Command

Generate task breakdowns from implementation plans using SpecPulse structure.

## Usage
```
/task [action]
```

Actions: `breakdown`, `update`, `status` (defaults to `breakdown`)

## Implementation

When called with `/task $ARGUMENTS`, I will:

1. **Parse arguments** to determine action:
   - If `$ARGUMENTS` is `update`: Update task status
   - If `$ARGUMENTS` is `status`: Show progress
   - Otherwise: Generate task breakdown

2. **For `/task breakdown` or `/task`:**
   
   a. **Read implementation plan** from `plans/XXX-feature/plan.md`
   
   b. **Generate tasks from plan**:
      - Create task categories:
   - Critical Path (Phase 0)
   - Phase 1: Foundation
   - Phase 2: Core Features
   - Phase 3: Polish
   - Phase 4: Testing

      - For each task:
   - Use T[XXX] format (T001, T002)
   - Include clear description
   - Mark dependencies
   - Estimate complexity (S/M/L/XL)
   - Assign priority

   c. **Write tasks** to `tasks/XXX-feature/tasks.md`

3. **For `/task update`:**
   - Read current tasks from `tasks/XXX-feature/tasks.md`
   - Ask which tasks to update
   - Mark tasks as completed/in-progress
   - Add newly discovered tasks
   - Update dependencies and blockers
   - Save updated task list

4. **For `/task status`:**
   - Read current tasks
   - Count completed vs total
   - Show current phase progress
   - List any blockers
   - Estimate remaining work
   - Display progress summary

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