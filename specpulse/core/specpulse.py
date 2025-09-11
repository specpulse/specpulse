"""
SpecPulse Core Implementation
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import yaml
import json
import os



class SpecPulse:
    """Core SpecPulse functionality"""
    
    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path or Path.cwd()
        self.config = self._load_config()
        # Get resource directory path
        self.resources_dir = Path(__file__).parent.parent / "resources"
    
    def _load_config(self) -> Dict:
        """Load project configuration"""
        config_path = self.project_path / ".specpulse" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def get_spec_template(self) -> str:
        """Get specification template from file"""
        template_path = self.resources_dir / "templates" / "spec.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded template if file not found
        return """<!-- SpecPulse Specification Template v1.0 -->
<!-- AI Instructions: Fill this template based on user description -->

# Specification: [FEATURE_NAME]

## Metadata
- **ID**: SPEC-[XXX]
- **Created**: [DATE]
- **Author**: [USER]
- **AI Assistant**: [CLAUDE|GEMINI]
- **Version**: 1.0.0

## Executive Summary
[One paragraph description of what this feature does and why it's needed]

## Problem Statement
[Detailed description of the problem being solved]

## Proposed Solution
[High-level approach to solving the problem]

## Detailed Requirements

### Functional Requirements
<!-- AI: Generate numbered list of specific, testable requirements -->

FR-001: [Requirement]
  - Acceptance: [How to verify this requirement is met]
  - Priority: [MUST|SHOULD|COULD]

### Non-Functional Requirements

#### Performance
- Response Time: [Target]
- Throughput: [Target]
- Resource Usage: [Limits]

#### Security
- Authentication: [Method]
- Authorization: [Model]
- Data Protection: [Requirements]

#### Scalability
- User Load: [Target]
- Data Volume: [Target]
- Geographic Distribution: [Requirements]

## User Stories

<!-- AI: Generate user stories in standard format -->

### Story 1: [Title]
**As a** [user type]
**I want** [action/feature]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Technical Constraints
<!-- List any technical limitations or requirements -->

## Dependencies
<!-- External services, libraries, or other features required -->

## Risks and Mitigations
<!-- Identify potential risks and how to address them -->

## Open Questions
<!-- Mark with [NEEDS CLARIFICATION] for items requiring user input -->

## Appendix
<!-- Additional diagrams, mockups, or references -->
"""
    
    def get_plan_template(self) -> str:
        """Get implementation plan template from file"""
        template_path = self.resources_dir / "templates" / "plan.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded template if file not found
        return """<!-- SpecPulse Implementation Plan Template v1.0 -->
<!-- AI Instructions: Generate plan from specification -->

# Implementation Plan: [FEATURE_NAME]

## Specification Reference
- **Spec ID**: SPEC-[XXX]
- **Generated**: [DATE]
- **Optimization Focus**: [PERFORMANCE|SECURITY|SIMPLICITY|COST]

## Architecture Overview
```mermaid
<!-- AI: Generate architecture diagram -->
```

## Technology Stack

### Core Technologies
- **Language**: [Choice with rationale]
- **Framework**: [Choice with rationale]
- **Database**: [Choice with rationale]
- **Cache**: [Choice with rationale]

### Supporting Tools
- **Testing**: [Framework choice]
- **CI/CD**: [Platform choice]
- **Monitoring**: [Solution choice]

## Implementation Phases

### Phase 0: Setup and Prerequisites
**Duration**: [Estimate]
**Tasks**:
1. Environment setup
2. Repository initialization
3. Dependency installation
4. Configuration

### Phase 1: Data Layer
**Duration**: [Estimate]
**Deliverables**:
- Database schema
- Migration scripts
- Data models
- Repository pattern implementation

**Tasks**:
1. Design database schema
2. Create migration scripts
3. Implement data models
4. Create repository interfaces
5. Write data layer tests

### Phase 2: Business Logic
**Duration**: [Estimate]
**Deliverables**:
- Service layer
- Business rules implementation
- Validation logic

**Tasks**:
1. Implement service interfaces
2. Create business logic modules
3. Add validation rules
4. Implement error handling
5. Write unit tests

### Phase 3: API Layer
**Duration**: [Estimate]
**Deliverables**:
- REST/GraphQL endpoints
- API documentation
- Authentication/Authorization

**Tasks**:
1. Design API contracts
2. Implement endpoints
3. Add authentication
4. Create API documentation
5. Write integration tests

### Phase 4: Testing and Optimization
**Duration**: [Estimate]
**Deliverables**:
- Complete test suite
- Performance optimization
- Security hardening

**Tasks**:
1. Complete test coverage
2. Performance testing
3. Security audit
4. Load testing
5. Documentation

## File Structure
```
[feature-name]/
├── src/
│   ├── models/
│   ├── services/
│   ├── controllers/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
└── config/
```

## API Contracts

### Endpoint: [ENDPOINT_NAME]
```yaml
method: POST
path: /api/v1/[resource]
request:
  headers:
    Content-Type: application/json
    Authorization: Bearer {token}
  body:
    field1: string
    field2: number
response:
  200:
    success: true
    data: object
  400:
    error: string
```

## Data Models

### Entity: [ENTITY_NAME]
```yaml
fields:
  id: uuid
  created_at: timestamp
  updated_at: timestamp
  [field_name]: [type]
relations:
  [relation_name]: [type]
indexes:
  - [field_name]
```

## Testing Strategy

### Unit Tests
- Coverage Target: 80%
- Framework: [Choice]
- Mock Strategy: [Approach]

### Integration Tests
- API Contract Tests
- Database Integration Tests
- External Service Tests

### E2E Tests
- Critical User Journeys
- Performance Benchmarks
- Security Scenarios

## Constitution Compliance

### Principle Validation
- [ ] Single Responsibility: Each component has one purpose
- [ ] Test-First: Tests written before implementation
- [ ] Documentation: All code is documented
- [ ] Security: Security considered by design
- [ ] Performance: Meets performance targets

## Risk Assessment

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | [H/M/L] | [H/M/L] | [Strategy] |

### Timeline Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | [H/M/L] | [H/M/L] | [Strategy] |

## Success Criteria
- [ ] All functional requirements implemented
- [ ] Test coverage > 80%
- [ ] Performance targets met
- [ ] Security audit passed
- [ ] Documentation complete
"""
    
    def get_task_template(self) -> str:
        """Get task list template from file"""
        template_path = self.resources_dir / "templates" / "task.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded template if file not found
        return """<!-- SpecPulse Task List Template v1.0 -->
<!-- AI Instructions: Generate from implementation plan -->

# Task List: [FEATURE_NAME]

## Metadata
- **Plan Reference**: [PLAN_ID]
- **Total Tasks**: [COUNT]
- **Estimated Duration**: [TOTAL_HOURS]
- **Parallel Groups**: [COUNT]

## Task Organization

### 🔄 Parallel Group A
*These tasks can be executed simultaneously*

#### TASK-001: [Task Name]
- **Type**: [setup|development|testing|documentation]
- **Priority**: [HIGH|MEDIUM|LOW]
- **Estimate**: [hours]
- **Dependencies**: None
- **Description**: [What needs to be done]
- **Acceptance**: [How to verify completion]
- **Assignable**: [role/skill required]

#### TASK-002: [Task Name]
[Same structure as above]

### 📝 Sequential Tasks
*These tasks must be completed in order*

#### TASK-003: [Task Name]
- **Dependencies**: TASK-001
[Rest of structure]

### 🎯 Critical Path
*Tasks that directly impact timeline*

1. TASK-001 → TASK-003 → TASK-007
2. Estimated critical path duration: [hours]

## Task Details

### Development Tasks
- [ ] TASK-XXX: Implement [component]
- [ ] TASK-XXX: Create [feature]
- [ ] TASK-XXX: Integrate [service]

### Testing Tasks
- [ ] TASK-XXX: Write unit tests for [component]
- [ ] TASK-XXX: Create integration tests
- [ ] TASK-XXX: Perform security testing

### Documentation Tasks
- [ ] TASK-XXX: Document API endpoints
- [ ] TASK-XXX: Create user guide
- [ ] TASK-XXX: Update README

## Execution Schedule

### Day 1-2
- Morning: TASK-001, TASK-002 (parallel)
- Afternoon: TASK-003

### Day 3-4
- Morning: TASK-004
- Afternoon: TASK-005, TASK-006

## Progress Tracking
```yaml
status:
  total: [count]
  completed: 0
  in_progress: 0
  blocked: 0
  
metrics:
  velocity: [tasks/day]
  estimated_completion: [date]
  blockers: []
```
"""
    
    def get_constitution_template(self) -> str:
        """Get constitution template from file"""
        template_path = self.resources_dir / "memory" / "constitution.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded template if file not found
        return """# Project Constitution

## Immutable Principles

### Principle 1: Simplicity First
Every solution must start with the simplest approach that could work.
Complexity is added only when proven necessary.

### Principle 2: Test-Driven Development
No production code without tests.
Tests are written first, implementation follows.

### Principle 3: Single Responsibility
Each module, function, and component does one thing well.
If you need "and" to describe it, split it.

### Principle 4: Documentation as Code
Documentation lives with code.
If it's not documented, it doesn't exist.

### Principle 5: Security by Design
Security is not an afterthought.
Every feature considers security implications from the start.

## Technical Standards

### Code Style
- Python: PEP 8 with type hints
- JavaScript: StandardJS
- Go: Official Go formatting

### Testing Requirements
- Minimum 80% code coverage
- All API endpoints must have contract tests
- Critical paths require E2E tests

### Performance Targets
- API response time: < 200ms (p95)
- Page load time: < 2 seconds
- Database queries: < 50ms

### Security Requirements
- All data encrypted in transit (TLS 1.3+)
- Sensitive data encrypted at rest
- Authentication: OAuth 2.0 / JWT
- Authorization: RBAC with least privilege

## Architecture Rules

### Service Boundaries
- Services communicate only through defined APIs
- No shared databases between services
- Each service owns its data

### Data Management
- Single source of truth for each data type
- Event sourcing for audit requirements
- CQRS where read/write patterns differ

### Error Handling
- All errors are handled explicitly
- User-facing errors are helpful and actionable
- System errors are logged with context

## Amendment Process

Changes to this constitution require:
1. Documented rationale
2. Team consensus
3. Gradual migration plan
4. Update to all affected documentation
"""
    
    def get_context_template(self) -> str:
        """Get context template from file"""
        template_path = self.resources_dir / "memory" / "context.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded template if file not found
        return """# Project Context

## Current State
Last Updated: [AI updates this automatically]

### Active Features
1. **[feature-name]** (SPEC-XXX)
   - Status: [Phase]
   - Branch: [branch-name]
   - Blockers: [None|List]

### Recent Decisions
- [Decision with rationale]

### Known Issues
- [Issue description]

## Team Preferences

### Technology Choices
- **Preferred Stack**: [Stack]
- **Testing**: [Framework]
- **CI/CD**: [Platform]
- **Deployment**: [Method]

### Coding Patterns
- [Pattern preference]

## Project Glossary

### Domain Terms
- **[Term]**: [Definition]

### Technical Terms
- **[Term]**: [Definition]
"""
    
    def get_decisions_template(self) -> str:
        """Get architectural decisions template from file"""
        template_path = self.resources_dir / "memory" / "decisions.md"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded template if file not found
        return """# Architectural Decisions

## Decision Log

### ADR-001: [Title]
**Date**: [DATE]
**Status**: [PROPOSED|ACCEPTED|DEPRECATED]
**Context**: [Why this decision was needed]
**Decision**: [What was decided]
**Consequences**: [What happens as a result]
**Alternatives Considered**: [Other options that were evaluated]

---

### ADR-002: [Title]
[Same structure as above]
"""
    
    def get_setup_script(self) -> str:
        """Get pulse-init script for feature initialization from file"""
        script_path = self.resources_dir / "scripts" / "pulse-init.sh"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded script if file not found
        return """#!/bin/bash
# SpecPulse Feature Initialization Script

set -e

# Get feature name from argument
FEATURE_NAME="$1"
if [ -z "$FEATURE_NAME" ]; then
    echo "Error: Feature name required"
    exit 1
fi

# Clean feature name (replace spaces with hyphens, lowercase)
CLEAN_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr '_' '-')

