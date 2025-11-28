---
name: /sp-task
id: sp-task
category: SpecPulse
description: Generate and manage task breakdowns with versioning using AI-optimized templates.
---
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the task management outcome
- Only edit files in tasks/, specs/, plans/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse sp-task breakdown <plan-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: tasks/, specs/, plans/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., 001-user-authentication)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first
2. **Parse arguments** to determine action:
   - If "update": Update task status
   - If "status": Show progress
   - Otherwise: Generate task breakdown
3. **For /sp-task breakdown or /sp-task:**
   - **Check for decomposition**: Look for `specs/XXX-feature/decomposition/` directory
   - **If decomposed**:
     - Read service definitions from decomposition
     - Show service-specific plan files (auth-service-plan.md, user-service-plan.md, etc.)
     - Generate tasks per service with service prefix (AUTH-T001, USER-T001)
     - Create integration tasks (INT-T001) for cross-service work
     - Structure: `tasks/XXX-feature/auth-service-tasks.md`, `integration-tasks.md`
   - **If not decomposed**:
     - Show existing plan files and ask user to select
     - Generate single task file with standard IDs (T001, T002)
   - **Try CLI First**:
     ```bash
     specpulse sp-task breakdown <plan-id>
     ```
     If CLI succeeds, STOP HERE.
   - **Read selected implementation plan** from selected plan file
   - **Generate tasks using STANDARDIZED FORMAT**:
     - **Step 1: Use this exact YAML structure for EVERY task**:
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
       ---
       ```
     - **Step 2: Read Standard Template**
       ```
       Read: templates/task_standard.md
       ```
     - **Step 2: Parse Plan and Create Task Files**
       ```
       For each phase/component in plan:
         Write: tasks/XXX-feature/task-001.md
         Write: tasks/XXX-feature/task-002.md
         ... (one file per task)

       Content includes:
         - Metadata (feature ID, task number, status: pending)
         - Task description from plan
         - Template structure for expansion
       ```
     - **IMPORTANT**: Can EDIT files in tasks/ folder, but NEVER modify templates/ or commands/ folders
   - **Generate structured task categories based on architecture**:
     - **For decomposed services**:
       * Service-specific tasks with bounded context
       * Inter-service integration tasks
       * Service deployment order tasks
       * Contract testing tasks between services
     - **For monolithic architecture**:
       * Layer-based tasks (data, business, API)
       * Module-specific tasks
     - **Common categories**:
       * SDD Gates Compliance
       * Critical Path identification
       * Parallel vs Sequential grouping
       * Progress Tracking configuration
   - **For each task**, generate comprehensive metadata:
     - **ID**: T[XXX] format (T001, T002)
     - **Type**: setup, development, testing, documentation
     - **Priority**: HIGH, MEDIUM, LOW
     - **Estimate**: Hours or complexity points
     - **Dependencies**: Task ID dependencies
     - **Description**: Clear what needs to be done
     - **Acceptance**: How to verify completion
     - **Files**: Files to be created/modified
     - **Assignable**: Role/skill required
     - **Parallel**: Whether can run in parallel [P]
   - **Generate AI execution guidelines** with workflow integration
   - **Version management**: Check existing task files and create next version (task-001.md, task-002.md, etc.)
   - **Write comprehensive task breakdown** to `tasks/XXX-feature/task-XXX.md`
4. **For /sp-task update:**
   - **Show existing task files**: List all task-XXX.md files in current feature directory
   - **Ask user to select**: Which task file to update
   - **Analysis** using script:
     ```bash
     specpulse task breakdown "$PLAN_ID"
     ```
   - **Parse current tasks** from selected file with comprehensive status:
     - Total tasks, completed, pending, blocked
     - Parallel tasks identification
     - SDD gates status
     - Completion percentage calculation
   - **Interactive task updates**:
     - Mark tasks as completed/in-progress/blocked
     - Update dependencies and blockers
     - Add newly discovered tasks with proper metadata
     - Adjust estimates based on actual progress
   - **Generate updated progress tracking** YAML
5. **For /sp-task status:**
   - **Show existing task files**: List all task-XXX.md files in current feature directory
   - **Ask user to select**: Which task file to show status for
   - **Enhanced reporting** from script output:
     ```bash
     TOTAL_TASKS=25
     COMPLETED_TASKS=10
     COMPLETION_PERCENTAGE=40%
     SDD_GATES_PENDING=2
     ```
   - **Display comprehensive progress**:
     - Overall completion percentage
     - Phase-by-phase progress
     - Blocker identification and resolution
     - Velocity metrics and estimates
     - SDD gates compliance status

**Usage**
```
/sp-task [action] [feature-directory]
```

Actions: `breakdown`, `update`, `status`, `execute` (defaults to `breakdown`)

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
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->