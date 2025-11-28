---
agent: build
description: Track project progress and status using SpecPulse SDD methodology.
---

The user has requested the following change proposal. Use the openspec instructions to create their change proposal.
<UserRequest>
  sp-status $ARGUMENTS
</UserRequest>

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the status tracking outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse status` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
1. **Parse arguments** to extract status query parameters from $ARGUMENTS
2. **Determine current context**:
   - Read: memory/context.md
   - Extract current.feature, current.feature_id, and progress information
3. **Try CLI first**:
   - Run `specpulse status [component]`
   - If this succeeds, display detailed status
4. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Analyze project structure**
     - Read: memory/context.md for current context
     - Scan: specs/, plans/, tasks/ directories for progress
     - Check: Git status and commit history
5. **Comprehensive status analysis**:
   - Generate detailed status sections:
     1. **Project Overview** (current feature, progress percentage)
     2. **Specification Status** (completion status, issues found)
     3. **Plan Status** (implementation phases, milestones)
     4. **Task Status** (completed, in-progress, pending tasks)
     5. **Quality Metrics** (test coverage, validation results)
   - Include timeline and milestone tracking

6. **Progress visualization**:
   - Create progress charts and graphs
   - Show task completion rates
   - Display timeline vs actual progress
   - Identify bottlenecks and risks

**Usage**
Arguments should be provided as: `[component] [options]`

**Examples**

**Overall Status:**
Input: (no arguments)
Output: Display comprehensive project status with progress metrics.

**Component Status:**
Input: `specs`
Output: Display detailed specification status and completion metrics.

**Status with Options:**
Input: `detailed:true include:metrics`
Output: Display detailed status with comprehensive metrics.

**Next steps:**
- Recommend: "Continue with next pending task or identify blockers"
- Action: "Use appropriate sp-* command to continue work"
- Status: `STATUS=analysis_complete, PROGRESS=68%, NEXT_ACTION=continue_task_execution`

**Reference**
- Use `specpulse status --help` for additional CLI options
- Check memory/context.md for current progress
- Use appropriate sp-* commands to continue work
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->