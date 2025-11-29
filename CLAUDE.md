# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SpecPulse v2.7.1** is an AI-Enhanced Specification-Driven Development Framework that enables structured development with AI assistance across 8 major AI platforms. It combines CLI-first reliability with AI enhancement for specification-driven development.

## Architecture

### Core Framework Structure
- **CLI-First Architecture**: All operations work through reliable CLI commands with AI enhancement as a secondary layer
- **Service-Oriented Design**: Refactored from monolithic to service-oriented architecture with dependency injection
- **Multi-Platform AI Integration**: Unified interface supporting Claude Code, Gemini CLI, Windsurf, Cursor, GitHub Copilot, OpenCode, Crush, and Qwen Code
- **Template-Based Generation**: Uses Jinja2 templates for consistent file generation
- **Memory Management**: Maintains project context, decisions, and learning history
- **Task Monitoring**: Real-time progress tracking with comprehensive analytics

### Key Components
- **`specpulse/core/specpulse.py`**: Main orchestrator (refactored from 1400+ lines to ~300 lines)
- **`specpulse/core/memory_manager.py`**: Project context and decision tracking (44KB)
- **`specpulse/core/template_manager.py`**: Template system and content generation (25KB)
- **`specpulse/monitor/`**: Complete task monitoring and progress tracking system
- **`specpulse/cli/`**: Command-line interface with handlers and parsers
- **`specpulse/resources/commands/`**: AI platform command templates for all 8 platforms

## Development Commands

### Installation and Setup
```bash
# Development installation
pip install -e ".[dev]"

# Standard installation
pip install specpulse

# Verify installation
specpulse --version
```

### Core CLI Commands
```bash
# Project management
specpulse init <project-name> --ai <platform>    # Initialize new project
specpulse doctor                                   # Health check
specpulse doctor --fix                            # Auto-fix issues

# Feature development
specpulse feature init <feature-name>             # Initialize new feature
specpulse feature continue <feature-id>           # Switch to existing feature
specpulse feature current                         # Show current feature
specpulse feature list                            # List all features

# Specification management
specpulse spec create <description>               # Create specification
specpulse spec validate <spec-id>                 # Validate specification
specpulse spec list                               # List specifications

# Planning and execution
specpulse plan create <description>               # Create implementation plan
specpulse task breakdown <plan-id>                # Break plan into tasks
specpulse task list                               # List tasks

# Task monitoring (NEW in v2.7.1)
specpulse monitor status                          # Show comprehensive progress
specpulse monitor progress                        # Progress analytics
specpulse monitor history                         # Task completion history
```

### AI Platform Commands (Works on all 8 platforms)
```bash
# These commands work identically across ALL AI platforms:
/sp-pulse <feature-name>          # Initialize new feature - PRIMARY ENTRY POINT
/sp-spec "<description>"           # Create specification
/sp-plan                           # Generate implementation plan
/sp-task                           # Break down into tasks
/sp-execute [task-id|all]          # Execute tasks
/sp-status                         # Check progress
/sp-validate                      # Validate work
/sp-continue <feature-id>          # Switch to existing feature
/sp-decompose <spec-id>            # Decompose specifications
/sp-clarify <spec-id>              # Clarify requirements
/sp-llm-enforce [action]           # LLM compliance enforcement
```

**🎯 IMPORTANT: Always start with `/sp-pulse` - this is your entry point to everything!**

## Testing

### Test Structure
```bash
# Run comprehensive test suite
pytest tests/

# Run with coverage
pytest --cov=specpulse --cov-report=html

# Run specific test categories
pytest tests/ -m unit              # Unit tests only
pytest tests/ -m integration       # Integration tests only
pytest tests/ -m performance       # Performance tests only
pytest tests/ -m security          # Security tests only

# Monitor-specific tests
pytest tests/monitor/              # Task monitoring tests
```

### Multi-Environment Testing with Tox
```bash
# Test across Python 3.11, 3.12, 3.13
tox

# Specific environments
tox -e py311                       # Python 3.11 tests
tox -e flake8                      # Linting
tox -e black                       # Code formatting
tox -e mypy                        # Type checking
tox -e coverage                    # Coverage report
tox -e all                         # All quality checks + tests
```

### Code Quality Standards
- **Coverage Target**: 90%+ code coverage
- **Formatting**: Black with 100-character line limit
- **Linting**: Flake8 (E203, W503 ignored)
- **Type Checking**: MyPy with strict mode
- **Security**: Bandit for security scanning, Safety for dependency checks

## Development Workflow

### Project Initialization
1. **Create New Project**: `specpulse init my-project --ai claude`
2. **Project Structure**: Creates `.specpulse/` directory with organized structure
3. **AI Integration**: Auto-deploys platform-specific commands (`.claude/`, `.gemini/`, etc.)
4. **Git Setup**: Initializes git repository with proper .gitignore

