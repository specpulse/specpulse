---
name: /sp-execute
id: sp-execute
category: SpecPulse
description: Execute tasks continuously without stopping - complete all pending work in sequence.
---
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the task execution outcome
- Only edit files in tasks/, specs/, plans/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse task execute <task-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: tasks/, specs/, plans/, memory/

**Continuous Execution Mode**
**This command enables NON-STOP task execution. I will:**
1. Execute the current/next task
2. Mark it as completed
3. Immediately move to the next task
4. Continue until ALL tasks are done or blocked

**NO STOPPING** between tasks unless:
- All tasks are completed
- Remaining tasks are blocked
- An error occurs that requires user intervention
- User explicitly stops me

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Check project status using CLI**:
   ```bash
   specpulse --no-color doctor
   specpulse --no-color spec-progress [feature-id]
   ```
   If CLI fails, use manual status checking.
2. **Read Task File**:
   ```
   Read: tasks/XXX-feature/task-YYY.md
   ```
3. **Mark Task as Started**:
   ```
   Edit: tasks/XXX-feature/task-YYY.md
   (Update metadata: STATUS: in_progress, add timestamp)
   ```
4. **Execute Task Implementation**:
   - Implement the solution based on task description
   - Test if applicable
   - Document any decisions or changes
5. **Mark Task as Completed**:
   ```
   Edit: tasks/XXX-feature/task-YYY.md
   (Update metadata: STATUS: completed, add completion timestamp)
   ```
6. **Continue immediately**:
   - NO PAUSE for confirmation
   - NO STOPPING to explain what was done
   - Move directly to next task
7. **Repeat until done**:
   - Continue executing tasks in sequence
   - Only stop when all tasks are completed or blocked

**Usage**
```
/sp-execute                    # Execute next pending task and continue
/sp-execute next               # Same as above
/sp-execute all                # Execute ALL pending tasks non-stop
/sp-execute T001               # Execute specific task
/sp-execute AUTH-T001          # Execute specific service task
```

**Task Execution Flow**

**Single Task Mode (`/sp-execute` or `/sp-execute next`)**:
1. Find next pending task (T001 or AUTH-T001)
2. Mark as in-progress: [ ] → [>]
3. Implement the task
4. Mark as completed: [>] → [x]
5. Automatically continue to next task
6. Repeat until all done

**Batch Mode (`/sp-execute all`)**:
1. Get list of ALL pending tasks
2. Execute each task in sequence
3. No stopping between tasks
4. Continue until all completed

**Specific Task Mode (`/sp-execute T001`)**:
1. Execute the specified task
2. Mark as completed
3. Continue to next pending task

**Task Format Tracking**
```markdown
- [ ] T001: [S] Set up project structure      # Pending
- [>] T002: [M] Create database schema       # In Progress
- [x] T003: [L] Implement authentication      # Completed
```

**Examples**

**Execute next task:**
```
/sp-execute
```
Output: Finds T001, marks as [>], implements it, marks as [x], moves to T002 without stopping.

**Execute all tasks:**
```
/sp-execute all
```
Output: Executes T001→T002→T003→... continuously until all done.

**Execute specific task:**
```
/sp-execute T005
```
Output: Executes T005, then continues with T006 and beyond.

**Continuous Progress Tracking**

**Status Updates During Execution:**
- Task start: Mark as in-progress with timestamp
- Task completion: Mark as completed with timestamp
- Blocker detection: Mark as blocked with reason
- Automatic progress calculation after each task

**Batch Execution Summary:**
```
EXECUTION_SUMMARY:
TASKS_EXECUTED=15
TASKS_COMPLETED=12
TASKS_BLOCKED=3
TOTAL_TIME=2h45m
AVERAGE_TASK_TIME=11m
```

**CLI Integration**

**Try CLI First:**
```bash
specpulse task execute <task-id>
specpulse task execute --all
```

**Fallback to Manual Execution if CLI Fails:**
1. Read task file manually
2. Parse task requirements
3. Implement task
4. Update task status
5. Continue to next task

**Error Handling**

**Recovery Strategies:**
- Task failure: Mark as blocked, continue with next task
- Dependency issue: Skip blocked task, continue with parallel tasks
- System error: Pause execution, report error, wait for user input

**Task Status Transitions:**
```
[ ] Pending → [>] In Progress → [x] Completed
                ↓
           [!] Blocked (with reason)
```

**Reference**
- Use `specpulse task execute --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- Use `/sp-status` to check overall progress
- Execution continues automatically until all tasks are complete
<!-- SPECPULSE:END -->