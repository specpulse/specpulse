---
name: sp-plan
description: Generate or validate implementation plans using AI-optimized templates
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-plan Command

Generate implementation plans from specifications following SpecPulse methodology with SDD compliance and AI-optimized templates.

## CRITICAL: LLM Workflow Rules

**PRIMARY WORKFLOW: Use CLI when available**
- Prefer `specpulse` CLI commands when they exist
- Use Bash tool ONLY for CLI commands, not for file editing
- Only use Read/Write/Edit tools when CLI doesn't cover the operation

**PROTECTED DIRECTORIES (NEVER EDIT):**
- `templates/` - Template files
- `.specpulse/` - Internal config
- `specpulse/` - Package code
- `.claude/` and `.gemini/` - AI configuration
- **ONLY EDIT**: specs/, plans/, tasks/, memory/
- Templates are COPIED to plans/ folder, then edited there

## Usage
```
/sp-plan [action] [feature-directory]
```

Actions: `generate`, `validate`, `optimize` (defaults to `generate`)

## Implementation

When called with `/sp-plan $ARGUMENTS`, I will:

1. **Detect current feature context**:
   - Read `memory/context.md` for current feature metadata
   - Use git branch name if available (e.g., `001-user-authentication`)
   - Fall back to most recently created feature directory
   - If no context found, ask user to specify feature or run `/sp-pulse` first

2. **Parse arguments** and determine action:
   - If `validate`: Check plan against SDD gates
   - If `optimize`: Improve existing plan complexity
   - Otherwise: Generate new plan

3. **For `/sp-plan generate` or `/sp-plan`:**
   a. **Check for decomposition**: Look for `specs/XXX-feature/decomposition/` directory
   b. **If decomposed**:
      - Read decomposition artifacts (microservices.md, api-contracts/, interfaces/)
      - Generate separate plans for each service
      - Create integration plan for service coordination
      - Structure: `plans/XXX-feature/service-A-plan.md`, `integration-plan.md`
   c. **If not decomposed**:
      - Show existing spec files and ask user to select
      - Generate single monolithic plan
   d. **Find and validate specification** from selected spec file
   
   d. **Validation** using CLI:
      ```bash
      specpulse --no-color validate plan --verbose
      ```

   e. **Run SDD Compliance Gates**:
      - Specification First: Requirements clear and traced
      - Incremental Planning: Phased approach defined
      - Task Decomposition: Clear breakdown planned
      - Quality Assurance: Testing strategy defined
      - Architecture Documentation: Decisions recorded

   f. **Generate AI-optimized plan** by COPYING template from templates/plan.md to plans/XXX-feature/:
      ```markdown
      # Implementation Plan: {{ feature_name }}
      ## Specification Reference
      - **Spec ID**: SPEC-{{ feature_id }}
      - **Spec Version**: {{ spec_version }}
      - **Plan Version**: {{ plan_version }}
      - **Generated**: {{ date }}
      ```

   g. **Generate comprehensive sections based on architecture**:
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
      - Common sections:
        * Technology stack with performance implications
        * Testing strategy with coverage targets
        * Security considerations
        * Deployment strategy with rollback plans

   h. **Architecture documentation**:
      - Document all architectural decisions with rationale
      - Create improvement strategies for technical debt
      - Track future enhancement opportunities

   i. **CRITICAL NUMBERING LOGIC**:
      - Check if `plans/XXX-feature/plan-001.md` exists
      - If plan-001.md does NOT exist: Create plan-001.md with full content from template
      - If plan-001.md EXISTS: Create plan-002.md (or next number) with new content
      - NEVER leave plan-001.md as placeholder if it's the first plan
   j. **Write FULL plan content** to `plans/XXX-feature/plan-XXX.md`
   k. **IMPORTANT**: Can EDIT files in plans/ folder, but NEVER modify templates/, scripts/, or commands/ folders

4. **For `/sp-plan validate`:**
   a. **Show existing plan files**: List all plan-XXX.md files in current feature directory
   b. **Ask user to select**: Which plan file to validate
   c. **Validation** using script:
     ```bash
     Read: templates/plan.md
     Write: plans/XXX-feature/plan-YYY.md
     (template content + user description)

     Then READ and EXPAND with full implementation details
     ```
   d. Verify all SDD gates are addressed
   e. Check architectural decisions have proper documentation
   f. Validate test-first approach is documented
   g. Ensure integration strategy uses real services
   h. Report detailed validation results

5. **For `/sp-plan optimize`:**
   a. **Show existing plan files**: List all plan-XXX.md files in current feature directory
   b. **Ask user to select**: Which plan file to optimize
   c. **Read existing plan** from detected context and analyze complexity
   d. **Identify optimization opportunities**:
      - Module consolidation opportunities
      - Abstraction layer removal candidates
      - Simplification strategies
   e. **Generate optimization recommendations**
   f. **Create new version**: Write optimized plan as next version (plan-XXX.md)

## SDD Compliance Gates (Phase -1)

**Must pass before implementation:**

### Principle 1: Specification First
- [ ] Clear requirements documented
- [ ] User stories with acceptance criteria
- [ ] [NEEDS CLARIFICATION] markers used
- [ ] Functional and non-functional requirements

### Principle 2: Incremental Planning
- [ ] Work broken into valuable phases
- [ ] Each phase delivers working software
- [ ] Milestones and checkpoints defined
- [ ] Features prioritized by business value

### Principle 3: Task Decomposition
- [ ] Tasks are specific and actionable
- [ ] Effort estimates provided
- [ ] Definition of Done clear
- [ ] Dependencies identified

### Principle 6: Quality Assurance
- [ ] Testing strategy appropriate for project
- [ ] Acceptance criteria testable
- [ ] Code review process defined
- [ ] Quality metrics identified

### Principle 7: Architecture Documentation
- [ ] Technology choices documented
- [ ] Integration points identified
- [ ] Technical debt tracked
- [ ] Trade-offs documented

## Examples

### Generate plan for decomposed spec
```
User: /sp-plan generate
```
Detecting decomposition in `specs/001-authentication/decomposition/`...
I will create:
- `plans/001-authentication/auth-service-plan.md`
- `plans/001-authentication/user-service-plan.md`
- `plans/001-authentication/integration-plan.md`

### Generate plan for monolithic spec
```
User: /sp-plan generate
```
No decomposition found. Creating single plan:
- `plans/001-authentication/plan-001.md`

### Validate existing plan
```
User: /sp-plan validate
```
I will run comprehensive validation:
```
PLAN_FILE=plans/001-user-authentication/plan.md
SDD_GATES_STATUS=COMPLETED
MISSING_SECTIONS=0
STATUS=validation_complete
```

### Optimize plan complexity
```
User: /sp-plan optimize
```
I will analyze and recommend complexity reductions.

## Enhanced Features

- **AI-optimized templates** with Jinja2-style variables
- **Script execution** with Bash
- **SDD compliance tracking** with gate status
- **Architecture decision tracking** with rationale
- **Performance and security considerations** integrated
- **Integration-first approach** with real service usage
- **Detailed validation reporting** with specific recommendations
- **Cross-platform operation** with Bash

## Error Handling

- Specification existence validation
- SDD gate compliance checking
- Template structure validation
- Directory structure verification
- Feature context auto-discovery