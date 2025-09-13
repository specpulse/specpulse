# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
```bash
# Run all tests with coverage
pytest tests/ --cov=specpulse --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py -v

# Run tests without coverage (faster)
pytest tests/ -v

# Run a single test function
pytest tests/test_cli.py::TestCLI::test_init_command -v
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

# Or use the shorthand
sp --help
```

### CLI Testing
```bash
# Initialize a new project
python -m specpulse.cli.main init test-project
python -m specpulse.cli.main init --here  # In current directory

# Validate project
python -m specpulse.cli.main validate

# Run diagnostics
python -m specpulse.cli.main doctor

# Sync project state
python -m specpulse.cli.main sync

# Decompose a specification
python -m specpulse.cli.main decompose 001
```

## Architecture Overview

SpecPulse is a specification-driven development framework that enforces a structured approach to software development through AI integration and constitutional principles.

### Core Components

1. **CLI Layer** (`specpulse/cli/main.py`)
   - Entry point: `SpecPulseCLI` class
   - Commands: init, validate, doctor, sync, decompose
   - Rich console output with animations and progress bars

2. **Core Engine** (`specpulse/core/specpulse.py`)
   - `SpecPulse` class: Template management and project initialization
   - Handles resource copying, command generation, and project structure

3. **Validator** (`specpulse/core/validator.py`)
   - `Validator` class: Validates specs, plans, and constitutional compliance
   - Enforces 9 immutable development principles
   - Phase gates system for quality control

4. **Utilities** (`specpulse/utils/`)
   - `Console`: Rich terminal output with tables, animations, and color coding
   - `GitUtils`: Git integration for version control

### AI Command System

The framework generates AI commands in two formats:

**Claude** (`.claude/commands/*.md`):
- Markdown files with YAML frontmatter
- Arguments passed via `$ARGUMENTS` to shell scripts
- Example: `/sp-pulse feature-name` → executes `scripts/sp-pulse-init.sh`

**Gemini** (`.gemini/commands/*.toml`):
- TOML configuration files
- Arguments interpolated via `{{args}}` placeholder
- Same command structure as Claude

### Project Structure Philosophy

```
project/
├── specs/           # Feature specifications (001-feature/)
├── plans/           # Implementation plans (derived from specs)
├── tasks/           # Task breakdowns (T001, T002 or SERVICE-T001)
├── memory/          # Persistent state
│   ├── constitution.md  # 9 immutable principles
│   ├── context.md      # Current project state
│   └── decisions.md    # Architecture Decision Records
├── templates/       # Customizable document templates
└── scripts/         # Shell scripts for AI execution
```

### Microservice Decomposition

For complex specifications, the framework supports automatic decomposition:
- Creates service boundaries using Domain-Driven Design
- Generates API contracts (OpenAPI 3.0)
- Service-specific plans and tasks (AUTH-T001, USER-T001)
- Integration plans for service communication

### Constitutional Principles

All development follows 9 immutable articles:
1. **Library-First**: Every feature must be modular
2. **CLI Interface**: Text-based interaction only
3. **Test-First**: Tests before implementation
4. **Specification as Source**: Specs drive all development
5. **Direct Framework Usage**: No unnecessary abstractions
6. **No Abstraction Layers**: Simplicity over complexity
7. **Simplicity Enforcement**: ≤3 modules per feature
8. **Complexity Tracking**: Document exceptions
9. **Framework-First**: Use existing solutions

### Template System

Templates use Jinja2 for dynamic generation:
- Specification templates include `[NEEDS CLARIFICATION]` markers
- Plan templates have architecture and phase sections
- Task templates use complexity estimates (Simple/Medium/Complex)
- Decomposition templates for microservices and APIs

### Shell Script Integration

All AI commands execute Bash scripts:
- `sp-pulse-init.sh`: Initialize features
- `sp-pulse-spec.sh`: Create specifications
- `sp-pulse-plan.sh`: Generate plans
- `sp-pulse-task.sh`: Break down tasks
- `sp-pulse-decompose.sh`: Decompose into microservices
- `sp-pulse-execute.sh`: Execute tasks continuously

Scripts work cross-platform (Git Bash on Windows, native on Linux/macOS).

### Continuous Task Execution

The `/sp-execute` command enables non-stop task completion:

```bash
/sp-execute         # Execute next task and continue
/sp-execute all     # Execute ALL pending tasks without stopping
/sp-execute T001    # Start from specific task
```

**Key Features:**
- NO STOPPING between tasks
- NO EXPLANATIONS until all done
- NO CONFIRMATIONS needed
- Automatic progression through entire task list
- Only stops when all tasks completed or blocked

