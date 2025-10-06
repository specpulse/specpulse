# Implementation Plan: Better Workflow Support (v1.9.0)

## Specification Reference
- **Spec ID**: SPEC-003
- **Spec File**: specs/003-better-workflow-support/spec-001.md
- **Spec Version**: 1.0.0
- **Plan Version**: 1.0.0
- **Generated**: 2025-10-06
- **Architecture**: Monolithic (no decomposition)

## Executive Summary

This plan implements v1.9.0 "Better Workflow Support" features to enable incremental spec building, automatic checkpoints, and progress tracking. The implementation adds three core subsystems (TierManager, CheckpointManager, IncrementalBuilder) plus three tiered template files, integrated with the existing CLI framework. Estimated timeline: 12 days over 4 phases.

## Architecture Overview

### System Design Philosophy

**Incremental First**: All features designed to support gradual spec building
**Safety First**: Checkpoints before every risky operation
**LLM-Friendly**: Templates and outputs optimized for AI consumption

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Layer (main.py)                      │
│  Commands: pulse --tier, expand, spec add-section,          │
│            spec progress, checkpoint [create|list|restore]   │
└──────────────┬──────────────────────────────┬────────────────┘
               │                              │
       ┌───────▼────────┐           ┌────────▼───────┐
       │  TierManager   │           │ CheckpointMgr  │
       │  (tier_manager.py)         │ (checkpoints.py)│
       │                │           │                 │
       │ - expand_tier()│           │ - create()      │
       │ - get_tier()   │           │ - list()        │
       │ - validate()   │           │ - restore()     │
       └────────┬───────┘           └─────────┬───────┘
                │                             │
                └──────────┬──────────────────┘
                           │
                  ┌────────▼──────────┐
                  │ IncrementalBuilder│
                  │ (incremental.py)  │
                  │                   │
                  │ - add_section()   │
                  │ - get_progress()  │
                  │ - next_section()  │
                  └───────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Template System       │
              │   (Jinja2 + Resources)  │
              │                         │
              │ - spec-tier1.md         │
              │ - spec-tier2.md         │
              │ - spec-tier3.md         │
              └─────────────────────────┘
