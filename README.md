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

> **Latest Update (v1.4.4)** - Critical Workflow Fixes:
> - 🐛 **Fixed Script Numbering**: Resolved `/sp-pulse` creating empty placeholders while subsequent commands created new files
> - 🎯 **Fixed Task Detection**: Execute scripts now properly detect task format (`### T001:` with `**Status**:`)
> - 📝 **Unified Placeholders**: All scripts use consistent `<!-- INSTRUCTION: Generate -->` markers
> - 🔧 **PowerShell Parity**: PowerShell scripts now match Bash behavior exactly
>
> **v1.4.3** - Script Numbering Fix:
> - 🔢 **Fixed Numbering Logic**: Spec, plan, and task files now number correctly (001, 002, 003...)
> - 📝 **No Empty First Files**: spec-001.md, plan-001.md, task-001.md always contain content
> - 🎯 **Proper Interactive Mode**: Scripts create placeholder files for AI to fill
>
> **v1.4.2** - Template System Enhancement:
> - 📁 **Physical Template Files**: Templates now exist as physical files for AI tools to read
> - 🔧 **Complete PowerShell Support**: Added PowerShell scripts matching all Bash functionality
> - 📝 **Enhanced Decomposition Templates**: Full microservice decomposition template support
>
> **v1.4.1** - Bug Fix Release:
> - 🐛 **Fixed Version Display**: Corrected `--version` command showing old version
>
> **v1.4.0** - Complete Framework Revolution:
> - 🚀 **Universal SDD Framework**: Transformed from Constitutional to Specification-Driven Development
> - 🎯 **No Technology Restrictions**: Support for ANY technology stack - web, mobile, desktop, games, ML
> - 🧪 **Comprehensive Testing**: Full test suite with extensive coverage
> - ✨ **9 Universal Principles**: Flexible principles replacing rigid articles
> - 🔄 **Major API Updates**: All methods renamed from `constitution` to `sdd_compliance`
> - 📝 **Enhanced Documentation**: Complete overhaul of docs and templates
> - 🏗️ **Hybrid Template System**: Templates exist as both files and embedded code

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
```

## ✨ Features

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
/sp-task status                   # Show current progress
/sp-execute all                   # [NEW] Execute ALL tasks non-stop until completion
/sp-execute                       # [NEW] Execute next task and continue
/sp-execute T001                  # [NEW] Execute specific task and continue
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

## 🏗️ Project Structure

```
my-project/
├── .specpulse/          # Configuration and cache
│   └── config.yaml      # Project settings
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

### Custom Templates

Create project-specific templates:

```bash
# Copy and modify templates
cp templates/spec-001.md templates/custom-spec.md
# Edit to match your needs
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

- **[PyPI Package](https://pypi.org/project/specpulse/)** - Official package page
- **[GitHub Repository](https://github.com/specpulse/specpulse)** - Source code and issues
- **Command Reference** - See AI Integration section above for full command list

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