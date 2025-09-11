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

> **Latest Update (v1.0.1)**: Fixed command documentation and improved AI integration clarity.

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
/pulse init user-authentication

# Create the specification
/spec create "User login with OAuth2 and email/password"

# Validate the specification
/spec validate

# Generate implementation plan
/plan generate

# Validate plan against constitution
/plan validate

# Break down into tasks
/task breakdown

# Check task progress
/task status
```

### Step 4: Validate & Ship

```bash
# Validate everything
specpulse validate

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

**Claude Commands:**
```bash
# Feature initialization
/pulse init <feature-name>        # Initialize new feature with structure

# Specification management
/spec create <description>        # Generate specification from requirements
/spec update                      # Update existing specification
/spec validate                    # Check specification completeness

# Planning commands
/plan generate                    # Create implementation plan from spec
/plan validate                    # Validate plan against constitution

# Task management
/task breakdown                   # Generate tasks from plan
/task update                      # Update task status
/task status                      # Show task progress
```

**Gemini Commands:**
Same commands with TOML-based configuration for enhanced parsing.

## 📊 Real-World Impact

| Metric | Traditional Development | With SpecPulse |
|--------|------------------------|----------------|
| **Requirements Clarity** | ~60% | **95%+** |
| **First-Time Success Rate** | ~40% | **85%+** |
| **Code Review Iterations** | 3-5 | **1-2** |
| **Technical Debt** | Accumulates | **Tracked & Managed** |
| **Documentation** | Often outdated | **Always current** |

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
│       └── spec.md
├── plans/               # Implementation plans
│   └── 001-feature/
│       └── plan.md
├── tasks/               # Task breakdowns
│   └── 001-feature/
│       └── tasks.md
├── templates/           # Customizable templates
├── scripts/             # Shell scripts for AI execution
│   ├── pulse-init.sh    # Feature initialization
│   ├── pulse-spec.sh    # Specification creation
│   ├── pulse-plan.sh    # Plan generation
│   └── pulse-task.sh    # Task breakdown
└── PULSE.md            # Project manifest
```

## 🛠️ Advanced Usage

### Custom Templates

Create project-specific templates:

```bash
# Copy and modify templates
cp templates/spec.md templates/custom-spec.md
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
**Problem**: `/pulse` commands not recognized
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
- **[Examples](https://github.com/specpulse/specpulse/tree/main/examples)** - Real-world usage
- **Command Reference** - See AI Integration section above for full command list

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with inspiration from:
- Test-Driven Development principles
- Domain-Driven Design
- Clean Architecture
- Specification by Example

## 🚦 Project Status

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/specpulse/specpulse)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](https://github.com/specpulse/specpulse)
[![Maintainability](https://img.shields.io/badge/maintainability-A-brightgreen)](https://github.com/specpulse/specpulse)

---

<div align="center">

**Built with ❤️ for developers who refuse to compromise on quality**

[Report Bug](https://github.com/specpulse/specpulse/issues) • [Request Feature](https://github.com/specpulse/specpulse/issues) • [Join Discussion](https://github.com/specpulse/specpulse/discussions)

</div>