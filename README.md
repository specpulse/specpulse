# SpecPulse v2.1.3

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

### 🚀 v2.1.3 Highlights

- ✨ **27 New sp-* Commands**: Complete CLI refactoring with dedicated command modules
- ✅ **sp-pulse**: Feature initialization and management (5 commands)
- ✅ **sp-spec**: Specification management (7 commands)
- ✅ **sp-plan**: Implementation plan management (7 commands)
- ✅ **sp-task**: Task management and execution (8 commands)
- ✅ **Context-Aware**: Auto-detect current feature from context.md or git branch
- ✅ **Metadata Tracking**: Automatic HTML comment-based tracking
- ✅ **Progress Visualization**: Built-in progress calculation
- ⚠️ **Breaking**: Removed `sp` alias (use full `specpulse` command)

---

## 📦 Installation

```bash
# Install from PyPI
pip install specpulse

# Or install specific version
pip install specpulse==2.1.3

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

### 2. Start a Feature (NEW in v2.1.3)

```bash
# Initialize feature structure
specpulse sp-pulse init user-authentication

# This creates:
# - specs/001-user-authentication/
# - plans/001-user-authentication/
# - tasks/001-user-authentication/
# - Git branch: 001-user-authentication
# - Updates memory/context.md
```

### 3. Create Specification (NEW in v2.1.3)

```bash
# Create spec template (LLM will expand this)
specpulse sp-spec create "OAuth2 login with JWT tokens"

# Creates: specs/001-user-authentication/spec-001.md
# With template, metadata, and LLM expansion markers
# LLM then reads and expands with actual requirements
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

### Feature Management (v2.1.3)

```bash
# NEW: sp-pulse commands (5 total)
specpulse sp-pulse init <name>          # Initialize new feature
specpulse sp-pulse continue <name>      # Switch to existing feature
specpulse sp-pulse list                 # List all features
specpulse sp-pulse status               # Show current feature status
specpulse sp-pulse delete <name>        # Delete feature (with confirmation)

# Inside Claude/Gemini (v2.1.3+ workflow)
/sp-pulse user-authentication
# Runs: specpulse sp-pulse init user-authentication
# Creates structure, branch, updates context
```

### Specification Management (v2.1.3)

```bash
# NEW: sp-spec commands (7 total)
specpulse sp-spec create "<desc>"       # Create specification template
specpulse sp-spec update <id> "<changes>" # Update specification
specpulse sp-spec validate [id]         # Validate spec(s)
specpulse sp-spec clarify <id>          # Show clarification markers
specpulse sp-spec list                  # List all specifications
specpulse sp-spec show <id>             # Display spec content
specpulse sp-spec progress <id>         # Show completion progress

# Inside Claude/Gemini (v2.1.3+ workflow)
/sp-spec OAuth2 login with JWT
# Step 1: Runs CLI to create template
#   specpulse sp-spec create "OAuth2 login with JWT"
# Step 2: LLM expands template with actual content
#   Read: specs/001-feature/spec-001.md
#   Edit: Add requirements, user stories, etc.
```

### Plan Management (v2.1.3)

```bash
# NEW: sp-plan commands (7 total)
specpulse sp-plan create "<desc>"       # Create plan template
specpulse sp-plan update <id> "<changes>" # Update plan
specpulse sp-plan validate [id]         # Validate plan(s)
specpulse sp-plan list                  # List all plans
specpulse sp-plan show <id>             # Display plan content
specpulse sp-plan progress <id>         # Show completion progress
specpulse sp-plan phases <id>           # Show implementation phases

# Inside Claude/Gemini (v2.1.3+ workflow)
/sp-plan generate
# Step 1: Runs CLI to create template
#   specpulse sp-plan create "Implementation plan"
# Step 2: LLM expands with architecture, tech stack, phases
```

### Task Management (v2.1.3)

```bash
# NEW: sp-task commands (8 total)
specpulse sp-task breakdown <plan-id>   # Create task template from plan
specpulse sp-task create "<desc>"       # Create manual task
specpulse sp-task update <id> "<changes>" # Update task
specpulse sp-task start <id>            # Mark task as started
specpulse sp-task done <id>             # Mark task as completed
specpulse sp-task list                  # List all tasks
specpulse sp-task show <id>             # Display task content
specpulse sp-task progress              # Show overall progress

# Inside Claude/Gemini (v2.1.3+ workflow)
/sp-task breakdown
# Step 1: Runs CLI to create template
#   specpulse sp-task breakdown 001
# Step 2: LLM breaks down plan into detailed tasks
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

## 📋 Complete Workflow Example (v2.1.3)

```bash
# 1. Initialize project
specpulse init my-app --ai claude

# 2. Start feature (NEW sp-pulse)
specpulse sp-pulse init user-authentication

# 3. Create specification template (NEW sp-spec)
specpulse sp-spec create "OAuth2 login with JWT tokens and 2FA"

# 4. LLM expands spec (in Claude Code)
#    - Reads spec-001.md
#    - Adds requirements, user stories, acceptance criteria
#    - Edits spec-001.md with full content

# 5. Validate specification
specpulse sp-spec validate 001

# 6. Generate plan template (NEW sp-plan)
specpulse sp-plan create "Implementation roadmap for OAuth2"

# 7. LLM expands plan (in Claude Code)
#    - Reads plan-001.md
#    - Adds architecture, tech stack, phases
#    - Edits plan-001.md with full plan

# 8. Break down to tasks template (NEW sp-task)
specpulse sp-task breakdown 001

# 9. LLM creates task details (in Claude Code)
#    - Reads tasks-001.md
#    - Breaks down each phase into actionable tasks
#    - Edits tasks-001.md with task list

# 10. Execute tasks (NEW sp-task)
specpulse sp-task start 001
# [Implement task]
specpulse sp-task done 001
specpulse sp-task progress
# Shows: 33% complete

# 11. Repeat for all tasks
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

**v2.1.3 Additions**:
- `.specpulse/logs/` - Application logs with rotation
- Enhanced config validation
- 27 new sp-* CLI commands
- Metadata tracking in all files
- Context-aware operations

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

## 🔄 Migration to v2.1.3

### From v2.1.2

```bash
# 1. Upgrade SpecPulse
pip install --upgrade specpulse

# 2. Update any scripts using 'sp' alias
# Change 'sp' to 'specpulse'

# 3. That's it!
```

**What's New in v2.1.3:**
- ✨ 27 new sp-* commands (sp-pulse, sp-spec, sp-plan, sp-task)
- ✅ Context-aware operations (auto-detect feature)
- ✅ Metadata tracking (HTML comments)
- ✅ Progress visualization
- ✅ Feature switching
- ⚠️ Breaking: Removed `sp` alias

**Deprecated Commands:**
- `specpulse feature init` → use `specpulse sp-pulse init`
- `specpulse spec create` → use `specpulse sp-spec create`

See [MIGRATION_v2.1.3.md](MIGRATION_v2.1.3.md) for details.

### From v2.1.0 or v2.1.1

```bash
# 1. Upgrade SpecPulse
pip install --upgrade specpulse

# 2. Same as above - update 'sp' alias
```

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

**🎉 Start building better software today with SpecPulse v2.1.3!**

```bash
pip install specpulse
specpulse init my-project --ai claude
specpulse sp-pulse init my-feature
```

---

<div align="center">

**Made with ❤️ for developers who value specifications**

[⬆ Back to Top](#specpulse-v213)

</div>
