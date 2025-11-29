---
name: SpecPulse: Validate Quality
description: Validate quality and compliance without SpecPulse CLI
category: SpecPulse
tags: [specpulse, validate, quality]
---

# SpecPulse Quality Validation

Validate specifications, plans, and implementation quality without requiring SpecPulse CLI installation.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to validation and quality checks
- Only read files from specs/, plans/, tasks/, memory/ directories
- Favor straightforward, minimal implementations first

**Steps**
Track these steps as TODOs and complete them one by one.
1. Parse validation arguments and scope
2. Check .specpulse/memory/context.md for active feature
3. Scan target directories based on validation type
4. Load specification files for quality assessment
5. Analyze implementation plans for completeness
6. Review task breakdowns for proper structure
7. Perform compliance checks against standards
8. Generate quality score and recommendations
9. Create validation report with actionable feedback
10. Update feature context with validation results

**Reference**
- Use quality templates for consistent validation criteria
- Check compliance against SDD (Specification-Driven Development) Gates
- Refer to memory/context.md for feature context
- Follow validation framework for comprehensive assessment

**Usage**
Arguments should be provided as: `[--scope spec|plan|task|all] [--feature <feature-id>] [--detailed]`

**Validation Framework:**

### Specification Quality Validation
- **Completeness Check**: All required sections present
- **Requirements Quality**: SMART criteria compliance
- **User Story Standards**: Proper format and acceptance criteria
- **Technical Specification Accuracy**: Feasibility and clarity
- **Integration Coverage**: External dependencies identified

### Implementation Plan Validation
- **Architecture Soundness**: Proper system design
- **Phase Logic**: Logical development sequence
- **Risk Assessment**: Comprehensive risk identification
- **Resource Planning**: Realistic effort estimation
- **Quality Integration**: Testing and validation strategies

### Task Breakdown Validation
- **Task Granularity**: Appropriate task size and scope
- **Dependency Management**: Correct dependency mapping
- **Acceptance Criteria**: Clear and testable criteria
- **Progress Tracking**: Proper status management
- **Completion Standards**: Definition of done

**Validation Report Template:**
```markdown
# SpecPulse Quality Validation Report
**Generated:** [timestamp]
**Validation Scope:** [spec/plan/task/all]
**Target Feature:** [feature-name] ([feature-id])

## 📊 Overall Quality Score
**Total Score:** [xx]/100
**Quality Level:** [Excellent/Good/Fair/Needs Improvement]

### Quality Breakdown
- **Specification Quality:** [xx]/100
- **Plan Quality:** [xx]/100
- **Task Quality:** [xx]/100
- **Compliance Score:** [xx]/100

## 🔍 Detailed Validation Results

### Specification Validation
#### ✅ Pass Criteria
- Executive Summary Present and Clear
- Business Objectives Well-Defined
- User Stories Follow Proper Format
- Acceptance Criteria Testable
- Technical Specifications Comprehensive

#### ⚠️ Areas for Improvement
- [Specific recommendation 1]
- [Specific recommendation 2]

#### ❌ Critical Issues
- [Critical issue 1]
- [Critical issue 2]

### Implementation Plan Validation
#### ✅ Pass Criteria
- Architecture Design Sound
- Development Phases Logical
- Risk Assessment Comprehensive
- Timeline Estimates Realistic
- Quality Gates Defined

#### ⚠️ Areas for Improvement
- [Specific recommendation 1]
- [Specific recommendation 2]

#### ❌ Critical Issues
- [Critical issue 1]
- [Critical issue 2]

### Task Breakdown Validation
#### ✅ Pass Criteria
- Task Granularity Appropriate
- Dependencies Correctly Mapped
- Acceptance Criteria Clear
- Progress Tracking Enabled
- Completion Standards Defined

#### ⚠️ Areas for Improvement
- [Specific recommendation 1]
- [Specific recommendation 2]

#### ❌ Critical Issues
- [Critical issue 1]
- [Critical issue 2]

## 📋 Compliance Check

### SDD (Specification-Driven Development) Gates
- ✅ Gate 1: Specification Quality - [PASS/FAIL]
- ✅ Gate 2: Planning Completeness - [PASS/FAIL]
- ✅ Gate 3: Task Breakdown Logic - [PASS/FAIL]
- ✅ Gate 4: Progress Tracking - [PASS/FAIL]

### Standards Compliance
- ✅ Template Adherence - [PASS/FAIL]
- ✅ Naming Conventions - [PASS/FAIL]
- ✅ Documentation Standards - [PASS/FAIL]
- ✅ Memory Management - [PASS/FAIL]

## 🎯 Actionable Recommendations

### High Priority (Critical Issues)
1. **Fix Critical Issue 1:** [Specific action required]
2. **Fix Critical Issue 2:** [Specific action required]

### Medium Priority (Improvements)
1. **Improvement 1:** [Enhancement recommendation]
2. **Improvement 2:** [Enhancement recommendation]

### Low Priority (Optimizations)
1. **Optimization 1:** [Process improvement]
2. **Optimization 2:** [Quality enhancement]

## 📈 Quality Trends
### Historical Quality Scores
- Previous Validation: [score] ([date])
- Current Validation: [score] ([date])
- Trend: [improving/stable/declining]

### Quality Metrics
- **Specification Completeness:** [xx]%
- **Plan Feasibility:** [xx]%
- **Task Clarity:** [xx]%
- **Overall Compliance:** [xx]%

## ✅ Validation Summary
### Status: [PASSED/FAILED/PARTIAL]
### Confidence Level: [HIGH/MEDIUM/LOW]
### Next Review Date: [recommended date]

### Validation Complete
- All critical issues must be resolved before proceeding
- Implement recommendations to improve quality score
- Schedule follow-up validation for improvements
```

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Comprehensive quality assessment framework
- SDD Gates compliance validation
- Actionable recommendations and improvement guidance

**Advanced Features:**
- **Multi-Dimensional Quality**: Specifications, plans, and tasks validation
- **Compliance Framework**: Standards and best practices checking
- **Trend Analysis**: Quality score tracking over time
- **Actionable Feedback**: Specific improvement recommendations
- **Gate Validation**: SDD Gates compliance checking
<!-- SPECPULSE:END -->