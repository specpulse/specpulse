# SpecPulse

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/specpulse.svg)](https://pypi.org/project/specpulse/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/specpulse)](https://pypi.org/project/specpulse/)

**Transform Your Development Process with Specification-Driven Development**

*Build better software faster by putting specifications first and letting AI handle the implementation details.*

[Installation](#-installation) • [Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 What is SpecPulse?

SpecPulse revolutionizes AI-assisted development by enforcing a **specification-first approach**. Instead of jumping straight into code, SpecPulse ensures every feature starts with clear specifications, validated plans, and tracked tasks - guaranteeing quality from day one.

> **Latest Update (v1.2.0)**: 
> - 🔀 **Microservice Decomposition**: New `/sp-decompose` command to break large specs into services
> - 🏗️ **Service-Based Planning**: Automatic service-specific plans and integration plans
> - 📊 **Service Task Management**: Task prefixes per service (AUTH-T001, USER-T001, INT-T001)
> - 🎯 **Smart Workflow Detection**: Automatic monolithic vs decomposed architecture handling
> - 📝 **Rich Templates**: New templates for services, APIs, interfaces, and integration
> - 🔧 **Previous (v1.1.0)**: Command prefix system, multi-spec workflow, versioned files

### Why SpecPulse?

- **🔍 Clarity First**: No more ambiguous requirements or scope creep
- **🤖 AI-Optimized**: Designed specifically for Claude and Gemini workflows
- **✅ Quality Gates**: Built-in checks prevent bad code from entering your codebase
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

### 🏛️ Constitutional Development

Nine immutable principles guide every line of code:

| Article | Principle | Benefit |
|---------|-----------|---------|
| **I** | Library-First | Every feature is modular and reusable |
| **II** | CLI Interface | Text-based interaction for automation |
| **III** | Test-First | Tests before code, always |
| **IV** | Staged Implementation | Incremental, validated progress |
| **V** | Direct Framework Usage | No unnecessary abstractions |
| **VI** | No Abstraction Layers | Keep it simple, keep it maintainable |
| **VII** | Simplicity Enforcement | Maximum 3 modules per feature |
| **VIII** | Complexity Tracking | Document and justify exceptions |
| **IX** | Framework-First | Don't reinvent the wheel |

### 🚦 Phase Gates System

Before any code is written, features must pass:

```
┌─────────────────┐
│ Specification   │ → Must be complete with no ambiguities
└────────┬────────┘
         ↓
┌─────────────────┐
│ Phase Gates     │ → Constitutional compliance check
└────────┬────────┘     Simplicity validation (≤3 modules)
         ↓              Test strategy defined
┌─────────────────┐     Framework selected
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
- **Constitutional Enforcement**: Principles that can't be violated

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
- **All Platforms**: Bash (.sh) scripts only
- **Requirements**: Bash shell required (Git Bash on Windows, native on Linux/macOS)
- **Universal Compatibility**: Works whether installed via PyPI or source code
- **Unicode Support**: Full international character support (≤, ≥, →, ←)

```bash
/sp-pulse user-authentication     # Start new feature with name
/sp-spec create OAuth2 login      # Create specification with description
/sp-spec update                   # Update existing specification
/sp-spec validate                 # Validate specification completeness
/sp-decompose 001                 # [NEW] Decompose spec into microservices
/sp-plan generate                 # Generate plan(s) - detects decomposition
/sp-plan validate                 # Validate plan against constitution
/sp-task breakdown                # Create task list(s) - per service if decomposed
/sp-task update                   # Update task statuses
/sp-task status                   # Show current progress
/sp-task execute AUTH-T001        # [NEW] Execute service-specific task
```

**Behind the Scenes:**
- Commands capture arguments using `$ARGUMENTS` variable
- **Shell scripts** in `resources/scripts/` folder process the arguments:
  - `sp-pulse-*.sh` - Bash scripts (all platforms)
- AI reads templates from `resources/templates/` folder
- Results are saved in `specs/`, `plans/`, `tasks/` folders
- Memory system tracks progress in `memory/` folder

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

## 🎯 Microservice Decomposition (NEW)

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
├── templates/           # Customizable templates
├── scripts/             # Shell scripts for AI execution
│   ├── sp-pulse-init.sh    # Feature initialization
│   ├── sp-pulse-spec.sh    # Specification creation
│   ├── sp-pulse-plan.sh    # Plan generation
│   └── sp-pulse-task.sh    # Task breakdown
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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🚦 Project Status

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/specpulse/specpulse)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/specpulse/specpulse)
[![Tests](https://img.shields.io/badge/tests-37%2B%20passed-brightgreen)](https://github.com/specpulse/specpulse)
[![Maintainability](https://img.shields.io/badge/maintainability-A-brightgreen)](https://github.com/specpulse/specpulse)

---

<div align="center">

**Built with ❤️ for developers who refuse to compromise on quality**

[Report Bug](https://github.com/specpulse/specpulse/issues) • [Request Feature](https://github.com/specpulse/specpulse/issues) • [Join Discussion](https://github.com/specpulse/specpulse/discussions)

</div>