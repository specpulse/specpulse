# Specification: Validation Feedback Improvements

## Metadata
- **ID**: SPEC-003
- **Created**: 2025-10-06
- **Author**: SpecPulse Development Team
- **AI Assistant**: Claude Code
- **Version**: 1.0.0

## Executive Summary
Enhance SpecPulse's validation system to provide actionable, LLM-friendly feedback that guides users through fixing validation issues. This feature transforms cryptic validation errors into clear, example-rich guidance with auto-fix suggestions, supports progressive validation for incomplete specs, and enables project-specific validation rules based on context.

## Problem Statement
Current validation in SpecPulse has several critical issues:
1. **Cryptic error messages**: Validation says "Missing section X" but LLMs don't know what content to generate
2. **Binary validation**: Specs either pass or fail; no support for partial/incomplete specs during development
3. **Generic validation**: Same rules apply to all projects regardless of type, tech stack, or requirements
4. **No actionable guidance**: LLMs receive errors but no examples, suggestions, or auto-fix options

These issues slow down spec creation, force users to interpret validation errors manually, and prevent incremental spec-building workflows.

## Proposed Solution
Implement a three-component validation enhancement system:

1. **Actionable Validation Messages** (Component 3.1): Transform error messages into guidance with examples, suggestions, and auto-fix commands
2. **Partial Validation** (Component 3.2): Support progressive validation showing completion status and next suggested sections
3. **Context-Based Validation Rules** (Component 3.3): Enable project-specific validation rules based on project type and tech stack

## Detailed Requirements

### Functional Requirements

FR-001: Actionable Validation Error Messages
  - Acceptance: Each validation error includes: what it means, example, suggestion, and help command
  - Priority: MUST

FR-002: Auto-Fix Command for Common Issues
  - Acceptance: `specpulse validate 001 --fix` adds missing template sections automatically
  - Priority: MUST

FR-003: Validation Examples Database
  - Acceptance: YAML file contains examples for each validation rule
  - Priority: MUST

FR-004: Partial Validation Mode
  - Acceptance: `specpulse validate 001 --partial` shows completion percentage and progress
  - Priority: MUST

FR-005: Section Status Indicators
  - Acceptance: Validation output shows ✓ complete, ⚠️ partial, ⭕ missing for each section
  - Priority: MUST

FR-006: Next Section Suggestions
  - Acceptance: Partial validation suggests which section to work on next
  - Priority: SHOULD

FR-007: Custom Validation Rules
  - Acceptance: `.specpulse/validation_rules.yaml` allows project-specific rules
  - Priority: MUST

FR-008: Rule Enable/Disable Control
  - Acceptance: CLI commands to enable, disable, list custom validation rules
  - Priority: SHOULD

FR-009: Project Type Detection
  - Acceptance: Validation rules adapt based on detected project type (web-app, api, mobile-app, etc.)
  - Priority: SHOULD

FR-010: Validation Rule Templates
  - Acceptance: Users can create custom rules using provided templates
  - Priority: COULD

### Non-Functional Requirements

#### Performance
- Response Time: Validation should complete in <2 seconds for typical specs
- Throughput: Support validation of 100+ specs in batch mode
- Resource Usage: Memory usage <50MB for validation operations

#### Security
- Authentication: Not applicable (local CLI tool)
- Authorization: File system permissions control access
- Data Protection: No sensitive data in validation rules or examples

#### Scalability
- User Load: Single-user CLI tool
- Data Volume: Support specs up to 10,000 lines
- Geographic Distribution: Not applicable (local tool)

## User Stories

### Story 1: LLM Receives Actionable Error Messages
**As a** LLM (Claude/Gemini) using SpecPulse
**I want** validation errors that include examples and suggestions
**So that** I know exactly what content to generate to fix the issue

**Acceptance Criteria:**
- [ ] Error message explains what the missing/invalid section means
- [ ] Error includes a concrete example of valid content
- [ ] Error suggests specific action to take (with command if applicable)
- [ ] Error includes help command for more information

### Story 2: Auto-Fix Common Validation Issues
**As a** solo developer
**I want** automatic fixes for common validation issues
**So that** I can quickly add missing template sections without manual work

