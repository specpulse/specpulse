# SpecPulse - Specification-Driven Development (SDD) Framework

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/specpulse)

SpecPulse implements Specification-Driven Development (SDD) - a revolutionary methodology where specifications don't serve code, code serves specifications. The specification becomes the source of truth from which all implementation flows.

## The Nine Articles of SDD

1. **Library-First Principle** - Every feature begins as a standalone library
2. **CLI Interface Mandate** - All libraries expose text-based interfaces
3. **Test-First Imperative** - No code before tests (Red-Green-Refactor)
4. **Specification as Source of Truth** - Code serves specifications
5. **Continuous Refinement** - Ongoing validation and improvement
6. **Research-Driven Context** - Every decision backed by research
7. **Simplicity and Anti-Abstraction** - Maximum 3 modules, no over-engineering
8. **Integration-First Testing** - Real environments over mocks
9. **Executable Documentation** - All docs must be runnable

## Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/specpulse/specpulse.git
cd specpulse
pip install -e .
```

### Initialize Your Project

```bash
# Create a new SpecPulse project
specpulse init my-project

# With Git integration
specpulse init my-project --git

# With AI assistant integration
specpulse init my-project --ai claude
specpulse init my-project --ai gemini

```

## Project Structure

SpecPulse creates an organized project structure:

```
my-project/
├── .specpulse/          # Configuration
│   └── config.yaml      # Project settings
├── memory/              # Project memory
│   ├── constitution.md  # Core principles
│   ├── context.md       # Current state
│   └── decisions.md     # Architecture decisions
├── specs/               # Feature specifications
├── plans/               # Implementation plans
├── tasks/               # Task breakdowns
├── templates/           # Custom templates
└── scripts/             # Automation scripts
```

## Key SDD Features

### Phase Gates
Every implementation must pass constitutional gates before proceeding:
- **Simplicity Gate**: ≤3 modules, no future-proofing
- **Test-First Gate**: Tests written and failing before code
- **Integration-First Gate**: Real services, not mocks
- **Research Gate**: Decisions backed by analysis

### [NEEDS CLARIFICATION] Markers
Specifications explicitly mark uncertainties instead of making assumptions. Every ambiguity becomes a specific question for stakeholders.

### Complexity Tracking
Any deviation from simplicity principles requires documented justification with approval and future simplification plans.

## Core Features

### Persistent Memory System

Maintain project context across sessions:

- **Constitution**: Immutable project principles
- **Context**: Current state and progress
- **Decisions**: Documented architecture choices

### AI Assistant Integration

Seamless integration with AI tools:

```bash
# Claude integration
specpulse init --ai claude

# Gemini integration
specpulse init --ai gemini
```

Custom commands for each AI assistant are automatically configured.

### Validation

Validate and fix project structure:

```bash
# Validate everything
specpulse validate

# Auto-fix issues
specpulse validate --fix

# Validate specific components
specpulse validate --component spec
specpulse validate --component plan
specpulse validate --component constitution
```

### Git Synchronization

Keep your project synchronized:

```bash
# Sync project state with git
specpulse sync
```

### Self-Diagnostics

Run comprehensive diagnostics:

```bash
# Check project health
specpulse doctor
```

### Project Status

Track project progress:

```bash
# Get project status
specpulse status
```

## Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize new project |
| `validate` | Validate project structure |
| `sync` | Sync with git |
| `doctor` | Run diagnostics |
| `update` | Update SpecPulse |

### Working with Specifications

```bash
# Initialize a new feature with SpecPulse
specpulse init my-feature --template web

# Validate specifications against constitution
specpulse validate spec

# Sync project state
specpulse sync

# Run diagnostics
specpulse doctor
```

### In AI Assistants (Claude/Gemini)
```bash
# Initialize feature
/pulse init user-authentication

# Create specification
/spec create "User authentication with OAuth"

# Generate implementation plan
/plan generate

# Create task breakdown
/task breakdown

# Validate everything
/validate all
```

## Testing

Run tests with pytest:

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=specpulse

# Coverage report
pytest --cov=specpulse --cov-report=html
```

## Templates

SpecPulse uses customizable templates for:

- **Specifications** - Feature requirements and acceptance criteria
- **Plans** - Implementation strategies and architecture
- **Tasks** - Work breakdown and tracking
- **Memory** - Constitution and context management

## Configuration

Configure SpecPulse via `.specpulse/config.yaml`:

```yaml
version: 1.0.0
project:
  name: my-project
  type: application
constitution:
  enforce: true
  principles:
    - simplicity_first
    - test_driven
    - security_by_design
```

## Documentation

- [Wiki](https://github.com/specpulse/specpulse/wiki) - Documentation
- [Issues](https://github.com/specpulse/specpulse/issues) - Bug reports
- [Discussions](https://github.com/specpulse/specpulse/discussions) - Community

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Fork and clone
git clone https://github.com/specpulse/specpulse.git

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
pytest tests/

# Submit PR
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**[GitHub](https://github.com/specpulse)**