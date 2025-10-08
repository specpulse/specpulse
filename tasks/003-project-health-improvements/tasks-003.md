<!-- SpecPulse Task List Template v1.0 -->
<!-- FEATURE_DIR: 003-project-health-improvements -->
<!-- FEATURE_ID: 003 -->
<!-- TASK_ID: TASKS-003 -->
<!-- STATUS: pending -->
<!-- CREATED: 2025-10-08 -->

# Task List: SpecPulse Project Health & Quality Improvements

## Metadata
- **Plan Reference**: PLAN-003
- **Spec Reference**: SPEC-003
- **Total Tasks**: 32
- **Estimated Duration**: 14-16 hours
- **Parallel Groups**: 3
- **Critical Path Duration**: 9 hours

## Task Organization

### 🚀 Phase 0: Preparation (1 hour) - Sequential

#### TASK-001: Create Feature Branch
- **Type**: setup
- **Priority**: HIGH
- **Estimate**: 0.15 hours (10 min)
- **Dependencies**: None
- **Description**: Create and checkout feature branch `003-project-health-improvements` from master
- **Acceptance**: Branch exists, checked out, git status clean
- **Assignable**: Any developer with git access
- **Commands**:
  ```bash
  git checkout master
  git pull origin master
  git checkout -b 003-project-health-improvements
  ```

#### TASK-002: Capture Baseline Metrics
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-001
- **Description**: Run full test suite and capture coverage, performance metrics
- **Acceptance**: Baseline report saved to .specpulse/baselines/phase0.json
- **Assignable**: Developer with pytest experience
- **Commands**:
  ```bash
  pytest --cov=specpulse --cov-report=json -v > baseline_tests.txt
  pytest --benchmark-only > baseline_benchmark.txt
  ```

#### TASK-003: Validate Development Environment
- **Type**: setup
- **Priority**: HIGH
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: None (Parallel with TASK-002)
- **Description**: Verify Python 3.11+, pytest, black, mypy installed and working
- **Acceptance**: All tools report correct versions
- **Assignable**: Any developer
- **Commands**:
  ```bash
  python --version  # Should be 3.11+
  pytest --version
  black --version
  mypy --version
  ```

#### TASK-004: Review Spec and Plan
- **Type**: documentation
- **Priority**: MEDIUM
- **Estimate**: 0.35 hours (20 min)
- **Dependencies**: TASK-001
- **Description**: Read SPEC-003 and PLAN-003, clarify any questions with team
- **Acceptance**: Developer understands requirements and approach
- **Assignable**: Implementing developer

---

### 🔴 Phase 1: Critical Fixes (3 hours) - Mostly Sequential

#### TASK-005: Synchronize Version Strings
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-004
- **Description**: Update all version references to 2.1.2
- **Acceptance**: grep -r "2.0.0\|2.1.0" returns only _version.py
- **Assignable**: Any developer
- **Files**:
  - setup.py (line 29): Update description
  - README.md (line 43, 489): Update install commands
  - Verify pyproject.toml reads from _version.py
- **Commands**:
  ```bash
  grep -r "SpecPulse v2.0" .
  grep -r "2.1.0" . | grep -v _version.py | grep -v CHANGELOG
  ```

#### TASK-006: Clean Up MANIFEST.in
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-005
- **Description**: Remove obsolete script references from MANIFEST.in
- **Acceptance**: Line 8 removed, build succeeds
- **Assignable**: Any developer
- **Files**:
  - MANIFEST.in: Remove `recursive-include specpulse/resources/scripts *`
- **Validation**:
  ```bash
  python setup.py sdist bdist_wheel
  tar -tzf dist/specpulse-2.1.2.tar.gz | grep scripts/
  # Should return nothing
  ```

#### TASK-007: Pin Dependency Versions
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-005
- **Description**: Add upper version bounds to all dependencies in pyproject.toml
- **Acceptance**: All dependencies have format >=X.Y,<Z.0
- **Assignable**: Developer familiar with dependency management
- **Files**:
  - pyproject.toml (lines 42-50): Add upper bounds
- **Test**:
  ```bash
  pip install -e ".[dev]"
  pytest  # Should pass
  ```

#### TASK-008: Remove Duplicate get_decomposition_template Method
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-004
- **Description**: Merge duplicate method definitions in specpulse/core/specpulse.py
- **Acceptance**: Only one get_decomposition_template method exists, all tests pass
- **Assignable**: Developer familiar with Python
- **Files**:
  - specpulse/core/specpulse.py: Lines 495-523 vs 1170-1181
