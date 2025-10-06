# Task Breakdown: Validation Feedback Improvements

## Feature Overview
- **Feature ID**: 003
- **Specification**: SPEC-003 (specs/003-validation-feedback-improvements/spec-001.md)
- **Plan**: PLAN-003 (plans/003-validation-feedback-improvements/plan-001.md)
- **Created**: 2025-10-06
- **Architecture**: Monolithic (no decomposition)

## Task Summary
- **Total Tasks**: 28
- **Estimated Effort**: ~40-50 hours (1 week)
- **Priority**: HIGH (v1.8.0 release feature)
- **Complexity Distribution**:
  - Simple: 10 tasks
  - Medium: 14 tasks
  - Complex: 4 tasks

## Task Status Legend
- [ ] Pending
- [>] In Progress
- [x] Completed
- [!] Blocked

## SDD Compliance Gates
- [x] **Phase -1 Gates**: All pre-implementation checks passed
- [x] Specification First: SPEC-003 complete with 10 functional requirements
- [x] Incremental Planning: 4-phase plan with clear deliverables
- [ ] Task Decomposition: 28 concrete, executable tasks
- [ ] Quality Assurance: >90% test coverage target, TDD approach
- [ ] Architecture Documentation: 6 key design decisions documented

---

## Phase 0: Foundation & Infrastructure (Est: 1-2 days)

### T001: Create validation_examples.yaml Resource File
**Complexity**: Simple
**Estimate**: 1-2 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: None
**Parallel**: [P] Can run in parallel with T002, T003

**Description**: Create YAML file structure for validation examples database
**Acceptance Criteria**:
- [ ] File created at `specpulse/resources/validation_examples.yaml`
- [ ] YAML schema defined with fields: message, meaning, example, suggestion, help_command, auto_fix
- [ ] 5 initial examples added: acceptance_criteria, requirements, user_stories, executive_summary, problem_statement
- [ ] YAML validates without errors
- [ ] Examples include multiline text formatting

**Files to Create/Modify**:
- `specpulse/resources/validation_examples.yaml` (new, ~100 lines)

**Technical Notes**:
- Use YAML anchors for reusable content
- Version file as v1.0.0 in header comment
- Follow existing YAML format in project

**Testing**:
- Validate YAML syntax with PyYAML
- Test example retrieval by key

---

### T002: Create validation_rules.yaml Template
**Complexity**: Simple
**Estimate**: 1-2 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: None
**Parallel**: [P] Can run in parallel with T001, T003

**Description**: Create YAML template for custom validation rules
**Acceptance Criteria**:
- [ ] File created at `specpulse/resources/validation_rules.yaml`
- [ ] Schema defined with fields: name, enabled, message, applies_to, severity
- [ ] 3 default rules added: security_requirement, accessibility_check, performance_consideration
- [ ] Rule configuration format documented in comments
- [ ] Rules support project type filtering (web-app, api, mobile-app)

**Files to Create/Modify**:
- `specpulse/resources/validation_rules.yaml` (new, ~100 lines)

**Technical Notes**:
- Include comprehensive comments explaining each field
- Provide examples for web-app, api, mobile-app project types
- Use severity levels: error, warning, info

**Testing**:
- Validate YAML syntax
- Test rule parsing logic

---

### T003: Set Up Test Infrastructure for Validation
**Complexity**: Simple
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: None
**Parallel**: [P] Can run in parallel with T001, T002

**Description**: Create test fixtures and utilities for validation testing
**Acceptance Criteria**:
- [ ] Test fixtures created in `tests/fixtures/validation/`
- [ ] Sample valid specs (complete, partial, minimal)
- [ ] Sample invalid specs (missing sections, malformed)
- [ ] Pytest markers for validation tests (@pytest.mark.validation)
- [ ] Test utilities for validation assertions

**Files to Create/Modify**:
- `tests/fixtures/validation/valid_spec.md` (new)
- `tests/fixtures/validation/partial_spec.md` (new)
- `tests/fixtures/validation/invalid_spec.md` (new)
- `tests/conftest.py` (+20 lines for fixtures)
- `tests/test_validation_helpers.py` (new, ~50 lines)

