# Specification: Better Context for LLMs (v1.7.0)

## Metadata
- **ID**: SPEC-001
- **Created**: 2025-10-06
- **Author**: SpecPulse Team
- **AI Assistant**: Claude Code
- **Version**: 1.7.0

## Executive Summary
Implement v1.7.0 of SpecPulse to provide better context management for LLMs working with solo developers. This release focuses on structured memory with LLM-readable formats, automatic context injection in scripts, and a lightweight note system for capturing insights during development. The goal is to reduce LLM back-and-forth, make relevant information easily discoverable, and maintain project context across multiple AI interactions.

## Problem Statement

### Current Pain Points
1. **Unstructured Memory**: The current `context.md` file lacks organization, making it hard for LLMs to quickly find relevant information
2. **Context Loss**: Each `/sp-*` command starts fresh without automatic context injection, forcing LLMs to reload information repeatedly
3. **Lost Insights**: Users learn important details during coding, but these insights aren't captured back into specifications
4. **Poor Discoverability**: No tagging or search system means LLMs struggle to find relevant decisions, patterns, or constraints

### Impact on Users
- LLMs ask repetitive questions about tech stack, preferences, and past decisions
- Longer conversation times due to context reloading
- Forgotten constraints and patterns from previous features
- Specs become outdated as real-world learnings aren't captured

## Proposed Solution

Implement three core improvements:

1. **Structured Memory System (§2.1)**: Replace flat context files with tagged, queryable memory structure
2. **Context Injection (§2.2)**: Auto-inject relevant context into all `/sp-*` script executions
3. **Quick Notes (§2.3)**: Lightweight note-taking during development with merge-to-spec capability

## Detailed Requirements

### Functional Requirements

FR-001: Structured Memory with Tags
  - Acceptance: Memory system supports tags (decision, pattern, current, constraint)
  - Priority: MUST
  - Details:
    - Tag format: `[tag:name]` in markdown headers
    - Queryable by tag using CLI
    - Date tracking for all entries
    - Related feature linking

FR-002: Memory CLI Commands
  - Acceptance: All memory operations available via CLI
  - Priority: MUST
  - Commands:
    - `specpulse memory add-decision "title" --rationale "reason"`
    - `specpulse memory add-pattern "title" --example "code"`
    - `specpulse memory query --tag decision`
    - `specpulse memory relevant 001` (get context for feature)

FR-003: Automatic Context Injection
  - Acceptance: All `/sp-*` scripts auto-inject relevant context
  - Priority: MUST
  - Details:
    - Inject project name, tech stack
    - Inject recent decisions (last 3)
    - Inject relevant patterns
    - Format: HTML comments in markdown

FR-004: Context Injection API
  - Acceptance: CLI command available for context injection
  - Priority: MUST
  - Command: `specpulse context inject [--feature 001]`
  - Output: Formatted markdown block for LLM consumption

FR-005: Quick Notes System
  - Acceptance: Notes can be added, listed, and merged into specs
  - Priority: MUST
  - Commands:
    - `specpulse note "message" [--feature 001]`
    - `specpulse notes list [001]`
    - `specpulse notes merge 001 --note 2`

FR-006: Project Context Variables
  - Acceptance: Key project variables stored and accessible
  - Priority: SHOULD
  - Variables: project.name, project.type, tech_stack.*, team_size, preferences
  - Commands:
    - `specpulse context set tech_stack.frontend "React"`
    - `specpulse context get tech_stack`

FR-007: Auto-Detection of Tech Stack
  - Acceptance: Automatically detect tech stack from package files
  - Priority: COULD
  - Detects: package.json, pyproject.toml, composer.json, Gemfile
  - Command: `specpulse context auto-detect`

### Non-Functional Requirements

#### Performance
- Response Time: Memory queries < 100ms
- Throughput: Support 1000+ memory entries
- Resource Usage: Memory file < 1MB in typical usage

#### Security
- Authentication: N/A (local-only tool)
- Authorization: N/A (local-only tool)
- Data Protection: All data stored in plain markdown (user-readable)

#### Scalability
- User Load: Single user (solo developer focus)
- Data Volume: Support 100+ features, 500+ decisions/patterns
- Geographic Distribution: N/A (local-only)

#### Maintainability
- Backward compatibility: Must read existing context.md files
- Migration: Auto-migrate old context to structured format
- Documentation: All CLI commands documented in help system