# Get next feature number
if [ -d "specs" ]; then
    FEATURE_NUM=$(find specs -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | wc -l)
    FEATURE_NUM=$((FEATURE_NUM + 1))
else
    FEATURE_NUM=1
fi

# Format with leading zeros
FEATURE_ID=$(printf "%03d" $FEATURE_NUM)
BRANCH_NAME="${FEATURE_ID}-${CLEAN_NAME}"

# Create directories
mkdir -p "specs/${BRANCH_NAME}"
mkdir -p "plans/${BRANCH_NAME}"
mkdir -p "tasks/${BRANCH_NAME}"

# Create feature branch if git is available
if command -v git &> /dev/null && [ -d ".git" ]; then
    git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"
fi

# Output JSON result
echo "{"
echo "  \\"branch_name\\": \\"$BRANCH_NAME\\","
echo "  \\"feature_id\\": \\"$FEATURE_ID\\","
echo "  \\"spec_dir\\": \\"specs/$BRANCH_NAME\\","
echo "  \\"plan_dir\\": \\"plans/$BRANCH_NAME\\","
echo "  \\"task_dir\\": \\"tasks/$BRANCH_NAME\\""
echo "}"
"""
    
    def get_spec_script(self) -> str:
        """Get pulse-spec script for getting current feature context from file"""
        script_path = self.resources_dir / "scripts" / "pulse-spec.sh"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded script if file not found
        return """#!/bin/bash
