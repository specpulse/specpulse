# Changelog

All notable changes to SpecPulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.6] - 2025-09-12

### Changed
- **Updated README.md**: Added Important Security Rules section explaining protected vs editable directories
- **Documentation**: Clarified that templates are copied to working directories, never modified directly

## [1.2.5] - 2025-09-12

### Fixed
- **Clarified File Edit Permissions**: Edit tool restored to Claude commands with clear restrictions
- **Added Security Notes**: All commands now explicitly state which directories are protected
- **Directory Protection**: templates/, scripts/, commands/ folders are read-only after init

### Changed
- Claude commands can use Edit tool but ONLY in specs/, plans/, tasks/, memory/ folders
- Added CRITICAL security notes to all command files
- Clarified that templates are COPIED to working directories, then edited there

## [1.2.4] - 2025-09-12

### Fixed
- **Critical Security Fix**: Prevented modification of template files
- **Script Improvements**: Fixed template file paths in all shell scripts
- **AI Command Security**: Removed Edit tool from Claude commands to prevent template modification
- **Template Protection**: Ensured all scripts only COPY templates, never modify originals

### Changed
- All scripts now use correct template names (spec.md, plan.md, task.md)
- Claude commands explicitly state templates must be COPIED, not edited
- Enhanced security by preventing any modification of resources/templates files

## [1.2.3] - 2025-09-12

### Changed
- **Simplified script execution**: Removed Python script fallback, now using only Bash scripts across all platforms
- **Streamlined packaging**: Removed Python scripts from package distribution
- **Updated documentation**: Clarified Bash requirement for all platforms (Git Bash on Windows)

### Removed
- All Python scripts (.py) from resources/scripts directory
- Python fallback references from all Claude and Gemini command files
- Python script references from package data in pyproject.toml and setup.py

## [1.2.2] - 2025-09-12

### Fixed
- **Version display**: Fixed `__version__` in `__init__.py` to show correct version
- Now `specpulse --version` displays the correct version number

## [1.2.1] - 2025-09-12

### Fixed
- **Critical**: Fixed syntax error in main.py line 480 - unterminated string literal
- Multi-line strings in decompose method now use proper triple quotes

## [1.2.0] - 2025-09-12

### Added
- **Microservice Decomposition**: New `/sp-decompose` command to break down large specifications into microservices
- **Service-Based Planning**: Automatic detection of decomposed specs and creation of service-specific plans
- **Integration Planning**: New integration plan template for coordinating between services
- **Service Task Management**: Task IDs with service prefixes (AUTH-T001, USER-T001, INT-T001)
- **Smart Workflow Detection**: Plans and tasks automatically adapt to monolithic vs decomposed architecture
- **New Templates**: Added templates for microservices, API contracts, interfaces, and integration plans
- **Decomposition CLI Command**: `specpulse decompose [spec-id] [--microservices] [--apis] [--interfaces]`
- **Enhanced Context Tracking**: `memory/context.md` now tracks decomposition status and service architecture

### Changed
- **Workflow Adaptation**: `/sp-plan` and `/sp-task` commands now detect decomposition and generate appropriate artifacts
- **Template Structure**: Added `templates/decomposition/` directory with specialized templates
- **Script Updates**: Added `sp-pulse-decompose.sh` and `sp-pulse-decompose.py` for decomposition orchestration

### Fixed
- **Template Loading**: Proper handling of decomposition templates in SpecPulse core
- **CLI Integration**: Decompose command properly integrated with existing workflow

## [1.1.0] - 2025-09-12

### Added
- **Command prefix system**: All commands now use `sp-` prefix to avoid reserved name conflicts
- **Multi-spec workflow**: Support for multiple specifications, plans, and tasks within the same feature
- **Versioned file system**: Automatic naming with spec-001.md, plan-001.md, task-001.md format
- **Context detection**: Automatic feature detection using memory/context.md and git branch names
- **Manual workflow control**: `/sp-pulse` only creates directories, manual control over `/spec`, `/plan`, `/task`
- **Enhanced AI integration**: Improved workflow coordination between Claude and Gemini assistants