## User Stories

### Story 1: LLM Finds Past Decisions Quickly
**As a** LLM (via Claude Code)
**I want** to query past architectural decisions by tag
**So that** I can make consistent recommendations without asking the user repeatedly

**Acceptance Criteria:**
- [ ] LLM can query decisions using `specpulse memory query --tag decision`
- [ ] Results include decision title, rationale, date, and related features
- [ ] Results are formatted in LLM-readable markdown
- [ ] Query returns results in < 100ms

### Story 2: Developer Captures Insights During Coding
**As a** solo developer
**I want** to quickly add notes while coding
**So that** I can capture important insights without breaking flow

**Acceptance Criteria:**
- [ ] Can add note with single command: `specpulse note "insight"`
- [ ] Notes are associated with current/specific feature
- [ ] Can review notes later with `specpulse notes list`
- [ ] Can merge notes into spec with `specpulse notes merge`

### Story 3: Scripts Have Automatic Context
**As a** LLM (via Claude Code)
**I want** scripts to automatically inject relevant project context
**So that** I don't have to ask about tech stack, preferences, and past decisions every time

**Acceptance Criteria:**
- [ ] All `/sp-*` scripts inject context at the beginning
- [ ] Context includes: project name, tech stack, recent decisions (3), patterns
- [ ] Context formatted as HTML comments (invisible to user, visible to LLM)
- [ ] Context injection happens automatically without user action

### Story 4: Developer Manages Project Variables
**As a** solo developer
**I want** to set project variables once (tech stack, preferences)
**So that** LLM doesn't ask the same questions for every feature

**Acceptance Criteria:**
- [ ] Can set variables: `specpulse context set tech_stack.frontend "React"`
- [ ] Can get variables: `specpulse context get tech_stack`
- [ ] Variables are used in context injection
- [ ] Variables persist across sessions

### Story 5: Developer Reviews Patterns
**As a** solo developer
**I want** to view established patterns for my project
**So that** I can maintain consistency across features

**Acceptance Criteria:**
- [ ] Can list all patterns: `specpulse memory query --tag pattern`
- [ ] Patterns show: name, example code/format, features where used
- [ ] Can add new patterns: `specpulse memory add-pattern`
- [ ] LLM can access patterns during spec/plan generation

## Technical Constraints

1. **Backward Compatibility**: Must read existing `memory/context.md` files without breaking
2. **Plain Text**: All memory stored in markdown (no databases)
3. **Cross-Platform**: Works on Windows (Git Bash), Linux, macOS
4. **No External Dependencies**: Uses existing Rich, Click, PyYAML libraries
5. **Git-Friendly**: All files are git-trackable plain text

## Dependencies

### Internal
- Rich library (already used for console output)
- Click library (already used for CLI)
- PyYAML (already used for config)
- Jinja2 (for template rendering)

### External
- None (local-only tool)

## Architecture

### File Structure
```
.specpulse/
├── memory/
│   ├── context.md          # Structured memory (upgraded)
│   ├── decisions.md        # Architectural decisions (existing)
│   ├── constitution.md     # SDD principles (existing)
│   └── notes/
│       ├── 001-feature.md  # Notes for feature 001
│       └── 002-feature.md  # Notes for feature 002
├── project_context.yaml    # Project variables (new)
└── config.yaml            # Existing config
```

### Memory Format (context.md)
```markdown
# Memory: Context

## Active [tag:current]
Feature: 003-payment-integration
Status: Planning phase
Blockers: None
Last Updated: 2024-10-06

## Decisions [tag:decision]
### DEC-001: Use Stripe over PayPal
Rationale: Better API, easier integration
Date: 2024-10-05
Related: 003-payment-integration

## Patterns [tag:pattern]
### PATTERN-001: API Error Handling
Always return: { success: bool, data: any, error: string }
Used in: 001-auth, 002-users
Date: 2024-10-04

## Constraints [tag:constraint]
### CONST-001: Rate Limiting
All APIs must implement 100 req/min per user
Applies to: All API features
Date: 2024-10-03
```

### Project Context Format (project_context.yaml)
```yaml
project:
  name: MyApp
  type: web-app
  tech_stack:
    frontend: React, TypeScript, Tailwind
    backend: Node.js, Express
    database: PostgreSQL
  team_size: 1
  preferences:
    - Functional components over class components
    - Prefer composition over inheritance
    - Always include loading states
```

