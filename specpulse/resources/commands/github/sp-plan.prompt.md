---
description: Generate or validate implementation plans using AI-optimized templates and SDD methodology.
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the implementation planning outcome
- Only edit files in plans/ directory - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse plan generate/validate/optimize` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/, .github/
- **EDITABLE ONLY**: plans/

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Parse arguments** from $ARGUMENTS and determine action:
   - If `validate`: Check plan against SDD gates
   - If `optimize`: Improve existing plan complexity
   - Otherwise: Generate new plan
2. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first
3. **For plan generation**:
   - **Check for decomposition**: Look for `.specpulse/specs/XXX-feature/decomposition/` directory
   - **If decomposed**:
     - Read decomposition artifacts (microservices.md, api-contracts/, interfaces/)
     - Generate separate plans for each service
     - Create integration plan for service coordination
     - Structure: `.specpulse/plans/XXX-feature/service-A-plan.md`, `integration-plan.md`
   - **If not decomposed**:
     - Show existing spec files and ask user to select
     - Generate single monolithic plan
   - **Find and validate specification** from selected spec file
   - **Try CLI First**:
     ```bash
     specpulse plan generate <spec-id>
     ```
     If CLI succeeds, STOP HERE.
   - **Run SDD Compliance Gates**:
     - Specification First: Requirements clear and traced
     - Incremental Planning: Phased approach defined
     - Task Decomposition: Clear breakdown planned
     - Quality Assurance: Testing strategy defined
     - Architecture Documentation: Decisions recorded
   - **Generate AI-optimized plan** by COPYING template from .specpulse/templates/plan.md to .specpulse/plans/XXX-feature/:
     ```markdown
     # Implementation Plan: {{ feature_name }}
     ## Specification Reference
     - **Spec ID**: SPEC-{{ feature_id }}
     - **Spec Version**: {{ spec_version }}
     - **Plan Version**: {{ plan_version }}
     - **Generated**: {{ date }}
     ```
   - **Generate comprehensive sections based on architecture**:
     - **For decomposed specs**:
       * Service-specific plans with bounded contexts
       * Inter-service communication plans
       * Data consistency strategies
       * Service deployment order
       * Integration testing approach
     - **For monolithic specs**:
       * Traditional layered architecture
       * Module boundaries
       * Single deployment strategy
     - **Common sections**:
       * Technology stack with performance implications
       * Testing strategy with coverage targets
       * Security considerations
       * Deployment strategy with rollback plans
   - **CRITICAL NUMBERING LOGIC**:
     - Check if `.specpulse/plans/XXX-feature/plan-001.md` exists
     - If plan-001.md does NOT exist: Create plan-001.md with full content from template
     - If plan-001.md EXISTS: Create plan-002.md (or next number) with new content
     - NEVER leave plan-001.md as placeholder if it's the first plan
4. **For plan validation**:
   - **Verify all SDD gates are addressed**:
     * Specification First: Requirements clear and traced
     * Incremental Planning: Phased approach defined
     * Task Decomposition: Clear breakdown planned
     * Quality Assurance: Testing strategy defined
     * Architecture Documentation: Decisions recorded
   - **Check architectural decisions** have proper documentation
   - **Validate test-first approach** is documented
   - **Ensure integration strategy** uses real services
   - **Report detailed validation results**

**Usage**
Arguments should be provided as: `[action] [feature-directory]`

Actions: `generate`, `validate`, `optimize` (defaults to `generate`)

**SDD Compliance Gates Tracking**

**Principle 1: Specification First**
- [ ] Clear requirements documented
- [ ] User stories with acceptance criteria
- [ ] [NEEDS CLARIFICATION] markers used
- [ ] Functional and non-functional requirements

**Principle 2: Incremental Planning**
- [ ] Work broken into valuable phases
- [ ] Each phase delivers working software
- [ ] Milestones and checkpoints defined
- [ ] Features prioritized by business value

**Examples**

**Generate plan for decomposed spec:**
Input: No arguments (or just action)
Output: Detecting decomposition in `specs/001-authentication/decomposition/`...
Creates service-specific plans.

**Validate existing plan:**
Input: `validate`
Output: Comprehensive validation with detailed reporting.

**Reference**
- Use `specpulse plan --help` if you need additional CLI options
- Check `memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- After plan creation, continue with `/sp-task` for task breakdown
<!-- SPECPULSE:END -->