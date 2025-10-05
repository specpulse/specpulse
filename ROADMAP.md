# SpecPulse Development Roadmap

> **Reality Check**: SpecPulse is a CLI tool that LLMs use via bash tool calling
> **Current Version**: 1.5.0
> **Philosophy**: Make it easy for LLMs to help solo developers write great specs

---

## 🎯 Understanding the Real Architecture

```
Solo Developer
    ↓
Claude Code / Gemini (LLM does the AI work)
    ↓
Custom Commands (/sp-pulse, /sp-spec, etc.)
    ↓
Bash Scripts (resources/scripts/*.sh)
    ↓
SpecPulse CLI (Python tool via tool calling)
    ↓
Templates, Validation, Memory Management
```

**Key Insight**:
- ✅ LLM handles: conversation, understanding, content generation
- ✅ SpecPulse handles: structure, validation, templates, context storage
- ❌ SpecPulse does NOT need: AI features, LLM API calls, chat interfaces

---

## 📊 Current Pain Points (Revised)

### What Works Well
- ✅ Custom commands (/sp-*) work smoothly in Claude Code/Gemini
- ✅ Bash scripts properly invoke CLI
- ✅ Template system is functional
- ✅ Memory/context storage works

### What Needs Improvement
- ⚠️ **Templates are verbose** → LLM has to generate too much content
- ⚠️ **Context is poorly organized** → LLM can't find relevant info quickly
- ⚠️ **Validation feedback is cryptic** → LLM doesn't know how to fix issues
- ⚠️ **No incremental workflow** → Can't build spec gradually
- ⚠️ **Memory grows messy** → Hard for LLM to recall decisions
- ⚠️ **Scripts lack flexibility** → Rigid workflow, no shortcuts

---

## 🚀 Roadmap (LLM-Friendly Focus)

### **v1.6.0: Better Templates for LLMs** (2 weeks)

#### 1.1 Minimal Templates with Progressive Expansion
**Problem**: LLM generates long specs from the start, overwhelming users

**Solution**: Multi-tier templates
```markdown
# Tier 1: Minimal (Quick Start)
## Feature: {{ feature_name }}
## What: [1 sentence]
## Why: [1 sentence]
## Done When: [3 checkboxes]

# Tier 2: Standard (After LLM interaction)
+ User stories
+ Technical approach
+ API design

# Tier 3: Complete (Before implementation)
+ Full acceptance criteria
+ Edge cases
+ Performance requirements
```

**CLI Commands:**
```bash
# Create minimal spec
specpulse pulse new-feature --tier minimal

# Expand when ready
specpulse expand 001 --to-tier standard
specpulse expand 001 --to-tier complete
```

**For LLM**: Templates have clear `<!-- EXPAND_NEXT -->` markers showing what to add

**Files**:
- `specpulse/resources/templates/spec-tier1.md` (minimal)
- `specpulse/resources/templates/spec-tier2.md` (standard)
- `specpulse/resources/templates/spec-tier3.md` (complete)
- `specpulse/core/tier_manager.py` (150 lines)

---

#### 1.2 LLM-Optimized Template Prompts
**Problem**: Templates don't guide LLM on what to write

**Solution**: Embed prompts in template comments
```markdown
## Functional Requirements

<!--
LLM GUIDANCE:
- List 3-7 concrete requirements
- Use format: FR-001: User can [action] so that [benefit]
- Focus on WHAT, not HOW
- If user mentioned security/performance, add specific requirements
-->

{{ requirements }}
```

**CLI**:
```bash
# Extract LLM guidance from templates
specpulse template guidance spec.md
```

**Files**:
- Update all templates in `resources/templates/` with LLM guidance
- `specpulse/utils/template_parser.py` (+50 lines) - extract guidance

---

#### 1.3 Template Variables from Context
**Problem**: LLM has to ask same questions every time (tech stack, team size, etc.)

**Solution**: Extract common variables from memory
```yaml
# .specpulse/project_context.yaml (auto-generated)
project:
  type: web-app
  tech_stack:
    frontend: React, TypeScript, Tailwind
    backend: Node.js, Express
    database: PostgreSQL
  team_size: 1 (solo)
  preferences:
    - Functional components over class components
    - Prefer composition over inheritance
    - Always include loading states
```

**Templates use these:**
```markdown
## Technology Stack
- Frontend: {{ tech_stack.frontend }}
- Backend: {{ tech_stack.backend }}
- Database: {{ tech_stack.database }}
```