```

### Data Flow

1. **Tier Expansion Flow**:
   ```
   User: specpulse expand 003 --to-tier standard
   → CLI parses command
   → CheckpointManager.create("before-expand-to-standard")
   → TierManager.expand_tier(from="minimal", to="standard")
   → Read current spec, parse sections
   → Load target tier template
   → Merge content (preserve existing, add new)
   → IncrementalBuilder.update_progress()
   → Write updated spec with YAML frontmatter
   → Display diff and success message
   ```

2. **Section Addition Flow**:
   ```
   User: specpulse spec add-section 003 requirements
   → CLI parses command
   → CheckpointManager.create("before-add-requirements")
   → IncrementalBuilder.add_section("requirements")
   → Load section template from appropriate tier
   → Insert at correct position
   → Update progress metadata
   → Write updated spec
   ```

3. **Progress Tracking Flow**:
   ```
   User: specpulse spec progress 003
   → CLI parses command
   → IncrementalBuilder.get_progress(spec_file)
   → Parse YAML frontmatter
   → Analyze section completion (✓ ⚠️ ⭕)
   → Calculate percentage
   → Get next recommended section
   → Display visual progress
   ```

## Technology Stack

### Core Dependencies (Existing)
- **Python**: 3.11+ (existing requirement)
- **Click**: CLI framework (existing)
- **Rich**: Terminal formatting (existing)
- **Jinja2**: Template rendering (existing)
- **PyYAML**: YAML parsing (existing)
- **GitPython**: Optional git integration (existing)

### New Modules (To Create)
- `specpulse/core/tier_manager.py`: Tier transition logic
- `specpulse/core/checkpoints.py`: Checkpoint lifecycle management
- `specpulse/core/incremental.py`: Section-by-section building
- `specpulse/resources/templates/spec-tier[1-3].md`: Tiered templates

### Development Tools
- **pytest**: Unit and integration testing (existing)
- **black**: Code formatting (existing)
- **mypy**: Type checking (existing)
- **flake8**: Linting (existing)

## Detailed Implementation Plan

### Phase 0: Template Preparation (2 days)

**Goal**: Create three tiered template files with LLM guidance

#### Tasks

**T001: Create Minimal Tier Template (spec-tier1.md)** [4 hours]
- **Description**: Design and implement minimal tier with 3 sections
- **Sections**:
  1. **What**: 1-sentence feature description
  2. **Why**: 1-sentence business value
  3. **Done When**: 3 acceptance checkboxes
- **LLM Guidance**: Add `<!-- LLM GUIDANCE -->` comments for each section
- **Acceptance**:
  - [ ] Template renders in 2-3 minutes
  - [ ] Contains exactly 3 sections
  - [ ] All sections have LLM guidance comments
  - [ ] Validates with existing validator
- **Files**: `specpulse/resources/templates/spec-tier1.md`

**T002: Create Standard Tier Template (spec-tier2.md)** [4 hours]
- **Description**: Extend minimal tier with 4-5 additional sections
- **New Sections**:
  1. **User Stories**: As a... I want... So that...
  2. **Functional Requirements**: FR-001, FR-002, etc.
  3. **Technical Approach**: High-level architecture
  4. **API Design**: Endpoints and contracts
  5. **Dependencies**: Internal and external
- **Content Preservation**: Include minimal tier sections at top
- **LLM Guidance**: Detailed comments explaining format, examples, common mistakes
- **Acceptance**:
  - [ ] Extends tier1 structure
  - [ ] 7-8 total sections
  - [ ] Renders in 10-15 minutes
  - [ ] LLM guidance for all new sections
- **Files**: `specpulse/resources/templates/spec-tier2.md`

**T003: Create Complete Tier Template (spec-tier3.md)** [4 hours]
- **Description**: Production-grade template with all sections
- **New Sections** (beyond standard):
  1. **Security Considerations**: Auth, encryption, threats
  2. **Performance Requirements**: SLAs, load targets
  3. **Monitoring & Alerts**: Metrics, dashboards
  4. **Rollback Strategy**: Deployment safety
  5. **Operational Runbook**: Support procedures
  6. **Compliance**: GDPR, SOC2, etc. if applicable
  7. **Cost Analysis**: Infrastructure estimates
  8. **Migration Strategy**: For existing systems
- **Acceptance**:
  - [ ] 15+ sections total
  - [ ] Renders in 30-45 minutes
  - [ ] Production-ready detail level
  - [ ] All sections have examples
- **Files**: `specpulse/resources/templates/spec-tier3.md`

**T004: Define Section Progression Map** [2 hours]
- **Description**: Create mapping of sections to tiers
- **Data Structure**:
  ```python
  SECTION_TIER_MAP = {
      "what": 1,
      "why": 1,
      "done_when": 1,
      "user_stories": 2,
      "functional_requirements": 2,
      "technical_approach": 2,
      "api_design": 2,
      "dependencies": 2,
      "security": 3,
      "performance": 3,
      # ... etc
  }
  ```
- **Acceptance**:
  - [ ] All sections mapped to tiers
  - [ ] Used for validation and tier checks
  - [ ] Documented in code
- **Files**: `specpulse/core/tier_constants.py` (new)

**T005: Test Template Rendering** [2 hours]
- **Description**: Validate templates render correctly with Jinja2
- **Tests**:
  - Render each tier with sample data
  - Verify section order
  - Check LLM guidance preserved
  - Validate YAML frontmatter structure
- **Acceptance**:
  - [ ] All three tiers render without errors
  - [ ] Variables replaced correctly
  - [ ] LLM comments not rendered to final output
- **Files**: `tests/test_tiered_templates.py` (new)

---

### Phase 1: Tier Manager (3 days)

**Goal**: Implement tier transition logic with content preservation

#### Tasks

**T006: Create TierManager Class** [6 hours]
- **Description**: Core class for managing tier transitions
- **Class Structure**:
  ```python
  class TierManager:
      def __init__(self, project_root: Path):
          self.project_root = project_root
          self.templates_dir = project_root / "templates"

      def get_current_tier(self, spec_file: Path) -> str:
          """Parse YAML frontmatter to get current tier"""

      def expand_tier(self, spec_file: Path, target_tier: str) -> ExpandResult:
          """Expand spec from current tier to target tier"""

      def validate_tier(self, spec_file: Path, tier: str) -> bool:
          """Validate spec matches tier requirements"""

      def preview_expansion(self, spec_file: Path, target_tier: str) -> str:
          """Show diff preview before expansion"""
  ```
- **Acceptance**:
  - [ ] Class instantiates correctly
  - [ ] All methods have type hints
  - [ ] Docstrings complete
  - [ ] No external state (pure functions)
- **Files**: `specpulse/core/tier_manager.py` (new)

**T007: Implement Content Preservation Logic** [8 hours]
- **Description**: Ensure user content never lost during expansion
- **Algorithm**:
  1. Parse current spec into sections
  2. Extract user content from each section
  3. Load target tier template
  4. Map existing sections to new structure
  5. Merge: existing content + new template sections
  6. Validate no data loss (hash comparison)
- **Edge Cases**:
  - Custom sections user added
  - Modified section headers
  - Multi-line content with special chars
  - Empty sections vs. missing sections
- **Acceptance**:
  - [ ] 100% content preservation (verified by tests)
  - [ ] Handles all edge cases
  - [ ] Shows diff before committing
  - [ ] Rollback available if validation fails
- **Files**: `specpulse/core/tier_manager.py` (expand_tier method)

**T008: Add CLI Command: specpulse expand** [4 hours]
- **Description**: User-facing command for tier expansion
- **Command Signature**:
  ```bash
  specpulse expand <feature-id> --to-tier <standard|complete> [--preview]
  ```
- **Options**:
  - `--preview`: Show diff without applying
  - `--no-checkpoint`: Skip automatic checkpoint (not recommended)
- **Output**:
  - Checkpoint created message
  - Diff preview (before/after)
  - Section count (3→7 or 7→15)
  - Progress update (43% complete)
- **Acceptance**:
  - [ ] Command works with all tier combinations
  - [ ] Preview mode shows diff correctly
  - [ ] Error messages clear and actionable
  - [ ] Success message shows what changed
- **Files**: `specpulse/cli/main.py` (add expand command)

**T009: Integration with Checkpoint System** [4 hours]
- **Description**: Auto-create checkpoint before expansion
- **Integration Points**:
  - Before expand_tier() execution
  - Checkpoint named: `before-expand-to-{target_tier}`
  - Rollback available immediately
- **Error Handling**:
  - If checkpoint fails, abort expansion
  - If expansion fails, restore from checkpoint
  - Preserve backup in temp directory
- **Acceptance**:
  - [ ] Checkpoint always created before expansion
  - [ ] Rollback works correctly
  - [ ] Error messages guide user to recovery
- **Files**: `specpulse/core/tier_manager.py`, `specpulse/core/checkpoints.py`

**T010: Unit Tests for TierManager** [2 hours]
- **Test Coverage**:
  - Tier detection from YAML frontmatter
  - Content preservation (all sections)
  - Invalid tier transitions (error handling)
  - Preview generation
  - Edge cases (empty sections, custom sections)
- **Acceptance**:
  - [ ] 90%+ code coverage
  - [ ] All edge cases tested
  - [ ] Fast execution (< 5 seconds total)
- **Files**: `tests/test_tier_manager.py` (new)

---

### Phase 2: Checkpoint System (2 days)

**Goal**: Automatic versioning and rollback capability

#### Tasks

**T011: Create CheckpointManager Class** [4 hours]
- **Description**: Manage checkpoint lifecycle
- **Class Structure**:
  ```python
  class CheckpointManager:
      def __init__(self, project_root: Path):
          self.project_root = project_root
          self.checkpoints_dir = project_root / ".specpulse" / "checkpoints"

      def create(self, feature_id: str, description: str) -> str:
          """Create checkpoint, return checkpoint name"""

      def list(self, feature_id: str) -> List[CheckpointInfo]:
          """List all checkpoints for feature"""

      def restore(self, feature_id: str, checkpoint_name: str) -> None:
          """Restore spec to checkpoint state"""

      def cleanup(self, feature_id: str, older_than_days: int = 30) -> int:
          """Delete old checkpoints, return count deleted"""
  ```
- **Storage Structure**:
  ```
  .specpulse/checkpoints/
    003-feature-name/
      checkpoint-001.spec.md         (spec snapshot)
      checkpoint-001.meta.yaml       (metadata)
      checkpoint-002.spec.md
      checkpoint-002.meta.yaml
  ```
- **Acceptance**:
  - [ ] Checkpoints created atomically
  - [ ] Metadata includes timestamp, tier, progress
  - [ ] Directory created if missing
- **Files**: `specpulse/core/checkpoints.py` (new)

**T012: Implement Checkpoint Storage** [3 hours]
- **Description**: File-based checkpoint storage with metadata
- **Metadata Format** (YAML):
  ```yaml
  created: 2025-10-06T16:30:00
  description: "Before adding security section"
  spec_file: spec-001.md
  tier: standard
  progress: 0.45
  sections_completed: ["what", "why", "user_stories"]
  file_hash: abc123def456  # SHA-256 of spec file
  ```
- **Validation**:
  - Verify file integrity using hash
  - Check file size < 10MB
  - Validate YAML structure
- **Acceptance**:
  - [ ] Checkpoint files written correctly
  - [ ] Metadata complete and valid
  - [ ] Hash verification works
- **Files**: `specpulse/core/checkpoints.py` (create method)

**T013: Implement Checkpoint Restoration** [3 hours]
- **Description**: Restore spec to previous checkpoint
- **Algorithm**:
  1. Validate checkpoint exists and is valid
  2. Create safety backup of current state
  3. Copy checkpoint file to spec location
  4. Update YAML frontmatter with checkpoint metadata
  5. Verify restoration (hash check)
- **Safety**:
  - Always create backup before restore
  - Show diff preview before applying
  - Confirm with user (unless --force)
- **Acceptance**:
  - [ ] Restoration is atomic (complete or rollback)
  - [ ] Current state backed up
  - [ ] User sees diff before applying
- **Files**: `specpulse/core/checkpoints.py` (restore method)

**T014: Add CLI Commands for Checkpoints** [4 hours]
- **Commands**:
  ```bash
  # Manual checkpoint
  specpulse checkpoint <feature-id> "description"

  # List checkpoints
  specpulse checkpoint list <feature-id>

  # Restore checkpoint
  specpulse checkpoint restore <feature-id> <checkpoint-name>

  # Cleanup old checkpoints
  specpulse checkpoint cleanup <feature-id> [--older-than-days 30]
  ```
- **Output Examples**:
  ```
  $ specpulse checkpoint list 003
  Checkpoints for 003-better-workflow-support:
    checkpoint-001: initial-minimal-spec (2025-10-06 16:00) [minimal, 100%]
    checkpoint-002: before-expand-to-standard (2025-10-06 16:10) [minimal, 100%]
    checkpoint-003: before-add-requirements (2025-10-06 16:15) [standard, 43%]
  ```
- **Acceptance**:
  - [ ] All commands work correctly
  - [ ] Output formatted with Rich tables
  - [ ] Error messages helpful
- **Files**: `specpulse/cli/main.py` (add checkpoint command group)

**T015: Unit Tests for CheckpointManager** [2 hours]
- **Test Coverage**:
  - Checkpoint creation
  - Metadata validation
  - Restoration (happy path + errors)
  - Cleanup (date-based deletion)
  - Concurrent access (if applicable)
- **Acceptance**:
  - [ ] 90%+ code coverage
  - [ ] Edge cases tested
  - [ ] Performance acceptable (< 1s per operation)
- **Files**: `tests/test_checkpoints.py` (new)

---

### Phase 3: Incremental Building (3 days)

**Goal**: Section-by-section spec building with progress tracking

#### Tasks

**T016: Create IncrementalBuilder Class** [5 hours]
- **Description**: Core class for incremental spec building
- **Class Structure**:
  ```python
  class IncrementalBuilder:
      def __init__(self, project_root: Path):
          self.project_root = project_root
          self.section_map = load_section_tier_map()

      def add_section(self, spec_file: Path, section_name: str) -> AddResult:
          """Add individual section to spec"""

      def get_progress(self, spec_file: Path) -> ProgressInfo:
          """Calculate completion percentage and section status"""

      def get_next_section(self, spec_file: Path) -> Optional[str]:
          """Recommend next section to work on"""

      def get_section_template(self, section_name: str) -> str:
          """Load section template with LLM guidance"""
  ```
- **Acceptance**:
  - [ ] All methods implemented
  - [ ] Type hints complete
  - [ ] Handles missing sections gracefully
- **Files**: `specpulse/core/incremental.py` (new)

**T017: Implement Section Addition** [5 hours]
- **Description**: Add individual sections to specs incrementally
- **Algorithm**:
  1. Validate section name exists in SECTION_TIER_MAP
  2. Check if section's tier <= current spec tier (warn if not)
  3. Load section template from appropriate tier
  4. Find insertion point in spec (maintain section order)
  5. Insert section with LLM guidance comments
  6. Update YAML frontmatter progress
- **Edge Cases**:
  - Section already exists (skip or warn)
  - Section requires higher tier (suggest expand)
  - Custom sections (allow but don't track in progress)
- **Acceptance**:
  - [ ] Sections inserted in correct order
  - [ ] LLM guidance included
  - [ ] Progress updated correctly
  - [ ] Handles all edge cases
- **Files**: `specpulse/core/incremental.py` (add_section method)

**T018: Implement Progress Calculation** [4 hours]
- **Description**: Calculate spec completion percentage
- **Algorithm**:
  1. Parse YAML frontmatter for tier and sections_completed
  2. Get expected sections for current tier
  3. Analyze each section:
     - ✓ Complete: Has user content (not template placeholders)
     - ⚠️ Partial: Has some content but incomplete
     - ⭕ Not started: Only template or empty
  4. Calculate: completed / total * 100
- **Weighting Strategy** (resolve open question):
  - **Option A**: Equal weight (simple, clear)
  - **Option B**: Weighted by complexity (more accurate)
  - **Decision**: Use equal weight initially, add complexity weighting in v1.9.1
- **Acceptance**:
  - [ ] Percentage accurate
  - [ ] Section status correct
  - [ ] Fast calculation (< 500ms)
- **Files**: `specpulse/core/incremental.py` (get_progress method)

**T019: Implement Next Section Recommendation** [3 hours]
- **Description**: Suggest which section to work on next
- **Algorithm**:
  1. Get all sections for current tier
  2. Filter: incomplete sections
  3. Sort by: dependency order (e.g., "what" before "user_stories")
  4. Return: first incomplete section
- **Recommendation Logic**:
  - If minimal tier 100% complete → suggest "expand to standard"
  - If standard tier 100% complete → suggest "expand to complete" or "ready for plan"
  - Otherwise → next incomplete section
- **Acceptance**:
  - [ ] Recommendations logical
  - [ ] Handles all tier states
  - [ ] Clear actionable suggestions
- **Files**: `specpulse/core/incremental.py` (get_next_section method)

**T020: Add CLI Commands for Incremental Building** [4 hours]
- **Commands**:
  ```bash
  # Add section
  specpulse spec add-section <feature-id> <section-name>

  # Show progress
  specpulse spec progress <feature-id>
  ```
- **Output Examples**:
  ```
  $ specpulse spec progress 003

  📊 Specification Progress: 003-better-workflow-support
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Current Tier: Standard (7 sections)
  Overall Progress: 57% complete

  ✅ Completed Sections (4/7)
    ✓ What: "Incremental spec building with tiers"
    ✓ Why: "Eliminate overwhelm"
    ✓ Done When: 3 acceptance criteria defined
    ✓ User Stories: 5 stories complete

  ⚠️  In Progress (1/7)
    ⏳ Functional Requirements: 3 of 8 requirements defined

  ⭕ Not Started (2/7)
    • Technical Approach
    • API Design

  🎯 Recommended Next Steps
  1. Complete Functional Requirements (add 5 more)
  2. Add Technical Approach section
  3. Define API Design

  💡 Tip: Ready to plan implementation? Run /sp-plan
  ```
- **Acceptance**:
  - [ ] Visual output clear and actionable
  - [ ] Colors/emojis used effectively
  - [ ] Time estimates shown
- **Files**: `specpulse/cli/main.py` (add spec subcommands)

**T021: Unit Tests for IncrementalBuilder** [3 hours]
- **Test Coverage**:
  - Section addition (all tiers)
  - Progress calculation (various completion levels)
  - Next section recommendation
  - Edge cases (empty specs, invalid sections)
- **Acceptance**:
  - [ ] 90%+ code coverage
  - [ ] All edge cases tested
  - [ ] Performance acceptable
- **Files**: `tests/test_incremental.py` (new)

---

### Phase 4: Integration & Testing (2 days)

**Goal**: End-to-end workflow validation and documentation

#### Tasks

**T022: Integration Tests for Complete Workflows** [6 hours]
- **Description**: Test full user workflows end-to-end
- **Workflow 1: Minimal → Standard → Complete**:
  ```python
  def test_tier_progression():
      # Initialize with minimal tier
      run_command("specpulse pulse test-feature --tier minimal")

      # Fill minimal spec
      update_spec("003-test-feature", "what", "User authentication")
      update_spec("003-test-feature", "why", "Security requirement")
      update_spec("003-test-feature", "done_when", ["Users can login", ...])

      # Verify 100% progress at minimal
      progress = get_progress("003-test-feature")
      assert progress.percentage == 1.0
      assert progress.tier == "minimal"

      # Expand to standard
      run_command("specpulse expand 003 --to-tier standard")

      # Verify content preserved
      spec_content = read_spec("003-test-feature/spec-001.md")
      assert "User authentication" in spec_content

      # Verify new sections added
      assert progress.sections_count == 7
      assert progress.percentage < 1.0  # Now incomplete
  ```
- **Workflow 2: Section-by-Section Building**:
  - Start minimal
  - Add sections one at a time
  - Verify progress updates
  - Check next section recommendations
- **Workflow 3: Checkpoint and Rollback**:
  - Create spec
  - Make changes with checkpoints
  - Restore to earlier checkpoint
  - Verify content matches checkpoint
- **Acceptance**:
  - [ ] All workflows pass
  - [ ] No data loss detected
  - [ ] Performance acceptable (< 30s per workflow)
- **Files**: `tests/integration/test_v190_workflow.py` (new)

**T023: Update /sp-pulse to Support --tier Flag** [3 hours]
- **Description**: Modify initialization to accept tier parameter
- **Command**:
  ```bash
  /sp-pulse new-feature --tier minimal    # Default
  /sp-pulse new-feature --tier standard
  /sp-pulse new-feature --tier complete
  ```
- **Behavior**:
  - Copy appropriate tier template to specs/
  - Set YAML frontmatter: `tier: minimal`
  - Display tier-appropriate instructions
- **Acceptance**:
  - [ ] Flag works for all tiers
  - [ ] Default is minimal (if not specified)
  - [ ] Documentation updated
- **Files**: `scripts/sp-pulse-init.sh`, `specpulse/cli/main.py`

**T024: Update Validator for Tier-Aware Validation** [3 hours]
- **Description**: Validator respects current tier when checking completeness
- **Logic**:
  - Parse spec YAML frontmatter for tier
  - Load expected sections for that tier
  - Validate only sections relevant to current tier
  - Suggest expansion if user needs more
- **Example**:
  - Minimal tier: Only validate What/Why/Done When
  - Standard tier: Validate 7-8 sections
  - Complete tier: Validate all 15+ sections
- **Acceptance**:
  - [ ] Validation tier-aware
  - [ ] Messages suggest next steps
  - [ ] No false positives/negatives
- **Files**: `specpulse/core/validator.py` (update validation logic)

**T025: Error Handling and Edge Cases** [2 hours]
- **Description**: Comprehensive error handling
- **Scenarios**:
  - Checkpoint directory read-only
  - Spec file corrupted
  - Invalid tier in frontmatter
  - Concurrent access (two processes)
  - Disk full during checkpoint
- **Error Messages**:
  - Clear description of what went wrong
  - Actionable recovery steps
  - Command to undo if applicable
- **Acceptance**:
  - [ ] All error scenarios handled
  - [ ] Messages helpful and clear
  - [ ] No data loss on errors
- **Files**: All core modules (tier_manager, checkpoints, incremental)

**T026: Documentation Updates** [4 hours]
- **Documents to Update**:
  1. **README.md**: Add workflow examples
  2. **CLAUDE.md**: Update with tier instructions
  3. **CHANGELOG.md**: Document v1.9.0 features
  4. **help commands**: Add tier, expand, checkpoint docs
- **Example Content**:
  ```markdown
  ## Tiered Templates (v1.9.0)

  Start minimal (2-3 min), expand when ready:

  $ specpulse pulse new-feature --tier minimal
  $ /sp-spec "What: User auth. Why: Security. Done When: Login works"
  $ specpulse expand 003 --to-tier standard
  ```
- **Acceptance**:
  - [ ] All docs updated
  - [ ] Examples tested and working
  - [ ] Help text accurate
- **Files**: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `specpulse/cli/help/`

**T027: Performance Benchmarking** [2 hours]
- **Description**: Verify performance requirements met
- **Benchmarks**:
  - Tier expansion: < 2 seconds (requirement: < 2s)
  - Checkpoint creation: < 1 second (requirement: < 1s)
  - Progress calculation: < 500ms (requirement: < 500ms)
- **Test Method**:
  - Run operations 10 times
  - Calculate mean and p95
  - Fail if any exceed requirements
- **Acceptance**:
  - [ ] All benchmarks pass
  - [ ] Performance documented
  - [ ] No regressions from baseline
- **Files**: `tests/performance/test_v190_performance.py` (new)

**T028: Cross-Platform Testing** [2 hours]
- **Description**: Validate on Windows, Linux, macOS
- **Test Matrix**:
  - Windows 11 + PowerShell
  - Ubuntu 22.04 + Bash
  - macOS 13+ + Bash
- **Focus Areas**:
  - Path handling (Windows backslashes)
  - Shell script execution
  - File permissions
- **Acceptance**:
  - [ ] All tests pass on all platforms
  - [ ] No platform-specific issues
- **Files**: CI/CD configuration (.github/workflows/)

---

## Testing Strategy

### Unit Tests
- **Target Coverage**: 90%+
- **Files**: `tests/test_tier_manager.py`, `test_checkpoints.py`, `test_incremental.py`
- **Focus**: Individual methods, edge cases, error handling

### Integration Tests
- **Target Coverage**: Core workflows
- **Files**: `tests/integration/test_v190_workflow.py`
- **Focus**: End-to-end user scenarios

### Performance Tests
- **Benchmarks**: Tier expansion, checkpoint creation, progress calculation
- **Files**: `tests/performance/test_v190_performance.py`
- **Thresholds**: 2s, 1s, 500ms respectively

### Manual Tests
- **LLM Interaction**: Test with Claude Code
- **Cross-Platform**: Windows, Linux, macOS
- **Edge Cases**: Large specs, special characters, concurrent operations

## Deployment Strategy

### Package Updates
1. Update version in `specpulse/_version.py`: `1.9.0`
2. Add new templates to `specpulse/resources/templates/`
3. Update `pyproject.toml` package data includes

### Rollout Plan
1. **Alpha Release**: Internal testing, feedback loop
2. **Beta Release**: Select users, gather metrics
3. **Stable Release**: General availability

### Backward Compatibility
- Existing specs continue to work (no tier = treated as complete)
- Auto-migration: Add tier to existing specs on first access
- Feature flag: `SPECPULSE_ENABLE_TIERS=true` (default enabled)

### Rollback Strategy
If critical issues found:
1. Release v1.9.1 with fixes
2. OR revert to v1.8.0 (no data loss)
3. Checkpoints preserved, can restore manually

## Security Considerations

### Checkpoint Storage
- **Location**: `.specpulse/checkpoints/` (local, not committed by default)
- **Permissions**: User-only read/write (0600)
- **Gitignore**: Add to default .gitignore template

### File Operations
- **Atomic writes**: Use temp file + rename pattern
- **Validation**: Hash check before/after operations
- **Sandboxing**: Never execute user content

### Input Validation
- Feature IDs: Alphanumeric + hyphens only
- Section names: Whitelist from SECTION_TIER_MAP
- File paths: Prevent directory traversal

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Load templates only when needed
2. **Caching**: Cache parsed YAML frontmatter (< 1MB)
3. **Incremental Parsing**: Don't re-parse entire spec for progress

### Resource Limits
- Maximum checkpoint size: 10MB
- Maximum checkpoints per feature: 100 (auto-cleanup)
- Maximum spec file size: 5MB (warning beyond)

### Monitoring
- Track operation duration (add to telemetry)
- Monitor checkpoint storage usage
- Alert if operations exceed thresholds

## Risk Mitigation

| Risk | Mitigation | Owner | Status |
|------|------------|-------|--------|
| Checkpoint corruption | Validate on create, store metadata separately | Phase 2 | Planned |
| Content loss during expansion | Diff preview, automatic backups, comprehensive tests | Phase 1 | Planned |
| Performance issues with large specs | Lazy loading, incremental parsing, size limits | Phase 4 | Planned |
| Backward compatibility breakage | Auto-migration, feature flag, existing tests pass | Phase 4 | Planned |
| User confusion about tiers | Clear docs, examples, in-CLI help | Phase 4 | Planned |

## Success Metrics

### Quantitative Metrics
- [ ] Spec creation time: 15 min → 3 min (80% reduction)
- [ ] Tier expansion: < 2 seconds (100% of operations)
- [ ] Checkpoint creation: < 1 second (100% of operations)
- [ ] Progress calculation: < 500ms (100% of operations)
- [ ] Test coverage: 90%+ (all new modules)
- [ ] All 377+ existing tests pass (zero regressions)

### Qualitative Metrics
- [ ] Users report "less overwhelm" (survey feedback)
- [ ] LLMs can use commands without clarification
- [ ] Documentation clear and sufficient
- [ ] Error messages helpful and actionable

## Timeline and Milestones

### Phase 0: Template Preparation
- **Duration**: 2 days
- **Deliverables**: 3 tiered templates, section map, rendering tests
- **Milestone**: Templates validated and merged

### Phase 1: Tier Manager
- **Duration**: 3 days
- **Deliverables**: TierManager class, expand command, unit tests
- **Milestone**: Tier expansion working end-to-end

### Phase 2: Checkpoint System
- **Duration**: 2 days
- **Deliverables**: CheckpointManager class, CLI commands, unit tests
- **Milestone**: Checkpoints creating and restoring correctly

### Phase 3: Incremental Building
- **Duration**: 3 days
- **Deliverables**: IncrementalBuilder class, CLI commands, unit tests
- **Milestone**: Section addition and progress tracking working

### Phase 4: Integration & Testing
- **Duration**: 2 days
- **Deliverables**: Integration tests, docs, performance benchmarks
- **Milestone**: v1.9.0 ready for release

**Total Duration**: 12 days (2 weeks)

## Dependencies and Prerequisites

### Internal Dependencies
- ✅ Existing template system (v1.5.0)
- ✅ Validator (v1.5.0)
- ✅ CLI framework (v1.5.0)
- ✅ Console utilities (v1.5.0)

### External Dependencies
- ✅ Jinja2 (already in requirements)
- ✅ Rich (already in requirements)
- ✅ PyYAML (already in requirements)
- ⚠️ GitPython (optional, already in requirements)

### Prerequisite Features
- None (standalone feature)

## Open Questions and Decisions

### Question 1: Tier Expansion Reversibility
- **Question**: Should tier expansion be reversible? (complete → standard)
- **Options**:
  - A: No, only forward progression (simpler)
  - B: Yes, with content truncation warning (more flexible)
- **Recommendation**: Start with A (forward only), add B in v1.9.1 if requested
- **Decision**: **DEFERRED** - Start with A, gather feedback

### Question 2: Checkpoint Retention
- **Question**: Maximum number of checkpoints to retain per feature?
- **Options**:
  - A: 10 (minimal storage)
  - B: 30 (more history)
  - C: Unlimited with auto-cleanup after 30 days
- **Recommendation**: C - Best balance of safety and storage
- **Decision**: **C - Unlimited with 30-day auto-cleanup**

### Question 3: Progress Weighting
- **Question**: Should progress percentage weight all sections equally?
- **Options**:
  - A: Equal weight (simple, clear)
  - B: Weighted by complexity (e.g., "what" = 1 point, "security" = 5 points)
- **Recommendation**: A initially, add B in v1.9.1 if users request
- **Decision**: **A - Equal weight** (revisit in v1.9.1)

### Question 4: Git Integration for Checkpoints
- **Question**: Store checkpoints in git history or separate storage?
- **Options**:
  - A: Git commits (version control integrated)
  - B: File system (simpler, faster)
- **Recommendation**: B - File system (git optional via GitPython)
- **Decision**: **B - File system** (git hooks optional for advanced users)

## Architecture Decision Records

### ADR-001: Tiered Template Architecture
- **Date**: 2025-10-06
- **Status**: Approved
- **Context**: Need to support incremental spec building without overwhelming users
- **Decision**: Three-tier template system (minimal/standard/complete)
- **Rationale**:
  - Minimal (3 sections) enables 2-3 minute quick starts
  - Standard (7-8 sections) provides implementation-ready detail
  - Complete (15+ sections) ensures production-grade specifications
- **Consequences**:
  - Positive: Users can start fast, expand when ready
  - Negative: Must maintain three template versions
- **Alternatives Considered**: Single template with optional sections (rejected: still overwhelming)

### ADR-002: Checkpoint Storage Strategy
- **Date**: 2025-10-06
- **Status**: Approved
- **Context**: Need rollback capability without git dependency
- **Decision**: File-based checkpoint storage in `.specpulse/checkpoints/`
- **Rationale**:
  - Simple implementation
  - No external dependencies
  - Fast creation and restoration (< 1s)
- **Consequences**:
  - Positive: Works without git, simple to implement
  - Negative: Requires disk space, manual cleanup
- **Alternatives Considered**: Git commits (rejected: requires git, slower)

### ADR-003: Progress Calculation Algorithm
- **Date**: 2025-10-06
- **Status**: Approved
- **Context**: Users need to know "how complete" their spec is
- **Decision**: Equal-weight progress calculation (completed / total * 100)
- **Rationale**:
  - Simple to understand and implement
  - Fast calculation (< 500ms)
  - Easy to explain to users and LLMs
- **Consequences**:
  - Positive: Clear, predictable, fast
  - Negative: Doesn't account for section complexity
- **Future Enhancement**: Add complexity weighting in v1.9.1 if requested

### ADR-004: YAML Frontmatter for Metadata
- **Date**: 2025-10-06
- **Status**: Approved
- **Context**: Need to store tier and progress in spec files
- **Decision**: Use YAML frontmatter at top of markdown files
- **Rationale**:
  - Standard markdown convention
  - Easy to parse with PyYAML
  - Human-readable and editable
- **Consequences**:
  - Positive: Standard, simple, editable
  - Negative: Must parse frontmatter on every read
- **Alternatives Considered**: Sidecar JSON files (rejected: separate file management)

## Appendix

### Example YAML Frontmatter
```yaml
---
tier: standard
progress: 0.57
sections_completed:
  - what
  - why
  - done_when
  - user_stories