# SpecPulse Spec Context Script

# Check for --current flag
if [ "$1" == "--current" ]; then
    # Find the current feature branch
    if command -v git &> /dev/null && [ -d ".git" ]; then
        BRANCH=$(git branch --show-current)
        if [[ "$BRANCH" =~ ^[0-9]{3}-.* ]]; then
            FEATURE_DIR="specs/$BRANCH"
            if [ -d "$FEATURE_DIR" ]; then
                echo "{"
                echo "  \\"branch\\": \\"$BRANCH\\","
                echo "  \\"spec_file\\": \\"$FEATURE_DIR/spec.md\\","
                echo "  \\"spec_dir\\": \\"$FEATURE_DIR\\""
                echo "}"
                exit 0
            fi
        fi
    fi
    
    # Fallback: find latest spec directory
    LATEST=$(find specs -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | sort -r | head -1)
    if [ -n "$LATEST" ]; then
        echo "{"
        echo "  \\"branch\\": \\"$(basename $LATEST)\\","
        echo "  \\"spec_file\\": \\"$LATEST/spec.md\\","
        echo "  \\"spec_dir\\": \\"$LATEST\\""
        echo "}"
    else
        echo "{\\"error\\": \\"No active feature found\\"}"
        exit 1
    fi
fi
"""
    
    def get_plan_script(self) -> str:
        """Get pulse-plan script for plan context from file"""
        script_path = self.resources_dir / "scripts" / "pulse-plan.sh"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded script if file not found
        return """#!/bin/bash
