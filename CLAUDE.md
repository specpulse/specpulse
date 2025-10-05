# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SpecPulse is a Python CLI tool (Python 3.11+) that enables Specification-Driven Development for ANY software project. It generates AI commands for Claude and Gemini, manages project templates, and enforces development principles through validation.

## Development Commands

### Testing
```bash
# Run all tests with coverage
pytest tests/ --cov=specpulse --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py -v

# Run a single test function
pytest tests/test_cli.py::TestCLI::test_init_command -v

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
# Or use the shorthand
sp --help
```

### CLI Commands
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

# Get help on various topics
python -m specpulse.cli.main help --list
python -m specpulse.cli.main help workflow
```

## Architecture Overview

SpecPulse is a universal Specification-Driven Development (SDD) framework that works with ANY software project type - web apps, mobile apps, desktop software, games, APIs, ML projects, and more.

### Core Components

1. **CLI Layer** (`specpulse/cli/main.py`)
   - Entry point: `SpecPulseCLI` class
   - Commands: init, validate, doctor, sync, decompose
   - Rich console output with animations and progress bars

2. **Core Engine** (`specpulse/core/specpulse.py`)
   - `SpecPulse` class: Template management and project initialization
   - Handles resource copying, command generation, and project structure

3. **Validator** (`specpulse/core/validator.py`)
   - `Validator` class: Validates specs, plans, and SDD compliance
   - Enforces 9 universal development principles (see below)
   - Phase gates system for quality control

4. **Utilities** (`specpulse/utils/`)
   - `Console` (`console.py`): Rich terminal output with tables, animations, and color coding
   - `GitUtils` (`git_utils.py`): Git integration for version control

5. **Resources** (`specpulse/resources/`)
   - `templates/`: Jinja2 template files (spec.md, plan.md, task.md, decomposition/)
   - `scripts/`: Bash (.sh) and PowerShell (.ps1) scripts for AI execution
   - `commands/`: AI command definitions (claude/*.md, gemini/*.toml)
   - `memory/`: Default memory files (constitution.md, context.md, decisions.md)

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
│   ├── constitution.md  # 9 universal SDD principles
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

### Universal SDD Principles

All development follows 9 universal principles for Specification-Driven Development:
1. **Specification First**: Every feature starts with clear requirements and acceptance criteria
2. **Incremental Planning**: Break work into phased, valuable increments
3. **Task Decomposition**: Create concrete, executable tasks with clear outcomes
4. **Traceable Implementation**: Link every piece of code to specifications
5. **Continuous Validation**: Regularly verify implementation matches specs
6. **Quality Assurance**: Ensure quality through appropriate testing strategies
7. **Architecture Documentation**: Record and justify technical decisions
8. **Iterative Refinement**: Evolve specs and implementation based on learnings
9. **Stakeholder Alignment**: Maintain shared understanding through clear specs

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

## Directory Structure and Script Execution

### How Scripts Work
When AI executes commands like `/sp-pulse`, `/sp-spec`, etc., the following happens:

1. **Script Location**: Scripts are copied to `project-root/scripts/`
2. **Script Execution**: `bash scripts/sp-pulse-init.sh [arguments]`
3. **Project Root Detection**: Scripts automatically detect project root as parent of scripts/ directory

### Directory Layout
```
project-root/                    # User's project directory
├── scripts/                     # Shell scripts (copied from SpecPulse)
│   ├── sp-pulse-init.sh
│   ├── sp-pulse-spec.sh
│   ├── sp-pulse-plan.sh
│   └── sp-pulse-task.sh
├── templates/                   # Template files (MUST have these exact names)
│   ├── spec.md                 # NOT spec-001.md
│   ├── plan.md                 # NOT plan-001.md
│   └── task.md                 # Correct name
├── specs/
│   └── 001-feature-name/       # Feature directory
│       ├── spec-001.md         # First specification
│       └── spec-002.md         # Updated specification
├── plans/
│   └── 001-feature-name/       # Same feature directory name
│       └── plan-001.md         # Implementation plan
└── tasks/
    └── 001-feature-name/       # Same feature directory name
        └── task-001.md         # Task breakdown
