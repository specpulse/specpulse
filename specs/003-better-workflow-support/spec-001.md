---
tier: complete
progress: 1.0
sections_completed:
  - what
  - why
  - done_when
  - user_stories
  - functional_requirements
  - technical_approach
  - dependencies
last_updated: 2025-10-06
---

# Specification: Better Workflow Support (v1.9.0)

## Metadata
- **ID**: SPEC-003
- **Created**: 2025-10-06
- **Author**: Development Team
- **AI Assistant**: Claude Code
- **Version**: 1.0.0

## Executive Summary
Implement workflow support features that enable solo developers and LLMs to build specifications incrementally and safely. This includes tiered templates (minimal/standard/complete), progressive expansion, section-by-section building, automatic checkpoints, and progress tracking. The goal is to eliminate overwhelm by allowing specs to start minimal (2-3 minutes) and grow as needed, with safety nets at every step.

## Problem Statement
Currently, SpecPulse forces users to generate complete specifications upfront, which creates several pain points:

1. **Overwhelm**: LLM generates long specs from the start, overwhelming users with too much information
2. **No Incremental Building**: Can't build spec gradually—must complete everything at once
3. **Risky Changes**: No safety net when modifying specs; changes can't be easily rolled back
4. **Poor Progress Visibility**: Users don't know how complete their spec is or what to work on next
5. **Rigid Workflow**: All-or-nothing approach doesn't match how real development works

These issues slow down spec creation from what should be 3 minutes to 15+ minutes, and discourage iterative refinement.

## Proposed Solution
Implement three core workflow improvements aligned with v1.9.0 roadmap:

1. **Incremental Spec Building (4.1)**: Section-by-section workflow with tiered templates
2. **Spec Checkpoints (4.2)**: Automatic versioning and rollback capability
3. **Progress Tracking**: Visual progress indicators and completion percentages

## Detailed Requirements

### Functional Requirements

FR-001: Tiered Template System
  - Acceptance: Templates exist in 3 tiers (minimal/standard/complete) with clear progression
  - Priority: MUST
  - Details:
    - Minimal tier: 3 sections (What/Why/Done When), 2-3 minutes to complete
    - Standard tier: 7-8 sections (adds User Stories, Requirements, API Design), 10-15 minutes
    - Complete tier: 15+ sections (adds Security, Performance, Monitoring), 30-45 minutes

FR-002: Progressive Tier Expansion
  - Acceptance: Users can expand from minimal → standard → complete without losing content
  - Priority: MUST
  - Details:
    - Command: `specpulse expand <feature-id> --to-tier <standard|complete>`
    - All existing content preserved during expansion
    - New sections added with template placeholders
    - Automatic backup created before expansion

FR-003: Section-by-Section Building
  - Acceptance: Users can add individual sections to specs incrementally
  - Priority: MUST
  - Details:
    - Command: `specpulse spec add-section <feature-id> <section-name>`
    - Supports adding any section from higher tiers
    - Each section includes LLM guidance comments
    - Warns if section requires tier expansion first

FR-004: Automatic Checkpoints
  - Acceptance: System creates checkpoints before major spec changes
  - Priority: MUST
  - Details:
    - Auto-checkpoint before: tier expansion, decomposition, plan generation
    - Manual checkpoint: `specpulse checkpoint <feature-id> "description"`
    - List checkpoints: `specpulse checkpoint list <feature-id>`
    - Restore checkpoint: `specpulse checkpoint restore <feature-id> <checkpoint-name>`

FR-005: Progress Tracking
  - Acceptance: Users can see spec completion percentage and next steps
  - Priority: MUST
  - Details:
    - Command: `specpulse spec progress <feature-id>`
    - Shows: completion %, section status (✓ ⚠️ ⭕), next recommended section
    - Visual indicators: complete (✓), partial (⚠️), not started (⭕)
    - Estimates time remaining based on tier and completion

FR-006: LLM Guidance in Templates
  - Acceptance: All template sections have <!-- LLM GUIDANCE --> comments
  - Priority: SHOULD
  - Details:
    - Guidance explains: what to write, how much detail, format, common mistakes
    - Extract guidance: `specpulse template guidance spec.md`
    - Helps LLM generate appropriate content for each section

FR-007: Content Preservation Guarantees
  - Acceptance: No user content lost during tier expansion or section addition
  - Priority: MUST
  - Details:
    - Validate no data loss before committing changes
    - Show diff before/after for user review
    - Rollback available immediately after operation

FR-008: Workflow State Persistence
  - Acceptance: Current tier and progress saved in spec metadata
  - Priority: SHOULD
  - Details:
    - YAML frontmatter in spec files: `tier: minimal`, `progress: 0.67`
    - Used for progress tracking and validation
    - Updated automatically on changes

### Non-Functional Requirements

#### Performance
- Response Time: Tier expansion < 2 seconds
- Checkpoint creation: < 1 second
- Progress calculation: < 500ms

#### Usability
- Clear error messages for invalid operations
- Visual progress indicators (ASCII art, colors)
- Helpful suggestions for next steps
- Time estimates for each tier/section