# SpecPulse Plan Context Script

# Check for --current flag
if [ "$1" == "--current" ]; then
    # Find the current feature branch
    if command -v git &> /dev/null && [ -d ".git" ]; then
        BRANCH=$(git branch --show-current)
        if [[ "$BRANCH" =~ ^[0-9]{3}-.* ]]; then
            SPEC_DIR="specs/$BRANCH"
            PLAN_DIR="plans/$BRANCH"
            if [ -d "$SPEC_DIR" ]; then
                echo "{"
                echo "  \\"branch\\": \\"$BRANCH\\","
                echo "  \\"spec_file\\": \\"$SPEC_DIR/spec.md\\","
                echo "  \\"plan_file\\": \\"$PLAN_DIR/plan.md\\","
                echo "  \\"plan_dir\\": \\"$PLAN_DIR\\""
                echo "}"
                exit 0
            fi
        fi
    fi
    
    # Fallback: find latest directories
    LATEST=$(find specs -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | sort -r | head -1)
    if [ -n "$LATEST" ]; then
        BRANCH=$(basename "$LATEST")
        echo "{"
        echo "  \\"branch\\": \\"$BRANCH\\","
        echo "  \\"spec_file\\": \\"specs/$BRANCH/spec.md\\","
        echo "  \\"plan_file\\": \\"plans/$BRANCH/plan.md\\","
        echo "  \\"plan_dir\\": \\"plans/$BRANCH\\""
        echo "}"
    else
        echo "{\\"error\\": \\"No active feature found\\"}"
        exit 1
    fi