```

### Script Arguments
- `/sp-pulse user-auth` → `bash scripts/sp-pulse-init.sh "user-auth"`
- `/sp-spec` → `bash scripts/sp-pulse-spec.sh "001-user-auth"`
- `/sp-plan` → `bash scripts/sp-pulse-plan.sh "001-user-auth"`
- `/sp-task` → `bash scripts/sp-pulse-task.sh "001-user-auth"`

The feature directory name (e.g., "001-user-auth") is passed to spec, plan, and task scripts.

## Tiered Templates (v1.6.0+)

### Using Tiered Templates

When creating specs, use the appropriate tier based on feature complexity:

- `/sp-pulse feature-name` - Creates minimal tier by default (quickest start)
- For simple features: stay at minimal tier (3 sections, 2-3 minutes)
- For features needing plans: expand to standard tier (7 sections, ready for implementation)
- For complex/production features: expand to complete tier (15 sections, production-ready)

### Tier Expansion Workflow

```bash
# 1. Start minimal
/sp-pulse user-authentication

# 2. Fill out minimal spec (What, Why, Done When)
# LLM fills in basic details

# 3. Expand when ready for implementation
specpulse expand 001 --to-tier standard

# 4. Fill out standard sections (User Stories, Requirements, etc.)
# LLM adds implementation details

# 5. Expand to complete for production
specpulse expand 001 --to-tier complete

# 6. Fill out comprehensive sections (Security, Performance, etc.)
# LLM adds production details
```

### LLM Guidance in Templates

Each template tier has `<!-- LLM GUIDANCE: ... -->` comments:
- **Minimal tier**: "Keep it minimal - just the essence"
- **Standard tier**: "Provide enough detail for planning"
- **Complete tier**: "Comprehensive production-grade details"

Follow these guidance comments when filling out templates. They tell you:
- What to write in each section
- How much detail is needed
- What format to use (bullet points, paragraphs, etc.)
- Suggested length (1 sentence, 2-3 items, etc.)

### Content Preservation

**IMPORTANT**: When expanding tiers, ALL user content is preserved:
- Existing sections keep their content
- New sections are added with template placeholders
- Nothing is lost or overwritten
- Backups are created automatically

### Template Tier Reference

| Tier | Sections | Use Case | Time to Complete |
|------|----------|----------|------------------|
| **Minimal** | 3 | Quick prototypes, simple features | 2-3 minutes |
| **Standard** | 7-8 | Most features, implementation planning | 10-15 minutes |
| **Complete** | 15+ | Production features, complex systems | 30-45 minutes |

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
- Current version: 1.5.0 (in `specpulse/_version.py`)
- Version is defined ONLY in `specpulse/_version.py`
- All other files read from this single source of truth
- Use semantic versioning for releases
- When updating version: modify only `specpulse/_version.py`

### Resource Handling
- Templates and scripts are copied from `specpulse/resources/`
- Resource structure mirrors project structure (templates/, scripts/, commands/, memory/)
- Never modify files in `.claude/` or `.gemini/` after initialization
- Templates in `templates/` are editable by users BUT filenames must stay the same
- Scripts in `scripts/` should remain executable
- Package data includes: .md, .yaml, .ts, .sh, .ps1, .toml files

### Testing Coverage
- 377+ tests with cross-platform CI/CD pipeline
- Use pytest with coverage reporting
- Mock external dependencies (Git, filesystem)
- Test files organized by component: `test_cli.py`, `test_core.py`, `test_validator.py`, etc.

### Console Features
- ASCII art banners for branding
- Progress bars for long operations
- Color-coded output (success=green, error=red, warning=yellow)
- Tables for structured data display
- Pulse animations for visual feedback

### Dependencies
Key external libraries (see pyproject.toml for full list):
- `click>=8.0` - CLI framework
- `rich>=13.0` - Rich terminal output
- `jinja2>=3.0` - Template rendering
- `gitpython>=3.1` - Git integration
- `pyyaml>=6.0` - YAML parsing
- `toml>=0.10` - TOML parsing

### Entry Points
The package provides two CLI entry points:
- `specpulse` - Main command
- `sp` - Shorthand alias

Both execute `specpulse.cli.main:main`