# Task Breakdown: Better Context for LLMs (v1.7.0)

## Feature Overview
- **Feature ID**: 001
- **Feature Name**: better-context-for-llms
- **Specification**: SPEC-001 (spec-001.md)
- **Plan**: PLAN-002 (plan-002.md)
- **Created**: 2025-10-06
- **Total Tasks**: 44
- **Estimated Effort**: 80-100 hours (2 weeks for solo developer)

## Task Summary
- **Phase 0 (Foundation)**: 5 tasks, 8 hours
- **Phase 1 (Structured Memory)**: 11 tasks, 28 hours
- **Phase 2 (Context Injection)**: 12 tasks, 24 hours
- **Phase 3 (Quick Notes)**: 7 tasks, 14 hours
- **Phase 4 (Integration & Polish)**: 9 tasks, 20 hours

## Task Status Legend
- [ ] Pending
- [>] In Progress
- [x] Completed
- [!] Blocked

---

## Phase 0: Foundation & Setup

### T001: Create MemoryManager Module
**Complexity**: Simple
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: None
**Parallel**: [P] Can work in parallel with T002, T003

**Description**: Create `specpulse/core/memory_manager.py` with core classes and interfaces

**Acceptance Criteria**:
- [ ] File created: `specpulse/core/memory_manager.py`
- [ ] MemoryManager class defined with type hints
- [ ] MemoryEntry dataclass: id, title, content, tags, date, related_features
- [ ] Methods: query_by_tag(), query_by_feature(), get_recent()
- [ ] Tag parser supports: decision, pattern, current, constraint
- [ ] 100% docstring coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (create)

**Technical Notes**:
- Use dataclasses for MemoryEntry model
- Tag format: `[tag:name]` in markdown headers
- Return type: List[MemoryEntry]

---

### T002: Create ContextInjector Module
**Complexity**: Simple
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: None
**Parallel**: [P] Can work in parallel with T001, T003

**Description**: Create `specpulse/core/context_injector.py` for HTML comment injection

**Acceptance Criteria**:
- [ ] File created: `specpulse/core/context_injector.py`
- [ ] ContextInjector class defined
- [ ] inject() method implemented
- [ ] HTML comment template defined
- [ ] Max 500 character limit enforced
- [ ] 100% docstring coverage

**Files to Create/Modify**:
- `specpulse/core/context_injector.py` (create)

**Technical Notes**:
- Format: `<!-- SPECPULSE CONTEXT -->...<!-- END SPECPULSE CONTEXT -->`
- Use Jinja2 for template rendering
- Include: project name, tech stack, recent decisions (3), patterns

---

### T003: Create NotesManager Module
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: None
**Parallel**: [P] Can work in parallel with T001, T002

**Description**: Create `specpulse/core/notes_manager.py` for note management

**Acceptance Criteria**:
- [ ] File created: `specpulse/core/notes_manager.py`
- [ ] NotesManager class defined
- [ ] Note dataclass: id, content, feature, timestamp
- [ ] Methods: add_note(), list_notes(), merge_to_spec()
- [ ] 100% docstring coverage

**Files to Create/Modify**:
- `specpulse/core/notes_manager.py` (create)

**Technical Notes**:
- Notes stored in: `memory/notes/{feature_id}.md`
- Use timestamp for note IDs
- Support feature auto-detection

---

### T004: Create ProjectContext Model
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: None
**Parallel**: [P] Can work in parallel with T001, T002, T003

**Description**: Create `specpulse/models/project_context.py` for project variables

**Acceptance Criteria**:
- [ ] File created: `specpulse/models/project_context.py`
- [ ] ProjectContext dataclass defined
- [ ] Fields: project (name, type), tech_stack, team_size, preferences
- [ ] YAML serialization/deserialization methods
- [ ] Validation for required fields
- [ ] 100% docstring coverage

**Files to Create/Modify**:
- `specpulse/models/project_context.py` (create)

**Technical Notes**:
- Use pydantic or dataclasses with validation
- Store in: `.specpulse/project_context.yaml`
- Support nested dict access

---

### T005: Set Up Test Fixtures
**Complexity**: Simple
**Estimate**: 1 hour
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T001, T002, T003, T004
**Parallel**: [S] Sequential after foundation modules

**Description**: Create test fixtures for all memory formats

**Acceptance Criteria**:
- [ ] Fixture: sample context.md with tags
- [ ] Fixture: sample project_context.yaml
- [ ] Fixture: sample notes files (3 features)
- [ ] Fixtures in: `tests/fixtures/`
- [ ] README documenting fixture structure

**Files to Create/Modify**:
- `tests/fixtures/context.md` (create)
- `tests/fixtures/project_context.yaml` (create)
- `tests/fixtures/notes/001-feature.md` (create)
- `tests/fixtures/README.md` (create)