**Workflow Example:**
```bash
/sp-pulse new-feature       # Initialize
/sp-spec "description"      # Create spec
/sp-plan                    # Generate plan
/sp-task                    # Break down tasks
/sp-execute all            # Complete EVERYTHING!
```

This enables maximum efficiency by eliminating context switching and maintaining flow state.

## CRITICAL WORKFLOW RULES

### ⚠️ NEVER MODIFY TEMPLATE FILES
**ABSOLUTELY CRITICAL**: The files in `templates/` directory are TEMPLATES. They must NEVER be renamed or have their filenames changed:
- `templates/spec.md` - MUST always remain as `spec.md`
- `templates/plan.md` - MUST always remain as `plan.md`
- `templates/task.md` - MUST always remain as `task.md`

These are SOURCE TEMPLATES that get COPIED to the appropriate directories with proper naming.

### Correct Workflow Examples

#### 1. Feature Initialization (`/sp-pulse user-authentication`)
Creates the following structure:
```
specs/001-user-authentication/
  └── spec-001.md         (copied from templates/spec.md)
plans/001-user-authentication/
  └── plan-001.md         (copied from templates/plan.md)
tasks/001-user-authentication/
  └── task-001.md         (copied from templates/task.md)
```

#### 2. Specification Updates (`/sp-spec`)
- First spec: `specs/001-user-authentication/spec-001.md`
- Updates create: `spec-002.md`, `spec-003.md` etc.
- NEVER modifies `templates/spec.md`

#### 3. Decomposition (`/sp-decompose 001`)
Creates decomposition subdirectory:
```
specs/001-user-authentication/
  ├── spec-001.md
  └── decomposition/
      ├── microservices.md     (from templates/decomposition/microservices.md)
      ├── api-contracts/
      │   └── *.yaml           (from templates/decomposition/api-contract.yaml)
      └── interfaces/
          └── *.ts             (from templates/decomposition/interface.ts)
```

Then creates service-specific plans:
```
plans/001-user-authentication/
  ├── auth-service-plan.md    (from templates/decomposition/service-plan.md)
  ├── user-service-plan.md    (from templates/decomposition/service-plan.md)
  └── integration-plan.md     (from templates/decomposition/integration-plan.md)
```

And service-specific tasks:
```
tasks/001-user-authentication/
  ├── auth-service-tasks.md   (with AUTH-T001, AUTH-T002...)
  ├── user-service-tasks.md   (with USER-T001, USER-T002...)
  └── integration-tasks.md    (with INT-T001, INT-T002...)

### ❌ NEVER DO THIS
- NEVER rename `templates/spec.md` to `templates/spec-001.md`
- NEVER rename `templates/plan.md` to `templates/001-plan.md`
- NEVER edit filenames in `templates/` directory
- NEVER modify files in `.claude/` or `.gemini/` directories
- NEVER edit scripts in `scripts/` directory unless fixing bugs
- NEVER create files directly in `templates/` directory
- NEVER confuse template files with working files

### Protected vs Editable Directories
**Protected (Read-Only after init):**
- `templates/` - Original template files (spec.md, plan.md, task.md)
- `scripts/` - Shell scripts (sp-pulse-*.sh)
- `.claude/commands/` - Claude command definitions
- `.gemini/commands/` - Gemini command definitions

**Editable (Working directories):**
- `specs/XXX-feature/` - Feature specifications (spec-001.md, spec-002.md)
- `plans/XXX-feature/` - Implementation plans (plan-001.md, plan-002.md)
- `tasks/XXX-feature/` - Task breakdowns (task-001.md, task-002.md)
- `memory/` - Project state (context.md, decisions.md)

## Important Notes

### Version Management
- Current version: 1.3.1 (in `pyproject.toml`)
- Version must sync between `pyproject.toml` and `setup.py`
- Use semantic versioning for releases

### Resource Handling
- Templates and scripts are copied from `specpulse/resources/`
- Never modify files in `.claude/` or `.gemini/` after initialization
- Templates in `templates/` are editable by users BUT filenames must stay the same
- Scripts in `scripts/` should remain executable

### Testing Coverage
- Comprehensive test suite in `tests/`
- Multiple test files for complete coverage
- Use pytest with coverage reporting
- Mock external dependencies (Git, filesystem)

### Console Features
- ASCII art banners for branding
- Progress bars for long operations
- Color-coded output (success=green, error=red, warning=yellow)
- Tables for structured data display
- Pulse animations for visual feedback