**Technical Notes**:
- Use realistic spec examples from existing features
- Create helpers for common validation assertions
- Set up pytest markers for test categorization

**Testing**:
- Verify all fixtures load correctly
- Test helper functions work as expected

---

### T004: Create progress_calculator.py Utility
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: None
**Parallel**: [P] Can run in parallel with T001-T003

**Description**: Implement utility for calculating spec completion progress
**Acceptance Criteria**:
- [ ] File created at `specpulse/utils/progress_calculator.py`
- [ ] `calculate_completion_percentage(spec_content)` method implemented
- [ ] `calculate_section_status(section_content)` method implemented (returns: complete/partial/missing)
- [ ] Section weights configured (executive_summary: 5%, requirements: 15%, etc.)
- [ ] Threshold logic for partial vs complete sections

**Files to Create/Modify**:
- `specpulse/utils/progress_calculator.py` (new, ~80 lines)
- `tests/test_progress_calculator.py` (new, ~100 lines)

**Technical Notes**:
- Use dataclass for ProgressResult (completion_pct, section_statuses)
- Define section weights in configuration dict
- Implement threshold logic (e.g., requirements needs 3+ items to be "complete")

**Testing**:
- Test completion percentage calculation with various specs
- Test section status determination
- Test weighted calculation logic
- Edge cases: empty spec, single section

---

## Phase 1: Actionable Validation Messages (Component 3.1) (Est: 2-3 days)

### T005: Add ValidationExample Dataclass to Validator
**Complexity**: Simple
**Estimate**: 1 hour
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T001
**Parallel**: No (sequential after T001)

**Description**: Add dataclass to represent enhanced validation errors
**Acceptance Criteria**:
- [ ] `ValidationExample` dataclass created with fields: message, meaning, example, suggestion, help_command, auto_fix
- [ ] Type hints for all fields
- [ ] Docstrings explaining each field
- [ ] Proper __str__ method for display

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+20 lines)
- `tests/test_validator.py` (+30 lines)

**Technical Notes**:
- Use @dataclass decorator from Python dataclasses
- Make auto_fix optional (default: False)
- Add validation for required fields

**Testing**:
- Test dataclass instantiation
- Test field validation
- Test string representation

---

### T006: Implement load_validation_examples() Method
**Complexity**: Medium
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T001, T005
**Parallel**: No (depends on T001, T005)

**Description**: Parse validation_examples.yaml and load into memory
**Acceptance Criteria**:
- [ ] Method `load_validation_examples()` implemented in Validator class
- [ ] YAML parsing with error handling
- [ ] Examples cached in memory (class variable)
- [ ] Lazy loading (load only when needed)
- [ ] Proper exception handling for malformed YAML

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+40 lines)
- `tests/test_validator.py` (+50 lines)

**Technical Notes**:
- Use PyYAML's safe_load()
- Cache examples in _validation_examples class variable
- Handle file not found gracefully
- Log loading errors

**Testing**:
- Test successful loading from valid YAML
- Test error handling for malformed YAML
- Test caching (second call doesn't reload file)
- Test file not found handling

---

### T007: Modify _check_section_exists() for Enhanced Messages
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T005, T006
**Parallel**: No (depends on T005, T006)

**Description**: Update section checking to use enhanced error messages
**Acceptance Criteria**:
- [ ] Method updated to return ValidationExample instead of string
- [ ] Example lookup by section name
- [ ] Fallback to default message if example not found
- [ ] Maintains backward compatibility

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+30 lines)
- `tests/test_validator.py` (+60 lines)

**Technical Notes**:
- Map section names to example keys
- Preserve existing validation logic
- Add logging for missing examples

**Testing**:
- Test enhanced messages for all section types
- Test fallback for unknown sections
- Test backward compatibility

---

### T008: Implement format_enhanced_error() Method
**Complexity**: Medium
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T005
**Parallel**: Can run after T005, parallel with T007

