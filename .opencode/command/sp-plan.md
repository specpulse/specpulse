---
agent: build
description: Create implementation plans from specifications using SpecPulse SDD methodology.
---

The user has requested the following change proposal. Use the openspec instructions to create their change proposal.
<UserRequest>
  sp-plan $ARGUMENTS
</UserRequest>

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the plan creation outcome
- Only edit files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse plan create <plan-title>` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/, .opencode/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
1. **Parse arguments** to extract plan details from $ARGUMENTS
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

**Usage**
Arguments should be provided as: `"plan title" [from:spec-id]"

**Examples**

**Basic Plan:**
Input: `"User authentication implementation"`
Output: Create comprehensive implementation plan with phases, tasks, and timeline.

**Plan from Specification:**
Input: `"OAuth2 integration" from:spec-001`
Output: Create implementation plan based on requirements in spec-001.md.

**Complex Plan:**
Input: `"Microservices migration strategy"`
Output: Create detailed migration plan with rollback strategies and testing phases.

**Next steps:**
- Guide: "Use `sp-task` to break down this plan into detailed tasks"
- Status: `STATUS=plan_complete, PLAN_FILE=plans/001/auth-implementation.md, READY_FOR_TASKS=true`

**Reference**
- Use `specpulse plan create --help` for additional CLI options
- Check related specifications for requirements
- Use `sp-task` to create detailed task breakdowns
- Run `specpulse doctor` if you encounter system issues
<!-- SPECPULSE:END -->