fi
"""
    
    def get_task_script(self) -> str:
        """Get pulse-task script for task context from file"""
        script_path = self.resources_dir / "scripts" / "pulse-task.sh"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()
        # Fallback to embedded script if file not found
        return """#!/bin/bash
# SpecPulse Task Context Script

# Check for --current flag
if [ "$1" == "--current" ]; then
    # Find the current feature branch
    if command -v git &> /dev/null && [ -d ".git" ]; then
        BRANCH=$(git branch --show-current)
        if [[ "$BRANCH" =~ ^[0-9]{3}-.* ]]; then
            SPEC_DIR="specs/$BRANCH"
            PLAN_DIR="plans/$BRANCH"
            TASK_DIR="tasks/$BRANCH"
            if [ -d "$SPEC_DIR" ]; then
                echo "{"
                echo "  \\"branch\\": \\"$BRANCH\\","
                echo "  \\"spec_file\\": \\"$SPEC_DIR/spec.md\\","
                echo "  \\"plan_file\\": \\"$PLAN_DIR/plan.md\\","
                echo "  \\"task_file\\": \\"$TASK_DIR/tasks.md\\","
                echo "  \\"task_dir\\": \\"$TASK_DIR\\""
                echo "}"
                exit 0
            fi
        fi
    fi
    
    # Fallback: find latest directories
    LATEST=$(find specs -maxdepth 1 -type d -name "[0-9][0-9][0-9]-*" | sort -r | head -1)
    if [ -n "$LATEST" ]; then
        BRANCH=$(basename "$LATEST")
        echo "{"
        echo "  \\"branch\\": \\"$BRANCH\\","
        echo "  \\"spec_file\\": \\"specs/$BRANCH/spec.md\\","
        echo "  \\"plan_file\\": \\"plans/$BRANCH/plan.md\\","
        echo "  \\"task_file\\": \\"tasks/$BRANCH/tasks.md\\","
        echo "  \\"task_dir\\": \\"tasks/$BRANCH\\""
        echo "}"
    else
        echo "{\\"error\\": \\"No active feature found\\"}"
        exit 1
    fi
fi
"""
    
    def get_validate_script(self) -> str:
        """Get validation script"""
        return """#!/bin/bash
# SpecPulse Validation Script