**Description**: Format enhanced error messages for display
**Acceptance Criteria**:
- [ ] Method `format_enhanced_error(example: ValidationExample)` implemented
- [ ] Output includes: "What this means", "Example", "Suggestion", "Quick fix", "Help"
- [ ] Rich formatting with panels and syntax highlighting
- [ ] Consistent layout for all errors

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+50 lines)
- `tests/test_validator.py` (+40 lines)

**Technical Notes**:
- Use Rich library for formatting
- Create Panel with title for each section
- Add color coding: green for examples, yellow for suggestions
- Format multiline examples properly

**Testing**:
- Test formatting with various examples
- Test Rich panel rendering
- Test multiline content formatting

---

### T009: Implement Auto-Fix Functionality
**Complexity**: Complex
**Estimate**: 5-7 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T005, T006
**Parallel**: No (complex, needs T005, T006 complete)

**Description**: Implement auto-fix for common validation issues
**Acceptance Criteria**:
- [ ] Method `auto_fix_validation_issues(spec_path, backup=True)` implemented
- [ ] Backup creation before modifications
- [ ] Missing sections added with template placeholders
- [ ] Diff report generation showing changes
- [ ] Rollback mechanism if auto-fix fails

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+80 lines)
- `specpulse/utils/backup_manager.py` (new, ~60 lines)
- `tests/test_validator_autofix.py` (new, ~120 lines)

**Technical Notes**:
- Create backup with timestamp suffix (.bak-TIMESTAMP)
- Use template sections from validation_examples.yaml
- Generate unified diff for reporting
- Atomic operations (all or nothing)
- Store backup path for rollback

**Testing**:
- Test backup creation
- Test section addition
- Test diff generation
- Test rollback on failure
- Test no modifications if spec is valid

---

### T010: Expand Validation Examples Database to 15+ Examples
**Complexity**: Simple
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T001
**Parallel**: [P] Can run parallel with other Phase 1 tasks after T001

**Description**: Add comprehensive examples covering all spec sections
**Acceptance Criteria**:
- [ ] 15+ examples in validation_examples.yaml
- [ ] Coverage: acceptance_criteria, user_stories, requirements, technical_constraints, dependencies, risks, success_criteria, executive_summary, problem_statement, proposed_solution, etc.
- [ ] Project-type-specific examples (web-app, api, mobile-app)
- [ ] Each example has all required fields
- [ ] Examples use realistic, helpful content

**Files to Create/Modify**:
- `specpulse/resources/validation_examples.yaml` (+100 lines)

**Technical Notes**:
- Use real-world examples from existing specs
- Include variety of project types
- Make suggestions actionable and specific
- Add help_command references for each

**Testing**:
- Validate YAML syntax
- Test all examples load correctly
- Verify completeness of each example

---

### T011: Add --fix Flag to CLI Validate Command
**Complexity**: Simple
**Estimate**: 1-2 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T009
**Parallel**: No (depends on T009)

**Description**: Add CLI flag to trigger auto-fix
**Acceptance Criteria**:
- [ ] `--fix` flag added to validate command
- [ ] Flag invokes auto_fix_validation_issues()
- [ ] Output shows diff of changes
- [ ] Success/failure message displayed

**Files to Create/Modify**:
- `specpulse/cli/main.py` (+30 lines)
- `tests/test_cli.py` (+40 lines)

**Technical Notes**:
- Use Click's flag option
- Add confirmation prompt before applying fixes
- Display backup location

**Testing**:
- Test --fix flag invokes auto-fix
- Test output formatting
- Test confirmation prompt

---

### T012: Add --show-examples Flag and help Command
**Complexity**: Simple
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: LOW
**Dependencies**: T006
**Parallel**: [P] Can run parallel with T011 after T006

**Description**: Add CLI options to view validation examples and help
**Acceptance Criteria**:
- [ ] `--show-examples` flag added to validate command
- [ ] `help <topic>` command added
- [ ] Examples displayed in Rich table format
- [ ] Help topics reference validation examples

**Files to Create/Modify**:
- `specpulse/cli/main.py` (+50 lines)
- `tests/test_cli.py` (+50 lines)

