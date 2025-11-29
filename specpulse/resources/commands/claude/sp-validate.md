---
name: sp-validate
description: Validate specifications, plans, tasks, and tests without SpecPulse CLI
allowed_tools:
  - Read
  - Bash
  - TodoWrite
  - Grep
  - Edit
---

# /sp-validate Command

Validate specifications, plans, tasks, and tests without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-validate [target] [feature-name]    # Validate specific component
```

Targets: `spec`, `plan`, `task`, `test`, `all` (defaults to `all`)

## Implementation

When called with `/sp-validate {{args}}`, I will:

### 1. Parse Arguments to Determine Validation Scope

**I will analyze the arguments:**
- If target specified: Validate only that component (spec, plan, task, test, all)
- If feature name provided: Focus on specific feature
- If no arguments: Validate all components in current feature
- Parse options like `--fix`, `--verbose`, `--strict`

### 2. Detect Current Feature Context

**I will identify the current working feature:**
- Check `.specpulse/memory/context.md` for active feature
- Look for most recently modified spec/plan/task directory
- Validate feature directory exists and is properly structured
- Extract feature ID and name from directory structure

### 3. For Specification Validation

**I will perform comprehensive specification analysis:**

#### A. File Structure Validation
- Verify specification files exist in `.specpulse/specs/[feature]/`
- Check file naming follows `spec-[###].md` pattern
- Validate file permissions and readability
- Ensure proper markdown formatting

#### B. Content Structure Validation
Check all required sections are present:
- **Executive Summary**: Problem statement and solution overview ✓
- **Functional Requirements**: Detailed feature specifications ✓
- **User Stories**: Given-When-Then format scenarios ✓
- **Acceptance Criteria**: Testable completion conditions ✓
- **Technical Constraints**: Performance and security requirements ✓
- **Non-Functional Requirements**: Usability and maintainability ✓
- **Risk Assessment**: Potential risks and mitigation strategies ✓

#### C. Content Quality Validation
- Count and analyze `[NEEDS CLARIFICATION]` markers
- Verify Given-When-Then format in user stories
- Check acceptance criteria are measurable and testable
- Validate technical constraints are specific and achievable
- Assess risk assessment completeness and mitigation strategies

#### D. SDD Gates Compliance
- **Specification First**: Verify requirements precede implementation
- **Traceable**: Ensure each requirement maps to user stories
- **Testable**: Confirm acceptance criteria can be verified
- **Complete**: Check all necessary sections for implementation

### 4. For Plan Validation

**I will analyze implementation plans:**

#### A. File Structure Validation
- Verify plan files exist in `.specpulse/plans/[feature]/`
- Check file naming follows `plan-[###].md` pattern
- Validate plan file format and readability
- Ensure proper markdown structure

#### B. Content Completeness Validation
Verify plan contains:
- **Implementation Strategy**: High-level approach and methodology
- **Phase Breakdown**: Structured implementation phases
- **Task Dependencies**: Dependency mapping and critical path
- **Resource Requirements**: Tools, libraries, and external dependencies
- **Timeline Estimates**: Realistic timeframes for each phase
- **Risk Mitigation**: Implementation risks and mitigation strategies

#### C. Technical Feasibility Validation
- Assess implementation approach complexity
- Validate dependency relationships are logical
- Check timeline estimates are realistic
- Verify resource requirements are achievable
- Identify potential implementation bottlenecks

### 5. For Task Validation

**I will validate task breakdowns:**

#### A. File Structure Validation
- Verify task files exist in `.specpulse/tasks/[feature]/`
- Check file naming follows task patterns (`tasks-*.md`, `*-tasks.md`)
- Validate task file permissions and format
- Ensure proper YAML frontmatter structure

#### B. Task Structure Validation
For each task, verify required fields:
- **Task ID**: Unique identifier with proper formatting
- **Title**: Clear, actionable task description
- **Status**: Valid status (todo, in-progress, blocked, done)
- **Description**: Detailed implementation guidance
- **Files Touched**: List of files to be modified
- **Success Criteria**: Testable completion conditions
- **Dependencies**: List of prerequisite tasks
- **Risk Assessment**: Risk level and mitigation notes

#### C. Task Quality Validation
- Check task descriptions provide clear implementation guidance
- Verify success criteria are specific and measurable
- Validate dependency chains are acyclic and logical
- Assess risk levels match task complexity
- Check MOSCOW categorization is appropriate

#### D. Dependency Validation
- Verify all referenced task IDs exist
- Check for circular dependencies
- Validate critical path identification
- Assess parallel task availability
- Ensure dependency chains are complete

### 6. For Test Validation

**I will analyze test coverage and structure:**

#### A. Test File Discovery
- Locate test files in `tests/features/[feature]/` directory
- Check for proper `test_*.py` naming convention
- Validate test file structure and imports
- Ensure test files are executable

#### B. Test Content Validation
For each test file, verify:
- **Proper Imports**: pytest, unittest, or other testing framework
- **Test Functions**: Adequate test function coverage
- **Test Coverage**: Tests align with requirements and user stories
- **Test Quality**: Clear assertions and edge case handling
- **Test Documentation**: Descriptive test names and docstrings

#### C. Requirements Traceability
- Map test files to specification requirements
- Verify user story test coverage
- Check acceptance criteria test implementation
- Identify gaps in test coverage
- Validate test completeness

### 7. For Comprehensive Validation (all)

**I will perform complete feature validation:**

#### A. Cross-Component Consistency
- Verify specifications link to plans and tasks
- Check task traceability to requirements
- Validate test coverage of specifications
- Ensure implementation plan completeness
- Assess overall project coherence

#### B. Quality Metrics Calculation
Calculate comprehensive quality scores:
- **Specification Completeness**: Percentage of required sections present
- **Plan Feasibility**: Assessment of implementation approach
- **Task Quality**: Task structure and dependency validation
- **Test Coverage**: Requirements traceability and test completeness
- **SDD Compliance**: Overall Specification-Driven Development adherence

#### C. Recommendations and Fixes
Provide actionable recommendations:
- **Critical Issues**: Must-fix items blocking implementation
- **Quality Improvements**: Enhancements for better development experience
- **Missing Elements**: Components that need to be added
- **Optimization Opportunities**: Areas for improvement and refinement

## Validation Output Formats

### Specification Validation Results
```
🔍 Specification Validation: 001-user-authentication
================================================================

📄 Files Analyzed: 2
   ✅ spec-001.md - User Registration (Readable)
   ✅ spec-002.md - Authentication Flow (Readable)

📋 Structure Validation
   ✅ Executive Summary: Present and complete
   ✅ Functional Requirements: 8 requirements defined
   ✅ User Stories: 6 stories in Given-When-Then format
   ✅ Acceptance Criteria: 24 criteria defined
   ✅ Technical Constraints: 5 constraints specified
   ✅ Non-Functional Requirements: 3 requirements defined
   ⚠️  Risk Assessment: Present but incomplete

📊 Content Quality
   ✅ Clarification Markers: 0 (resolved)
   ✅ User Story Format: All follow Given-When-Then pattern
   ✅ Acceptance Criteria: All are measurable and testable
   ✅ Technical Constraints: Specific and achievable
   ⚠️  Risk Mitigation: 2 risks lack mitigation strategies

🛡️  SDD Gates Compliance
   ✅ Specification First: 100% (requirements precede implementation)
   ✅ Traceable: 95% (requirements mapped to user stories)
   ✅ Testable: 100% (acceptance criteria are verifiable)
   ✅ Complete: 90% (minor gaps in risk assessment)

📈 Overall Score: 93% (Excellent)
⚠️  Issues Requiring Attention: 1
🎯 Recommended Actions:
   1. Complete risk assessment with mitigation strategies
   2. Consider adding performance requirements
```

### Plan Validation Results
```
🏗️  Plan Validation: 001-user-authentication
================================================================

📄 Files Analyzed: 1
   ✅ plan-001.md - Implementation Strategy (Readable)

📋 Structure Validation
   ✅ Implementation Strategy: Clear and comprehensive
   ✅ Phase Breakdown: 5 phases defined with timelines
   ✅ Task Dependencies: Mapped and validated
   ✅ Resource Requirements: Specified and achievable
   ✅ Timeline Estimates: Realistic and detailed
   ⚠️  Risk Mitigation: Present but needs enhancement

🔍 Technical Feasibility Analysis
   ✅ Implementation Approach: Sound and achievable
   ✅ Dependency Logic: No circular dependencies detected
   ✅ Timeline Realism: Estimates align with task complexity
   ✅ Resource Availability: All requirements are obtainable
   ⚠️  Bottleneck Identification: Phase 2 may need parallelization

📊 Quality Metrics
   Implementation Clarity: 90%
   Dependency Accuracy: 95%
   Timeline Realism: 85%
   Risk Assessment: 70%

🎯 Recommendations:
   1. Enhance risk mitigation strategies
   2. Consider parallel execution for Phase 2 tasks
   3. Add contingency buffers for critical path items
```

### Task Validation Results
```
📋 Task Validation: 001-user-authentication
================================================================

📄 Files Analyzed: 1
   ✅ auth-service-tasks.md (25 tasks)

📊 Task Structure Analysis
   ✅ Task IDs: All unique and properly formatted
   ✅ Task Titles: Clear and actionable
   ✅ Task Descriptions: Provide implementation guidance
   ✅ Success Criteria: Specific and measurable
   ✅ File Dependencies: Properly mapped
   ⚠️  Risk Assessment: 3 tasks missing risk analysis

🔗 Dependency Validation
   ✅ Task References: All dependencies exist
   ✅ Circular Dependencies: None detected
   ✅ Critical Path: Properly identified
   ✅ Parallel Tasks: 8 tasks can run in parallel
   ✅ Sequential Chains: 3 dependency chains identified

📈 Quality Metrics
   Task Completeness: 88%
   Dependency Accuracy: 100%
   Risk Assessment Coverage: 76%
   MOSCOW Categorization: 96%

⚠️  Issues Found: 3
   1. T007: Missing risk assessment for OAuth integration
   2. T015: High-risk task lacks mitigation strategy
   3. T021: Unclear success criteria for error handling

🎯 Recommended Actions:
   1. Complete risk assessments for identified tasks
   2. Clarify success criteria for complex tasks
   3. Add risk mitigation strategies for high-risk items
```

### Test Validation Results
```
🧪 Test Validation: 001-user-authentication
================================================================

📄 Test Files Analyzed: 3
   ✅ test_user_registration.py (8 test functions)
   ✅ test_authentication_flow.py (12 test functions)
   ✅ test_token_validation.py (6 test functions)

📋 Test Structure Validation
   ✅ Test Imports: Proper pytest framework usage
   ✅ Test Functions: All follow naming convention
   ✅ Test Documentation: Descriptive names and docstrings
   ✅ Test Quality: Clear assertions and edge cases
   ✅ Test Organization: Logical grouping and structure

🔗 Requirements Traceability
   ✅ User Story Coverage: 6/6 stories tested
   ✅ Acceptance Criteria Coverage: 22/24 criteria tested
   ⚠️  Missing Tests: 2 acceptance criteria not covered
   ✅ Edge Case Coverage: Critical paths tested
   ✅ Error Handling: Failure scenarios addressed

📊 Coverage Metrics
   User Story Test Coverage: 100%
   Acceptance Criteria Coverage: 92%
   Edge Case Coverage: 85%
   Error Handling Coverage: 90%

⚠️  Gaps Identified:
   1. Missing test for password reset email delivery
   2. No test for account lockout after failed attempts

🎯 Recommended Actions:
   1. Add tests for missing acceptance criteria
   2. Enhance edge case coverage for authentication flows
   3. Add performance tests for token validation
```

### Comprehensive Validation Report
```
📊 Complete Feature Validation: 001-user-authentication
================================================================

🎯 Overall Quality Score: 91% (Excellent)

📋 Component Summary
   ✅ Specifications: 93% (2 files)
   ✅ Plans: 85% (1 file)
   ✅ Tasks: 88% (1 file, 25 tasks)
   ✅ Tests: 90% (3 files, 26 test functions)

🛡️  SDD Gates Compliance
   ✅ Specification First: 100%
   ✅ Traceable: 95%
   ✅ Testable: 92%
   ✅ Complete: 89%

⚠️  Issues Requiring Attention (6 total)
   Critical: 0
   Major: 2 (Risk assessment, Test coverage gaps)
   Minor: 4 (Documentation, Minor format issues)

🎯 Recommended Priority Actions
   1. Complete risk assessment in specifications and tasks
   2. Add missing test coverage for 2 acceptance criteria
   3. Enhance plan risk mitigation strategies
   4. Clarify success criteria for complex tasks

🚀 Readiness Assessment
   ✅ Ready for implementation with minor improvements
   🎯 Address 2 major items for production readiness
```

## Error Handling and Recovery

### Common Validation Issues

#### File Structure Problems
- **Missing directories**: Guide user through creating proper structure
- **File permission errors**: Provide permission fix instructions
- **Invalid file formats**: Offer template corrections
- **Corrupted files**: Suggest recovery procedures

#### Content Quality Issues
- **Missing required sections**: Provide section templates
- **Vague requirements**: Guide through clarification process
- **Untestable criteria**: Help refine acceptance criteria
- **Complex dependencies**: Suggest dependency simplification

#### Validation Process Errors
- **Memory constraints**: Process files in batches
- **Time limits**: Prioritize critical validations
- **Access restrictions**: Provide alternative validation approaches
- **System errors**: Implement retry mechanisms

This `/sp-validate` command provides **comprehensive validation** of all project components without requiring any SpecPulse CLI installation, using only validated file operations and detailed quality analysis.