- **Steps**:
  1. Compare both implementations
  2. Keep more comprehensive version
  3. Delete duplicate
  4. Run tests: `pytest tests/ -k decomposition`

#### TASK-009: Commit Modified Command Files
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-001
- **Description**: Stage and commit modified .claude/commands/ files
- **Acceptance**: git status shows no uncommitted changes in .claude/
- **Assignable**: Any developer
- **Commands**:
  ```bash
  git add .claude/commands/
  git commit -m "chore: sync command files for v2.1.2"
  ```

#### TASK-010: Remove Deleted Files from Git
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-009
- **Description**: Remove deleted files from git index
- **Acceptance**: git status shows no deleted files
- **Assignable**: Any developer
- **Commands**:
  ```bash
  git rm RELEASE_v2.1.0_COMPLETE.md
  git rm -r scripts/
  git commit -m "chore: remove obsolete files"
  ```

#### TASK-011: Update .gitignore
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-010
- **Description**: Add missing entries to .gitignore
- **Acceptance**: .gitignore contains all required entries
- **Assignable**: Any developer
- **Entries to Add**:
  ```
  *.pyc
  __pycache__/
  *.egg-info/
  .specpulse/cache/
  dist/
  build/
  *.log
  .specpulse/logs/
  ```

#### TASK-012: Phase 1 Validation
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-005, TASK-006, TASK-007, TASK-008, TASK-011
- **Description**: Validate all Phase 1 changes
- **Acceptance**: All checks pass, tests pass, package builds
- **Assignable**: Any developer
- **Validation**:
  ```bash
  pytest
  python setup.py sdist bdist_wheel
  unzip -l dist/specpulse-2.1.2-*.whl | grep scripts  # Should be empty
  git status  # Should be clean
  ```

---

### 🟠 Phase 2: Code Quality (4 hours) - Partially Parallel

#### 🔄 Parallel Group A: Resource & Console (2.25 hours)

#### TASK-013: Add ResourceError Class
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-012
- **Description**: Add ResourceError class to error_handler.py
- **Acceptance**: Class defined with proper inheritance, tested
- **Assignable**: Developer familiar with exception handling
- **Files**:
  - specpulse/utils/error_handler.py: Add new class after line 117
- **Implementation**:
  ```python
  class ResourceError(SpecPulseError):
      """Resource loading errors with specific recovery"""
      def __init__(self, resource_type: str, resource_path: Path):
          # See PLAN-003 for full implementation
  ```

#### TASK-014: Simplify Resource Loading
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 1.5 hours (90 min)
- **Dependencies**: TASK-013
- **Description**: Refactor specpulse/core/specpulse.py:__init__ resource loading
- **Acceptance**: <5 lines of code, no bare except, specific exceptions only
- **Assignable**: Senior developer
- **Files**:
  - specpulse/core/specpulse.py: Lines 17-51 refactor
- **Validation**:
  ```bash
  pytest tests/test_specpulse.py -v
  pip install -e .  # Test dev mode
  pip install dist/specpulse-*.whl  # Test installed mode
  ```

#### TASK-015: Implement Emoji Auto-Detection
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.75 hours (45 min)
- **Dependencies**: TASK-012
- **Description**: Add emoji support detection to Console class
- **Acceptance**: Works on Windows CMD, Windows Terminal, macOS, Linux
- **Assignable**: Developer with cross-platform experience
- **Files**:
  - specpulse/utils/console.py: Add _check_emoji_support() method
  - specpulse/utils/error_handler.py: Remove try-catch (lines 150-153)
- **Test on**: Windows CMD (should disable), Windows Terminal (should enable)

#### 📝 Sequential Group B: Test Reorganization (1.75 hours)

#### TASK-016: Create New Test Directory Structure
- **Type**: setup
- **Priority**: HIGH
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-012
- **Description**: Create unit/, integration/, performance/ folders in tests/
- **Acceptance**: Folders exist, conftest.py copied to each
- **Assignable**: Any developer
- **Commands**:
  ```bash
  mkdir tests/unit tests/integration tests/performance
  cp tests/conftest.py tests/unit/
  cp tests/conftest.py tests/integration/
  cp tests/conftest.py tests/performance/
  ```

