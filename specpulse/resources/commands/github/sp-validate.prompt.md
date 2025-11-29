$ARGUMENTS

# GitHub Copilot SpecPulse Validation Engine

Validate specifications, plans, tasks, and tests without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-validate [target] [feature-name]    # Validate specific component
```

Targets: `spec`, `plan`, `task`, `test`, `all` (defaults to `all`)

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the validation outcome
- Only read files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/ (read-only validation)

**Implementation Steps**

1. **Parse Arguments to Determine Validation Scope**
   - If target specified: Validate only that component (spec, plan, task, test, all)
   - If feature name provided: Focus on specific feature
   - If no arguments: Validate all components in current feature
   - Parse options like --fix, --verbose, --strict

2. **Detect Current Feature Context**
   - Check .specpulse/memory/context.md for active feature
   - Look for most recently modified spec/plan/task directory
   - Validate feature directory exists and is properly structured
   - Extract feature ID and name from directory structure

3. **For Specification Validation**
   - **File Structure Validation**
     - Verify specification files exist in .specpulse/specs/[feature]/
     - Check file naming follows spec-[###].md pattern
     - Validate file permissions and readability
     - Ensure proper markdown formatting
   - **Content Structure Validation**
     - Check required sections: Executive Summary, Functional Requirements, User Stories, Acceptance Criteria, Technical Constraints, Non-Functional Requirements, Risk Assessment
   - **Content Quality Validation**
     - Count [NEEDS CLARIFICATION] markers, verify Given-When-Then format
     - Check acceptance criteria are measurable and testable
     - Validate technical constraints are specific and achievable
   - **SDD Gates Compliance**
     - Specification First, Traceable, Testable, Complete validation

4. **For Plan Validation**
   - **File Structure Validation**
     - Verify plan files exist in .specpulse/plans/[feature]/
     - Check file naming follows plan-[###].md pattern
     - Validate plan file format and readability
   - **Content Completeness Validation**
     - Verify Implementation Strategy, Phase Breakdown, Task Dependencies, Resource Requirements, Timeline Estimates, Risk Mitigation
   - **Technical Feasibility Validation**
     - Assess implementation approach complexity, validate dependency relationships
     - Check timeline estimates are realistic, verify resource requirements are achievable

5. **For Task Validation**
   - **File Structure Validation**
     - Verify task files exist in .specpulse/tasks/[feature]/
     - Check file naming follows task patterns (tasks-*.md, *-tasks.md)
     - Validate task file permissions and format
   - **Task Structure Validation**
     - Verify required fields: Task ID, Title, Status, Description, Files Touched, Success Criteria, Dependencies, Risk Assessment
   - **Task Quality Validation**
     - Check task descriptions provide clear implementation guidance
     - Verify success criteria are specific and measurable
     - Validate dependency chains are acyclic and logical
   - **Dependency Validation**
     - Verify all referenced task IDs exist, check for circular dependencies
     - Validate critical path identification, assess parallel task availability

6. **For Test Validation**
   - **Test File Discovery**
     - Locate test files in tests/features/[feature]/ directory
     - Check for proper test_*.py naming convention
     - Validate test file structure and imports
   - **Test Content Validation**
     - Verify proper imports, test functions, test coverage, test quality, test documentation
   - **Requirements Traceability**
     - Map test files to specification requirements
     - Verify user story test coverage, check acceptance criteria test implementation

7. **For Comprehensive Validation (all)**
   - **Cross-Component Consistency**
     - Verify specifications link to plans and tasks
     - Check task traceability to requirements
     - Validate test coverage of specifications
   - **Quality Metrics Calculation**
     - Calculate Specification Completeness, Plan Feasibility, Task Quality, Test Coverage, SDD Compliance
   - **Recommendations and Fixes**
     - Provide actionable recommendations for critical issues, quality improvements, missing elements

8. **Validate structure and report comprehensive validation results**

**Examples**

**Validate All Components:**
```
/sp-validate
```

Output: Comprehensive validation of specs, plans, tasks, and tests with quality metrics and recommendations.

**Validate Specifications Only:**
```
/sp-validate spec
```

Output: Detailed specification validation with SDD Gates compliance assessment.

**Validate Specific Feature:**
```
/sp-validate all 001-user-authentication
```

Output: Complete feature validation with cross-component consistency analysis.

**Validation Scopes:**
- **spec**: Specification structure, content quality, SDD compliance
- **plan**: Implementation plan feasibility and completeness
- **task**: Task structure, dependencies, quality validation
- **test**: Test coverage, requirements traceability, quality
- **all**: Comprehensive validation across all components

**Advanced Features:**
- **Quality Metrics**: Percentage scores for completeness, feasibility, coverage
- **SDD Gates Compliance**: Specification-Driven Development standards
- **Cross-Component Analysis**: Consistency across specs, plans, tasks, tests
- **Requirements Traceability**: End-to-end validation from requirements to tests
- **Risk Assessment**: Identification of blocking issues and mitigation strategies

**Validation Output:**
- File structure validation results
- Content completeness assessment
- Quality metrics and scoring
- Issues classification (Critical, Major, Minor)
- Actionable recommendations and fixes
- Readiness assessment for implementation

**Error Handling**
- Missing directories: Guide user through creating proper structure
- File permission errors: Provide permission fix instructions
- Invalid file formats: Offer template corrections
- Content quality issues: Provide section templates and clarification guidance

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Uses LLM-safe file operations for comprehensive validation
- Quality metrics and scoring for objective assessment
- SDD Gates compliance validation for specification-driven development
- Cross-component consistency analysis and requirements traceability
<!-- SPECPULSE:END -->

## Implementation Notes

When called with the specified arguments, execute the validation workflow according to the target scope. Use only read operations within the allowed directories, perform comprehensive quality analysis, and provide actionable recommendations for improvement.