**Technical Notes**:
- Use Rich Table for examples display
- Group examples by category
- Add search/filter capability for help topics

**Testing**:
- Test --show-examples displays all examples
- Test help command for validation topics
- Test table formatting

---

## Phase 2: Partial Validation (Component 3.2) (Est: 1-2 days)

### T013: Create ValidationProgress Dataclass
**Complexity**: Simple
**Estimate**: 1 hour
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: None
**Parallel**: [P] Can start Phase 2 in parallel with Phase 1 completion

**Description**: Create dataclass for partial validation results
**Acceptance Criteria**:
- [ ] `ValidationProgress` dataclass with fields: completion_pct, section_statuses, next_suggestion
- [ ] Type hints for all fields
- [ ] __str__ method for display
- [ ] SectionStatus enum (COMPLETE, PARTIAL, MISSING)

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+30 lines)
- `tests/test_validator.py` (+20 lines)

**Technical Notes**:
- Use Enum for SectionStatus
- section_statuses should be Dict[str, SectionStatus]
- Add helpful string representation

**Testing**:
- Test dataclass creation
- Test enum values
- Test string representation

---

### T014: Implement validate_partial() Method
**Complexity**: Medium
**Estimate**: 4-6 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T004, T013
**Parallel**: No (depends on T004, T013)

**Description**: Implement progressive validation for incomplete specs
**Acceptance Criteria**:
- [ ] Method `validate_partial(spec_path)` returns ValidationProgress
- [ ] Completion percentage calculated using progress_calculator
- [ ] Section status determined (complete/partial/missing)
- [ ] No errors raised for incomplete specs
- [ ] Next section suggestion included

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+60 lines)
- `tests/test_validator_partial.py` (new, ~100 lines)

**Technical Notes**:
- Use progress_calculator for completion logic
- Define section quality checks (min items, length)
- Calculate next suggestion based on completion state

**Testing**:
- Test with complete spec (100%)
- Test with partial spec (40%, 60%, 80%)
- Test with minimal spec (20%)
- Test section status calculation
- Test next suggestion logic

---

### T015: Implement Section Status Calculation Logic
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T004
**Parallel**: Can run parallel with T014 after T004

**Description**: Determine section status (complete/partial/missing)
**Acceptance Criteria**:
- [ ] Logic added to progress_calculator.py
- [ ] Thresholds defined for each section type
- [ ] Requirements: min 3 items for "complete"
- [ ] User stories: min 2 stories for "complete"
- [ ] Visual status indicators: ✓ (complete), ⚠️ (partial), ⭕ (missing)

**Files to Create/Modify**:
- `specpulse/utils/progress_calculator.py` (+40 lines)
- `tests/test_progress_calculator.py` (+60 lines)

**Technical Notes**:
- Define threshold config dict
- Check item count, line count, content quality
- Return enum value with icon

**Testing**:
- Test threshold logic for all section types
- Test status determination
- Test icon mapping

---

### T016: Implement Next Section Suggestion Engine
**Complexity**: Simple
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T014
**Parallel**: Can run after T014, parallel with T015

**Description**: Suggest next section to work on based on completion
**Acceptance Criteria**:
- [ ] Method `suggest_next_section(current_sections)` implemented
- [ ] Recommended order defined: executive → problem → solution → requirements → user_stories → acceptance_criteria
- [ ] Context-aware suggestions (if "security" mentioned, suggest security section)
- [ ] Returns None when spec is complete

**Files to Create/Modify**:
- `specpulse/utils/progress_calculator.py` (+30 lines)
- `tests/test_progress_calculator.py` (+40 lines)

**Technical Notes**:
- Define section order priority list
- Parse spec content for keywords (security, performance, etc.)
- Use heuristics for context awareness

**Testing**:
- Test suggestion follows recommended order
- Test context-aware suggestions
- Test returns None for complete spec
- Test handles custom sections

---

### T017: Add --partial Flag to CLI Validate Command
**Complexity**: Simple
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T014
**Parallel**: No (depends on T014)

