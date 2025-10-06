# SpecPulse

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/specpulse.svg)](https://pypi.org/project/specpulse/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/specpulse)](https://pypi.org/project/specpulse/)

**Transform Your Development Process with Specification-Driven Development**

*Build better software faster by putting specifications first and letting AI handle the implementation details.*

[Installation](#-installation) • [Quick Start](#-quick-start) • [Usage Guide](#-usage-guide) • [Features](#-features) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 What is SpecPulse?

SpecPulse is a universal **Specification-Driven Development (SDD)** framework that works with ANY software project - web apps, mobile apps, desktop software, games, APIs, ML projects, and more. It ensures every feature starts with clear specifications, validated plans, and tracked tasks.

## 📋 What's New in v1.8.0 - Better Validation Feedback

> **✨ Actionable Validation for LLMs**
> - **💬 Enhanced Error Messages**: Errors include meaning, examples, suggestions, and help commands
> - **🔧 Auto-Fix**: `--fix` flag automatically adds missing sections with backups
> - **📊 Partial Validation**: `--partial` for work-in-progress specs (shows completion %)
> - **🎨 Rich Formatting**: Beautiful color-coded error panels with icons (✓ ⚠️ ⭕)
> - **🎯 Custom Rules**: Project-type-specific validation (web-app, api, mobile-app)
> - **🤖 LLM-Optimized**: Examples show exactly what to add, suggestions are actionable
> - **⚡ Smart Suggestions**: Next section recommendations based on completion state
>
> See [Validation Feedback](#-validation-feedback-v180) section below for details.

## 📋 What's New in v1.7.0 - Better Context for LLMs

> **🧠 Intelligent Context Management**
> - **🏷️ Structured Memory**: Tag-based organization (decisions, patterns, constraints, current state)
> - **🔄 Auto Context Injection**: AI scripts automatically receive project context
> - **📝 Quick Notes**: Capture insights during development, merge to specs later
> - **🎯 Zero Friction**: LLMs stop asking repetitive questions about tech stack
> - **🔍 Queryable Memory**: Find past decisions and patterns instantly
> - **⚡ Performance**: Sub-100ms queries, <500 char context injection
>
> See [Memory Management](#-memory-management-v170) section below for details.

## 📋 What's New in v1.6.0 - Tiered Templates

> **🎯 Progressive Specification Building**
> - **📑 Three Template Tiers**: Minimal (3 sections), Standard (7-8 sections), Complete (15+ sections)
> - **✅ Content Preservation**: Your work is never lost during tier expansion
> - **🎯 LLM Guidance**: AI-optimized comments in every template
> - **🔄 Flexible Workflow**: Start minimal, expand when ready
> - **📊 Automatic Backups**: Timestamped backups before each expansion
> - **👁️ Preview Changes**: `--show-diff` to see what will be added
>
> See [Tiered Templates](#-tiered-templates-v160) section below for details.

## 🔖 Recent Release History

<details>
<summary>View Previous Releases (v1.4.0 - v1.5.0)</summary>

### v1.5.0 - Quality & Documentation Enhancement
- 🎯 Comprehensive help system with 6 detailed topics
- 📚 Complete documentation suite
- 🧪 377+ tests with cross-platform CI/CD
- 🔧 Template validation, memory management, advanced error handling
- 🚀 Enhanced Windows, macOS, and Linux compatibility

### v1.4.5 - Version Management
- 🎯 Single source of truth in `_version.py`
- 📦 Module support: `python -m specpulse`

### v1.4.4 - Critical Workflow Fixes
- 🐛 Fixed script numbering issues
- 🎯 Proper task detection in execute scripts
- 🔧 PowerShell parity with Bash scripts

### v1.4.3 - Script Numbering Fix
- 🔢 Correct file numbering (001, 002, 003...)
- 📝 No empty first files

### v1.4.2 - Template System Enhancement
- 📁 Physical template files for AI tools
- 🔧 Complete PowerShell support

### v1.4.1 - Bug Fix
- 🐛 Fixed version display

### v1.4.0 - Framework Revolution
- 🚀 Universal SDD framework
- ✨ 9 universal principles
- 🔄 Major API updates
- 🏗️ Hybrid template system

</details>

### Why SpecPulse?

- **🎯 Universal**: Works with ANY project type - web, mobile, desktop, games, APIs, ML
- **🔍 Clarity First**: No more ambiguous requirements or scope creep
- **🤖 AI-Optimized**: Designed specifically for Claude and Gemini workflows
- **✅ Quality Gates**: Built-in checks ensure quality for your specific project type
- **📊 Full Traceability**: Every decision, change, and requirement is tracked
- **🚀 Faster Delivery**: Structured approach reduces rework and debugging time

## 📦 Installation

```bash
pip install specpulse --upgrade
```

**Requirements:**
- Python 3.11 or higher
- Git (optional, for version control features)
- Claude or Gemini CLI (for AI integration)

**Cross-Platform Support:**
- **Windows**: Requires Git Bash or WSL
- **Linux**: Native Bash support  
- **macOS**: Native Bash support
- **Source Installation**: Works perfectly from source code (not just PyPI)

## 🚀 Quick Start

### Step 1: Initialize Your Project

```bash
# Create a new project
specpulse init my-awesome-project

# Or add to existing project
cd existing-project
specpulse init --here
```

### Step 2: Configure AI Assistant

```bash
# For Claude projects
specpulse init --ai claude

# For Gemini projects
specpulse init --ai gemini
```

### Step 3: Start Building (Inside AI)

```bash
# Initialize a new feature
/sp-pulse user-authentication
# Creates structure for 001-user-authentication feature

# Create the specification
/sp-spec create user login with OAuth2 and email/password
# Or just: /sp-spec (for interactive mode)

# [NEW] Decompose large specs into microservices (optional)
/sp-decompose 001
# Creates service boundaries, API contracts, and interfaces

# Generate implementation plan
/sp-plan generate
# For decomposed: Creates service-specific plans + integration plan
# For monolithic: Creates single comprehensive plan

# Break down into tasks
/sp-task breakdown
# For decomposed: Creates AUTH-T001, USER-T001, INT-T001 tasks
# For monolithic: Creates T001, T002, T003 tasks

# [NEW] Execute all tasks continuously without stopping
/sp-execute all
# Completes ALL tasks in sequence without interruptions
# Or: /sp-execute (for next task), /sp-execute T001 (specific task)
```

### Step 4: Validate & Ship

```bash
# Validate everything
specpulse validate

# [NEW] Decompose specifications
specpulse decompose 001
# Or with options:
specpulse decompose --microservices
specpulse decompose --apis
specpulse decompose --interfaces

# Run diagnostics
specpulse doctor

# Sync project state
specpulse sync

# Template management
specpulse template list                    # List all templates
specpulse template validate [name]         # Validate templates
specpulse template preview <name>          # Preview template
specpulse template backup                  # Backup templates
specpulse template restore <path>          # Restore from backup

# Memory management
specpulse memory search <query>            # Search memory system
specpulse memory summary                   # Show memory summary
specpulse memory cleanup [--days 90]       # Clean old entries
specpulse memory export [--format json]    # Export memory data

# Help system
specpulse help [topic]                     # Show help
specpulse help --list                      # List all help topics
```

## ✨ Features

### 🧠 Memory Management (v1.7.0)

**Structured memory with tag-based organization:**
```bash
# Add architectural decision
specpulse memory add-decision "Use Stripe for payments" \
  --rationale "Better API, superior documentation" \
  --feature 003

# Add code pattern
specpulse memory add-pattern "API Error Format" \
  --example "{ success: bool, data: any, error: string }" \
  --features "001,002"

# Query decisions
specpulse memory query --tag decision --recent 5

# Get all relevant memory for feature
specpulse memory relevant 003
```

**Context injection for AI:**
```bash
# Set project context once
specpulse context set project.name "MyApp"
specpulse context set tech_stack.frontend "React, TypeScript"
specpulse context auto-detect  # Or auto-detect from package.json

# Context auto-injected in all /sp-* commands!
/sp-pulse new-feature
# AI sees tech stack automatically - no repetitive questions!
```

**Quick notes during development:**
```bash
# Capture insights without breaking flow
specpulse note "Stripe webhooks require HTTPS" --feature 003
specpulse note "Rate limit: 100 req/min per user"

# Review later
specpulse notes list 003

# Merge important notes to spec
specpulse notes merge 003 --note 20241006120000
```

### 📑 Tiered Templates (v1.6.0+)

SpecPulse supports three template tiers for progressive spec building - start minimal and expand when ready:

#### Tier 1: Minimal (Quick Start)
Perfect for rapid prototyping and simple features. Complete in 2-3 minutes:
- **What** (1 sentence)
- **Why** (1 sentence)
- **Done When** (3 checkboxes)

```bash
specpulse pulse new-feature --tier minimal
```

#### Tier 2: Standard (Ready to Plan)
Expand when you're ready for implementation planning:
- All Tier 1 content (preserved!)
- Executive Summary
- User Stories
- Functional Requirements
- Technical Approach

```bash
specpulse expand 001 --to-tier standard
```

#### Tier 3: Complete (Production Ready)
Full specification with comprehensive production details:
- All Tier 2 content (preserved!)
- Non-Functional Requirements
- Security Considerations
- Performance Requirements
- Testing Strategy
- Deployment Considerations

```bash
specpulse expand 001 --to-tier complete
```

**Key Features:**
- ✅ **Content Preservation**: Your work is never lost during expansion
- 🎯 **LLM Guidance**: Each template has comments guiding AI assistants
- 🔄 **Flexible Workflow**: Expand only when you need more detail
- 📊 **Automatic Backups**: Expansion creates timestamped backups
- 👁️ **Preview Changes**: Use `--show-diff` to see what will be added

### 🏛️ Universal SDD Principles

Nine principles that enable Specification-Driven Development for ANY project:

| # | Principle | Purpose | Applies To |
|---|-----------|---------|------------|
| **1** | Specification First | Start with clear requirements | All projects |
| **2** | Incremental Planning | Phased implementation | Web, mobile, desktop, games |
| **3** | Task Decomposition | Concrete, executable tasks | Any technology stack |
| **4** | Traceable Implementation | Link code to specs | All languages |
| **5** | Continuous Validation | Ensure spec alignment | Any framework |
| **6** | Quality Assurance | Appropriate testing | GUI, CLI, API, games |
| **7** | Architecture Documentation | Record decisions | Any architecture |
| **8** | Iterative Refinement | Evolve with learnings | All methodologies |
| **9** | Stakeholder Alignment | Shared understanding | Any team size |

### 🚦 Phase Gates System

Before any code is written, features must pass:

```
┌─────────────────┐
│ Specification   │ → Must be complete with no ambiguities
└────────┬────────┘
         ↓
┌─────────────────┐
│ Phase Gates     │ → SDD compliance check
└────────┬────────┘     Quality assurance strategy defined
         ↓              Architecture documented
┌─────────────────┐     Stakeholder alignment confirmed
│ Implementation  │     Research completed
└────────┬────────┘
         ↓
┌─────────────────┐
│ Validation      │ → Automated quality checks
└─────────────────┘
```

### 🎨 Beautiful CLI Experience

<details>
<summary>View CLI Screenshots</summary>

```
+=====================================================================+
|                                                                     |
|    _____ ____  _____ _____ ____  _   _ _     _____ _____           |
|   / ____|  _ \|  ___/ ____|  _ \| | | | |   / ____|  ___|          |
|   | (___ | |_) | |__ | |    | |_) | | | | |   | (___ | |__          |
|   \___ \|  __/|  __|| |    |  __/| | | | |    \___ \|  __|         |
|   ____) | |   | |___| |____| |   | |_| | |________) | |___         |
|   |_____/|_|   |______\_____|_|    \___/|______|_____/|_____|       |
|                                                                     |
|          Specification-Driven Development Framework                |
|                    Beyond Traditional Development                   |
|                                                                     |
+=====================================================================+
```

</details>

- **ASCII Art Banners** - Beautiful project initialization
- **Color-Coded Output** - Instant status recognition
- **Progress Indicators** - Real-time operation feedback
- **Interactive Tables** - Clean data presentation
- **Celebration Animations** - Milestone achievements

### 🧠 Intelligent Memory System

```
memory/
├── constitution.md  # Immutable project principles
├── context.md      # Current state and progress tracking
└── decisions.md    # Architecture Decision Records (ADRs)
```

- **Persistent Context**: Never lose track of project state
- **Decision History**: Understand why choices were made
- **SDD Enforcement**: Universal principles for any software project

### 🔍 [NEEDS CLARIFICATION] Markers

Stop guessing what users want:

```markdown
## Requirements
- User authentication via OAuth2
- Password reset via email
- [NEEDS CLARIFICATION: Should we support 2FA?]
- [NEEDS CLARIFICATION: Password complexity rules?]
```

### 🤖 Deep AI Integration

**Available AI Commands:**
- `/sp-pulse` - Initialize features
- `/sp-spec` - Create/update specifications
- `/sp-plan` - Generate implementation plans
- `/sp-task` - Create task breakdowns
- `/sp-execute` - Execute tasks continuously
- `/sp-decompose` - Decompose into microservices
- `/sp-status` - Show feature progress
- `/sp-continue` - Resume execution

**How AI Commands Work:**

Claude and Gemini use slash commands that accept arguments via `$ARGUMENTS`:

**Script Execution:**
- **Cross-Platform Scripts**: Bash (.sh) and PowerShell (.ps1) scripts included
- **Requirements**: Bash shell (Git Bash on Windows) or PowerShell
- **Universal Compatibility**: Works whether installed via PyPI or source code
- **Unicode Support**: Full international character support (≤, ≥, →, ←)
- **Template System**: Templates exist as physical files in `resources/templates/` for AI tools to read

```bash
/sp-pulse user-authentication     # Start new feature with name
/sp-spec create OAuth2 login      # Create specification with description
/sp-spec update                   # Update existing specification
/sp-spec validate                 # Validate specification completeness
/sp-decompose 001                 # Decompose spec into microservices
/sp-plan generate                 # Generate plan(s) - detects decomposition
/sp-plan validate                 # Validate plan against constitution
/sp-task breakdown                # Create task list(s) - per service if decomposed
/sp-task update                   # Update task statuses
/sp-status                        # Show current feature status and progress
/sp-execute all                   # Execute ALL tasks non-stop until completion
/sp-execute                       # Execute next task and continue
/sp-execute T001                  # Execute specific task and continue
/sp-continue                      # Continue from last stopped task
```

**Behind the Scenes:**
- Commands capture arguments using `$ARGUMENTS` variable
- **Shell scripts** in `resources/scripts/` folder process the arguments:
  - `sp-pulse-*.sh` - Bash scripts (all platforms)
  - `sp-pulse-*.ps1` - PowerShell scripts (Windows native)
- Templates are **physical files** in `resources/templates/` and also embedded in code
- Results are saved in `specs/`, `plans/`, `tasks/` folders
- Memory system tracks progress in `memory/` folder

**🔒 Important Security Rules:**
- **Protected Directories** (Read-Only after init):
  - `templates/` - Generated template files (created on init)
  - `scripts/` - Shell and PowerShell scripts
  - `commands/` - AI command definitions
  - `.claude/` and `.gemini/` - AI configurations
- **Editable Directories**:
  - `specs/` - Feature specifications (AI creates/edits here)
  - `plans/` - Implementation plans (AI creates/edits here)
  - `tasks/` - Task breakdowns (AI creates/edits here)
  - `memory/` - Project context and decisions
- **Workflow**: Templates are used as references, content is generated in working directories

**Claude vs Gemini:**
- **Claude**: Uses Markdown command files (`.claude/commands/*.md`) with YAML frontmatter
  - Arguments passed via `$ARGUMENTS` variable to shell scripts
- **Gemini**: Uses TOML command files (`.gemini/commands/*.toml`) with simple format
  - Arguments handled via `{{args}}` placeholder in prompts
- Both support arguments and work the same way from user perspective

**Command Arguments:**
- Commands can accept arguments: `/command arg1 arg2`
- Claude: Arguments passed to scripts via `$ARGUMENTS`
- Gemini: Arguments injected via `{{args}}` placeholder
- Commands can be used without arguments for interactive mode

## 📊 Real-World Impact

| Metric | Traditional Development | With SpecPulse |
|--------|------------------------|----------------|
| **Requirements Clarity** | ~60% | **95%+** |
| **First-Time Success Rate** | ~40% | **85%+** |
| **Code Review Iterations** | 3-5 | **1-2** |
| **Technical Debt** | Accumulates | **Tracked & Managed** |
| **Documentation** | Often outdated | **Always current** |

## 🚀 Continuous Task Execution (NEW in v1.3.0)

SpecPulse now supports **non-stop task execution** for maximum development efficiency:

### The `/sp-execute` Command

Complete entire features without interruptions:

```bash
# Execute ALL tasks continuously
/sp-execute all
# AI will complete every task in sequence without stopping

# Execute next task and continue
/sp-execute
# Starts with next pending task and keeps going

# Execute from specific task
/sp-execute T001
# Starts from T001 and continues through all remaining tasks
```

### Flow State Development

The continuous execution mode enables:
- **Zero Context Switching**: No stops between tasks
- **Maximum Efficiency**: Complete features 10x faster
- **Uninterrupted Flow**: Maintain focus and productivity
- **Automatic Progression**: Smart task advancement
- **Batch Processing**: Handle entire task lists in one go

### Example Workflow

```bash
# Traditional approach (multiple commands, lots of waiting)
/sp-task execute T001
# ... wait for completion ...
/sp-task execute T002
# ... wait for completion ...
/sp-task execute T003
# ... and so on ...

# NEW: Continuous execution (one command, no waiting)
/sp-execute all
# Completes T001, T002, T003... T025 automatically!
```

### Benefits

| Traditional Execution | Continuous Execution |
|----------------------|---------------------|
| Stop after each task | Non-stop completion |
| Constant confirmations | Automatic progression |
| Context switching | Flow state maintained |
| 5-10 tasks/hour | 50+ tasks/hour |
| Manual task selection | Smart task ordering |

## 🎯 Microservice Decomposition

For large, complex specifications, SpecPulse can automatically decompose them into microservices:

```bash
# Decompose a specification
/sp-decompose 001
```

This creates:
- **Service Boundaries**: Using Domain-Driven Design principles
- **API Contracts**: OpenAPI 3.0 specifications for each service
- **Interface Definitions**: TypeScript/Java/Go interfaces
- **Integration Map**: Service communication architecture
- **Migration Plan**: Strategy for breaking down monoliths

### Workflow Adaptation

SpecPulse automatically adapts based on architecture:

**Monolithic Flow:**
```
spec-001.md → plan-001.md → task-001.md (T001, T002...)
```

**Decomposed Flow:**
```
spec-001.md → decomposition/ → service plans → service tasks
                ├── microservices.md      ├── auth-service-plan.md    ├── AUTH-T001
                ├── api-contracts/        ├── user-service-plan.md    ├── USER-T001
                └── interfaces/           └── integration-plan.md     └── INT-T001
```

## 🏗️ Architecture

**Core Components:**
1. **CLI Layer** (`specpulse/cli/main.py`) - Command-line interface with argparse
2. **Core Engine** (`specpulse/core/`) - Template management, validation, memory
   - `specpulse.py` - Project initialization and resource management
   - `validator.py` - Specification validation with enhanced rules
   - `template_manager.py` - Template validation and management
   - `memory_manager.py` - Project memory and context tracking
   - `validation_rules.py` - Comprehensive validation rule system
3. **Utilities** (`specpulse/utils/`) - Console, Git, error handling, version check
   - `console.py` - Rich terminal output with animations
   - `git_utils.py` - Git integration
   - `error_handler.py` - Advanced error handling and recovery
   - `version_check.py` - PyPI version checking
4. **Resources** (`specpulse/resources/`) - Templates, scripts, commands, memory files

## 🏗️ Project Structure

```
my-project/
├── .specpulse/          # Configuration and cache
│   ├── config.yaml      # Project settings
│   └── backups/         # Template backups
├── .claude/             # Claude AI integration
│   └── commands/        # Claude command definitions (.md)
├── .gemini/             # Gemini AI integration
│   └── commands/        # Gemini command definitions (.toml)
├── memory/              # Project intelligence
│   ├── constitution.md  # Immutable principles
│   ├── context.md      # Current state
│   └── decisions.md    # Architecture Decision Records
├── specs/               # Feature specifications
│   └── 001-feature/
│       ├── spec-001.md
│       └── decomposition/    # [NEW] Microservice decomposition
│           ├── microservices.md
│           ├── api-contracts/
│           └── interfaces/
├── plans/               # Implementation plans
│   └── 001-feature/
│       ├── plan-001.md      # Monolithic plan
│       # OR for decomposed:
│       ├── auth-service-plan.md
│       ├── user-service-plan.md
│       └── integration-plan.md
├── tasks/               # Task breakdowns
│   └── 001-feature/
│       ├── task-001.md      # Monolithic tasks
│       # OR for decomposed:
│       ├── auth-service-tasks.md
│       ├── user-service-tasks.md
│       └── integration-tasks.md
├── templates/           # Generated templates (created on init)
├── scripts/             # Cross-platform scripts for AI execution
│   ├── sp-pulse-init.sh     # Feature initialization (Bash)
│   ├── sp-pulse-init.ps1    # Feature initialization (PowerShell)
│   ├── sp-pulse-spec.sh     # Specification creation (Bash)
│   ├── sp-pulse-spec.ps1    # Specification creation (PowerShell)
│   ├── sp-pulse-plan.sh     # Plan generation (Bash)
│   ├── sp-pulse-plan.ps1    # Plan generation (PowerShell)
│   ├── sp-pulse-task.sh     # Task breakdown (Bash)
│   ├── sp-pulse-task.ps1    # Task breakdown (PowerShell)
│   ├── sp-pulse-decompose.sh  # Microservice decomposition (Bash)
│   ├── sp-pulse-decompose.ps1 # Microservice decomposition (PowerShell)
│   ├── sp-pulse-execute.sh    # Continuous task execution (Bash)
│   └── sp-pulse-execute.ps1   # Continuous task execution (PowerShell)
└── PULSE.md            # Project manifest
```

## 🛠️ Advanced Usage

### Template Management

**List Templates:**
```bash
specpulse template list                    # All templates
specpulse template list --category spec    # Specific category
```

**Validate Templates:**
```bash
specpulse template validate                # All templates
specpulse template validate spec.md        # Specific template
specpulse template validate --fix          # Auto-fix issues
```

**Preview & Backup:**
```bash
specpulse template preview spec.md         # Preview with sample data
specpulse template backup                  # Create backup
specpulse template restore /path/backup    # Restore from backup
```

### Memory Management

**Search Memory:**
```bash
specpulse memory search "authentication"      # Search all
specpulse memory search "API" --category decisions  # Filter by category
specpulse memory search "bug" --days 30      # Last 30 days
```

**Memory Operations:**
```bash
specpulse memory summary                   # Show statistics
specpulse memory cleanup --days 90         # Remove old entries
specpulse memory export --format json      # Export to JSON
specpulse memory export --format yaml --output backup.yaml
```

### Custom Templates

Create project-specific templates:

```bash
# Templates are in templates/ directory
# Modify as needed, but keep filenames unchanged
# spec.md, plan.md, task.md must remain as-is
```

### Validation Rules

Configure validation in `.specpulse/config.yaml`:

```yaml
validation:
  enforce_constitution: true
  max_complexity: 3
  require_tests: true
  spec_sections:
    - requirements
    - user_stories
    - acceptance_criteria
```

### Git Integration

```bash
# Smart commits with context
specpulse sync

# Branch management
git checkout -b 001-new-feature
```

## 📈 Metrics & Reporting

Track your project health:

```bash
# Full system diagnostic
specpulse doctor

# Detailed validation report
specpulse validate --verbose

# Component-specific checks
specpulse validate --component spec
specpulse validate --component plan
specpulse validate --component constitution
```

## 🔧 Troubleshooting

<details>
<summary>Common Issues & Solutions</summary>

### Import Error
**Problem**: `ModuleNotFoundError: No module named 'specpulse'`
**Solution**: Ensure Python 3.11+ and run `pip install --upgrade specpulse`

### Git Integration Issues
**Problem**: Git commands failing
**Solution**: Install Git or use `--no-git` flag

### Template Not Found
**Problem**: Custom templates not loading
**Solution**: Check template path in config.yaml

### AI Commands Not Working
**Problem**: `/sp-pulse` commands not recognized
**Solution**: Ensure you ran `specpulse init --ai claude` or `--ai gemini`

</details>

## 🤝 Contributing

We welcome contributions! The project is actively maintained and looking for contributors.

```bash
# Fork and clone
git clone https://github.com/specpulse/specpulse.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
pytest tests/

# Submit PR
```

## 📚 Documentation

### 🎯 Help System
SpecPulse includes a comprehensive built-in help system with 6 detailed topics:
```bash
# List all help topics
specpulse help --list

# Get specific help
specpulse help overview         # Key concepts and principles
specpulse help commands         # Complete command reference
specpulse help workflow         # Development workflow
specpulse help templates        # Template system and customization
specpulse help examples         # Real-world usage examples
specpulse help troubleshooting  # Common issues and solutions
```

**Help Topics Include:**
- **Overview**: SDD principles, project structure, AI integration
- **Commands**: Full CLI reference with examples
- **Workflow**: Step-by-step development process
- **Templates**: Template system, variables, customization
- **Examples**: Real-world scenarios for web, mobile, API, microservices
- **Troubleshooting**: Common issues, solutions, debug mode

### 📖 Documentation Files
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation index
- **[CLI_REFERENCE.md](CLI_REFERENCE.md)** - Comprehensive CLI command reference
- **[HELP_SYSTEM.md](HELP_SYSTEM.md)** - Help system documentation
- **[SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md)** - Complete usage guide
- **[SPECDRIVEN.md](SPECDRIVEN.md)** - Specification-Driven Development methodology
- **[CLAUDE.md](CLAUDE.md)** - Development instructions for AI assistants
- **[PyPI Package](https://pypi.org/project/specpulse/)** - Official package page
- **[GitHub Repository](https://github.com/specpulse/specpulse)** - Source code and issues

### 🔧 Advanced Features (v1.5.0)

**Template Management:**
- Template validation with auto-fix capability
- Template preview with sample data
- Backup and restore functionality
- Category filtering (spec, plan, task, decomposition)

**Memory Management:**
- Full-text search across memory system
- Memory summary with statistics
- Automatic cleanup of old entries
- Export to JSON/YAML formats

**Enhanced Error Handling:**
- Context-aware error messages
- Automatic recovery suggestions
- Command correction suggestions
- Detailed technical information in verbose mode

**Version Management:**
- Automatic PyPI version checking
- Update notifications for new releases
- Single source of truth in `_version.py`

## 📚 Usage Guide

### How to Break Your Project into Features (Pulses)

A complete guide is available in **[SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md)** which covers:
- Feature decomposition strategies
- Sizing guidelines (3-15 tasks per pulse)
- Naming conventions (001-feature-name format)
- Real-world examples for different project types
- Best practices for feature boundaries

#### Quick Examples

**E-Commerce Platform:**
```
001-user-authentication    # Registration, login, sessions
002-product-catalog        # Products, categories, search
003-shopping-cart          # Cart management, calculations
004-payment-processing     # Gateway, transactions, receipts
005-order-management       # History, tracking, refunds
```

**SaaS Application:**
```
001-tenant-management      # Multi-tenancy, workspaces
002-subscription-billing   # Plans, payments, invoices
003-api-management        # Keys, rate limiting, docs
004-admin-dashboard       # Analytics, reports, settings
005-webhook-system        # Events, notifications, logs
```

**Key Principles:**
- Each pulse should be **independent** and **testable**
- Size appropriately for your project type
- Use **sequential numbering** (001, 002, 003...)
- Follow the **9 universal SDD principles**

See the full guide for detailed breakdowns and strategies.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🚦 Project Status

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/specpulse/specpulse)
[![Coverage](https://img.shields.io/badge/coverage-improving-yellow)](https://github.com/specpulse/specpulse)
[![Tests](https://img.shields.io/badge/tests-core%20passing-brightgreen)](https://github.com/specpulse/specpulse)
[![Maintainability](https://img.shields.io/badge/maintainability-A-brightgreen)](https://github.com/specpulse/specpulse)

---

<div align="center">

**Built with ❤️ for developers who refuse to compromise on quality**

[Report Bug](https://github.com/specpulse/specpulse/issues) • [Request Feature](https://github.com/specpulse/specpulse/issues) • [Join Discussion](https://github.com/specpulse/specpulse/discussions)

</div>