### Feature Development Workflow
1. **Initialize Feature**: `/sp-pulse feature-name` - THE WAY TO START EVERYTHING
2. **Create Specification**: `/sp-spec "description"` - AI generates comprehensive specs
3. **Generate Plan**: `/sp-plan` - AI creates detailed implementation plan
4. **Break into Tasks**: `/sp-task` - AI creates actionable tasks with dependencies
5. **Execute Tasks**: `/sp-execute all` - Continuous task execution
6. **Monitor Progress**: `/sp-status` - Real-time progress tracking

**Note**: You can still use CLI commands like `specpulse feature init feature-name` but the AI approach with `/sp-pulse` is recommended as it sets up everything including AI command integration.

### File Organization
```
your-project/
├── .specpulse/                     # All project data (git-tracked)
│   ├── specs/                      # Feature specifications
│   ├── plans/                      # Implementation plans
│   ├── tasks/                      # Development tasks
│   ├── memory/                     # Project context and decisions
│   └── templates/                  # Customizable templates
├── .claude/                        # Claude Code commands (auto-deployed)
├── .gemini/                        # Gemini CLI commands
├── .windsurf/                      # Windsurf AI workflows
└── your-project-files/             # Your actual code
```

## Important Implementation Details

### Service Architecture (Refactored)
The codebase has been refactored from a monolithic design to a clean service-oriented architecture:

- **`ServiceContainer`**: Dependency injection container
- **`TemplateProvider`**: Template management service
- **`MemoryProvider`**: Project memory and context service
- **`ScriptGenerator`**: Code generation service
- **`DecompositionService`**: Specification decomposition service
- **`AIInstructionProvider`**: AI platform instruction service

### CLI-First with AI Enhancement Pattern
SpecPulse uses a unique "CLI-First with AI Enhancement" approach:
1. **CLI Creates Foundation**: Reliable commands that always work
2. **AI Enhances Content**: AI adds detailed specifications and implementations
3. **Fallback Protection**: Work continues even if AI fails
4. **Platform Independence**: Works identically across all platforms

### Version Management
- **Single Source of Truth**: `specpulse/_version.py` contains version only
- **Current Version**: 2.7.1
- **Update Process**: Modify `_version.py` only, all other files import from it

### Security Considerations
- **Privacy-First**: No external API calls, all processing local
- **Protected Directories**: Never edit `templates/`, `.specpulse/`, `specpulse/` directly
- **Input Validation**: Comprehensive input sanitization
- **Path Protection**: Protected against directory traversal attacks

## AI Platform Integration

### Supported Platforms (8 Total)
- **Claude Code**: Custom slash commands (`.claude/sp-*.md`)
- **Gemini CLI**: Custom commands (`.gemini/sp-*.toml`)
- **Windsurf**: Custom slash commands
- **Cursor**: Custom slash commands
- **GitHub Copilot**: Custom prompts (`.github/prompts/sp-*.prompt.md`)
- **OpenCode**: Agent-based workflow
- **Crush**: Category commands
- **Qwen Code**: TOML configuration

### Command Deployment
Commands are auto-deployed during project initialization:
```bash
specpulse init my-project --ai claude    # Deploys Claude commands
specpulse init --here --ai gemini       # Deploys Gemini commands in existing project
```

## Troubleshooting

### Common Issues
```bash
# Command not found
pip show specpulse                       # Verify installation
python -m specpulse --version           # Check version

# AI commands not working
specpulse doctor --fix                   # Fix integration issues

# File permission errors
chmod 755 .specpulse/                   # Fix permissions

# Git integration problems
git init                                 # Initialize git repository
```

### Debug Mode
```bash
export SPECPULSE_DEBUG=1                # Enable debug mode
set SPECPULSE_DEBUG=1                   # Windows
```

### Debug File Locations
- **Logs**: `.specpulse/logs/debug.log`
- **Cache**: `.specpulse/cache/`
- **Temp**: `.specpulse/tmp/`

## Key Files to Understand

### Core Architecture
- **`specpulse/core/specpulse.py`**: Main orchestrator (service-oriented design)
- **`specpulse/cli/main.py`**: CLI entry point with UTF-8 Windows support
- **`specpulse/_version.py`**: Single source of truth for version

### Services and Interfaces
- **`specpulse/core/interfaces.py`**: Service interface definitions
- **`specpulse/core/service_container.py`**: Dependency injection container
- **`specpulse/core/template_provider.py`**: Template management service

### Monitoring System
- **`specpulse/monitor/models.py`**: Task monitoring data models
- **`specpulse/monitor/state_manager.py`**: Task state management
- **`specpulse/monitor/calculator.py`**: Progress calculation algorithms

### AI Commands
- **`specpulse/resources/commands/claude/`**: Claude Code slash command templates
- **`specpulse/resources/commands/gemini/`**: Gemini CLI TOML configurations
- **`specpulse/resources/commands/README.md`**: AI platform integration guide

This framework represents a mature, well-architected approach to AI-enhanced software development with strong testing practices, comprehensive documentation, and cross-platform compatibility.