#### Reliability
- Checkpoints never fail silently
- All file operations atomic (complete or rollback)
- Backup directory preserved on errors

## User Stories

### Story 1: Quick Start with Minimal Spec
**As a** solo developer using LLM assistance
**I want** to start with a minimal 3-section spec
**So that** I can get started in 2-3 minutes without overwhelm

**Acceptance Criteria:**
- [ ] Can initialize feature with `--minimal` flag
- [ ] Minimal spec has only What/Why/Done When sections
- [ ] LLM can fill out minimal spec in single interaction
- [ ] Progress tracking shows 0% → completion percentage

### Story 2: Expand When Ready for Implementation
**As a** developer ready to implement a feature
**I want** to expand my minimal spec to standard tier
**So that** I have enough detail for planning without losing my initial work

**Acceptance Criteria:**
- [ ] Command `expand 003 --to-tier standard` works
- [ ] All minimal content preserved exactly
- [ ] New sections added with templates
- [ ] Checkpoint created automatically before expansion
- [ ] Clear message shows what was added

### Story 3: Add Specific Sections Incrementally
**As a** developer building a spec
**I want** to add only the sections I need right now
**So that** I can work incrementally without committing to full tier

**Acceptance Criteria:**
- [ ] Can add individual sections: `spec add-section 003 requirements`
- [ ] Section includes LLM guidance comments
- [ ] Checkpoint created before addition
- [ ] Progress updated to reflect new section

### Story 4: Safe Experimentation with Rollback
**As a** developer trying different approaches
**I want** to create checkpoints and rollback if needed
**So that** I can experiment without fear of losing work

**Acceptance Criteria:**
- [ ] Manual checkpoint creation with description
- [ ] List all checkpoints with timestamps
- [ ] Restore to any checkpoint
- [ ] Restored files identical to checkpoint state

### Story 5: Track Progress Toward Completion
**As a** developer working on a spec
**I want** to see visual progress and next steps
**So that** I know how much is left and what to work on next

**Acceptance Criteria:**
- [ ] `spec progress 003` shows percentage complete
- [ ] Visual indicators (✓ ⚠️ ⭕) for each section
- [ ] Recommends next section to work on
- [ ] Shows estimated time remaining

## Technical Constraints

- Must work cross-platform (Windows, Linux, macOS)
- Bash scripts must handle paths with spaces
- Checkpoint storage in `.specpulse/checkpoints/<feature-id>/`
- Maximum checkpoint size: 10MB per file
- Checkpoint retention: 30 days (configurable)
- Template structure must remain backward compatible

## Dependencies

### Internal
- Existing template system (`specpulse/resources/templates/`)
- Validator (`specpulse/core/validator.py`)
- CLI framework (`specpulse/cli/main.py`)
- Console utilities (`specpulse/utils/console.py`)

### External
- Jinja2 (template rendering)
- Rich (visual progress indicators)
- PyYAML (frontmatter parsing)
- GitPython (optional: git integration for checkpoints)

### Feature Dependencies
- None (standalone feature)

## Architecture Design

### New Files to Create

1. **specpulse/core/tier_manager.py** (~150 lines)
   - `TierManager` class
   - Methods: `expand_tier()`, `get_current_tier()`, `validate_tier()`
   - Handles tier transitions and content preservation

2. **specpulse/core/checkpoints.py** (~120 lines)
   - `CheckpointManager` class
   - Methods: `create()`, `list()`, `restore()`, `cleanup()`
   - Manages checkpoint lifecycle

3. **specpulse/core/incremental.py** (~150 lines)
   - `IncrementalBuilder` class
   - Methods: `add_section()`, `get_progress()`, `get_next_section()`
   - Section-by-section building logic

4. **specpulse/resources/templates/spec-tier1.md** (minimal)
   - 3 sections: What, Why, Done When
   - LLM guidance comments

5. **specpulse/resources/templates/spec-tier2.md** (standard)
   - 7 sections: Tier 1 + User Stories, Requirements, API Design, Dependencies
   - LLM guidance comments

6. **specpulse/resources/templates/spec-tier3.md** (complete)
   - 15 sections: Tier 2 + Security, Performance, Monitoring, Rollback, etc.
   - LLM guidance comments

### CLI Commands to Add

```bash
# Initialize with tier
specpulse pulse new-feature --tier minimal

# Expand tier
specpulse expand 003 --to-tier standard
specpulse expand 003 --to-tier complete

# Section management
specpulse spec add-section 003 requirements
specpulse spec progress 003

# Checkpoint management
specpulse checkpoint 003 "Before adding security section"
specpulse checkpoint list 003
specpulse checkpoint restore 003 checkpoint-name
```

### Data Structures

**Spec Metadata (YAML frontmatter):**
```yaml
---
tier: minimal | standard | complete
progress: 0.67
sections_completed:
  - what
  - why
sections_partial:
  - done_when
last_checkpoint: checkpoint-name
last_updated: 2025-10-06T16:30:00
---
```