#### TASK-017: Categorize and Move Unit Tests
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-016
- **Description**: Move unit tests to tests/unit/ folder
- **Acceptance**: All unit tests in correct folder, still pass
- **Assignable**: Any developer
- **Files to Move**:
  ```bash
  mv tests/test_console.py tests/unit/
  mv tests/test_git_utils.py tests/unit/
  mv tests/test_validator.py tests/unit/
  mv tests/test_template_manager.py tests/unit/
  mv tests/test_memory_manager.py tests/unit/
  mv tests/test_error_handler.py tests/unit/
  mv tests/test_specpulse.py tests/unit/
  # ... all other unit tests
  ```

#### TASK-018: Categorize and Move Integration Tests
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-016
- **Description**: Move integration tests to tests/integration/ folder
- **Acceptance**: All integration tests in correct folder, still pass
- **Assignable**: Any developer
- **Files to Move**:
  ```bash
  mv tests/integration/test_v170_workflow.py tests/integration/
  mv tests/integration/test_v180_workflow.py tests/integration/
  mv tests/test_integration_workflow.py tests/integration/
  mv tests/test_integration.py tests/integration/
  ```

#### TASK-019: Categorize and Move Performance Tests
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.25 hours (15 min)
- **Dependencies**: TASK-016
- **Description**: Move performance tests to tests/performance/ folder
- **Acceptance**: All performance tests in correct folder, still pass
- **Assignable**: Any developer
- **Files to Move**:
  ```bash
  mv tests/benchmarks/test_v170_performance.py tests/performance/
  mv tests/test_performance.py tests/performance/
  ```

#### TASK-020: Consolidate Duplicate Test Files
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-017, TASK-018, TASK-019
- **Description**: Identify and merge duplicate test files
- **Acceptance**: No duplicate tests, coverage maintained
- **Assignable**: Developer familiar with test suite
- **Files to Review**:
  - test_complete_100.py
  - test_coverage_100.py
  - test_final_100.py
  - test_full_coverage.py
  - test_cli_fixed.py
- **Process**: Compare tests, merge unique ones, delete duplicates

#### TASK-021: Add Type Hints to CLI Module
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.75 hours (45 min)
- **Dependencies**: TASK-012
- **Description**: Add type hints to all methods in specpulse/cli/main.py
- **Acceptance**: mypy passes on CLI module
- **Assignable**: Developer familiar with type hints
- **Files**:
  - specpulse/cli/main.py: Add return types, parameter types
- **Validation**:
  ```bash
  mypy specpulse/cli/main.py
  ```

#### TASK-022: Phase 2 Validation
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-014, TASK-015, TASK-020, TASK-021
- **Description**: Validate all Phase 2 changes
- **Acceptance**: All tests pass, coverage maintained, mypy passes
- **Assignable**: Any developer
- **Commands**:
  ```bash
  pytest tests/unit tests/integration tests/performance
  pytest --cov=specpulse --cov-report=html
  mypy specpulse/cli/
  ```

---

### 🟡 Phase 3: Infrastructure (4 hours) - Partially Parallel

#### 🔄 Parallel Group C: Logging & Config (3 hours)

#### TASK-023: Create Logger Module
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 1.5 hours (90 min)
- **Dependencies**: TASK-022
- **Description**: Create specpulse/utils/logger.py with setup_logger function
- **Acceptance**: Logger creates files, rotates correctly, respects log levels
- **Assignable**: Developer familiar with Python logging
- **Files**:
  - specpulse/utils/logger.py (new file)
- **Implementation**: See PLAN-003 Task 3.1
- **Test**:
  ```python
  from specpulse.utils.logger import setup_logger
  logger = setup_logger(Path.cwd(), verbose=True)
  logger.info("Test message")
  # Check .specpulse/logs/specpulse.log exists
  ```

#### TASK-024: Create Config Validator Module
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 1.0 hours (60 min)
- **Dependencies**: TASK-022
- **Description**: Create specpulse/core/config_validator.py
- **Acceptance**: Validates config structure, provides helpful errors
- **Assignable**: Developer familiar with YAML and validation
- **Files**:
  - specpulse/core/config_validator.py (new file)
- **Implementation**: See PLAN-003 Task 3.2
- **Test**:
  ```python
  validator = ConfigValidator()
  errors = validator.validate(Path(".specpulse/config.yaml"))
  assert len(errors) == 0
  ```

