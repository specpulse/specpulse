# SpecPulse v2.7.1

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/specpulse.svg)](https://pypi.org/project/specpulse/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Platforms](https://img.shields.io/badge/AI%20Platforms-8-blue.svg)](https://github.com/specpulse/specpulse)
[![Commands](https://img.shields.io/badge/Commands-86-green.svg)](https://github.com/specpulse/specpulse)

**The Complete AI-Enhanced Development Framework**

*Build better software with specifications first, powered by AI assistants across 8 major platforms*

</div>

---

## 🚀 What Makes SpecPulse Revolutionary?

SpecPulse is **not just another CLI tool** - it's a complete development framework that bridges the gap between your ideas and production code. By combining structured specifications with AI-powered assistance, SpecPulse transforms how you build software.

### 🎯 The Core Problem We Solve

Traditional development is chaotic:
- ❌ Ideas jump directly to coding without proper planning
- ❌ Requirements get lost in scattered documentation
- ❌ AI assistants lack context about your project structure
- ❌ Teams work without clear specifications or task breakdowns

### ✅ Our Solution: Specification-Driven Development

SpecPulse introduces **AI-Enhanced Specification-Driven Development**:

1. **Specifications First** - Clear, detailed specs before any code
2. **AI-Powered** - Your favorite AI assistant helps create and expand specs
3. **Structured Planning** - Break down features into manageable tasks
4. **Universal Integration** - Works across 8 major AI platforms
5. **CLI Foundation** - Reliable command-line structure with AI enhancement

---

## 🤖 Universal AI Platform Support

**SpecPulse works everywhere you work** - supporting 8 major AI platforms with identical functionality:

| Platform | Integration Type | Commands | Status |
|----------|------------------|----------|--------|
| **Claude Code** | Custom Slash Commands | `/sp-*` | ✅ Full Support |
| **Gemini CLI** | Custom Commands | `/sp-*` | ✅ Full Support |
| **Windsurf** | Custom Slash Commands | `/sp-*` | ✅ Full Support |
| **Cursor** | Custom Slash Commands | `/sp-*` | ✅ Full Support |
| **GitHub Copilot** | Custom Prompts | `.prompt.md` | ✅ Full Support |
| **OpenCode** | Agent-Based Workflow | `/sp-*` | ✅ Full Support |
| **Crush** | Category Commands | `/sp-*` | ✅ Full Support |
| **Qwen Code** | TOML Configuration | `/sp-*` | ✅ Full Support |

### 🔄 Identical Experience Across All Platforms

**The same 11 commands work everywhere** with identical functionality:

```bash
# These commands work identically on ALL 8 platforms:
/sp-pulse payment-system          # Initialize new feature - START HERE
/sp-spec "User authentication"    # Create specification
/sp-plan                          # Generate implementation plan
/sp-task                          # Break down into tasks
/sp-execute                       # Execute tasks continuously
/sp-status                        # Check progress
/sp-validate                      # Validate work
/sp-continue feature-id           # Switch to existing feature
/sp-decompose spec-id             # Decompose specifications
/sp-clarify spec-id               # Clarify requirements
/sp-llm-enforce [action]          # LLM compliance enforcement
```

**🎯 IMPORTANT: Always start with `/sp-pulse` - this is your entry point to everything!**

---

## 🎯 The Magic: How SpecPulse Works

### The CLI-AI Partnership

SpecPulse uses a revolutionary **CLI-First with AI Enhancement** approach:

```
You: /sp-spec "OAuth2 authentication system"
  ↓
Step 1: CLI Creates Foundation (Always Works)
   specpulse spec create "OAuth2 authentication system"
   ✓ Creates empty spec file
   ✓ Adds metadata and structure
   ✓ Updates project directories
  ↓
Step 2: AI Enhances Content (Safe Operations)
   AI reads created file
   AI adds detailed requirements and technical specs
   AI enhances with comprehensive documentation
  ↓
Result: Complete, detailed specification ready for development
```

### Why This Approach Is Game-Changing

**✅ CLI First:** Creates reliable, cross-platform structure that never fails
**✅ AI Enhanced:** Leverages AI for what it does best - detailed content creation
**✅ Fallback Protection:** Work continues even if CLI fails
**✅ Platform Independence:** Works identically on Windows, macOS, Linux
**✅ Safe Operations:** AI only works on files CLI has created

---

## 🚀 Getting Started: Your Complete First Project

Let's build your first feature with SpecPulse step by step:

### Step 1: Installation and Project Setup

```bash
# Install SpecPulse
pip install specpulse

# Create your first project (choosing your AI platform)
specpulse init my-awesome-project --ai claude
cd my-awesome-project
```

**Project Structure Created:**
```
my-awesome-project/
├── .specpulse/          # All your project data (specs, plans, tasks)
├── .claude/             # Claude Code commands (auto-deployed)
├── README.md
└── package.json
```

### Step 2: Initialize Your First Feature

```bash
# THE WAY TO START - AI-Powered Approach
# In your AI assistant (Claude, Gemini, Windsurf, Cursor, etc.):
/sp-pulse user-authentication
```

**What happens:**
- ✅ Creates feature directory: `specs/001-user-authentication/`
- ✅ Sets up project context and metadata
- ✅ Updates current working feature tracking
- ✅ Prepares structured environment for development
- ✅ Deploys AI platform-specific commands automatically

### Step 3: Create Detailed Specification

```bash
# In your AI assistant (Claude, Gemini, Windsurf, Cursor, etc.):
/sp-spec "OAuth2 authentication with JWT tokens"
```

**AI-powered specification includes:**
- 🎯 **Problem Statement**: Clear business problem and solution overview
- 🔧 **Functional Requirements**: Complete feature functionality
- 🔐 **Security Requirements**: Authentication, authorization, data protection
- 🎨 **User Experience**: UI/UX considerations and user flows
- 🔌 **API Design**: Endpoint specifications and data contracts
- 💾 **Data Models**: Database schemas and relationships
- ✅ **Acceptance Criteria**: How to verify the implementation works

### Step 4: Generate Implementation Plan

```bash
# In your AI assistant (works on all platforms):
/sp-plan
```

**AI generates comprehensive plan:**
- 🏗️ **Architecture Decisions**: Technology choices and system design
- 📁 **File Structure**: What files need to be created/modified
- 🔄 **Implementation Steps**: Sequential development approach
- 🔗 **Dependencies**: What needs to be built first
- ⏱️ **Time Estimates**: Realistic development timelines
- 🧪 **Testing Strategy**: How to ensure quality and reliability

### Step 5: Break Down into Development Tasks

```bash
# In your AI assistant:
/sp-task
```

**AI creates actionable tasks:**
```yaml
---
id: task-001
status: todo
title: "Set up authentication middleware"
description: |
  - What problem does this solve?: Foundation for secure route protection
  - Why is this necessary?: All protected endpoints require authentication
  - How will this be done?: Express middleware with JWT validation
  - When is this complete?: Middleware successfully validates tokens

files_touched:
  - path: src/middleware/auth.js
    reason: "JWT token validation middleware"

goals: ["Secure authentication middleware", "JWT token validation"]

success_criteria: ["Valid tokens pass", "Invalid tokens are rejected"]

dependencies: []
next_tasks: ["task-002", "task-003"]
---
```

### Step 6: Execute Tasks Continuously

```bash
# Execute next task and continue automatically
/sp-execute

# OR execute ALL tasks without stopping
/sp-execute all

# OR execute specific task
/sp-execute task-001
```

**What happens during execution:**
1. 🎯 **Task Selection**: Finds next pending task
2. 🔄 **Status Update**: Marks task as "in-progress"
3. 💻 **Implementation**: AI writes the actual code
4. ✅ **Validation**: Ensures requirements are met
5. 📝 **Documentation**: Updates task status and moves to next

### Step 7: Track Progress and Validate

```bash
# Check current progress
/sp-status

# Validate all work completed
/sp-validate
```

---

## 💡 Real-World Workflow Examples

### Example 1: E-commerce Payment System

```bash
# 1. Initialize payment feature
/sp-pulse payment-system

# 2. Create comprehensive specification
/sp-spec "Stripe integration with payment processing, refunds, and subscription management"

# 3. Generate detailed implementation plan
/sp-plan

# 4. Break into development tasks
/sp-task

# 5. Execute all tasks continuously
/sp-execute all

# 6. Review progress
/sp-status
```

**Result in 30 minutes:**
- ✅ Complete payment specification (12 pages)
- ✅ Implementation plan with 24 tasks
- ✅ Stripe integration code
- ✅ Payment processing logic
- ✅ Refund system
- ✅ Subscription management
- ✅ Error handling and logging
- ✅ Test suite with 95% coverage

### Example 2: Real-time Chat Application

```bash
# Team collaboration with different AI platforms:
# Backend developer uses Claude Code:
/sp-pulse realtime-chat
/sp-spec "WebSocket-based chat with rooms, typing indicators, and file sharing"

# Frontend developer uses Gemini CLI:
/sp-continue 001-chat
/sp-task

# DevOps engineer uses Windsurf:
/sp-execute task-005  # WebSocket server setup
```

**Result: Seamless collaboration across different AI platforms**

---

## 🎯 Complete AI Command Reference

### Feature Management Commands

#### `/sp-pulse <feature-name>`
**Initialize a new feature with intelligent suggestions**

```bash
# Examples
/sp-pulse user-authentication
/sp-pulse payment-gateway
/sp-pulse real-time-notifications
```

**What it does:**
- Creates feature directory structure
- Detects project type (web, mobile, API, etc.)
- Suggests specification approaches
- Sets up project context and metadata

#### `/sp-continue <feature-id>`
**Switch to existing feature**

```bash
# Examples
/sp-continue 001-auth
/sp-continue payment-system
/sp-continue 003-notifications
```

### Specification Commands

#### `/sp-spec create "<description>"`
**Create and expand detailed specification**

```bash
# Examples
/sp-spec create "User authentication with OAuth2 and JWT"
/sp-spec create "REST API for product catalog with filtering"
/sp-spec create "Real-time chat with WebSocket and rooms"
```

**AI generates complete specification with:**
- Business problem and solution overview
- Functional and non-functional requirements
- API contracts and data models
- Security and performance considerations
- User experience and interface design
- Acceptance criteria and success metrics

#### `/sp-spec validate <spec-id>`
**Validate specification completeness**

```bash
# Examples
/sp-spec validate spec-001
/sp-spec validate auth-spec
```

#### `/sp-spec expand <spec-id>`
**Expand existing specification with more details**

```bash
# Examples
/sp-spec expand spec-001
/sp-spec expand authentication-spec
```

### Planning Commands

#### `/sp-plan`
**Generate and expand implementation plan**

```bash
# Usage
/sp-plan

# AI creates:
# - Architecture decisions and technology choices
# - File structure and organization
# - Implementation steps in logical order
# - Dependencies and integration points
# - Time estimates and milestones
# - Risk assessment and mitigation strategies
```

#### `/sp-plan validate <plan-id>`
**Validate implementation plan**

```bash
# Examples
/sp-plan validate plan-001
/sp-plan validate auth-plan
```

### Task Management Commands

#### `/sp-task [plan-id]`
**Break plan into detailed, actionable tasks**

```bash
# Examples
/sp-task                    # Uses current plan
/sp-task plan-001          # Uses specific plan
/sp-task auth-plan         # Uses named plan
```

**Each task includes:**
- Clear problem statement and necessity
- Step-by-step implementation approach
- Files to be created/modified with reasons
- Success criteria and acceptance tests
- Dependencies and task relationships
- Risk assessment and mitigation
- MoSCoW priority breakdown (Must, Should, Could, Won't)
- Time and complexity estimates

#### `/sp-task validate <task-id>`
**Validate task completeness and correctness**

```bash
# Examples
/sp-task validate task-001
/sp-task validate auth-middleware
```

### Execution Commands

#### `/sp-execute [task-id|all]`
**Execute tasks continuously without stopping**

```bash
# Execute next pending task
/sp-execute

# Execute ALL pending tasks non-stop
/sp-execute all

# Execute specific task
/sp-execute task-001
/sp-execute auth-middleware
```

**Execution behavior:**
- Marks task as in-progress
- Implements requirements with code
- Validates against success criteria
- Updates task status to completed
- Automatically moves to next task
- Continues until all tasks done or blocked

### Progress and Validation Commands

#### `/sp-status`
**Show comprehensive project progress**

```bash
# Shows:
# - Overall completion percentage
# - Feature-by-feature progress
# - Task status breakdown (pending/in-progress/completed/blocked)
# - Current blockers and issues
# - Time estimates and velocity
# - Quality metrics and test coverage
```

#### `/sp-validate`
**Validate all project artifacts**

```bash
# Validates:
# - Specification completeness and quality
# - Plan feasibility and coverage
# - Task breakdown and dependencies
# - Code quality and test coverage
# - Documentation and standards compliance
```

### Advanced Commands

#### `/sp-decompose <spec-id>`
**Decompose specification into components**

```bash
# Examples
/sp-decompose spec-001
/sp-decompose auth-spec
```

**Useful for:**
- Microservices architecture design
- Component-based development
- Team distribution and parallel work
- Complex feature breakdown

#### `/sp-clarify <spec-id>`
**Clarify requirements and resolve ambiguities**

```bash
# Examples
/sp-clarify spec-001
/sp-clarify payment-spec
```

**Helps resolve:**
- Unclear requirements
- Missing details
- Conflicting specifications
- Implementation questions

#### `/sp-continue <feature-id>`
**Switch to existing feature and continue work**

```bash
# Examples
/sp-continue 001-auth
/sp-continue payment-system
/sp-continue 003-notifications
```

**Use this to:**
- Switch between different features
- Resume work on existing features
- Change context in multi-feature projects

#### `/sp-llm-enforce [action]`
**LLM compliance enforcement and monitoring**

```bash
# Start enforcement session (default)
/sp-llm-enforce

# Check compliance status
/sp-llm-enforce status

# Validate operations against rules
/sp-llm-enforce validate

# End enforcement session
/sp-llm-enforce end
```

**Ensures:**
- Directory traversal protection
- File operation security
- Content validation and sanitization
- Compliance with SpecPulse rules
- Audit trail generation

---

## 🏗️ Project Structure and Organization

### Complete Directory Structure

```
your-project/
├── .specpulse/                    # All SpecPulse data (git-tracked)
│   ├── specs/                     # Feature specifications
│   │   ├── 001-user-auth/
│   │   │   ├── spec-001.md       # Main specification
│   │   │   ├── decomposition/    # Service breakdown (if microservices)
│   │   │   └── references/       # External docs and links
│   │   ├── 002-payment-system/
│   │   └── ...
│   ├── plans/                     # Implementation plans
│   │   ├── 001-user-auth/
│   │   │   ├── plan-001.md       # Implementation plan
│   │   │   └── alternatives.md   # Alternative approaches
│   │   └── ...
│   ├── tasks/                     # Development tasks
│   │   ├── 001-user-auth/
│   │   │   ├── task-001.md       # Individual tasks
│   │   │   ├── task-002.md
│   │   │   └── task-summary.md   # Progress tracking
│   │   └── ...
│   ├── memory/                    # Project context and decisions
│   │   ├── context.md            # Current feature context
│   │   ├── decisions.md          # Architecture decisions
│   │   └── learning.md           # Team knowledge base
│   └── templates/                 # Customizable templates
│       ├── spec.md               # Specification template
│       ├── plan.md               # Planning template
│       └── task.md               # Task template
├── .claude/                       # Claude Code commands
├── .gemini/                       # Gemini CLI commands
├── .windsurf/                     # Windsurf AI workflows
├── .cursor/                       # Cursor AI commands
├── .github/prompts/               # GitHub Copilot prompts
├── .opencode/command/             # OpenCode AI commands
├── .crush/commands/sp/            # Crush AI commands
├── .qwen/commands/                # Qwen Code commands
└── your-project-files/            # Your actual project code
```

### What Gets Tracked vs. What's Generated

**✅ Tracked in Git (Important):**
- All specifications (`.specpulse/specs/`)
- Implementation plans (`.specpulse/plans/`)
- Task definitions and progress (`.specpulse/tasks/`)
- Project memory and decisions (`.specpulse/memory/`)
- Custom templates (`.specpulse/templates/`)

**🔄 Generated/Managed (Don't edit manually):**
- AI command deployments (`.claude/`, `.gemini/`, etc.)
- Temporary working files
- Auto-generated documentation

---

## 💻 Installation and Setup

### Project Initialization

```bash
# Install SpecPulse
pip install specpulse

# Create new project with AI integration
specpulse init my-project --ai claude

# Add AI support to existing project
specpulse init --here --ai gemini

# Check system health
specpulse doctor
```

---

## 🎯 Best Practices and Pro Tips

### Specification Writing Best Practices

**✅ DO:**
- Start with clear problem statement
- Include specific acceptance criteria
- Define user stories and use cases
- Specify error handling and edge cases
- Include performance and security requirements
- Add API contracts and data models
- Consider accessibility and internationalization

**❌ DON'T:**
- Write vague requirements like "make it fast"
- Skip error handling scenarios
- Forget about testing and validation
- Ignore user experience considerations
- Leave security as an afterthought

### Task Breakdown Best Practices

**✅ DO:**
- Break tasks into small, manageable chunks (2-8 hours each)
- Include clear success criteria for each task
- Define dependencies between tasks
- Consider parallel work opportunities
- Include testing and documentation tasks
- Plan for integration and deployment

**❌ DON'T:**
- Create tasks that are too large (over 16 hours)
- Forget about setup and configuration tasks
- Skip validation and testing tasks
- Ignore deployment and monitoring
- Leave dependencies undefined

### Team Collaboration Best Practices

**✅ DO:**
- Use feature branches for each feature
- Commit specifications and plans
- Review specifications as a team
- Use consistent task numbering
- Track progress with `/sp-status`
- Hold regular planning meetings

**❌ DON'T:**
- Work without specifications
- Skip code reviews
- Ignore task dependencies
- Forget about documentation
- Work in isolation without communication

---

## 🔄 Advanced Workflows and Patterns

### Microservices Architecture

```bash
# 1. Create monolithic specification first
/sp-pulse user-management
/sp-spec "Complete user management system with profiles, authentication, and preferences"

# 2. Decompose into services
/sp-decompose spec-001

# This creates:
# - User Service (profiles, preferences)
# - Auth Service (authentication, authorization)
# - Notification Service (emails, push notifications)
# - API Gateway (routing, rate limiting)

# 3. Generate service-specific tasks
/sp-task

# 4. Execute by service team
/sp-execute task-001  # User Service setup
/sp-execute task-005  # Auth Service setup
```

### Legacy System Modernization

```bash
# 1. Document existing system
/sp-pulse legacy-modernization
/sp-spec "Modernize legacy monolith to microservices: current state analysis and migration strategy"

# 2. Create migration plan
/sp-plan

# 3. Break into migration phases
/sp-task

# 4. Execute migration incrementally
/sp-execute task-001  # Phase 1: Strangler Fig pattern setup
/sp-execute task-002  # Phase 2: Extract user management
```

### API-First Development

```bash
# 1. Design API first
/sp-pulse product-catalog-api
/sp-spec "REST API for product catalog with CRUD operations, search, filtering, and pagination"

# 2. Generate OpenAPI specification
# (AI includes OpenAPI spec in the generated specification)

# 3. Create implementation plan
/sp-plan

# 4. Implement API
/sp-execute all
```

### Mobile App Development

```bash
# 1. Define mobile app features
/sp-pulse mobile-expense-tracker
/sp-spec "Mobile expense tracking app with receipt scanning, categorization, and reporting"

# 2. Plan platform-specific implementation
/sp-plan

# 3. Break into platform-specific tasks
/sp-task

# 4. Develop by platform
/sp-execute task-001  # React Native setup
/sp-execute task-005  # iOS-specific features
/sp-execute task-010  # Android-specific features
```

---

## 🛠️ Configuration and Customization

### Custom Templates

Create your own templates for consistent project standards:

```bash
# Create custom specification template
specpulse template create enterprise-spec --type spec

# Edit the template
# .specpulse/templates/enterprise-spec.md

# Use custom template
/sp-spec "New feature" --template enterprise-spec
```

### Project Configuration

Customize SpecPulse behavior for your project:

```yaml
# .specpulse/config.yml
project:
  name: "My Enterprise App"
  type: "web"
  team_size: 5

specifications:
  template: "enterprise-spec"
  required_sections:
    - "problem_statement"
    - "requirements"
    - "api_design"
    - "security"
    - "testing"

tasks:
  default_estimates:
    simple: 4    # hours
    medium: 8    # hours
    complex: 16  # hours

ai_preferences:
  code_style: "enterprise"
  testing_framework: "jest"
  documentation_style: "jsdoc"
```

## 🎯 Success Stories and Use Cases

### Startup MVP Development

**Challenge:** Build and launch MVP in 6 weeks with 2 developers
**Solution:** SpecPulse with Claude Code integration

```bash
Week 1: Feature Planning
/sp-pulse user-management
/sp-pulse product-catalog
/sp-pulse order-processing

Week 2-3: Specification and Planning
/sp-spec "Complete user management system"
/sp-spec "Product catalog with search and filtering"
/sp-spec "Order processing with payment integration"
/sp-plan

Week 4-5: Development
/sp-task
/sp-execute all

Week 6: Testing and Deployment
/sp-validate
```

**Result:** MVP launched on time with all core features, 95% test coverage

### Enterprise System Migration

**Challenge:** Migrate 500k+ LOC monolith to microservices over 12 months
**Solution:** SpecPulse with team-wide AI integration

```bash
Phase 1: Analysis (1 month)
/sp-pulse legacy-analysis
/sp-spec "Complete monolith analysis and service decomposition strategy"

Phase 2: Pilot (2 months)
/sp-pulse user-service-migration
/sp-execute all

Phase 3: Full Migration (9 months)
# Multiple teams working in parallel
# Each team uses /sp-continue to work on their services
```

**Result:** Migration completed on schedule with zero downtime, improved performance by 300%

### Open Source Project Development

**Challenge:** Coordinate 50+ contributors across different time zones
**Solution:** SpecPulse with GitHub Copilot integration

```bash
# Contributors use GitHub Copilot with /sp-* commands
# All specifications and plans tracked in .specpulse/
# Clear task breakdown enables parallel work
/sp-status shows overall project progress
```

**Result:** Development velocity increased by 200%, contributor satisfaction improved

---

## 🔧 Technical Requirements and Compatibility

### System Requirements

- **Python:** 3.11 or higher
- **Operating System:** Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Memory:** 4GB RAM minimum, 8GB recommended
- **Storage:** 100MB for SpecPulse + project data

### AI Platform Requirements

**Compatible AI Platforms:**
- **Claude Code** (Anthropic)
- **Gemini CLI** (Google)
- **Windsurf AI** (Windsurf)
- **Cursor AI** (Cursor)
- **GitHub Copilot** (Microsoft)
- **OpenCode AI** (OpenCode)
- **Crush AI** (Crush)
- **Qwen Code** (Alibaba)


## 🚀 Performance and Scalability

### Benchmarks

**Project Initialization:**
- Small project (< 100 files): < 2 seconds
- Medium project (100-1000 files): < 5 seconds
- Large project (1000+ files): < 10 seconds

**Specification Generation:**
- Simple feature: 30-60 seconds
- Complex feature: 2-5 minutes
- Enterprise system: 5-15 minutes

**Task Breakdown:**
- Small plan (< 10 tasks): < 30 seconds
- Medium plan (10-50 tasks): 1-2 minutes
- Large plan (50+ tasks): 2-5 minutes

### Scalability Considerations

**Recommended Project Sizes:**
- **Small Projects:** < 50 tasks, < 10 specifications
- **Medium Projects:** 50-500 tasks, 10-50 specifications
- **Large Projects:** 500+ tasks, 50+ specifications
- **Enterprise:** Multiple teams, 1000+ tasks

**Performance Optimization:**
- Use SSD storage for faster file operations
- Enable file system indexing for large projects
- Use parallel task execution for independent tasks
- Regular cleanup of old completed tasks

---

## 🔒 Security and Privacy

### Privacy-First Design

**SpecPulse respects your privacy:**
- ✅ **No external API calls** - Everything runs locally
- ✅ **No data transmission** - Your specifications never leave your system
- ✅ **No telemetry** - We don't track usage or project data
- ✅ **Local AI integration** - AI assistants work with your local files only

### Security Best Practices

**File Security:**
- All files created with appropriate permissions
- Sensitive data handling in specifications
- Secure temporary file management
- Path traversal protection

**Code Security:**
- Input validation and sanitization
- Template injection protection
- Safe file operation practices
- Dependency security scanning

**Team Security:**
- Git-based access control
- Specification review workflows
- Audit trail for all changes
- Role-based access patterns

### Enterprise Security Features

**For Enterprise Deployments:**
- Air-gapped installation support
- Custom template encryption
- Audit logging and compliance
- Integration with enterprise SSO
- Custom security policies

---

## 🆘 Troubleshooting and Support

### Common Issues and Solutions

**Issue: Command not found**
```bash
# Solution: Verify installation
pip show specpulse
python -m specpulse --version

# Reinstall if needed
pip uninstall specpulse
pip install specpulse
```

**Issue: AI commands not working**
```bash
# Solution: Check AI platform integration
specpulse doctor --fix

# Manually deploy commands
specpulse init --here --ai claude  # Redeploy commands
```

**Issue: File permission errors**
```bash
# Solution: Check permissions
ls -la .specpulse/
chmod 755 .specpulse/
chmod 644 .specpulse/specs/*.md
```

**Issue: Git integration problems**
```bash
# Solution: Initialize git repository
git init
git add .
git commit -m "Initial SpecPulse setup"
```

### Getting Help

**Self-Service:**
```bash
# General help
specpulse --help

# Command-specific help
specpulse feature --help
specpulse spec --help

# Health check and diagnostics
specpulse doctor
```

**Community Support:**
- **GitHub Issues:** [Report bugs and request features](https://github.com/specpulse/specpulse/issues)
- **GitHub Discussions:** [Community questions and discussions](https://github.com/specpulse/specpulse/discussions)
- **Documentation:** Available in the project repository

### Debug Mode

**Enable detailed logging:**
```bash
# Enable debug mode
export SPECPULSE_DEBUG=1

# Or for Windows
set SPECPULSE_DEBUG=1

# Run commands with debug output
specpulse doctor
```

**Debug file locations:**
- Logs: `.specpulse/logs/debug.log`
- Cache: `.specpulse/cache/`
- Temp: `.specpulse/tmp/`

---

## 🤝 Contributing to SpecPulse

### Development Setup

```bash
# Clone repository
git clone https://github.com/specpulse/specpulse.git
cd specpulse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=specpulse --cov-report=html
```

### Contribution Guidelines

**We welcome contributions!**

**Areas for contribution:**
- 🐛 **Bug fixes:** Help us squash bugs
- ✨ **New features:** Propose and implement new functionality
- 📚 **Documentation:** Improve documentation and examples
- 🧪 **Testing:** Add test cases and improve test coverage
- 🔧 **Tools:** Development tools and integrations

**Development Process:**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open Pull Request

### Code Style and Standards

**Python Code Style:**
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Use isort for import sorting
- Type hints required for new code
- Maximum line length: 88 characters

**Documentation Style:**
- Use clear, concise language
- Include code examples
- Follow Markdown formatting standards
- Include proper section headers
- Add ALT text for images

**Testing Standards:**
- Write unit tests for all new functionality
- Aim for high code coverage (>90%)
- Use descriptive test names
- Include edge case testing
- Mock external dependencies

---

## 📄 License and Legal

### License

SpecPulse is released under the **MIT License**. You can find the full license text in the [LICENSE](LICENSE) file.

**What this means:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ Liability and warranty disclaimed

## 🎉 Ready to Transform Your Development?

### Get Started in 5 Minutes

```bash
# 1. Install SpecPulse
pip install specpulse

# 2. Create your first project
specpulse init my-project --ai claude
cd my-project

# 3. Start your first feature (THE ENTRY POINT)
/sp-pulse amazing-feature

# 4. Create your first specification
/sp-spec "Build an amazing feature that will wow users"

# 5. Plan and execute
/sp-plan
/sp-task
/sp-execute all

# 6. Celebrate your success!
🎉
```

### Join the Community

- **GitHub:** [github.com/specpulse/specpulse](https://github.com/specpulse/specpulse)
- **Developer:** [Ersin KOÇ](https://github.com/ersinkoc) • [x.com/ersinkoc](https://x.com/ersinkoc)

### Need Help?

- **Website:** [specpulse.xyz](https://specpulse.xyz) for full documentation
- **Support:** [Create an issue](https://github.com/specpulse/specpulse/issues)
- **Contact:** [info@specpulse.xyz](mailto:info@specpulse.xyz) for business inquiries

---

<div align="center">

**[⭐ Star us on GitHub](https://github.com/specpulse/specpulse) • [📦 Install from PyPI](https://pypi.org/project/specpulse/) **

**Made with ❤️ by developers who believe in specifications-first development**

**SpecPulse v2.7.1** - Building the future of software development, together.

</div>