**Technical Notes**:
- Cover all tag types: decision, pattern, current, constraint
- Include edge cases: empty files, malformed entries
- Use realistic content

---

## Phase 1: Structured Memory System

### T101: Implement MemoryManager.add_decision()
**Complexity**: Medium
**Estimate**: 2.5 hours
**Priority**: HIGH
**Status**: [ ] Pending
**Dependencies**: T001
**Parallel**: [P] Can work in parallel with T102, T103

**Description**: Add decision entry to memory/context.md with auto-incrementing IDs

**Acceptance Criteria**:
- [ ] Method: add_decision(title, rationale, related_features)
- [ ] Format: `### DEC-{id}: {title}\nRationale: ...\nDate: ...\nRelated: ...`
- [ ] Appends to `## Decisions [tag:decision]` section
- [ ] Auto-increment decision ID (DEC-001, DEC-002)
- [ ] Creates section if missing
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `tests/test_memory_manager.py` (create/modify)

**Technical Notes**:
- Parse existing decisions to find max ID
- Handle concurrent writes with file locking
- Validate title is non-empty

---

### T102: Implement MemoryManager.add_pattern()
**Complexity**: Medium
**Estimate**: 2.5 hours
**Priority**: HIGH
**Status**: [ ] Pending
**Dependencies**: T001
**Parallel**: [P] Can work in parallel with T101, T103

**Description**: Add pattern entry to memory/context.md

**Acceptance Criteria**:
- [ ] Method: add_pattern(title, example, features_used)
- [ ] Format: `### PATTERN-{id}: {title}\n{example}\nUsed in: ...\nDate: ...`
- [ ] Appends to `## Patterns [tag:pattern]` section
- [ ] Auto-increment pattern ID
- [ ] Truncate long examples (>200 chars)
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `tests/test_memory_manager.py` (modify)

**Technical Notes**:
- Support code snippets in example field
- Preserve formatting in markdown
- Features_used is comma-separated list

---

### T103: Implement MemoryManager.add_constraint()
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: MEDIUM
**Status**: [ ] Pending
**Dependencies**: T001
**Parallel**: [P] Can work in parallel with T101, T102

**Description**: Add constraint entry to memory/context.md

**Acceptance Criteria**:
- [ ] Method: add_constraint(title, description, scope)
- [ ] Format: `### CONST-{id}: {title}\n{description}\nApplies to: ...`
- [ ] Appends to `## Constraints [tag:constraint]` section
- [ ] Auto-increment constraint ID
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `tests/test_memory_manager.py` (modify)

**Technical Notes**:
- Scope can be: "All features", specific feature list
- Validate description is non-empty

---

### T104: Implement MemoryManager.query_by_tag()
**Complexity**: Medium
**Estimate**: 3 hours
**Priority**: HIGH
**Status**: [ ] Pending
**Dependencies**: T001, T101, T102, T103
**Parallel**: [S] Sequential after add methods

**Description**: Parse context.md and extract entries by tag with performance <100ms

**Acceptance Criteria**:
- [ ] Method: query_by_tag(tag, feature=None, recent=None)
- [ ] Supported tags: decision, pattern, current, constraint
- [ ] Returns List[MemoryEntry]
- [ ] Performance: <100ms for 1000 entries
- [ ] Optional filters: feature, recent (count)
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `tests/test_memory_manager.py` (modify)

**Technical Notes**:
- Use regex for section detection: `## .* \[tag:(\w+)\]`
- Cache parsed results for repeated queries
- Benchmark with pytest-benchmark

---

### T105: Implement MemoryManager.query_relevant()
**Complexity**: Complex
**Estimate**: 4 hours
**Priority**: HIGH
**Status**: [ ] Pending
**Dependencies**: T104
**Parallel**: [S] Sequential after query_by_tag

**Description**: Get all relevant memory entries for a feature

**Acceptance Criteria**:
- [ ] Method: query_relevant(feature_id)
- [ ] Returns: decisions, patterns, current context, constraints
- [ ] Checks "Related:" field for feature mentions
- [ ] Includes patterns used in related features
- [ ] Includes current active context
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `tests/test_memory_manager.py` (modify)

**Technical Notes**:
- Feature matching: exact ID match or feature name
- Sort by relevance (direct > related)
- Return consolidated MemoryEntry list

---

### T106: CLI Command - memory add-decision
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T101
**Parallel**: [P] Can work in parallel with T107, T108

**Description**: Implement `specpulse memory add-decision` command

**Acceptance Criteria**:
- [ ] Command: `specpulse memory add-decision "title" --rationale "reason" [--feature 001]`
- [ ] Calls MemoryManager.add_decision()
- [ ] Output: Success message with decision ID (DEC-XXX)
- [ ] Error handling for missing arguments
- [ ] Help text with examples
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify - add command)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Click for CLI framework
- Use Rich for formatted output
- --feature is optional