**Checkpoint Metadata:**
```yaml
# .specpulse/checkpoints/003-feature/checkpoint-name.meta.yaml
created: 2025-10-06T16:30:00
description: "Before adding security section"
spec_file: spec-001.md
tier: standard
progress: 0.45
```

## Implementation Phases

### Phase 0: Template Preparation (2 days)
- Create tier1, tier2, tier3 template files
- Add LLM guidance comments to all sections
- Define section progression map
- Test template rendering

### Phase 1: Tier Manager (3 days)
- Implement `TierManager` class
- Content preservation logic
- Tier expansion with diff preview
- CLI command: `specpulse expand`

### Phase 2: Checkpoint System (2 days)
- Implement `CheckpointManager` class
- Auto-checkpoint hooks (before expansion, etc.)
- CLI commands: `checkpoint`, `checkpoint list`, `checkpoint restore`

### Phase 3: Incremental Building (3 days)
- Implement `IncrementalBuilder` class
- Section addition with validation
- Progress calculation algorithm
- CLI commands: `spec add-section`, `spec progress`

### Phase 4: Integration & Testing (2 days)
- Integration tests for all workflows
- Update `/sp-pulse` to support `--tier` flag
- Update documentation
- Error handling and edge cases

**Total: ~12 days (2 weeks)**

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Checkpoint corruption | High | Low | Validate checkpoints on creation, store metadata separately |
| Content loss during expansion | Critical | Low | Diff preview before commit, automatic backups, comprehensive tests |
| Performance issues with large specs | Medium | Medium | Lazy loading, incremental parsing, checkpoint size limits |
| Backward compatibility breakage | High | Medium | Keep existing templates working, migration script, feature flag |
| User confusion about tiers | Medium | High | Clear docs, examples, in-CLI help, recommended defaults |

## Success Criteria
- [ ] Users can start specs in 2-3 minutes with minimal tier
- [ ] Tier expansion preserves 100% of user content (verified by tests)
- [ ] Checkpoints created automatically before risky operations
- [ ] Progress tracking shows accurate completion percentages
- [ ] All 377+ existing tests still pass
- [ ] 50+ new tests for workflow features
- [ ] Documentation updated with examples and workflows
- [ ] LLM can successfully use new commands without user intervention

## Testing Strategy

### Unit Tests
- `test_tier_manager.py`: Tier transitions, content preservation
- `test_checkpoints.py`: Checkpoint creation, restoration, cleanup
- `test_incremental.py`: Section addition, progress calculation

### Integration Tests
- `test_v190_workflow.py`: End-to-end workflows
  - Minimal → standard → complete progression
  - Section-by-section building
  - Checkpoint creation and restoration
  - Progress tracking accuracy

### Manual Testing
- Cross-platform validation (Windows, Linux, macOS)
- LLM interaction testing with Claude Code
- Edge cases: large specs, special characters, concurrent operations

## Open Questions
- [NEEDS CLARIFICATION: Should tier expansion be reversible? E.g., complete → standard]
- [NEEDS CLARIFICATION: Maximum number of checkpoints to retain per feature?]
- [NEEDS CLARIFICATION: Should progress percentage weight all sections equally or by complexity?]
- [NEEDS CLARIFICATION: Git integration for checkpoints or separate storage?]

## Appendix

### Example Workflow

```bash
# 1. Start minimal
$ specpulse pulse payment-integration --tier minimal
✓ Created minimal spec (3 sections)

# 2. Fill out minimal spec (2-3 minutes with LLM)
$ /sp-spec "What: Integrate Stripe. Why: Enable payments. Done When: Users can pay"

# 3. Check progress
$ specpulse spec progress 003
Progress: 100% (minimal tier complete)
Recommendation: Expand to standard for implementation

# 4. Expand when ready
$ specpulse expand 003 --to-tier standard
✓ Checkpoint created: before-expand-to-standard
✓ Expanded to standard (7 sections)
Progress: 43% (3/7 sections)

# 5. Add sections incrementally
$ specpulse spec add-section 003 requirements
✓ Checkpoint created: before-add-requirements
✓ Added Functional Requirements section

# 6. Continue until ready
$ specpulse spec progress 003
Progress: 85% (6/7 sections)
Next: Add API Design section

# 7. Rollback if needed
$ specpulse checkpoint list 003
checkpoint-001: initial-minimal-spec (2025-10-06 16:00)
checkpoint-002: before-expand-to-standard (2025-10-06 16:10)
checkpoint-003: before-add-requirements (2025-10-06 16:15)

$ specpulse checkpoint restore 003 before-add-requirements
✓ Restored to checkpoint: before-add-requirements
```

### Related Roadmap Items

This specification implements **v1.9.0: Better Workflow Support** from ROADMAP.md:
- Section 4.1: Incremental Spec Building
- Section 4.2: Spec Checkpoints (Versioning)
- Partial support for 4.3: Feature Dependencies (metadata only)

### References
- ROADMAP.md: Lines 407-487 (v1.9.0 section)
- CLAUDE.md: Tiered Templates section (Lines 93-145)
- examples/v1.9.0-sp-pulse-example.md
- examples/v1.9.0-sp-spec-example.md
