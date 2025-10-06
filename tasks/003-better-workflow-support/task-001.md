# Task Breakdown: Better Workflow Support (v1.9.0)

## Metadata
- **Feature ID**: 003
- **Feature Name**: better-workflow-support
- **Spec File**: specs/003-better-workflow-support/spec-001.md
- **Plan File**: plans/003-better-workflow-support/plan-001.md
- **Task Version**: 1.0.0
- **Generated**: 2025-10-06
- **Total Tasks**: 28
- **Total Phases**: 4
- **Estimated Duration**: 12 days (96 hours)

## Progress Tracking

```yaml
status:
  total: 28
  completed: 24
  in_progress: 0
  blocked: 4
  pending: 0

phases:
  phase_0:
    name: "Template Preparation"
    tasks: 5
    completed: 5
    duration_days: 2
  phase_1:
    name: "Tier Manager"
    tasks: 5
    completed: 3
    duration_days: 3
    notes: "TierManager already existed from v1.6.0"
  phase_2:
    name: "Checkpoint System"
    tasks: 5
    completed: 5
    duration_days: 2
  phase_3:
    name: "Incremental Building"
    tasks: 6
    completed: 5
    duration_days: 3
  phase_4:
    name: "Integration & Testing"
    tasks: 7
    completed: 3
    duration_days: 2
    notes: "Full integration tests pending, core functionality working"

metrics:
  estimated_velocity: "2-3 tasks/day"
  completion_percentage: 86
  estimated_completion: "2025-10-20"
  actual_completion: "2025-10-06"
  status: "SHIPPED - v1.9.0 released with core features"

sdd_gates:
  specification_first: true
  task_decomposition: true
  quality_assurance: pending
  traceable_implementation: true
```

## Critical Path

The following tasks form the critical path (must be completed sequentially):

```
T001 → T002 → T003 → T004 → T005 (Phase 0)
  ↓
T006 → T007 → T008 → T009 (Phase 1)
  ↓
T011 → T012 → T013 → T014 (Phase 2)
  ↓
T016 → T017 → T018 → T019 → T020 (Phase 3)
  ↓
T022 → T023 → T024 (Phase 4)
```

**Critical Path Duration**: 10 days (80 hours)

## Parallel Execution Groups

Tasks that CAN be executed in parallel:

**Group A (Phase 0)**: T001, T002, T003 [P]
- All template creation tasks are independent
- Can be done simultaneously by different team members or LLM sessions

**Group B (Phase 1)**: T010 (testing can start while T009 is being finalized) [P]

**Group C (Phase 2)**: T015 (testing can run parallel to T014) [P]

**Group D (Phase 3)**: T021 (testing can run parallel to T020) [P]

**Group E (Phase 4)**: T025, T026, T027, T028 [P]
- Final integration tasks can run in parallel

---

## Phase 0: Template Preparation (2 days, 16 hours)

**Goal**: Create three tiered template files with LLM guidance

### T001: Create Minimal Tier Template (spec-tier1.md)

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: None
- **Parallel**: [P] - Can run with T002, T003

**Description**:
Design and implement minimal tier template with 3 sections (What/Why/Done When). Add LLM guidance comments to each section to guide AI assistants on what content to generate.

**Sections to Create**:
1. **What**: 1-sentence feature description with guidance on brevity
2. **Why**: 1-sentence business value with guidance on user benefit
3. **Done When**: 3 acceptance checkboxes with guidance on testability

**LLM Guidance Requirements**:
- Each section needs `<!-- LLM GUIDANCE: ... -->` comments
- Guidance should explain: what to write, format, length, examples
- Include common mistakes to avoid
- Provide good/bad examples

**Acceptance Criteria**:
- [ ] Template file created at `specpulse/resources/templates/spec-tier1.md`
- [ ] Contains exactly 3 sections
- [ ] All sections have LLM guidance comments
- [ ] Template renders in 2-3 minutes when filled
- [ ] Validates with existing validator (no errors)
- [ ] YAML frontmatter includes `tier: minimal`

**Files to Create**:
- `specpulse/resources/templates/spec-tier1.md`

**Testing**:
- Manual: Fill out template and time completion (should be 2-3 min)
- Validation: Run through validator, expect zero errors
- Render: Process with Jinja2, verify LLM comments preserved

**Assignable**: developer, technical writer
**SDD Trace**: FR-001, FR-006

---

### T002: Create Standard Tier Template (spec-tier2.md)

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: None (though logically follows T001)
- **Parallel**: [P] - Can run with T001, T003

**Description**:
Extend minimal tier with 4-5 additional sections for implementation planning. Include all minimal tier sections at the top, then add new sections with detailed LLM guidance.

**New Sections to Add** (beyond minimal):
1. **User Stories**: As a... I want... So that... format
2. **Functional Requirements**: FR-001, FR-002 format with priorities
3. **Technical Approach**: High-level architecture description
4. **API Design**: Endpoints, contracts, data models
5. **Dependencies**: Internal and external dependencies

**Content Preservation**:
- Include all 3 minimal tier sections at top
- Maintain same section order as tier1
- Add note: "Expanded from minimal tier"

**LLM Guidance Requirements**:
- Detailed comments for each NEW section
- Format explanations (e.g., "Use FR-XXX: format")
- Examples of good user stories vs bad
- Common mistakes in requirements writing
- API design patterns (REST, GraphQL guidance)

**Acceptance Criteria**:
- [ ] Template file created at `specpulse/resources/templates/spec-tier2.md`
- [ ] Extends tier1 structure (includes all 3 minimal sections)
- [ ] Total of 7-8 sections
- [ ] Renders in 10-15 minutes when filled
- [ ] LLM guidance for all new sections
- [ ] YAML frontmatter includes `tier: standard`

**Files to Create**:
- `specpulse/resources/templates/spec-tier2.md`

**Testing**:
- Inheritance test: Verify tier1 sections present and identical
- Render test: Fill out and time (10-15 min target)
- Validation: Run through validator

**Assignable**: developer, technical writer
**SDD Trace**: FR-001, FR-006

---

### T003: Create Complete Tier Template (spec-tier3.md)

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: High
- **Dependencies**: None (though logically follows T002)
- **Parallel**: [P] - Can run with T001, T002

**Description**:
Production-grade template with all sections for enterprise/critical features. Include all standard tier sections plus 8 additional production-readiness sections.

**New Sections to Add** (beyond standard):
1. **Security Considerations**: Auth, encryption, threat model
2. **Performance Requirements**: SLAs, load targets, latency
3. **Monitoring & Alerts**: Metrics, dashboards, alerting rules
4. **Rollback Strategy**: Deployment safety, rollback procedures
5. **Operational Runbook**: Support procedures, on-call guides
6. **Compliance**: GDPR, SOC2, HIPAA if applicable
7. **Cost Analysis**: Infrastructure estimates, scaling costs
8. **Migration Strategy**: For existing systems, data migration

