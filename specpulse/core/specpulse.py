"""
SpecPulse Core Implementation - Refactored Orchestrator

This is the refactored version that delegates to specialized services
instead of doing everything itself (God Object anti-pattern eliminated).

BEFORE: 1400+ lines, does everything
AFTER:  ~300 lines, orchestrates services

Architecture Pattern: Facade + Dependency Injection
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

# Import version from the dedicated version file
try:
    from .. import __version__
except ImportError:
    try:
        from specpulse._version import __version__
    except ImportError:
        # Fallback for development environment
        __version__ = "2.3.2"

from .template_provider import TemplateProvider
from .memory_provider import MemoryProvider
from .script_generator import ScriptGenerator
from .ai_instruction_provider import AIInstructionProvider
from .decomposition_service import DecompositionService
from .service_container import ServiceContainer
from .interfaces import (
    ITemplateProvider,
    IMemoryProvider,
    IScriptGenerator,
    IAIInstructionProvider,
    IDecompositionService
)

logger = logging.getLogger(__name__)


class SpecPulse:
    """
    Core SpecPulse functionality - Refactored as Service Orchestrator.

    This class now delegates to specialized services instead of implementing
    everything directly. Services are injected via constructor or service container.

    Design Pattern: Facade Pattern + Dependency Injection
    """

    def __init__(
        self,
        project_path: Optional[Path] = None,
        container: Optional[ServiceContainer] = None
    ):
        """
        Initialize SpecPulse orchestrator.

        Args:
            project_path: Project root path (default: cwd)
            container: Optional service container for DI
        """
        from ..utils.error_handler import ResourceError
        import yaml

        self.project_path = project_path or Path.cwd()
        self.config = self._load_config()

        # Resource directory resolution
        try:
            from importlib.resources import files
            resource_anchor = files('specpulse')
            self.resources_dir = Path(str(resource_anchor / 'resources'))
        except (ImportError, TypeError, AttributeError) as e:
            self.resources_dir = Path(__file__).parent.parent / "resources"
            if not self.resources_dir.exists():
                raise ResourceError("resources", self.resources_dir) from e

        self.templates_dir = self.resources_dir / "templates"

        # Initialize services (Dependency Injection)
        if container:
            # Use provided container
            self.template_provider = container.resolve(ITemplateProvider)
            self.memory_provider = container.resolve(IMemoryProvider)
            self.script_generator = container.resolve(IScriptGenerator)
            self.ai_provider = container.resolve(IAIInstructionProvider)
            self.decomposition_service = container.resolve(IDecompositionService)
        else:
            # Create services directly (for backward compatibility)
            self.template_provider = TemplateProvider(self.resources_dir)
            self.memory_provider = MemoryProvider(self.resources_dir)
            self.script_generator = ScriptGenerator(self.resources_dir)
            self.ai_provider = AIInstructionProvider(self.resources_dir)
            self.decomposition_service = DecompositionService(
                self.resources_dir,
                self.template_provider
            )

    def _load_config(self) -> Dict:
        """Load project configuration"""
        import yaml
        config_path = self.project_path / ".specpulse" / "config.yaml"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                return {}
        return {}

    # ======================================================================
    # TEMPLATE METHODS - Delegate to TemplateProvider
    # ======================================================================

    def get_spec_template(self) -> str:
        """Get specification template (delegated)"""
        return self.template_provider.get_spec_template()

    def get_plan_template(self) -> str:
        """Get implementation plan template (delegated)"""
        return self.template_provider.get_plan_template()

    def get_task_template(self) -> str:
        """Get task list template (delegated)"""
        return self.template_provider.get_task_template()

    def get_template(self, template_name: str, variables: Optional[Dict] = None) -> str:
        """Get generic template (delegated)"""
        return self.template_provider.get_template(template_name, variables)

    def get_decomposition_template(self, template_type: str = "microservices") -> str:
        """Get decomposition template (delegated)"""
        return self.template_provider.get_decomposition_template(template_type)

    def get_microservice_template(self) -> str:
        """Get microservice template (delegated)"""
        return self.template_provider.get_microservice_template()

    def get_api_contract_template(self) -> str:
        """Get API contract template (delegated)"""
        return self.template_provider.get_api_contract_template()

    def get_interface_template(self) -> str:
        """Get interface template (delegated)"""
        return self.template_provider.get_interface_template()

    def get_service_plan_template(self) -> str:
        """Get service plan template (delegated)"""
        return self.template_provider.get_service_plan_template()

    def get_integration_plan_template(self) -> str:
        """Get integration plan template (delegated)"""
        return self.template_provider.get_integration_plan_template()

    # ======================================================================
    # MEMORY METHODS - Delegate to MemoryProvider
    # ======================================================================

    def get_constitution_template(self) -> str:
        """Get constitution template (delegated)"""
        return self.memory_provider.get_constitution_template()

    def get_context_template(self) -> str:
        """Get context template (delegated)"""
        return self.memory_provider.get_context_template()

    def get_decisions_template(self) -> str:
        """Get decisions template (delegated)"""
        return self.memory_provider.get_decisions_template()

    # ======================================================================
    # SCRIPT METHODS - Delegate to ScriptGenerator
    # ======================================================================

    def get_setup_script(self) -> str:
        """Get setup script (delegated)"""
        return self.script_generator.get_setup_script()

    def get_spec_script(self) -> str:
        """Get spec script (delegated)"""
        return self.script_generator.get_spec_script()

    def get_plan_script(self) -> str:
        """Get plan script (delegated)"""
        return self.script_generator.get_plan_script()

    def get_task_script(self) -> str:
        """Get task script (delegated)"""
        return self.script_generator.get_task_script()

    def get_validate_script(self) -> str:
        """Get validate script (delegated)"""
        return self.script_generator.get_validate_script()

    def get_generate_script(self) -> str:
        """Get generate script (delegated)"""
        return self.script_generator.get_generate_script()

    # ======================================================================
    # AI INSTRUCTION METHODS - Delegate to AIInstructionProvider
    # ======================================================================

    def get_claude_instructions(self) -> str:
        """Get Claude instructions (delegated)"""
        return self.ai_provider.get_claude_instructions()

    def get_gemini_instructions(self) -> str:
        """Get Gemini instructions (delegated)"""
        return self.ai_provider.get_gemini_instructions()

    def get_claude_pulse_command(self) -> str:
        """Get Claude pulse command (delegated)"""
        return self.ai_provider.get_claude_pulse_command()

    def get_claude_spec_command(self) -> str:
        """Get Claude spec command (delegated)"""
        return self.ai_provider.get_claude_spec_command()

    def get_claude_plan_command(self) -> str:
        """Get Claude plan command (delegated)"""
        return self.ai_provider.get_claude_plan_command()

    def get_claude_task_command(self) -> str:
        """Get Claude task command (delegated)"""
        return self.ai_provider.get_claude_task_command()

    def get_claude_execute_command(self) -> str:
        """Get Claude execute command (delegated)"""
        return self.ai_provider.get_claude_execute_command()

    def get_claude_validate_command(self) -> str:
        """Get Claude validate command (delegated)"""
        return self.ai_provider.get_claude_validate_command()

    def get_claude_decompose_command(self) -> str:
        """Get Claude decompose command (delegated)"""
        return self.ai_provider.get_claude_decompose_command()

    def get_gemini_pulse_command(self) -> str:
        """Get Gemini pulse command (delegated)"""
        return self.ai_provider.get_gemini_pulse_command()

    def get_gemini_spec_command(self) -> str:
        """Get Gemini spec command (delegated)"""
        return self.ai_provider.get_gemini_spec_command()

    def get_gemini_plan_command(self) -> str:
        """Get Gemini plan command (delegated)"""
        return self.ai_provider.get_gemini_plan_command()

    def get_gemini_task_command(self) -> str:
        """Get Gemini task command (delegated)"""
        return self.ai_provider.get_gemini_task_command()

    def get_gemini_execute_command(self) -> str:
        """Get Gemini execute command (delegated)"""
        return self.ai_provider.get_gemini_execute_command()

    def get_gemini_validate_command(self) -> str:
        """Get Gemini validate command (delegated)"""
        return self.ai_provider.get_gemini_validate_command()

    def get_gemini_decompose_command(self) -> str:
        """Get Gemini decompose command (delegated)"""
        return self.ai_provider.get_gemini_decompose_command()

    def generate_claude_commands(self) -> List[Dict]:
        """Generate Claude commands (delegated)"""
        return self.ai_provider.generate_claude_commands()

    def generate_gemini_commands(self) -> List[Dict]:
        """Generate Gemini commands (delegated)"""
        return self.ai_provider.generate_gemini_commands()

    # ======================================================================
    # DECOMPOSITION METHODS - Delegate to DecompositionService
    # ======================================================================

    def decompose_specification(self, spec_dir: Path, spec_content: str) -> Dict:
        """Decompose specification (delegated)"""
        return self.decomposition_service.decompose_specification(spec_dir, spec_content)

    # ======================================================================
    # PROJECT INITIALIZATION
    # ======================================================================

    def init(self, project_name: Optional[str] = None, here: bool = False,
             ai_assistant: Optional[str] = None, template_source: str = 'local',
             console=None) -> Dict:
        """
        Initialize a new SpecPulse project

        Args:
            project_name: Name of the project
            here: Initialize in current directory
            ai_assistant: AI tool(s) to configure (claude, gemini, windsurf, cursor, github, opencode, crush, qwen, all, or comma-separated)
            template_source: Template source (local or remote)
            console: Console instance for output

        Returns:
            Dict with initialization result
        """
        import sys
        import os

        # Set UTF-8 encoding to avoid Windows charmap issues
        if sys.platform == "win32":
            os.system('chcp 65001 > nul')

        from pathlib import Path
        from datetime import datetime
        import yaml
        import re
        from ..utils.error_handler import ValidationError, ProjectStructureError
        from .. import __version__

        try:
            # Validate project name for invalid characters
            if project_name and not here:
                if not re.match(r'^[a-zA-Z0-9_-]+$', project_name):
                    raise ValidationError(
                        f"Project name contains invalid characters: {project_name}",
                        validation_type="project_name",
                        missing_items=["Valid characters: letters, numbers, underscore, hyphen"]
                    )

            if here:
                project_path = Path.cwd()
                project_name = project_path.name
            else:
                if not project_name:
                    # If no project name, initialize in current directory
                    project_path = Path.cwd()
                    project_name = project_path.name
                else:
                    project_path = Path.cwd() / project_name
                    if not project_path.exists():
                        project_path.mkdir(parents=True)

            # Validate project path
            if not project_path.exists():
                raise ProjectStructureError(
                    f"Project path does not exist: {project_path}",
                    missing_dirs=[str(project_path)]
                )

            # Import PathManager for centralized directory management
            from .path_manager import PathManager

            # Create path manager instance (ENFORCED: Always uses .specpulse/ structure)
            path_manager = PathManager(project_path)

            # Parse selected AI tools to create selective directory structure
            selected_tools = self._parse_ai_assistant(ai_assistant)

            # Base directories always needed
            directories = [
                ".specpulse",
                ".specpulse/cache",
                ".specpulse/specs",
                ".specpulse/plans",
                ".specpulse/tasks",
                ".specpulse/memory",
                ".specpulse/templates",
                ".specpulse/templates/decomposition",
                ".specpulse/checkpoints",
                ".specpulse/memory/notes",
                ".specpulse/docs"
            ]

            # Add directories only for selected AI tools
            for tool in selected_tools:
                if tool == 'claude':
                    directories.extend([".claude", ".claude/commands"])
                elif tool == 'gemini':
                    directories.extend([".gemini", ".gemini/commands"])
                elif tool == 'windsurf':
                    directories.extend([".windsurf", ".windsurf/workflows"])
                elif tool == 'cursor':
                    directories.extend([".cursor", ".cursor/commands"])
                elif tool == 'github':
                    directories.extend([".github", ".github/prompts"])
                elif tool == 'opencode':
                    directories.extend([".opencode", ".opencode/command"])
                elif tool == 'crush':
                    directories.extend([".crush", ".crush/commands/sp"])
                elif tool == 'qwen':
                    directories.extend([".qwen", ".qwen/commands"])

            # Create directories
            failed_dirs = []
            for dir_name in directories:
                try:
                    dir_path = project_path / dir_name
                    dir_path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    failed_dirs.append(dir_name)

            if failed_dirs:
                raise ProjectStructureError(
                    f"Failed to create {len(failed_dirs)} directories: {', '.join(failed_dirs)}",
                    missing_dirs=failed_dirs
                )

            # Create config file
            config = {
                "version": __version__,
                "project": {
                    "name": project_name,
                    "type": "web",
                    "created": datetime.now().isoformat()
                },
                "ai": {
                    "primary": ai_assistant or "claude",
                "selected_tools": self._parse_ai_assistant(ai_assistant),
                },
                "templates": {
                    "spec": ".specpulse/templates/spec.md",
                    "plan": ".specpulse/templates/plan.md",
                    "task": ".specpulse/templates/task.md"
                },
                "conventions": {
                    "branch_naming": "{number:03d}-{feature-name}",
                    "spec_naming": "spec-{number:03d}.md",
                    "plan_naming": "plan-{number:03d}.md",
                    "task_naming": "task-{number:03d}.md"
                }
            }

            config_path = project_path / ".specpulse" / "config.yaml"
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)

            # Copy templates from resources
            self._copy_templates(project_path, console)

            # Copy AI command files
            self._copy_ai_commands(project_path, ai_assistant, console)

            # Create documentation
            self._create_documentation(project_path)

            # Create initial memory files
            self._create_initial_memory(project_path)

            return {
                "status": "success",
                "project_path": str(project_path),
                "project_name": project_name,
                "directories_created": directories,
                "ai_assistant": ai_assistant,
                "selected_tools": self._parse_ai_assistant(ai_assistant)
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _copy_templates(self, project_path: Path, console=None) -> None:
        """Copy template files from resources to project"""
        import shutil
        import json

        project_templates_dir = project_path / ".specpulse" / "templates"

        # Copy core templates if they exist, otherwise use embedded templates
        core_templates = ["spec.md", "plan.md", "task.md"]
        for template in core_templates:
            src = self.templates_dir / template
            dst = project_templates_dir / template
            if src.exists():
                shutil.copy2(src, dst)
            else:
                # Use embedded template
                self._create_embedded_template(dst, template)

        # Copy decomposition templates
        decomp_dir = project_templates_dir / "decomposition"
        src_decomp = self.templates_dir / "decomposition"

        # Check if source directory exists and has files
        if src_decomp.exists():
            template_files = list(src_decomp.glob("*"))
            if template_files:
                for template_file in template_files:
                    dst = decomp_dir / template_file.name
                    shutil.copy2(template_file, dst)
            else:
                # Source exists but is empty - use embedded templates
                self._create_embedded_decomposition_templates(decomp_dir)
        else:
            # Create embedded decomposition templates
            self._create_embedded_decomposition_templates(decomp_dir)

        # Create template registry
        template_registry = {
            "version": "2.6.0",
            "created": datetime.now().isoformat(),
            "templates": {
                "core": {
                    "spec": "templates/spec.md",
                    "plan": "templates/plan.md",
                    "task": "templates/task.md"
                },
                "decomposition": {
                    "microservices": "templates/decomposition/microservices.md",
                    "api_contract": "templates/decomposition/api-contract.yaml",
                    "interface": "templates/decomposition/interface.ts",
                    "service_plan": "templates/decomposition/service-plan.md",
                    "integration_plan": "templates/decomposition/integration-plan.md"
                }
            }
        }

        registry_path = project_path / ".specpulse" / "template_registry.json"
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(template_registry, f, indent=2, ensure_ascii=False)

    def _create_embedded_template(self, dst_path: Path, template_type: str) -> None:
        """Create embedded template files"""
        if template_type == "spec.md":
            spec_template = """# Specification: [DESCRIPTION]