#### TASK-025: Write Logger Tests
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-023
- **Description**: Create tests/unit/test_logger.py with comprehensive tests
- **Acceptance**: >90% coverage on logger module
- **Assignable**: Developer with testing experience
- **Files**:
  - tests/unit/test_logger.py (new file)
- **Test Cases**:
  - Logger setup in different modes
  - Log rotation after 10MB
  - Log level filtering
  - Multiple logger instances

#### 📝 Sequential Group D: Integration (1 hour)

#### TASK-026: Integrate Logger into CLI
- **Type**: development
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-023
- **Description**: Add logger setup to specpulse/cli/main.py:__init__
- **Acceptance**: Logs created on CLI startup, commands logged
- **Assignable**: Developer familiar with CLI module
- **Files**:
  - specpulse/cli/main.py: Add logger setup in __init__
- **Log Points**: Command entry, errors, resource loading, config changes

#### TASK-027: Integrate Config Validator
- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-024
- **Description**: Add config validation to init and doctor commands
- **Acceptance**: Invalid config shows warning, doesn't block execution
- **Assignable**: Developer familiar with CLI module
- **Files**:
  - specpulse/cli/main.py: Add validation calls

#### TASK-028: Write Config Validator Tests
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-024
- **Description**: Create tests/unit/test_config_validator.py
- **Acceptance**: >85% coverage on config_validator module
- **Assignable**: Developer with testing experience
- **Files**:
  - tests/unit/test_config_validator.py (new file)
- **Test Cases**:
  - Valid v2.1.1 config
  - Valid v2.0.0 config (backward compat)
  - Missing required keys
  - Invalid structure
  - Auto-fix capability

#### TASK-029: Phase 3 Validation
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.5 hours (30 min)
- **Dependencies**: TASK-026, TASK-027, TASK-028
- **Description**: Validate all Phase 3 changes
- **Acceptance**: Logging works, config validation works, all tests pass
- **Assignable**: Any developer
- **Commands**:
  ```bash
  specpulse init test-project --here
  ls .specpulse/logs/  # Should have specpulse.log
  pytest tests/unit/test_logger.py tests/unit/test_config_validator.py -v
  ```

---

### 🟢 Phase 4: Optimization & Release (2-3 hours) - Mostly Parallel

#### 🔄 Parallel Group D: Final Tasks (2 hours)

#### TASK-030: Add Template Caching
- **Type**: development
- **Priority**: LOW
- **Estimate**: 0.75 hours (45 min)
- **Dependencies**: TASK-029
- **Description**: Add @lru_cache to template methods in specpulse.py
- **Acceptance**: Template loading 2-3x faster (benchmark)
- **Assignable**: Developer familiar with caching
- **Files**:
  - specpulse/core/specpulse.py: Add @lru_cache decorators
- **Benchmark**:
  ```bash
  pytest tests/performance/ --benchmark-compare
  ```

#### TASK-031: Update Documentation
- **Type**: documentation
- **Priority**: HIGH
- **Estimate**: 1.0 hours (60 min)
- **Dependencies**: TASK-029
- **Description**: Update all documentation for v2.1.2
- **Acceptance**: CHANGELOG, README, CLAUDE.md all accurate
- **Assignable**: Any developer
- **Files**:
  - CHANGELOG.md: Add v2.1.2 section
  - README.md: Update features, installation
  - CLAUDE.md: Document new logging/config features
  - docs/MIGRATION.md: Add v2.1.1 → v2.1.2 section

#### TASK-032: Final Release Validation
- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 0.75 hours (45 min)
- **Dependencies**: TASK-030, TASK-031
- **Description**: Complete final validation before release
- **Acceptance**: All release checklist items completed
- **Assignable**: Release manager or senior developer
- **Checklist**:
  ```bash
  # Run full test suite
  pytest --cov=specpulse --cov-report=term-missing

  # Build package
  python setup.py sdist bdist_wheel

  # Test installation in clean virtualenv
  python -m venv test_env
  source test_env/bin/activate  # or test_env\Scripts\activate on Windows
  pip install dist/specpulse-2.1.2-*.whl
  specpulse --version  # Should show 2.1.2
  specpulse doctor
  specpulse init test-proj --here

  # Test backward compatibility
  # (Use existing v2.1.1 project)
  cd existing_v211_project
  pip install --upgrade ~/path/to/specpulse-2.1.2.whl
  specpulse doctor  # Should pass

  # Performance comparison
  pytest tests/performance/ --benchmark-compare=baseline
  ```

