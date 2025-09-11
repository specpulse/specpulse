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
   a. **Show existing spec files**: List all spec-XXX.md files in current feature directory
   b. **Ask user to select**: Which spec file to base plan on
   c. **Find and validate specification** from selected spec file
   
   d. **Enhanced validation** using cross-platform script:
      ```bash
      # Cross-platform detection
      if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
          python scripts/sp-pulse-plan.py "$FEATURE_DIR"
      else
          bash scripts/sp-pulse-plan.sh "$FEATURE_DIR" || python scripts/sp-pulse-plan.py "$FEATURE_DIR"
      fi
      ```

   e. **Run Constitutional Phase Gates** (Article VII):
      - Simplicity Gate: ≤3 modules justification
      - Anti-Abstraction Gate: Direct framework usage
      - Test-First Gate: Tests before implementation
      - Integration-First Gate: Real services over mocks
      - Research Gate: Technology choices documented

   f. **Generate AI-optimized plan** using template variables:
      ```markdown
      # Implementation Plan: {{ feature_name }}
      ## Specification Reference
      - **Spec ID**: SPEC-{{ feature_id }}
      - **Spec Version**: {{ spec_version }}
      - **Plan Version**: {{ plan_version }}
      - **Generated**: {{ date }}
      ```

   g. **Generate comprehensive sections**:
      - Technology stack with performance implications
      - Architecture overview with component relationships
      - Implementation phases with timeline estimates
      - API contracts with authentication requirements
      - Data models with validation rules
      - Testing strategy with coverage targets
      - Security considerations with compliance requirements
      - Deployment strategy with rollback plans

   h. **Complexity tracking** (Article VII):
      - Document all complexity exceptions with justifications
      - Create mitigation strategies for each exception
      - Track optimization opportunities

   i. **Version management**: Check existing plan files and create next version (plan-001.md, plan-002.md, etc.)
   j. **Write optimized plan** to `plans/XXX-feature/plan-XXX.md`

4. **For `/sp-plan validate`:**
   a. **Show existing plan files**: List all plan-XXX.md files in current feature directory
   b. **Ask user to select**: Which plan file to validate
   c. **Enhanced validation** using cross-platform script:
     ```bash
     # Cross-platform detection
     if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
         python scripts/sp-pulse-plan.py "$FEATURE_DIR"
     else
         bash scripts/sp-pulse-plan.sh "$FEATURE_DIR" || python scripts/sp-pulse-plan.py "$FEATURE_DIR"
     fi
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

### Generate plan with validation
```
User: /sp-plan generate
```
I will:
- Run: `bash scripts/sp-pulse-plan.sh "$FEATURE_DIR"`
- Validate: Constitutional gates compliance
- Create: AI-optimized plan with template variables
- Output: `CONSTITUTIONAL_GATES_STATUS=PENDING`

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
- **Cross-platform script execution** with automatic detection
- **Enhanced script integration** for Bash and Python
- **Constitutional compliance tracking** with gate status
- **Complexity exception management** with justifications
- **Performance and security considerations** integrated
- **Integration-first approach** with real service usage
- **Detailed validation reporting** with specific recommendations
- **Platform-agnostic operation** for any development environment

## Error Handling

- Specification existence validation
- Constitutional gate compliance checking
- Template structure validation
- Directory structure verification
- Feature context auto-discovery