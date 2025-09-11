# Changelog

All notable changes to SpecPulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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