### Context Injection Format
```markdown
<!-- SPECPULSE CONTEXT -->
Project: MyApp (web-app)
Tech Stack: React, TypeScript, Tailwind | Node.js, Express | PostgreSQL
Recent Decisions:
  - DEC-001: Use Stripe over PayPal (2024-10-05)
  - DEC-002: PostgreSQL for primary database (2024-10-04)
Patterns:
  - PATTERN-001: API Error Handling - { success, data, error }
<!-- END SPECPULSE CONTEXT -->
```

## Implementation Phases

### Phase 1: Structured Memory (Week 1)
- Core memory manager with tag support
- Migration from old context.md format
- CLI commands: add-decision, add-pattern, query

### Phase 2: Context Injection (Week 1)
- Project context YAML system
- Context injection command
- Update all sp-pulse-*.sh scripts

### Phase 3: Quick Notes (Week 2)
- Notes system implementation
- Notes CLI commands
- Merge-to-spec functionality

## Risks and Mitigations

### Risk 1: Breaking Existing Projects
**Likelihood**: Medium
**Impact**: High
**Mitigation**:
- Auto-migration script that preserves all existing content
- Backward compatibility for reading old formats
- Backup creation before migration

### Risk 2: Memory File Growth
**Likelihood**: Medium
**Impact**: Low
**Mitigation**:
- Archive old entries (>6 months)
- Cleanup commands for unused patterns
- Memory usage warnings in `specpulse doctor`

### Risk 3: Context Injection Overhead
**Likelihood**: Low
**Impact**: Low
**Mitigation**:
- Cache context to avoid repeated file reads
- Keep injection < 500 characters
- Only inject when running sp-pulse scripts

## Success Criteria

- [ ] All functional requirements (FR-001 through FR-007) implemented
- [ ] All user stories completed
- [ ] Performance targets met (queries < 100ms)
- [ ] Backward compatibility verified with existing projects
- [ ] 95%+ test coverage for new code
- [ ] Documentation updated (help system, ROADMAP.md)
- [ ] Migration tested on 3+ real SpecPulse projects

## Metrics

### Developer Experience
- Time to find relevant decision: 2 min → 10 sec
- Questions LLM asks about context: 5-10 → 0-2
- Context reload time: 30 sec → 0 sec (auto-injected)

### Code Quality
- Test coverage: 95%+
- Type hints: 100% of public APIs
- Docstrings: 100% of public functions

### Performance
- Memory query: < 100ms
- Context injection: < 50ms
- Note creation: < 10ms

## Open Questions

- [RESOLVED] Should we support multiple context files for large projects? → No, keep simple with single file + archiving
- [NEEDS CLARIFICATION] What is the maximum context injection size before it becomes noise? → Suggest 500 chars max
- [NEEDS CLARIFICATION] Should patterns include code snippets or just descriptions? → Support both, truncate long code in queries

## Appendix

### Related Files
- ROADMAP.md:168-272 (v1.7.0 specification)
- specpulse/core/memory_manager.py (to be enhanced)
- resources/scripts/sp-pulse-*.sh (to be updated)

### Example Use Case
```bash
# Developer starts new feature
/sp-pulse payment-integration

# LLM sees auto-injected context
<!-- SPECPULSE CONTEXT -->
Project: MyApp
Tech Stack: React | Node.js | PostgreSQL
Recent Decisions: Use Stripe, Use JWT auth
Patterns: API Error Format, Loading States
<!-- END SPECPULSE CONTEXT -->

# LLM generates spec without asking about tech stack

# During coding, developer learns something
specpulse note "Stripe webhooks require HTTPS in production" --feature 003

# Later, developer reviews notes
specpulse notes list 003
# Output:
# [1] Stripe webhooks require HTTPS (2h ago)
# [2] Rate limit: 100 req/min (1h ago)

# Merge important note to spec
specpulse notes merge 003 --note 1
# → Adds to spec under Technical Constraints
```

### Memory Query Examples
```bash
# Find all decisions
specpulse memory query --tag decision

# Find patterns used in feature 001
specpulse memory query --tag pattern --related 001

# Get all relevant context for feature 003
specpulse memory relevant 003
```