**Content Preservation**:
- Include all 7-8 standard tier sections
- Maintain consistent section order
- Add note: "Expanded from standard tier"

**LLM Guidance Requirements**:
- Enterprise-level guidance for each section
- Security best practices and threat modeling guidance
- Performance testing and SLA definition guidance
- Compliance checklist examples (GDPR, etc.)
- Cost estimation formulas and tools
- Migration planning patterns

**Acceptance Criteria**:
- [ ] Template file created at `specpulse/resources/templates/spec-tier3.md`
- [ ] Extends tier2 structure (includes all 7-8 standard sections)
- [ ] Total of 15+ sections
- [ ] Renders in 30-45 minutes when filled
- [ ] Production-ready detail level
- [ ] All sections have comprehensive examples
- [ ] YAML frontmatter includes `tier: complete`

**Files to Create**:
- `specpulse/resources/templates/spec-tier3.md`

**Testing**:
- Inheritance test: Verify tier2 sections present
- Production readiness: Review with security/ops teams
- Render test: Full completion timing (30-45 min)

**Assignable**: senior developer, architect, security engineer
**SDD Trace**: FR-001, FR-006

---

### T004: Define Section Progression Map

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 2 hours
- **Complexity**: Simple
- **Dependencies**: T001, T002, T003 (needs to know all sections)
- **Parallel**: NO - Sequential after template creation

**Description**:
Create Python constants file mapping section names to tier numbers. This will be used by TierManager and IncrementalBuilder to validate tier requirements and determine which sections belong to which tier.

**Data Structure**:
```python
SECTION_TIER_MAP = {
    # Tier 1 (Minimal)
    "what": 1,
    "why": 1,
    "done_when": 1,

    # Tier 2 (Standard) - adds these
    "user_stories": 2,
    "functional_requirements": 2,
    "technical_approach": 2,
    "api_design": 2,
    "dependencies": 2,

    # Tier 3 (Complete) - adds these
    "security": 3,
    "performance": 3,
    "monitoring": 3,
    "rollback_strategy": 3,
    "operational_runbook": 3,
    "compliance": 3,
    "cost_analysis": 3,
    "migration_strategy": 3,
}

TIER_SECTIONS = {
    1: ["what", "why", "done_when"],
    2: ["what", "why", "done_when", "user_stories", "functional_requirements",
        "technical_approach", "api_design", "dependencies"],
    3: [... all sections ...]
}
```

**Acceptance Criteria**:
- [ ] File created at `specpulse/core/tier_constants.py`
- [ ] All sections from tier1/2/3 templates mapped
- [ ] Mapping used for validation and tier checks
- [ ] Constants documented with docstrings
- [ ] Section order preserved (for insertion logic)

**Files to Create**:
- `specpulse/core/tier_constants.py`

**Testing**:
- Import test: Verify constants importable
- Completeness: Check all template sections mapped
- Order test: Verify section order matches templates

**Assignable**: developer
**SDD Trace**: FR-001, FR-003, FR-008

---

### T005: Test Template Rendering

- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 2 hours
- **Complexity**: Simple
- **Dependencies**: T001, T002, T003 (needs templates to exist)
- **Parallel**: NO - Sequential after templates created

**Description**:
Validate that all three tier templates render correctly with Jinja2. Create test file with sample data for each tier and verify output is correct.

**Test Cases**:
1. **Render Test**: Each tier renders without errors
2. **Variable Substitution**: All `{{variable}}` placeholders replaced
3. **Section Order**: Sections appear in correct order
4. **LLM Guidance**: Comments preserved in output (not stripped)
5. **YAML Frontmatter**: Valid YAML, correct tier value
6. **Inheritance**: Tier2 includes tier1, tier3 includes tier2

**Test Data**:
```python
tier1_data = {
    "feature_name": "test-feature",
    "what": "A test feature",
    "why": "Testing purposes",
    "done_when": ["Item 1", "Item 2", "Item 3"]
}
```

**Acceptance Criteria**:
- [ ] Test file created at `tests/test_tiered_templates.py`
- [ ] All three tiers render without errors
- [ ] Variables replaced correctly
- [ ] LLM comments preserved in output
- [ ] Section order validated
- [ ] Test passes with pytest

**Files to Create**:
- `tests/test_tiered_templates.py`

**Testing Commands**:
```bash
pytest tests/test_tiered_templates.py -v
pytest tests/test_tiered_templates.py --cov=specpulse/resources/templates
```

**Assignable**: developer, QA engineer
**SDD Trace**: FR-001, FR-006, Success Criteria

---

## Phase 1: Tier Manager (3 days, 24 hours)

**Goal**: Implement tier transition logic with content preservation

### T006: Create TierManager Class

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 6 hours
- **Complexity**: High
- **Dependencies**: T004 (needs SECTION_TIER_MAP)
- **Parallel**: NO - Sequential

**Description**:
Implement core class for managing tier transitions. This class will handle tier detection, expansion, validation, and preview generation.

**Class Structure**:
```python
class TierManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.templates_dir = project_root / "templates"
        self.section_map = SECTION_TIER_MAP

    def get_current_tier(self, spec_file: Path) -> str:
        """Parse YAML frontmatter to get current tier"""

    def expand_tier(self, spec_file: Path, target_tier: str) -> ExpandResult:
        """Expand spec from current tier to target tier"""

    def validate_tier(self, spec_file: Path, tier: str) -> bool:
        """Validate spec matches tier requirements"""

    def preview_expansion(self, spec_file: Path, target_tier: str) -> str:
        """Show diff preview before expansion"""
```

**Methods to Implement**:
1. `__init__`: Load templates, import constants
2. `get_current_tier`: Parse YAML, return tier string
3. `expand_tier`: Main expansion logic (implemented in T007)
4. `validate_tier`: Check all required sections present
5. `preview_expansion`: Generate before/after diff

**Acceptance Criteria**:
- [ ] File created at `specpulse/core/tier_manager.py`
- [ ] Class instantiates correctly
- [ ] All methods have type hints (Path, str, bool, etc.)
- [ ] Docstrings complete with examples
- [ ] No external state (pure functions where possible)
- [ ] Error handling for missing files

**Files to Create**:
- `specpulse/core/tier_manager.py`

**Testing**:
- Unit tests for each method
- Type checking with mypy
- Docstring validation

**Assignable**: senior developer
**SDD Trace**: FR-002, FR-007

---

### T007: Implement Content Preservation Logic

- **Type**: development
- **Priority**: CRITICAL
- **Estimate**: 8 hours
- **Complexity**: Very High
- **Dependencies**: T006 (needs TierManager class)
- **Parallel**: NO - Sequential

**Description**:
Implement the most critical feature: content preservation during tier expansion. This ensures user content is NEVER lost when expanding from one tier to another.

**Algorithm**:
1. Parse current spec into sections (using markdown parser)
2. Extract user content from each section (strip template placeholders)
3. Load target tier template
4. Map existing sections to new structure
5. Merge: existing content + new template sections
6. Validate no data loss (hash comparison before/after)
7. Return merged spec with YAML frontmatter updated