**CLI**:
```bash
specpulse context set tech_stack.frontend "React, TypeScript"
specpulse context get tech_stack
specpulse context auto-detect  # Parse package.json, pyproject.toml
```

**For LLM**: Reduces back-and-forth, spec generation is faster

**Files**:
- `specpulse/core/project_context.py` (200 lines)
- `specpulse/utils/tech_detector.py` (150 lines)

---

### **v1.7.0: Better Context for LLMs** ✅ COMPLETED (2025-10-06)

#### 2.1 Structured Memory with LLM-Readable Format
**Problem**: `context.md` is unstructured, LLM struggles to find info

**Solution**: Structured memory with tags
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
```

**CLI**:
```bash
specpulse memory add-decision "Use Stripe" --rationale "Better API"
specpulse memory add-pattern "API error format" --example "{ success, data, error }"
specpulse memory query --tag decision
specpulse memory relevant 003  # Get relevant context for feature 003
```

**For LLM**: Easy to find relevant info with tags

**Implementation Notes**:
- ✅ Enhanced `specpulse/core/memory_manager.py` (+310 lines)
  - `add_decision()`, `add_pattern()`, `add_constraint()`
  - `query_by_tag()`, `query_relevant()`
  - Auto-migration with `migrate_to_tagged_format()`
- ✅ CLI commands: `memory add-decision`, `add-pattern`, `query`, `relevant`, `migrate`, `rollback`
- ✅ Full backward compatibility with auto-migration
- ✅ Test coverage: Integration tests in `tests/integration/test_v170_workflow.py`

**Related Files**:
- `specpulse/core/memory_manager.py:591-1151` (v1.7.0 methods)
- `specpulse/cli/main.py:1240-1454` (CLI commands)
- `tests/fixtures/context.md` (test data)

---

#### 2.2 Context Injection for Scripts
**Problem**: Each /sp-* command starts fresh, LLM has to reload context

**Solution**: Scripts auto-inject relevant context
```bash
#!/bin/bash
# sp-pulse-plan.sh

# Auto-inject context for LLM
cat << EOF
<!-- SPECPULSE CONTEXT -->
Project: $(specpulse context get project.name)
Tech Stack: $(specpulse context get tech_stack)
Recent Decisions: $(specpulse memory query --tag decision --limit 3)
Patterns to Follow: $(specpulse memory query --tag pattern)
<!-- END CONTEXT -->
EOF

# Then proceed with plan generation
...
```

**For LLM**: Always has relevant context without user asking

**Implementation Notes**:
- ✅ Created `specpulse/core/context_injector.py` (195 lines)
  - `build_context()` with 500 char limit
  - `inject()` for template integration
- ✅ Created `specpulse/models/project_context.py` (273 lines)
  - YAML-based project context storage
  - `load()`, `save()`, `set_value()`, `get_value()`
- ✅ CLI commands: `context set`, `get`, `auto-detect`, `inject`
- ✅ Updated 5 scripts: sp-pulse-{init,spec,plan,task,decompose}.sh
- ✅ Auto-detection for: package.json, pyproject.toml, go.mod, Gemfile

**Related Files**:
- `specpulse/core/context_injector.py` (new)
- `specpulse/models/project_context.py` (new)
- `specpulse/cli/main.py:1456-1673` (context commands)
- `scripts/sp-pulse-*.sh` (context injection added)

---

#### 2.3 Quick Notes During Development
**Problem**: User learns things while coding but spec isn't updated

**Solution**: Lightweight note system
```bash
# User (or LLM) adds notes quickly
specpulse note "Stripe webhooks require HTTPS in production"
specpulse note "Rate limit: 100 req/min per user" --feature 003

# Later, review and merge into spec
specpulse notes list 003
specpulse notes merge 003 --note 2  # Adds to spec
```

**CLI Output**:
```
Notes for 003-payment-integration:
  [1] Stripe webhooks require HTTPS (added 2h ago)
  [2] Rate limit: 100 req/min per user (added 1h ago)
  [3] Testing: use stripe CLI for local webhooks (added 30m ago)