### Fixed
- **Comprehensive codebase review**: Fixed all old command references throughout the project
- **Template system cleanup**: Removed nonsensical shell script execution commands from templates
- **File path consistency**: Updated all hardcoded file paths to use versioned naming system
- **Script naming**: All scripts now consistently use `sp-` prefix (sp-pulse-*.py, sp-pulse-*.sh)
- **Documentation updates**: Updated all README references and examples to use new command structure

### Changed
- **Breaking change**: All command names changed from `/pulse`, `/spec`, `/plan`, `/task` to `/sp-pulse`, `/sp-spec`, `/sp-plan`, `/sp-task`
- **Removed PowerShell scripts**: Now only supporting .sh and .py scripts for cross-platform compatibility
- **Improved project structure**: Better organization of scripts and templates with consistent naming
- **Enhanced error handling**: Better validation and error messages throughout the system

## [1.0.6] - 2025-09-11

### Fixed
- **Critical cross-platform template bug**: Fixed `specpulse init` command to use proper cross-platform scripts from `@specpulse/resources` instead of embedded templates
- **Package data configuration**: Added missing `.py` and `.ps1` script files to package manifest in `pyproject.toml`
- **CLI script creation**: Updated `_create_scripts` method to copy all cross-platform scripts from resources directory
- **Resource path resolution**: Enhanced resource path detection using `pkg_resources.resource_filename()`

### Added
- Complete cross-platform script availability: All 12 scripts (4 types × 3 platforms) now properly installed
- Better error handling for script copying operations
- Improved script count reporting during initialization

## [1.0.5] - 2025-09-11

### Added
- **Complete cross-platform compatibility** with Windows, Linux, and macOS support
- **Python script equivalents** of all bash scripts (.py files)
- **PowerShell script equivalents** for Windows systems (.ps1 files)
- **Automatic platform detection** in AI commands with fallback mechanisms
- **Comprehensive cross-platform test suite** with 100% success rate
- **Unicode character support** for international feature names (≤, ≥, →, ←)
- **Enhanced template system** with proper path resolution across platforms

### Changed
- **AI commands now detect operating system automatically** and choose appropriate script type
- **Template paths updated** to use consistent `/resources/templates/` structure
- **Error handling improved** with platform-specific logging and fallback mechanisms
- **Package data updated** to include all script variants (Python, PowerShell, Bash)

### Fixed
- **Template path resolution issues** across different platforms
- **File permission handling** for cross-platform compatibility
- **Unicode encoding issues** on Windows systems
- **Script execution failures** on non-Unix platforms

## [1.0.4] - 2025-09-11

### Added
- Comprehensive test suite with 95% code coverage (193+ tests)
- Proper Gemini command format following official documentation
- Claude command frontmatter with YAML metadata
- Support for command arguments in both Claude (`$ARGUMENTS`) and Gemini (`{{args}}`)
- Test files for AI command validation
- CHANGELOG.md for tracking version changes

### Changed
- Updated Claude command files to include proper frontmatter
- Converted Gemini command files to official simple TOML format
- Improved README documentation with accurate command examples
- Enhanced test coverage from 69% to 95%

### Fixed
- AI commands now properly accept and handle arguments
- Command documentation matches actual implementation
- Gemini commands use correct `{{args}}` placeholder
- Claude commands use correct `$ARGUMENTS` variable

## [1.0.3] - 2025-09-10

### Added
- Initial PyPI release
- Core SpecPulse framework
- CLI interface with init, validate, sync, doctor commands
- Claude and Gemini AI integration
- Constitution-based development principles
- Phase Gates validation system

### Changed
- Improved project structure
- Enhanced validation logic

### Fixed
- Various bug fixes and improvements

## [1.0.2] - 2025-09-10

### Added
- Basic test coverage
- Documentation improvements

### Fixed
- Minor bug fixes

## [1.0.1] - 2025-09-10

### Added
- Initial beta release
- Basic functionality

### Fixed
- Setup and installation issues