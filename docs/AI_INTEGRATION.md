# SpecPulse v2.7.1 AI Integration Guide

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [AI Commands](#ai-commands)
- [Smart Context Detection](#smart-context-detection)
- [AI-Powered Suggestions](#ai-powered-suggestions)
- [Multi-LLM Support](#multi-llm-support)
- [AI Workflow Checkpoints](#ai-workflow-checkpoints)
- [Privacy-First Design](#privacy-first-design)
- [Multi-Platform AI Integration](#multi-platform-ai-integration)
- [Integration with AI Assistants](#integration-with-ai-assistants)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## 🎯 Overview

SpecPulse v2.7.1 introduces comprehensive multi-platform AI integration that enhances your specification-driven development workflow while maintaining complete privacy and control. Unlike traditional AI tools that require external API calls, SpecPulse's AI integration works entirely offline, processing all logic locally on your machine.

### Key Principles

1. **Privacy-First**: No data leaves your system
2. **Local Processing**: All AI logic runs locally
3. **Context-Aware**: Understands your project structure
4. **Multi-Platform Support**: Works with 8 AI platforms (Claude, Gemini, GPT, Windsurf, Cursor, GitHub, OpenCode, Crush, Qwen)
5. **Selective Initialization**: Only create directories for selected AI platforms
6. **Intelligent Suggestions**: Provides context-aware recommendations
7. **Consistent Command Structure**: Uniform slash commands across all platforms

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐
│  AI Assistant   │  (Claude/Gemini)
└─────────┬───────┘
          │
    ┌───▼───┐
    │ SpecPulse │  (Local CLI Tool)
    └─┬─────┘
      │
      ▼
┌─────────────────────────────────────────┐
│        AI Integration System              │
│  • Context Detection                    │
│  • Smart Suggestions                    │
│  • Workflow Tracking                   │
│  • Multi-LLM Management               │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│        File System                      │
│  • Specifications                      │
│  • Plans                              │
│  • Tasks                              │
│  • Memory                            │
│  • Templates                        │
└─────────────────────────────────────────┘
```

### Data Flow

1. **Context Detection**: AI Integration analyzes git branches, memory files, and recent activity
2. **Smart Processing**: Local AI logic processes context without external calls
3. **User Interface**: CLI commands provide access to AI features
4. **File Operations**: All file operations remain local and private

### Security Model

- ✅ **No External API Calls**: Never connects to external AI services
- ✅ **Local Processing**: All AI logic runs on your machine
- ✅ **Data Privacy**: No data leaves your system
- ✅ **Corporate Compliant**: Meets enterprise security requirements

---

## 🤖 AI Integration in v2.7.1

### CLI-First Architecture (v2.7.1+)

**Critical Design Change**: SpecPulse v2.7.1 follows a CLI-first architecture where AI assistants should ALWAYS try CLI commands before using file operations.

#### **Primary Workflow Hierarchy**

1. **FIRST: Start with AI Command** (recommended)
   ```bash
   /sp-pulse <feature-name>        # Start new feature
   /sp-spec "<description>"         # Create specification
   /sp-plan                       # Generate implementation plan
   /sp-task                       # Break down into tasks
   /sp-validate                   # Validate work
   ```

2. **SECOND: File Operations** (if CLI doesn't exist or doesn't cover operation)
   - READ templates from `.specpulse/templates/`
   - WRITE/EDIT files in `.specpulse/specs/`, `.specpulse/plans/`, `.specpulse/tasks/`, `.specpulse/memory/`

3. **NEVER: Direct edits to protected directories**
   - ❌ `.specpulse/templates/` - Read-only template source
   - ❌ `.specpulse/` - Internal configuration
   - ❌ `specpulse/` - Package code
   - ❌ `.claude/` and `.gemini/` - AI command definitions

### AI Assistant Integration

#### **Claude Code Integration**

Initialize project with Claude support:
```bash
specpulse init my-project --ai claude
```

Use custom slash commands:
```bash
# Start new feature
/sp-pulse user-authentication

# Create specification
/sp-spec create "user authentication with OAuth2"

# Generate implementation plan
/sp-plan generate

# Create task breakdown
/sp-task breakdown

# Validate work
/sp-spec validate
```

#### **Gemini CLI Integration**

Initialize project with Gemini support:
```bash
specpulse init my-project --ai gemini
```

Use custom commands:
```bash
# Start new feature
/sp-pulse user-authentication

# Create specification
/sp-spec create "user authentication with OAuth2"

# Generate implementation plan
/sp-plan generate

# Create task breakdown
/sp-task breakdown

# Validate work
/sp-spec validate
```

---

## 🧠 Context Detection & Memory Management

### Git Integration

SpecPulse leverages git for context detection:

```bash
# Feature branch naming automatically detected
001-user-authentication      → Feature: 001-user-authentication
002-api-redesign             → Feature: 002-api-redesign
003-mobile-onboarding        → Feature: 003-mobile-onboarding
```

### Memory System

The memory system provides context-aware assistance:

#### Memory Files Structure
```
.specpulse/memory/
├── context.md          # Current project context
├── decisions.md        # Architectural decisions
├── patterns.md         # Reusable patterns
└── knowledge.md        # Project knowledge base
```

#### Context Management

```yaml
# .specpulse/memory/context.md
current_feature: "003-user-authentication"
tech_stack:
  frontend: "React"
  backend: "FastAPI"
  database: "PostgreSQL"
last_updated: "2025-11-01T12:00:00Z"
```

### AI Context Detection (v2.7.1)

While AI commands have been deprecated, context detection still works through:

1. **Git Branch Analysis**: Automatic feature detection from branch names
2. **Memory File Parsing**: Context extraction from memory files
3. **Recent Activity Tracking**: Analysis of recent file modifications
4. **Template Usage Pattern**: Understanding project workflow

**Note**: Context detection is now handled through CLI commands rather than dedicated AI commands.

---

## 💡 Workflow Guidance & Templates

### Template System (v2.7.1)

SpecPulse provides intelligent template selection and workflow guidance:

#### **Template Tiers**

```bash
# Quick prototypes and MVPs (2-3 min)
spec-tier1-minimal
- Basic problem statement
- Simple acceptance criteria
- Minimal requirements

# Standard production features (10-15 min)
spec-tier2-standard
- Comprehensive requirements
- Technical considerations
- Security aspects
- Performance requirements

# Enterprise-grade specifications (30-45 min)
spec-tier3-complete
- Full compliance requirements
- Detailed technical specifications
- Complete testing strategies
- Deployment and maintenance procedures
```

#### **CLI-Based Template Selection**

```bash
# Initialize with specific template
specpulse init my-project --template web

# Change template after initialization
specpulse template change spec-tier2-standard

# Expand template complexity
specpulse spec expand 001-feature --to-tier complete
```

### Feature Workflow

#### **Standard Development Workflow**

```bash
# 1. Initialize feature (PRIMARY ENTRY POINT)
/sp-pulse user-authentication

# 2. Create specification
/sp-spec "User authentication with OAuth2 and JWT tokens"

# 3. Generate implementation plan
/sp-plan

# 4. Break down into tasks
/sp-task

# 5. Execute tasks
/sp-execute

# 6. Track progress
/sp-status

# 7. Validate work
/sp-validate
```

#### **Context Switching**

```bash
# Switch to existing feature
/sp-continue 001-user-authentication

# Check current status
/sp-status

# Decompose specifications if needed
/sp-decompose spec-001
```

---

## 🔄 Multi-LLM Support

### Supported AI Assistants

#### Claude Code Integration

```bash
# Initialize project with Claude support
specpulse init my-project --ai claude

# Claude automatically creates custom slash commands:
/sp-pulse    # Initialize new feature
/sp-spec     # Create/update specifications
/sp-plan     # Generate implementation plans
/sp-task     # Break down into tasks
/sp-execute  # Execute tasks continuously
/sp-continue # Switch context to existing feature
/sp-status   # Track progress across features
/sp-decompose # Decompose specs into microservices
```

**Claude Strengths:**
- Advanced reasoning capabilities
- Better context understanding
- Superior code analysis
- Enhanced documentation generation

#### Gemini CLI Integration

```bash
# Initialize project with Gemini support
specpulse init my-project --ai gemini

# Gemini automatically creates custom commands:
/sp-pulse    # Initialize new feature
/sp-spec     # Create/update specifications
/sp-plan     # Generate implementation plans
/sp-task     # Break down into tasks
/sp-execute  # Execute tasks continuously
/sp-continue # Switch context to existing feature
/sp-status   # Track progress across features
/sp-decompose # Decompose specs into microservices
```

**Gemini Strengths:**
- Fast response times
- Good template filling
- Efficient batch processing
- Cost-effective operation

### Multi-LLM Mode

When using both Claude and Gemini:

```bash
# Initialize with both AI assistants
specpulse init my-project --ai both
```

**Benefits:**
1. **Context Sharing**: Both LLMs access the same project context
2. **Parallel Processing**: Can leverage strengths of both systems
3. **Cross-Validation**: Different perspectives on the same problem
4. **Enhanced Capabilities**: Combines insights from both AI systems

### Command File Locations

**Claude Code Commands:** `.claude/commands/*.md`
**Gemini CLI Commands:** `.gemini/commands/*.toml`

Both sets of commands provide identical functionality but are formatted for their respective AI assistants.

---

## 📸 Memory & Checkpoint System

### Memory System (v2.7.1)

SpecPulse provides a structured memory system for tracking project knowledge and decisions:

#### **Memory Files Structure**

```
.specpulse/memory/
├── context.md          # Current project context and state
├── decisions.md        # Architectural decisions and rationale
├── patterns.md         # Reusable code patterns and approaches
├── knowledge.md        # Project-specific knowledge base
└── checkpoints/        # Workflow checkpoints and states
```

#### **Context Management**

```yaml
# .specpulse/memory/context.md
current_feature: "001-user-authentication"
project_info:
  name: "My Project"
  type: "web"
  tech_stack:
    frontend: "React"
    backend: "FastAPI"
    database: "PostgreSQL"

workflow:
  phase: "implementation"
  last_command: "specpulse task breakdown"
  progress: 45.0

last_updated: "2025-11-01T12:00:00Z"
```

#### **Architectural Decisions**

```markdown
# .specpulse/memory/decisions.md
## Decision: OAuth2 Implementation (2025-11-01)
**Context**: User Authentication Feature
**Decision**: Use OAuth2 with JWT tokens
**Rationale**: Industry standard, secure, good library support
**Alternatives Considered**: Basic auth, Session auth
**Impact**: Enhanced security, better user experience
```

#### **Reusable Patterns**

```markdown
# .specpulse/memory/patterns.md
## Repository Pattern
**Usage**: Data access layer implementation
**Benefits**: Centralized data operations, easier testing
**Projects**: 001-user-authentication, 002-api-redesign
**Example**:
```python
class UserRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, user_data):
        # Implementation
        pass
```

### Workflow Checkpoints

While dedicated checkpoint commands have been deprecated, the memory system provides similar functionality:

#### **Manual Checkpoints via Memory**

```bash
# Create decision checkpoint
echo "## Decision: Major Architecture Change" >> .specpulse/memory/decisions.md
echo "**Date**: $(date)" >> .specpulse/memory/decisions.md
echo "**Context**: Refactoring authentication system" >> .specpulse/memory/decisions.md

# Create progress checkpoint
echo "## Progress Checkpoint" >> .specpulse/memory/context.md
echo "**Date**: $(date)" >> .specpulse/memory/context.md
echo "**Status**: Ready for testing phase" >> .specpulse/memory/context.md
```

#### **Git-Based Checkpoints**

```bash
# Create git tag for milestone
git tag -a milestone-001 -m "Feature 001 implementation complete"

# Create branch for experimental changes
git checkout -b experiment/new-approach

# Return to safe point
git checkout main
git checkout milestone-001
```

---

## 🌐 Multi-Platform AI Integration

### Supported AI Platforms (v2.7.1)

SpecPulse v2.7.1 supports 8 major AI platforms with consistent command structure:

| Platform | Directory | Command Format | File Type | Custom Commands |
|----------|-----------|---------------|-----------|-----------------|
| **Claude** | `.claude/commands/` | YAML + Markdown | `.md` | 14 commands |
| **Gemini** | `.gemini/commands/` | TOML Configuration | `.toml` | 12 commands |
| **GPT** | `.gpt/commands/` | YAML + Markdown | `.md` | 12 commands |
| **Windsurf** | `.windsurf/workflows/` | Custom Front Matter | `.md` | 12 commands |
| **Cursor** | `.cursor/commands/` | YAML + Markdown | `.md` | 8 commands |
| **GitHub** | `.github/prompts/` | Prompt Format | `.prompt.md` | 8 commands |
| **OpenCode** | `.opencode/command/` | YAML + Markdown | `.md` | 8 commands |
| **Crush** | `.crush/commands/sp/` | YAML + Markdown | `.md` | 8 commands |
| **Qwen** | `.qwen/commands/` | TOML Configuration | `.toml` | 12 commands |

### Selective AI Tool Initialization

SpecPulse v2.7.1 introduces selective AI tool initialization for cleaner projects:

```bash
# Initialize with all AI platforms
specpulse init my-project --ai all

# Initialize with specific platforms
specpulse init my-project --ai claude,gemini

# Initialize with single platform
specpulse init my-project --ai claude

# Interactive selection
specpulse init my-project --ai interactive
```

#### Directory Structure Benefits

**Before (All Platforms)**:
```
.claude/
.gemini/
.gpt/
.windsurf/
.cursor/
.github/
.opencode/
.crush/
.qwen/
```

**After (Selective)**:
```
# Only selected platforms
.claude/
.gemini/
.cursor/
```

### Unified Command Set

All platforms support these core commands:

| Command | Function | Platforms |
|---------|----------|-----------|
| `/sp-pulse` | Initialize feature - PRIMARY ENTRY POINT | All |
| `/sp-spec` | Create specification | All |
| `/sp-plan` | Generate implementation plan | All |
| `/sp-task` | Break down into tasks | All |
| `/sp-execute` | Execute tasks | All |
| `/sp-status` | Show project status | All |
| `/sp-validate` | Validate project | All |
| `/sp-continue` | Switch to existing feature | All |
| `/sp-decompose` | Decompose specifications | All |
| `/sp-clarify` | Clarify requirements | All |
| `/sp-llm-enforce` | LLM compliance enforcement | All |

**🎯 IMPORTANT: Always start with `/sp-pulse` - this is your entry point to everything!**

#### Platform-Specific Commands

**Claude Code**:
- `/sp-clarify` - Clarify requirements
- `/sp-continue` - Continue current work
- `/sp-decompose` - Decompose complex features
- `/sp-llm-enforce` - Enforce LLM compliance
- `/sp-test` - Generate tests

**Gemini CLI**:
- `/sp-clarify` - Requirements clarification (TOML)
- `/sp-continue` - Work continuation (TOML)
- `/sp-decompose` - Feature decomposition (TOML)
- `/sp-ops` - Operations commands (TOML)

**Windsurf**:
- `/sp-clarify` - Clarify with SPECPULSE blocks
- `/sp-continue` - Continue with workflow blocks
- `/sp-decompose` - Decompose with structured blocks
- `/sp-ops` - Operations with workflow integration

### Platform Configuration

Each platform has its own configuration style:

#### Claude Code (YAML Front Matter)
```yaml
---
command: sp-spec
description: Create specification
version: 1.0
---
```

#### Gemini CLI (TOML)
```toml
[command]
name = "sp-spec"
description = "Create specification"
version = "1.0"
```

#### Windsurf (Custom Front Matter)
```frontmatter
<!-- @command: sp-spec -->
<!-- @description: Create specification -->
<!-- @version: 1.0 -->
```

### Cross-Platform Compatibility

All commands work identically across platforms:

```bash
# These work the same on ALL platforms
/sp-pulse user-authentication    # PRIMARY ENTRY POINT
/sp-spec "OAuth2 authentication system"
/sp-plan "Implementation roadmap"
/sp-task breakdown
/sp-execute all
/sp-status
/sp-validate
/sp-continue 001-auth
/sp-decompose spec-001
/sp-clarify spec-001
/sp-llm-enforce
```

**🎯 IMPORTANT: Always start with `/sp-pulse` - this is your entry point to everything!**

### Migration Between Platforms

Switching between AI platforms is seamless:

```bash
# Current project with Claude
ls .claude/commands/

# Add Gemini support
specpulse init . --ai gemini

# Both platforms now available
ls .claude/commands/  # Existing
ls .gemini/commands/  # Newly added
```

### Best Practices

1. **Choose Your Primary Platform**: Select 1-2 platforms for daily use
2. **Use Selective Initialization**: Only initialize needed platforms
3. **Maintain Consistency**: Use same commands across platforms
4. **Leverage Platform Strengths**: Use unique features when beneficial

---

## 🔒 Privacy-First Design

### Privacy Principles (v2.7.1)

SpecPulse v2.7.1 maintains privacy as a fundamental requirement while providing enhanced AI integration:

#### **No External API Calls**

- ✅ **Local Processing**: All CLI logic runs on your machine
- ✅ No data transmission: No information leaves your system
- ✅ Offline Operation: Works without internet connectivity
- ✅ Corporate Compliance: Meets enterprise security requirements

#### **Data Privacy**

- ✅ **Local Storage**: All data stored in `.specpulse/` directory
- ✅ No Cloud Dependencies: No cloud storage required
- ✅ **No Telemetry**: No usage data collected or transmitted
- ✅ **User Control**: You have complete control over your data

#### **AI Assistant Privacy**

- ✅ **No External LLM Access**: SpecPulse never calls external AI APIs
- ✅ **Local AI Integration**: AI assistants work through local CLI commands
- ✅ **No Prompt Leakage**: AI prompts remain in your local environment
- ✅ **Model Agnostic**: Works with Claude Code, Gemini CLI without API dependencies

### Security Benefits

#### **Enterprise Ready**

- **No Data Exfiltration Risk**: No data can leave your network
- **Compliance Friendly**: Meets GDPR, HIPAA, and other regulations
- **Audit Trail**: All actions logged locally for audit purposes
- **Air Gapped Networks**: Works completely offline

#### **Intellectual Property Protection**

- **Code Privacy**: Your code never leaves your development environment
- **Specification Security**: Sensitive specifications remain local
- **Team Collaboration**: Share work through standard version control
- **No IP Leakage**: Intellectual property stays within your organization

### Performance Benefits

#### **Network Independence**

- **No Latency**: No waiting for external API responses
- **Consistent Performance**: Performance doesn't depend on external services
- **Reliability**: Works even when internet is unavailable
- **Cost Control**: No ongoing API usage costs

#### **Scalability**

- **Local Processing Power**: Leverages your machine's capabilities
- **No Rate Limits**: No external API rate limiting
- **Parallel Processing**: Can run multiple operations simultaneously
- **Resource Efficiency**: Optimized for local execution

---

## 🔗 Integration with AI Assistants

### Claude Code Integration

#### Initialization

```bash
# Initialize project with Claude support
specpulse init my-project --ai claude
```

This creates `.claude/commands/` directory with custom slash commands:

#### **Claude Slash Commands**

```markdown
# .claude/commands/sp-pulse.md
/sp-pulse {{name}}
Initialize new feature with full structure

# .claude/commands/sp-spec.md
/sp-spec {{description}}
Create or update feature specifications

# .claude/commands/sp-plan.md
/sp-plan {{description}}
Generate implementation plans

# .claude/commands/sp-task.md
/sp-task {{plan_id}}
Break down into tasks

# .claude/commands/sp-execute.md
/sp-execute {{feature_id}}
Execute tasks continuously

# .claude/commands/sp-continue.md
/sp-continue {{feature_id}}
Switch context to existing feature

# .claude/commands/sp-status.md
/sp-status
Track progress across features

# .claude/commands/sp-decompose.md
/sp-decompose {{spec_id}}
Decompose specs into microservices
```

#### **Claude Usage Pattern**

```bash
# In Claude Code, use slash commands:
/sp-pulse user-authentication
/sp-spec create "OAuth2 authentication with JWT tokens"
/sp-plan generate "Secure authentication flow implementation"
/sp-task breakdown plan-001
/sp-status
```

### Gemini CLI Integration

#### Initialization

```bash
# Initialize project with Gemini support
specpulse init my-project --ai gemini
```

This creates `.gemini/commands/` directory with custom commands:

#### **Gemini Command Files**

```toml
# .gemini/commands/sp-pulse.toml
description = "Initialize new feature with full structure"
prompt = """
## Command: /sp-pulse {{name}}

When called, I will:
1. Try CLI first: specpulse feature init {{name}}
2. If CLI doesn't exist, use file operations:
3. Read template from .specpulse/templates/
4. Create feature directory structure
5. Update context.md
"""

# .gemini/commands/sp-spec.toml
description = "Create or update feature specifications"
prompt = """
## Command: /sp-spec {{description}}

When called, I will:
1. Try CLI first: specpulse spec create "{{description}}"
2. If CLI doesn't exist, use file operations:
3. Read template from .specpulse/templates/spec.md
4. Write to .specpulse/specs/ directory
5. Expand specification with AI
"""
```

#### **Gemini Usage Pattern**

```bash
# In Gemini CLI, use custom commands:
/sp-pulse user-authentication
/sp-spec create "OAuth2 authentication with JWT tokens"
/sp-plan generate "Secure authentication flow implementation"
/sp-task breakdown plan-001
/sp-status
```

### Integration Architecture

#### **CLI-First Workflow Pattern**

```
User Request: /sp-spec OAuth2 login with JWT
    ↓
Step 1: Try CLI first
    Bash: specpulse spec create "OAuth2 login with JWT"
    ↓
Step 2: If CLI doesn't exist, use File Operations:
    Claude reads: .specpulse/templates/spec.md
    Claude writes: .specpulse/specs/001-feature/spec-001.md
    Claude edits: .specpulse/specs/001-feature/spec-001.md (expand)
    ↓
Complete specification ready
```

#### **Why CLI First?**

- **Metadata Handling**: CLI manages timestamps, IDs, status automatically
- **Structure Validation**: CLI validates before creating files
- **Context Updates**: CLI updates context.md consistently
- **Error Handling**: CLI provides recovery and validation
- **File Operations**: Fallback for flexibility when CLI doesn't cover operation

---

## ⚙️ Configuration (v2.7.1)

### Environment Variables

```bash
# Set custom templates directory
export SPECPULSE_TEMPLATES_DIR="/path/to/custom/templates"

# Enable verbose logging
export SPECPULSE_VERBOSE=1

# Set custom editor
export SPECPULSE_EDITOR="code"
```

### Project Configuration

SpecPulse v2.7.1 uses simplified configuration:

#### **No Configuration Required**

SpecPulse works out of the box with sensible defaults. All configuration is handled through CLI commands.

#### **Optional Settings**

If needed, you can customize specific aspects:

```bash
# Set default template tier
specpulse config set template_tier standard

# Set default AI assistant
specpulse config set ai_assistant claude

# Enable/disable features
specpulse config set auto_validate true
specpulse config set git_integration true
```

### Memory System Configuration

#### **Context File** (`.specpulse/memory/context.md`)

```yaml
current_feature: "001-user-authentication"
project_info:
  name: "My Project"
  type: "web"
  tech_stack:
    frontend: "React"
    backend: "FastAPI"
    database: "PostgreSQL"

workflow:
  phase: "specification"
  last_command: "specpulse spec create"
  progress: 15.0

last_updated: "2025-11-01T12:00:00Z"
```

#### **Decisions File** (`.specpulse/memory/decisions.md`)

```markdown
# Architectural Decisions

## Decision: OAuth2 Implementation (2025-11-01)
**Context**: User Authentication Feature
**Decision**: Use OAuth2 with JWT tokens
**Rationale**: Industry standard, secure, good library support
**Alternatives**: Basic auth, Session auth
**Impact**: Enhanced security, better user experience
```

### Template Customization

#### **Copy and Modify Templates**

```bash
# Copy default template to customize
cp .specpulse/templates/spec-tier2-standard.md .specpulse/templates/my-custom-spec.md

# Edit the template
vim .specpulse/templates/my-custom-spec.md

# Use custom template
specpulse spec create "My feature" --template my-custom-spec
```

#### **Template Variables**

Templates support these variables:
- `{{ feature_name }}` - Current feature name
- `{{ feature_id }}` - Current feature ID
- `{{ timestamp }}` - Current timestamp
- `{{ author }}` - Git author name
- `{{ project_name }}` - Project name

### Directory Structure

```
.specpulse/
├── templates/                 # Template files
│   ├── spec-tier1-minimal.md
│   ├── spec-tier2-standard.md
│   ├── spec-tier3-complete.md
│   ├── plan.md
│   └── task.md
├── memory/                   # Memory and context files
│   ├── context.md
│   ├── decisions.md
│   ├── patterns.md
│   └── knowledge.md
├── specs/                    # Generated specifications
├── plans/                    # Generated implementation plans
├── tasks/                    # Generated task breakdowns
└── context.md               # Project context file
```

### AI Command Files

#### **Claude Code Commands** (`.claude/commands/`)

All Claude commands instruct Claude to use **file operations**, not CLI commands:

```markdown
# .claude/commands/sp-spec.md
When called with /sp-spec, I will:
1. Read template from .specpulse/templates/spec.md
2. Write new file to .specpulse/specs/001-feature/spec-XXX.md
3. Edit that file to expand it with full specification
4. Optionally run validation
```

#### **Gemini CLI Commands** (`.gemini/commands/`)

All Gemini commands instruct Gemini to use **file operations**, not CLI commands:

```toml
# .gemini/commands/sp-spec.toml
prompt = """
## Command: /sp-spec {{args}}

When called, I will:
1. Read template from .specpulse/templates/spec.md
2. Write new file to .specpulse/specs/001-feature/spec-XXX.md
3. Edit that file to expand it with full specification
4. Optionally run validation
"""
```

**Important**: Never edit files in `.specpulse/templates/`, `.claude/`, `.gemini/`, or `specpulse/` folders.

---

## 🐛 Troubleshooting (v2.7.1)

### Common Issues

#### CLI Commands Not Working

**Issue**: CLI commands fail with "command not found"

**Solutions**:

```bash
# Check installation
pip show specpulse

# Verify PATH
which specpulse

# Reinstall if needed
pip uninstall specpulse
pip install specpulse

# Use development mode
pip install -e .
```

#### AI Assistant Commands Not Found

**Issue**: `/sp-*` commands not recognized

**Solutions**:

```bash
# Initialize project with AI support
specpulse init my-project --ai claude
# or
specpulse init my-project --ai gemini

# Check command files exist
ls .claude/commands/
ls .gemini/commands/

# Reinitialize commands
specpulse init --here --ai claude
```

#### Template Loading Issues

**Issue**: Templates not found or errors loading templates

**Solutions**:

```bash
# Check template directory
ls .specpulse/templates/

# Verify template files exist
ls .specpulse/templates/spec-*.md

# Reinitialize project
rm -rf .specpulse/
specpulse init --here

# Use development installation
pip install -e .
```

#### Git Integration Problems

**Issue**: Git branches not detected or git errors

**Solutions**:

```bash
# Check git status
git status
git branch --show-current

# Initialize git if needed
git init
git add .
git commit -m "Initial commit"

# Create feature branch
git checkout -b 001-my-feature
```

### Memory System Issues

#### Context Not Updating

**Issue**: Project context not reflecting current state

**Solutions**:

```bash
# Check context file
cat .specpulse/memory/context.md

# Update context manually
echo "current_feature: 001-my-feature" >> .specpulse/memory/context.md

# Use feature commands
specpulse feature continue 001-my-feature
```

#### Memory Files Missing

**Issue**: Memory files not created or corrupted

**Solutions**:

```bash
# Check memory directory
ls .specpulse/memory/

# Create memory files manually
mkdir -p .specpulse/memory/
echo "# Context" > .specpulse/memory/context.md
echo "# Decisions" > .specpulse/memory/decisions.md
echo "# Patterns" > .specpulse/memory/patterns.md
```

### Platform-Specific Issues

#### Windows Issues

**Issue**: Path separator problems or encoding issues

**Solutions**:

```bash
# Use PowerShell instead of Command Prompt
# Set UTF-8 encoding
chcp 65001

# Use forward slashes in paths
# SpecPulse handles path conversion automatically
```

#### Linux/macOS Issues

**Issue**: Permission errors or Python environment issues

**Solutions**:

```bash
# Use virtual environment
python -m venv specpulse-env
source specpulse-env/bin/activate
pip install specpulse

# Install for user only
pip install --user specpulse

# Check Python version (requires 3.11+)
python --version
```

### Performance Issues

#### Slow Operations

**Issue**: Commands taking too long to execute

**Solutions**:

```bash
# Clean up old files
find .specpulse/ -name "*.md" -mtime +30 -delete

# Use verbose mode to debug
export SPECPULSE_VERBOSE=1
specpulse feature list

# Check for large files
du -sh .specpulse/
```

### Getting Help

#### Command Help

```bash
# Get general help
specpulse --help

# Get specific command help
specpulse feature --help
specpulse spec --help
specpulse plan --help

# Check version
specpulse --version
```

#### System Diagnostics

```bash
# Run system check
specpulse doctor

# Check all configurations
specpulse config show

# Validate project structure
specpulse validate all
```

---

## 📋 Best Practices (v2.7.1)

### CLI-First Workflow Best Practices

#### 1. Always Try CLI Commands First

```bash
# CORRECT: Try CLI command first
specpulse spec create "User authentication with OAuth2"

# INCORRECT: Direct file operations (CLI exists)
# Reading/writing files directly when CLI command is available
```

#### 2. Use File Operations as Fallback

```bash
# When CLI doesn't exist or doesn't cover operation:
# 1. Read template from .specpulse/templates/
# 2. Write/EDIT files in appropriate directories
# 3. Never edit protected directories
```

#### 3. Follow the Workflow Hierarchy

1. **FIRST**: Try CLI command (if exists)
2. **SECOND**: File operations (if CLI doesn't exist)
3. **NEVER**: Direct edits to protected directories

### Project Initialization Best Practices

#### Choose Right AI Assistant

```bash
# For reasoning-heavy projects
specpulse init my-project --ai claude

# For template-heavy projects
specpulse init my-project --ai gemini

# For maximum capability
specpulse init my-project --ai both
```

#### Initialize in Existing Directory

```bash
# Initialize in current directory
specpulse init --here --ai claude

# Initialize new directory
specpulse init my-project --ai claude
cd my-project
```

### Feature Development Best Practices

#### Use Feature Branch Naming

```bash
# Create properly named feature branches
git checkout -b 001-user-authentication
git checkout -b 002-api-redesign
git checkout -b 003-mobile-onboarding

# SpecPulse automatically detects feature from branch name
```

#### Follow Standard Workflow

```bash
# 1. Initialize feature
specpulse feature init user-authentication

# 2. Create specification
specpulse spec create "OAuth2 authentication with JWT tokens"

# 3. Generate implementation plan
specpulse plan create "Secure authentication flow"

# 4. Break down into tasks
specpulse task breakdown <plan-id>

# 5. Validate work
specpulse validate all
```

#### Context Switching

```bash
# Switch to existing feature
specpulse feature continue 001-user-authentication

# Get feature status
specpulse feature status 001-user-authentication

# List all features
specpulse feature list
```

### Template Usage Best Practices

#### Choose Appropriate Template Tier

```bash
# Quick prototypes (2-3 min)
spec-tier1-minimal

# Standard production features (10-15 min)
spec-tier2-standard

# Enterprise specifications (30-45 min)
spec-tier3-complete
```

#### Customize Templates Properly

```bash
# Copy template to customize (never edit original)
cp .specpulse/templates/spec-tier2-standard.md .specpulse/templates/my-custom.md

# Edit your copy
vim .specpulse/templates/my-custom.md

# Use custom template
specpulse spec create "My feature" --template my-custom
```

### Memory Management Best Practices

#### Maintain Context Files

```bash
# Keep context.md updated
echo "current_feature: 001-user-auth" >> .specpulse/memory/context.md

# Document architectural decisions
echo "## Decision: Use OAuth2" >> .specpulse/memory/decisions.md

# Track reusable patterns
echo "## Repository Pattern" >> .specpulse/memory/patterns.md
```

#### Use Git for Checkpoints

```bash
# Create milestone tags
git tag -a milestone-001 -m "Feature 001 complete"

# Create experimental branches
git checkout -b experiment/new-approach

# Return to safe points
git checkout main
git checkout milestone-001
```

### AI Assistant Integration Best Practices

#### Claude Code Usage

```bash
# Use slash commands in Claude Code
/sp-pulse user-authentication
/sp-spec create "OAuth2 authentication"
/sp-plan generate
/sp-task breakdown
/sp-status
```

#### Gemini CLI Usage

```bash
# Use custom commands in Gemini CLI
/sp-pulse user-authentication
/sp-spec create "OAuth2 authentication"
/sp-plan generate
/sp-task breakdown
/sp-status
```

### Validation Best Practices

#### Validate Frequently

```bash
# Validate specifications
specpulse validate spec

# Validate plans
specpulse validate plan

# Validate all components
specpulse validate all

# Auto-fix issues when possible
specpulse validate all --fix
```

### Troubleshooting Best Practices

#### Use System Commands

```bash
# Check system health
specpulse doctor

# Get help
specpulse --help
specpulse feature --help

# Validate project
specpulse validate all

# Use verbose mode for debugging
export SPECPULSE_VERBOSE=1
```

---

## 📞 Support

### Documentation Resources

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [Migration Guide](MIGRATION.md) - Upgrading from previous versions
- [Migration Guide v2.7.1](MIGRATION_v2.7.1.md) - Specific migration for v2.7.1
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions

### Getting Help

```bash
# Get general help
specpulse --help

# Get specific command help
specpulse feature --help
specpulse spec --help
specpulse plan --help
specpulse task --help

# Check system health
specpulse doctor

# Validate project structure
specpulse validate all
```

### Command Reference

#### **Setup Commands**
```bash
pip install specpulse                 # Install SpecPulse
specpulse init my-project --ai claude # Initialize with AI
specpulse doctor                      # System health check
```

#### **AI Commands (Use in AI Assistants)**
```bash
/sp-pulse <feature-name>             # Start new feature (PRIMARY ENTRY POINT)
/sp-spec "<description>"             # Create specification
/sp-plan                             # Generate implementation plan
/sp-task                             # Break down into tasks
/sp-execute                          # Execute tasks
/sp-status                           # Check progress
/sp-validate                         # Validate work
/sp-continue <feature-id>            # Switch to existing feature
/sp-decompose <spec-id>              # Decompose specifications
/sp-clarify <spec-id>                # Clarify requirements
/sp-llm-enforce [action]             # LLM compliance enforcement
```

### Community Resources

- **GitHub Issues**: [github.com/specpulse/specpulse/issues](https://github.com/specpulse/specpulse/issues)
- **GitHub Discussions**: [github.com/specpulse/specpulse/discussions](https://github.com/specpulse/specpulse/discussions)
- **GitHub Releases**: [github.com/specpulse/specpulse/releases](https://github.com/specpulse/specpulse/releases)

### Reporting Issues

When reporting issues, please include:

1. **System Information**: Operating system, Python version, SpecPulse version
2. **Error Messages**: Full error output and stack traces
3. **Steps to Reproduce**: Clear steps to reproduce the issue
4. **Expected vs Actual**: What you expected vs what actually happened

### Quick Debug Commands

```bash
# Check version
specpulse --version

# Enable verbose logging
export SPECPULSE_VERBOSE=1

# Check installation
pip show specpulse

# Validate everything
specpulse validate all

# System diagnostics
specpulse doctor
```

---

**🎉 Congratulations! You now have a complete understanding of SpecPulse v2.7.1's AI integration capabilities. Build better software, faster, with intelligent AI assistance while maintaining complete privacy and control!**