---
name: SpecPulse: Create Implementation Plan
description: Create implementation plans from specifications using SpecPulse SDD methodology
category: SpecPulse
tags: [specpulse, planning, implementation, strategy]
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the plan creation outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse plan create <plan-title>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/, .crush/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments** to extract plan details
2. **Determine current context**:
   - Read: memory/context.md
   - Extract current.feature and current.feature_id if available
   - Check for existing specifications in specs/current-feature_id/
3. **Try CLI first**:
   - Run `specpulse plan create "<plan-title>"`
   - If this succeeds, continue with expansion
4. **If CLI doesn't exist, use File Operations**:
   - **Step 1: Create plan file**
     - Create: plans/current-feature_id/plan-001.md (or next available number)
     - Use appropriate implementation planning template
5. **Intelligent plan generation**:
   - Analyze related specifications and extract requirements
   - Generate comprehensive implementation plan sections:
     1. **Implementation Overview** (summary and approach)
     2. **Technical Architecture** (system design and components)
     3. **Implementation Phases** (step-by-step development phases)
     4. **Resource Requirements** (skills, tools, dependencies)
     5. **Risk Assessment** (potential issues and mitigation strategies)
   - Include detailed timeline and milestones

6. **Break down into tasks**:
   - Create granular work breakdown structure
   - Assign complexity estimates and dependencies
   - Identify parallel work opportunities
   - Define validation criteria for each phase

**Reference**
- Use `specpulse plan create --help` for additional CLI options
- Check related specifications for requirements
- Use `task` to create detailed task breakdowns
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->