**Acceptance Criteria:**
- [ ] `--fix` flag available on validate command
- [ ] Missing sections are added with template placeholders
- [ ] Auto-fix creates backup before making changes
- [ ] Auto-fix reports what was changed

### Story 3: Validate Incomplete Specs
**As a** solo developer building specs incrementally
**I want** validation to show progress on partial specs
**So that** I can validate work-in-progress without errors blocking me

**Acceptance Criteria:**
- [ ] `--partial` flag enables progressive validation mode
- [ ] Output shows completion percentage (0-100%)
- [ ] Each section shows status: complete, partial, or missing
- [ ] Validation suggests next section to work on

### Story 4: Project-Specific Validation Rules
**As a** solo developer working on a web application
**I want** validation rules specific to web apps
**So that** I'm reminded to include security, accessibility, and performance requirements

**Acceptance Criteria:**
- [ ] Validation rules file supports project type filtering
- [ ] Rules can be enabled/disabled per project
- [ ] Custom error messages for project-specific rules
- [ ] CLI commands to manage validation rules

### Story 5: LLM-Parseable Validation Output
**As a** LLM processing validation results
**I want** structured, consistent validation output
**So that** I can parse errors and generate appropriate fixes

**Acceptance Criteria:**
- [ ] Validation output follows consistent format
- [ ] Errors are grouped by section
- [ ] Suggestions are clearly marked
- [ ] Optional JSON output mode for machine parsing

## Technical Constraints

1. **Backward Compatibility**: Existing validation must continue to work; new features are opt-in
2. **Performance**: Validation enhancements must not slow down existing validation by >10%
3. **File Format**: Validation rules must use YAML for consistency with project config
4. **CLI Integration**: All validation features accessible via CLI commands and flags
5. **Template System**: Validation examples must use same template system as specs
6. **Cross-Platform**: Validation must work on Windows, macOS, and Linux

## Dependencies

- Existing `specpulse/core/validator.py` module
- YAML parsing library (PyYAML)
- Template rendering system (Jinja2)
- Rich library for formatted CLI output
- Project context system (from v1.7.0)

## Risks and Mitigations

**Risk 1: Validation Rules Too Strict**
- Mitigation: Make custom rules opt-in; provide disable/enable controls
- Mitigation: Include escape hatch for projects that need flexibility

**Risk 2: Auto-Fix Breaks Existing Content**
- Mitigation: Always create backups before auto-fix
- Mitigation: Make auto-fix conservative (only add, never modify existing content)
- Mitigation: Show diff of changes before applying

**Risk 3: Performance Degradation**
- Mitigation: Cache validation examples in memory
- Mitigation: Make partial validation lightweight (skip expensive checks)
- Mitigation: Add benchmarking tests to CI/CD

**Risk 4: Examples Become Outdated**
- Mitigation: Store examples in YAML (easy to update)
- Mitigation: Version validation examples database
- Mitigation: Add validation for examples file itself

## Success Criteria

- [ ] All 10 functional requirements implemented and tested
- [ ] LLMs receive actionable feedback on validation errors
- [ ] Partial validation supports incremental spec building
- [ ] Custom validation rules work for web-app, api, and mobile-app project types
- [ ] Backward compatibility: existing validation continues to work
- [ ] Performance: validation completes in <2 seconds
- [ ] Test coverage: >90% for new validation code
- [ ] Documentation: validation examples file includes 15+ examples

## Implementation Components

### Component 3.1: Actionable Validation Messages

**Files to Modify/Create:**
- `specpulse/core/validator.py` (+150 lines for enhanced feedback)
- `specpulse/resources/validation_examples.yaml` (new file, ~200 lines)
- `specpulse/utils/template_parser.py` (+50 lines for example extraction)

**Key Features:**
- Enhanced error messages with "What this means", "Example", "Suggestion", "Quick fix"
- Validation examples YAML structure:
  ```yaml
  missing_acceptance_criteria:
    message: "Missing: Acceptance Criteria"
    meaning: "Acceptance criteria define when the feature is 'done'"
    example: |
      ✓ User can login with email/password
      ✓ Invalid credentials show error message
      ✓ Successful login redirects to dashboard
    suggestion: "Add a section '## Acceptance Criteria' with 3-5 testable conditions"
    help_command: "specpulse help acceptance-criteria"
    auto_fix: true
  ```

