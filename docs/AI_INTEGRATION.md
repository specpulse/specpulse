# SpecPulse v2.0.0 AI Integration Guide

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [AI Commands](#ai-commands)
- [Smart Context Detection](#smart-context-detection)
- [AI-Powered Suggestions](#ai-powered-suggestions)
- [Multi-LLM Support](#multi-llm-support)
- [AI Workflow Checkpoints](#ai-workflow-checkpoints)
- [Privacy-First Design](#privacy-first-design)
- [Integration with AI Assistants](#integration-with-ai-assistants)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## 🎯 Overview

SpecPulse v2.0.0 introduces revolutionary AI integration that enhances your specification-driven development workflow while maintaining complete privacy and control. Unlike traditional AI tools that require external API calls, SpecPulse's AI integration works entirely offline, processing all logic locally on your machine.

### Key Principles

1. **Privacy-First**: No data leaves your system
2. **Local Processing**: All AI logic runs locally
3. **Context-Aware**: Understands your project structure
4. **Multi-LLM Support**: Works with Claude, Gemini, or both
5. **Intelligent Suggestions**: Provides context-aware recommendations

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

## 🤖 AI Commands

### Core AI Commands

#### `specpulse ai context`

Show AI-detected project context and current state.

```bash
specpulse ai context
```

**Example Output:**
```
AI Context Detection

Current Feature
Feature: 003-user-authentication

Git Context
Branch: 003-validation-feedback-improvements

Recent Activity
Recent Specs:
- specs/001-user-authentication/spec-001.md
- specs/002-api-redesign/spec-001.md

Recent Plans:
- plans/001-user-authentication/plan-001.md
```

#### `specpulse ai suggest`

Get AI-powered suggestions based on current project state.

```bash
specpulse ai suggest
```

**Example Output:**
```
AI-Powered Suggestions

Next Steps
1. Create specification with /sp-spec
2. Consider security requirements for authentication
3. Plan database migrations for PostgreSQL
```

#### `specpulse ai suggest --query <topic>`

Get help with specific topics or questions.

```bash
specpulse ai suggest --query "template selection"
specpulse ai suggest --query "validation errors"
specpulse ai suggest --query "project structure"
```

**Example Output:**
```
Query: template selection

Template Recommendations
- spec-tier1-minimal (2-3 min, quick prototypes)
- spec-tier2-standard (10-15 min, most features)
- spec-tier3-complete (30-45 min, production features)
```

#### `specpulse ai switch <llm>`

Switch between different AI assistants.

```bash
specpulse ai switch claude    # Use Claude Code
specpulse ai switch gemini    # Use Gemini CLI
specpulse ai switch both      # Use both simultaneously
```

**Example Output:**
```
Switched to CLAUDE
Using both Claude and Gemini for enhanced capabilities
```

#### `specpulse ai checkpoint <description>`

Create AI workflow checkpoints to save and restore states.

```bash
specpulse ai checkpoint "Before implementing user authentication"
specpulse ai checkpoint "Major design decision completed"
specpulse ai checkpoint "Before production deployment"
```

**Example Output:**
```
AI Workflow Checkpoint

Checkpoint created: checkpoint-003
Description: Before implementing user authentication
```

#### `specpulse ai summary`

Show complete AI workflow summary with current status and suggestions.

```bash
specpulse ai summary
```

**Example Output:**
```
AI Workflow Summary

Current Status
Feature: 003-user-authentication
Phase: Spec
Active LLM: BOTH
Progress: 0.0%

Suggestions
- Create specification with /sp-spec
- Consider security requirements for authentication

Recent Activity
Last activity: 2025-10-07 15:30:45
Checkpoints: 3
```

---

## 🧠 Smart Context Detection

### Context Sources

SpecPulse automatically detects context from multiple sources:

#### 1. Git Branch Analysis

```bash
# Example branch names and detected features
001-user-authentication      → Feature: 001-user-authentication
002-api-redesign             → Feature: 002-api-redesign
003-mobile-onboarding         → Feature: 003-mobile-onboarding
```

#### 2. Memory File Analysis

```yaml
# memory/context.md content
current_feature: "003-user-authentication"
tech_stack:
  frontend: "React"
  backend: "Node.js"
  database: "PostgreSQL"
last_updated: "2025-10-07T15:30:00Z"
```

#### 3. Recent Activity Tracking

- **Recent Specifications**: Analyzes newly created or modified spec files
- **Recent Plans**: Tracks plan file activity
- **Recent Tasks**: Monitors task list updates
- **Template Usage**: Identifies which templates are being used

#### 4. Technology Stack Detection

```json
{
  "project_type": "web",
  "detected_technologies": ["React", "Node.js", "PostgreSQL"],
  "inferred_patterns": ["REST API", "JWT Authentication"]
}
```

### Context Features

#### **Smart Feature Recognition**

- **Branch Pattern Matching**: Automatically detects feature IDs from branch names
- **Project Type Classification**: Identifies web, API, mobile, or other project types
- **Technology Stack Inference**: Detects frameworks and tools being used
- **Workflow Phase Detection**: Determines current development phase (spec, plan, task, etc.)

#### **Dynamic Context Updates**

- **Real-time Updates**: Context refreshes automatically as you work
- **Manual Refresh**: Use `specpulse ai context --refresh` to force refresh
- **Context Persistence**: Context is saved and restored across sessions

---

## 💡 AI-Powered Suggestions

### Suggestion Engine

The AI suggestion engine analyzes your current project state and provides intelligent recommendations:

#### **Context-Aware Suggestions**

```bash
# Different suggestions based on project state
# Starting new feature:
Suggestions:
1. Create specification with /sp-spec
2. Set up development environment
3. Choose appropriate template tier

# After specification created:
Suggestions:
1. Validate specification with /sp-spec validate
2. Create implementation plan with /sp-plan
3. Set up task breakdown with /sp-task

# During implementation:
Suggestions:
1. Track progress with /sp-task progress
2. Add development notes for insights
3. Create checkpoints before major changes
```

#### **Project-Specific Recommendations**

```bash
# Authentication projects:
Suggestions:
1. Consider security requirements
2. Plan password policies
3. Design session management
4. Plan database migrations

# API projects:
Suggestions:
1. Design API contracts
2. Plan integration tests
3. Consider rate limiting
4. Document error handling

# Mobile projects:
Suggestions:
1. Consider offline functionality
2. Plan responsive design
3. Design navigation patterns
4. Plan app store deployment
```

#### **Technology-Specific Advice**

```bash
# React projects:
Suggestions:
1. Consider component architecture
2. Plan state management
3. Choose testing strategy
4. Plan build optimization

# Django projects:
Suggestions:
1. Design app structure
2. Plan Django apps
3. Consider database migrations
4. Plan API versioning
```

### Query-Based Assistance

The AI system can provide targeted help for specific topics:

```bash
# Template selection help
specpulse ai suggest --query "which template should I use"

# Validation help
specpulse ai suggest --query "validation errors keep appearing"

# Workflow guidance
specpulse ai suggest --query "what should I work on next"

# Project structure advice
specpulse ai suggest --query "how should I organize my project"
```

---

## 🔄 Multi-LLM Support

### Supported AI Assistants

#### Claude Code

```bash
# Initialize with Claude support
specpulse init my-project --ai claude

# Switch to Claude
specpulse ai switch claude

# Use both simultaneously
specpulse ai switch both
```

**Features:**
- Advanced reasoning capabilities
- Better context understanding
- Superior code analysis
- Enhanced documentation generation

#### Gemini CLI

```bash
# Initialize with Gemini support
specpulse init my-project --ai gemini

# Switch to Gemini
specpulse ai switch gemini

# Use both simultaneously
specpulse ai switch both
```

**Features:**
- Fast response times
- Good template filling
- Efficient batch processing
- Cost-effective operation

### Multi-LLM Mode

When using `specpulse ai switch both`, SpecPulse:

1. **Context Sharing**: Both LLMs access the same project context
2. **Parallel Processing**: Can leverage strengths of both systems
3. **Cross-Validation**: Different perspectives on the same problem
4. **Enhanced Suggestions**: Combines insights from both AI systems

### LLM Management

#### **Switching Between LLMs**

```bash
# Check current active LLM
specpulse ai summary

# Switch to different LLM
specpulse ai switch gemini

# Switch back to Claude
specpulse ai switch claude
```

#### **LLM-Specific Features**

- **Claude**: Better at complex reasoning and architectural decisions
- **Gemini**: Faster at template filling and routine tasks
- **Both**: Combines strengths of both systems

---

## 📸 AI Workflow Checkpoints

### Checkpoint System Overview

AI workflow checkpoints allow you to save and restore specific states during your development process, providing safety nets and progress tracking.

### Creating Checkpoints

```bash
# Create automatic checkpoints
# (Happens automatically before major operations)

# Create manual checkpoints
specpulse ai checkpoint "Before implementing user authentication"
specpulse ai checkpoint "Major architecture decision made"
specpulse ai checkpoint "Ready for code review"
```

### Checkpoint Features

#### **Automatic Checkpoints**

- **Before Tier Expansion**: Saves state before expanding template complexity
- **Before Major Changes**: Creates backups before significant modifications
- **Before Validation**: Saves state before running validation operations
- **Error Recovery**: Automatic checkpoints before potentially risky operations

#### **Manual Checkpoints**

- **Milestone Markers**: Mark important decision points
- **Phase Transitions**: Save state between workflow phases
- **Team Handoffs**: Create checkpoints before team member handoffs
- **Risk Mitigation**: Save state before experimental changes

#### **Checkpoint Content**

Each checkpoint includes:

```json
{
  "id": "checkpoint-003",
  "timestamp": "2025-10-07T15:30:00Z",
  "phase": "spec",
  "feature_id": "001-user-authentication",
  "description": "Before implementing user authentication",
  "context": {
    "current_feature": "001-user-authentication",
    "branch_name": "001-user-authentication",
    "recent_files": ["specs/001-user-authentication/spec-001.md"],
    "suggestions": ["Create implementation plan", "Set up testing"],
    "ai_state": {
      "active_llm": "claude",
      "last_command": "specpulse ai context",
      "progress": 25.0
    }
  }
}
```

### Checkpoint Management

#### **Listing Checkpoints**

```bash
# List all checkpoints for a feature
specpulse checkpoint list 001-user-authentication
```

#### **Restoring Checkpoints**

```bash
# Restore to previous state
specpulse checkpoint restore 001-user-authentication checkpoint-002

# Force restore without confirmation
specpulse checkpoint restore 001-user-authentication checkpoint-002 --force
```

#### **Cleanup Operations**

```bash
# Clean up old checkpoints
specpulse checkpoint cleanup 001-user-authentication --older-than-days 30
```

### Checkpoint Benefits

- **Risk Mitigation**: Safe experimentation with guaranteed recovery
- **Progress Tracking**: Clear markers of important milestones
- **Team Collaboration**: Easy handoff points between team members
- **Learning & Review**: Save states for later analysis and learning

---

## 🔒 Privacy-First Design

### Privacy Principles

SpecPulse v2.0.0 is designed with privacy as a fundamental requirement:

#### **No External API Calls**

- ✅ **Local Processing**: All AI logic runs on your machine
- ✅ No data transmission: No information leaves your system
- ✅ Offline Operation: Works without internet connectivity
- ✅ Corporate Compliance: Meets enterprise security requirements

#### **Data Privacy**

- ✅ **Local Storage**: All data stored on your local filesystem
- ✅ No Cloud Dependencies: No cloud storage required
- ✅ **No Telemetry**: No usage data collected or transmitted
- ✅ **User Control**: You have complete control over your data

#### **AI Privacy**

- ✅ **No External LLM Access**: SpecPulse never calls external AI APIs
- ✅ **Local AI Logic**: All AI processing happens locally
- ✅ **No Prompt Leakage**: AI prompts remain in your local environment
- ✅ **Model Agnostic**: Works with any AI assistant without API dependencies

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

#### Installation

```bash
# Initialize project with Claude support
specpulse init my-project --ai claude
```

#### Custom Commands

SpecPulse automatically creates custom Claude Code commands:

```markdown
# .claude/commands/sp-spec.md
# /sp-spec Command

When called with `/sp-spec $ARGUMENTS`, I will:
1. Detect current feature context
2. Parse arguments to determine action
3. Read template from templates/spec.md
4. Generate specification using AI
5. Save to specs/ directory
6. Run validation
```

#### Usage in Claude Code

```bash
# Start new feature
/sp-pulse user-authentication

# Create specification
/sp-spec create user authentication with OAuth2

# Generate implementation plan
/sp-plan generate

# Create task breakdown
/sp-task breakdown

# Validate work
/sp-spec validate
```

### Gemini CLI Integration

#### Installation

```bash
# Initialize project with Gemini support
specpulse init my-project --ai gemini
```

#### Custom Commands

SpecPulse automatically creates custom Gemini CLI commands:

```toml
# .gemini/commands/sp-spec.toml
description = "Create or manage feature specifications"

prompt = """
## Command: /sp-spec {{args}}

When called, I will:
1. Detect current feature context
2. Parse arguments to determine action
3. Read template from @{templates/spec.md}
4. Generate specification using AI
5. Save to specs/ directory
6. Run validation
"""
```

#### Usage in Gemini CLI

```toml
# Start new feature
/sp-pulse user-authentication

# Create specification
/sp-spec create user authentication with OAuth2

# Generate implementation plan
/sp-plan generate

# Create task breakdown
/sp-task breakdown

# Validate work
/sp-spec validate
```

### Integration Benefits

#### **Seamless Workflow**

- **Context Awareness**: AI assistants automatically understand project context
- **Template Access**: Direct access to project templates
- **Validation Integration**: Can run validation commands directly
- **Memory System**: Access to project memory and knowledge base

#### **Enhanced Capabilities**

- **Smart Suggestions**: AI provides context-aware recommendations
- **Progress Tracking**: Real-time workflow monitoring
- **Error Prevention**: Early detection of potential issues
- **Best Practices**: AI follows established patterns and conventions

#### **Unified Experience**

- **Consistent Interface**: Same commands across different AI assistants
- **Shared Context**: All AI assistants access the same project information
- **Synchronized State**: Changes are immediately available to all team members
- **Version Control**: All work tracked through standard Git workflow

---

## ⚙️ Advanced Configuration

### Environment Variables

```bash
# Set custom templates directory
export SPECPULSE_TEMPLATES_DIR="/path/to/custom/templates"

# Set custom memory directory
export SPECPULSE_MEMORY_DIR="/path/to/custom/memory"

# Enable verbose logging
export SPECPULSE_VERBOSE=1

# Set AI cache directory
export SPECPULSE_AI_CACHE_DIR="/path/to/ai/cache"
```

### Configuration Files

#### Project Configuration (`.specpulse/config.yaml`)

```yaml
ai:
  primary: claude
  context_detection:
    enabled: true
    auto_refresh: true
    git_integration: true

  suggestions:
    enabled: true
    learning_mode: false
    contextual: true

  multi_llm:
    enabled: true
    default_llm: claude
    allow_both: true

  privacy:
    local_only: true
    no_external_apis: true
    cache_encryption: false
```

#### AI Configuration (`.specpulse/ai_state.json`)

```json
{
  "current_phase": "spec",
  "active_llm": "claude",
  "last_command": "specpulse ai context",
  "suggestions": [
    "Create specification with /sp-spec",
    "Consider security requirements",
    "Plan database migrations"
  ],
  "checkpoints": [
    {
      "id": "checkpoint-001",
      "timestamp": "2025-10-07T15:30:00Z",
      "phase": "spec",
      "description": "Starting user authentication"
    }
  ],
  "progress": 25.0,
  "last_activity": "2025-10-07T15:30:00Z"
}
```

### Custom Templates

#### Creating Custom Templates

```bash
# Create custom template directory
mkdir -p templates/custom

# Create custom specification template
cat > templates/custom/my-spec.md << 'EOF'
---
template: my-spec
name: My Custom Specification
tier: custom
description: Custom specification for my team
sections: [overview, requirements, acceptance]
---

# Specification: {{ feature_name }}
## Overview
{{ problem_statement }}

## Requirements
{{ functional_requirements }}

## Acceptance Criteria
{{ acceptance_criteria }}
EOF

# Validate custom template
specpulse template validate my-spec
```

#### Template Inheritance

```yaml
# templates/my-spec.yaml
extends: spec-tier2-standard
name: Enhanced Standard Template
description: Standard template with custom sections
additional_sections:
  - compliance
  - performance_requirements
  - deployment_procedures
```

### Memory Configuration

#### Structured Memory System

```bash
# Add architectural decision
specpulse memory add-decision "OAuth2 Implementation" \
  --rationale "Industry standard for secure authentication" \
  --feature "001-user-auth"

# Add code pattern
specpulse memory add-pattern "Repository Pattern" \
  --example "class UserRepository:" \
  --features "001-user-auth,002-api"

# Query memory by tag
specpulse memory query --tag decision --feature "001-user-auth"
specpulse memory query --tag pattern --recent 5
```

#### Memory Organization

```yaml
# memory/decisions.md
## Architecture Decisions

### Decision: OAuth2 Implementation (2025-10-07)
**Context**: User Authentication Feature
**Rationale**: Industry standard for secure authentication
**Alternatives Considered**: Basic auth, Session auth
**Impact**: Security improvement, user experience

# memory/patterns.md
## Code Patterns

### Repository Pattern (2025-10-07)
**Usage**: Data access layer implementation
**Features**: Centralized data operations, caching
**Projects**: 001-user-auth, 002-api-redesign
```

---

## 🐛 Troubleshooting

### Common AI Integration Issues

#### Context Detection Problems

**Issue**: AI context not detected correctly

**Symptoms**:
- `specpulse ai context` shows "No current feature detected"
- Git branch names not recognized
- Technology stack not inferred

**Solutions**:

```bash
# Check Git status
git status
git branch --show-current

# Initialize git if needed
git init
git add .
git commit -m "Initial commit"

# Check project structure
ls -la
ls specs/ plans/ tasks/ memory/

# Refresh context manually
specpulse ai context --refresh
```

#### AI Suggestions Not Working

**Issue**: AI suggestions are generic or irrelevant

**Symptoms**:
- Suggestions don't match project context
- Recommendations seem generic
- No project-specific advice

**Solutions**:

```bash
# Check project context
specpulse ai context

# Verify recent activity
specpulse memory summary

# Provide specific query
specpulse ai suggest --query "my specific problem"

# Update project context if needed
specpulse context set tech_stack.framework React
```

#### Multi-LLM Issues

**Issue**: LLM switching doesn't work properly

**Symptoms**:
- `specpulse ai switch claude` fails
- Both mode doesn't activate
- AI assistant not recognized

**Solutions**:

```bash
# Check available LLMs
specpulse ai summary

# Verify AI state
cat .specpulse/ai_state.json

# Reset AI state if needed
rm .specpulse/ai_state.json
specpulse ai context
```

### Performance Issues

#### Slow Context Detection

**Issue**: Context detection takes too long

**Symptoms**:
- `specpulse ai context` takes >10 seconds
- AI suggestions are delayed
- Workflow feels sluggish

**Solutions**:

```bash
# Clean up old memory entries
specpulse memory cleanup --days 30

# Optimize AI cache
export SPECPULSE_AI_CACHE_DIR="/tmp/specpulse-cache"
rm -rf /tmp/specpulse-cache

# Use targeted context refresh
specpulse ai context --refresh
```

#### Memory Usage High

**Issue**: Memory consumption is excessive

**Solutions**:

```bash
# Check memory usage
specpulse memory summary

# Clean up old entries
specpulse memory cleanup --days 7

# Adjust retention policy
# Edit .specpulse/config.yaml
```

### Template Issues

#### Template Loading Problems

**Issue**: Templates not found or corrupted

**Solutions**:

```bash
# Validate templates
specpulse template validate

# Restore from backup
specpulse template restore

# Reinstall templates
pip uninstall specpulse
pip install specpulse==2.0.0
```

#### Template Inheritance Issues

**Issue**: Custom templates don't inherit properly

**Solutions**:

```bash
# Check template registry
cat .specpulse/template_registry.json

# Validate inheritance
specpulse template validate my-custom-template

# Fix template metadata
# Edit templates/my-custom-template.yaml
```

### System Compatibility

#### Windows-Specific Issues

**Issue**: Unicode errors on Windows

**Symptoms**:
- Error messages with character encoding
- Console output garbled
- File encoding problems

**Solutions**:
- ✅ **Already Fixed**: v2.0.0 includes Unicode fixes
- Use PowerShell instead of Command Prompt
- Set console encoding: `chcp 65001`

#### Linux-Specific Issues

**Issue**: Permission errors on Linux

**Solutions**:

```bash
# Install for user only
pip install --user specpulse==2.0.0

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Use virtual environment
python -m venv specpulse-env
source specpulse-env/bin/activate
pip install specpulse==2.0.0
```

---

## 📋 Best Practices

### AI Integration Best Practices

#### 1. Initialize Projects Correctly

```bash
# Choose appropriate AI assistant for your team
specpulse init my-project --ai claude    # For reasoning-heavy projects
specpulse init my-project --ai gemini    # For template-heavy projects
specpulse init my-project --ai both       # For maximum capability
```

#### 2. Use Context Effectively

```bash
# Always check context before major decisions
specpulse ai context

# Get suggestions when unsure what to do next
specpulse ai suggest

# Use targeted queries for specific help
specpulse ai suggest --query "validation approach"
```

#### 3. Leverage Checkpoints

```bash
# Create checkpoints before major changes
specpulse ai checkpoint "Before implementing authentication"

# Create checkpoints for team handoffs
specpulse ai checkpoint "Before code review"

# Create checkpoints before risky experiments
specpulse ai checkpoint "Before major refactoring"
```

#### 4. Multi-LLM Strategy

```bash
# Use Claude for complex reasoning
specpulse ai switch claude
/sp-spec create complex architectural decision

# Use Gemini for routine tasks
specpulse ai switch gemini
/sp-plan generate from specification

# Use both for comprehensive work
specpulse ai switch both
# Get multiple perspectives on complex problems
```

### Template Best Practices

#### 1. Choose Appropriate Template Tier

```bash
# Quick prototypes and MVPs
specpulse init my-project --template web
# Use spec-tier1-minimal template

# Most production features
specpulse init my-project --template api
# Use spec-tier2-standard template

# Enterprise-grade specifications
specpulse init my-project --template mobile
# Use spec-tier3-complete template
```

#### 2. Expand Iteratively

```bash
# Start minimal
# (spec-tier1-minimal template)

# Expand when ready
specpulse expand 001-feature --to-tier standard

# Expand further when needed
specpulse expand 001-feature --to-tier complete
```

#### 3. Customize When Needed

```bash
# Create custom template
cp templates/spec-tier2-standard.md templates/my-custom-template.md

# Modify for your needs
vim templates/my-custom-template.md

# Register custom template
# Update .specpulse/template_registry.json
```

### Memory Management Best Practices

#### 1. Capture Decisions

```bash
# Add architectural decisions immediately
specpulse memory add-decision "Use OAuth2 for authentication"
specpulse memory add-decision "Choose PostgreSQL for primary database"

# Add with rationale
specpulse memory add-decision "OAuth2 Implementation" \
  --rationale "Industry standard with good library support"
```

#### 2. Document Patterns

```bash
# Add code patterns for reuse
specpulse memory add-pattern "Repository Pattern" \
  --example "class UserRepository:" \
  --features "001-user-auth"
```

#### 3. Query Knowledge

```bash
# Find past decisions
specpulse memory search "authentication"

# Get recent patterns
specpulse memory query --tag pattern --recent 5

# Get feature-specific knowledge
specpulse memory relevant 001-user-auth
```

### Workflow Best Practices

#### 1. Start with Context

```bash
# Always begin with context awareness
specpulse ai context
specpulse ai suggest
```

#### 2. Validate Frequently

```bash
# Validate specifications
specpulse validate spec --fix

# Validate all components
specpulse validate all --fix

# Validate before major changes
specpulse validate all
```

#### 3. Track Progress

```bash
# Monitor specification progress
specpulse spec progress 001-feature

# Show workflow summary
specpulse ai summary
```

#### 4. Save State Regularly

```bash
# Create checkpoints before major operations
specpulse ai checkpoint "Before implementation"
specpulse ai checkpoint "Before deployment"
```

---

## 📞 Support

### Documentation Resources

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [Migration Guide](MIGRATION.md) - Upgrading from previous versions
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [API Reference](docs/API_REFERENCE.md) - Complete command reference

### Community Resources

- **GitHub Issues**: [github.com/specpulse/specpulse/issues](https://github.com/specpulse/specpulse/issues)
- **GitHub Discussions**: [github.com/specpulse/specpulse/discussions](https://github.com/specpulse/specpulse/discussions)
- **GitHub Wiki**: [github.com/specpulse/specpulse/wiki](https://github.com/specpulse/specpulse/wiki)
- **GitHub Releases**: [github.com/specpulse/specpulse/releases](https://github.com/specpulse/specpulse/releases)

### Getting Help

```bash
# Show available help topics
specpulse help --list

# Get help on specific topics
specpulse help ai_integration
specpulse help workflow
specpulse help templates

# Get contextual help
specpulse ai suggest --query "help"
```

### Reporting Issues

When reporting issues, please include:

1. **System Information**: Operating system, Python version, SpecPulse version
2. **Error Messages**: Full error output and stack traces
3. **Steps to Reproduce**: Clear steps to reproduce the issue
4. **Expected vs Actual**: What you expected vs what actually happened

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and development setup instructions.

---

**🎉 Congratulations! You now have a complete understanding of SpecPulse v2.0.0's AI integration capabilities. Build better software, faster, with intelligent AI assistance!**