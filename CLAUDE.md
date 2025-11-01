# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SpecPulse v2.1.2 is an AI-Enhanced Specification-Driven Development (SDD) Framework distributed as a Python CLI package. It enables specification-first development with AI assistance through Claude Code and Gemini CLI.

## 🔴 CRITICAL: LLM Workflow Rules (v2.1.2+)

**PRIMARY WORKFLOW HIERARCHY:**

1. **FIRST: Try CLI Command** (if exists)
   ```bash
   specpulse feature init <name>
   specpulse spec create "<description>"
   specpulse plan create "<description>"
   specpulse task breakdown <plan-id>
   specpulse validate <type>
   ```

2. **SECOND: File Operations** (if CLI doesn't exist or doesn't cover operation)
   - READ templates from `.specpulse/templates/`
   - WRITE/EDIT files in `.specpulse/specs/`, `.specpulse/plans/`, `.specpulse/tasks/`, `.specpulse/memory/`

3. **NEVER: Direct edits to protected directories**
   - ❌ `.specpulse/templates/` - Read-only template source
   - ❌ `.specpulse/` - Internal configuration
   - ❌ `specpulse/` - Package code
   - ❌ `.claude/` and `.gemini/` - AI command definitions

**Key Design Philosophy**: CLI-first architecture where AI assistants MUST try CLI commands before using file operations. The CLI handles metadata, validation, and structure creation. File operations are used ONLY when CLI doesn't provide the functionality.

## Essential Commands

### Development Environment

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest                           # All tests
pytest tests/test_cli.py        # Specific test file
pytest -k "test_name"           # Specific test pattern
pytest --cov=specpulse          # With coverage

# Code quality
black specpulse/                # Format code (max line 100)
flake8 specpulse/               # Linting
mypy specpulse/                 # Type checking

# Build and distribution
python setup.py sdist bdist_wheel
pip install dist/specpulse-*.whl

# Version management
# Edit specpulse/_version.py to change version
```

### Testing the CLI

```bash
# Test CLI commands directly
specpulse --help
specpulse init test-project --ai claude
specpulse doctor

# Test in a temporary project
cd /tmp
specpulse init testproj --here --ai claude
cd testproj
specpulse feature init user-auth
```

## Architecture

### Core Design Principle: CLI First > File Operations (v2.1.2+)

**Critical Understanding**: In AI-assisted workflows, Claude Code should ALWAYS try CLI commands FIRST. File operations are used ONLY when CLI doesn't exist or doesn't cover the specific operation.

#### Workflow Pattern (v2.1.2+)
```
User in Claude Code: /sp-spec OAuth2 login with JWT
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

**Why CLI First?**
- CLI handles metadata automatically (timestamps, IDs, status)
- CLI validates structure before creating files
- CLI updates context.md consistently
- CLI provides error handling and recovery
- File Operations are fallback for flexibility

### Directory Structure

```
specpulse/
├── cli/                    # CLI entry points
│   ├── main.py            # Main CLI orchestration (SpecPulseCLI class)
│   ├── feature_commands.py # Feature init/continue commands (v2.1.0)
│   ├── spec_commands.py    # Spec create/update/validate (v2.1.0)
│   └── plan_task_commands.py # Plan/Task/Execute commands (v2.1.0)
├── core/                   # Core business logic
│   ├── specpulse.py       # Main SpecPulse class
│   ├── validator.py       # Specification validation
│   ├── template_manager.py # Template handling
│   ├── memory_manager.py  # Context/memory tracking
│   ├── checkpoints.py     # Checkpoint system
│   └── ai_integration.py  # AI context detection
├── utils/                  # Utilities
│   ├── console.py         # Rich console output
│   ├── error_handler.py   # Error handling & recovery
│   ├── git_utils.py       # Git integration
│   └── version_check.py   # PyPI version checking
├── resources/             # Bundled resources (installed with package)
│   ├── commands/
│   │   ├── claude/*.md    # Claude Code slash commands
│   │   └── gemini/*.toml  # Gemini CLI commands
│   ├── .specpulse/templates/         # Specification templates (spec.md, plan.md, task.md)
│   └── .specpulse/memory/            # Memory templates
└── models/                # Data models
    └── project_context.py # Project context model
```

### Key Components

**SpecPulse Class** (`core/specpulse.py`):
- Core functionality and configuration management
- Template loading from bundled resources
- Resource directory resolution (handles installed package vs dev)

**CLI Classes** (`cli/*.py`):
- `SpecPulseCLI`: Main entry point with error handling
- `FeatureCommands`: Feature initialization and context switching
- `SpecCommands`: Specification creation and validation
- `PlanCommands`, `TaskCommands`, `ExecuteCommands`: Plan/Task workflow

**Template System**:
- Templates stored in `resources/templates/`
- Copied to project on `specpulse init`
- AI expands templates using metadata markers
- User-customizable after initialization

### Metadata System

All generated files (specs, plans, tasks) contain HTML comment metadata:

```markdown
<!-- FEATURE_DIR: 001-user-auth -->
<!-- FEATURE_ID: 001 -->
<!-- STATUS: pending -->
<!-- CREATED: 2025-10-07T12:00:00 -->
```

This enables:
- Machine-readable tracking
- Easy parsing by LLMs
- No external database needed
- Self-contained files

## Working with Custom Slash Commands

The project includes 8 custom slash commands in `.claude/commands/` and `.gemini/commands/`:

- `/sp-pulse` - Initialize new feature with full structure
- `/sp-spec` - Create/update/validate specifications
- `/sp-plan` - Generate implementation plans
- `/sp-task` - Break down into tasks
- `/sp-execute` - Execute tasks continuously (non-stop mode)
- `/sp-continue` - Switch context to existing feature
- `/sp-status` - Track progress across features
- `/sp-decompose` - Decompose specs into microservices

**Important**: Slash commands instruct Claude to use **file operations**, not CLI commands.

### Example: How /sp-spec Works

1. Claude reads `.specpulse/templates/spec.md`
2. Claude writes new file to `.specpulse/specs/001-feature/spec-XXX.md`
3. Claude edits that file to expand it with full specification
4. Optionally: Run `specpulse validate spec` for verification

**Never** edit files in `.specpulse/templates/`, `.claude/`, `.gemini/`, or `scripts/` folders.

## Testing Strategy

### Test Structure

```
tests/
├── test_cli.py              # CLI command tests
├── test_specpulse.py        # Core functionality tests
├── test_validator.py        # Validation tests
├── test_template_manager.py # Template system tests
├── test_memory_manager.py   # Memory/context tests
├── conftest.py              # Pytest fixtures
└── integration/
    ├── test_v170_workflow.py
    └── test_v180_workflow.py
```

### Running Tests

- Use `pytest` fixtures from `conftest.py` for temporary directories
- Tests should be isolated and not affect each other
- Mock external dependencies (git, network)
- Test both CLI interface and direct class usage

## Version Management

**Version Location**: `specpulse/_version.py`

```python
__version__ = "2.1.1"
```

**Version Checking**:
- `utils/version_check.py` checks PyPI for updates
- Non-blocking, 1-second timeout
- Only shows on `init` and `--version` commands

## Error Handling

The `utils/error_handler.py` module provides:
- Custom exception classes (`SpecPulseError`, `ValidationError`, etc.)
- Recovery suggestions for common errors
- User-friendly error messages
- Severity levels (INFO, WARNING, ERROR, CRITICAL)

**Pattern**:
```python
from specpulse.utils.error_handler import ErrorHandler, ValidationError

try:
    # Operation
    pass
except Exception as e:
    raise ValidationError(f"Validation failed: {e}")
```

## Building and Distribution

### Package Structure

- `pyproject.toml` - Modern Python packaging config
- `setup.py` - Fallback/compatibility setup
- `MANIFEST.in` - Include non-Python files

### Resource Files

Resources are bundled with the package and installed to site-packages:

```python
[tool.setuptools.package-data]
specpulse = [
    "resources/templates/*.md",
    "resources/commands/claude/*.md",
    "resources/commands/gemini/*.toml",
    # ...
]
```

### Building

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution
python setup.py sdist bdist_wheel

# Install locally for testing
pip install dist/specpulse-*.whl
```

## AI Integration Principles

### Privacy-First Design

- **No external API calls** from the CLI
- All processing is local
- LLM interactions happen through Claude Code/Gemini CLI (user controls)
- No data transmission to SpecPulse servers

### LLM-Optimized Templates

Templates use:
- Jinja2-style variable markers: `{{ feature_name }}`
- AI instruction comments: `<!-- AI: Fill this section -->`
- Structured sections for easy parsing
- `[NEEDS CLARIFICATION]` markers for uncertainties

### Context Detection

The `core/ai_integration.py` module provides:
- Auto-detect current feature from git branch
- Parse `.specpulse/memory/context.md` for active feature
- Suggest next steps based on project state

## Common Development Patterns

### Adding a New CLI Command

1. Add method to appropriate command class in `cli/`
2. Register in `cli/main.py` parser
3. Add tests in `tests/test_cli.py`
4. Update help documentation

### Modifying Templates

1. Edit files in `specpulse/resources/templates/`
2. Test with `specpulse init` to verify copying works
3. Ensure AI instruction comments are clear
4. Update validation rules if structure changes

### Adding Validation Rules

1. Edit `core/validator.py` or `core/validation_rules.py`
2. Add corresponding tests
3. Update error messages to be actionable
4. Document in template comments

## Git Integration

SpecPulse uses git for:
- Feature branch naming: `001-feature-name`
- Context detection from current branch
- Auto-checkout on `feature init`
- Status tracking in `sp-status`

**Git Utilities** (`utils/git_utils.py`):
- Branch creation and switching
- Feature ID extraction from branch names
- Repository validation

## Cross-Platform Considerations

- Use `pathlib.Path` for all file paths
- Avoid shell-specific commands in CLI
- Test on Windows, macOS, and Linux
- Use `os.path` fallbacks where needed

## Migration Notes (v2.0 → v2.1)

**Breaking Changes**:
- Removed `scripts/` folder (replaced with CLI commands)
- Slash commands now call CLI directly instead of shell scripts
- No data migration needed - backward compatible with v2.0 projects

**What Changed**:
- Faster execution (~3x) - no shell overhead
- Cross-platform - pure Python
- Smaller projects (~50KB less without scripts)

## Code Style

- **Line length**: 100 characters (Black config)
- **Python version**: 3.11+ required
- **Type hints**: Use where helpful, mypy validation
- **Docstrings**: Google style for public APIs
- **Comments**: Explain "why", not "what"

## Documentation Files

- `README.md` - User-facing quickstart and features
- `ARCHITECTURE.md` - Detailed system architecture
- `CHANGELOG.md` - Version history and changes
- `docs/` - Comprehensive guides (installation, migration, troubleshooting, AI integration)
