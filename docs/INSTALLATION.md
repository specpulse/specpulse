# SpecPulse v2.4.1 Installation Guide

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## 🔧 System Requirements

### Minimum Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free disk space

### Recommended Requirements

- **Python**: 3.12 or higher
- **Git**: 2.30 or higher (recommended for context detection)
- **Memory**: 1GB RAM
- **Storage**: 500MB free disk space

### Optional Dependencies

- **Claude Code**: For AI-enhanced workflow (recommended)
- **Gemini CLI**: For AI-enhanced workflow (alternative)
- **VS Code**: For enhanced development experience
- **Git Client**: Command-line git tools

---

## 📦 Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Install SpecPulse
pip install specpulse==2.4.1

# Or upgrade from previous version
pip install --upgrade specpulse==2.4.1
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/specpulse/specpulse.git
cd specpulse

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Method 3: Install with Conda

```bash
# Create conda environment (optional)
conda create -n specpulse python=3.11
conda activate specpulse

# Install SpecPulse
pip install specpulse==2.4.1
```

### Method 4: Install with pipx (Recommended for isolated environments)

```bash
# Install pipx if not already installed
pip install --user pipx

# Install SpecPulse
pipx install specpulse==2.4.1

# Ensure pipx path is in your PATH
pipx ensurepath
```

---

## 🐍 Platform-Specific Instructions

### Windows

#### Using PowerShell (Recommended)

```powershell
# Install SpecPulse
pip install specpulse==2.4.1

# Verify installation
specpulse --version
```

#### Using Command Prompt

```cmd
# Install SpecPulse
pip install specpulse==2.4.1

# Verify installation
specpulse --version
```

#### Using Chocolatey

```powershell
# Install SpecPulse via Chocolatey (if available)
choco install specpulse

# Or using pip
pip install specpulse==2.4.1
```

### macOS

#### Using Homebrew (Recommended)

```bash
# Install Python if not already installed
brew install python3

# Install SpecPulse
pip3 install specpulse==2.0.0

# Verify installation
specpulse --version
```

#### Using pip

```bash
# Install SpecPulse
pip install specpulse==2.4.1

# Verify installation
specpulse --version
```

### Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install SpecPulse
pip3 install specpulse==2.0.0

# Verify installation
specpulse --version
```

#### CentOS/RHEL/Fedora

```bash
# Install Python and pip
sudo dnf install python3 python3-pip

# Or on older systems
sudo yum install python3 python3-pip

# Install SpecPulse
pip3 install specpulse==2.0.0

# Verify installation
specpulse --version
```

#### Using pipx

```bash
# Install pipx
pip install --user pipx

# Install SpecPulse
pipx install specpulse==2.4.1

# Ensure pipx path is in PATH
pipx ensurepath
```

---

## ✅ Verification

### Basic Verification

```bash
# Check version
specpulse --version

# Expected output:
# SpecPulse 2.4.1

# Show help
specpulse --help

# Expected output should show all available commands
```

### AI Integration Verification

```bash
# Test feature commands
specpulse feature --help

# Test specification commands
specpulse spec --help

# Test plan commands
specpulse plan --help

# Test task commands
specpulse task --help

# Test validation commands
specpulse validate --help
```

### Template System Verification

```bash
# List available templates
specpulse template list

# Validate templates
specpulse template validate
```

### Project Initialization Verification

```bash
# Create test project
specpulse init test-project

# Navigate to project
cd test-project

# Verify project structure
ls -la

# Expected directories: specs, plans, tasks, memory, templates
# Expected AI command directories: .claude, .gemini (if AI assistants were specified)
```

---

## 🛠️ Development Installation

### For Contributors

```bash
# Clone repository
git clone https://github.com/specpulse/specpulse.git
cd specpulse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify
pytest

# Run code quality checks
black specpulse/
flake8 specpulse/
mypy specpulse/
```

### Development Dependencies

The `[dev]` extra includes:
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `black>=23.0` - Code formatting
- `flake8>=6.0` - Linting
- `mypy>=1.0` - Type checking
- `pre-commit>=3.0` - Git hooks

---

## 🔧 Configuration

### Environment Variables

```bash
# Set custom templates directory (optional)
export SPECPULSE_TEMPLATES_DIR="/path/to/custom/templates"

# Set custom memory directory (optional)
export SPECPULSE_MEMORY_DIR="/path/to/custom/memory"

# Enable verbose mode (optional)
export SPECPULSE_VERBOSE=1
```

### Git Integration

SpecPulse automatically integrates with Git for:

- **Context Detection**: Detects current feature from branch names
- **Version Control**: Tracks specification and plan versions
- **Branch Management**: Suggests branch naming conventions

### AI Assistant Configuration

#### Claude Code

```bash
# Initialize with Claude support
specpulse init my-project --ai claude

