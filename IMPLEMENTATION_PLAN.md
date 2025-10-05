# SpecPulse v1.6.0 - v2.0.0 Implementation Plan

> **Meta Note**: We're using SpecPulse's own spec-driven methodology to build SpecPulse!
> **Start Date**: 2025-10-06
> **Target**: v1.6.0 release in 2 weeks

---

## 🎯 Implementation Strategy

### Phase-by-Phase Approach
We'll implement ROADMAP.md features in order, using SpecPulse itself:

```
For each feature:
1. Write spec (specs/XXX-feature/spec-001.md)
2. Create plan (plans/XXX-feature/plan-001.md)
3. Break into tasks (tasks/XXX-feature/task-001.md)
4. Execute with AI (/sp-execute all)
5. Validate and iterate
```

### Working in the SpecPulse Repository
```
SpecPulse/
├── specs/                    # Feature specifications
│   ├── 001-tiered-templates/
│   ├── 002-llm-guidance/
│   ├── 003-context-variables/
│   └── ...
├── plans/                    # Implementation plans
├── tasks/                    # Task breakdowns
├── specpulse/               # Source code
└── tests/                   # Test suite
```

---

## 📋 Feature Implementation Order (v1.6.0)

### Priority 1: Foundation Features (Week 1)

#### Feature 001: Tiered Templates
**Why First**: Core feature that enables progressive spec building

**Specs**: `specs/001-tiered-templates/`
**Deliverables**:
- `specpulse/resources/templates/spec-tier1-minimal.md`
- `specpulse/resources/templates/spec-tier2-standard.md`
- `specpulse/resources/templates/spec-tier3-complete.md`
- `specpulse/core/tier_manager.py`
- CLI command: `specpulse expand 001 --to-tier standard`

**Tasks**: ~8 tasks
**Estimate**: 2-3 days

---

#### Feature 002: LLM Guidance in Templates
**Why Second**: Makes templates self-documenting for LLMs

**Specs**: `specs/002-llm-guidance/`
**Deliverables**:
- Update all templates with `<!-- LLM GUIDANCE -->` comments
- `specpulse/utils/template_parser.py` (guidance extraction)
- CLI command: `specpulse template guidance spec.md`

**Tasks**: ~6 tasks
**Estimate**: 1-2 days

---

#### Feature 003: Project Context System
**Why Third**: Enables context reuse across specs

**Specs**: `specs/003-context-system/`
**Deliverables**:
- `.specpulse/project_context.yaml` structure
- `specpulse/core/project_context.py`
- `specpulse/utils/tech_detector.py`
- CLI commands: `specpulse context set/get/detect`

**Tasks**: ~10 tasks
**Estimate**: 3-4 days

---

### Priority 2: Enhanced Features (Week 2)

#### Feature 004: Quick Notes System
**Specs**: `specs/004-quick-notes/`
**Deliverables**:
- `specpulse/core/notes.py`
- CLI commands: `specpulse note`, `specpulse notes list/merge`
- `/sp-note` AI command

**Tasks**: ~7 tasks
**Estimate**: 2 days

---

#### Feature 005: Structured Memory with Tags
**Specs**: `specs/005-structured-memory/`
**Deliverables**:
- Refactor `specpulse/core/memory_manager.py`
- Add tagging system (decision, pattern, active)
- CLI commands: `specpulse memory add-decision/pattern/query`

**Tasks**: ~8 tasks
**Estimate**: 2-3 days

---

#### Feature 006: Context Injection in Scripts
**Specs**: `specs/006-context-injection/`
**Deliverables**:
- Update all bash scripts in `resources/scripts/`
- Add `specpulse context inject` command
- Auto-inject context in /sp-* commands

**Tasks**: ~5 tasks
**Estimate**: 1-2 days

---

## 🎯 Success Criteria for v1.6.0

### Functional Requirements
- ✅ User can create minimal spec with `--tier minimal`
- ✅ User can expand spec with `expand` command
- ✅ Templates contain LLM guidance comments
- ✅ Project context auto-detected from package files
- ✅ Quick notes can be added and merged
- ✅ Memory supports tags and queries
- ✅ AI commands receive auto-injected context

### Quality Requirements
- ✅ All new code has tests (>85% coverage)
- ✅ Type hints on all functions
- ✅ Documentation for all CLI commands
- ✅ No breaking changes to existing features

### Performance Requirements
- ✅ Context injection adds <100ms to commands
- ✅ Template expansion completes in <500ms
- ✅ Memory queries return in <200ms

---

## 📝 Task Template

Each feature follows this structure:

```markdown
# Feature: [Feature Name]

## Tasks

### T001: Initial Setup
**Status**: Pending
**Complexity**: Simple
**Estimate**: 30 min
**Description**: Create directory structure and files

**Acceptance**:
- [ ] Spec file created
- [ ] Plan file created
- [ ] Task file created

---

### T002: Core Implementation
**Status**: Pending
**Complexity**: Medium
**Estimate**: 2 hours
**Description**: Implement core functionality

**Acceptance**:
- [ ] Module created with type hints
- [ ] Core functions implemented
- [ ] Error handling added

---

### T003: CLI Integration
**Status**: Pending
**Complexity**: Simple
**Estimate**: 1 hour
**Description**: Add CLI commands

**Acceptance**:
- [ ] CLI command added to main.py
- [ ] Help text written
- [ ] Command tested manually

---

### T004: Tests
**Status**: Pending
**Complexity**: Medium
**Estimate**: 1.5 hours
**Description**: Write comprehensive tests

**Acceptance**:
- [ ] Unit tests cover >85% of code
- [ ] Integration test for full workflow
- [ ] All tests pass

---

### T005: Documentation
**Status**: Pending
**Complexity**: Simple
**Estimate**: 30 min
**Description**: Update documentation

**Acceptance**:
- [ ] README.md updated
- [ ] CLAUDE.md updated
- [ ] Help system updated

---

### T006: Validation
**Status**: Pending
**Complexity**: Simple
**Estimate**: 30 min
**Description**: Final validation and cleanup

**Acceptance**:
- [ ] Feature works end-to-end
- [ ] No regressions in tests
- [ ] Code formatted and linted
```

---

## 🔄 Development Workflow

### For Each Feature

1. **Initialize Feature**
   ```bash
   cd SpecPulse
   specpulse init --here  # If not already initialized
   specpulse pulse 001-tiered-templates
   ```

2. **Write Specification**
   ```bash
   # In Claude Code / Gemini
   /sp-spec
   # LLM writes the spec based on ROADMAP.md
   ```

3. **Create Plan**
   ```bash
   /sp-plan
   # LLM creates implementation plan
   ```

4. **Break Down Tasks**
   ```bash
   /sp-task
   # LLM creates task list
   ```

5. **Execute Tasks**
   ```bash
   /sp-execute all
   # LLM executes all tasks non-stop
   ```

6. **Validate**
   ```bash
   specpulse validate 001
   pytest tests/
   ```

7. **Commit**
   ```bash
   git add .
   git commit -m "feat: implement tiered templates (001)"
   ```

---

## 🧪 Testing Strategy

### Test Types

**Unit Tests** (most features)
- Test individual functions
- Mock external dependencies
- Fast execution (<1s per test)

**Integration Tests** (key workflows)
- Test complete workflows
- Use temporary directories
- Validate end-to-end behavior

**Regression Tests** (existing features)
- Ensure no breaking changes
- Run full test suite before commit

### Coverage Goals
- New code: >85% coverage
- Overall project: maintain current 86%+

---

## 📦 Release Process

### v1.6.0 Release Checklist

- [ ] All 6 features implemented
- [ ] All tests passing (>85% coverage)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `_version.py`
- [ ] Build package: `python -m build`
- [ ] Test package: `pip install dist/specpulse-1.6.0-py3-none-any.whl`
- [ ] Create git tag: `git tag v1.6.0`
- [ ] Push to GitHub: `git push origin v1.6.0`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Announce release

---

## 🎯 Quick Start: First Feature

Let's start with **Feature 001: Tiered Templates**

### Step 1: Create Spec
```bash
# Create feature directory
mkdir -p specs/001-tiered-templates
mkdir -p plans/001-tiered-templates
mkdir -p tasks/001-tiered-templates

# In Claude Code
/sp-pulse 001-tiered-templates
```

### Step 2: Write Specification
Use ROADMAP.md section 1.1 as basis:
- Multi-tier templates (minimal, standard, complete)
- CLI commands for creation and expansion
- Progressive disclosure

### Step 3: Create Implementation Plan
Technical approach:
- Create three template files
- Build tier_manager.py module
- Add expand command to CLI

### Step 4: Break Down Tasks
See detailed task list below ↓

---

## 📋 Feature 001: Tiered Templates - Detailed Tasks

