---
description: Generate or validate implementation plans using AI-optimized templates and SDD methodology
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the implementation planning outcome
- Only edit files in plans/ directory - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use `specpulse plan generate/validate/optimize` when available
- **FALLBACK**: File Operations only if CLI fails
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/
- **EDITABLE ONLY**: plans/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Detect current feature context**:
   - Read `.specpulse/memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first

2. **Parse arguments** and determine action:
   - If `validate`: Check plan against SDD gates
   - If `optimize`: Improve existing plan complexity
   - Otherwise: Generate new plan

3. **For /sp-plan:**
   a. **Check for decomposition**: Look for `.specpulse/specs/XXX-feature/decomposition/` directory
   b. **If decomposed**:
      - Read decomposition artifacts (microservices.md, api-contracts/, interfaces/)
      - Generate separate plans for each service
      - Create integration plan for service coordination
      - Structure: `.specpulse/plans/XXX-feature/service-A-plan.md`, `integration-plan.md`
   c. **If not decomposed**:
      - Show existing spec files and ask user to select
      - Generate single monolithic plan
   d. **Find and validate specification** from selected spec file

   e. **Try CLI First**:
      ```bash
      specpulse plan generate <spec-id>
      ```
      If CLI succeeds, STOP HERE.

   f. **Run SDD Compliance Gates**:
      - Specification First: Requirements clear and traced
      - Incremental Planning: Phased approach defined
      - Task Decomposition: Clear breakdown planned
      - Quality Assurance: Testing strategy defined
      - Architecture Documentation: Decisions recorded

   g. **Generate AI-optimized plan** using File Operations:
      - **Read Template**: `.specpulse/templates/plan.md`
      - **Create Plan File**: `.specpulse/plans/XXX-feature/plan-YYY.md`
      - **CRITICAL NUMBERING LOGIC**:
        * Check if `plan-001.md` exists
        * If plan-001.md does NOT exist: Create plan-001.md with full content
        * If plan-001.md EXISTS: Create plan-002.md (or next number)
        * NEVER leave plan-001.md as placeholder if it's the first plan

   h. **Generate comprehensive sections based on architecture**:
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

   i. **Architecture documentation**:
      - Document all architectural decisions with rationale
      - Create improvement strategies for technical debt
      - Track future enhancement opportunities

   j. **Write FULL plan content** to `.specpulse/plans/XXX-feature/plan-XXX.md`

4. **For /sp-plan validate:**
   a. **Show existing plan files**: List all plan-XXX.md files in current feature directory
   b. **Ask user to select**: Which plan file to validate
   c. **Validation** using script:
     ```bash
     specpulse plan validate <plan-id>
     ```
     If CLI fails, use manual validation.
   d. **Verify all SDD gates are addressed**:
     * Specification First: Requirements clear and traced
     * Incremental Planning: Phased approach defined
     * Task Decomposition: Clear breakdown planned
     * Quality Assurance: Testing strategy defined
     * Architecture Documentation: Decisions recorded
   e. **Check architectural decisions** have proper documentation
   f. **Validate test-first approach** is documented
   g. **Ensure integration strategy** uses real services
   h. **Report detailed validation results**

5. **For /sp-plan optimize:**
   a. **Show existing plan files**: List all plan-XXX.md files in current feature directory
   b. **Ask user to select**: Which plan file to optimize
   c. **Read existing plan** from detected context and analyze complexity
   d. **Identify optimization opportunities**:
      - Module consolidation opportunities
      - Abstraction layer removal candidates
      - Simplification strategies
   e. **Generate optimization recommendations**
   f. **Create new version**: Write optimized plan as next version (plan-XXX.md)

**Usage**
```
/sp-plan [action] [feature-directory]
```

Actions: `generate`, `validate`, `optimize` (defaults to `generate`)

**Examples**

**Generate plan for decomposed spec:**
```
/sp-plan
```
Output: Detecting decomposition in `specs/001-authentication/decomposition/`...
Creates:
- `plans/001-authentication/auth-service-plan.md`
- `plans/001-authentication/user-service-plan.md`
- `plans/001-authentication/integration-plan.md`

**Generate plan for monolithic spec:**
```
/sp-plan
```
Output: No decomposition found. Creating single plan:
- `plans/001-authentication/plan-001.md`

**Validate existing plan:**
```
/sp-plan validate
```
Output: Comprehensive validation:
```
PLAN_FILE=plans/001-user-authentication/plan.md
SDD_GATES_STATUS=COMPLETED
MISSING_SECTIONS=0
STATUS=validation_complete
```

**Optimize plan complexity:**
```
/sp-plan optimize
```
Output: Analyzes and recommends complexity reductions.

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

**Principle 3: Task Decomposition**
- [ ] Tasks are specific and actionable
- [ ] Effort estimates provided
- [ ] Definition of Done clear
- [ ] Dependencies identified

**Principle 6: Quality Assurance**
- [ ] Testing strategy appropriate for project
- [ ] Acceptance criteria testable
- [ ] Code review process defined
- [ ] Quality metrics identified

**Principle 7: Architecture Documentation**
- [ ] Technology choices documented
- [ ] Integration points identified
- [ ] Technical debt tracked
- [ ] Trade-offs documented

**Task Format**
```markdown
- [ ] Detect current feature context
- [ ] Parse command arguments
- [ ] Check for decomposition
- [ ] Try CLI command first
- [ ] Create plan files if CLI fails
- [ ] Generate AI-optimized content
- [ ] Validate SDD compliance
- [ ] Report results
```

**Error Handling**

- Specification existence validation
- SDD gate compliance checking
- Template structure validation
- Directory structure verification
- Feature context auto-discovery
- CLI failure detection and fallback

**Reference**
- Use `specpulse plan --help` if you need additional CLI options
- Check `.specpulse/memory/context.md` for current feature context
- Run `specpulse doctor` if you encounter system issues
- After plan creation, continue with `/sp-task` for task breakdown
<!-- SPECPULSE:END -->