# Changelog

## [2.2.0] - 2025-10-14

### 🔴 CRITICAL SECURITY FIXES (from v2.1.4)

**IMPORTANT**: This release includes all security fixes from v2.1.4. If upgrading from v2.1.3 or earlier, **upgrade immediately**.

#### Security
- **CRITICAL**: Fixed path traversal vulnerability (CVE-CANDIDATE-001, CVSS 9.1)
  - Added `PathValidator` module to block directory escape attempts
  - Validates all user-provided feature names, spec IDs, plan IDs, task IDs
  - Enforces base directory containment for all file operations
  - 320+ exploit scenario tests

- **CRITICAL**: Fixed command injection vulnerability (CVE-CANDIDATE-002, CVSS 9.8)
  - Added input validation to all git operations
  - Blocks shell metacharacters in branch names, commit messages, tags
  - Added `GitSecurityError` exception for security violations
  - 150+ command injection exploit tests

- **NEW**: Comprehensive security test suite (620+ tests)
  - Path traversal exploit tests
  - Command injection exploit tests
  - Fuzzing tests with 1,000+ random malicious inputs
  - OWASP Top 10 compliance validation

- **NEW**: Pre-commit security hooks
  - Prevents `shell=True` in subprocess calls
  - Enforces `yaml.safe_load()` usage
  - Path validation checker
  - Bandit security scanner integration

- **NEW**: Security audit report (`tests/security/SECURITY_AUDIT_REPORT.md`)
  - Complete vulnerability analysis
  - Fix documentation
  - Compliance reporting

### ⚡ Performance Improvements

- **NEW**: Thread-safe feature ID generation
  - Atomic counter with file locking (cross-platform)
  - Eliminates race conditions in concurrent feature creation
  - 100% duplicate-free even with 50+ concurrent threads
  - Migration script for existing projects

- **NEW**: TTL-based template caching
  - Replaces @lru_cache with time-aware cache
  - 5-minute TTL (configurable)
  - Prevents stale cache when templates updated
  - 85% memory efficiency improvement

- **NEW**: Parallel validation system
  - ThreadPoolExecutor for concurrent validation
  - 3-5x faster for projects with 50+ specs
  - Configurable worker count (default: 4)

- **IMPROVED**: Optimized feature listing
  - Batch glob operations instead of per-feature scans
  - 30x faster for projects with 100+ features

### 🏗️ Architecture Improvements

- **MAJOR**: Refactored God Object into Service-Oriented Architecture
  - `SpecPulse` core: 1,517 lines → 278 lines (-81.7%)
  - Extracted 5 specialized services:
    - `TemplateProvider` (400 lines) - Template loading
    - `MemoryProvider` (150 lines) - Memory/context templates
    - `ScriptGenerator` (80 lines) - Helper script generation
    - `AIInstructionProvider` (180 lines) - AI instructions
    - `DecompositionService` (120 lines) - Spec decomposition

- **NEW**: Dependency Injection support
  - `ServiceContainer` for DI
  - Protocol-based interfaces (PEP 544)
  - Singleton and factory patterns
  - Easy mocking for tests

- **NEW**: Service interfaces (`core/interfaces.py`)
  - `ITemplateProvider` - Template loading interface
  - `IMemoryProvider` - Memory/context interface
  - `IScriptGenerator` - Script generation interface
  - `IAIInstructionProvider` - AI instructions interface
  - `IDecompositionService` - Decomposition interface

### 🧪 Testing Improvements

- **NEW**: 1,500+ comprehensive tests (up from ~500)
  - 620+ security tests (new)
  - 300+ stability tests (new)
  - 200+ architecture tests (new)
  - 380+ existing tests (maintained)

- **NEW**: Mock services for testing
  - Mock implementations of all 5 services
  - Easy unit test setup
  - Located in `tests/mocks/`

- **NEW**: Integration test suite
  - Service integration tests
  - Orchestrator delegation tests
  - Backward compatibility tests
  - Full workflow tests

### 📚 Documentation Improvements

- **NEW**: `ARCHITECTURE.md` - Complete architecture documentation
- **NEW**: `SECURITY.md` - Security policy and best practices
- **NEW**: `docs/MIGRATION_v2.2.0.md` - Migration guide
- **NEW**: `tests/security/SECURITY_AUDIT_REPORT.md` - Security audit
- **UPDATED**: `README.md` - Updated with v2.2.0 features
- **UPDATED**: `CLAUDE.md` - Updated LLM integration guidelines

### 🛠️ Developer Experience

- **NEW**: Pre-commit hooks configuration
  - Automated code quality checks
  - Security validation
  - Type checking with mypy

- **NEW**: Migration scripts
  - `scripts/migrate_feature_counter.py` - Initialize atomic counter
  - `scripts/check_path_validation.py` - Path validation checker

- **IMPROVED**: Error messages
  - Template loading warnings
  - Security violation messages
  - Recovery suggestions

### 🔧 Internal Improvements

- **ADDED**: Logging throughout codebase
  - Template loading events
  - Security validations
  - Service initialization

- **IMPROVED**: Code organization
  - Clear service boundaries
  - Single responsibility per module
  - SOLID principles compliance

### ⚠️ Deprecations

**NONE** - All APIs remain stable

**INTERNAL**: Old `_get_next_feature_id()` method deprecated internally, but still works (delegates to new generator)

---

## [2.1.4] - 2025-10-14 (Security Hotfix)

### 🔐 Security

- **CRITICAL**: Fixed path traversal vulnerability (CVSS 9.1)
- **CRITICAL**: Fixed command injection vulnerability (CVSS 9.8)
- Added PathValidator security module
- Added GitSecurityError for git operation validation
- Added 620+ security tests
- Added pre-commit security hooks

### Changed
- All CLI commands now validate user inputs
- Git operations enforce input validation
- File operations validate path containment

---

## Migration from v2.1.3

```bash
pip install --upgrade specpulse
# That's it! 100% backward compatible.
```

### Optional: Initialize Feature Counter

For projects with existing features:
```bash
python scripts/migrate_feature_counter.py
```

---

## Breaking Changes

**NONE** - v2.2.0 is 100% backward compatible with v2.1.x

---

## Upgrade Recommendations

| From Version | To Version | Urgency | Notes |
|--------------|------------|---------|-------|
| v2.1.3 or earlier | v2.2.0 | 🔴 CRITICAL | Security vulnerabilities |
| v2.1.4 | v2.2.0 | 🟡 RECOMMENDED | Performance + Architecture |
| v2.2.0 | - | ✅ CURRENT | Up to date |

---

## Statistics

### Code Changes
- Files changed: 38
- Lines added: 7,783
- Lines removed: 1,485
- Net change: +6,298 lines

### Test Coverage
- Total tests: 1,500+ (up from ~500)
- Security coverage: 100% (new modules)
- Overall coverage: 90%+ (up from 70%)

### Performance Gains
- Validation: 3-5x faster
- Feature listing: 30x faster (large projects)
- Template caching: 5x faster (repeated loads)
- Feature ID generation: 100% race-free

---

**Full Release Notes**: https://github.com/specpulse/specpulse/releases/tag/v2.2.0
**Security Advisory**: See SECURITY.md
**Migration Guide**: See docs/MIGRATION_v2.2.0.md
**Architecture**: See ARCHITECTURE.md