```markdown
# Feature 001: Tiered Templates

## Overview
Implement multi-tier template system for progressive spec building

## Tasks

### T001: Project Setup
**Status**: Pending
**Complexity**: Simple
**Estimate**: 15 min

**Description**: Create directory structure for tiered templates feature

**Steps**:
1. Create `specs/001-tiered-templates/` directory
2. Create `plans/001-tiered-templates/` directory
3. Create `tasks/001-tiered-templates/` directory
4. Create spec-001.md, plan-001.md, task-001.md files

**Acceptance**:
- [ ] Directory structure exists
- [ ] Initial files created
- [ ] Git tracked

---

### T002: Design Tier 1 (Minimal) Template
**Status**: Pending
**Complexity**: Simple
**Estimate**: 45 min

**Description**: Create minimal spec template for quick starts

**Steps**:
1. Create `specpulse/resources/templates/spec-tier1-minimal.md`
2. Add minimal sections: What, Why, Done When
3. Add `<!-- EXPAND_NEXT: tier2 -->` marker
4. Add LLM guidance comments

**Acceptance**:
- [ ] Template file created
- [ ] Contains 3 core sections
- [ ] Has expansion markers
- [ ] Has LLM guidance

**Template Preview**:
```markdown
# Feature: {{ feature_name }}

<!-- LLM GUIDANCE:
Keep this tier minimal - just the essence of what's being built.
User can expand later with /sp-expand command.
-->

## What
{{ what_description }}

## Why
{{ why_description }}

## Done When
- [ ] {{ acceptance_1 }}
- [ ] {{ acceptance_2 }}
- [ ] {{ acceptance_3 }}

---
<!-- EXPAND_NEXT: tier2 -->
💡 Ready for more detail? Run: specpulse expand {{ feature_id }} --to-tier standard
```

---

### T003: Design Tier 2 (Standard) Template
**Status**: Pending
**Complexity**: Medium
**Estimate**: 1 hour

**Description**: Create standard spec template with user stories and requirements

**Steps**:
1. Create `specpulse/resources/templates/spec-tier2-standard.md`
2. Copy tier1 content + add new sections
3. Add User Stories, Functional Requirements, Technical Approach
4. Add expansion marker to tier3

**Acceptance**:
- [ ] Template includes all tier1 sections
- [ ] Adds 3-4 new sections
- [ ] Has LLM guidance for each section
- [ ] Has tier3 expansion marker

---

### T004: Design Tier 3 (Complete) Template
**Status**: Pending
**Complexity**: Medium
**Estimate**: 1 hour

**Description**: Create complete spec template with all details

**Steps**:
1. Create `specpulse/resources/templates/spec-tier3-complete.md`
2. Copy tier2 content + add comprehensive sections
3. Add Edge Cases, Performance, Security, Testing Strategy
4. Add completion marker

**Acceptance**:
- [ ] Template includes all tier2 sections
- [ ] Adds comprehensive sections
- [ ] Has detailed LLM guidance
- [ ] Marked as complete (no further expansion)

---

### T005: Implement Tier Manager Module
**Status**: Pending
**Complexity**: Medium
**Estimate**: 2 hours

**Description**: Create core module for managing template tiers

**Steps**:
1. Create `specpulse/core/tier_manager.py`
2. Implement `TierManager` class
3. Add methods: `get_tier()`, `expand_tier()`, `validate_tier()`
4. Add type hints and docstrings

**Acceptance**:
- [ ] Module created with proper structure
- [ ] All methods implemented
- [ ] Type hints on all functions
- [ ] Docstrings written

**Code Structure**:
```python
# specpulse/core/tier_manager.py
from pathlib import Path
from typing import Literal, Dict, Optional

TierLevel = Literal["minimal", "standard", "complete"]

