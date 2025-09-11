---
name: plan
description: Generate or validate implementation plans using AI-optimized templates
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /plan Command

Generate implementation plans from specifications following SpecPulse methodology with constitutional compliance and AI-optimized templates.

## Usage
```
/plan [action] [feature-directory]
```

Actions: `generate`, `validate`, `optimize` (defaults to `generate`)

## Implementation

When called with `/plan $ARGUMENTS`, I will:

1. **Parse arguments** and determine action:
   - If `validate`: Check plan against constitutional gates
   - If `optimize`: Improve existing plan complexity
   - Otherwise: Generate new plan

2. **For `/plan generate` or `/plan`:**
   a. **Find and validate specification** from current context or provided directory
   
   b. **Enhanced validation** using cross-platform script:
      ```bash
      # Cross-platform detection
      if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
          powershell scripts/pulse-plan.ps1 "$FEATURE_DIR"
      else
          bash scripts/pulse-plan.sh "$FEATURE_DIR" || python scripts/pulse-plan.py "$FEATURE_DIR"
      fi
      ```

   c. **Run Constitutional Phase Gates** (Article VII):
      - Simplicity Gate: ≤3 modules justification
      - Anti-Abstraction Gate: Direct framework usage
      - Test-First Gate: Tests before implementation
      - Integration-First Gate: Real services over mocks
      - Research Gate: Technology choices documented

   d. **Generate AI-optimized plan** using template variables:
      ```markdown
      # Implementation Plan: {{ feature_name }}
      ## Specification Reference
      - **Spec ID**: SPEC-{{ feature_id }}
      - **Generated**: {{ date }}
      ```

   e. **Generate comprehensive sections**:
      - Technology stack with performance implications
      - Architecture overview with component relationships
      - Implementation phases with timeline estimates
      - API contracts with authentication requirements
      - Data models with validation rules
      - Testing strategy with coverage targets
      - Security considerations with compliance requirements
      - Deployment strategy with rollback plans

   f. **Complexity tracking** (Article VII):
      - Document all complexity exceptions with justifications
      - Create mitigation strategies for each exception
      - Track optimization opportunities

   g. **Write optimized plan** to `plans/XXX-feature/plan.md`

3. **For `/plan validate`:**
   - **Enhanced validation** using cross-platform script:
     ```bash
     # Cross-platform detection
     if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
         powershell scripts/pulse-plan.ps1 "$FEATURE_DIR"
     else
         bash scripts/pulse-plan.sh "$FEATURE_DIR" || python scripts/pulse-plan.py "$FEATURE_DIR"
     fi
     ```
   - Verify all constitutional gates are addressed
   - Check complexity exceptions have proper justifications
   - Validate test-first approach is documented
   - Ensure integration strategy uses real services
   - Report detailed validation results

4. **For `/plan optimize`:**
   - **Read existing plan** and analyze complexity
   - **Identify optimization opportunities**:
     - Module consolidation opportunities
     - Abstraction layer removal candidates
     - Simplification strategies
   - **Generate optimization recommendations**
   - **Update plan** with reduced complexity

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
User: /plan generate
```
I will:
- Run: `bash scripts/pulse-plan.sh "$FEATURE_DIR"`
- Validate: Constitutional gates compliance
- Create: AI-optimized plan with template variables
- Output: `CONSTITUTIONAL_GATES_STATUS=PENDING`

### Validate existing plan
```
User: /plan validate
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
User: /plan optimize
```
I will analyze and recommend complexity reductions.

## Enhanced Features

- **AI-optimized templates** with Jinja2-style variables
- **Cross-platform script execution** with automatic detection
- **Enhanced script integration** for Bash, PowerShell, and Python
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