**Edge Cases to Handle**:
- Custom sections user added (preserve them)
- Modified section headers (match by content not header)
- Multi-line content with special characters (preserve formatting)
- Empty sections vs. missing sections (distinguish)
- Code blocks in sections (preserve fenced code)
- Lists and nested lists (preserve indentation)

**Content Detection**:
```python
def is_template_placeholder(content: str) -> bool:
    """Check if content is just template placeholder"""
    placeholders = [
        "[placeholder]",
        "[description]",
        "[TODO",
        "<!-- fill this in -->",
    ]
    return any(ph in content.lower() for ph in placeholders)
```

**Acceptance Criteria**:
- [ ] 100% content preservation (verified by tests)
- [ ] Handles all edge cases listed above
- [ ] Shows diff before committing changes
- [ ] Rollback available if validation fails
- [ ] Hash comparison confirms no data loss
- [ ] Performance: < 2 seconds for typical spec

**Files to Modify**:
- `specpulse/core/tier_manager.py` (expand_tier method)

**Testing**:
- Test with empty spec (baseline)
- Test with partially filled spec
- Test with custom sections
- Test with special characters
- Test hash before/after matching

**Assignable**: senior developer, architect
**SDD Trace**: FR-002, FR-007

---

### T008: Add CLI Command: specpulse expand

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: T007 (needs expand_tier working)
- **Parallel**: NO - Sequential

**Description**:
Create user-facing CLI command for tier expansion. Integrate with TierManager and provide rich terminal output.

**Command Signature**:
```bash
specpulse expand <feature-id> --to-tier <standard|complete> [--preview]
```

**Options**:
- `--to-tier`: Target tier (standard or complete)
- `--preview`: Show diff without applying changes
- `--no-checkpoint`: Skip automatic checkpoint (not recommended)

**Output Format**:
```
🚀 Expanding Specification Tier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From: Minimal (3 sections)
To: Standard (7 sections)

✨ Created checkpoint: before-expand-to-standard
   All your content is preserved!

📋 Content Preservation
  ✓ Keeping: What (already filled)
  ✓ Keeping: Why (already filled)
  ✓ Keeping: Done When (partially filled)

➕ Adding New Sections
  + User Stories (with LLM guidance)
  + Functional Requirements (with LLM guidance)
  + Technical Approach (with examples)
  + API Design (with template)
  + Dependencies (with checklist)

✅ Expansion Complete!

📊 New Structure: 003-feature
Progress: 43% complete (3/7 sections)

🎯 Next Steps
1. Fill User Stories section
2. Add Functional Requirements
3. Define Technical Approach
```

**Acceptance Criteria**:
- [ ] Command added to `specpulse/cli/main.py`
- [ ] Works with all tier combinations (minimal→standard, standard→complete)
- [ ] Preview mode shows diff correctly
- [ ] Error messages clear and actionable
- [ ] Success message shows what changed
- [ ] Uses Rich for colored output

**Files to Modify**:
- `specpulse/cli/main.py` (add expand command)

**Testing**:
- CLI integration test
- All tier combinations
- Preview mode test
- Error handling test

**Assignable**: developer
**SDD Trace**: FR-002

---

### T009: Integration with Checkpoint System

- **Type**: integration
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: T008, T011 (needs expand command and CheckpointManager)
- **Parallel**: NO - Sequential (needs both components)

**Description**:
Integrate automatic checkpoint creation before tier expansion. This ensures users can always rollback if expansion causes issues.

**Integration Points**:
1. **Before expand_tier() execution**: Create checkpoint
2. **Checkpoint naming**: `before-expand-to-{target_tier}`
3. **Rollback available**: Immediately after expansion
4. **Error handling**: If expansion fails, auto-restore

**Flow**:
```python
def expand(feature_id, target_tier):
    # 1. Create checkpoint
    checkpoint_mgr = CheckpointManager(project_root)
    checkpoint_name = checkpoint_mgr.create(
        feature_id,
        f"Before expanding to {target_tier}"
    )

    try:
        # 2. Perform expansion
        tier_mgr = TierManager(project_root)
        result = tier_mgr.expand_tier(spec_file, target_tier)

        # 3. Validate result
        if not result.success:
            raise ExpansionError(result.error)

    except Exception as e:
        # 4. Rollback on error
        checkpoint_mgr.restore(feature_id, checkpoint_name)
        raise
```

**Error Handling**:
- If checkpoint fails → abort expansion
- If expansion fails → restore from checkpoint
- Preserve backup in temp directory
- Log all operations for debugging

**Acceptance Criteria**:
- [ ] Checkpoint ALWAYS created before expansion
- [ ] Rollback works correctly on errors
- [ ] Error messages guide user to recovery
- [ ] Integration test passes
- [ ] No orphaned checkpoints

**Files to Modify**:
- `specpulse/core/tier_manager.py` (add checkpoint call)
- `specpulse/cli/main.py` (error handling)

**Testing**:
- Happy path: Expansion succeeds, checkpoint kept
- Error path: Expansion fails, rollback works
- Edge case: Checkpoint fails, expansion aborted

**Assignable**: developer
**SDD Trace**: FR-004, FR-007

---

### T010: Unit Tests for TierManager

- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 2 hours
- **Complexity**: Medium
- **Dependencies**: T006, T007 (needs TierManager implemented)
- **Parallel**: [P] - Can run parallel to T009

**Description**:
Comprehensive unit tests for TierManager class. Achieve 90%+ code coverage.

**Test Cases**:
1. **Tier Detection**:
   - Valid tier in frontmatter
   - Missing tier (default to complete)
   - Invalid tier (error handling)
2. **Content Preservation**:
   - All sections preserved
   - Custom sections preserved
   - Special characters handled
3. **Tier Transitions**:
   - Minimal → Standard
   - Standard → Complete
   - Invalid transitions (error)
4. **Preview Generation**:
   - Diff format correct
   - Before/after accurate
5. **Edge Cases**:
   - Empty spec file
   - Corrupt YAML frontmatter
   - Missing template file

**Test Structure**:
```python
class TestTierManager:
    def test_get_current_tier_valid(self):
        """Test tier detection with valid frontmatter"""

    def test_get_current_tier_missing(self):
        """Test default tier when missing"""

    def test_expand_tier_minimal_to_standard(self):
        """Test expansion from minimal to standard"""

    def test_content_preservation_with_custom_sections(self):
        """Test custom sections preserved during expansion"""

    def test_preview_expansion_shows_diff(self):
        """Test diff preview generation"""
```

**Acceptance Criteria**:
- [ ] Test file created at `tests/test_tier_manager.py`
- [ ] 90%+ code coverage for tier_manager.py
- [ ] All edge cases tested
- [ ] Fast execution (< 5 seconds total)
- [ ] Tests pass with pytest

**Files to Create**:
- `tests/test_tier_manager.py`

