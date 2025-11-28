---
name: SpecPulse: Track Progress
description: Track project progress and status using SpecPulse SDD methodology
category: SpecPulse
tags: [specpulse, status, progress, monitoring]
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the status tracking outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse status` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/, .crush/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments** to extract status query parameters
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

**Reference**
- Use `specpulse status --help` for additional CLI options
- Check memory/context.md for current progress
- Use appropriate commands to continue work
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->