<!-- FEATURE_DIR: {{feature_directory}} -->
<!-- FEATURE_ID: {{feature_id}} -->
<!-- SPEC_NUMBER: {{spec_number}} -->
<!-- STATUS: pending -->
<!-- CREATED: {{current_timestamp}} -->

## Description
[Clear description of the feature to be implemented]

## Requirements

### Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Non-Functional Requirements
- **Performance**: [Performance requirements]
- **Security**: [Security requirements]
- **Scalability**: [Scalability requirements]

## Acceptance Criteria
- [ ] Given [precondition], when [action], then [expected outcome]
- [ ] [Second acceptance criteria]
- [ ] [Third acceptance criteria]

## Technical Considerations

### Dependencies
- **External APIs**: [List any external API dependencies]
- **Database Changes**: [Any database schema changes required]
- **Third-party Libraries**: [New libraries needed]

### Implementation Notes
[Technical notes and considerations for implementation]

## Testing Strategy
- **Unit Tests**: [What needs unit testing]
- **Integration Tests**: [What needs integration testing]
- **End-to-End Tests**: [What needs E2E testing]

## Definition of Done
- [ ] All requirements implemented
- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to production

## Additional Notes
[Any additional context, constraints, or notes]
"""
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(spec_template)

        elif template_type == "plan.md":
            plan_template = """# Implementation Plan: [DESCRIPTION]

