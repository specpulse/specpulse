# Changelog

All notable changes to SpecPulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-09-11

### Fixed
- **Version Display**: Fixed --version command to show correct version
- Dynamic version import from __init__.py instead of hardcoded values
- Fixed version display in doctor command banner

### Technical
- Version now centrally managed in __init__.py
- All CLI commands now use dynamic version import

## [1.0.2] - 2025-09-11

### Fixed
- **Critical**: Fixed package installation by properly declaring all subpackages
- Fixed ModuleNotFoundError for specpulse.core, cli, and utils modules
- Corrected package structure in pyproject.toml

### Technical
- Added all subpackages to setuptools configuration
- Ensured proper module discovery during installation

## [1.0.1] - 2025-09-11

### Fixed
- Corrected AI command documentation in README
- Clarified actual command structure for Claude and Gemini
- Updated Quick Start guide with accurate command examples

### Improved
- Enhanced project structure documentation
- Added shell script details to structure diagram
- Clarified AI integration requirements

## [1.0.0] - 2025-09-11

### Added
- Initial release of SpecPulse framework
- CLI commands: `init`, `doctor`, `validate`, `sync`, `update`
- Specification-Driven Development methodology implementation
- The Nine Articles constitutional framework
- Phase Gates system for quality control
- [NEEDS CLARIFICATION] marker system
- Beautiful CLI with ASCII art and animations
- AI integration for Claude and Gemini
- Custom command system for AI assistants
- Shell scripts for automation
- Template system for specifications, plans, and tasks
- Memory system (constitution, context, decisions)
- Git integration utilities
- Multi-level validation engine
- Auto-fix capabilities
- Color-coded console output
- Progress indicators and tables
- PyPI package distribution

### Features
- Project initialization with complete structure
- System diagnostics and health checks
- Component validation with auto-fix
- Project state synchronization
- AI-driven specification creation
- Implementation plan generation
- Task breakdown automation
- Test-first development enforcement
- Complexity tracking and management
- Framework-first integration approach

### Technical
- Python 3.11+ support
- Cross-platform compatibility (Windows, macOS, Linux)
- Resource file management
- Extensible template system
- Modular architecture
- Rich library integration for beautiful CLI

### Documentation
- Comprehensive README
- Framework documentation
- AI command guides
- Template documentation
- Installation instructions
- Usage examples

## Links
- [PyPI Package](https://pypi.org/project/specpulse/)
- [GitHub Repository](https://github.com/specpulse)
- [Issue Tracker](https://github.com/specpulse/specpulse/issues)