class TierManager:
    """Manages multi-tier template system"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.templates_dir = project_root / "templates"

    def get_current_tier(self, feature_id: str) -> TierLevel:
        """Detect current tier of a spec"""
        ...

    def expand_tier(
        self,
        feature_id: str,
        to_tier: TierLevel,
        preserve_content: bool = True
    ) -> bool:
        """Expand spec to higher tier"""
        ...

    def validate_tier(self, spec_path: Path) -> Dict:
        """Validate spec against tier requirements"""
        ...
```

---

### T006: Add Expand CLI Command
**Status**: Pending
**Complexity**: Simple
**Estimate**: 1 hour

**Description**: Add `expand` command to CLI

**Steps**:
1. Update `specpulse/cli/main.py`
2. Add `expand` subcommand with arguments
3. Integrate with TierManager
4. Add help text and examples

**Acceptance**:
- [ ] Command added to CLI
- [ ] Arguments: feature_id, --to-tier
- [ ] Help text written
- [ ] Works from command line

**CLI Usage**:
```bash
specpulse expand 001 --to-tier standard
specpulse expand 001 --to-tier complete
specpulse expand 001 --show-diff  # Preview changes
```

---

### T007: Update Init Command for Tiers
**Status**: Pending
**Complexity**: Simple
**Estimate**: 45 min

**Description**: Add --tier option to init/pulse commands

**Steps**:
1. Update `init` command
2. Update `pulse` command (if separate)
3. Add --tier option (minimal|standard|complete)
4. Default to "minimal"

**Acceptance**:
- [ ] --tier option works
- [ ] Defaults to minimal
- [ ] Creates correct template tier

**CLI Usage**:
```bash
specpulse pulse new-feature --tier minimal
specpulse pulse new-feature --tier standard
specpulse pulse new-feature  # defaults to minimal
```

---

### T008: Write Unit Tests
**Status**: Pending
**Complexity**: Medium
**Estimate**: 1.5 hours

**Description**: Test tier manager functionality

**Steps**:
1. Create `tests/test_tier_manager.py`
2. Test get_current_tier()
3. Test expand_tier()
4. Test validate_tier()
5. Test error cases

**Acceptance**:
- [ ] Test file created
- [ ] >85% coverage of tier_manager.py
- [ ] All tests pass
- [ ] Edge cases covered

**Test Cases**:
```python
def test_get_current_tier_minimal()
def test_get_current_tier_standard()
def test_expand_tier_minimal_to_standard()
def test_expand_tier_preserves_content()
def test_expand_tier_invalid_transition()
def test_validate_tier_missing_sections()
```

---

### T009: Write Integration Test
**Status**: Pending
**Complexity**: Medium
**Estimate**: 1 hour

**Description**: Test full workflow from minimal to complete

**Steps**:
1. Update `tests/test_integration_workflow.py`
2. Test: create minimal → expand to standard → expand to complete
3. Verify content preserved
4. Verify all sections present

**Acceptance**:
- [ ] Integration test added
- [ ] Full workflow tested
- [ ] Test passes

---

### T010: Update Documentation
**Status**: Pending
**Complexity**: Simple
**Estimate**: 30 min

**Description**: Document tiered templates feature

**Steps**:
1. Update README.md with examples
2. Update CLAUDE.md with guidance
3. Add to help system
4. Update CLI_REFERENCE.md

**Acceptance**:
- [ ] README.md updated
- [ ] CLAUDE.md updated
- [ ] Help system includes tiered templates
- [ ] Examples clear and helpful

---

### T011: Manual Testing & Validation
**Status**: Pending
**Complexity**: Simple
**Estimate**: 30 min

**Description**: Manually test the feature end-to-end

**Steps**:
1. Create minimal spec
2. Expand to standard
3. Expand to complete
4. Verify all content preserved
5. Test error cases

**Acceptance**:
- [ ] Feature works as expected
- [ ] No bugs found
- [ ] User experience is smooth

---

### T012: Code Review & Cleanup
**Status**: Pending
**Complexity**: Simple
**Estimate**: 30 min

**Description**: Final code review and cleanup

**Steps**:
1. Run `black specpulse/ tests/`
2. Run `flake8 specpulse/ tests/`
3. Run `mypy specpulse/`
4. Fix any issues

**Acceptance**:
- [ ] Code formatted
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Ready for commit
```

---

## 🚀 Next Steps

1. **Start with Feature 001**
   - Use the task list above
   - Execute with `/sp-execute all` in Claude Code

2. **After Feature 001 Complete**
   - Create specs for Features 002-006
   - Follow same process
   - Build momentum

3. **Weekly Review**
   - Every Friday: review progress
   - Adjust timeline if needed
   - Update ROADMAP.md

---

## 📊 Progress Tracking

Track progress in `.specpulse/progress.yaml`:

```yaml
version: 1.6.0
status: in_progress
started: 2025-10-06

features:
  001-tiered-templates:
    status: pending
    tasks_total: 12
    tasks_completed: 0
    started: null
    completed: null

  002-llm-guidance:
    status: not_started
    tasks_total: 0

  003-context-system:
    status: not_started
    tasks_total: 0

milestones:
  - name: Week 1 Complete
    date: 2025-10-13
    features: [001, 002, 003]

  - name: v1.6.0 Release
    date: 2025-10-20
    features: [001, 002, 003, 004, 005, 006]
```

---

*Let's build SpecPulse using SpecPulse! Meta development at its finest.* 🚀

**Last Updated**: 2025-10-06
**Ready to Start**: ✅ Yes - Begin with Feature 001