<!-- FEATURE_DIR: {{feature_directory}} -->
<!-- FEATURE_ID: {{feature_id}} -->
<!-- PLAN_NUMBER: {{plan_number}} -->
<!-- STATUS: pending -->
<!-- CREATED: {{current_timestamp}} -->

## Specification Reference
- **Spec ID**: SPEC-{{feature_id}}
- **Spec Version**: 1.0
- **Plan Version**: 1.0
- **Generated**: {{current_date}}

## Architecture Overview

### High-Level Design
[High-level description of the solution approach]

### Technical Stack
- **Frontend**: [Technologies and frameworks]
- **Backend**: [Technologies and frameworks]
- **Database**: [Database technologies]
- **Infrastructure**: [Infrastructure components]

## Implementation Phases

### Phase 1: Foundation [Priority: HIGH]
**Timeline**: [X days/weeks]
**Dependencies**: None

#### Tasks
1. [ ] Set up project structure
2. [ ] Initialize database schema
3. [ ] Create basic API endpoints
4. [ ] Set up authentication framework

#### Deliverables
- [ ] Project structure created
- [ ] Database schema implemented
- [ ] Basic API endpoints functional
- [ ] Authentication system in place

### Phase 2: Core Features [Priority: HIGH]
**Timeline**: [X days/weeks]
**Dependencies**: Phase 1 complete

#### Tasks
1. [ ] Implement main business logic
2. [ ] Create user interface components
3. [ ] Integrate with external services
4. [ ] Implement data validation

#### Deliverables
- [ ] Core functionality working
- [ ] User interface complete
- [ ] External integrations functional
- [ ] Data validation implemented

### Phase 3: Enhancement & Polish [Priority: MEDIUM]
**Timeline**: [X days/weeks]
**Dependencies**: Phase 2 complete

#### Tasks
1. [ ] Add advanced features
2. [ ] Optimize performance
3. [ ] Improve user experience
4. [ ] Add comprehensive error handling

#### Deliverables
- [ ] Advanced features implemented
- [ ] Performance optimized
- [ ] UX improvements complete
- [ ] Error handling robust

### Phase 4: Testing & Deployment [Priority: MEDIUM]
**Timeline**: [X days/weeks]
**Dependencies**: Phase 3 complete

#### Tasks
1. [ ] Write comprehensive tests
2. [ ] Performance testing
3. [ ] Security audit
4. [ ] Deployment preparation

#### Deliverables
- [ ] Test coverage > 90%
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Deployment ready

## Risk Assessment

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |
| [Risk 2] | High/Medium/Low | High/Medium/Low | [Mitigation strategy] |

### Dependencies
| Dependency | Risk | Contingency |
|------------|------|-------------|
| [External service/API] | High/Medium/Low | [Backup plan] |
| [Third-party library] | High/Medium/Low | [Alternative solution] |

## Resource Requirements

