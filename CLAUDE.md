# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install for development
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run single test file
pytest tests/unit/test_core/test_service_container.py -v

# Run single test function
pytest tests/unit/test_core/test_service_container.py::test_function_name -v

# Run by test category (markers: unit, integration, performance, security)
pytest tests/ -m unit
pytest tests/ -m integration

# Coverage report
pytest --cov=specpulse --cov-report=html tests/

# Lint check
flake8 specpulse/ tests/

# Format check (does NOT fix)
black --check specpulse/ tests/

# Format fix
black specpulse/ tests/

# Type check
mypy specpulse/

# Run all quality checks with tox
tox -e all
```

## Architecture Overview

### Service-Oriented Design with Dependency Injection

The codebase was refactored from a monolithic design to service-oriented architecture:

- **`specpulse/core/specpulse.py`**: Main orchestrator (~300 lines) - delegates to services, does not implement business logic directly
- **`specpulse/core/service_container.py`**: DI container for service registration and resolution
- **`specpulse/core/interfaces.py`**: Service interface definitions (ITemplateProvider, IMemoryProvider, etc.)

Key services injected into SpecPulse:

- `TemplateProvider` - Jinja2 template loading and rendering
- `MemoryProvider` - Project context, decisions, and learning history
- `ScriptGenerator` - Code/script generation
- `AIInstructionProvider` - AI platform-specific command generation
- `DecompositionService` - Specification decomposition

### CLI-First with AI Enhancement Pattern

SpecPulse uses a unique architectural pattern:

1. CLI commands create file structure and templates reliably
2. AI platforms enhance content by expanding templates
3. Fallback procedures exist when CLI fails (see `.specpulse/docs/AI_FALLBACK_GUIDE.md`)

### Multi-Platform AI Command System

Commands are generated for 8 AI platforms from templates in `specpulse/resources/commands/`:

- Claude Code: `.claude/commands/*.md`
- Gemini CLI: `.gemini/commands/*.toml`
- GitHub Copilot: `.github/prompts/*.prompt.md`
- Others: windsurf, cursor, opencode, crush, qwen

The `PathManager` class (`specpulse/core/path_manager.py`) enforces directory isolation between AI platforms.

### Version Management

Single source of truth: `specpulse/_version.py` - update version here only, all other files import from it.

## Key Patterns to Follow

### Test Fixtures

Tests use shared fixtures from `tests/conftest.py`:

- `temp_project_dir` - creates temporary `.specpulse/` structure
- `specpulse_instance` - pre-configured SpecPulse object
- `service_container` - DI container with mocked services
- `sample_spec_content`, `sample_plan_content`, `sample_task_content` - test data

### Error Handling

Custom exceptions in `specpulse/utils/error_handler.py`:

- `ValidationError` - validation failures
- `ProjectStructureError` - missing directories
- `ResourceError` - missing resources/templates

### Code Style

- Line length: 100 characters (Black + Flake8)
- Flake8 ignores: E203, W503
- MyPy: strict mode with `disallow_untyped_defs`
- Python target: 3.11+ (uses `importlib.resources.files`)
