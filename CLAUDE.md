# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
```bash
# Run all tests with coverage
pytest tests/ --cov=specpulse --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py -v

# Run with coverage report
pytest tests/ --cov=specpulse --cov-report=term-missing

# Run tests without coverage (faster)
pytest tests/ -v
```

### Code Quality
```bash
# Format code with black
black specpulse/ tests/

# Lint with flake8
flake8 specpulse/ tests/

# Type checking with mypy
mypy specpulse/

# Run all quality checks
black specpulse/ tests/ && flake8 specpulse/ tests/ && mypy specpulse/
```

### Build and Package
```bash
# Build package
python -m build

# Install in development mode
pip install -e .

# Run CLI locally
python -m specpulse.cli.main --help
```

### CLI Testing
```bash
# Test CLI commands
python -m specpulse.cli.main init test-project --here
python -m specpulse.cli.main validate
python -m specpulse.cli.main doctor
python -m specpulse.cli.main sync
```

## Architecture Overview

### Core Components
1. **CLI Layer** (`specpulse/cli/`) - Command-line interface with rich output
2. **Core Engine** (`specpulse/core/`) - Main business logic and template management
3. **Utilities** (`specpulse/utils/`) - Helper modules for console, git, etc.
4. **Resources** (`specpulse/resources/`) - Templates, commands, and memory files

### Key Classes
- `SpecPulseCLI` - Main CLI interface, handles all user commands
- `SpecPulse` - Core engine, manages templates and project state
- `Validator` - Validates project components against constitution
- `Console` - Rich console output with animations and tables

### AI Command Integration
The framework generates AI command files in two formats:
- **Claude**: Markdown files with YAML frontmatter (`.claude/commands/*.md`)
- **Gemini**: TOML files with simple format (`.gemini/commands/*.toml`)

Both use the same command structure but handle arguments differently:
- Claude: `$ARGUMENTS` variable passed to shell scripts
- Gemini: `{{args}}` placeholder in prompts

### Project Structure Philosophy
SpecPulse follows a specification-first approach with these key directories:
- `specs/` - Feature specifications with numbered folders (001-feature, 002-feature)
- `plans/` - Implementation plans derived from specs
- `tasks/` - Task breakdowns from plans
- `memory/` - Persistent project state (constitution, context, decisions)
- `templates/` - Customizable document templates
- `scripts/` - Shell scripts for AI execution

### Constitutional Development
All development follows 9 immutable principles defined in `memory/constitution.md`:
- Library-First Principle
- CLI Interface Mandate
- Test-First Imperative
- Specification as Source of Truth
- And more...

### Phase Gates System
Before implementation, features must pass constitutional checks:
- Simplicity validation (≤3 modules)
- Test strategy definition
- Framework selection
- Research completion

## Important File Locations

### Templates and Resources
- `specpulse/resources/templates/` - Default templates copied to projects
- `specpulse/resources/memory/` - Default constitution and memory files
- `specpulse/resources/commands/` - AI command definitions

### Configuration
- `pyproject.toml` - Build configuration, version 1.0.4
- `setup.py` - Alternative setup configuration (synced with pyproject.toml)
- `.gitignore` - Excludes build artifacts, cache, and test coverage

### Testing
- `tests/` - Comprehensive test suite with 95% coverage
- `test-*/` - Example projects for integration testing

## Development Notes

### Version Management
- Current version: 1.0.4 (defined in pyproject.toml)
- Version must be kept in sync between pyproject.toml and setup.py
- CHANGELOG.md tracks version changes and release dates

### Console Output
The framework uses rich console output with:
- ASCII art banners
- Progress indicators
- Color-coded status messages
- Animated celebrations
- Interactive tables

### Template System
Templates are generated dynamically and can be customized:
- Specification templates follow a structured format with [NEEDS CLARIFICATION] markers
- Plan templates include architecture sections and phase breakdowns
- Task templates use T[XXX] numbering with complexity estimates

### Shell Script Integration
AI commands execute shell scripts in the project's `scripts/` directory:
- `sp-pulse-init.sh` - Feature initialization
- `sp-pulse-spec.sh` - Specification creation
- `sp-pulse-plan.sh` - Plan generation
- `sp-pulse-task.sh` - Task breakdown

Scripts receive arguments via `$ARGUMENTS` (Claude) or `{{args}}` (Gemini).