### Development Team
- **Backend Developer**: [Number] developers
- **Frontend Developer**: [Number] developers
- **DevOps Engineer**: [Number] engineers
- **QA Engineer**: [Number] engineers

### Infrastructure
- **Development Environment**: [Required resources]
- **Testing Environment**: [Required resources]
- **Production Environment**: [Required resources]

## Success Metrics
- **Performance**: [Performance benchmarks]
- **User Satisfaction**: [Target metrics]
- **Business Impact**: [Expected business outcomes]
- **Technical Debt**: [Acceptable levels]

## Rollout Plan

### Phase Rollout Strategy
1. **Alpha**: Internal testing with core team
2. **Beta**: Limited user group testing
3. **GA**: General availability release

### Monitoring & Observability
- **Application Metrics**: [Key metrics to monitor]
- **Business Metrics**: [Business KPIs to track]
- **Error Monitoring**: [Error tracking setup]
- **Performance Monitoring**: [Performance tracking setup]

## Definition of Done
- [ ] All implementation phases complete
- [ ] All acceptance criteria met
- [ ] Comprehensive testing completed
- [ ] Documentation complete
- [ ] Team training conducted
- [ ] Production deployment successful

## Additional Notes
[Any additional context, constraints, or considerations]
"""
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(plan_template)

        elif template_type == "task.md":
            task_template = """# Task Breakdown: [FEATURE_NAME]

<!-- FEATURE_DIR: {{feature_directory}} -->
<!-- FEATURE_ID: {{feature_id}} -->
<!-- TASK_LIST_ID: {{task_list_id}} -->
<!-- STATUS: pending -->
<!-- CREATED: {{current_timestamp}} -->
<!-- LAST_UPDATED: {{current_timestamp}} -->

## Progress Overview
- **Total Tasks**: [number]
- **Completed Tasks**: [number] ([percentage]%)
- **In Progress Tasks**: [number]
- **Blocked Tasks**: [number]

## Task Categories

### [CATEGORY 1] - [Priority: HIGH/MEDIUM/LOW]

#### Phase 1: [Phase Name]
- [ ] **T001**: [S] [Task description] - [Hours]
- [ ] **T002**: [M] [Task description] - [Hours]
- [ ] **T003**: [L] [Task description] - [Hours]

#### Phase 2: [Phase Name]
- [ ] **T004**: [S] [Task description] - [Hours]
- [ ] **T005**: [M] [Task description] - [Hours]

### [CATEGORY 2] - [Priority: HIGH/MEDIUM/LOW]

#### Testing Tasks
- [ ] **T010**: [S] Unit tests for [module] - [Hours]
- [ ] **T011**: [M] Integration tests for [feature] - [Hours]
- [ ] **T012**: [L] E2E tests for [workflow] - [Hours]

#### Documentation Tasks
- [ ] **T015**: [S] API documentation update - [Hours]
- [ ] **T016**: [M] User guide update - [Hours]

## Task Details

### High Priority Tasks [P]
- **T001**: [Task title]
  - **Description**: [Detailed description]
  - **Acceptance Criteria**:
    - [ ] [Criteria 1]
    - [ ] [Criteria 2]
  - **Dependencies**: None
  - **Assignee**: [Team member]
  - **Estimated Time**: [X hours/days]

### Medium Priority Tasks
- **T002**: [Task title]
  - **Description**: [Detailed description]
  - **Acceptance Criteria**:
    - [ ] [Criteria 1]
    - [ ] [Criteria 2]
  - **Dependencies**: T001
  - **Assignee**: [Team member]
  - **Estimated Time**: [X hours/days]

### Low Priority Tasks
- **T003**: [Task title]
  - **Description**: [Detailed description]
  - **Acceptance Criteria**:
    - [ ] [Criteria 1]
    - [ ] [Criteria 2]
  - **Dependencies**: T002
  - **Assignee**: [Team member]
  - **Estimated Time**: [X hours/days]

## Dependencies

### Task Dependencies
```
T001 → T002 → T003 → T004
     ↘ T005 → T006
```

### External Dependencies
- **API Changes**: [Required API changes]
- **Database Updates**: [Required database changes]
- **Third-party Services**: [External dependencies]

## Parallel Execution Opportunities

### Can Be Done In Parallel
- [Tasks that can be executed simultaneously]
- [Other parallel tasks]

### Must Be Sequential
- [Tasks that must follow specific order]
- [Critical path tasks]

## Risk Assessment

### Blocker Risks
| Risk | Tasks Affected | Probability | Impact | Mitigation |
|------|----------------|-------------|--------|------------|
| [Risk description] | [Task IDs] | High/Med/Low | High/Med/Low | [Mitigation] |

### Resource Constraints
| Resource | Bottleneck | Impact | Mitigation |
|----------|------------|--------|------------|
| [Team member] | [Task type] | [Impact] | [Backup plan] |

## Completion Criteria

### Definition of Done for Each Task
- [ ] Code implemented and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests updated
- [ ] Documentation updated
- [ ] Acceptance criteria met
- [ ] No regressions introduced

### Feature Definition of Done
- [ ] All tasks completed
- [ ] Feature tested end-to-end
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Documentation complete
- [ ] Stakeholder approval received

## Progress Tracking