Merge note into spec? [number]: 2
✓ Added to spec under Technical Constraints
```

**For LLM**: Can suggest "Let me add a note for this" during conversation

**Implementation Notes**:
- ✅ Created `specpulse/core/notes_manager.py` (273 lines)
  - `add_note()`, `list_notes()`, `merge_to_spec()`
  - Auto-detection of target spec sections
  - Timestamp-based note IDs
- ✅ CLI commands: `note`, `notes list`, `notes merge`
- ✅ Integration with `specpulse sync` (shows unmerged notes count)
- ✅ Smart section detection: security → Security Considerations, performance → Performance Requirements

**Related Files**:
- `specpulse/core/notes_manager.py` (new)
- `specpulse/cli/main.py:1675-1782` (notes commands)
- `specpulse/cli/main.py:795-814` (status integration)
- `tests/fixtures/notes/*.md` (test data)

**Completion Date**: 2025-10-06
**Total Implementation**: ~70 hours of development
**Test Coverage**: Integration tests + performance benchmarks
**Documentation**: MIGRATION.md + help system (memory.md, context.md, notes.md)

---

### **v1.8.0: Better Validation Feedback** (1 week)

#### 3.1 Actionable Validation Messages
**Problem**: Validation says "Missing section X" but LLM doesn't know what to write

**Solution**: Validation with examples and suggestions
```bash
specpulse validate 001

# Output:
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
```

**For LLM**: Knows exactly what to add and how to format it

**Files**:
- Update `specpulse/core/validator.py` (+150 lines for suggestions)
- Add `specpulse/resources/validation_examples.yaml`

---

#### 3.2 Partial Validation (Progressive)
**Problem**: Can't validate incomplete specs

**Solution**:
```bash
# Validate what exists so far
specpulse validate 001 --partial

# Output:
Progress: 40% complete

✓ Executive Summary (complete)
✓ Problem Statement (complete)
⚠️ Requirements (2 items - consider adding 1-2 more)
⭕ User Stories (not started)
⭕ Acceptance Criteria (not started)

Next suggested section: User Stories
```

**For LLM**: Knows what to work on next

**Files**:
- Update `specpulse/core/validator.py` (+100 lines)

---

#### 3.3 Validation Rules from Project Context
**Problem**: Generic validation doesn't match project needs

**Solution**: Custom validation rules
```yaml
# .specpulse/validation_rules.yaml
rules:
  - name: security_requirement
    enabled: true
    message: "Web apps must include security requirements"
    applies_to: [web-app, api]

  - name: accessibility_check
    enabled: true
    message: "UI features should mention accessibility"
    applies_to: [web-app, mobile-app]
```

**CLI**:
```bash
specpulse validation rules list
specpulse validation rules enable security_requirement
specpulse validation rules add custom-rule --template
```

**For LLM**: Gets project-specific validation feedback

**Files**:
- `specpulse/core/custom_validation.py` (180 lines)

---

### **v1.9.0: Better Workflow Support** (1-2 weeks)

#### 4.1 Incremental Spec Building
**Problem**: LLM generates full spec at once, user gets overwhelmed

**Solution**: Section-by-section workflow
```bash
# Start with minimal
specpulse pulse new-feature --minimal

# Add sections incrementally
specpulse spec add-section 001 requirements
specpulse spec add-section 001 user-stories
specpulse spec add-section 001 acceptance-criteria

# Check progress
specpulse spec progress 001
```

**For LLM**: Can ask "Should we add requirements now or later?"

**Files**:
- `specpulse/core/incremental.py` (150 lines)
- Add section templates to resources

---

#### 4.2 Spec Checkpoints (Versioning)
**Problem**: Spec changes but old version is lost

**Solution**: Auto-versioning
```bash
# Auto-saves checkpoint before major changes
specpulse checkpoint 001 "Before adding payment methods"

# List checkpoints
specpulse checkpoint list 001

# Restore if needed
specpulse checkpoint restore 001 checkpoint-3
```

**Automatic checkpoints on:**
- Before decomposition
- Before plan generation
- When user requests

**For LLM**: Can confidently suggest changes, "Let me save a checkpoint first"

**Files**:
- `specpulse/core/checkpoints.py` (120 lines)

---

#### 4.3 Feature Dependencies
**Problem**: Features depend on each other, no tracking

**Solution**: Dependency graph
```yaml
# In spec frontmatter
depends_on:
  - 001-user-auth    # Must be complete first
  - 002-database     # Must be complete first

blocks:
  - 005-admin-panel  # Can't start until this is done
```

**CLI**:
```bash
specpulse deps show 003
specpulse deps graph --ascii
specpulse deps ready  # Show features ready to start
```

**For LLM**: Can suggest "We should complete 001 first"

**Files**:
- `specpulse/core/dependencies.py` (150 lines)

---

### **v2.0.0: Enhanced LLM Integration** (2 weeks)

#### 5.1 Better Script Outputs for LLM Parsing
**Problem**: Script outputs are for humans, hard for LLM to parse

**Solution**: Structured outputs
```bash
specpulse validate 001 --format json

# JSON output:
{
  "status": "incomplete",
  "completion": 0.6,
  "sections": {
    "executive_summary": { "status": "complete", "quality": "good" },
    "requirements": { "status": "partial", "count": 2, "suggested": 5 },
    "user_stories": { "status": "missing", "action": "add_section" }
  },
  "suggestions": [
    { "type": "add_section", "section": "user_stories", "priority": "high" }
  ]
}
```

**CLI**:
```bash
specpulse <any-command> --format json
specpulse <any-command> --format yaml
specpulse <any-command> --format markdown  # Default
```

**For LLM**: Can easily parse and act on structured data

**Files**:
- Add output formatters to all commands
- `specpulse/utils/formatters.py` (200 lines)

---

#### 5.2 LLM-Friendly Status Command
**Problem**: Hard to know current state

**Solution**: Comprehensive status
```bash
specpulse status --feature 003

# Output (markdown for LLM):
# Feature 003: Payment Integration

## Current State
- Phase: Planning
- Spec: ✓ Complete (100%)
- Plan: ⏳ In Progress (60%)
- Tasks: ⭕ Not Started

## Next Steps
1. Complete architecture section in plan
2. Add deployment considerations
3. Generate task breakdown

## Context
- Decided to use Stripe (see DEC-001)
- Following API error pattern (PATTERN-001)
- Depends on: 001-auth (complete), 002-database (complete)

## Notes
- Stripe webhooks need HTTPS
- Rate limit: 100 req/min
- Testing: use Stripe CLI locally
```

**For LLM**: Perfect summary to resume work

**Files**:
- Enhance existing status command
- `specpulse/cli/status.py` (+100 lines)

---

#### 5.3 Template Introspection
**Problem**: LLM doesn't know what templates expect

**Solution**: Template metadata
```bash
specpulse template info spec.md

# Output:
Template: spec.md
Tier: Standard
Variables Required:
  - feature_name (string)
  - problem_statement (text)
  - target_users (string)

Sections:
  - Executive Summary (required)
  - Problem Statement (required)
  - Requirements (required, min 3 items)
  - User Stories (optional, recommended)
  - Acceptance Criteria (required, min 3 items)

LLM Guidance Available: Yes
Estimated Time to Complete: 10-15 minutes
```

**For LLM**: Knows exactly what to generate

**Files**:
- Add metadata to templates
- `specpulse/core/template_introspection.py` (100 lines)

---

## 🔧 Code Quality & Architecture

### Priority Refactoring

#### 1. Split Large Core Files
```python
# Current: specpulse/core/specpulse.py (1400 lines)

# Split into:
specpulse/core/
  ├── project_init.py        # Project initialization (300 lines)
  ├── resource_manager.py    # Resource copying (200 lines)
  ├── template_loader.py     # Template loading (150 lines)
  ├── command_generator.py   # AI command generation (200 lines)
  └── config_manager.py      # Config handling (150 lines)
```

#### 2. Improve Error Messages
```python
# Before:
raise ValueError("Invalid spec")

# After:
raise SpecValidationError(
    "Specification validation failed",
    details={
        "missing_sections": ["Acceptance Criteria"],
        "suggestion": "Add '## Acceptance Criteria' section with 3-5 testable conditions",
        "example": "✓ User can login with email/password",
        "help_command": "specpulse help acceptance-criteria"
    }
)
```

#### 3. Type Hints Everywhere
```python
from typing import List, Dict, Optional, Union
from pathlib import Path

def create_spec(
    feature_name: str,
    template: Path,
    tier: str = "standard"
) -> Dict[str, Union[bool, str, List[str]]]:
    """Create specification from template.

    Args:
        feature_name: Name of the feature (e.g., "user-auth")
        template: Path to template file
        tier: Template tier (minimal|standard|complete)

    Returns:
        Result dict with status, message, and created files
    """
    ...
```

---

## 📅 Timeline

| Version | Duration | Focus | Key Deliverable |
|---------|----------|-------|-----------------|
| **v1.6.0** | 2 weeks | LLM-friendly templates | Tiered templates, context variables, LLM guidance |
| **v1.7.0** | 1-2 weeks | Better context | Structured memory, auto-injection, quick notes |
| **v1.8.0** | 1 week | Validation | Actionable feedback, partial validation, custom rules |
| **v1.9.0** | 1-2 weeks | Workflow | Incremental building, checkpoints, dependencies |
| **v2.0.0** | 2 weeks | LLM integration | JSON outputs, better status, template introspection |

**Total**: ~7-9 weeks (1.5-2 months)

---

## 🎯 Success Criteria

### For Solo Developers Using LLMs

**Time Savings:**
- LLM generates spec: 10 min → 3 min (better templates)
- Find relevant context: 2 min → 10 sec (structured memory)
- Fix validation issues: 5 min → 1 min (actionable feedback)

**Quality Improvements:**
- Specs are more complete (progressive building)
- Fewer forgotten requirements (context awareness)
- Better consistency (patterns and decisions tracked)

**LLM Experience:**
- LLM gives better suggestions (has context)
- Fewer clarifying questions (context variables)
- Faster iteration (incremental workflow)

---

## 🚫 What We're NOT Building

### Features that LLM Already Does
- ❌ Conversation UI (LLM does this)
- ❌ Natural language understanding (LLM does this)
- ❌ Content generation (LLM does this)
- ❌ AI-powered refining (LLM does this)

### Unnecessary Complexity
- ❌ Team collaboration (solo focus)
- ❌ Cloud sync (local-first)
- ❌ Real-time features (no need)
- ❌ Plugin system (keep simple)
- ❌ Web UI (CLI is enough)

**Why**: SpecPulse is a tool FOR LLMs, not a replacement OF LLMs

---

## 🔄 Quick Wins (v1.5.1 - This Week)

### 1. Add LLM Guidance to Templates
Update all templates with `<!-- LLM GUIDANCE -->` comments

**Files**: All `.md` files in `resources/templates/`
**Time**: 2-3 hours

---

### 2. Project Context Auto-Detection
```bash
specpulse context detect

# Analyzes:
- package.json → Node.js, React, dependencies
- pyproject.toml → Python, FastAPI, packages
- composer.json → PHP, Laravel
- Gemfile → Ruby, Rails
```

**Files**: `specpulse/utils/tech_detector.py` (100 lines)
**Time**: 4-6 hours

---

### 3. Better Status Output
```bash
specpulse status --current

# Shows:
- Active feature
- Current phase
- Next steps
- Recent context
```

**Files**: Update `specpulse/cli/main.py` (+50 lines)
**Time**: 2-3 hours

---

## 📝 Design Principles

### For Every Feature

**Ask:**
1. Does this help LLM understand better?
2. Does this make spec generation faster?
3. Does this reduce user friction?
4. Is the CLI output LLM-parseable?

**If no to any → Reconsider**

### CLI Design

- **Human-readable by default** (markdown output)
- **Machine-parseable on request** (--format json)
- **Context-aware** (inject relevant info)
- **Incremental** (build gradually)
- **Recoverable** (checkpoints, undo)

### Template Design

- **Progressive disclosure** (start minimal, expand when ready)
- **LLM-guided** (comments explaining what to write)
- **Variable-driven** (reuse context)
- **Example-rich** (show, don't just tell)

---

## 🎓 Measuring Success

### Metrics to Track (Locally)

```yaml
# .specpulse/metrics.yaml
spec_creation:
  average_time_seconds: 180
  llm_interactions: 3
  completion_rate: 0.95

validation:
  first_pass_success_rate: 0.75
  average_fixes_needed: 2

context_usage:
  queries_per_feature: 5
  context_reuse_rate: 0.8
```

**CLI**:
```bash
specpulse metrics show
specpulse metrics export
```

---

## 💡 Future Ideas (Post v2.0)

**If users actually ask for it:**
- Export to Notion/Confluence
- GitHub Action for validation
- VS Code snippets
- Diff viewer for specs
- Pattern library (reusable solutions)

**When:**
- After core is stable
- When users request it
- When it doesn't add complexity

---

*This roadmap focuses on making SpecPulse the best tool FOR LLMs to help solo developers with specification-driven development.*

**Last Updated**: 2025-10-06
**Status**: ✅ LLM-Aware & Realistic