sections_partial:
  - functional_requirements
last_checkpoint: before-add-requirements
last_updated: 2025-10-06T16:30:00
---
```

### Example Checkpoint Metadata
```yaml
# .specpulse/checkpoints/003-better-workflow-support/checkpoint-002.meta.yaml
created: 2025-10-06T16:10:00
description: "Before expanding to standard tier"
spec_file: spec-001.md
tier: minimal
progress: 1.0
sections_completed:
  - what
  - why
  - done_when
file_hash: a1b2c3d4e5f6789012345678901234567890abcd
file_size_bytes: 2048
```

### Command Reference

```bash
# Initialize with tier
specpulse pulse new-feature --tier minimal    # 3 sections, 2-3 min
specpulse pulse new-feature --tier standard   # 7-8 sections, 10-15 min
specpulse pulse new-feature --tier complete   # 15+ sections, 30-45 min

# Expand tier (progressive)
specpulse expand 003 --to-tier standard       # minimal → standard
specpulse expand 003 --to-tier complete       # standard → complete
specpulse expand 003 --to-tier complete --preview  # Show diff only

# Section management
specpulse spec add-section 003 requirements   # Add one section
specpulse spec progress 003                   # Show progress

# Checkpoint management
specpulse checkpoint 003 "Before major changes"  # Manual checkpoint
specpulse checkpoint list 003                    # List all checkpoints
specpulse checkpoint restore 003 checkpoint-002  # Restore to checkpoint
specpulse checkpoint cleanup 003 --older-than-days 30  # Delete old

# Validation (tier-aware)
specpulse validate 003                        # Validates current tier only
```

### Related Files

**Specification**: `specs/003-better-workflow-support/spec-001.md`
**Roadmap**: `ROADMAP.md` (lines 407-487, v1.9.0 section)
**Examples**: `examples/v1.9.0-sp-pulse-example.md`, `examples/v1.9.0-sp-spec-example.md`
**Templates**: `specpulse/resources/templates/spec-tier[1-3].md` (to be created)

---

**Plan Status**: Ready for Implementation
**Next Step**: Begin Phase 0 (Template Preparation)
**Estimated Completion**: 2025-10-20 (12 working days from now)
