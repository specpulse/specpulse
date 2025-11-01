# SpecPulse v2.4.2

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

# CLI creates empty template
specpulse spec create "OAuth2 authentication with JWT tokens"

# AI ESSENTIAL: Expand specification with details
# In Claude Code or Gemini CLI:
/sp-spec expand "OAuth2 authentication with JWT tokens"

# Generate implementation plan (CLI creates template)
specpulse plan create "Secure authentication flow"

# AI ESSENTIAL: Expand plan with detailed steps
# In Claude Code or Gemini CLI:
/sp-plan expand "Secure authentication flow"

# Break into tasks (CLI creates template)
specpulse task breakdown plan-001

# AI ESSENTIAL: Create detailed task breakdown
# In Claude Code or Gemini CLI:
/sp-task expand plan-001
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
✅ **AI-Enhanced** - **Essential** for creating and expanding specifications
✅ **CLI-First Architecture** - Fast, reliable commands for structure
✅ **Privacy-First** - No external API calls, completely local
✅ **Git Integration** - Automatic branch and context management

**Important**: SpecPulse CLI provides the structure, but AI assistants are essential for creating detailed specifications and implementation plans.

---

## 🤖 AI Integration

### Supported AI Platforms

- **Claude Code** - Custom slash commands (`/sp-*`)
- **Gemini CLI** - Custom commands (`/sp-*`)

### How It Works

**Critical CLI-AI Balance**:

```
User Request: /sp-spec "OAuth2 login with JWT"
    ↓
Step 1: TRY CLI FIRST (Never fail)
    Bash: specpulse spec create "OAuth2 login with JWT"
    ↓
Step 2: CLI creates structure and files
    ✓ Empty spec file created
    ✓ Metadata added
    ✓ Directory structure ready
    ↓
Step 3: AI expands content (Safe file operations)
    Claude reads created file, adds detailed content
    ↓
Step 4: Result: Complete specification
```

**Critical Balance Rules:**
1. **CLI First** - Always try CLI commands first
2. **No CLI Errors** - CLI commands must never fail with valid input
3. **Safe File Operations** - AI only works on files CLI creates
4. **Cross-Platform** - Works on Windows, macOS, Linux without issues
5. **Unicode Safe** - No encoding problems on any platform

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
specpulse spec create "<description>"  # Create empty template (AI needed for content)
specpulse spec validate [id]           # Validate spec(s)
specpulse spec list                    # List all specs
```

**Note**: `specpulse spec create` creates empty templates. Use AI commands (`/sp-spec`) to fill with detailed content.

### Planning & Tasks

```bash
specpulse plan create "<description>"  # Create empty plan template (AI needed for details)
specpulse task breakdown <plan-id>     # Create empty task breakdown (AI needed for details)
specpulse task list                    # List all tasks
```

**Note**: CLI creates templates, but AI is essential for detailed planning and task breakdown.

---

## 🤖 AI Commands (Slash Commands)

### Feature Commands

```bash
/sp-pulse <feature-name>             # Initialize feature
/sp-continue <feature-id>            # Switch to existing feature
/sp-status                          # Track progress across features
```

### Specification Commands (ESSENTIAL)

```bash
/sp-spec create "<description>"      # Create and expand detailed specification
/sp-spec validate <spec-id>         # Validate specification
/sp-spec expand <spec-id>           # Expand existing specification with more details
```

### Planning Commands (ESSENTIAL)

```bash
/sp-plan generate                    # Generate detailed implementation plan
/sp-plan validate <plan-id>         # Validate plan
/sp-plan expand <plan-id>           # Expand plan with more implementation details
```

### Task Commands (ESSENTIAL)

```bash
/sp-task breakdown                   # Break plan into detailed tasks
/sp-task expand <plan-id>           # Expand tasks with implementation details
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

## 🤖 Custom Commands Architecture

### How Custom Commands Work

All `/sp-*` commands follow the same **CLI-First Pattern**:

```
User: /sp-spec "Create user authentication"
    ↓
Step 1: Try CLI Command (Never fails)
    Bash: specpulse spec create "Create user authentication"
    ✓ Creates empty spec file
    ✓ Adds metadata
    ✓ Updates project structure
    ↓
Step 2: AI Expands Content (Safe operations)
    Claude reads the created file
    Claude expands with detailed requirements
    Claude saves the enhanced content
    ↓
Result: Complete, detailed specification
```

### Critical Design Principles

#### ✅ **CLI First, Always**
- Custom commands ALWAYS try CLI commands first
- CLI commands are guaranteed to work on all platforms
- CLI handles cross-platform path and encoding issues
- CLI creates the foundation that AI builds upon

#### ✅ **Safe File Operations**
- AI only works on files that CLI has already created
- AI uses proper encoding and path handling
- AI never creates files in protected directories
- AI respects file permissions and ownership

#### ✅ **Platform Independence**
- Same behavior on Windows, macOS, Linux
- Unicode and emoji support on all platforms
- Automatic path separator handling
- Consistent error handling and recovery

#### ✅ **Error Resilience**
- CLI commands validate input and provide helpful errors
- AI gracefully handles file operation failures
- Built-in recovery mechanisms
- Clear error messages and suggestions

### Custom Command Examples

