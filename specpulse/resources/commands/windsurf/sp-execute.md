---
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the task execution outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments and determine execution mode**:
   - Parse the command arguments:
     - `all` → Execute ALL pending tasks non-stop
     - `next` or no argument → Execute next pending task and continue
     - `T001` or `AUTH-T001` → Execute specific task
   - Set execution mode accordingly
   - Determine if continuous execution is needed

2. **Detect current feature context**:
   - Use Read tool to examine .specpulse/memory/context.md
   - Look for **Directory**: field to identify current feature
   - If no context found, use Glob tool to find first feature with task files
   - Validate feature directory follows naming convention (XXX-feature-name)
   - Set tasks_dir to .specpulse/tasks/[current-feature]

3. **Load and analyze task files**:
   - Use Glob tool to find all *.md files in tasks directory
   - Use Read tool to examine each task file
   - Parse task status markers:
     - `[ ]` = Pending task
     - `[>]` = In progress task
     - `[x]` = Completed task
     - `[!]` = Blocked task
   - Build task inventory with status and dependencies
   - Validate task file structure and content

4. **Determine task execution order**:
   - For continuous mode (all or next):
     - Find first pending task (`[ ]`)
     - Check if dependencies are completed
     - If dependencies not met, skip to next available task
     - For specific task mode, validate the requested task exists
   - For service tasks: Handle AUTH-T001, USER-T001 patterns, respect service-specific dependencies

5. **Execute task implementation**:
   - **Step 1: Mark Task In Progress**
     - Use Edit tool to change task status from `[ ]` to `[>]` (in progress)
     - Parse task requirements from the file content
     - Extract specific implementation steps from task description
   - **Step 2: Atomic File Operations**
     - For Backend/API Tasks: Database operations, API endpoints, Authentication, Validation
     - For Frontend Tasks: Component creation, Styling, User interactions, Routing
     - For Integration Tasks: Service communication, Data synchronization, Testing, Documentation
     - For Infrastructure Tasks: Configuration, CI/CD, Monitoring, Security
   - **Step 3: Implementation Verification**
     - Syntax Validation: Use Bash to run linters, type checkers, syntax validators
     - Unit Testing: Create and run unit tests for implemented code
     - Integration Testing: Test component interactions and API endpoints
     - Manual Verification: Test functionality through actual usage scenarios

6. **Mark task completion**:
   - Use Edit tool to change task status from `[>]` to `[x]` (completed)
   - Add completion timestamp if not present
   - Verify all requirements from task description are met
   - Update any dependent tasks that can now be executed

7. **Continue execution (If in continuous mode)**:
   - Immediately move to next pending task
   - Repeat steps 4-6 without stopping for confirmation
   - Continue until all tasks are completed or blocked
   - Only stop when all tasks completed, no more tasks can execute, error occurs, or user stops

8. **Final status report**:
   - Use Read tool to verify final state of all task files
   - Count completed vs remaining tasks
   - Calculate completion percentage
   - List any blockers that prevented completion
   - Provide summary of work accomplished
   - Suggest next steps

**Usage**
```
/sp-execute [task-id|all|next]
```

**Examples**

**Execute Next Task:**
```
/sp-execute
```

Output: Find current feature, locate next `[ ]` task, execute implementation, mark complete, continue to next.

**Execute All Tasks:**
```
/sp-execute all
```

Output: Find ALL pending tasks, execute each in sequence without stopping, update progress, report final results.

**Execute Specific Task:**
```
/sp-execute T001
```

Output: Find task file T001.md, execute all pending tasks in that file, update progress accordingly.

**Advanced Features:**
- **Atomic File Operations**: Safe task status updates prevent corruption
- **Continuous Execution**: Non-stop task completion for `all` mode
- **Service-Specific Handling**: Proper dependency management for microservices
- **Implementation Verification**: Comprehensive testing and validation
- **Progress Tracking**: Real-time status updates and completion metrics

**Task Status Markers**
- `[ ]` - Pending task (ready to execute)
- `[>]` - In progress (currently working on)
- `[x]` - Completed (done)
- `[!]` - Blocked (waiting for dependency)

**Error Handling**
- Implementation errors: Document failure, mark task as blocked, continue
- Test failures: Fix implementation errors, retry testing, mark as completed
- File system errors: Provide specific error messages and resolution steps
- Network issues: Retry operations, provide offline alternatives

**Safety Features**
- **Atomic Operations**: Complete file content replacement to prevent corruption
- **Safe Directory Access**: Path validation within .specpulse/ directory only
- **Backup Creation**: Create .backup files before major changes
- **Rollback on Failure**: Restore original content if update fails

**Reference**
- Check memory/context.md for current feature context
- Validate task dependencies before execution
- After task completion, continue with next available task or run /sp-status for progress

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations with atomic updates
- Comprehensive error recovery and rollback mechanisms
- Manual task parsing and progress tracking
<!-- SPECPULSE:END -->