---

## 🎯 Critical Path Analysis

**Critical Path** (Tasks that block progress):
1. TASK-001 (branch) →
2. TASK-004 (review) →
3. TASK-005 (version sync) →
4. TASK-012 (phase 1 validation) →
5. TASK-013 (ResourceError) →
6. TASK-014 (resource loading) →
7. TASK-022 (phase 2 validation) →
8. TASK-023 (logger) →
9. TASK-026 (logger integration) →
10. TASK-029 (phase 3 validation) →
11. TASK-032 (final validation)

**Critical Path Duration**: ~8.5 hours

**Parallelization Opportunities**:
- TASK-002 and TASK-003 (parallel)
- TASK-015 while TASK-013+014 happen
- TASK-016-020 (test reorg) can partially overlap with TASK-021
- TASK-023 and TASK-024 (parallel)
- TASK-030 and TASK-031 (parallel)

**Estimated Real Duration**: 14-16 hours with parallelization

---

## Task Details by Category

### Development Tasks (20 tasks)
- [ ] TASK-005: Synchronize Version Strings
- [ ] TASK-006: Clean Up MANIFEST.in
- [ ] TASK-007: Pin Dependency Versions
- [ ] TASK-008: Remove Duplicate Method
- [ ] TASK-009: Commit Modified Command Files
- [ ] TASK-010: Remove Deleted Files from Git
- [ ] TASK-011: Update .gitignore
- [ ] TASK-013: Add ResourceError Class
- [ ] TASK-014: Simplify Resource Loading
- [ ] TASK-015: Implement Emoji Auto-Detection
- [ ] TASK-017: Categorize and Move Unit Tests
- [ ] TASK-018: Categorize and Move Integration Tests
- [ ] TASK-019: Categorize and Move Performance Tests
- [ ] TASK-020: Consolidate Duplicate Test Files
- [ ] TASK-021: Add Type Hints to CLI Module
- [ ] TASK-023: Create Logger Module
- [ ] TASK-024: Create Config Validator Module
- [ ] TASK-026: Integrate Logger into CLI
- [ ] TASK-027: Integrate Config Validator
- [ ] TASK-030: Add Template Caching

### Testing Tasks (7 tasks)
- [ ] TASK-002: Capture Baseline Metrics
- [ ] TASK-012: Phase 1 Validation
- [ ] TASK-022: Phase 2 Validation
- [ ] TASK-025: Write Logger Tests
- [ ] TASK-028: Write Config Validator Tests
- [ ] TASK-029: Phase 3 Validation
- [ ] TASK-032: Final Release Validation

### Setup Tasks (3 tasks)
- [ ] TASK-001: Create Feature Branch
- [ ] TASK-003: Validate Development Environment
- [ ] TASK-016: Create New Test Directory Structure

### Documentation Tasks (2 tasks)
- [ ] TASK-004: Review Spec and Plan
- [ ] TASK-031: Update Documentation

---

## Execution Schedule

### Day 1 (6-7 hours)
**Morning** (3-4 hours):
- TASK-001: Create branch (10 min)
- TASK-002, TASK-003: Baselines & env (parallel, 30 min)
- TASK-004: Review (20 min)
- TASK-005: Version sync (30 min)
- TASK-006: MANIFEST cleanup (15 min)
- TASK-007: Pin dependencies (30 min)
- TASK-008: Remove duplicate (30 min)
- TASK-009, TASK-010, TASK-011: Git cleanup (45 min)
- TASK-012: Phase 1 validation (30 min)

**Afternoon** (3 hours):
- TASK-013: ResourceError class (15 min)
- TASK-014: Simplify resource loading (90 min)
- TASK-015: Emoji detection (45 min) [parallel with test reorg]
- TASK-016: Test directory structure (15 min)

### Day 2 (6-7 hours)
**Morning** (3-4 hours):
- TASK-017, TASK-018, TASK-019: Move tests (60 min)
- TASK-020: Consolidate duplicates (30 min)
- TASK-021: Add type hints (45 min)
- TASK-022: Phase 2 validation (30 min)
- TASK-023: Create logger (90 min) [start early afternoon]

**Afternoon** (3 hours):
- TASK-023: Complete logger (if not done)
- TASK-024: Config validator (60 min) [parallel with logger]
- TASK-025: Logger tests (30 min)
- TASK-026: Integrate logger (30 min)
- TASK-027: Integrate config validator (30 min)
- TASK-028: Config validator tests (30 min)
- TASK-029: Phase 3 validation (30 min)

