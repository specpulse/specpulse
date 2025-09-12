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

Generate implementation plans from specifications following SpecPulse methodology with constitutional compliance and AI-optimized templates.

## CRITICAL: File Edit Restrictions
- **NEVER EDIT**: templates/, scripts/, commands/, .claude/, .gemini/
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
   - If `validate`: Check plan against constitutional gates
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
   
   d. **Validation** using script:
      ```bash
      bash scripts/sp-pulse-plan.sh "$FEATURE_DIR"
      ```

   e. **Run Constitutional Phase Gates** (Article VII):
      - Simplicity Gate: ≤3 modules justification
      - Anti-Abstraction Gate: Direct framework usage
      - Test-First Gate: Tests before implementation
      - Integration-First Gate: Real services over mocks
      - Research Gate: Technology choices documented

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

   h. **Complexity tracking** (Article VII):
      - Document all complexity exceptions with justifications
      - Create mitigation strategies for each exception
      - Track optimization opportunities

   i. **Version management**: Check existing plan files and create next version (plan-001.md, plan-002.md, etc.)
   j. **Write NEW plan file** to `plans/XXX-feature/plan-XXX.md`
   k. **IMPORTANT**: Can EDIT files in plans/ folder, but NEVER modify templates/, scripts/, or commands/ folders

4. **For `/sp-plan validate`:**
   a. **Show existing plan files**: List all plan-XXX.md files in current feature directory
   b. **Ask user to select**: Which plan file to validate
   c. **Validation** using script:
     ```bash
     bash scripts/sp-pulse-plan.sh "$FEATURE_DIR"
     ```
   d. Verify all constitutional gates are addressed
   e. Check complexity exceptions have proper justifications
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

## Constitutional Phase Gates (Phase -1)

**Must pass before implementation:**

### Article VII: Simplicity Gate
- [ ] Using ≤3 projects/modules for initial implementation
- [ ] No future-proofing without documented need
- [ ] Direct framework usage (no unnecessary wrappers)
- [ ] Single model representation per concept

### Article VII: Anti-Abstraction Gate  
- [ ] Using framework features directly
- [ ] No unnecessary abstraction layers
- [ ] Clear, simple interfaces
- [ ] Avoiding premature optimization

### Article III: Test-First Gate
- [ ] Test specifications written
- [ ] Tests reviewed and approved
- [ ] Tests confirmed to FAIL before implementation
- [ ] TDD cycle planned (Red-Green-Refactor)

### Article VIII: Integration-First Gate
- [ ] Contract tests defined
- [ ] Using real services over mocks
- [ ] Production-like test environment planned
- [ ] End-to-end test scenarios identified

### Article VI: Research Gate
- [ ] Library options researched
- [ ] Performance implications documented
- [ ] Security considerations analyzed
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
CONSTITUTIONAL_GATES_STATUS=COMPLETED
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
- **Constitutional compliance tracking** with gate status
- **Complexity exception management** with justifications
- **Performance and security considerations** integrated
- **Integration-first approach** with real service usage
- **Detailed validation reporting** with specific recommendations
- **Cross-platform operation** with Bash

## Error Handling

- Specification existence validation
- Constitutional gate compliance checking
- Template structure validation
- Directory structure verification
- Feature context auto-discovery