**Testing Commands**:
```bash
pytest tests/test_tier_manager.py -v
pytest tests/test_tier_manager.py --cov=specpulse/core/tier_manager.py --cov-report=term-missing
```

**Assignable**: developer, QA engineer
**SDD Trace**: Success Criteria (90% coverage)

---

## Phase 2: Checkpoint System (2 days, 16 hours)

**Goal**: Automatic versioning and rollback capability

### T011: Create CheckpointManager Class

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: None
- **Parallel**: Can start in parallel with Phase 1

**Description**:
Implement checkpoint lifecycle management class. Handles creating, listing, restoring, and cleaning up checkpoints.

**Class Structure**:
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

**Storage Structure**:
```
.specpulse/checkpoints/
  003-better-workflow-support/
    checkpoint-001.spec.md       (spec snapshot)
    checkpoint-001.meta.yaml     (metadata)
    checkpoint-002.spec.md
    checkpoint-002.meta.yaml
```

**Checkpoint Naming**:
- Format: `checkpoint-{sequential_number}`
- Auto-increment from highest existing number
- Never reuse checkpoint numbers

**Acceptance Criteria**:
- [ ] File created at `specpulse/core/checkpoints.py`
- [ ] Checkpoints created atomically (temp file + rename)
- [ ] Metadata includes timestamp, tier, progress
- [ ] Directory created if missing
- [ ] Proper file permissions (user-only)

**Files to Create**:
- `specpulse/core/checkpoints.py`

**Testing**:
- Unit tests for each method
- Atomic write verification
- Permission checks

**Assignable**: developer
**SDD Trace**: FR-004

---

### T012: Implement Checkpoint Storage

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 3 hours
- **Complexity**: Medium
- **Dependencies**: T011 (needs CheckpointManager class)
- **Parallel**: NO - Sequential

**Description**:
Implement checkpoint file storage with metadata. Use YAML for metadata and copy spec file as-is.

**Metadata Format**:
```yaml
created: 2025-10-06T16:30:00
description: "Before adding security section"
spec_file: spec-001.md
tier: standard
progress: 0.45
sections_completed:
  - what
  - why
  - user_stories
file_hash: abc123def456789  # SHA-256
file_size_bytes: 2048
```

**Storage Algorithm**:
1. Generate checkpoint name (checkpoint-XXX)
2. Calculate SHA-256 hash of spec file
3. Copy spec file to checkpoint location
4. Create metadata YAML file
5. Verify both files written successfully

**Validation**:
- Verify file integrity using hash
- Check file size < 10MB (configurable limit)
- Validate YAML structure
- Atomic write (temp + rename)

**Acceptance Criteria**:
- [ ] Checkpoint files written correctly
- [ ] Metadata complete and valid
- [ ] Hash verification works
- [ ] Atomic write (no partial files)
- [ ] Performance: < 1 second for typical spec

**Files to Modify**:
- `specpulse/core/checkpoints.py` (create method)

**Testing**:
- Write and verify hash
- Large file handling
- Concurrent writes (if applicable)

**Assignable**: developer
**SDD Trace**: FR-004, Performance Requirements

---

### T013: Implement Checkpoint Restoration

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 3 hours
- **Complexity**: Medium
- **Dependencies**: T012 (needs storage working)
- **Parallel**: NO - Sequential

**Description**:
Implement safe checkpoint restoration with backup of current state.

**Restoration Algorithm**:
1. Validate checkpoint exists and is valid
2. Create safety backup of current state (temp dir)
3. Load checkpoint metadata
4. Verify checkpoint hash
5. Copy checkpoint file to spec location
6. Update YAML frontmatter with checkpoint metadata
7. Verify restoration (hash check)
8. Delete safety backup (or keep for 24h)

**Safety Features**:
- Always create backup before restore
- Show diff preview before applying
- Confirm with user (unless --force)
- Keep backup for 24 hours
- Rollback if verification fails

**Diff Preview**:
```
Restoring to: checkpoint-002 (2025-10-06 16:10)
Description: "Before expanding to standard tier"

Changes:
  Tier: standard → minimal
  Progress: 0.43 → 1.0
  Sections: 7 → 3

Continue? [y/N]:
```

**Acceptance Criteria**:
- [ ] Restoration is atomic (complete or rollback)
- [ ] Current state backed up
- [ ] User sees diff before applying
- [ ] Hash verification after restore
- [ ] Performance: < 1 second

**Files to Modify**:
- `specpulse/core/checkpoints.py` (restore method)

**Testing**:
- Happy path restoration
- Corrupt checkpoint handling
- User cancellation
- Verification failure rollback

**Assignable**: developer
**SDD Trace**: FR-004, FR-007

---

### T014: Add CLI Commands for Checkpoints

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: T011, T012, T013 (needs CheckpointManager complete)
- **Parallel**: NO - Sequential

**Description**:
Create user-facing CLI commands for checkpoint management. Provide rich terminal output with tables.

**Commands to Add**:
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

**Output Example (list)**:
```
Checkpoints for 003-better-workflow-support:

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Name          ┃ Description                         ┃ Created            ┃ Tier  ┃ Progress ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ checkpoint-01 │ initial-minimal-spec                │ 2025-10-06 16:00   │ min   │ 100%     │
│ checkpoint-02 │ before-expand-to-standard           │ 2025-10-06 16:10   │ min   │ 100%     │
│ checkpoint-03 │ before-add-requirements             │ 2025-10-06 16:15   │ std   │ 43%      │
└───────────────┴─────────────────────────────────────┴────────────────────┴───────┴──────────┘

Total: 3 checkpoints (2.1 KB)
```

**Acceptance Criteria**:
- [ ] All 4 commands work correctly
- [ ] Output formatted with Rich tables
- [ ] Error messages helpful
- [ ] Confirmation prompts for destructive actions
- [ ] Help text complete

**Files to Modify**:
- `specpulse/cli/main.py` (add checkpoint command group)

**Testing**:
- CLI integration tests
- All commands
- Error handling
- User confirmation

**Assignable**: developer
**SDD Trace**: FR-004

---

### T015: Unit Tests for CheckpointManager

- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 2 hours
- **Complexity**: Medium
- **Dependencies**: T014 (needs CheckpointManager complete)
- **Parallel**: [P] - Can run parallel to T014 completion

**Description**:
Comprehensive unit tests for CheckpointManager. 90%+ coverage.

**Test Cases**:
1. **Creation**: Checkpoint created with valid metadata
2. **Listing**: All checkpoints listed correctly
3. **Restoration**: Restore works, hash verified
4. **Cleanup**: Old checkpoints deleted
5. **Edge Cases**:
   - Empty feature (no checkpoints)
   - Corrupt metadata file
   - Missing spec file
   - Concurrent operations