---

### T107: CLI Command - memory add-pattern
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T102
**Parallel**: [P] Can work in parallel with T106, T108

**Description**: Implement `specpulse memory add-pattern` command

**Acceptance Criteria**:
- [ ] Command: `specpulse memory add-pattern "title" --example "code" [--features "001,002"]`
- [ ] Calls MemoryManager.add_pattern()
- [ ] Output: Success message with pattern ID (PATTERN-XXX)
- [ ] Support multi-line examples via editor
- [ ] Help text with examples
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- If --example omitted, open editor for input
- Features is comma-separated list

---

### T108: CLI Command - memory query
**Complexity**: Medium
**Estimate**: 2.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T104
**Parallel**: [P] Can work in parallel with T106, T107

**Description**: Implement `specpulse memory query` command with formatted output

**Acceptance Criteria**:
- [ ] Command: `specpulse memory query --tag decision [--feature 001] [--recent 3]`
- [ ] Calls MemoryManager.query_by_tag()
- [ ] Output: Rich table with columns: ID, Title, Date, Related
- [ ] Support all tags: decision, pattern, current, constraint
- [ ] Optional filters work correctly
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Rich Table for output
- Truncate long content in table view
- Show count of results

---

### T109: CLI Command - memory relevant
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T105
**Parallel**: [S] Sequential after query_relevant

**Description**: Implement `specpulse memory relevant` command for feature context

**Acceptance Criteria**:
- [ ] Command: `specpulse memory relevant 001`
- [ ] Calls MemoryManager.query_relevant()
- [ ] Output: Markdown-formatted context for LLM
- [ ] Groups by: Decisions, Patterns, Constraints, Current
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Output format optimized for LLM parsing
- Include headers for each section
- Feature ID auto-detected if in feature directory

---

### T110: Implement Auto-Migration for Old Context
**Complexity**: Complex
**Estimate**: 5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T104
**Parallel**: [S] Sequential, critical path

**Description**: Auto-migrate unstructured context.md to tagged format

**Acceptance Criteria**:
- [ ] Detect unstructured context.md (missing tag headers)
- [ ] Create backup: `context.md.backup.{timestamp}`
- [ ] Parse and categorize existing content
- [ ] Restructure with tag headers: Decisions, Patterns, Current, Constraints
- [ ] Preserve ALL original content
- [ ] Migration report with summary
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify - add migrate() method)
- `specpulse/cli/main.py` (modify - add migrate command)
- `tests/test_memory_manager.py` (modify)

**Technical Notes**:
- Use heuristics to categorize: keywords like "decided", "pattern", "constraint"
- Ask user to confirm categorization
- Allow manual categorization for ambiguous content

---

### T111: Add Migration Validation
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T110
**Parallel**: [S] Sequential after migration

**Description**: Validate migration preserves all content and allow rollback

**Acceptance Criteria**:
- [ ] Compare pre/post migration line count
- [ ] Ensure no content loss (diff check)
- [ ] Report migration summary: sections created, entries categorized
- [ ] Rollback command: restore from backup
- [ ] Unit tests for validation logic

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `specpulse/cli/main.py` (modify - add rollback command)
- `tests/test_memory_manager.py` (modify)

**Technical Notes**:
- Use difflib for content comparison
- Show diff if content changed unexpectedly
- Keep backups for 30 days

---

## Phase 2: Context Injection System

### T201: Implement ProjectContext.load()
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed (done in T004)
**Dependencies**: T004
**Parallel**: [P] Can work in parallel with T202

**Description**: Load project context from YAML file

**Acceptance Criteria**:
- [ ] Method: ProjectContext.load(path=".specpulse/project_context.yaml")
- [ ] Parse YAML into ProjectContext model
- [ ] Handle missing file gracefully (return defaults)
- [ ] Validate YAML structure
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/models/project_context.py` (modify)
- `tests/test_project_context.py` (create)

**Technical Notes**:
- Default values: project.name="Unknown", team_size=1
- Use PyYAML for parsing
- Catch YAMLError and return meaningful error

---

### T202: Implement ProjectContext.save()
**Complexity**: Simple
**Estimate**: 1 hour
**Priority**: HIGH
**Status**: [x] Completed (done in T004)
**Dependencies**: T004
**Parallel**: [P] Can work in parallel with T201

**Description**: Save project context to YAML file

**Acceptance Criteria**:
- [ ] Method: ProjectContext.save(path=".specpulse/project_context.yaml")
- [ ] Serialize ProjectContext to YAML
- [ ] Create directory if needed
- [ ] Preserve comments in existing file
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/models/project_context.py` (modify)
- `tests/test_project_context.py` (modify)