# Claude automatically detects SpecPulse context
# Custom commands are copied to .claude/commands/
```

#### Gemini CLI

```bash
# Initialize with Gemini support
specpulse init my-project --ai gemini

# Gemini automatically detects SpecPulse context
# Custom commands are copied to .gemini/commands/
```

---

## 🐛 Troubleshooting

### Common Installation Issues

#### Python Version Issues

```bash
# Check Python version
python --version

# Should show 3.11+ for SpecPulse 2.4.1
```

**Solution**: Upgrade Python or use pyenv to manage versions:

```bash
# Using pyenv
pyenv install 3.12.0
pyenv global 3.12.0

# Verify installation
python --version
pip install specpulse==2.4.1
```

#### Permission Issues

**Linux/macOS**:
```bash
# Install for user only
pip install --user specpulse==2.0.0

# Or use sudo (not recommended)
sudo pip3 install specpulse==2.0.0
```

**Windows**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install SpecPulse
pip install specpulse==2.4.1
```

#### Network Issues

```bash
# Use PyPI mirror (China)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ specpulse==2.0.0

# Or use alternative index
pip install --index-url https://pypi.org/simple/ specpulse==2.0.0
```

#### Virtual Environment Issues

```bash
# Create new virtual environment
python -m venv specpulse-env
source specpulse-env/bin/activate  # Windows: specpulse-env\Scripts\activate

# Install SpecPulse
pip install specpulse==2.4.1
```

### Post-Installation Issues

#### Command Not Found

```bash
# Check if SpecPulse is in PATH
which specpulse

# If not found, add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or use python module directly
python -m specpulse --version
```

#### Template Loading Issues

```bash
# Verify templates directory
ls templates/

# Reinstall if necessary
pip uninstall specpulse
pip install specpulse==2.4.1
```

#### AI Integration Issues

```bash
# Check AI integration
specpulse ai context

# If context detection fails, check Git
git branch --show-current

# Initialize git if needed
git init
git add .
git commit -m "Initial commit"
```

---

## 📋 Platform-Specific Notes

### Windows

- **PowerShell Recommended**: Use PowerShell instead of Command Prompt for better experience
- **Unicode Support**: SpecPulse v2.4.1 includes Unicode encoding fixes for Windows
- **Path Length**: Be aware of Windows path length limitations (260 characters)
- **Antivirus**: Some antivirus software may flag Python packages - add exceptions if needed

### macOS

- **Python Installation**: Use Homebrew for easier Python management
- **Permissions**: May need to allow unsigned applications on macOS
- **Xcode Command Line Tools**: Install Xcode command line tools for development dependencies

### Linux

- **Package Manager**: Use your distribution's package manager for Python
- **Virtual Environments**: Highly recommended for isolation
- **System Python**: Avoid installing packages globally unless necessary

---

## 🔄 Upgrading from Previous Versions

### From v1.x to v2.4.1

```bash
# Backup existing projects (recommended)
cp -r my-project my-project.backup

# Upgrade SpecPulse
pip install --upgrade specpulse==2.4.1

# Verify upgrade
specpulse --version

# Test new CLI features
specpulse doctor
specpulse feature --help
```

### Migration Checklist

- [ ] Backup existing projects
- [ ] Upgrade SpecPulse package
- [ ] Test CLI integration features
- [ ] Validate existing specifications
- [ ] Update team on CLI-first workflow

---

## 🚀 Next Steps

After successful installation:

1. **Initialize Your First Project**:
   ```bash
   specpulse init my-awesome-project --ai claude
   ```

2. **Explore CLI Features**:
   ```bash
   cd my-awesome-project
   specpulse feature init user-auth
   specpulse spec create "User authentication with OAuth2"
   specpulse doctor
   ```

3. **Read the Documentation**:
   - [AI Integration Guide](AI_INTEGRATION.md)
   - [Migration Guide](MIGRATION.md)
   - [Troubleshooting Guide](TROUBLESHOOTING.md)

4. **Join the Community**:
   - [GitHub Discussions](https://github.com/specpulse/specpulse/discussions)
   - [Issues](https://github.com/specpulse/specpulse/issues)
   - [Wiki](https://github.com/specpulse/specpulse/wiki)

---

## 📞 Support

If you encounter issues during installation:

1. **Check this guide** for platform-specific solutions
2. **Search existing issues**: [GitHub Issues](https://github.com/specpulse/specpulse/issues)
3. **Create new issue**: Include system information and error messages
4. **Community help**: [GitHub Discussions](https://github.com/specpulse/specpulse/discussions)

### System Information for Bug Reports

```bash
# Collect system information
python --version
pip --version
specpulse --version
git --version
uname -a  # Linux/macOS
systeminfo  # Windows
```

---

**🎉 Congratulations! You have successfully installed SpecPulse v2.4.1.**