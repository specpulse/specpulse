# SpecPulse v2.1.2

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

### 🚀 v2.1.2 Highlights

- ✅ **CLI-First Architecture**: LLM MUST use `specpulse` CLI before file operations
- ✅ **Protected Directories**: Templates, configs, and package code cannot be modified by LLM
- ✅ **Enhanced Logging**: File-based logging with rotation (10MB, 5 backups)
- ✅ **Config Validation**: Automatic validation for `.specpulse/config.yaml`
- ✅ **Faster Performance**: Template caching with @lru_cache (2-3x faster)
- ✅ **Better Testing**: Organized into unit/integration/performance folders
- ✅ **Cross-Platform Unicode**: Emoji auto-detection for Windows/macOS/Linux

---

## 📦 Installation

```bash
# Install from PyPI
pip install specpulse

# Or install specific version
pip install specpulse==2.1.2

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

- **CLI-First Architecture**: LLM uses CLI commands before file operations (v2.1.2+)
- **Feature Management**: Initialize and switch between features
- **Specification Management**: Create, validate, and version specifications
- **Plan Generation**: AI-assisted implementation planning
- **Task Breakdown**: Convert plans into actionable tasks
- **Execution Tracking**: Track task progress and completion
- **Logging System**: File-based logs with rotation (v2.1.2+)
- **Config Validation**: Automatic .specpulse/config.yaml validation (v2.1.2+)
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

**Two Ways to Use SpecPulse (v2.1.2+):**

1. **Inside AI Assistant (Primary)** - LLM uses CLI commands first, then file operations
2. **Terminal (Optional)** - Direct CLI commands for manual use

**🔴 CRITICAL: LLM Workflow Hierarchy (v2.1.2+)**

LLM must follow this order:
1. ✅ **FIRST**: Try `specpulse` CLI command (if exists)
2. ✅ **SECOND**: Use File Operations (Read/Write/Edit) if CLI doesn't exist
3. ❌ **NEVER**: Edit templates/, .specpulse/, specpulse/, .claude/, .gemini/

### Feature Management

```bash
# Terminal use
specpulse feature init <name>           # Initialize new feature
specpulse feature continue <name>       # Switch to existing feature

# Inside Claude/Gemini (v2.1.2+ workflow)
/sp-pulse user-authentication
# Step 1 (LLM MUST try first):
#   Bash: specpulse feature init user-authentication
# Step 2 (if CLI doesn't exist):
#   Use mkdir, Write, Edit tools to create structure
```

### Specification Management

```bash
# Terminal use
specpulse spec create <description>     # Create specification
specpulse spec update <id> <desc>       # Update specification
specpulse spec validate                 # Validate specifications
specpulse spec progress <feature-id>    # Show completion progress

# Inside Claude/Gemini (v2.1.2+ workflow)
/sp-spec OAuth2 login with JWT
# Step 1 (LLM MUST try first):
#   Bash: specpulse spec create "OAuth2 login with JWT"
# Step 2 (if CLI doesn't exist):
#   Read: templates/spec.md
#   Write: specs/001-feature/spec-001.md
#   Edit: specs/001-feature/spec-001.md (expand)
```

### Plan Management

```bash
# Terminal use
specpulse plan create <description>     # Create implementation plan
specpulse plan update <id> <desc>       # Update plan

# Inside Claude/Gemini (v2.1.2+ workflow)
/sp-plan generate
# Step 1 (LLM MUST try first):
#   Bash: specpulse plan create "Implementation plan"
# Step 2 (if CLI doesn't exist):
#   Read: templates/plan.md
#   Write: plans/001-feature/plan-001.md
```

### Task Management

```bash
# Terminal use
specpulse task create <description>     # Create task
specpulse task breakdown <plan-id>      # Generate tasks from plan
specpulse task update <id> <desc>       # Update task

# Inside Claude/Gemini (v2.1.2+ workflow)
/sp-task breakdown
# Step 1 (LLM MUST try first):
#   Bash: specpulse task breakdown 001
# Step 2 (if CLI doesn't exist):
#   Read: templates/task.md
#   Write: tasks/001-feature/tasks-001.md
```

### Execution Tracking

```bash
# Terminal use
specpulse execute start <task-id>       # Mark task as started
specpulse execute done <task-id>        # Mark task as completed

# Inside Claude/Gemini (v2.1.2+ workflow)
/sp-execute
# LLM reads tasks, executes them, updates status via Edit tool
# No CLI for execute yet - uses File Operations
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

## 🤖 AI Integration (v2.1.2 CLI-First Architecture)

SpecPulse works seamlessly with AI assistants while maintaining **privacy-first design** (no external API calls).

### How It Works (v2.1.2+)

```
User in Claude Code / Gemini CLI
    ↓
Custom Slash Commands (/sp-pulse, /sp-spec, etc.)
    ↓
LLM FOLLOWS WORKFLOW HIERARCHY:
    ↓
Step 1: Try CLI First (PRIMARY)
    Bash: specpulse spec create "description"
    ↓
    If successful → DONE ✅
    If not exists → Continue to Step 2
    ↓
Step 2: File Operations (FALLBACK)
    1. Read template (templates/spec.md)
    2. Write file (specs/001-feature/spec-001.md)
    3. Read created file
    4. Expand with AI intelligence
    5. Edit file with expanded content
    ↓
Complete Specifications, Plans, Tasks
```

**🔴 CRITICAL (v2.1.2+)**: CLI commands are **PRIMARY**, not optional. LLM MUST try CLI first. File operations are **FALLBACK** when CLI doesn't exist or doesn't cover the operation.

**Why CLI-First?**
- ✅ Metadata handled automatically (IDs, timestamps, status)
- ✅ Validation before file creation
- ✅ Context updates consistent
- ✅ Error handling built-in
- ✅ Protects templates and configs from accidental edits

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

**Note**: No `scripts/` folder! v2.1.0+ uses pure Python CLI.

**v2.1.2 Additions**:
- `.specpulse/logs/` - Application logs with rotation
- Enhanced config validation
- CLI-first workflow enforcement

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

## 🔄 Migration to v2.1.2

### From v2.1.0 or v2.1.1

```bash
# 1. Upgrade SpecPulse
pip install --upgrade specpulse

# 2. That's it! No breaking changes
```

**What's New in v2.1.2:**
- ✅ CLI-first workflow (LLM uses CLI before file operations)
- ✅ Logging infrastructure (automatic)
- ✅ Config validation (automatic)
- ✅ Template caching (automatic performance boost)
- ✅ Better test organization (transparent to users)
- ✅ Enhanced error messages

**No Breaking Changes** - Direct upgrade compatible

### From v2.0.0

```bash
# 1. Upgrade SpecPulse
pip install --upgrade specpulse

# 2. Delete old scripts (safe to remove)
rm -rf scripts/

# 3. That's it! v2.1.2 is fully compatible
```

**Major Changes:**
- ⚠️ Scripts removed in v2.1.0 (replaced with CLI)
- ✅ CLI-first workflow in v2.1.2 (enhanced automation)
- ✅ All slash commands work identically
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
- Everyone who helped shape v2.1.0's architecture and v2.1.2's CLI-first workflow

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

**🎉 Start building better software today with SpecPulse v2.1.2!**

```bash
pip install specpulse
specpulse init my-project --ai claude
```

---

<div align="center">

**Made with ❤️ for developers who value specifications**

[⬆ Back to Top](#specpulse-v212)

</div>