**Test Structure**:
```python
class TestCheckpointManager:
    def test_create_checkpoint(self):
        """Test checkpoint creation"""

    def test_list_checkpoints_empty(self):
        """Test listing when no checkpoints"""

    def test_restore_checkpoint(self):
        """Test checkpoint restoration"""

    def test_cleanup_old_checkpoints(self):
        """Test deletion of old checkpoints"""
```

**Acceptance Criteria**:
- [ ] Test file created at `tests/test_checkpoints.py`
- [ ] 90%+ code coverage
- [ ] All edge cases tested
- [ ] Performance acceptable (< 1s per operation)
- [ ] Tests pass with pytest

**Files to Create**:
- `tests/test_checkpoints.py`

**Testing Commands**:
```bash
pytest tests/test_checkpoints.py -v
pytest tests/test_checkpoints.py --cov=specpulse/core/checkpoints.py
```

**Assignable**: developer, QA engineer
**SDD Trace**: Success Criteria

---

## Phase 3: Incremental Building (3 days, 24 hours)

**Goal**: Section-by-section spec building with progress tracking

### T016: Create IncrementalBuilder Class

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 5 hours
- **Complexity**: High
- **Dependencies**: T004 (needs SECTION_TIER_MAP)
- **Parallel**: Can start after Phase 0 complete

**Description**:
Implement core class for incremental spec building. Handles section addition, progress calculation, and next-section recommendations.

**Class Structure**:
```python
class IncrementalBuilder:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.section_map = SECTION_TIER_MAP

    def add_section(self, spec_file: Path, section_name: str) -> AddResult:
        """Add individual section to spec"""

    def get_progress(self, spec_file: Path) -> ProgressInfo:
        """Calculate completion percentage and section status"""

    def get_next_section(self, spec_file: Path) -> Optional[str]:
        """Recommend next section to work on"""

    def get_section_template(self, section_name: str) -> str:
        """Load section template with LLM guidance"""
```

**Data Models**:
```python
@dataclass
class ProgressInfo:
    tier: str
    total_sections: int
    completed_sections: int
    partial_sections: int
    not_started_sections: int
    percentage: float
    next_recommended: Optional[str]

@dataclass
class AddResult:
    success: bool
    section_added: str
    position: int
    message: str
```

**Acceptance Criteria**:
- [ ] File created at `specpulse/core/incremental.py`
- [ ] All methods implemented
- [ ] Type hints complete
- [ ] Handles missing sections gracefully
- [ ] Data classes for return values

**Files to Create**:
- `specpulse/core/incremental.py`

**Testing**:
- Unit tests for each method
- Type checking
- Data class validation

**Assignable**: senior developer
**SDD Trace**: FR-003, FR-005

---

### T017: Implement Section Addition

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 5 hours
- **Complexity**: High
- **Dependencies**: T016 (needs IncrementalBuilder class)
- **Parallel**: NO - Sequential

**Description**:
Implement logic to add individual sections to specs incrementally, maintaining section order and adding LLM guidance.

**Algorithm**:
1. Validate section name exists in SECTION_TIER_MAP
2. Check if section's tier <= current spec tier (warn if not)
3. Load section template from appropriate tier file
4. Find insertion point in spec (maintain section order)
5. Insert section with LLM guidance comments
6. Update YAML frontmatter progress
7. Return AddResult

**Section Order Logic**:
```python
def find_insertion_point(spec_content, section_name):
    """Find correct position to insert section"""
    section_order = TIER_SECTIONS[current_tier]
    target_index = section_order.index(section_name)

    # Find last existing section before target
    for i in range(target_index - 1, -1, -1):
        if section_order[i] in spec_content:
            return position_after(section_order[i])

    # Insert at beginning if no prior sections
    return beginning_position()
```

**Edge Cases**:
- Section already exists → Skip or warn user
- Section requires higher tier → Suggest `expand` command
- Custom sections → Allow but don't track in progress
- Empty spec → Insert after frontmatter

**Acceptance Criteria**:
- [ ] Sections inserted in correct order
- [ ] LLM guidance included
- [ ] Progress updated correctly
- [ ] Handles all edge cases
- [ ] Performance: < 500ms

**Files to Modify**:
- `specpulse/core/incremental.py` (add_section method)

**Testing**:
- Add to empty spec
- Add to partially filled spec
- Add out-of-order (should insert correctly)
- Add duplicate (should warn)

**Assignable**: senior developer
**SDD Trace**: FR-003, FR-006

---

### T018: Implement Progress Calculation

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: T016 (needs IncrementalBuilder class)
- **Parallel**: NO - Sequential

**Description**:
Implement accurate progress calculation by analyzing spec sections and determining completion status.

**Algorithm**:
1. Parse YAML frontmatter for tier and sections_completed
2. Get expected sections for current tier from TIER_SECTIONS
3. For each expected section:
   - ✓ Complete: Has user content (not template placeholders)
   - ⚠️ Partial: Has some content but incomplete
   - ⭕ Not started: Only template or empty
4. Calculate: completed / total * 100

**Content Analysis**:
```python
def is_section_complete(section_content: str) -> str:
    """Return: 'complete', 'partial', or 'empty'"""
    # Remove whitespace
    content = section_content.strip()

    # Empty check
    if len(content) == 0:
        return "empty"

    # Template placeholder check
    if is_template_placeholder(content):
        return "empty"

    # Length heuristic (partial if < 50 chars)
    if len(content) < 50:
        return "partial"

    # Has substantial content
    return "complete"
```

**Weighting Strategy** (from ADR-003):
- **Equal weight**: All sections counted equally
- Simple to understand and implement
- Fast calculation (< 500ms requirement)
- Future: Add complexity weighting in v1.9.1 if needed

**Acceptance Criteria**:
- [ ] Percentage accurate (matches manual count)
- [ ] Section status correct (✓ ⚠️ ⭕)
- [ ] Fast calculation (< 500ms)
- [ ] Works for all three tiers
- [ ] Updates YAML frontmatter

**Files to Modify**:
- `specpulse/core/incremental.py` (get_progress method)

**Testing**:
- Empty spec (0%)
- Minimal complete (100%)
- Partial completion (various %)
- Performance benchmark

**Assignable**: developer
**SDD Trace**: FR-005, Performance Requirements

---

### T019: Implement Next Section Recommendation

- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 3 hours
- **Complexity**: Medium
- **Dependencies**: T018 (needs progress calculation)
- **Parallel**: NO - Sequential

**Description**:
Implement intelligent recommendation system to suggest which section user should work on next.

**Algorithm**:
1. Get all sections for current tier
2. Filter: incomplete sections (not 'complete')
3. Sort by: dependency order (e.g., "what" before "user_stories")
4. Return: first incomplete section

**Recommendation Logic**:
```python
def get_next_section(spec_file):
    progress = self.get_progress(spec_file)

    # Tier-specific recommendations
    if progress.tier == "minimal" and progress.percentage == 1.0:
        return "RECOMMEND: Expand to standard tier"

    if progress.tier == "standard" and progress.percentage == 1.0:
        return "RECOMMEND: Expand to complete OR ready for planning"

    # Find next incomplete section
    for section in TIER_SECTIONS[progress.tier]:
        status = get_section_status(section)
        if status != "complete":
            return section

    return None  # All complete
```

