"""
Core Service Interfaces for Dependency Injection

This module defines Protocol-based interfaces for all core services.
Using Protocols (PEP 544) enables structural subtyping and better
type checking without tight coupling.

These interfaces are the foundation of the dependency injection system.
"""

from typing import Protocol, Dict, List, Optional
from pathlib import Path


class ITemplateProvider(Protocol):
    """
    Interface for template provider service.

    Responsible for loading and caching all template files:
    - Specification templates
    - Plan templates
    - Task templates
    - Decomposition templates
    """

    def get_spec_template(self) -> str:
        """
        Get specification template.

        Returns:
            Specification template content
        """
        ...

    def get_plan_template(self) -> str:
        """
        Get implementation plan template.

        Returns:
            Plan template content
        """
        ...

    def get_task_template(self) -> str:
        """
        Get task list template.

        Returns:
            Task template content
        """
        ...

    def get_template(self, template_name: str, variables: Optional[Dict] = None) -> str:
        """
        Get generic template by name with variable substitution.

        Args:
            template_name: Name of template file
            variables: Optional variables for substitution

        Returns:
            Template content with variables replaced
        """
        ...

    def get_decomposition_template(self, template_type: str) -> str:
        """
        Get decomposition template.

        Args:
            template_type: Type of template (microservices, api, interface)

        Returns:
            Decomposition template content
        """
        ...


class IMemoryProvider(Protocol):
    """
    Interface for memory/context provider service.

    Responsible for loading memory templates:
    - Constitution (SDD principles)
    - Context (current project state)
    - Decisions (architectural decisions)
    """

    def get_constitution_template(self) -> str:
        """
        Get constitution template (SDD principles).

        Returns:
            Constitution template content
        """
        ...

    def get_context_template(self) -> str:
        """
        Get context template (project state).

        Returns:
            Context template content
        """
        ...

    def get_decisions_template(self) -> str:
        """
        Get architectural decisions template.

        Returns:
            Decisions template content
        """
        ...


class IScriptGenerator(Protocol):
    """
    Interface for script generation service.

    Responsible for generating helper scripts:
    - Feature initialization scripts
    - Validation scripts
    - Context detection scripts
    """

    def get_setup_script(self) -> str:
        """
        Get feature initialization script.

        Returns:
            Setup script content
        """
        ...

    def get_spec_script(self) -> str:
        """
        Get spec context detection script.

        Returns:
            Spec script content
        """
        ...

    def get_plan_script(self) -> str:
        """
        Get plan context detection script.

        Returns:
            Plan script content
        """
        ...

    def get_task_script(self) -> str:
        """
        Get task context detection script.

        Returns:
            Task script content
        """
        ...

    def get_validate_script(self) -> str:
        """
        Get validation script.

        Returns:
            Validation script content
        """
        ...

    def get_generate_script(self) -> str:
        """
        Get generation script.

        Returns:
            Generation script content
        """
        ...


class IAIInstructionProvider(Protocol):
    """
    Interface for AI instruction provider service.

    Responsible for AI-specific instructions and commands:
    - Claude Code instructions
    - Gemini CLI instructions
    - Command generation
    """

    def get_claude_instructions(self) -> str:
        """
        Get Claude AI instructions.

        Returns:
            Claude instructions content
        """
        ...

    def get_gemini_instructions(self) -> str:
        """
        Get Gemini CLI instructions.

        Returns:
            Gemini instructions content
        """
        ...

    def get_claude_pulse_command(self) -> str:
        """Get Claude pulse command"""
        ...

    def get_claude_spec_command(self) -> str:
        """Get Claude spec command"""
        ...

    def get_claude_plan_command(self) -> str:
        """Get Claude plan command"""
        ...

    def get_claude_task_command(self) -> str:
        """Get Claude task command"""
        ...

    def get_claude_execute_command(self) -> str:
        """Get Claude execute command"""
        ...

    def get_claude_validate_command(self) -> str:
        """Get Claude validate command"""
        ...

    def get_claude_decompose_command(self) -> str:
        """Get Claude decompose command"""
        ...

    def get_gemini_pulse_command(self) -> str:
        """Get Gemini pulse command"""
        ...

    def get_gemini_spec_command(self) -> str:
        """Get Gemini spec command"""
        ...

    def get_gemini_plan_command(self) -> str:
        """Get Gemini plan command"""
        ...

    def get_gemini_task_command(self) -> str:
        """Get Gemini task command"""
        ...

    def get_gemini_execute_command(self) -> str:
        """Get Gemini execute command"""
        ...

    def get_gemini_validate_command(self) -> str:
        """Get Gemini validate command"""
        ...

    def get_gemini_decompose_command(self) -> str:
        """Get Gemini decompose command"""
        ...

    def generate_claude_commands(self) -> List[Dict]:
        """
        Generate all Claude AI commands.

        Returns:
            List of command definitions
        """
        ...

    def generate_gemini_commands(self) -> List[Dict]:
        """
        Generate all Gemini AI commands.

        Returns:
            List of command definitions
        """
        ...


class IDecompositionService(Protocol):
    """
    Interface for decomposition service.

    Responsible for specification decomposition:
    - Microservice decomposition
    - API contract generation
    - Interface generation
    - Integration planning
    """

    def decompose_specification(self, spec_dir: Path, spec_content: str) -> Dict:
        """
        Decompose specification into microservices.

        Args:
            spec_dir: Specification directory
            spec_content: Specification content

        Returns:
            Decomposition result with services, contracts, interfaces
        """
        ...

    def get_microservice_template(self) -> str:
        """Get microservice template"""
        ...

    def get_api_contract_template(self) -> str:
        """Get API contract template"""
        ...

    def get_interface_template(self) -> str:
        """Get interface template"""
        ...

    def get_service_plan_template(self) -> str:
        """Get service plan template"""
        ...

    def get_integration_plan_template(self) -> str:
        """Get integration plan template"""
        ...

    def get_decomposition_template(self, template_name: str) -> str:
        """
        Get specific decomposition template.

        Args:
            template_name: Name of decomposition template

        Returns:
            Template content
        """
        ...


# Type aliases for convenience
TemplateProvider = ITemplateProvider
MemoryProvider = IMemoryProvider
ScriptGenerator = IScriptGenerator
AIInstructionProvider = IAIInstructionProvider
DecompositionService = IDecompositionService


__all__ = [
    'ITemplateProvider',
    'IMemoryProvider',
    'IScriptGenerator',
    'IAIInstructionProvider',
    'IDecompositionService',
    'TemplateProvider',
    'MemoryProvider',
    'ScriptGenerator',
    'AIInstructionProvider',
    'DecompositionService',
]
