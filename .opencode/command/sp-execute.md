---
agent: build
description: Execute tasks continuously using SpecPulse SDD methodology.
---

The user has requested the following change proposal. Use the openspec instructions to create their change proposal.
<UserRequest>
  sp-execute $ARGUMENTS
</UserRequest>

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the continuous task execution outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse task execute` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
1. **Parse arguments** to extract execution parameters from $ARGUMENTS
2. **Determine current context**:
   - Read: memory/context.md
   - Extract current.feature, current.feature_id, and current.task if available
3. **Try CLI first**:
   - Run `specpulse task execute [task-id]`
   - If this succeeds, monitor execution progress
4. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Read task breakdown**
     - Read: tasks/current-feature_id/tasks-*.md
     - Extract task list and dependencies
5. **Continuous execution strategy**:
   - Execute tasks in dependency order
   - For each task:
     1. **Task Preparation**
        - Read task requirements and acceptance criteria
        - Prepare development environment
        - Check dependencies and prerequisites
     2. **Task Execution**
        - Implement task requirements
        - Create code, tests, and documentation
        - Follow coding standards and best practices
     3. **Task Validation**
        - Run tests and validation checks
        - Verify acceptance criteria met
        - Update progress and status
     4. **Task Completion**
        - Update memory/context.md with progress
        - Mark task as completed
        - Move to next task

6. **Progress tracking**:
   - Monitor task completion and progress
   - Handle errors and rollback when needed
   - Update context with current status
   - Generate progress reports

**Usage**
Arguments should be provided as: `[task-id] [options]`

**Examples**

**Execute All Tasks:**
Input: (no arguments)
Output: Execute all pending tasks in dependency order.

**Execute Specific Task:**
Input: `task-005`
Output: Execute specific task with all its requirements.

**Execute with Options:**
Input: `parallel:false validate:true`
Output: Execute sequentially with strict validation.

**Next steps:**
- Monitor: "Execution progress tracked in memory/context.md"
- Continue: "Use `sp-status` to check current progress"
- Status: `STATUS=executing, CURRENT_TASK=task-003, PROGRESS=45%`

**Reference**
- Use `specpulse task execute --help` for additional CLI options
- Check task breakdown files for task details
- Use `sp-status` to monitor execution progress
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->