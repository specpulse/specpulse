"""
SpecPulse Core Implementation - Refactored Orchestrator

This is the refactored version that delegates to specialized services
instead of doing everything itself (God Object anti-pattern eliminated).

BEFORE: 1400+ lines, does everything
AFTER:  ~300 lines, orchestrates services

Architecture Pattern: Facade + Dependency Injection
"""

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
            except:
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
            ai_assistant: AI assistant to configure (claude or gemini)
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

            # Create directory structure
            directories = [
                ".specpulse",
                ".specpulse/cache",
                ".claude",
                ".claude/commands",
                ".gemini",
                ".gemini/commands",
                "memory",
                "specs",
                "plans",
                "tasks",
                "templates",
                "templates/decomposition"
            ]

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
                    "primary": ai_assistant or "claude"
                },
                "templates": {
                    "spec": "templates/spec.md",
                    "plan": "templates/plan.md",
                    "task": "templates/task.md"
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
            self._copy_templates(project_path)

            # Copy AI command files
            self._copy_ai_commands(project_path, ai_assistant)

            # Create initial memory files
            self._create_initial_memory(project_path)

            return {
                "status": "success",
                "project_path": str(project_path),
                "project_name": project_name,
                "directories_created": directories,
                "ai_assistant": ai_assistant
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _copy_templates(self, project_path: Path) -> None:
        """Copy template files from resources to project"""
        import shutil

        project_templates_dir = project_path / "templates"

        # Copy core templates
        core_templates = ["spec.md", "plan.md", "task.md"]
        for template in core_templates:
            src = self.templates_dir / template
            dst = project_templates_dir / template
            if src.exists():
                shutil.copy2(src, dst)

        # Copy decomposition templates
        decomp_dir = project_templates_dir / "decomposition"
        src_decomp = self.templates_dir / "decomposition"
        if src_decomp.exists():
            for template_file in src_decomp.glob("*.md"):
                dst = decomp_dir / template_file.name
                shutil.copy2(template_file, dst)

    def _copy_ai_commands(self, project_path: Path, ai_assistant: Optional[str]) -> None:
        """Copy AI command files based on chosen assistant"""
        import shutil

        commands_dir = self.resources_dir / "commands"

        # Copy Claude commands
        claude_commands = commands_dir / "claude"
        if claude_commands.exists():
            dst_claude = project_path / ".claude" / "commands"
            for cmd_file in claude_commands.glob("*.md"):
                shutil.copy2(cmd_file, dst_claude / cmd_file.name)

        # Copy Gemini commands
        gemini_commands = commands_dir / "gemini"
        if gemini_commands.exists():
            dst_gemini = project_path / ".gemini" / "commands"
            for cmd_file in gemini_commands.glob("*.toml"):
                shutil.copy2(cmd_file, dst_gemini / cmd_file.name)

    def _create_initial_memory(self, project_path: Path) -> None:
        """Create initial memory files"""
        memory_dir = project_path / "memory"

        # Create context.md
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

        with open(memory_dir / "context.md", 'w', encoding='utf-8') as f:
            f.write(context_content)

        # Create decisions.md
        decisions_content = """# Architectural Decisions

No decisions recorded yet.

## Decision Log Format
- **AD-[number]**: [Decision Title] (Date)
  - **Status**: [Proposed/Approved/Implemented/Deprecated]
  - **Context**: Background and problem
  - **Decision**: What was decided
  - **Consequences**: Impact of this decision

---
*This file is automatically maintained by SpecPulse*
"""

        with open(memory_dir / "decisions.md", 'w', encoding='utf-8') as f:
            f.write(decisions_content)


__all__ = ['SpecPulse']