#### **Specification Creation**
```bash
# User: /sp-spec "OAuth2 authentication with JWT"

# Command execution:
# Step 1: CLI (Always succeeds)
specpulse spec create "OAuth2 authentication with JWT"
# → Creates: .specpulse/specs/001-feature/spec-001.md

# Step 2: AI (Safe content expansion)
# Claude reads the created file
# Claude adds detailed requirements, security considerations, API design
# Claude saves the enhanced specification
```

#### **Task Breakdown**
```bash
# User: /sp-task breakdown plan-001

# Command execution:
# Step 1: CLI (Always succeeds)
specpulse task breakdown plan-001
# → Creates: .specpulse/tasks/001-feature/task-001.md, task-002.md, etc.

# Step 2: AI (Safe content expansion)
# Claude reads task files
# Claude adds implementation details, dependencies, time estimates
# Claude enhances task descriptions with technical specifics
```

#### **Continuous Execution**
```bash
# User: /sp-execute

# Command execution:
# Step 1: CLI (Status check)
specpulse --no-color doctor
# → Gets current project status and pending tasks

# Step 2: AI (Safe task execution)
# Claude reads next task file
# Claude implements the task requirements
# Claude marks task as completed and moves to next
```

### Cross-Platform Handling

#### **Windows (CMD/PowerShell)**
```bash
# Works with Unicode and emojis
/sp-spec "User authentication 🔐 with JWT tokens"

# Automatic path handling
# CLI: Creates C:\project\.specpulse\specs\001-feature\spec-001.md
# AI: Reads and writes with UTF-8 encoding
```

#### **macOS (zsh/bash)**
```bash
# Works with native macOS paths
/sp-spec "iOS notification system 📱"

# Automatic path handling
# CLI: Creates /Users/user/project/.specpulse/specs/001-feature/spec-001.md
# AI: Reads and writes with proper macOS encoding
```

#### **Linux (bash/zsh)**
```bash
# Works with Linux file permissions
/sp-spec "Docker container orchestration 🐳"

# Automatic path handling
# CLI: Creates /home/user/project/.specpulse/specs/001-feature/spec-001.md
# AI: Reads and writes with proper Linux permissions
```

### Benefits of This Architecture

- ✅ **Reliability**: CLI commands are tested and stable
- ✅ **Consistency**: Same behavior across all platforms
- ✅ **Safety**: AI only operates on CLI-created foundation
- ✅ **Recovery**: Clear error handling and fallback mechanisms
- ✅ **Flexibility**: AI can enhance without breaking core functionality

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

## 🤖 CLI vs AI: Essential Partnership

### What CLI Does (Structure)
- ✅ Creates directory structure
- ✅ Generates empty templates
- ✅ Manages metadata and IDs
- ✅ Validates syntax and structure
- ✅ Handles file operations
- ✅ Provides health checks

### What AI Does (Content)
- ✅ **Fills templates with detailed content**
- ✅ **Creates comprehensive specifications**
- ✅ **Generates implementation plans**
- ✅ **Breaks down complex tasks**
- ✅ **Provides technical insights**
- ✅ **Executes implementation tasks**

### They Work Together (Critical Balance)

```
CLI: Creates structure (NEVER FAILS)
AI:  Expands with detailed content
CLI: Validates and organizes
AI:  Suggests improvements
CLI: Manages cross-platform paths
AI:  Executes implementation
```

**Critical Balance**: CLI creates safe, cross-platform foundation. AI adds value without breaking the system.

**Platform Guarantee**: Works identically on Windows, macOS, Linux with proper Unicode handling.

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
- **Platform:** Windows, macOS, Linux (full cross-platform support)

## 🌍 Cross-Platform Guarantees

SpecPulse works identically on all platforms:

### ✅ Windows Support
- **Unicode Safe**: No encoding issues with emojis and special characters
- **Path Handling**: Automatic path separator conversion (`\` ↔ `/`)
- **PowerShell + CMD**: Works with both Windows shells
- **Long Paths**: Handles Windows path length limitations

### ✅ macOS Support
- **Native Compatibility**: Works with macOS file system and shell
- **Homebrew Integration**: Easy installation and updates
- **Xcode Tools**: All development dependencies supported

### ✅ Linux Support
- **All Distributions**: Ubuntu, CentOS, Fedora, Arch, etc.
- **Package Managers**: Works with apt, yum, dnf, pacman
- **File Permissions**: Proper handling of Linux file permissions

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
# Install SpecPulse (cross-platform)
pip install specpulse

# Create your first project
specpulse init my-project --ai claude
cd my-project

# Start developing with AI assistance
specpulse feature init my-feature

# CLI creates structure, AI fills content
specpulse spec create "My first feature"
# Then in Claude Code: /sp-spec expand "My first feature"

# Or use AI commands directly
# In Claude Code or Gemini CLI:
# /sp-pulse my-new-feature
# /sp-spec create "Detailed feature description"
# /sp-plan generate
# /sp-execute all

# Validate and enjoy
specpulse doctor
```

**Guaranteed to work on**: Windows, macOS, Linux with full Unicode support! 🌍

---

<div align="center">

**Made with ❤️ for developers who value specifications and quality**

**SpecPulse v2.4.2** - CLI-First • AI-Enhanced • Cross-Platform • Reliable

[⭐ Star us on GitHub](https://github.com/specpulse/specpulse) | [📦 Install from PyPI](https://pypi.org/project/specpulse/)

</div>