### Day 3 (2-3 hours)
**Morning/Afternoon** (2-3 hours):
- TASK-030: Template caching (45 min) [parallel with docs]
- TASK-031: Update documentation (60 min)
- TASK-032: Final validation (45 min)
- Buffer time for unexpected issues (30-60 min)

---

## Progress Tracking

```yaml
status:
  total: 32
  completed: 0
  in_progress: 0
  blocked: 0

progress:
  phase_0: 0/4 (0%)
  phase_1: 0/8 (0%)
  phase_2: 0/10 (0%)
  phase_3: 0/7 (0%)
  phase_4: 0/3 (0%)

metrics:
  velocity: 0 tasks/day
  estimated_completion: 2025-10-11
  blockers: []

timeline:
  start_date: 2025-10-08
  day_1_completed: 0
  day_2_completed: 0
  day_3_completed: 0
```

---

## Task Dependencies Graph

```
TASK-001 (branch)
  ├─→ TASK-002 (baseline)
  ├─→ TASK-003 (env) [parallel]
  └─→ TASK-004 (review)
        └─→ TASK-005 (version)
              ├─→ TASK-006 (manifest)
              ├─→ TASK-007 (deps) [parallel]
              └─→ TASK-008 (duplicate) [parallel]
                    └─→ TASK-012 (p1 validate)
                          ├─→ TASK-013 (ResourceError)
                          │     └─→ TASK-014 (resource loading)
                          ├─→ TASK-015 (emoji) [parallel]
                          └─→ TASK-016 (test dirs)
                                ├─→ TASK-017 (move unit)
                                ├─→ TASK-018 (move int)
                                └─→ TASK-019 (move perf)
                                      └─→ TASK-020 (consolidate)
                                            └─→ TASK-022 (p2 validate)
                                                  ├─→ TASK-023 (logger)
                                                  │     ├─→ TASK-025 (logger tests)
                                                  │     └─→ TASK-026 (logger int)
                                                  └─→ TASK-024 (config) [parallel]
                                                        ├─→ TASK-027 (config int)
                                                        └─→ TASK-028 (config tests)
                                                              └─→ TASK-029 (p3 validate)
                                                                    ├─→ TASK-030 (cache)
                                                                    └─→ TASK-031 (docs) [parallel]
                                                                          └─→ TASK-032 (final)
```

---

## Risk Mitigation Tasks

**If Test Reorganization Takes Too Long**:
- Priority: Complete at least unit/ and integration/ separation
- Defer: Duplicate consolidation to post-release cleanup

**If Cross-Platform Testing Unavailable**:
- Priority: Test on Windows (most issues)
- Defer: macOS/Linux validation to community feedback

**If Timeline Slips**:
- Cut: TASK-030 (template caching) - nice-to-have
- Cut: TASK-021 (type hints) - can be incremental
- Keep: All critical fixes, logging, config validation

---

## Success Metrics

**Code Quality**:
- [x] Zero version mismatches
- [ ] Zero duplicate methods
- [ ] Zero bare except blocks
- [ ] All dependencies pinned

**Test Quality**:
- [ ] 615+ tests passing
- [ ] Coverage >80%
- [ ] Tests organized logically

**Performance**:
- [ ] CLI startup <500ms
- [ ] Template loading <50ms (cached)
- [ ] Test suite <60s

**User Experience**:
- [ ] No Unicode errors on Windows
- [ ] Logs created automatically
- [ ] Config validated on init
- [ ] Helpful error messages

---

## Completion Checklist

Before marking feature complete:
- [ ] All 32 tasks completed
- [ ] Full test suite passing (pytest)
- [ ] Coverage report >80%
- [ ] Package builds successfully
- [ ] Fresh install works in virtualenv
- [ ] Backward compatibility tested (v2.1.1 project)
- [ ] Documentation updated
- [ ] CHANGELOG.md has v2.1.2 section
- [ ] Git branch merged to master
- [ ] Tag created: v2.1.2
- [ ] Ready for PyPI upload

---

**Total Estimated Effort**: 14-16 hours
**Recommended Schedule**: 2-3 days
**Critical Path**: 8.5 hours
**Parallelization Factor**: ~40% time savings

**Status**: Ready to begin implementation ✅