**Technical Notes**:
- Use ruamel.yaml for comment preservation
- Set file permissions: 644
- Atomic write (write to temp, then rename)

---

### T203: CLI Command - context set
**Complexity**: Medium
**Estimate**: 2.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T201, T202
**Parallel**: [P] Can work in parallel with T204, T205

**Description**: Implement `specpulse context set` for nested keys

**Acceptance Criteria**:
- [ ] Command: `specpulse context set tech_stack.frontend "React"`
- [ ] Support nested keys with dot notation
- [ ] Load, modify, save ProjectContext
- [ ] Output: Confirmation message
- [ ] Handle invalid keys gracefully
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Parse dot notation: "tech_stack.frontend" → nested dict access
- Support setting list values: --append flag
- Validate key exists in model

---

### T204: CLI Command - context get
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T201
**Parallel**: [P] Can work in parallel with T203, T205

**Description**: Implement `specpulse context get` to view variables

**Acceptance Criteria**:
- [ ] Command: `specpulse context get [key]`
- [ ] If key omitted, show all as formatted YAML
- [ ] If key provided, show specific value
- [ ] Support nested keys with dot notation
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Rich Panel for output
- Syntax highlighting for YAML
- Handle missing keys gracefully

---

### T205: CLI Command - context auto-detect
**Complexity**: Complex
**Estimate**: 4 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T201, T202
**Parallel**: [S] Sequential, requires mature load/save

**Description**: Auto-detect tech stack from package files

**Acceptance Criteria**:
- [ ] Command: `specpulse context auto-detect`
- [ ] Scan for: package.json, pyproject.toml, composer.json, Gemfile, go.mod
- [ ] Extract: language, frameworks, dependencies
- [ ] Auto-populate tech_stack fields
- [ ] Prompt user to confirm/edit detected values
- [ ] Integration test for each package manager

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `specpulse/utils/tech_detector.py` (create)
- `tests/test_tech_detector.py` (create)

**Technical Notes**:
- package.json → detect React, Vue, Angular, Express
- pyproject.toml → detect FastAPI, Django, Flask
- Use JSON/YAML/TOML parsers
- Interactive prompts with Rich

---

### T206: Implement ContextInjector.build_context()
**Complexity**: Medium
**Estimate**: 3 hours
**Priority**: HIGH
**Status**: [x] Completed (done in T002)
**Dependencies**: T002, T104, T201
**Parallel**: [S] Sequential after memory and context modules

**Description**: Build HTML comment context block (<500 chars)

