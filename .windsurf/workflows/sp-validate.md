---
description: Validate current specifications, plans, or tasks for completeness and SDD compliance
auto_execution_mode: 3
---

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the validation outcome
- READ-ONLY OPERATION: This command only validates, never modifies files

**Critical Rules**
- **PRIMARY**: Use `specpulse validate <target>` when available
- **FALLBACK**: File Operations only if CLI fails
- **READ-ONLY VALIDATION**: This command never modifies any files
- **PROTECTED DIRECTORIES**: All directories are read-only during validation

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse validation target**:
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
   - **Check dependencies mapped** correctly
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
```
/sp-validate                  # Validate current spec
/sp-validate spec             # Validate specifications
/sp-validate plan             # Validate plans
/sp-validate task             # Validate tasks
/sp-validate all              # Validate everything
```

**Validation Scoring**

**Status Indicators:**
- ✓ **Complete**: All requirements met, ready for next phase
- ⚠ **Partial**: Mostly complete, minor issues to address
- ✗ **Incomplete**: Significant issues, needs work before proceeding
- 🚫 **Blocked**: Critical blockers prevent progress

**Validation Categories:**

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
```
/sp-validate
```
Output:
```
## ✓ Specification Validation Results

**File**: specs/001-user-authentication/spec-001.md
**Status**: Complete ✓

### Validation Summary
- **Sections**: 12/12 complete ✓
- **Clarifications**: 0 needed ✓
- **Acceptance Criteria**: 8 defined ✓
- **User Stories**: 5 provided ✓
- **SDD Compliance**: Full ✓

### Quality Metrics
- **Requirements Clarity**: High
- **Testability**: Excellent
- **Completeness**: 100%

### Next Steps
✓ Ready for /sp-plan
```

**Validate with issues:**
```
/sp-validate spec
```
Output:
```
## ⚠ Specification Validation Results

**File**: specs/002-payment-processing/spec-001.md
**Status**: Partial ⚠

### Issues Found
- **Missing Sections**: Technical Constraints, Performance Requirements
- **Clarifications Needed**: 3 [NEEDS CLARIFICATION] markers
- **User Stories**: Only 3, expected 5-7
- **Acceptance Criteria**: 4 need Given-When-Then format

### Required Actions
1. Add Technical Constraints section
2. Address 3 clarification points:
   - Payment gateway provider selection
   - Transaction timeout requirements
   - Compliance standards (PCI DSS)
3. Add 2 more user stories for edge cases
4. Fix 4 acceptance criteria to use Given-When-Then format

### Recommendations
- Use /sp-clarify to resolve [NEEDS CLARIFICATION] markers
- Review similar specifications for reference
- Consider stakeholder review for missing sections

### Next Steps
⚠ Complete missing sections, then re-run validation
```

**Validate plan:**
```
/sp-validate plan
```
Output:
```
## ✓ Plan Validation Results

**File**: plans/001-user-authentication/plan-001.md
**Status**: Complete ✓

### Validation Summary
- **Architecture Decisions**: 8 documented ✓
- **Phases Defined**: 5 logical phases ✓
- **Task Dependencies**: Clear mapping ✓
- **Testing Strategy**: Comprehensive ✓
- **SDD Gates**: All passed ✓

### Architecture Quality
- **Decision Rationale**: Clear for all choices
- **Trade-offs**: Properly documented
- **Integration Points**: Well defined

### Next Steps
✓ Ready for /sp-task
```

**Validate tasks:**
```
/sp-validate task
```
Output:
```
## ⚠ Task Validation Results

**File**: tasks/001-user-authentication/task-001.md
**Status**: Partial ⚠

### Task Analysis
- **Total Tasks**: 25
- **Completed**: 15 (60%)
- **In Progress**: 3
- **Blocked**: 2
- **Pending**: 5

### Issues Found
- **Blocked Tasks**: 2 blockers need resolution
- **Missing Dependencies**: T020 has undefined dependency
- **Unclear Acceptance**: 3 tasks need clearer criteria

### Blockers
1. **T004**: Authentication bug waiting for security review
2. **T015**: Database schema waiting for DBA approval

### Required Actions
1. Resolve T004 and T015 blockers
2. Define T020 dependency
3. Clarify acceptance criteria for T012, T018, T023

### Progress Report
- **Current Phase**: Phase 2 (Core Features) - 75% complete
- **Estimated Completion**: 3 days (if blockers resolved)
- **Velocity**: 2.5 tasks/day

### Next Steps
⚠ Resolve blockers, then continue with /sp-execute
```

**Validate all components:**
```
/sp-validate all
```
Output:
```
## 🚫 Full Project Validation Results

### Overview
**Project**: user-authentication
**Overall Status**: Blocked 🚫

### Component Status
- **Specification**: Complete ✓
- **Plan**: Complete ✓
- **Tasks**: Partial ⚠ (2 blockers)

### Blockers Impact
**Critical Issue**: 2 blocked tasks preventing progress
- **T004**: Security review required
- **T015**: Database schema approval needed

### Recommendations
1. **Priority 1**: Resolve T004 security review
2. **Priority 2**: Get database schema approval
3. **Continue**: Unblocked parallel tasks

### Overall Assessment
- **Quality**: High (spec and plan excellent)
- **Progress**: Good (60% tasks complete)
- **Risk**: Medium (2 critical blockers)

### Action Plan
1. Schedule security review for T004
2. Follow up with DBA on T015
3. Continue with unblocked tasks
4. Re-validate after blockers resolved
```

**CLI Integration**

**Try CLI First:**
```bash
specpulse validate spec --verbose
specpulse validate plan
specpulse validate task
specpulse validate all
```

**Fallback to Manual Validation if CLI Fails:**
1. Read component files manually
2. Check required sections and structure
3. Validate SDD compliance
4. Generate validation report

**Advanced Validation Features**

**Cross-Component Validation:**
- Specification → Plan consistency
- Plan → Tasks traceability
- Dependency conflict detection
- Workflow progression validation

**Quality Metrics:**
- Completeness percentage
- Clarity score
- Testability assessment
- SDD compliance rating

**Integration Scenarios:**

**CI/CD Pipeline Integration:**
```
specpulse validate all
if [ $? -eq 0 ]; then
  echo "Validation passed, proceeding with deployment"
else
  echo "Validation failed, check report"
  exit 1
fi
```

**Pre-commit Hooks:**
```bash
#!/bin/sh
# Pre-commit validation hook
specpulse validate spec
specpulse validate plan
```

**Error Handling**

**Validation Errors:**
- File not found: Suggest creating missing component
- Parse errors: Report specific syntax issues
- Inconsistent data: Highlight conflicts
- Missing dependencies: Show dependency graph

**Recovery Strategies:**
- Auto-suggest fixes for common issues
- Provide templates for missing sections
- Generate dependency lists
- Create validation checklists

**Reference**
- Use `specpulse validate --help` if you need additional CLI options
- Check `memory/context.md` for current component context
- Run `specpulse doctor` if you encounter system issues
- Use `/sp-status` for overall project health
- This command is READ-ONLY - it never modifies files
<!-- SPECPULSE:END -->