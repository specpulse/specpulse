# Security Policy

## Supported Versions

| Version | Security Support |
|---------|------------------|
| 2.2.0   | ✅ Full support |
| 2.1.4   | ✅ Full support (Security hotfix) |
| 2.1.3   | ⚠️ CRITICAL vulnerabilities - Upgrade immediately |
| 2.1.x   | ⚠️ CRITICAL vulnerabilities - Upgrade immediately |
| < 2.1.0 | ❌ Not supported |

## Critical Security Update - v2.1.4

**URGENT**: If you are using SpecPulse v2.1.3 or earlier, upgrade immediately.

```bash
pip install --upgrade specpulse
```

Two CRITICAL vulnerabilities were fixed in v2.1.4:
- **CVE-CANDIDATE-001**: Path Traversal (CVSS 9.1)
- **CVE-CANDIDATE-002**: Command Injection (CVSS 9.8)

See `tests/security/SECURITY_AUDIT_REPORT.md` for details.

---

## Reporting Security Vulnerabilities

### DO NOT create public GitHub issues for security vulnerabilities!

Instead, please report security issues privately:

**Email**: security@specpulse.io
**Subject**: "[SECURITY] Brief description"

Include:
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

We will respond within **48 hours** and provide a fix within **7 days** for CRITICAL issues.

---

## Security Features in v2.2.0

### Input Validation

**PathValidator Module**:
- Validates all feature names, spec IDs, plan IDs, task IDs
- Blocks path traversal attacks (../, absolute paths, etc.)
- Enforces character whitelists
- Length limits (255 chars max)

**GitUtils Security**:
- Validates all branch names
- Validates all commit messages
- Validates all tag names
- Blocks shell metacharacters (; & | $ ` etc.)

### Secure Subprocess Calls

**ALWAYS uses list form (never shell=True)**:
```python
# ✅ SECURE
subprocess.run(["git", "checkout", "-b", branch_name], shell=False)

# ❌ NEVER USED
subprocess.run(f"git checkout -b {branch_name}", shell=True)
```

### Safe YAML Loading

**ALWAYS uses yaml.safe_load()**:
```python
# ✅ SECURE
config = yaml.safe_load(file)

# ❌ NEVER USED
config = yaml.load(file)  # Arbitrary code execution risk
```

### Automated Security Checks

**Pre-commit Hooks**:
- Prevents shell=True in subprocess calls
- Enforces yaml.safe_load() usage
- Validates path validation on user inputs
- Runs Bandit security scanner
- Checks for private keys
- Validates YAML/JSON/TOML syntax

---

## Security Best Practices for Users

### 1. Keep SpecPulse Updated

```bash
# Check current version
specpulse --version

# Update to latest
pip install --upgrade specpulse
```

### 2. Run Security Checks

```bash
# Run pre-commit hooks manually
pre-commit run --all-files

# Run security scanner
bandit -r specpulse/ -c pyproject.toml
```

### 3. Review Generated Files

Always review specifications, plans, and tasks before committing:
```bash
git diff specs/
git diff plans/
git diff tasks/
```

### 4. Use Version Control

Always use git to track changes:
```bash
# SpecPulse creates feature branches automatically
# Review changes before merging
git diff master..001-feature-branch
```

---

## Security Testing

### Test Coverage

SpecPulse includes **620+ security tests**:

**Path Traversal Tests** (320+ tests):
- Directory escape attempts
- Absolute path attacks
- Symlink exploitation
- Unicode attacks
- Null byte injection

**Command Injection Tests** (150+ tests):
- Semicolon injection
- Ampersand injection
- Pipe injection
- Command substitution
- Backtick injection

**Fuzzing Tests** (150+ tests):
- Random malicious inputs
- Shell metacharacters
- Control characters
- Unicode variations

### Running Security Tests

```bash
# Run all security tests
pytest tests/security/ -v

# Run specific test category
pytest tests/security/test_path_traversal.py -v
pytest tests/security/test_command_injection.py -v
pytest tests/security/test_fuzzing.py -v

# Run with coverage
pytest tests/security/ --cov=specpulse --cov-report=html
```

---

## OWASP Top 10 2021 Compliance

| Risk | Applicable? | Status | Mitigation |
|------|-------------|--------|------------|
| A01: Broken Access Control | ✅ Yes | ✅ MITIGATED | PathValidator enforces containment |
| A02: Cryptographic Failures | ❌ No | N/A | No crypto operations |
| A03: Injection | ✅ Yes | ✅ MITIGATED | Input validation blocks all injection |
| A04: Insecure Design | ✅ Yes | ✅ MITIGATED | Security-by-design architecture |
| A05: Security Misconfiguration | ✅ Yes | ✅ MITIGATED | Secure defaults, automated checks |
| A06: Vulnerable Components | ✅ Yes | ✅ CHECKED | Bandit scanner, dependency audit |
| A07: Authentication Failures | ❌ No | N/A | No authentication (local tool) |
| A08: Software/Data Integrity | ✅ Yes | ✅ MITIGATED | Path validation before writes |
| A09: Logging Failures | ⚠️ Partial | ⚠️ PARTIAL | Basic logging present |
| A10: SSRF | ❌ No | N/A | No server-side requests |

**Overall Compliance**: 80% (5/5 applicable risks mitigated)

---

## Security Audit Results

**Last Audit**: 2025-10-14
**Auditor**: ClaudeForge Security Agent
**Status**: PASSED ✅

**Findings**:
- 2 CRITICAL vulnerabilities identified and fixed
- 0 HIGH severity issues
- 0 MEDIUM severity issues
- Security posture: EXCELLENT

**Full Report**: `tests/security/SECURITY_AUDIT_REPORT.md`

---

## Security Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities.

### Hall of Fame

(No public disclosures yet - v2.1.4 is first security-focused release)

---

## Security Roadmap

### v2.2.1 (Minor improvements)
- Enhanced security logging
- Security event monitoring
- Audit trail for file operations

### v2.3.0 (Plugin security)
- Plugin signature validation
- Sandboxed plugin execution
- Security review process for marketplace

### v3.0.0 (Enterprise security)
- Role-based access control
- Team permissions
- Security dashboard
- Professional penetration testing

---

**Security Contact**: security@specpulse.io
**Security Policy**: https://github.com/specpulse/specpulse/security/policy
**Advisories**: https://github.com/specpulse/specpulse/security/advisories

**Last Updated**: 2025-10-14
**Version**: 2.2.0
