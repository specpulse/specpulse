# SpecPulse v2.4.1

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/specpulse.svg)](https://pypi.org/project/specpulse/) [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-Enhanced Specification-Driven Development Framework**

*Build better software with specifications first, enhanced by AI*

</div>

---

## 🚀 Quick Start

### Install

```bash
pip install specpulse
```

### Initialize Project

```bash
# New project
specpulse init my-project --ai claude
cd my-project

# Or add to existing project
cd existing-project
specpulse init --here --ai claude
```

### Start Your First Feature

```bash
# Initialize feature
specpulse feature init user-authentication

# Create specification
specpulse spec create "OAuth2 authentication with JWT tokens"

# Generate implementation plan
specpulse plan create "Secure authentication flow"

# Break into tasks
specpulse task breakdown plan-001
```

### Use AI Commands

In Claude Code or Gemini CLI:

```bash
/sp-pulse payment-system          # Initialize feature
/sp-spec create "Payment processing"  # Create specification
/sp-plan generate                   # Generate implementation plan
/sp-task breakdown                  # Break into tasks
/sp-status                          # Check progress
```

---

## 📋 What It Does

SpecPulse helps you build software systematically:

✅ **Specification First** - Clear specs before coding
✅ **AI-Enhanced** - Works with Claude Code and Gemini CLI
✅ **CLI-First Architecture** - Fast, reliable commands
✅ **Privacy-First** - No external API calls, completely local
✅ **Git Integration** - Automatic branch and context management

---

## 🤖 AI Integration

### Supported AI Platforms

- **Claude Code** - Custom slash commands (`/sp-*`)
- **Gemini CLI** - Custom commands (`/sp-*`)

### How It Works

**CLI-First Pattern** (v2.1.2+):

```
User Request: /sp-spec OAuth2 login
    ↓
Step 1: Try CLI first
    Bash: specpulse spec create "OAuth2 login"
    ↓
Step 2: If CLI doesn't exist, use File Operations
    Claude reads template, writes file, expands content
```

---

## 📁 Project Structure

After initialization:

```
my-project/
├── .specpulse/          # All project data
│   ├── specs/           # Feature specifications
│   ├── plans/           # Implementation plans
│   ├── tasks/           # Development tasks
│   ├── memory/          # Project context and decisions
│   └── templates/       # Specification templates
├── .claude/             # Claude Code commands
└── .gemini/             # Gemini CLI commands
```

---

## 💻 Core Commands

### Project Management

```bash
specpulse init <project-name>          # Initialize new project
specpulse init --here --ai claude      # Add to existing project
specpulse doctor                       # Health check
specpulse validate all                 # Validate all components
```

### Feature Development

```bash
specpulse feature init <name>          # Start new feature
specpulse feature continue <id>        # Switch to existing feature
specpulse feature list                 # List all features
```

### Specifications

```bash
specpulse spec create "<description>"  # Create specification
specpulse spec validate [id]           # Validate spec(s)
specpulse spec list                    # List all specs
```

### Planning & Tasks

```bash
specpulse plan create "<description>"  # Create implementation plan
specpulse task breakdown <plan-id>     # Break into tasks
specpulse task list                    # List all tasks
```

---

## 🤖 AI Commands (Slash Commands)

### Feature Commands

```bash
/sp-pulse <feature-name>             # Initialize feature
/sp-continue <feature-id>            # Switch to existing feature
/sp-status                          # Track progress across features
```

### Specification Commands

```bash
/sp-spec create "<description>"      # Create specification
/sp-spec validate <spec-id>         # Validate specification
```

### Planning Commands

```bash
/sp-plan generate                    # Generate implementation plan
/sp-plan validate <plan-id>         # Validate plan
```

### Task Commands

```bash
/sp-task breakdown                   # Break plan into tasks
/sp-task status <task-id>           # Check task status
```

### Advanced Commands

```bash
/sp-execute                         # Execute next pending task and continue
/sp-execute next                    # Same as above
/sp-execute all                     # Execute ALL pending tasks non-stop
/sp-execute T001                    # Execute specific task
/sp-execute AUTH-T001               # Execute specific service task
/sp-decompose <spec-id>             # Decompose spec into components
/sp-clarify <spec-id>               # Clarify specification
```

---

## 🔄 Task Execution with /sp-execute

### What is /sp-execute?

`/sp-execute` is a **continuous execution mode** that executes tasks without stopping between them. It implements tasks sequentially and automatically moves to the next task until all are completed or blocked.

### How /sp-execute Works

**Non-Stop Execution Pattern:**

```
/sp-execute
    ↓
Step 1: Find next pending task (T001 or AUTH-T001)
    ↓
Step 2: Mark as in-progress: [ ] → [>]
    ↓
Step 3: Implement the task
    ↓
Step 4: Mark as completed: [>] → [x]
    ↓
Step 5: Automatically continue to next task
    ↓
Repeat until all tasks complete
```

### /sp-execute Usage

In Claude Code or Gemini CLI:

```bash
# Execute next pending task and continue
/sp-execute

# Execute ALL pending tasks non-stop
/sp-execute all

# Execute specific task and continue with related tasks
/sp-execute T001
/sp-execute AUTH-T001
```

### Task Status Markers

- `[ ]` - Pending task (ready to execute)
- `[>]` - In progress (currently working on)
- `[x]` - Completed (done)
- `[!]` - Blocked (waiting for dependency)

### Continuous Execution Example

```bash
# User: /sp-execute

# AI response:
Found 15 pending tasks
Starting with T001: Implementing user model...
✓ User model created
Moving to T002: Creating authentication service...
✓ Authentication service implemented
Continue with T003, T004, T005... WITHOUT STOPPING
All 15 tasks completed successfully!
```

### Batch Execution

```bash
# User: /sp-execute all

# AI response:
Processing ALL pending tasks in one go
No interruptions or pauses
Complete the entire task list
Final report only
```

### Non-Stop Execution Rules

**CRITICAL**: `/sp-execute` follows strict non-stop execution rules:

1. **NO EXPLANATIONS** between tasks - just execute
2. **NO WAITING** for confirmation - keep going
3. **NO SUMMARIES** after each task - save for the end
4. **ONLY STOP** when:
   - All tasks completed
   - Hit a blocker
   - Critical error occurs
   - User explicitly says "stop"

### Workflow Integration

#### Starting Fresh

```bash
/sp-pulse new-feature
/sp-spec "Create user authentication with OAuth2"
/sp-plan
/sp-task
/sp-execute all    # Complete everything!
```

#### Resuming Work

```bash
/sp-continue 001-user-auth
/sp-execute        # Continue from where we left off
```

### Error Handling

If an error occurs during task execution:
1. Mark task as blocked: `[!]`
2. Note the error in task file
3. Skip to next available task
4. Continue execution
5. Report all blockers at the end

### Progress Tracking

During execution, AI maintains:
- Task completion counter
- Progress percentage
- List of completed tasks
- List of any blockers encountered

### Final Report Example

```
## Execution Complete

**Progress**: 100% (25/25 tasks)
**Duration**: Continuous execution
**Status**: All tasks completed

### Summary
✓ 25 tasks completed
✗ 0 tasks blocked
→ 0 tasks remaining

Ready for validation: /sp-validate
```

### Benefits of /sp-execute

- **Maximum efficiency** - No time wasted between tasks
- **Flow state** - Continuous productive work
- **Rapid delivery** - Complete features faster
- **Reduced context switching** - Stay focused on implementation
- **Automated workflow** - Let AI handle the execution

**Perfect for**: Completing entire feature sets, maintaining momentum, and rapid prototyping.

---

## 🔄 Complete Workflow Example

```bash
# 1. Initialize project
specpulse init my-app --ai claude
cd my-app

# 2. Start feature
specpulse feature init user-auth

# 3. Create specification (CLI)
specpulse spec create "OAuth2 login with JWT"

# 4. Or use AI commands
# In Claude Code:
# /sp-spec create "OAuth2 login with JWT"

# 5. Generate plan
specpulse plan create "OAuth2 implementation"

# 6. Break into tasks
specpulse task breakdown plan-001

# 7. Validate everything
specpulse validate all
specpulse doctor
```

---

## 🔧 Requirements

- **Python:** 3.11 or higher
- **Git:** Recommended for branch-based features
- **Platform:** Windows, macOS, Linux

---

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation
- **[AI Integration Guide](docs/AI_INTEGRATION.md)** - AI assistant setup
- **[Migration Guide](docs/MIGRATION.md)** - Upgrading from previous versions
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues

### Getting Help

```bash
specpulse --help                      # General help
specpulse feature --help              # Feature commands help
specpulse spec --help                 # Specification commands help
specpulse doctor                      # Project health check
```

---

## 🆕 What's New in v2.4.1

### CLI-First Architecture
- AI assistants try CLI commands before file operations
- Deprecated `specpulse ai *` commands
- Better performance and reliability

### Enhanced Features
- Improved validation system with auto-fix
- Better error handling and recovery
- Optimized performance and memory usage

---

## 🚀 Get Started Now

```bash
# Install SpecPulse
pip install specpulse

# Create your first project
specpulse init my-project --ai claude
cd my-project

# Start developing
specpulse feature init my-feature
specpulse spec create "My first feature"

# Validate and enjoy
specpulse doctor
```

---

<div align="center">

**Made with ❤️ for developers who value specifications and quality**

**SpecPulse v2.4.1** - CLI-First • AI-Enhanced • Privacy-First • Fast

[⭐ Star us on GitHub](https://github.com/specpulse/specpulse) | [📦 Install from PyPI](https://pypi.org/project/specpulse/)

</div>