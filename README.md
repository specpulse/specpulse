# SpecPulse v2.1.0

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/specpulse.svg)](https://pypi.org/project/specpulse/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/specpulse)](https://pypi.org/project/specpulse/)

**AI-Enhanced Specification-Driven Development Framework**

*Build better software faster with specifications first, AI assistance, and intelligent workflow management.*

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [CLI Commands](#cli-commands) • [Documentation](#documentation)

</div>

---

## 🎯 What is SpecPulse?

SpecPulse is a **CLI-first, AI-enhanced framework** for Specification-Driven Development (SDD). It helps teams build software by:

1. **Specification First**: Every feature starts with a clear, validated specification
2. **AI-Enhanced**: Works seamlessly with Claude Code and Gemini CLI
3. **CLI-Driven**: Pure Python CLI - no scripts, fully cross-platform
4. **LLM-Friendly**: Generates files optimized for AI assistants to expand

### 🚀 v2.1.0 Highlights

- ✅ **No Scripts**: Eliminated bash/PowerShell scripts - pure Python CLI
- ✅ **Smaller Projects**: ~50KB less per project (no scripts folder)
- ✅ **Faster**: ~3x faster execution (no shell overhead)
- ✅ **Cross-Platform**: Works identically on Windows, macOS, Linux
- ✅ **LLM-Optimized**: Files designed for AI expansion

---

## 📦 Installation

```bash
# Install from PyPI
pip install specpulse==2.1.0

# Or upgrade from previous version
pip install --upgrade specpulse
```

**Requirements:**
- Python 3.11 or higher
- Git (recommended for branch-based features)
- Works on Windows, macOS, and Linux

---

## 🚀 Quick Start

### 1. Initialize Project

```bash
# Create new project
specpulse init my-project --ai claude

# Or add to existing project
cd existing-project
specpulse init --here --ai claude
```

### 2. Start a Feature

```bash
# Initialize feature structure
specpulse feature init user-authentication

# This creates:
# - specs/001-user-authentication/
# - plans/001-user-authentication/
# - tasks/001-user-authentication/
# - Updates memory/context.md
```

### 3. Create Specification

```bash
# Create spec (LLM will expand this)
specpulse spec create "OAuth2 login with JWT tokens"

# Creates: specs/001-user-authentication/spec-001.md
# With template and LLM expansion markers
```

### 4. Work in Claude Code or Gemini CLI

Use custom slash commands for AI-assisted development:

```bash
# In Claude Code or Gemini CLI:
/sp-pulse user-authentication        # Initialize feature
/sp-spec create OAuth2 with JWT      # Create specification
/sp-plan generate                     # Generate implementation plan
/sp-task breakdown                    # Break down into tasks
/sp-execute                           # Execute tasks continuously
```

---

## ✨ Features

### 🎯 Core Features

- **Feature Management**: Initialize and switch between features
- **Specification Management**: Create, validate, and version specifications
- **Plan Generation**: AI-assisted implementation planning
- **Task Breakdown**: Convert plans into actionable tasks
- **Execution Tracking**: Track task progress and completion
- **Memory System**: Project context and decision tracking
- **AI Integration**: Works with Claude Code and Gemini CLI

### 🔧 3-Tier Template System

Choose the right level of detail for your project:

1. **Minimal** (2-3 min): Quick prototypes and MVPs
2. **Standard** (10-15 min): Most production features
3. **Complete** (30-45 min): Enterprise-grade specifications

### 📊 Validation & Progress Tracking

- Automatic validation with actionable feedback
- Progress indicators for specs, plans, tasks
- Checkpoint system for safe iterations
- Auto-fix capabilities for common issues

---

## 💻 CLI Commands

**Two Ways to Use SpecPulse:**

1. **Inside AI Assistant (Primary)** - LLM uses file operations
2. **Terminal (Optional)** - Direct CLI commands for manual use

### Feature Management

```bash
# Terminal use (optional - for manual workflow)
specpulse feature init <name>           # Initialize new feature
specpulse feature continue <name>       # Switch to existing feature

# Inside Claude/Gemini (primary - LLM does this automatically)
/sp-pulse user-authentication
# → LLM uses mkdir, Write, Edit tools to create structure
```

### Specification Management

```bash
# Terminal use (optional)
specpulse spec create <description>     # Create specification
specpulse spec update <id> <desc>       # Update specification
specpulse spec validate                 # Validate specifications
specpulse spec progress <feature-id>    # Show completion progress

# Inside Claude/Gemini (primary)
/sp-spec OAuth2 login with JWT
# → LLM uses Read (template) → Write (file) → Edit (expand)
```

### Plan Management

```bash
# Terminal use (optional)
specpulse plan create <description>     # Create implementation plan
specpulse plan update <id> <desc>       # Update plan

# Inside Claude/Gemini (primary - LLM file operations)
/sp-plan generate
```

### Task Management

```bash
# Terminal use (optional)
specpulse task create <description>     # Create task
specpulse task breakdown <plan-id>      # Generate tasks from plan
specpulse task update <id> <desc>       # Update task

# Inside Claude/Gemini (primary - LLM file operations)
/sp-task breakdown
```

### Execution Tracking

```bash
# Terminal use (optional)
specpulse execute start <task-id>       # Mark task as started
specpulse execute done <task-id>        # Mark task as completed

# Inside Claude/Gemini (primary - LLM edits task metadata)
/sp-execute
```

### Project Management (Terminal Only)

These are **utility commands** - used from terminal, not by LLM:

```bash
specpulse init <project>                # Initialize project
specpulse validate all --fix            # Validate and auto-fix
specpulse doctor                        # System health check
specpulse sync                          # Synchronize project state
specpulse ai context                    # Show AI-detected context
specpulse ai suggest                    # Get AI recommendations
```

---

## 🤖 AI Integration

SpecPulse works seamlessly with AI assistants while maintaining **privacy-first design** (no external API calls).

### How It Works

```
User in Claude Code / Gemini CLI
    ↓
Custom Slash Commands (/sp-pulse, /sp-spec, etc.)
    ↓
LLM Uses File Operations (Read, Write, Edit)
    ↓
    1. Read template (templates/spec.md)
    2. Write file (specs/001-feature/spec-001.md)
    3. Read created file
    4. Expand with AI intelligence
    5. Write expanded content back
    ↓
Complete Specifications, Plans, Tasks
```

**Note**: CLI commands (`specpulse spec create`) are **optional helpers** for terminal use. LLM primarily uses **file operations** (Read/Write/Edit) for better control.

### AI Commands

```bash
# Context detection
specpulse ai context                    # Show detected feature, branch, etc.

# Suggestions
specpulse ai suggest                    # Get next-step recommendations
specpulse ai suggest --query "help"     # Get help on specific topic

# LLM switching
specpulse ai switch claude              # Use Claude
specpulse ai switch gemini              # Use Gemini
specpulse ai switch both                # Use both

# Checkpoints
specpulse ai checkpoint "description"   # Create workflow checkpoint
specpulse ai summary                    # Show workflow summary
```

---

## 📋 Complete Workflow Example

```bash
# 1. Initialize project
specpulse init my-app --ai claude

# 2. Start feature
specpulse feature init user-authentication

# 3. Create specification
specpulse spec create "OAuth2 login with JWT tokens and 2FA"

# 4. LLM expands spec (in Claude Code: /sp-spec validate)

# 5. Generate plan
specpulse plan create "Implementation roadmap for OAuth2"

# 6. LLM generates plan (in Claude Code: /sp-plan validate)

# 7. Break down tasks
specpulse task breakdown 001

# 8. LLM creates tasks (in Claude Code: /sp-task validate)

# 9. Execute tasks
specpulse execute start 001
# [Implement task]
specpulse execute done 001

# 10. Repeat for all tasks
```

---

## 📁 Project Structure

After initialization:

```
my-project/
├── .specpulse/          # SpecPulse configuration
├── .claude/commands/    # Claude Code slash commands
├── .gemini/commands/    # Gemini CLI slash commands
├── memory/              # Project context and decisions
│   └── context.md       # Current feature, decisions
├── templates/           # Specification templates
│   ├── spec.md
│   ├── plan.md
│   └── task.md
├── specs/               # Feature specifications (created on-demand)
├── plans/               # Implementation plans (created on-demand)
└── tasks/               # Task breakdowns (created on-demand)
```

**Note**: No `scripts/` folder! v2.1.0 uses pure CLI.

---

## 📚 Documentation

### Comprehensive Guides

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[AI Integration Guide](docs/AI_INTEGRATION.md)** - Complete AI integration documentation
- **[Migration Guide](docs/MIGRATION.md)** - Upgrading from previous versions
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Help System

```bash
# Get help
specpulse --help
specpulse feature --help
specpulse spec --help

# Show version
specpulse --version
```

---

## 🔄 Migration from v2.0.0

v2.1.0 is backward compatible with v2.0.0 projects:

```bash
# 1. Upgrade SpecPulse
pip install --upgrade specpulse

# 2. Delete old scripts (safe to remove)
rm -rf scripts/

# 3. That's it! Slash commands now use CLI
```

**Breaking Changes:**
- ⚠️ Scripts removed (replaced with CLI commands)
- ✅ All slash commands updated automatically
- ✅ No data migration needed
- ✅ Existing specs, plans, tasks remain compatible

---

## 🛠️ Advanced Features

### Custom Templates

```bash
# List templates
specpulse template list

# Validate templates
specpulse template validate

# Backup templates
specpulse template backup
```

### Memory Management

```bash
# Add architectural decision
specpulse memory add-decision "Use OAuth2" --rationale "Industry standard"

# Search memory
specpulse memory search "authentication"

# Export memory
specpulse memory export --format json
```

### Checkpoint System

```bash
# Create checkpoint
specpulse checkpoint create 001 "Before major refactor"

# List checkpoints
specpulse checkpoint list 001

# Restore checkpoint
specpulse checkpoint restore 001 checkpoint-001

# Cleanup old checkpoints
specpulse checkpoint cleanup 001 --older-than-days 30
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

```bash
# Clone repository
git clone https://github.com/specpulse/specpulse.git
cd specpulse

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run code quality checks
black specpulse/
flake8 specpulse/
mypy specpulse/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to:
- The SpecPulse community for feedback and contributions
- Claude Code and Gemini CLI teams for AI assistant platforms
- Everyone who helped shape v2.1.0's architecture

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/specpulse/specpulse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/specpulse/specpulse/discussions)
- **Help Command**: `specpulse --help`

---

## 🎯 Why SpecPulse?

### Before SpecPulse

```
❌ No standardized workflow
❌ Specifications often outdated
❌ Hard to track feature progress
❌ Manual context switching
❌ Inconsistent documentation
```

### After SpecPulse

```
✅ Standardized SDD workflow
✅ Specifications always up-to-date
✅ Automatic progress tracking
✅ Smart context detection
✅ Consistent, validated documentation
```

---

**🎉 Start building better software today with SpecPulse v2.1.0!**

```bash
pip install specpulse==2.1.0
specpulse init my-project --ai claude
```

---

<div align="center">

**Made with ❤️ for developers who value specifications**

[⬆ Back to Top](#specpulse-v210)

</div>
