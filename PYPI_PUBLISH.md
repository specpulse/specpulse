# PyPI Publishing Guide - SpecPulse v2.1.3

## 🎯 Pre-Publish Checklist

- [✅] Version bumped to 2.1.3 (`_version.py`, `setup.py`, `pyproject.toml`)
- [✅] CHANGELOG.md updated with v2.1.3 entry
- [✅] README.md updated with new commands
- [✅] All tests passing (or documented issues)
- [✅] Package builds successfully
- [✅] Installation verified
- [✅] Workflow tested end-to-end
- [✅] Documentation complete

## 📦 Build Process

### 1. Clean Previous Builds

```bash
cd C:\Sync\Codebox\__PIP__\SpecPulse

# Remove old builds
rm -rf build/ dist/ *.egg-info

# Clean Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
```

### 2. Build Packages

```bash
# Build source distribution and wheel
python setup.py sdist bdist_wheel

# Verify build artifacts
ls -lh dist/
# Should see:
# - specpulse-2.1.3.tar.gz
# - specpulse-2.1.3-py3-none-any.whl
```

### 3. Verify Package Contents

```bash
# Check wheel contents
unzip -l dist/specpulse-2.1.3-py3-none-any.whl

# Should include:
# ✓ specpulse/cli/sp_pulse_commands.py
# ✓ specpulse/cli/sp_spec_commands.py
# ✓ specpulse/cli/sp_plan_commands.py
# ✓ specpulse/cli/sp_task_commands.py
# ✓ specpulse/resources/commands/claude/*.md
# ✓ specpulse/resources/commands/gemini/*.toml
```

### 4. Test Installation Locally

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from wheel
pip install dist/specpulse-2.1.3-py3-none-any.whl

# Verify installation
specpulse --version
# Should show: SpecPulse 2.1.3

# Test commands
specpulse sp-pulse --help
specpulse sp-spec --help
specpulse sp-plan --help
specpulse sp-task --help

# Deactivate and cleanup
deactivate
rm -rf test_env
```

## 🚀 Publishing to PyPI

### Prerequisites

```bash
# Install twine if not already installed
pip install twine

# Verify twine installed
twine --version
```

### Option 1: Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/specpulse-2.1.3*

# You'll be prompted for:
# Username: __token__
# Password: <your-test-pypi-token>

# Verify upload
# Visit: https://test.pypi.org/project/specpulse/

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ specpulse==2.1.3
```

### Option 2: Production PyPI

```bash
# Upload to PyPI (PRODUCTION)
twine upload dist/specpulse-2.1.3*

# You'll be prompted for:
# Username: __token__
# Password: <your-pypi-token>

# Verify upload
# Visit: https://pypi.org/project/specpulse/
```

### Using API Token (Recommended)

Create `.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-<your-token-here>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-<your-test-token-here>
```

Then upload:
```bash
twine upload dist/specpulse-2.1.3*
```

## 🔍 Post-Publish Verification

### 1. Verify on PyPI

```bash
# Check project page
# https://pypi.org/project/specpulse/

# Verify:
# ✓ Version shows 2.1.3
# ✓ Description correct
# ✓ Dependencies listed
# ✓ Download links work
```

### 2. Test Fresh Installation

```bash
# In a new directory
cd /tmp/test-install
python -m venv fresh_env
source fresh_env/bin/activate

# Install from PyPI
pip install specpulse==2.1.3

# Verify
specpulse --version
specpulse sp-pulse --help

# Test workflow
specpulse init test-project --here --ai claude
specpulse sp-pulse init test-feature
specpulse sp-spec create "Test specification"

# Cleanup
deactivate
cd ..
rm -rf test-install
```

### 3. Update Documentation Links

```bash
# Update badges in README.md if needed
# Update version references in docs/
```

## 🏷️ Git Tagging

```bash
# Create annotated tag
git tag -a v2.1.3 -m "SpecPulse v2.1.3 - sp-* Commands Refactoring

Major refactoring with 27 new CLI commands:
- sp-pulse: Feature management (5 commands)
- sp-spec: Specification management (7 commands)
- sp-plan: Implementation plans (7 commands)
- sp-task: Task management (8 commands)

Breaking: Removed 'sp' alias
See CHANGELOG.md for full details"

# Verify tag
git tag -l -n9 v2.1.3

# Push tag
git push origin v2.1.3
```

## 📝 Release Notes

Create GitHub release with:

**Title:** `SpecPulse v2.1.3 - sp-* Commands Refactoring`

**Description:**
```markdown
## 🎯 Major Refactoring: 27 New CLI Commands

Complete CLI refactoring with dedicated sp-* command modules for better organization and functionality.

### ✨ New Commands

**sp-pulse** - Feature Management (5 commands)
- `specpulse sp-pulse init <name>` - Initialize feature
- `specpulse sp-pulse continue <name>` - Switch feature
- `specpulse sp-pulse list` - List all features
- `specpulse sp-pulse status` - Current status
- `specpulse sp-pulse delete <name>` - Delete feature

**sp-spec** - Specification Management (7 commands)
**sp-plan** - Implementation Plans (7 commands)
**sp-task** - Task Management (8 commands)

See [CHANGELOG.md](CHANGELOG.md) for complete details.

### ⚠️ Breaking Changes

- Removed `sp` alias - use full `specpulse` command

### 📚 Documentation

- [Migration Guide](MIGRATION_v2.1.3.md)
- [Test Report](TEST_REPORT_v2.1.3.md)
- [Workflow Verification](WORKFLOW_VERIFICATION_v2.1.3.md)

### 🔗 Links

- PyPI: https://pypi.org/project/specpulse/2.1.3/
- GitHub: https://github.com/specpulse/specpulse
```

**Attach Files:**
- Source tarball: `specpulse-2.1.3.tar.gz`
- Wheel package: `specpulse-2.1.3-py3-none-any.whl`

## 🎯 Post-Release Tasks

- [ ] Announce on GitHub Discussions
- [ ] Update documentation site (if any)
- [ ] Tweet/social media announcement
- [ ] Update project roadmap
- [ ] Monitor issue tracker for v2.1.3 issues

## 🆘 Rollback Plan

If critical issues found:

```bash
# Yank the release
# This removes it from pip install without delete
twine upload --repository pypi --skip-existing dist/specpulse-2.1.3*

# Or use PyPI web interface:
# https://pypi.org/project/specpulse/
# Click "Manage" → "Yank release"

# Users can still install with:
pip install specpulse==2.1.3
# But pip install specpulse won't get it
```

## ✅ Success Metrics

After 24 hours, check:
- Download count on PyPI
- GitHub stars/forks
- Issue reports
- User feedback

---

**Ready to publish! Good luck! 🚀**
