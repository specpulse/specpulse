# SpecPulse Documentation Index

## Overview

This document serves as a comprehensive index to all SpecPulse documentation resources. It provides quick access to guides, references, and examples for users at all levels.

## 📚 Core Documentation

### Getting Started
| Document | Description | Audience |
|----------|-------------|----------|
| [README.md](README.md) | Project overview, installation, and quick start | New Users |
| [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md) | Complete usage guide with examples | All Users |
| [SPECDRIVEN.md](SPECDRIVEN.md) | Specification-Driven Development methodology | All Users |
| [CLAUDE.md](CLAUDE.md) | Development instructions and guidelines | Developers |

### CLI Reference
| Document | Description | Audience |
|----------|-------------|----------|
| [CLI_REFERENCE.md](CLI_REFERENCE.md) | Complete CLI command reference | All Users |
| [HELP_SYSTEM.md](HELP_SYSTEM.md) | Help system documentation | All Users |

### Development
| Document | Description | Audience |
|----------|-------------|----------|
| [UPDATE_TASKS.md](UPDATE_TASKS.md) | Development roadmap and task list | Developers |
| [CHANGELOG.md](CHANGELOG.md) | Version history and release notes | All Users |

## 🚀 Quick Start Guides

### For New Users
1. **Read**: [README.md](README.md) - Project overview and installation
2. **Try**: `specpulse help overview` - Understand key concepts
3. **Run**: `specpulse init my-project` - Create first project
4. **Learn**: [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md) - Complete usage guide

### For Developers
1. **Setup**: Follow [CLAUDE.md](CLAUDE.md) development instructions
2. **Understand**: [SPECDRIVEN.md](SPECDRIVEN.md) - SDD methodology
3. **Reference**: [CLI_REFERENCE.md](CLI_REFERENCE.md) - Command reference
4. **Contribute**: [UPDATE_TASKS.md](UPDATE_TASKS.md) - Current development tasks

### For Teams
1. **Methodology**: [SPECDRIVEN.md](SPECDRIVEN.md) - Team development approach
2. **Workflow**: [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md) - Team workflows
3. **Commands**: [CLI_REFERENCE.md](CLI_REFERENCE.md) - Shared command reference
4. **Troubleshooting**: Built-in help system (`specpulse help troubleshooting`)

## 🔧 Help System Navigation

### Built-in Help
```bash
# List all help topics
specpulse help --list

# Get overview
specpulse help overview

# Command reference
specpulse help commands

# Development workflow
specpulse help workflow

# Template system
specpulse help templates

# Troubleshooting
specpulse help troubleshooting

# Examples
specpulse help examples
```

### CLI Help Commands
```bash
# General help
specpulse --help

# Command-specific help
specpulse init --help
specpulse validate --help
specpulse template --help
specpulse memory --help
```

## 📖 Documentation by Topic

### Project Setup
- [README.md](README.md) - Installation and initialization
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - `specpulse init` command
- [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md) - Project configuration

### Development Workflow
- [SPECDRIVEN.md](SPECDRIVEN.md) - SDD methodology
- [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md) - Step-by-step workflow
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Workflow commands
- Built-in help: `specpulse help workflow`

### Commands and Tools
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Complete command reference
- [HELP_SYSTEM.md](HELP_SYSTEM.md) - Help system documentation
- Built-in help: `specpulse help commands`

### Template System
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Template management commands
- Built-in help: `specpulse help templates`
- Template files in `templates/` directory

### Memory System
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Memory management commands
- Built-in help: Memory search and summary commands

### Troubleshooting
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Error handling and recovery
- Built-in help: `specpulse help troubleshooting`
- `specpulse doctor` - System diagnostics

## 🏗️ Architecture Documentation

### Core Components
| Component | Description | Documentation |
|-----------|-------------|----------------|
| CLI Layer | Command-line interface | [CLI_REFERENCE.md](CLI_REFERENCE.md) |
| Core Engine | Main framework logic | [CLAUDE.md](CLAUDE.md) |
| Template System | Document templates | Built-in help: `specpulse help templates` |
| Memory System | Project state management | [CLI_REFERENCE.md](CLI_REFERENCE.md) |
| Validator | Project validation | [CLI_REFERENCE.md](CLI_REFERENCE.md) |