**Acceptance Criteria**:
- [ ] Method: build_context(feature_id=None)
- [ ] Load ProjectContext
- [ ] Get recent decisions (last 3) from MemoryManager
- [ ] Get active patterns from MemoryManager
- [ ] Format into HTML comment block
- [ ] Total size < 500 characters
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/context_injector.py` (modify)
- `tests/test_context_injector.py` (create)

**Technical Notes**:
- Template: `<!-- SPECPULSE CONTEXT -->\nProject: {name}\nTech: {stack}\n...\n<!-- END -->`
- Truncate long values to fit 500 char limit
- If feature_id provided, include feature-specific context

---

### T207: CLI Command - context inject
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T206
**Parallel**: [S] Sequential after build_context

**Description**: Implement `specpulse context inject` command

**Acceptance Criteria**:
- [ ] Command: `specpulse context inject [--feature 001]`
- [ ] Calls ContextInjector.build_context()
- [ ] Output: HTML comment block ready for copy-paste
- [ ] Optional --feature for feature-specific context
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Output to stdout (no file modification)
- Use Rich Panel to highlight output
- Feature ID auto-detected if in feature directory

---

### T208: Update sp-pulse-init.sh for Context Injection
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T207
**Parallel**: [P] Can work in parallel with T209, T210, T211, T212

**Description**: Auto-inject context in sp-pulse-init.sh script

**Acceptance Criteria**:
- [ ] Call `specpulse context inject` at script start
- [ ] Prepend context to template before rendering
- [ ] Ensure context appears in generated spec-001.md
- [ ] Test on Windows (Git Bash), Linux, macOS
- [ ] Update script comments/documentation

**Files to Create/Modify**:
- `resources/scripts/sp-pulse-init.sh` (modify)
- `tests/test_scripts.py` (create/modify)

**Technical Notes**:
- Capture output: `CONTEXT=$(specpulse context inject)`
- Prepend to template: `echo "$CONTEXT" > temp.md`
- Ensure cross-platform compatibility

---

### T209: Update sp-pulse-spec.sh for Context Injection
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T207
**Parallel**: [P] Can work in parallel with T208, T210, T211, T212

**Description**: Auto-inject feature-specific context in sp-pulse-spec.sh

**Acceptance Criteria**:
- [ ] Call `specpulse context inject --feature $FEATURE_DIR`
- [ ] Include feature-specific patterns and decisions
- [ ] Prepend context to prompt
- [ ] Test cross-platform
- [ ] Update script documentation

**Files to Create/Modify**:
- `resources/scripts/sp-pulse-spec.sh` (modify)
- `tests/test_scripts.py` (modify)

**Technical Notes**:
- Extract feature ID from FEATURE_DIR (001-feature-name → 001)
- Include in LLM prompt as context

---

### T210: Update sp-pulse-plan.sh for Context Injection
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T207
**Parallel**: [P] Can work in parallel with T208, T209, T211, T212

**Description**: Auto-inject architectural decisions in sp-pulse-plan.sh

**Acceptance Criteria**:
- [ ] Call `specpulse context inject --feature $FEATURE_DIR`
- [ ] Include architectural decisions
- [ ] Prepend context to prompt
- [ ] Test cross-platform
- [ ] Update script documentation

**Files to Create/Modify**:
- `resources/scripts/sp-pulse-plan.sh` (modify)
- `tests/test_scripts.py` (modify)

**Technical Notes**:
- Prioritize architectural patterns in context
- Keep under 500 chars

---

### T211: Update sp-pulse-task.sh for Context Injection
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T207
**Parallel**: [P] Can work in parallel with T208, T209, T210, T212

**Description**: Auto-inject patterns and constraints in sp-pulse-task.sh

**Acceptance Criteria**:
- [ ] Call `specpulse context inject --feature $FEATURE_DIR`
- [ ] Include patterns and constraints
- [ ] Prepend context to prompt
- [ ] Test cross-platform
- [ ] Update script documentation

**Files to Create/Modify**:
- `resources/scripts/sp-pulse-task.sh` (modify)
- `tests/test_scripts.py` (modify)

**Technical Notes**:
- Focus on implementation patterns
- Include relevant constraints

---

### T212: Update sp-pulse-decompose.sh for Context Injection
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T207
**Parallel**: [P] Can work in parallel with T208, T209, T210, T211

**Description**: Auto-inject architectural patterns in sp-pulse-decompose.sh

**Acceptance Criteria**:
- [ ] Call `specpulse context inject --feature $FEATURE_DIR`
- [ ] Include architectural patterns
- [ ] Prepend context to prompt
- [ ] Test cross-platform
- [ ] Update script documentation

**Files to Create/Modify**:
- `resources/scripts/sp-pulse-decompose.sh` (modify)
- `tests/test_scripts.py` (modify)

**Technical Notes**:
- Include microservice patterns if available
- Focus on service boundary patterns

---

## Phase 3: Quick Notes System

### T301: Implement NotesManager.add_note()
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed (done in T003)
**Dependencies**: T003
**Parallel**: [P] Can work in parallel with T302

**Description**: Add note to feature-specific notes file

**Acceptance Criteria**:
- [ ] Method: add_note(content, feature_id=None)
- [ ] Create `memory/notes/{feature_id}.md` if needed
- [ ] Append note with timestamp
- [ ] Return note ID (timestamp-based)
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/notes_manager.py` (modify)
- `tests/test_notes_manager.py` (create)

**Technical Notes**:
- Note format: `### Note {id}\nTimestamp: {datetime}\n{content}`
- Feature ID auto-detected from context.md if omitted
- Create memory/notes/ directory if missing

---

### T302: Implement NotesManager.list_notes()
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed (done in T003)
**Dependencies**: T003
**Parallel**: [P] Can work in parallel with T301

**Description**: List notes for a feature

