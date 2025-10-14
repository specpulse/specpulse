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


__all__ = ['SpecPulse']