**Description**: Add CLI flag for partial validation mode
**Acceptance Criteria**:
- [ ] `--partial` flag added to validate command
- [ ] Flag invokes validate_partial()
- [ ] Output formatted with Rich tables
- [ ] Progress bar visualization
- [ ] Section status displayed with icons

**Files to Create/Modify**:
- `specpulse/cli/main.py` (+40 lines)
- `tests/test_cli.py` (+50 lines)

**Technical Notes**:
- Use Rich Table for section status
- Add Progress bar showing completion %
- Format output similar to plan example in spec

**Testing**:
- Test --partial flag invokes partial validation
- Test output formatting
- Test progress bar rendering
- Test section status display

---

### T018: Add --progress Flag for Quick Percentage Display
**Complexity**: Simple
**Estimate**: 1 hour
**Status**: [ ] Pending
**Priority**: LOW
**Dependencies**: T014
**Parallel**: [P] Can run parallel with T017 after T014

**Description**: Add flag to show just completion percentage
**Acceptance Criteria**:
- [ ] `--progress` flag added to validate command
- [ ] Output shows only percentage (e.g., "65% complete")
- [ ] Fast execution (minimal output)

**Files to Create/Modify**:
- `specpulse/cli/main.py` (+20 lines)
- `tests/test_cli.py` (+20 lines)

**Technical Notes**:
- Simple output format for scripting
- No Rich formatting for speed

**Testing**:
- Test --progress shows percentage only
- Test fast execution

---

## Phase 3: Context-Based Validation Rules (Component 3.3) (Est: 2-3 days)

### T019: Create ValidationRule Dataclass and RuleEngine Class
**Complexity**: Complex
**Estimate**: 4-5 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T002
**Parallel**: Can start Phase 3 after T002

**Description**: Implement core custom validation rule infrastructure
**Acceptance Criteria**:
- [ ] File created: `specpulse/core/custom_validation.py`
- [ ] `ValidationRule` dataclass with fields: name, enabled, message, applies_to, severity, check_function
- [ ] `RuleEngine` class with methods: load_rules(), execute_rules(), filter_by_project_type()
- [ ] Severity enum: ERROR, WARNING, INFO
- [ ] Rule execution pipeline

**Files to Create/Modify**:
- `specpulse/core/custom_validation.py` (new, ~180 lines)
- `tests/test_custom_validation.py` (new, ~120 lines)

**Technical Notes**:
- Use dataclass for ValidationRule
- RuleEngine loads from validation_rules.yaml
- Filter rules based on project type from context
- Execute rules and collect results

**Testing**:
- Test rule loading from YAML
- Test filtering by project type
- Test rule execution
- Test severity handling
- Test error collection

---

### T020: Implement Project Type Detection
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: None (uses v1.7.0 project_context.py if available)
**Parallel**: [P] Can run parallel with T019

**Description**: Detect project type from context or file structure
**Acceptance Criteria**:
- [ ] File created: `specpulse/utils/project_detector.py`
- [ ] Method `detect_project_type()` implemented
- [ ] Checks `.specpulse/project_context.yaml` first (from v1.7.0)
- [ ] Fallback detection from file structure (package.json → web-app, requirements.txt → api, etc.)
- [ ] Manual override support
- [ ] Caching of detection results

**Files to Create/Modify**:
- `specpulse/utils/project_detector.py` (new, ~100 lines)
- `tests/test_project_detector.py` (new, ~80 lines)

**Technical Notes**:
- Return enum: WEB_APP, API, MOBILE_APP, DESKTOP, CLI, LIBRARY, UNKNOWN
- Cache result in memory
- Check common files: package.json, pyproject.toml, go.mod, Gemfile, etc.

**Testing**:
- Test detection from context.yaml
- Test fallback detection from files
- Test manual override
- Test caching
- Test multiple project types

---

### T021: Implement Rule Manager Utility
**Complexity**: Medium
**Estimate**: 4-5 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T019
**Parallel**: No (depends on T019)