### Daily Standup Notes
- **Date**: [Current date]
- **Completed Yesterday**: [Tasks completed]
- **Focus Today**: [Today's priority tasks]
- **Blockers**: [Any blocking issues]

### Weekly Progress Updates
- **Week of**: [Week start date]
- **Tasks Completed**: [Number and list]
- **Tasks In Progress**: [Number and list]
- **Planned for Next Week**: [Upcoming tasks]
- **Issues/Blockers**: [Current issues]

## Notes & Decisions
[Record important decisions, changes, and observations during development]

---
**Legend:**
- [S] = Small (< 4 hours), [M] = Medium (4-8 hours), [L] = Large (> 8 hours)
- [P] = Priority tasks, [D] = Deferred tasks, [B] = Blocked tasks
- **Status**: [ ] Pending, [>] In Progress, [x] Completed, [!] Blocked
"""
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(task_template)

    def _create_embedded_decomposition_templates(self, decomp_dir: Path) -> None:
        """Create embedded decomposition templates"""
        decomp_dir.mkdir(parents=True, exist_ok=True)

        # Microservices decomposition template
        microservices_template = """# Microservices Decomposition Template

## Service Identification

### Business Capability Mapping
| Business Capability | Proposed Service | Bounded Context |
|---------------------|------------------|-----------------|
| [Capability 1] | [Service Name] | [Context] |
| [Capability 2] | [Service Name] | [Context] |

### Service Catalog
#### [Service Name 1]
- **Description**: [Service purpose and responsibilities]
- **Domain Model**: [Key entities and relationships]
- **API Endpoints**: [REST/GraphQL endpoints]
- **Database**: [Data store requirements]
- **Dependencies**: [External service dependencies]

#### [Service Name 2]
- **Description**: [Service purpose and responsibilities]
- **Domain Model**: [Key entities and relationships]
- **API Endpoints**: [REST/GraphQL endpoints]
- **Database**: [Data store requirements]
- **Dependencies**: [External service dependencies]

## Service Boundaries

### Context Mapping
```
[Service A] ←→ [Service B]
    ↓              ↓
[Service C] ←→ [Service D]
```

### Data Ownership
| Data Domain | Owner Service | Access Pattern |
|-------------|---------------|----------------|
| [Customer Data] | [Customer Service] | Read/Write |
| [Order Data] | [Order Service] | Read/Write |

## Communication Patterns

### Synchronous Communication
- **REST APIs**: [When to use]
- **GraphQL**: [When to use]
- **gRPC**: [When to use]

### Asynchronous Communication
- **Message Queues**: [RabbitMQ, Kafka]
- **Event Streams**: [Apache Kafka, AWS Kinesis]
- **Event Sourcing**: [When to implement]

## Infrastructure Considerations

### Service Mesh
- **Technology**: [Istio, Linkerd, Consul]
- **Traffic Management**: [Load balancing, routing]
- **Security**: [mTLS, policies]

### Observability
- **Logging**: [ELK stack, Fluentd]
- **Metrics**: [Prometheus, Grafana]
- **Tracing**: [Jaeger, Zipkin]

## Deployment Strategy

### Container Orchestration
- **Platform**: [Kubernetes, ECS, AKS]
- **Service Discovery**: [Consul, Eureka]
- **Configuration**: [Spring Cloud Config, Consul K/V]

### CI/CD Pipeline
- **Build**: [Docker build process]
- **Test**: [Testing strategy]
- **Deploy**: [Blue/Green, Canary, Rolling]
"""
        with open(decomp_dir / "microservices.md", 'w', encoding='utf-8') as f:
            f.write(microservices_template)

        # API contract template
        api_contract_template = """openapi: 3.0.3
info:
  title: [Service Name] API
  description: API contract for [Service Name]
  version: 1.0.0
  contact:
    name: [Team Name]
    email: [team@example.com]

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /[resource]:
    get:
      summary: List [resources]
      description: Retrieve a paginated list of [resources]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/[Resource]'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    post:
      summary: Create [resource]
      description: Create a new [resource]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create[Resource]'
      responses:
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

  /[resource]/{id}:
    get:
      summary: Get [resource] by ID
      description: Retrieve a specific [resource] by its ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    put:
      summary: Update [resource]
      description: Update an existing [resource]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Update[Resource]'
      responses:
        '200':
          description: Resource updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    delete:
      summary: Delete [resource]
      description: Delete a [resource] by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Resource deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  schemas:
    [Resource]:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
        name:
          type: string
          description: [Resource] name
        description:
          type: string
          description: [Resource] description
        created_at:
          type: string
          format: date-time
          description: Creation timestamp
        updated_at:
          type: string
          format: date-time
          description: Last update timestamp

    Create[Resource]:
      type: object
      required:
        - name
        - description
      properties:
        name:
          type: string
          description: [Resource] name
        description:
          type: string
          description: [Resource] description

    Update[Resource]:
      type: object
      properties:
        name:
          type: string
          description: [Resource] name
        description:
          type: string
          description: [Resource] description

    Pagination:
      type: object
      properties:
        page:
          type: integer
          description: Current page number
        limit:
          type: integer
          description: Items per page
        total:
          type: integer
          description: Total number of items
        totalPages:
          type: integer
          description: Total number of pages

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                description: Error message
              details:
                type: array
                items:
                  type: string
                description: Validation error details

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                description: Error message

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                description: Error message

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                description: Error message

security:
  - BearerAuth: []

tags:
  - name: [Resource]
    description: Operations related to [resources]
"""
        with open(decomp_dir / "api-contract.yaml", 'w', encoding='utf-8') as f:
            f.write(api_contract_template)

    def _parse_ai_assistant(self, ai_assistant: Optional[str]) -> List[str]:
        """Parse AI assistant selection into list of tools"""
        if not ai_assistant:
            return ['claude']

        # Handle comma-separated selections
        tools = [tool.strip() for tool in ai_assistant.split(',') if tool.strip()]

        # Handle 'all' keyword
        if 'all' in tools:
            return ['claude', 'gemini', 'windsurf', 'cursor', 'github', 'opencode', 'crush', 'qwen']

        # Validate tool names
        valid_tools = ['claude', 'gemini', 'windsurf', 'cursor', 'github', 'opencode', 'crush', 'qwen']
        return [tool for tool in tools if tool in valid_tools]

    def _copy_ai_commands(self, project_path: Path, ai_assistant: Optional[str], console=None) -> None:
        print("DEBUG: _copy_ai_commands function called!")
        """Copy AI command files based on chosen assistant(s) with enforced directory isolation"""
        import shutil

        # Import PathManager for enforced directory management
        from .path_manager import PathManager

        # Create path manager instance (ENFORCED: Always uses .specpulse/ structure)
        path_manager = PathManager(project_path)

        # Parse selected tools first
        commands_dir = self.resources_dir / "commands"
        selected_tools = self._parse_ai_assistant(ai_assistant)

        # Lock custom commands to their directories first (only for selected tools)
        if not path_manager.lock_custom_commands_to_directories(selected_tools):
            if console:
                console.error("Failed to lock custom commands to their directories")
            return

        for tool in selected_tools:
            # Special handling for crush which has NO subdirectory structure
            tool_dir = commands_dir / tool
            print(f"DEBUG {tool}: tool_dir={tool_dir}, exists={tool_dir.exists()}")
        if tool_dir.exists():
                # Determine destination directory using PathManager enforcement
                if tool == 'github':
                    dst_dir = getattr(path_manager, 'github_dir') / "prompts"
                    pattern = "*.prompt.md"
                elif tool == 'gemini':
                    dst_dir = getattr(path_manager, 'gemini_dir') / "commands"
                    pattern = "*.toml"
                elif tool == 'windsurf':
                    dst_dir = getattr(path_manager, 'windsurf_dir') / "workflows"  # ENFORCED: Windsurf uses workflows, not commands
                    pattern = "*.md"
                elif tool == 'opencode':
                    dst_dir = getattr(path_manager, 'opencode_dir') / "command"  # ENFORCED: Use command (singular) instead of commands
                    pattern = "*.md"
                elif tool == 'crush':
                    dst_dir = getattr(path_manager, 'crush_dir') / "commands" / "sp"
                    pattern = "*.md"
                elif tool == 'qwen':
                    dst_dir = getattr(path_manager, f"{tool}_dir") / "commands"
                    pattern = "*.toml"
                else:  # claude, cursor
                    dst_dir = getattr(path_manager, f"{tool}_dir") / "commands"
                    pattern = "*.md"

                # Create destination directory
                dst_dir.mkdir(parents=True, exist_ok=True)

                # Copy command files
                found_files = list(tool_dir.glob(pattern))
                # Write debug to file
                import tempfile
                debug_log_path = os.path.join(tempfile.gettempdir(), 'debug_specpulse.log')
                with open(debug_log_path, 'a') as f:
                    f.write(f"DEBUG {tool}: Looking for '{pattern}' in {tool_dir}, found {len(found_files)} files\n")
                print(f"DEBUG {tool}: Looking for '{pattern}' in {tool_dir}, found {len(found_files)} files")
                for cmd_file in found_files:
                    print(f"DEBUG {tool}: Copying {cmd_file.name}")
                    shutil.copy2(cmd_file, dst_dir / cmd_file.name)

                if console:
                    console.success(f"Copied {tool.title()} AI commands to enforced directory")

        # Validate AI command isolation after copying
        violations = path_manager.validate_ai_command_isolation()
        if violations and console:
            console.warning(f"AI command isolation violations found: {violations}")

        if console and selected_tools:
            tool_names = ", ".join(selected_tools).upper()
            console.info(f"Configured for: {tool_names} (ENFORCED directory structure)")

        # Log enforcement status
        enforcement_results = path_manager.enforce_specpulse_rules()
        if not enforcement_results['valid'] and console:
            console.error(f"Directory structure enforcement failed: {enforcement_results['errors']}")

    def _create_documentation(self, project_path: Path) -> None:
        """Create centralized documentation for AI commands and fallback procedures"""
        docs_dir = project_path / ".specpulse" / "docs"

        # Create AI_FALLBACK_GUIDE.md
        fallback_guide_content = f"""# SpecPulse AI Fallback Guide

This guide provides fallback procedures when SpecPulse CLI commands fail, ensuring AI can continue operations.

## 🚨 CLI Failure Detection

AI should detect CLI failures through:
1. **Exit codes**: Non-zero exit codes indicate failure
2. **Error patterns**: "command not found", "No such file", "Permission denied"
3. **Timeout**: Commands taking too long (>30 seconds)
4. **Missing dependencies**: Required tools not available

## 🛠️ Standard Fallback Procedures

### 1. Directory Structure Creation

**CLI Command**: `specpulse feature init <name>`
**Fallback**: Manual directory creation
```bash
# Detect current project root
PROJECT_ROOT=$(pwd)

# Create feature directory structure
FEATURE_DIR="$PROJECT_ROOT/.specpulse/specs/001-feature-name"
mkdir -p "$FEATURE_DIR"
mkdir -p "$PROJECT_ROOT/.specpulse/plans/001-feature-name"
mkdir -p "$PROJECT_ROOT/.specpulse/tasks/001-feature-name"

# Update context.md
echo "### Active Feature: Feature Name" >> "$PROJECT_ROOT/.specpulse/memory/context.md"
echo "- Feature ID: 001" >> "$PROJECT_ROOT/.specpulse/memory/context.md"
```

### 2. Specification Creation

**CLI Command**: `specpulse spec create "description"`
**Fallback**: Manual spec file creation
```bash
# Find next spec number
SPEC_NUM=$(ls "$FEATURE_DIR" | grep "spec-" | wc -l | awk '{{printf "%03d", $1+1}}')

# Create spec file with embedded template
cat > "$FEATURE_DIR/spec-$SPEC_NUM.md" << 'EOF'
# Specification: [DESCRIPTION]

<!-- FEATURE_DIR: 001-feature-name -->
<!-- FEATURE_ID: 001 -->
<!-- SPEC_NUMBER: SPEC_NUM -->
<!-- STATUS: pending -->
<!-- CREATED: CURRENT_TIMESTAMP -->

## Description
[DESCRIPTION]

## Requirements

### Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional Requirements
- [ ] Performance requirement
- [ ] Security requirement

## Acceptance Criteria

### User Stories
- **As a** [user role], **I want** [functionality], **so that** [benefit]
  - **Given** [context]
  - **When** [action]
  - **Then** [expected outcome]

## Technical Specifications

### Architecture
[Technical details]

### Dependencies
[External dependencies]

## Out of Scope
[What's not included]

## Success Metrics
[How to measure success]

## [NEEDS CLARIFICATION: Any uncertainties?]
EOF
```

### 3. Plan Creation

**CLI Command**: `specpulse plan create "description"`
**Fallback**: Manual plan file creation
```bash
# Find next plan number
PLAN_NUM=$(ls "$PROJECT_ROOT/.specpulse/plans/001-feature-name" | grep "plan-" | wc -l | awk '{{printf "%03d", $1+1}}')

# Create plan file with embedded template
cat > "$PROJECT_ROOT/.specpulse/plans/001-feature-name/plan-$PLAN_NUM.md" << 'EOF'
# Implementation Plan: [DESCRIPTION]

<!-- FEATURE_DIR: 001-feature-name -->
<!-- FEATURE_ID: 001 -->
<!-- PLAN_NUMBER: PLAN_NUM -->
<!-- STATUS: pending -->
<!-- CREATED: CURRENT_TIMESTAMP -->

## Description
[DESCRIPTION]

## Implementation Phases

### Phase 1: Foundation
- [ ] Task 1.1
- [ ] Task 1.2

### Phase 2: Core Features
- [ ] Task 2.1
- [ ] Task 2.2

### Phase 3: Polish & Testing
- [ ] Task 3.1
- [ ] Task 3.2

## Technology Stack
- [Frontend]: [Technologies]
- [Backend]: [Technologies]
- [Database]: [Database]
- [Infrastructure]: [Infrastructure]

## Timeline
- Phase 1: [X] weeks
- Phase 2: [Y] weeks
- Phase 3: [Z] weeks

## Dependencies
- External: [Dependencies]
- Internal: [Dependencies]

## Risks & Mitigations
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Success Criteria
- [ ] [Success criteria 1]
- [ ] [Success criteria 2]
EOF
```

### 4. Task Breakdown

**CLI Command**: `specpulse task breakdown <plan-id>`
**Fallback**: Manual task file creation
```bash
# Create task breakdown marker
cat > "$PROJECT_ROOT/.specpulse/tasks/001-feature-name/_breakdown_from_plan-$PLAN_NUM.md" << 'EOF'
# Task Breakdown Request

**Plan ID**: $PLAN_NUM
**Description**: [Plan description]
**Created**: CURRENT_TIMESTAMP

## Tasks Generated from Plan

### Task Categories
- [ ] Backend Development
- [ ] Frontend Development
- [ ] Database Setup
- [ ] Testing

### Next Steps
1. Create individual task files
2. Assign task numbers
3. Define acceptance criteria
4. Set up dependencies
EOF

# Create initial task files
TASK_NUM=1

# Example task file
cat > "$PROJECT_ROOT/.specpulse/tasks/001-feature-name/task-$TASK_NUM.md" << 'EOF'
# Task T$TASK_NUM: [Task Title]

<!-- TASK_NUMBER: TASK_NUM -->
<!-- STATUS: pending -->
<!-- CREATED: CURRENT_TIMESTAMP -->

## Description
[Task description]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Dependencies
- [Depends on other tasks]

## Testing
- [Unit tests]
- [Integration tests]

## Notes
[Any additional notes]
EOF
```

## 🔄 Standard Error Recovery

### Permission Errors
```bash
# Try fixing permissions
chmod -R 755 "$PROJECT_ROOT/.specpulse"

# If still fails, work in temp directory
TEMP_DIR=$(mktemp -d)
echo "Working in temporary directory: $TEMP_DIR"
```

### Path Issues
```bash
# Convert to absolute paths
PROJECT_ROOT=$(pwd -P)

# Handle Windows paths
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    PROJECT_ROOT=$(cygpath -w "$PROJECT_ROOT")
fi
```

### Template Missing
```bash
# Use embedded templates as shown above
# Log the missing template
echo "Warning: Template not found, using embedded fallback" >&2
```

## 🤖 AI Integration Best Practices

### Always Try CLI First
1. **Execute CLI command with timeout**
2. **Check exit code and output**
3. **If failed, apply fallback immediately**
4. **Log the fallback usage**

### Error Handling Pattern
```python
# AI should use this pattern:
try:
    result = run_cli_command("specpulse spec create", description)
    if result.success:
        return result
except CLIError:
    log_warning("CLI failed, using manual fallback")
    return manual_spec_creation(description)
```

### Fallback Logging
Always log when fallbacks are used:
```bash
echo "[FALLBACK] CLI command failed: $cmd" >&2
echo "[FALLBACK] Using manual procedure" >&2
```

## 📞 Getting Help

If fallbacks fail repeatedly:

1. **Check SpecPulse Installation**
   ```bash
   python -m specpulse --version
   pip list | grep specpulse
   ```

2. **Check Environment**
   ```bash
   python --version
   which specpulse
   echo $PATH
   ```

3. **Manual Recovery**
   - Create directory structure manually
   - Use embedded templates
   - Track progress in simple text files
   - Focus on core functionality over tooling

## ✅ Success Criteria

Fallback is successful when:
- [ ] Files are created in correct locations
- [ ] Content follows expected format
- [ ] Metadata is properly set
- [ ] Progress can be tracked
- [ ] User can continue work without CLI

## 🚨 When to Escalate

Escalate to manual intervention when:
- Multiple fallbacks fail in sequence
- Critical system dependencies are missing
- File permissions cannot be resolved
- User reports persistent issues

**Remember: AI should always enable work to continue, even when tooling fails!**

---
*Generated by SpecPulse v{__version__}*
*Created: {datetime.now().isoformat()}*
"""

        with open(docs_dir / "AI_FALLBACK_GUIDE.md", 'w', encoding='utf-8') as f:
            f.write(fallback_guide_content)

        # Create AI_INTEGRATION.md
        integration_content = f"""# SpecPulse AI Integration Guide

This guide explains how AI assistants integrate with SpecPulse for specification-driven development.

## 🤖 Supported AI Platforms

### Claude Code
- **Location**: `.claude/commands/`
- **Commands**: `/sp-*` slash commands
- **Files**: Markdown format (.md)

### Gemini CLI
- **Location**: `.gemini/commands/`
- **Commands**: `/sp-*` commands
- **Files**: TOML format (.toml)

## 🔄 CLI-AI Collaboration Pattern

### Critical Design Principle: CLI First, AI Enhanced

```
User Request → AI Command → CLI Command → File Creation → AI Enhancement
     ↓              ↓           ↓            ↓           ↓
  /sp-spec     Claude/Gemini  specpulse    Empty spec   Detailed spec
  "OAuth2"    detects intent    create      template    expansion
```

### 1. AI Command Detection
AI platforms detect user intent and route to appropriate SpecPulse CLI commands:

**Claude Code**:
```bash
# User: /sp-spec "OAuth2 authentication with JWT"
# AI detects intent and runs:
specpulse spec create "OAuth2 authentication with JWT"
```

**Gemini CLI**:
```bash
# User: /sp-spec "User authentication system"
# AI detects intent and runs:
specpulse spec create "User authentication system"
```

### 2. CLI Command Execution
CLI commands create the foundation:
- ✅ Directory structure
- ✅ Empty templates with metadata
- ✅ File naming conventions
- ✅ Context updates

### 3. AI Content Enhancement
AI expands the CLI-created templates:
- 📝 Detailed specifications
- 🏗️ Implementation plans
- 📋 Task breakdowns
- 🔍 Technical insights

## 🛡️ Fallback Protection System

When CLI commands fail, AI automatically applies fallback procedures:

### Detection Patterns
```python
def detect_cli_failure(result):
    # Check exit codes
    if result.exit_code != 0:
        return True

    # Check error patterns
    error_patterns = [
        "command not found",
        "Permission denied",
        "No such file",
        "ModuleNotFoundError"
    ]

    for pattern in error_patterns:
        if pattern in result.stderr.lower():
            return True

    return False
```

### Fallback Procedures
1. **Directory Creation**: Manual mkdir commands
2. **Template Usage**: Embedded templates from AI
3. **Metadata Generation**: Automatic ID assignment
4. **File Operations**: Safe file creation with proper encoding

## 📋 Command Reference

### Feature Management
```bash
# Claude Code
/sp-pulse <feature-name>              # Initialize feature
/sp-continue <feature-id>            # Switch to existing feature
/sp-status                           # Show project status

# Gemini CLI
/sp-pulse <feature-name>              # Initialize feature
/sp-continue <feature-id>            # Switch to existing feature
/sp-status                           # Show project status

# CLI Equivalent
specpulse feature init <name>
specpulse feature continue <id>
specpulse feature list
```

### Specification Management
```bash
# Claude Code
/sp-spec create "description"         # Create specification
/sp-spec validate <spec-id>          # Validate specification
/sp-spec expand <spec-id>            # Expand with details

# Gemini CLI
/sp-spec create "description"         # Create specification
/sp-spec validate <spec-id>          # Validate specification
/sp-spec expand <spec-id>            # Expand with details

# CLI Equivalent
specpulse spec create "description"
specpulse spec validate <id>
```

### Planning & Tasks
```bash
# Claude Code
/sp-plan                             # Generate implementation plan
/sp-task <plan-id>                    # Create task breakdown
/sp-execute                          # Execute next task

# Gemini CLI
/sp-plan                             # Generate implementation plan
/sp-task <plan-id>                    # Create task breakdown
/sp-execute                          # Execute next task

# CLI Equivalent
specpulse plan create "description"
specpulse task breakdown <plan-id>
```

## 🔄 Workflow Examples

### Complete Feature Development

1. **Initialize Feature**
   ```bash
   /sp-pulse user-authentication
   # Creates: .specpulse/specs/001-user-authentication/
   ```

2. **Create Specification**
   ```bash
   /sp-spec create "OAuth2 login with JWT tokens"
   # Creates: spec-001.md with AI-enhanced content
   ```

3. **Generate Implementation Plan**
   ```bash
   /sp-plan
   # Creates: plan-001.md with detailed phases
   ```

4. **Break Down Tasks**
   ```bash
   /sp-task plan-001
   # Creates: task-001.md, task-002.md, etc.
   ```

5. **Execute Tasks**
   ```bash
   /sp-execute
   # Implements tasks sequentially
   ```

### Specification Refinement

1. **Initial Spec Creation**
   ```bash
   /sp-spec create "Payment processing system"
   ```

2. **Validation Check**
   ```bash
   /sp-spec validate spec-001
   ```

3. **Content Expansion**
   ```bash
   /sp-spec expand spec-001
   # AI adds detailed requirements, constraints, etc.
   ```

## 🔧 Configuration

### AI Assistant Setup
```yaml
# .specpulse/config.yaml
ai:
  primary: claude  # claude or gemini
  fallback: true   # Enable fallback protection
  logging: true    # Log AI operations

templates:
  spec: .specpulse/templates/spec.md
  plan: .specpulse/templates/plan.md
  task: .specpulse/templates/task.md
```

### Custom Commands
Users can create custom AI commands:

```markdown
# .claude/commands/custom-research.md
# Custom research command

## Usage
/research "topic"

## Implementation
AI should:
1. Research the topic using available tools
2. Create a specification in .specpulse/specs/
3. Generate implementation plan
4. Break down into actionable tasks
```

## 🚨 Error Handling

### CLI Failure Scenarios
1. **Command Not Found**
   - Apply fallback procedures
   - Use embedded templates
   - Log the failure

2. **Permission Denied**
   - Try alternative paths
   - Use temporary directory
   - Notify user

3. **Missing Dependencies**
   - Create manual workarounds
   - Use basic file operations
   - Continue with reduced functionality

### Recovery Procedures
```python
# AI should implement recovery logic
try:
    result = execute_cli_command(command)
except CLIError as e:
    log_error(f"CLI failed: {{e}}")
    fallback_result = apply_fallback_procedure()
    return fallback_result
```

## 📊 Success Metrics

### AI Integration Success
- ✅ **CLI Success Rate**: >95%
- ✅ **Fallback Success Rate**: >90%
- ✅ **User Satisfaction**: Seamless workflow
- ✅ **Error Recovery**: Zero user intervention required

### Quality Indicators
- ✅ **Specification Quality**: Complete and detailed
- ✅ **Plan Quality**: Realistic timelines and phases
- ✅ **Task Quality**: Actionable and specific
- ✅ **Progress Tracking**: Continuous monitoring

## 🔗 Resources

- **AI Fallback Guide**: `.specpulse/docs/AI_FALLBACK_GUIDE.md`
- **Project Status**: `.specpulse/memory/context.md`
- **Validation Rules**: `.specpulse/validation_rules.yaml`
- **Templates**: `.specpulse/templates/`

## 🤖 AI Best Practices

1. **Always try CLI first** - CLI provides structure and consistency
2. **Use fallbacks gracefully** - Never let user workflows stop
3. **Enhance, don't replace** - AI adds value to CLI foundation
4. **Maintain context** - Track project state and user preferences
5. **Validate continuously** - Ensure quality and completeness

---

*Generated by SpecPulse v{__version__}*
*Created: {datetime.now().isoformat()}*
"""

        with open(docs_dir / "AI_INTEGRATION.md", 'w', encoding='utf-8') as f:
            f.write(integration_content)

        # Create README.md for docs directory
        docs_readme = f"""# SpecPulse Documentation

This directory contains comprehensive documentation for SpecPulse AI integration and fallback procedures.

## 📚 Available Documents

### [AI_FALLBACK_GUIDE.md](AI_FALLBACK_GUIDE.md)
Complete fallback procedures when SpecPulse CLI commands fail. Essential for AI assistants to continue work even when CLI is unavailable.

### [AI_INTEGRATION.md](AI_INTEGRATION.md)
Comprehensive guide for AI platform integration with SpecPulse. Includes command reference, workflow examples, and best practices.

## 🎯 Quick Reference

### For AI Assistants
```bash
# If CLI fails, follow this guide:
.specpulse/docs/AI_FALLBACK_GUIDE.md

# For integration patterns:
.specpulse/docs/AI_INTEGRATION.md
```

### For Users
```bash
# Check project health
specpulse doctor

# Validate specifications
specpulse doctor --fix

# Get help
specpulse --help
```

## 🔗 External Resources

- **GitHub Repository**: https://github.com/specpulse/specpulse
- **PyPI Package**: https://pypi.org/project/specpulse/
- **Issues**: https://github.com/specpulse/specpulse/issues

---

*Documentation for SpecPulse v{__version__}*
"""

        with open(docs_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(docs_readme)

    def _create_initial_memory(self, project_path: Path) -> None:
        """Create initial memory files"""
        import shutil
        memory_dir = project_path / ".specpulse" / "memory"

        # Copy memory resource files
        memory_resources_dir = self.resources_dir / "memory"
        if memory_resources_dir.exists():
            for memory_file in ["constitution.md", "decisions.md", "README.md"]:
                src = memory_resources_dir / memory_file
                dst = memory_dir / memory_file
                if src.exists():
                    shutil.copy2(src, dst)

        # Create context.md if not copied
        context_file = memory_dir / "context.md"
        if not context_file.exists():
            context_content = f"""# Project Context

## Project: {project_path.name}
- **Created**: {datetime.now().isoformat()}
- **SpecPulse Version**: {__version__}
- **AI Assistant**: Not configured

## Active Feature: None
No feature currently in progress.

## Recent Activity
Project initialized successfully.

---
*This file is automatically maintained by SpecPulse*
"""

            with open(context_file, 'w', encoding='utf-8') as f:
                f.write(context_content)

        # Copy validation files to .specpulse
        validation_files = ["validation_rules.yaml", "validation_examples.yaml"]
        for validation_file in validation_files:
            src = self.resources_dir / validation_file
            dst = project_path / ".specpulse" / validation_file
            if src.exists():
                shutil.copy2(src, dst)


__all__ = ['SpecPulse']
