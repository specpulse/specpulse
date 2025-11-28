---
name: SpecPulse: Task Breakdown
description: Break down plans into detailed tasks using SpecPulse SDD methodology
category: SpecPulse
tags: [specpulse, tasks, breakdown, execution]
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the task breakdown outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse task breakdown <plan-id>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/, .crush/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments** to extract plan reference and task options
2. **Determine current context**:
   - Read: memory/context.md
   - Extract current.feature and current.feature_id if available
3. **Try CLI first**:
   - Run `specpulse task breakdown <plan-id>`
   - If this succeeds, continue with task refinement
4. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Read plan file**
     - Read: plans/current-feature_id/<plan-id>.md
     - Extract implementation phases and requirements
   - **Step 2: Create task breakdown file**
     - Create: tasks/current-feature_id/tasks-001.md (or next available number)
5. **Generate tasks using STANDARDIZED FORMAT**:
   - Analyze plan phases and create granular task breakdown
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

6. **Task optimization**:
   - Identify parallel execution opportunities
   - Optimize critical path
   - Assign resource requirements
   - Define milestones and checkpoints

**Reference**
- Use `specpulse task breakdown --help` for additional CLI options
- Check related plans for implementation phases
- Use `execute` to start task execution
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->