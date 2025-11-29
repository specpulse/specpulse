$ARGUMENTS

# GitHub Copilot SpecPulse Task Management

Create and manage tasks without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-task [action] [feature-directory]
```

Actions: `breakdown`, `update`, `status`, `execute`, `validate` (defaults to `breakdown`)

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the task management outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Implementation Steps**

1. **Detect Current Feature Context**
   - Check .specpulse/memory/context.md for active feature
   - Look for most recently modified spec/plan/task directory
   - Validate feature directory exists and is properly structured
   - Extract feature ID and name from directory structure

2. **Parse Arguments to Determine Action**
   - If first argument is breakdown, update, status, execute, or validate → Use that action
   - If no action specified → Default to breakdown
   - For other arguments → Look for feature name or use current feature

3. **For Action: breakdown (default)**
   - **Check for Service Decomposition**
     - Look for .specpulse/specs/[feature]/decomposition/ directory
     - If decomposition exists, identify service directories
     - Parse service names for task categorization
     - Plan service-specific task generation
   - **Generate Task Breakdown**
     - Read implementation plan from .specpulse/plans/[feature]/ directory
     - Analyze plan phases and identify implementation steps
     - Create detailed tasks with proper dependencies
     - Assign task IDs using universal numbering system
   - **Create Service-Specific Tasks**
     - If decomposition exists: Auth Service Tasks (AUTH-T001), User Service Tasks (USER-T001), Integration Tasks (INT-T001)
   - **Generate Comprehensive Task Metadata**
     - Task ID, Status, Title, Description, Files Touched, Goals, Success Criteria
     - Dependencies, Next Tasks, Risk Level, Risk Notes, MOSCOW Analysis, Priority
     - SDD Gates Compliance validation
   - **Universal ID System Implementation**
     - Use Glob tool to scan .specpulse/tasks/[feature]/ directory
     - Parse existing task files to extract current numbering (T###.md patterns)
     - Create numbering map: {task_type: max_number_used}
     - Generate next ID: For each task type, use max_num + 1
     - Zero-pad format: format(next_num, '03d') ensures 001, 002, 003
   - **Write Task Files**
     - Create .specpulse/tasks/[feature]/ with appropriate task files
     - Use atomic file operations to prevent corruption

4. **For Action: update**
   - Scan .specpulse/tasks/[feature]/ directory for task files
   - Display available task files for selection
   - Parse current task structure and status
   - Provide interactive update options (mark completed/in-progress/blocked)
   - Update task descriptions or metadata, add new tasks or remove obsolete ones
   - Recalculate progress metrics after updates

5. **For Action: status**
   - Scan all task files in current feature
   - Calculate completion percentages
   - Show progress by service (if decomposed)
   - Display task status distribution (completed, in-progress, blocked, pending)
   - Show SDD Gates compliance status
   - Calculate velocity metrics (tasks/day)
   - Identify parallel tasks and sequential chains
   - Provide recommendations for next actions

6. **For Action: execute**
   - Allow task selection from available pending tasks
   - Validate task readiness and dependencies
   - Display task details before execution
   - Implement task requirements through code changes
   - Test implementation when applicable
   - Mark task as completed automatically
   - Continue with next available task if requested
   - Update progress metrics and context

7. **For Action: validate**
   - Validate task file structure and format
   - Check required fields are present and valid
   - Verify task dependencies exist and are valid
   - Validate SDD Gates compliance
   - Check for duplicate task IDs
   - Verify success criteria are testable
   - Assess risk levels and mitigation strategies
   - Report validation results with fixes needed

8. **Validate structure and report comprehensive status**

**Examples**

**Basic Usage:**
```
/sp-task breakdown
```

Output: Create comprehensive task breakdown with service-specific organization, universal ID system, and detailed metadata.

**Task Status:**
```
/sp-task status
```

Output: Display comprehensive progress with completion percentages, velocity metrics, and recommendations.

**Execute Task:**
```
/sp-task execute AUTH-T005
```

Output: Execute specific task with validation, implementation, testing, and progress updates.

**Advanced Features:**
- **Universal ID System**: Conflict-free task numbering with service-specific patterns
- **Service-Specific Organization**: Tasks organized by microservice boundaries
- **Progress Analytics**: Velocity calculation, completion estimates, dependency tracking
- **SDD Gates Compliance**: Specification traced, task decomposed, quality assured, traceable implementation

**Error Handling**
- No active feature: Prompt to run /sp-pulse first
- Missing plan file: Guide user to create plan with /sp-plan
- Invalid task format: Identify and fix structural issues
- Circular dependencies: Detect and resolve dependency loops

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations with atomic writes
- Comprehensive task lifecycle management
- Advanced analytics and progress tracking
<!-- SPECPULSE:END -->

## Implementation Notes

When called with the specified arguments, execute the task management workflow according to the action type. Use only file operations within the allowed directories and maintain comprehensive error handling throughout the process.