**Description**: CRUD operations for validation rules
**Acceptance Criteria**:
- [ ] File created: `specpulse/utils/rule_manager.py`
- [ ] Methods: list_rules(), enable_rule(name), disable_rule(name), add_custom_rule(rule)
- [ ] Rule validation (ensure structure is valid)
- [ ] Rule template generator
- [ ] Persistence to validation_rules.yaml

**Files to Create/Modify**:
- `specpulse/utils/rule_manager.py` (new, ~120 lines)
- `tests/test_rule_manager.py` (new, ~100 lines)

**Technical Notes**:
- Validate rule structure before adding
- Update YAML file atomically
- Generate template with all required fields
- Handle concurrent access (file locking)

**Testing**:
- Test rule listing
- Test enable/disable
- Test custom rule creation
- Test template generation
- Test file persistence
- Test validation errors

---

### T022: Create Default Validation Rules for Common Project Types
**Complexity**: Simple
**Estimate**: 2-3 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T002
**Parallel**: [P] Can run parallel with T019-T021 after T002

**Description**: Add 5+ default rules for web-app, api, mobile-app
**Acceptance Criteria**:
- [ ] Web-app rules: security_requirement, accessibility_check, performance_requirement
- [ ] API rules: api_documentation, rate_limiting, authentication
- [ ] Mobile-app rules: platform_support, offline_mode, app_store_requirements
- [ ] Rules documented with examples in comments
- [ ] All rules disabled by default (opt-in)

**Files to Create/Modify**:
- `specpulse/resources/validation_rules.yaml` (+50 lines)

**Technical Notes**:
- Use clear, actionable messages
- Reference relevant sections to check
- Include rationale in comments

**Testing**:
- Validate YAML syntax
- Test each rule loads correctly

---

### T023: Add CLI Commands for Rule Management
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T021
**Parallel**: No (depends on T021)

**Description**: CLI interface for managing validation rules
**Acceptance Criteria**:
- [ ] Command group: `validation rules`
- [ ] Subcommands: list, enable <name>, disable <name>, add <name> --template
- [ ] Rich table output for list command
- [ ] Interactive prompts for add command
- [ ] Clear success/error messages

**Files to Create/Modify**:
- `specpulse/cli/main.py` (+80 lines)
- `tests/test_cli.py` (+80 lines)

**Technical Notes**:
- Use Click command groups
- Rich Table for list display
- Prompt for rule details in add command

**Testing**:
- Test list command
- Test enable/disable commands
- Test add command
- Test help text for all commands

---

### T024: Integrate Custom Rules into Validation Pipeline
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T019, T020
**Parallel**: No (depends on T019, T020)

**Description**: Add custom rule execution to main validate() method
**Acceptance Criteria**:
- [ ] Custom rules executed in validate() method
- [ ] Rules filtered by detected project type
- [ ] Custom rule errors formatted using enhanced error format
- [ ] Custom rules included in validation report
- [ ] Performance: early exit for disabled rules

**Files to Create/Modify**:
- `specpulse/core/validator.py` (+50 lines)
- `tests/test_validator.py` (+70 lines)

**Technical Notes**:
- Load rules from RuleEngine
- Filter by project type before execution
- Merge custom rule errors with standard errors
- Format with format_enhanced_error()

**Testing**:
- Test custom rules execute during validation
- Test project type filtering
- Test error formatting
- Test disabled rules are skipped
- Test integration with standard validation

---

## Phase 4: Integration & Testing (Est: 1 day)

### T025: Component Integration Testing
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T012, T018, T024 (all Phase 1-3 complete)
**Parallel**: No (requires all components)

**Description**: Test all three components work together
**Acceptance Criteria**:
- [ ] Actionable messages work with partial validation
- [ ] Custom rules work with both full and partial validation
- [ ] Auto-fix doesn't interfere with custom rules
- [ ] All components seamlessly integrated
- [ ] End-to-end workflow tests passing

**Files to Create/Modify**:
- `tests/integration/test_v180_workflow.py` (new, ~200 lines)

**Technical Notes**:
- Test full workflow: validate → errors with examples → partial → custom rules → auto-fix
- Use realistic spec fixtures
- Test error scenarios and edge cases