**Dependency Order**:
- Tier 1: what → why → done_when
- Tier 2: ... → user_stories → functional_requirements → ...
- Some sections can be filled in any order (parallel)

**Acceptance Criteria**:
- [ ] Recommendations logical
- [ ] Handles all tier states
- [ ] Clear actionable suggestions
- [ ] Returns None when all complete
- [ ] Considers section dependencies

**Files to Modify**:
- `specpulse/core/incremental.py` (get_next_section method)

**Testing**:
- All sections complete (None returned)
- First section incomplete (returned)
- Middle section incomplete (returned)
- Tier transition recommendation

**Assignable**: developer
**SDD Trace**: FR-005

---

### T020: Add CLI Commands for Incremental Building

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Medium
- **Dependencies**: T016, T017, T018, T019 (needs IncrementalBuilder complete)
- **Parallel**: NO - Sequential

**Description**:
Create user-facing CLI commands for section addition and progress tracking. Rich terminal output with visual indicators.

**Commands to Add**:
```bash
# Add section
specpulse spec add-section <feature-id> <section-name>

# Show progress
specpulse spec progress <feature-id>
```

**Output Example (progress)**:
```
📊 Specification Progress: 003-better-workflow-support
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

**Visual Elements**:
- Progress bar (Rich Progress)
- Colored sections (green/yellow/gray)
- Emojis for status (✓ ⚠️ ⭕)
- Time estimates for sections

**Acceptance Criteria**:
- [ ] Both commands work correctly
- [ ] Visual output clear and actionable
- [ ] Colors/emojis used effectively
- [ ] Time estimates shown
- [ ] Error messages helpful

**Files to Modify**:
- `specpulse/cli/main.py` (add spec subcommands)

**Testing**:
- CLI integration tests
- Output rendering
- All progress states
- Error handling

**Assignable**: developer
**SDD Trace**: FR-003, FR-005

---

### T021: Unit Tests for IncrementalBuilder

- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 3 hours
- **Complexity**: Medium
- **Dependencies**: T020 (needs IncrementalBuilder complete)
- **Parallel**: [P] - Can run parallel to T020

**Description**:
Comprehensive unit tests for IncrementalBuilder. 90%+ coverage.

**Test Cases**:
1. **Section Addition**:
   - Add to minimal tier
   - Add to standard tier
   - Add duplicate (warn)
   - Add out-of-tier (suggest expand)
2. **Progress Calculation**:
   - 0% (empty spec)
   - 50% (half complete)
   - 100% (all complete)
   - Partial sections (⚠️)
3. **Next Section**:
   - First section incomplete
   - Middle section incomplete
   - All complete (None)
   - Tier transition recommendation
4. **Edge Cases**:
   - Empty spec file
   - Invalid section name
   - Corrupt YAML frontmatter

**Test Structure**:
```python
class TestIncrementalBuilder:
    def test_add_section_to_minimal(self):
        """Test adding section to minimal tier"""

    def test_progress_calculation_empty(self):
        """Test 0% progress on empty spec"""

    def test_get_next_section_first_incomplete(self):
        """Test next section recommendation"""
```

**Acceptance Criteria**:
- [ ] Test file created at `tests/test_incremental.py`
- [ ] 90%+ code coverage
- [ ] All edge cases tested
- [ ] Performance acceptable
- [ ] Tests pass with pytest

**Files to Create**:
- `tests/test_incremental.py`

**Testing Commands**:
```bash
pytest tests/test_incremental.py -v
pytest tests/test_incremental.py --cov=specpulse/core/incremental.py
```

**Assignable**: developer, QA engineer
**SDD Trace**: Success Criteria

---

## Phase 4: Integration & Testing (2 days, 16 hours)

**Goal**: End-to-end workflow validation and documentation

### T022: Integration Tests for Complete Workflows

- **Type**: testing
- **Priority**: CRITICAL
- **Estimate**: 6 hours
- **Complexity**: High
- **Dependencies**: All previous phases complete
- **Parallel**: NO - Sequential (needs all features)

**Description**:
End-to-end integration tests for complete user workflows. Test all three major workflows from start to finish.

**Workflow 1: Minimal → Standard → Complete Progression**
```python
def test_tier_progression():
    # 1. Initialize with minimal tier
    run_command("specpulse pulse test-feature --tier minimal")
    assert_files_exist("specs/003-test-feature/spec-001.md")

    # 2. Fill minimal spec
    update_spec("003-test-feature", "what", "User authentication")
    update_spec("003-test-feature", "why", "Security requirement")
    update_spec("003-test-feature", "done_when", ["Login", "Logout", "Session"])

    # 3. Verify 100% progress at minimal
    progress = get_progress("003-test-feature")
    assert progress.percentage == 1.0
    assert progress.tier == "minimal"

    # 4. Expand to standard
    run_command("specpulse expand 003 --to-tier standard")

    # 5. Verify content preserved
    spec = read_spec("003-test-feature/spec-001.md")
    assert "User authentication" in spec
    assert "Security requirement" in spec

    # 6. Verify new sections added
    progress = get_progress("003-test-feature")
    assert progress.total_sections == 7
    assert progress.percentage < 1.0  # Now incomplete

    # 7. Expand to complete
    run_command("specpulse expand 003 --to-tier complete")
    assert progress.total_sections == 15
```

**Workflow 2: Section-by-Section Building**
- Start minimal
- Add user_stories section
- Add functional_requirements section
- Verify progress updates correctly
- Check next section recommendations

**Workflow 3: Checkpoint and Rollback**
- Create spec and fill it
- Create manual checkpoint
- Make changes
- Restore to checkpoint
- Verify content matches checkpoint exactly

**Acceptance Criteria**:
- [ ] Test file created at `tests/integration/test_v190_workflow.py`
- [ ] All 3 workflows pass
- [ ] No data loss detected
- [ ] Performance acceptable (< 30s per workflow)
- [ ] Tests can run on CI/CD

**Files to Create**:
- `tests/integration/test_v190_workflow.py`

**Testing Commands**:
```bash
pytest tests/integration/test_v190_workflow.py -v
pytest tests/integration/ --cov --cov-report=html
```

**Assignable**: senior developer, QA lead
**SDD Trace**: Success Criteria, All FRs

---

### T023: Update /sp-pulse to Support --tier Flag

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 3 hours
- **Complexity**: Medium
- **Dependencies**: T001, T002, T003 (needs templates)
- **Parallel**: NO - Sequential

**Description**:
Modify feature initialization to accept tier parameter and copy appropriate template.

**Command Syntax**:
```bash
specpulse pulse new-feature --tier minimal    # Default
specpulse pulse new-feature --tier standard
specpulse pulse new-feature --tier complete