validate_spec() {
    local spec_file=$1
    local errors=0
    
    echo "Validating: $spec_file"
    
    # Check required sections
    if ! grep -q "## Requirements" $spec_file; then
        echo "  ❌ Missing Requirements section"
        ((errors++))
    fi
    
    if ! grep -q "## User Stories" $spec_file; then
        echo "  ❌ Missing User Stories section"
        ((errors++))
    fi
    
    if ! grep -q "## Acceptance Criteria" $spec_file; then
        echo "  ❌ Missing Acceptance Criteria section"
        ((errors++))
    fi
    
    # Check for clarification markers
    if grep -q "\\[NEEDS CLARIFICATION\\]" $spec_file; then
        echo "  ⚠️  Contains items needing clarification"
    fi
    
    if [ $errors -eq 0 ]; then
        echo "  ✅ Specification valid"
        return 0
    else
        echo "  ❌ Specification has $errors errors"
        return 1
    fi
}

# Main
if [ "$1" == "spec" ]; then
    validate_spec $2
elif [ "$1" == "all" ]; then
    for spec in specs/*/spec.md; do
        validate_spec $spec
    done
fi
"""
    
    def get_generate_script(self) -> str:
        """Get generation script"""
        return """#!/bin/bash
# SpecPulse Generation Script

generate_from_template() {
    local template=$1
    local output=$2
    local feature_name=$3
    
    # Replace placeholders
    sed "s/\\[FEATURE_NAME\\]/$feature_name/g" $template > $output
    sed -i "s/\\[DATE\\]/$(date +%Y-%m-%d)/g" $output
    sed -i "s/\\[XXX\\]/$(printf '%03d' $RANDOM)/g" $output
    
    echo "Generated: $output"
}

# Main
if [ "$1" == "spec" ]; then
    generate_from_template templates/spec.md $2 $3
elif [ "$1" == "plan" ]; then
    generate_from_template templates/plan.md $2 $3
elif [ "$1" == "task" ]; then
    generate_from_template templates/task.md $2 $3
fi
"""
    
    def get_claude_instructions(self) -> str:
        """Get Claude instructions"""
        return """# SpecPulse Commands for Claude

You have access to SpecPulse commands for specification-driven development.

## Available Commands

### /pulse init <feature-name>
Initializes a new feature with proper structure.
- Creates feature branch
- Sets up specification directory
- Loads templates
- Updates context

### /spec create <description>
Creates a detailed specification from description.
- Use the template in templates/spec.md
- Mark uncertainties with [NEEDS CLARIFICATION]
- Ensure all sections are complete
- Validate against constitution

### /plan generate
Generates implementation plan from current specification.
- Read the active specification
- Create detailed phases
- Include technology decisions
- Add time estimates

### /task breakdown
Creates task list from implementation plan.
- Identify dependencies
- Mark parallel tasks with [P]
- Add time estimates
- Create critical path

### /validate <component>
Validates specifications, plans, or project.
- Check completeness
- Verify consistency
- Ensure constitution compliance

## Workflow

1. User requests feature → Use `/pulse init`
2. User describes requirements → Use `/spec create`
3. Specification complete → Use `/plan generate`
4. Plan approved → Use `/task breakdown`
5. Before implementation → Use `/validate all`

## Constitution Rules

Always enforce these principles:
1. Simplicity first
2. Test-driven development
3. Single responsibility
4. Documentation as code
5. Security by design

## Context Management

- Read `memory/context.md` for project state
- Update context after major decisions
- Check `memory/constitution.md` for principles
- Reference previous specs for consistency

## Templates

Always use templates from `templates/` directory:
- `spec.md` for specifications
- `plan.md` for implementation plans
- `task.md` for task lists

## Best Practices

1. Always validate before moving to next phase
2. Keep specifications testable and measurable
3. Update context.md with decisions
4. Create atomic, focused commits
5. Document rationale for technology choices
"""
    
    # Claude command getters
    def get_claude_pulse_command(self) -> str:
        """Get Claude pulse command"""
        command_path = self.resources_dir / "commands" / "claude" / "pulse.md"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# /pulse command not found"
    
    def get_claude_spec_command(self) -> str:
        """Get Claude spec command"""
        command_path = self.resources_dir / "commands" / "claude" / "spec.md"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# /spec command not found"
    
    def get_claude_plan_command(self) -> str:
        """Get Claude plan command"""
        command_path = self.resources_dir / "commands" / "claude" / "plan.md"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# /plan command not found"
    
    def get_claude_task_command(self) -> str:
        """Get Claude task command"""
        command_path = self.resources_dir / "commands" / "claude" / "task.md"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# /task command not found"
    
    # Gemini command getters
    def get_gemini_pulse_command(self) -> str:
        """Get Gemini pulse command"""
        command_path = self.resources_dir / "commands" / "gemini" / "pulse.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# Gemini pulse command not found"
    
    def get_gemini_spec_command(self) -> str:
        """Get Gemini spec command"""
        command_path = self.resources_dir / "commands" / "gemini" / "spec.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# Gemini spec command not found"
    
    def get_gemini_plan_command(self) -> str:
        """Get Gemini plan command"""
        command_path = self.resources_dir / "commands" / "gemini" / "plan.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# Gemini plan command not found"
    
    def get_gemini_task_command(self) -> str:
        """Get Gemini task command"""
        command_path = self.resources_dir / "commands" / "gemini" / "task.toml"
        if command_path.exists():
            with open(command_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "# Gemini task command not found"
    
    def get_gemini_instructions(self) -> str:
        """Get Gemini instructions"""
        return """# SpecPulse Commands for Gemini CLI

This project uses SpecPulse for specification-driven development.

## Command Reference

### Initialization
```
/pulse init <feature-name>
```
Creates new feature structure and branch.

### Specification Creation
```
/spec create <description>
```
Generates detailed specification from natural language.

Required sections:
- Requirements (functional and non-functional)
- User stories with acceptance criteria
- Technical constraints
- Dependencies
- Risks and mitigations

### Plan Generation
```
/plan generate [--optimize <focus>]
```
Creates implementation plan from specification.

Optimization options:
- performance: Speed and efficiency focus
- security: Security-first approach
- simplicity: Maintainable solution
- cost: Resource optimization

### Task Breakdown
```
/task breakdown [--parallel]
```
Generates actionable task list.

Features:
- Dependency detection
- Parallel task identification
- Time estimation
- Critical path analysis

### Validation
```
/validate [all|spec|plan|constitution]
```
Validates project components.

## Templates Location

Use templates from `templates/` directory:
- Specification: templates/spec.md
- Implementation: templates/plan.md
- Tasks: templates/task.md

## Memory System

Project memory in `memory/` directory:
- constitution.md: Immutable principles
- context.md: Current project state
- decisions.md: Architectural decisions

## Workflow Process

1. **Initialize Feature**
   - Run: `/pulse init feature-name`
   - Creates branch and structure

2. **Create Specification**
   - Run: `/spec create "description"`
   - Fill template completely
   - Mark unclear items: [NEEDS CLARIFICATION]

3. **Generate Plan**
   - Run: `/plan generate`
   - Choose optimization focus
   - Review technology choices

4. **Create Tasks**
   - Run: `/task breakdown`
   - Review dependencies
   - Check time estimates

5. **Validate**
   - Run: `/validate all`
   - Fix any issues
   - Proceed to implementation

## Constitution Principles

Enforce these rules:
1. Start simple, add complexity only when needed
2. Write tests before code
3. One responsibility per component
4. Document everything
5. Consider security from start

## Project Structure

```
project/
├── specs/          # Specifications
├── plans/          # Implementation plans
├── tasks/          # Task lists
├── memory/         # Project memory
├── scripts/        # Automation
└── templates/      # Templates
```

## Important Notes

- Always update context.md after decisions
- Validate specifications before planning
- Use [P] marker for parallel tasks
- Keep commits atomic and focused
- Reference constitution for all decisions
"""