**Testing**:
- Full validation with enhanced errors
- Partial validation with custom rules
- Auto-fix with all features enabled
- Error scenarios and recovery

---

### T026: Comprehensive Test Suite and Coverage
**Complexity**: Complex
**Estimate**: 4-6 hours
**Status**: [ ] Pending
**Priority**: HIGH
**Dependencies**: T025
**Parallel**: No (after T025)

**Description**: Achieve >90% test coverage for all new code
**Acceptance Criteria**:
- [ ] Test coverage >90% for new validation code
- [ ] Unit tests: 100+ tests total
- [ ] Integration tests: 30+ tests
- [ ] Performance tests: 10+ benchmarks
- [ ] Regression tests: 20+ tests for v1.7.0 compatibility
- [ ] Cross-platform tests (Windows, macOS, Linux)

**Files to Create/Modify**:
- Various test files (+300 lines across all test files)
- `tests/performance/test_validation_perf.py` (new, ~100 lines)

**Technical Notes**:
- Run pytest with coverage reporting
- Add missing tests for uncovered code
- Performance target: <2 seconds for validation
- Use tox for cross-platform testing

**Testing**:
- Run full test suite
- Generate coverage report
- Performance benchmarks
- Cross-platform CI checks

---

### T027: Performance Optimization
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T026
**Parallel**: Can run parallel with T028

**Description**: Optimize validation performance
**Acceptance Criteria**:
- [ ] Validation completes in <2 seconds for typical specs
- [ ] Example loading cached (no repeated YAML parsing)
- [ ] Rule execution optimized (early exit for disabled rules)
- [ ] Section parsing optimized
- [ ] Memory usage <50MB

**Files to Create/Modify**:
- `specpulse/core/validator.py` (optimize existing code)
- `specpulse/utils/progress_calculator.py` (optimize existing code)

**Technical Notes**:
- Profile with cProfile
- Cache validation examples at module level
- Use lazy loading where possible
- Optimize regex patterns

**Testing**:
- Performance benchmarks before/after
- Memory profiling
- Load testing with large specs

---

### T028: Documentation and Migration Guide
**Complexity**: Medium
**Estimate**: 3-4 hours
**Status**: [ ] Pending
**Priority**: MEDIUM
**Dependencies**: T025
**Parallel**: [P] Can run parallel with T027

**Description**: Complete documentation for v1.8.0
**Acceptance Criteria**:
- [ ] CLI help text updated for all new commands
- [ ] Validation examples documented
- [ ] Custom rule creation guide written
- [ ] Migration guide from v1.7.0 created
- [ ] README updated with v1.8.0 features

**Files to Create/Modify**:
- `docs/validation_examples.md` (new, ~100 lines)
- `docs/custom_rules.md` (new, ~150 lines)
- `MIGRATION_v1.8.0.md` (new, ~80 lines)
- `README.md` (+30 lines)
- `specpulse/cli/main.py` (update help text)

**Technical Notes**:
- Include examples for all features
- Provide migration checklist
- Document breaking changes (none expected)
- Add screenshots/examples

**Testing**:
- Verify all links work
- Test documentation examples
- Review migration guide

---

## Dependencies Visualization

```
Phase 0 (Foundation):
[T001] ─┐
[T002] ─┤
[T003] ─┼─→ [Phase 1 can start]
[T004] ─┘

Phase 1 (Actionable Messages):
[T001] → [T005] → [T006] → [T007]
                    └────→ [T009] → [T011]
                                  ↓
[T001] ────────────────────────→ [T010]
[T005] ──────────────────────→ [T008] → [T012]

Phase 2 (Partial Validation):
[T004] → [T013] → [T014] → [T017]
[T004] ────────→ [T015] ──┘
[T014] ────────→ [T016]
[T014] ────────→ [T018]

Phase 3 (Custom Rules):
[T002] → [T019] → [T021] → [T023]
              └─→ [T024]
[T002] ────────→ [T022]
[None] ────────→ [T020] → [T024]

Phase 4 (Integration):
[All Phase 1-3] → [T025] → [T026] → [T027]
[T025] ──────────────────────────→ [T028]
```

