---
description: Validate current specifications, plans, or tasks for completeness and SDD compliance.
---

$ARGUMENTS
<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the validation outcome
- READ-ONLY OPERATION: This command only validates, never modifies any files

**Critical Rules**
- **PRIMARY**: Use `specpulse validate <target>` when available
- **FALLBACK**: File Operations only if CLI fails
- **READ-ONLY VALIDATION**: This command never modifies any files
- **PROTECTED DIRECTORIES**: All directories are read-only during validation

**Steps**
Track these steps as TODOs and complete them one by one.
1. **Parse arguments** from $ARGUMENTS to determine validation target:
   - If `spec`: Validate specifications
   - If `plan`: Validate plans
   - If `task`: Validate tasks
   - If `all`: Validate everything
   - If no argument: Default to current spec
2. **Try CLI First**:
   ```bash
   specpulse validate spec --verbose
   specpulse validate plan
   specpulse validate task
   specpulse validate all
   ```
   If CLI succeeds, STOP HERE.
3. **For spec validation** (if CLI fails):
   - **Read current spec file**: Detect from context or list available specs
   - **Check required sections present**:
     * Executive Summary
     * Problem Statement
     * Functional Requirements
     * User Stories
     * Acceptance Criteria
     * Technical Constraints
   - **Count `[NEEDS CLARIFICATION]` markers**
   - **Verify Given-When-Then format** in acceptance criteria
   - **Check SDD compliance indicators**
4. **For plan validation** (if CLI fails):
   - **Read plan file**: Detect from context or list available plans
   - **Check phases defined** and logical flow
   - **Verify task breakdown exists** with proper structure
   - **Validate architecture decisions** with rationale
   - **Verify testing strategy** is comprehensive
5. **For task validation** (if CLI fails):
   - **Read task files**: Detect from context or list available tasks
   - **Check status fields present** and consistent
   - **Verify dependencies listed** accurately
   - **Check acceptance criteria** are testable
   - **Validate task priority** and estimates
   - **Check SDD gates compliance**
6. **For all validation**:
   - Run complete validation across all components
   - Check cross-component consistency
   - Validate workflow progression
   - Verify integration points
7. **Generate comprehensive validation report**:
   - Show validation status (✓ or ✗)
   - List missing sections
   - Count clarifications needed
   - Highlight blockers and issues
   - Suggest fixes
   - Recommend next steps

**Usage**
Arguments should be provided as: `[target]`

Targets: `spec`, `plan`, `task`, `all` (defaults to current spec)

**Validation Scoring**

**Status Indicators:**
- ✓ **Complete**: All requirements met, ready for next phase
- ⚠ **Partial**: Mostly complete, minor issues to address
- ✗ **Incomplete**: Significant issues, needs work before proceeding
- 🚫 **Blocked**: Critical blockers prevent progress

**Validation Categories**

**Specification Validation:**
- **Content Completeness**: All required sections present
- **Quality Metrics**: Clear requirements, testable criteria
- **SDD Compliance**: Specification First principle satisfied
- **Clarity Score**: Number of [NEEDS CLARIFICATION] markers

**Plan Validation:**
- **Structure Integrity**: Logical phases and dependencies
- **Architecture Documentation**: Clear decision rationale
- **Task Decomposition**: Proper breakdown into manageable units
- **Integration Strategy**: Clear coordination approach

**Task Validation:**
- **Task Definition**: Clear descriptions and acceptance criteria
- **Dependency Management**: Accurate dependency mapping
- **Progress Tracking**: Consistent status updates
- **Quality Gates**: SDD compliance satisfied

**Examples**

**Validate current spec (success):**
Input: No arguments or `spec`
Output: Specification validation results showing completion status.

**Validate with issues:**
Input: `spec`
Output: Validation report with missing sections and required actions.

**Validate all components:**
Input: `all`
Output: Comprehensive validation across specs, plans, and tasks.

**Reference**
- Use `specpulse validate --help` if you need additional CLI options
- Check `memory/context.md` for current component context
- Run `specpulse doctor` if you encounter system issues
- Use `/sp-status` for overall project health
- This command is READ-ONLY - it never modifies files
<!-- SPECPULSE:END -->