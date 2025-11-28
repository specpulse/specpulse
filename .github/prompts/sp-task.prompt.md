---
description: Generate and manage task breakdowns with versioning using AI-optimized templates.
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the task management outcome
- Only edit files in tasks/, specs/, plans/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse sp-task breakdown <plan-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/
- **EDITABLE ONLY**: tasks/, specs/, plans/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Parse arguments** from $ARGUMENTS to determine action:
   - If "update": Update task status
   - If "status": Show progress
   - Otherwise: Generate task breakdown
2. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., 001-user-authentication)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first
3. **For task breakdown**:
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
   - **Generate AI-optimized tasks using File Operations**:
     - **Step 1: Read Task Template**
       ```
       Read: templates/task.md
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
4. **For task update**:
   - **Show existing task files**: List all task-XXX.md files in current feature directory
   - **Ask user to select**: Which task file to update
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
5. **For task status**:
   - **Show existing task files**: List all task-XXX.md files in current feature directory
   - **Ask user to select**: Which task file to show status for
   - **Display comprehensive progress**:
     - Overall completion percentage
     - Phase-by-phase progress
     - Blocker identification and resolution
     - Velocity metrics and estimates
     - SDD gates compliance status

**Usage**
Arguments should be provided as: `[action] [feature-directory]`

Actions: `breakdown`, `update`, `status`, `execute` (defaults to `breakdown`)

**Task Format**
```markdown
- [ ] T001: [S] Set up project structure
- [ ] T002: [M] Create database schema
- [x] T003: [L] Implement authentication
```

**Examples**

**Generate tasks for decomposed spec:**
Input: `breakdown`
Output: Detecting decomposition in `specs/001-authentication/decomposition/`...
Creates service-specific and integration tasks.

**Update task status:**
Input: `update mark T001-T005 as completed`
Output: Updates task status and recalculates progress metrics.

**Reference**
- Use `specpulse task breakdown --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->