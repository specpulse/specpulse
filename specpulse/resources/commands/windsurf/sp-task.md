---
description: Generate and manage task breakdowns with versioning using SpecPulse methodology
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the requested task management outcome
- Only edit files in tasks/, specs/, plans/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse sp-task breakdown <plan-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

## For /sp-task breakdown or /sp-task:
1. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., 001-user-authentication)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first

2. **Show list of existing plan files** in current feature directory
3. **Ask user which plan file** to base tasks on
4. **Read selected implementation plan** from `@{.specpulse/.specpulse/plans/*/plan-XXX.md}`
5. **Try CLI first**: Run `!{bash specpulse sp-task breakdown <plan-id>}`
6. **If CLI succeeds**: Let user know tasks are generated and show summary
7. **If CLI fails**: Continue with file operations below

8. **Generate tasks from plan using STANDARDIZED FORMAT** (File Operations Fallback):
   - Create task categories:
     • Critical Path (Phase 0)
     • Phase 1: Foundation
     • Phase 2: Core Features
     • Phase 3: Polish
     • Phase 4: Testing

   - For each task, MUST use this exact YAML format:
     ```yaml
     ---
     id: task-[slug]
     status: todo | in-progress | blocked | done
     title: "Short but clear task title"
     description: |
       *Answer these 4 questions with sufficient detail:*
       - What problem does this solve?
       - Why is this necessary?
       - How will this be done? (step-by-step, include function/file names when possible)
       - When is this considered complete?

     files_touched:
       - path: src/...
         reason: "What changes in this file, briefly"

     goals:
       - "Concrete goal 1 achieved when this task completes"
       - "Concrete goal 2"

     success_criteria:
       - "Test/acceptance criteria 1 (measurable or verifiable)"
       - "Test/acceptance criteria 2"

     dependencies:
       - task-[id-1]
       - task-[id-2]

     next_tasks:
       - task-[id-x]
       - task-[id-y]

     risk_level: low | medium | high
     risk_notes: |
       "Important risks, edge cases, technical debt notes for this task"

     moscow:
       must:
         - "Must-have requirements/behaviors for this task"
         - "Without these, task is not considered complete"
       should:
         - "Additional improvements if time/budget allows"
         - "Performance, UX, DX improvements, etc."
       know:
         - "Critical knowledge, context, or domain details developer must know"
         - "Documentation links, rationale for specific decisions"
       wont:
         - "Things we WILL NOT do in this task scope - out of scope"
         - "Topics for future tasks"

     priority_overall: must | should | could | wont
     priority_reason: "Why this task has this priority - short, clear explanation."
     ```

9. **Check existing task files** and create next version (task-001.md, task-002.md, etc.)
10. **Write tasks to** `.specpulse/tasks/XXX-feature/task-XXX.md`
11. **Run validation**: `!{bash specpulse --no-color validate task --verbose}`

## For /sp-task update:
1. **Show existing task files** in current feature directory
2. **Ask user which task file** to update
3. **Read selected current tasks** from `@{.specpulse/.specpulse/tasks/*/task-XXX.md}`
4. **Ask which tasks to update**
5. **Mark tasks as completed/in-progress**
6. **Add newly discovered tasks**
7. **Update dependencies and blockers**
8. **Save updated task list**
9. **Run validation**: `!{bash specpulse --no-color validate task --verbose}`

## For /sp-task status:
1. **Show existing task files** in current feature directory
2. **Ask user which task file** to show status for
3. **Read selected current tasks**
4. **Run analysis**: `!{bash specpulse --no-color validate task --verbose}`
5. **Count completed vs total**
6. **Show current phase progress**
7. **List any blockers**
8. **Estimate remaining work**
9. **Display progress summary**

**Task Format**
```markdown
- [ ] T001: [S] Set up project structure
- [ ] T002: [M] Create database schema
- [x] T003: [L] Implement authentication
```

**Examples**
- `/sp-task breakdown`
- `/sp-task update`
- `/sp-task status`

**Reference**
- Use `specpulse task breakdown --help` if you need additional CLI options
- Check `.specpulse/memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->