**Acceptance Criteria**:
- [ ] Method: list_notes(feature_id=None)
- [ ] Read from `memory/notes/{feature_id}.md`
- [ ] Parse notes with IDs and timestamps
- [ ] Return List[Note] ordered by timestamp (newest first)
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/notes_manager.py` (modify)
- `tests/test_notes_manager.py` (modify)

**Technical Notes**:
- Feature ID auto-detected if omitted
- Handle missing notes file gracefully (return empty list)
- Note includes: id, content, timestamp, merged status

---

### T303: Implement NotesManager.merge_to_spec()
**Complexity**: Complex
**Estimate**: 4 hours
**Priority**: HIGH
**Status**: [x] Completed (done in T003)
**Dependencies**: T301, T302
**Parallel**: [S] Sequential, critical integration

**Description**: Merge note content into specification file

**Acceptance Criteria**:
- [ ] Method: merge_to_spec(feature_id, note_id, section=None)
- [ ] Read note content
- [ ] Find latest spec file in `specs/{feature_id}/`
- [ ] Determine appropriate section (or use provided)
- [ ] Insert note content with proper formatting
- [ ] Mark note as merged in notes file
- [ ] Unit tests with 95%+ coverage

**Files to Create/Modify**:
- `specpulse/core/notes_manager.py` (modify)
- `tests/test_notes_manager.py` (modify)

**Technical Notes**:
- Section detection heuristics: keywords like "security", "performance", "constraints"
- Default section: "Additional Notes" at end
- Preserve markdown formatting
- Add comment: `<!-- Merged from note {id} -->`

---

### T304: CLI Command - note
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T301
**Parallel**: [P] Can work in parallel with T305, T306

**Description**: Implement `specpulse note` command

**Acceptance Criteria**:
- [ ] Command: `specpulse note "message" [--feature 001]`
- [ ] Auto-detect current feature from context.md if not provided
- [ ] Call NotesManager.add_note()
- [ ] Output: Confirmation with note ID
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Click for CLI
- Rich output for confirmation
- Support multi-line notes via editor if message omitted

---

### T305: CLI Command - notes list
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T302
**Parallel**: [P] Can work in parallel with T304, T306

**Description**: Implement `specpulse notes list` command

**Acceptance Criteria**:
- [ ] Command: `specpulse notes list [feature_id]`
- [ ] Call NotesManager.list_notes()
- [ ] Output: Rich table with columns: ID, Timestamp, Preview, Merged
- [ ] Preview truncated to 50 chars
- [ ] Show merged status
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Rich Table
- Color-code merged notes (green)
- Show count: "5 notes (2 merged)"

---

### T306: CLI Command - notes merge
**Complexity**: Medium
**Estimate**: 2 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T303
**Parallel**: [S] Sequential after merge_to_spec

**Description**: Implement `specpulse notes merge` command

**Acceptance Criteria**:
- [ ] Command: `specpulse notes merge feature_id --note note_id [--section "Technical Constraints"]`
- [ ] Call NotesManager.merge_to_spec()
- [ ] Output: Success message with spec file updated
- [ ] Show diff preview before merge
- [ ] Ask for confirmation
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Rich to display diff
- Interactive confirmation prompt
- Validate spec file exists

---

### T307: Add Notes Preview in Status Command
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T302
**Parallel**: [P] Can work in parallel with T304, T305, T306

**Description**: Show unmerged notes in `specpulse status` output

**Acceptance Criteria**:
- [ ] Show unmerged notes count for current feature
- [ ] Preview latest 3 notes
- [ ] Prompt to run `specpulse notes list` for full list
- [ ] Only show if notes exist
- [ ] Integration test

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify - update status command)
- `tests/test_cli.py` (modify)

**Technical Notes**:
- Use Rich Panel for notes section
- Show: "📝 3 unmerged notes"
- Include quick links to notes commands

---

## Phase 4: Integration & Polish

### T401: Create End-to-End Integration Test
**Complexity**: Complex
**Estimate**: 4 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T111, T207, T303
**Parallel**: [S] Sequential, requires all features complete

**Description**: Full workflow integration test

**Acceptance Criteria**:
- [ ] Test: Initialize project → Add context → Create feature → Add decision → Generate spec
- [ ] Verify context auto-injected in spec
- [ ] Add note → Merge to spec
- [ ] Validate spec contains note and context
- [ ] Test passes on Windows, Linux, macOS
- [ ] Integration test in CI/CD

**Files to Create/Modify**:
- `tests/integration/test_full_workflow.py` (create)
- `.github/workflows/ci.yml` (modify - add integration tests)

**Technical Notes**:
- Use temporary directory for test project
- Mock user inputs with Click testing utilities
- Clean up test artifacts

---

### T402: Test Migration on Real Projects
**Complexity**: Medium
**Estimate**: 3 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T111
**Parallel**: [P] Can work in parallel with T403

**Description**: Test auto-migration on 3+ existing SpecPulse projects

**Acceptance Criteria**:
- [ ] Test on 3 different real projects (varying complexity)
- [ ] Verify no data loss (content comparison)
- [ ] Check backward compatibility (old tools still work)
- [ ] Document any edge cases found
- [ ] Fix issues discovered during testing

**Files to Create/Modify**:
- `tests/migration/test_real_projects.py` (create)
- `MIGRATION.md` (create - document edge cases)

**Technical Notes**:
- Use projects with different structures: minimal, standard, complex
- Test migration rollback
- Capture before/after snapshots

---

### T403: Performance Benchmarking
**Complexity**: Medium
**Estimate**: 3 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T104, T206, T301
**Parallel**: [P] Can work in parallel with T402, T404

**Description**: Benchmark performance against targets

**Acceptance Criteria**:
- [ ] Benchmark: Memory query time (target <100ms)
- [ ] Benchmark: Context injection time (target <50ms)
- [ ] Benchmark: Note creation time (target <10ms)
- [ ] Test with 1000+ memory entries
- [ ] Optimize if targets not met
- [ ] Document results

**Files to Create/Modify**:
- `tests/benchmarks/test_performance.py` (create)
- `PERFORMANCE.md` (create - document results)

**Technical Notes**:
- Use pytest-benchmark
- Create fixtures with 1000+ entries
- Profile slow operations

---

### T404: Update Help System
**Complexity**: Medium
**Estimate**: 2.5 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T106-T109, T203-T205, T304-T306
**Parallel**: [P] Can work in parallel with T402, T403, T405

**Description**: Add help topics for memory, context, notes

**Acceptance Criteria**:
- [ ] Create: `specpulse help memory-management`
- [ ] Update command descriptions with examples
- [ ] Add help text to all new commands
- [ ] Create: `resources/help/memory.md`
- [ ] Create: `resources/help/context.md`
- [ ] Create: `resources/help/notes.md`

**Files to Create/Modify**:
- `resources/help/memory.md` (create)
- `resources/help/context.md` (create)
- `resources/help/notes.md` (create)
- `specpulse/cli/main.py` (modify - update help texts)

**Technical Notes**:
- Include examples for each command
- Follow existing help format
- Use Rich formatting

---

### T405: Update ROADMAP.md
**Complexity**: Simple
**Estimate**: 1 hour
**Priority**: LOW
**Status**: [x] Completed
**Dependencies**: All previous tasks
**Parallel**: [P] Can work in parallel with T404, T406, T407

**Description**: Mark v1.7.0 as completed in ROADMAP.md

**Acceptance Criteria**:
- [ ] Mark v1.7.0 as ✅ COMPLETED
- [ ] Add implementation notes
- [ ] Link to relevant files (memory_manager.py, context_injector.py, notes_manager.py)
- [ ] Update version history

**Files to Create/Modify**:
- `ROADMAP.md` (modify)

**Technical Notes**:
- Follow existing roadmap format
- Add completion date
- Link to spec-001.md and plan-002.md

---

### T406: Update README.md
**Complexity**: Simple
**Estimate**: 1.5 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: All previous tasks
**Parallel**: [P] Can work in parallel with T404, T405, T407

**Description**: Add v1.7.0 features to README

**Acceptance Criteria**:
- [ ] Add v1.7.0 to feature list
- [ ] Update usage examples with memory/context/notes commands
- [ ] Add sections: "Memory Management", "Context Injection", "Quick Notes"
- [ ] Update installation instructions if needed
- [ ] Add screenshots/examples

**Files to Create/Modify**:
- `README.md` (modify)

**Technical Notes**:
- Include code examples
- Add badges if applicable
- Update table of contents

---

### T407: Add Rich Console Output
**Complexity**: Simple
**Estimate**: 2 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T106-T109, T203-T205, T304-T306
**Parallel**: [P] Can work in parallel with T404, T405, T406

**Description**: Enhance CLI with rich console output

**Acceptance Criteria**:
- [ ] Color-coded memory query results (decisions=blue, patterns=green)
- [ ] Progress bar for migration
- [ ] Animated spinner for context injection
- [ ] Rich tables for notes list
- [ ] Consistent styling across all commands

**Files to Create/Modify**:
- `specpulse/utils/console.py` (modify)
- `specpulse/cli/main.py` (modify - apply rich styling)

**Technical Notes**:
- Use Rich library (already dependency)
- Follow existing console styling
- Add animations sparingly

---

### T408: Error Handling and Validation
**Complexity**: Medium
**Estimate**: 3 hours
**Priority**: HIGH
**Status**: [x] Completed
**Dependencies**: T106-T109, T203-T205, T304-T306
**Parallel**: [P] Can work in parallel with T407, T409

**Description**: Comprehensive error handling and validation

**Acceptance Criteria**:
- [ ] Validate YAML syntax in project_context.yaml
- [ ] Handle missing memory files gracefully
- [ ] Validate feature IDs exist before operations
- [ ] User-friendly error messages (no stack traces)
- [ ] Log errors with context
- [ ] Unit tests for error cases

**Files to Create/Modify**:
- `specpulse/core/memory_manager.py` (modify)
- `specpulse/core/context_injector.py` (modify)
- `specpulse/core/notes_manager.py` (modify)
- `tests/test_error_handling.py` (create)

**Technical Notes**:
- Use custom exceptions: MemoryError, ContextError, NotesError
- Rich traceback for debugging (--debug flag)
- Validate inputs early

---

### T409: Add Doctor Checks for v1.7.0
**Complexity**: Simple
**Estimate**: 2 hours
**Priority**: MEDIUM
**Status**: [x] Completed
**Dependencies**: T104, T201, T302
**Parallel**: [P] Can work in parallel with T407, T408

**Description**: Add `specpulse doctor` checks for memory system

**Acceptance Criteria**:
- [ ] Check: memory file size (warn if >1MB)
- [ ] Check: unmerged notes count
- [ ] Check: project_context.yaml validity
- [ ] Check: context injection in scripts (verify scripts updated)
- [ ] Output: Health report with recommendations

**Files to Create/Modify**:
- `specpulse/cli/main.py` (modify - update doctor command)
- `tests/test_doctor.py` (modify)

**Technical Notes**:
- Use Rich Panel for health report
- Color-code: green (OK), yellow (warning), red (error)
- Provide actionable recommendations

---

## Critical Path (Must Complete in Order)

1. **Foundation**: T001-T005 (8 hours)
2. **Memory Core**: T101-T105 (13.5 hours)
3. **Memory CLI**: T106-T109 (8 hours)
4. **Migration**: T110-T111 (7 hours)
5. **Context Core**: T201-T202, T206 (5.5 hours)
6. **Context CLI**: T203-T205, T207 (9.5 hours)
7. **Script Updates**: T208-T212 (10 hours)
8. **Notes Core**: T301-T303 (7 hours)
9. **Notes CLI**: T304-T306 (5 hours)
10. **Integration**: T401-T403 (10 hours)
11. **Documentation**: T404-T406 (5 hours)
12. **Polish**: T407-T409 (7 hours)

**Total Critical Path**: ~95 hours (2 weeks for solo developer at 40-50 hr/week)

## Parallel Work Opportunities

### Group A (Foundation - Week 1, Day 1)
- T001, T002, T003, T004 can all be done in parallel (6 hours)

### Group B (Memory Add Methods - Week 1, Day 2)
- T101, T102, T103 can be done in parallel (6.5 hours)

### Group C (Memory CLI - Week 1, Day 3)
- T106, T107, T108 can be done in parallel (6.5 hours)

### Group D (Context CLI - Week 1, Day 5)
- T203, T204 can be done in parallel (4 hours)

### Group E (Script Updates - Week 2, Day 1-2)
- T208, T209, T210, T211, T212 can all be done in parallel (10 hours)

### Group F (Notes Core - Week 2, Day 3)
- T301, T302 can be done in parallel (3 hours)

### Group G (Notes CLI - Week 2, Day 3-4)
- T304, T305, T307 can be done in parallel (4.5 hours)

### Group H (Final Polish - Week 2, Day 5)
- T404, T405, T406, T407, T409 can be done in parallel (9 hours)

## Dependencies Graph

```
Foundation (T001-T005)
  ├─> Memory (T101-T111)
  │     ├─> Memory CLI (T106-T109)
  │     └─> Migration (T110-T111)
  ├─> Context (T201-T212)
  │     ├─> Context Core (T201-T202, T206)
  │     ├─> Context CLI (T203-T205, T207)
  │     └─> Script Updates (T208-T212)
  └─> Notes (T301-T307)
        ├─> Notes Core (T301-T303)
        └─> Notes CLI (T304-T307)