## Parallel Execution Groups

### Group A (Foundation - All Parallel):
- T001, T002, T003, T004

### Group B (Phase 1 - After T001):
- T005, T010 (after T001)
- T008, T012 (independent paths)

### Group C (Phase 2 - After T004):
- T013, T015, T016, T018 (various dependencies)

### Group D (Phase 3 - After T002):
- T019, T020, T022 (can run parallel)

### Group E (Final - Sequential):
- T025 → T026 → (T027 || T028)

## Progress Tracking

```yaml
status:
  total: 28
  completed: 0
  in_progress: 0
  blocked: 0
  pending: 28

phases:
  phase_0_foundation:
    tasks: 4
    completed: 0
    percentage: 0%
  phase_1_actionable_messages:
    tasks: 8
    completed: 0
    percentage: 0%
  phase_2_partial_validation:
    tasks: 6
    completed: 0
    percentage: 0%
  phase_3_custom_rules:
    tasks: 6
    completed: 0
    percentage: 0%
  phase_4_integration:
    tasks: 4
    completed: 0
    percentage: 0%

metrics:
  estimated_effort: "40-50 hours"
  estimated_duration: "5-7 days"
  velocity: "4-6 tasks/day"
  estimated_completion: "2025-10-13"
  completion_percentage: 0%

sdd_gates:
  specification_first: true
  incremental_planning: true
  task_decomposition: true
  quality_assurance: false (tests pending)
  architecture_documentation: true
```

## Critical Path

The critical path for completing this feature (longest dependency chain):

**T001 → T005 → T006 → T009 → T011** (Actionable messages with auto-fix)
**Estimated Critical Path Duration**: 12-17 hours

**Parallel Critical Path**:
**T002 → T019 → T024** (Custom rules integration)
**Estimated Duration**: 11-13 hours

**Overall Critical Path**: ~17 hours (actionable messages path is longer)

## Risk Mitigation

### High-Risk Tasks
- **T009 (Auto-Fix)**: Complex logic, potential data loss risk
  - Mitigation: Mandatory backups, comprehensive testing
- **T019 (RuleEngine)**: Complex architecture, plugin system
  - Mitigation: Clear interfaces, extensive unit tests
- **T026 (Test Coverage)**: Time-consuming, may reveal issues
  - Mitigation: Start early, allocate extra time

### Blockers to Watch
- YAML parsing issues (T001, T002)
- Performance degradation (T027)
- Backward compatibility (T026)

## Notes

### Implementation Tips
1. **Start with Foundation**: Complete all Phase 0 tasks before Phase 1
2. **Test as You Go**: Don't wait for T026 to write tests
3. **Use TDD**: Write tests before implementation for complex tasks (T009, T019)
4. **Profile Early**: Run performance tests during Phase 1-3, not just Phase 4

### Files Summary
**New Files** (12):
- validation_examples.yaml (200 lines)
- validation_rules.yaml (100 lines)
- custom_validation.py (180 lines)
- progress_calculator.py (80 lines)
- project_detector.py (100 lines)
- rule_manager.py (120 lines)
- backup_manager.py (60 lines)
- 5+ test files (600+ lines)

**Modified Files** (2):
- validator.py (+250 lines)
- main.py (+150 lines)

**Total New Code**: ~1,840 lines
**Total Test Code**: ~1,200 lines
**Test-to-Code Ratio**: 0.65 (65% test coverage by lines)

### Next Steps
1. Review task breakdown with team
2. Set up project tracking (GitHub Issues, Jira, etc.)
3. Assign tasks to sprints
4. Begin Phase 0 (Foundation)
5. Daily standups to track progress
6. Update task status as work progresses

### Acceptance
- [ ] All 28 tasks completed
- [ ] All tests passing (>90% coverage)
- [ ] Performance benchmarks met (<2 seconds)
- [ ] Documentation complete
- [ ] Code reviewed and merged
- [ ] v1.8.0 released