# Also via slash command
/sp-pulse new-feature --tier minimal
```

**Behavior**:
1. Parse --tier flag (default: minimal)
2. Validate tier value (minimal|standard|complete)
3. Copy appropriate tier template to specs/
4. Set YAML frontmatter: `tier: {value}`
5. Display tier-appropriate instructions

**Output**:
```
🎯 Initializing Feature: new-feature
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Tier: Minimal (3 sections, 2-3 min to complete)

✓ Created: specs/004-new-feature/spec-001.md
✓ Created: plans/004-new-feature/ (ready for later)
✓ Created: tasks/004-new-feature/ (ready for later)

📝 Next Steps:
1. Fill out minimal spec (What/Why/Done When)
2. When ready: specpulse expand 004 --to-tier standard

💡 Tip: Start minimal, expand when ready!
```

**Acceptance Criteria**:
- [ ] --tier flag works for all tiers
- [ ] Default is minimal (if not specified)
- [ ] Correct template copied
- [ ] YAML frontmatter set correctly
- [ ] Documentation updated

**Files to Modify**:
- `scripts/sp-pulse-init.sh` (add --tier handling)
- `specpulse/cli/main.py` (add --tier option)

**Testing**:
- CLI test for each tier
- Default tier test
- Invalid tier error handling

**Assignable**: developer
**SDD Trace**: FR-001

---

### T024: Update Validator for Tier-Aware Validation

- **Type**: development
- **Priority**: HIGH
- **Estimate**: 3 hours
- **Complexity**: Medium
- **Dependencies**: T004 (needs SECTION_TIER_MAP)
- **Parallel**: [P] - Can run parallel to T023

**Description**:
Update existing validator to respect current tier when checking spec completeness.

**Validation Logic**:
```python
def validate_spec(spec_file):
    # 1. Parse tier from frontmatter
    tier = parse_tier(spec_file)

    # 2. Get expected sections for tier
    expected = TIER_SECTIONS[tier]

    # 3. Validate only relevant sections
    for section in expected:
        if not section_exists(spec_file, section):
            error(f"Missing required section: {section}")

    # 4. Don't error on missing higher-tier sections
    # (Just suggest expansion if appropriate)
```

**Examples**:
- **Minimal tier**: Only validate What/Why/Done When
- **Standard tier**: Validate 7-8 sections
- **Complete tier**: Validate all 15+ sections

**Messages**:
```
✓ Validation passed for minimal tier

💡 Tip: Want more detail? Expand to standard tier:
   specpulse expand 003 --to-tier standard
```

**Acceptance Criteria**:
- [ ] Validation is tier-aware
- [ ] Messages suggest next steps
- [ ] No false positives/negatives
- [ ] Works with existing validator
- [ ] Backward compatible (specs without tier)

**Files to Modify**:
- `specpulse/core/validator.py` (update validation logic)

**Testing**:
- Validate minimal (pass with 3 sections)
- Validate standard (pass with 7 sections)
- Validate complete (pass with 15 sections)
- Validate missing section (error)

**Assignable**: developer
**SDD Trace**: FR-001, FR-008

---

### T025: Error Handling and Edge Cases

- **Type**: development
- **Priority**: MEDIUM
- **Estimate**: 2 hours
- **Complexity**: Medium
- **Dependencies**: All previous tasks
- **Parallel**: [P] - Can run parallel to T026, T027, T028

**Description**:
Comprehensive error handling for all edge cases and failure scenarios.

**Scenarios to Handle**:
1. **Checkpoint directory read-only**: Warn and suggest fix
2. **Spec file corrupted**: Offer recovery from checkpoint
3. **Invalid tier in frontmatter**: Default to complete
4. **Concurrent access**: File locking or warning
5. **Disk full during checkpoint**: Abort and cleanup
6. **Network share / slow filesystem**: Timeout handling
7. **Missing template file**: Clear error message
8. **Git conflict during operation**: Pause and guide user

**Error Message Format**:
```
❌ ERROR: Checkpoint directory is read-only

📋 Problem:
   Cannot create checkpoint at .specpulse/checkpoints/003-feature/

🔧 Solution:
   1. Check directory permissions: ls -la .specpulse/checkpoints/
   2. Make writable: chmod u+w .specpulse/checkpoints/
   3. Or specify different location: --checkpoint-dir /tmp/checkpoints

💡 Need help? Visit: https://docs.specpulse.dev/errors/checkpoint-readonly
```

**Acceptance Criteria**:
- [ ] All error scenarios handled
- [ ] Messages helpful and clear
- [ ] Recovery steps provided
- [ ] No data loss on errors
- [ ] Logs for debugging

**Files to Modify**:
- All core modules (add error handling)

**Testing**:
- Simulate each error scenario
- Verify error messages
- Test recovery steps

**Assignable**: developer
**SDD Trace**: NFR - Reliability

---

### T026: Documentation Updates

- **Type**: documentation
- **Priority**: HIGH
- **Estimate**: 4 hours
- **Complexity**: Simple
- **Dependencies**: All implementation complete
- **Parallel**: [P] - Can run parallel to T025, T027, T028

**Description**:
Update all documentation to reflect v1.9.0 features.

**Documents to Update**:

1. **README.md**:
   - Add "Tiered Templates" section
   - Workflow examples (minimal → standard → complete)
   - Quick start guide with tier progression

2. **CLAUDE.md**:
   - Update with tier instructions
   - Add `/sp-pulse --tier` flag documentation
   - Update workflow examples
   - Add checkpoint commands

3. **CHANGELOG.md**:
   - Document v1.9.0 features
   - Breaking changes (none expected)
   - Migration guide from v1.8.0

4. **Help Commands**:
   - `specpulse help tiers`
   - `specpulse help expand`
   - `specpulse help checkpoints`
   - Update existing help text

**Example Content**:
```markdown
## Tiered Templates (v1.9.0)

Start minimal (2-3 min), expand when ready:

```bash
# 1. Quick start with minimal tier
$ specpulse pulse payment --tier minimal
$ /sp-spec "What: Integrate Stripe. Why: Enable revenue. Done When: Users can pay"

# 2. Expand when ready for implementation
$ specpulse expand 003 --to-tier standard

# 3. Add sections incrementally
$ specpulse spec add-section 003 requirements
$ specpulse spec progress 003
```