Integration (T401-T409)
  ├─> Testing (T401-T403)
  └─> Documentation & Polish (T404-T409)
```

## Progress Tracking

```yaml
status:
  total: 44
  completed: 44
  in_progress: 0
  blocked: 0

metrics:
  actual_velocity: 44 tasks in continuous execution
  completion_date: 2025-10-06
  completion_percentage: 100%

phases:
  phase_0: 5/5 (100%) ✅
  phase_1: 11/11 (100%) ✅
  phase_2: 12/12 (100%) ✅
  phase_3: 7/7 (100%) ✅
  phase_4: 9/9 (100%) ✅
```

## Notes

### Implementation Strategy
1. **Week 1 Focus**: Phases 0-2 (Foundation, Memory, Context)
   - Days 1-2: Foundation + Memory core
   - Days 3-4: Memory CLI + Migration
   - Day 5: Context system

2. **Week 2 Focus**: Phases 3-4 (Notes, Integration, Polish)
   - Days 1-2: Context injection + Script updates
   - Days 3-4: Notes system
   - Day 5: Integration testing + Documentation

### Testing Approach
- **Unit tests**: After each module/method (T001-T409)
- **Integration tests**: After each phase (T401)
- **Performance tests**: After optimization targets (T403)
- **Migration tests**: With real projects (T402)

### Risk Mitigation
- **Backward compatibility**: T111 ensures safe migration
- **Performance**: T403 validates all targets met
- **Cross-platform**: Test on Windows/Linux/macOS throughout
- **Data loss**: T110 creates backups before migration

### Success Metrics
- All 44 tasks completed
- 95%+ test coverage achieved
- Performance targets met (<100ms queries)
- 3+ real projects migrated successfully
- Documentation complete and accurate