**CLI Commands:**
- `specpulse validate 001` - Enhanced output with examples
- `specpulse validate 001 --fix` - Auto-add missing sections
- `specpulse help <topic>` - Show detailed help for validation topics

### Component 3.2: Partial Validation (Progressive)

**Files to Modify/Create:**
- `specpulse/core/validator.py` (+100 lines for partial mode)
- `specpulse/utils/progress_calculator.py` (new, ~80 lines)

**Key Features:**
- Progress tracking: completion percentage based on required sections
- Section status indicators: ✓ complete, ⚠️ partial (needs more items), ⭕ missing
- Smart suggestions for next section based on spec phase
- Output format:
  ```
  Progress: 40% complete

  ✓ Executive Summary (complete)
  ✓ Problem Statement (complete)
  ⚠️ Requirements (2 items - consider adding 1-2 more)
  ⭕ User Stories (not started)
  ⭕ Acceptance Criteria (not started)

  Next suggested section: User Stories
  ```

**CLI Commands:**
- `specpulse validate 001 --partial` - Progressive validation mode
- `specpulse validate 001 --progress` - Show just completion percentage

### Component 3.3: Validation Rules from Project Context

**Files to Modify/Create:**
- `specpulse/core/custom_validation.py` (new, ~180 lines)
- `.specpulse/validation_rules.yaml` (new, user-editable)
- `specpulse/utils/rule_manager.py` (new, ~120 lines)

**Key Features:**
- Project-type-aware validation rules
- Enable/disable controls for rules
- Custom error messages per rule
- Rule configuration:
  ```yaml
  rules:
    - name: security_requirement
      enabled: true
      message: "Web apps must include security requirements"
      applies_to: [web-app, api]
      severity: warning

    - name: accessibility_check
      enabled: true
      message: "UI features should mention accessibility"
      applies_to: [web-app, mobile-app]
      severity: info
  ```

**CLI Commands:**
- `specpulse validation rules list` - Show all rules
- `specpulse validation rules enable <rule-name>` - Enable rule
- `specpulse validation rules disable <rule-name>` - Disable rule
- `specpulse validation rules add <name> --template` - Add custom rule

## Open Questions

- [NEEDS CLARIFICATION: Should auto-fix require confirmation or have --no-confirm flag?]
- [NEEDS CLARIFICATION: What should minimum completion percentage be for partial validation to suggest moving to planning phase?]
- [NEEDS CLARIFICATION: Should validation rules support regex patterns for content validation, or just section presence?]

## Appendix

### Validation Flow Diagram
```
User runs: specpulse validate 001
    ↓
Load spec file
    ↓
Check mode: --partial flag?
    ↓                    ↓
NO (full)           YES (partial)
    ↓                    ↓
Run all checks    Run progressive checks
    ↓                    ↓
Check custom      Calculate completion %
validation rules      ↓
    ↓              Show section status
Format errors         ↓
with examples     Suggest next section
    ↓                    ↓
Show --fix        Exit (no errors for
suggestion        partial specs)
    ↓
Exit with status
```

### Example Validation Output (Enhanced)

**Before (Current v1.7.0):**
```
❌ Validation failed
Missing sections: Acceptance Criteria
```

**After (v1.8.0):**
```
❌ Missing: Acceptance Criteria

What this means:
  Acceptance criteria define when the feature is "done"

Example:
  ✓ User can login with email/password
  ✓ Invalid credentials show error message
  ✓ Successful login redirects to dashboard

Suggestion for LLM:
  Add a section "## Acceptance Criteria" with 3-5 testable conditions

Quick fix:
  specpulse validate 001 --fix  # Adds template section

Help:
  specpulse help acceptance-criteria
```

### Related ROADMAP Sections

- **v1.6.0**: Tiered templates (already implemented) - provides foundation for validation examples
- **v1.7.0**: Memory management (already implemented) - provides project context for custom rules
- **v1.9.0**: Incremental spec building (planned) - will leverage partial validation heavily
- **v2.0.0**: JSON outputs (planned) - will add `--format json` to validation commands