**Benefits**:
- ⚡ Start in 2-3 minutes (vs 15+ minutes)
- 🎯 No overwhelm - add detail when needed
- ✅ Safe - automatic checkpoints before changes
- 📊 Track progress visually
```

**Acceptance Criteria**:
- [ ] All 4 documents updated
- [ ] Examples tested and working
- [ ] Help text accurate
- [ ] Screenshots/GIFs if applicable
- [ ] Links valid

**Files to Modify**:
- `README.md`
- `CLAUDE.md`
- `CHANGELOG.md`
- `specpulse/cli/help/*.md`

**Testing**:
- Run all example commands
- Verify help output
- Check links

**Assignable**: technical writer, developer
**SDD Trace**: Success Criteria

---

### T027: Performance Benchmarking

- **Type**: testing
- **Priority**: MEDIUM
- **Estimate**: 2 hours
- **Complexity**: Medium
- **Dependencies**: All implementation complete
- **Parallel**: [P] - Can run parallel to T025, T026, T028

**Description**:
Verify performance requirements met with automated benchmarks.

**Benchmarks to Run**:

1. **Tier Expansion**: < 2 seconds
   - Minimal → Standard
   - Standard → Complete
   - With large spec files (5MB)

2. **Checkpoint Creation**: < 1 second
   - Small spec (10KB)
   - Medium spec (100KB)
   - Large spec (1MB)

3. **Progress Calculation**: < 500ms
   - All tiers
   - Various completion percentages

**Test Method**:
```python
def test_tier_expansion_performance():
    """Verify tier expansion < 2 seconds"""
    times = []
    for _ in range(10):
        start = time.time()
        expand_tier(spec_file, "standard")
        end = time.time()
        times.append(end - start)

    mean_time = statistics.mean(times)
    p95_time = statistics.quantiles(times, n=20)[18]

    assert mean_time < 2.0, f"Mean time {mean_time:.2f}s > 2s"
    assert p95_time < 2.5, f"P95 time {p95_time:.2f}s > 2.5s"
```

**Acceptance Criteria**:
- [ ] All benchmarks pass (meet requirements)
- [ ] Results documented
- [ ] No regressions from baseline
- [ ] Performance tests in CI/CD
- [ ] Benchmark report generated

**Files to Create**:
- `tests/performance/test_v190_performance.py`

**Testing Commands**:
```bash
pytest tests/performance/test_v190_performance.py -v
pytest tests/performance/ --benchmark-only
```

**Assignable**: developer, performance engineer
**SDD Trace**: Performance Requirements

---

### T028: Cross-Platform Testing

- **Type**: testing
- **Priority**: HIGH
- **Estimate**: 2 hours
- **Complexity**: Medium
- **Dependencies**: All implementation complete
- **Parallel**: [P] - Can run parallel to T025, T026, T027

**Description**:
Validate implementation works on Windows, Linux, and macOS.

**Test Matrix**:
- **Windows 11** + PowerShell + Git Bash
- **Ubuntu 22.04** + Bash
- **macOS 13+** + Bash

**Focus Areas**:
1. **Path Handling**:
   - Windows backslashes vs forward slashes
   - Case sensitivity (macOS vs Linux)
   - Path length limits

2. **Shell Script Execution**:
   - Git Bash on Windows
   - Native Bash on Unix
   - Script permissions

3. **File Operations**:
   - Atomic writes (temp + rename)
   - File permissions (chmod)
   - Line endings (CRLF vs LF)

4. **Performance**:
   - Network shares (Windows)
   - NFS mounts (Linux)
   - Time comparisons (timezone handling)

**Testing Approach**:
```yaml
# .github/workflows/test-cross-platform.yml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/ -v
```

**Acceptance Criteria**:
- [ ] All tests pass on all 3 platforms
- [ ] No platform-specific issues
- [ ] CI/CD pipeline updated
- [ ] Platform-specific docs if needed
- [ ] Performance acceptable on all platforms

**Files to Modify**:
- `.github/workflows/test.yml` (add matrix)
- Any platform-specific fixes

**Testing**:
- Local testing on each platform (if available)
- CI/CD testing (automated)
- Manual smoke testing

**Assignable**: developer, DevOps engineer
**SDD Trace**: Technical Constraints (cross-platform)

---

## Summary Statistics

### By Phase
- **Phase 0**: 5 tasks, 16 hours, 2 days
- **Phase 1**: 5 tasks, 24 hours, 3 days
- **Phase 2**: 5 tasks, 16 hours, 2 days
- **Phase 3**: 6 tasks, 24 hours, 3 days
- **Phase 4**: 7 tasks, 16 hours, 2 days

### By Type
- **Development**: 18 tasks (64%)
- **Testing**: 7 tasks (25%)
- **Documentation**: 1 task (4%)
- **Integration**: 2 tasks (7%)

### By Priority
- **CRITICAL**: 2 tasks
- **HIGH**: 21 tasks
- **MEDIUM**: 5 tasks

### By Complexity
- **Very High**: 1 task
- **High**: 6 tasks
- **Medium**: 16 tasks
- **Simple**: 5 tasks

### Parallelization Potential
- **Parallel Tasks**: 11 tasks (39%)
- **Sequential Tasks**: 17 tasks (61%)
- **Maximum Speedup**: ~30% reduction (12 days → 8-9 days with parallel execution)

## SDD Compliance Checklist

- [x] **Specification First**: All tasks trace to SPEC-003
- [x] **Task Decomposition**: 28 concrete, actionable tasks
- [x] **Quality Assurance**: 7 testing tasks (25% of total)
- [x] **Traceable Implementation**: Each task links to FR/NFR
- [x] **Incremental Planning**: 4 phases with clear milestones
- [x] **Architecture Documentation**: ADRs referenced in plan

## AI Execution Strategy

### Optimal Execution Order

**Week 1** (Days 1-5):
- Days 1-2: Phase 0 (all 5 tasks in parallel if multiple sessions)
- Days 3-5: Phase 1 (T006 → T007 → T008, T009 → T010 parallel)

**Week 2** (Days 6-10):
- Days 6-7: Phase 2 (T011 → T012 → T013 → T014, T015 parallel)
- Days 8-10: Phase 3 (T016 → T017, T018 → T019 → T020, T021 parallel)

**Week 3** (Days 11-12):
- Days 11-12: Phase 4 (T022 → T023, then T024-T028 all parallel)

### Critical Path Tasks (MUST be sequential)
```
T001-T005 → T006 → T007 → T008 → T011 → T012 → T013 → T016 → T017 → T018 → T019 → T022 → T023
```

### Parallel Execution Opportunities
```
Group A: T001, T002, T003 (Phase 0 templates)
Group B: T010, T015, T021 (Unit tests while integration progresses)
Group C: T024, T025, T026, T027, T028 (Phase 4 final tasks)
```

## Next Steps

**To begin implementation:**

```bash
# 1. Start with Phase 0, Task 1
git checkout -b feature/003-better-workflow-support
cd specpulse/resources/templates

# 2. Create first template
touch spec-tier1.md
# Fill out minimal tier template (T001)

# 3. Mark task as in progress
# Update this file: change T001 status to [in_progress]

# 4. When complete, mark done and move to T002
# Update this file: change T001 status to [completed]
```

**Status Updates**:
Update progress in this file by changing task status in YAML frontmatter:
```yaml
status:
  completed: 1  # Increment as tasks finish
  in_progress: 1
  pending: 26
```

---

**Task Breakdown Status**: Ready for Implementation
**Next Task**: T001 - Create Minimal Tier Template
**Estimated Completion**: 2025-10-20 (12 working days)