### File Structure
```
project/
├── README.md                 # Project overview
├── SPECPULSE_USAGE_GUIDE.md # Usage guide
├── CLI_REFERENCE.md          # Command reference
├── HELP_SYSTEM.md            # Help system docs
├── specpulse/                # Source code
│   ├── cli/                  # CLI commands
│   ├── core/                 # Core framework
│   └── utils/                # Utilities
├── tests/                    # Test suite
├── templates/                # Document templates
├── scripts/                  # Shell scripts
└── docs/                     # Additional docs
```

## 🎯 Use Case Guides

### Web Development
1. **Start**: `specpulse init my-app --template web`
2. **Learn**: [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md)
3. **Reference**: [CLI_REFERENCE.md](CLI_REFERENCE.md)
4. **Examples**: Built-in help: `specpulse help examples`

### API Development
1. **Start**: `specpulse init my-api --template api`
2. **Decompose**: `specpulse decompose` commands
3. **Document**: Auto-generated API specifications
4. **Reference**: Template system documentation

### Microservices
1. **Planning**: [SPECDRIVEN.md](SPECDRIVEN.md) methodology
2. **Decomposition**: `specpulse decompose --microservices`
3. **Integration**: Service boundaries and contracts
4. **Management**: Memory system for service tracking

### CLI Tools
1. **Template**: `specpulse init my-tool --template cli`
2. **Structure**: Command and argument patterns
3. **Validation**: Input validation and error handling
4. **Distribution**: Packaging and installation

## 🔍 Finding Information

### Search Strategies
1. **Built-in Help**: Start with `specpulse help --list`
2. **Command Help**: Use `<command> --help` for specific commands
3. **Documentation**: Browse topic-specific documents
4. **Examples**: Built-in help: `specpulse help examples`

### Quick Access
```bash
# Quick reference card
specpulse help commands

# Troubleshooting guide
specpulse help troubleshooting

# Workflow overview
specpulse help workflow

# Template information
specpulse help templates
```

### External Resources
- **GitHub Repository**: https://github.com/specpulse/specpulse
- **Issues and Discussions**: GitHub issues for support
- **Community**: Contributions and examples welcome

## 📝 Contributing to Documentation

### Documentation Standards
1. **Clear Structure**: Use consistent formatting and headings
2. **Practical Examples**: Include real-world usage examples
3. **Cross-References**: Link to related documentation
4. **Accessibility**: Ensure content is searchable and navigable

### Adding Documentation
1. **Update**: Modify existing documents for clarity
2. **Create**: Add new documents for new features
3. **Index**: Update this index for new content
4. **Test**: Verify help system integration

### Help System Updates
When adding new features:
1. Update built-in help content in `specpulse/cli/main.py`
2. Add command documentation to [CLI_REFERENCE.md](CLI_REFERENCE.md)
3. Create examples for [SPECPULSE_USAGE_GUIDE.md](SPECPULSE_USAGE_GUIDE.md)
4. Update this index if needed

## 🆘 Getting Support

### Self-Service
1. **Built-in Help**: `specpulse help` system
2. **Documentation**: Browse referenced documents
3. **Examples**: Built-in examples and guides
4. **Diagnostics**: `specpulse doctor` for system issues

### Community Support
1. **GitHub Issues**: Report bugs and request features
2. **Discussions**: Ask questions and share experiences
3. **Documentation**: Contribute improvements and examples
4. **Code Reviews**: Participate in development

### Professional Support
For enterprise or commercial support options, refer to the project repository for current information.

## 📈 Documentation Evolution

This documentation index is continuously updated with:
- New feature documentation
- User feedback and suggestions
- Community contributions
- Best practice refinements

### Version Tracking
- Documentation versions align with SpecPulse releases
- [CHANGELOG.md](CHANGELOG.md) tracks documentation changes
- New features include updated help content
- Deprecated features are clearly marked

### Feedback Loop
1. **Usage**: Built-in help system tracks popular topics
2. **Issues**: Documentation bugs and gaps reported via GitHub
3. **Contributions**: Community improves and extends documentation
4. **Analytics**: Help system usage guides content priorities

---

*This documentation index provides comprehensive access to all SpecPulse resources. For the most current information, use the built-in help system: `specpulse help`.*