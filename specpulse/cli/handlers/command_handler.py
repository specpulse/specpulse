"""
Command Handler - Centralized command execution and routing

This module provides a centralized way to execute CLI commands,
handling initialization, error handling, and command routing.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from typing import Protocol

from ..commands.project_commands import ProjectCommands
from ..commands.feature_commands import FeatureCommands
from ..commands.spec_commands import SpecCommands
from ..commands.plan_task_commands import PlanCommands, TaskCommands, ExecuteCommands
from ..commands.sp_pulse_commands import SpPulseCommands
from ..commands.sp_spec_commands import SpSpecCommands
from ..commands.sp_plan_commands import SpPlanCommands
from ..commands.sp_task_commands import SpTaskCommands

from ...core.specpulse import SpecPulse
from ...core.validator import Validator
from ...core.template_manager import TemplateManager
from ...core.memory_manager import MemoryManager
from ...utils.console import Console
from ...utils.error_handler import (
    ErrorHandler, SpecPulseError, handle_specpulse_error
)
from ...utils.version_check import check_pypi_version, get_update_message, should_check_version, compare_versions


class CommandHandler:
    """Centralized command handler for SpecPulse CLI"""

    def __init__(self, no_color: bool = False, verbose: bool = False):
        """Initialize command handler with console and error handling"""
        self.console = Console(no_color=no_color, verbose=verbose)
        self.verbose = verbose
        self.error_handler = ErrorHandler(verbose=verbose)

        # Initialize core components
        self._initialize_components()

        # Initialize command modules
        self._initialize_commands()

        # Check for updates (non-blocking)
        self._check_for_updates()

    def _initialize_components(self) -> None:
        """Initialize core SpecPulse components"""
        try:
            self.specpulse = SpecPulse()
            self.validator = Validator()

            # Initialize project-dependent components
            project_root = Path.cwd()
            if self._is_specpulse_project(project_root):
                self.template_manager = TemplateManager(project_root)
                self.memory_manager = MemoryManager(project_root)
                self.project_root = project_root
            else:
                self.template_manager = None
                self.memory_manager = None
                self.project_root = None

        except Exception as e:
            self.console.error("Failed to initialize SpecPulse components")
            suggestions = self.error_handler.suggest_recovery_for_error(str(e))
            self.console.warning("Recovery suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                self.console.info(f"   {i}. {suggestion}")
            if self.verbose:
                self.console.warning(f"Technical details: {str(e)}")
            sys.exit(1)

    def _initialize_commands(self) -> None:
        """Initialize all command modules"""
        project_root = self.project_root or Path.cwd()

        # Core command modules
        self.project_commands = ProjectCommands(self.console, project_root)

        # Initialize project-dependent commands only if in a SpecPulse project
        if self.project_root:
            self.feature_commands = FeatureCommands(self.console, project_root)
            self.spec_commands = SpecCommands(self.console, project_root)
            self.plan_commands = PlanCommands(self.console, project_root)
            self.task_commands = TaskCommands(self.console, project_root)
            self.execute_commands = ExecuteCommands(self.console, project_root)

            # Slash command modules
            self.sp_pulse_commands = SpPulseCommands(self.console, project_root)
            self.sp_spec_commands = SpSpecCommands(self.console, project_root)
            self.sp_plan_commands = SpPlanCommands(self.console, project_root)
            self.sp_task_commands = SpTaskCommands(self.console, project_root)
        else:
            # Set to None for non-project contexts
            self.feature_commands = None
            self.spec_commands = None
            self.plan_commands = None
            self.task_commands = None
            self.execute_commands = None
            self.sp_pulse_commands = None
            self.sp_spec_commands = None
            self.sp_plan_commands = None
            self.sp_task_commands = None

    def _check_for_updates(self) -> None:
        """Check for available updates on PyPI (non-blocking)"""
        try:
            if not should_check_version():
                return

            from ...utils.version_check import check_pypi_version, get_update_message

            latest = check_pypi_version(timeout=1)
            if latest:
                from ... import __version__
                if compare_versions(latest, __version__) > 0:
                    message = get_update_message(__version__, latest)
                    self.console.info(message)
        except Exception:
            # Version check should never block CLI functionality
            pass

    def _is_specpulse_project(self, path: Path) -> bool:
        """Check if the given path is a SpecPulse project"""
        try:
            from ...utils.error_handler import validate_project_directory
            return validate_project_directory(path)
        except Exception:
            return False

    def execute_command(self, command_name: str, **kwargs) -> Any:
        """
        Execute a command by name with given arguments

        Args:
            command_name: Name of the command to execute
            **kwargs: Command-specific arguments

        Returns:
            Result of command execution

        Raises:
            SpecPulseError: If command execution fails
        """
        try:
            # Route to appropriate command handler
            if command_name in ['init', 'doctor']:
                return getattr(self.project_commands, command_name)(**kwargs)

            # Project-dependent commands
            elif command_name in ['feature', 'f']:
                if not self.feature_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return getattr(self.feature_commands, command_name)(**kwargs)

            elif command_name in ['spec', 's']:
                if not self.spec_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return getattr(self.spec_commands, command_name)(**kwargs)

            elif command_name in ['plan', 'p']:
                if not self.plan_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return getattr(self.plan_commands, command_name)(**kwargs)

            elif command_name in ['task', 't']:
                if not self.task_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return getattr(self.task_commands, command_name)(**kwargs)

            elif command_name in ['execute', 'exec', 'e']:
                if not self.execute_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return getattr(self.execute_commands, command_name.replace('execute', 'execute_commands'))(**kwargs)

            # Slash commands
            elif command_name in ['sp-pulse']:
                if not self.sp_pulse_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return self.sp_pulse_commands.pulse(**kwargs)

            elif command_name in ['sp-spec']:
                if not self.sp_spec_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return self.sp_spec_commands.spec(**kwargs)

            elif command_name in ['sp-plan']:
                if not self.sp_plan_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return self.sp_plan_commands.plan(**kwargs)

            elif command_name in ['sp-task']:
                if not self.sp_task_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                return self.sp_task_commands.task(**kwargs)

            # Other commands (update, validate, decompose, etc.)
            elif hasattr(self, command_name.replace('-', '_')):
                method_name = command_name.replace('-', '_')
                return getattr(self, method_name)(**kwargs)
            else:
                raise SpecPulseError(f"Unknown command: {command_name}")

        except SpecPulseError:
            # Re-raise SpecPulse errors as-is
            raise
        except Exception as e:
            # Handle unexpected errors
            exit_code = self.error_handler.handle_error(e, f"Command '{command_name}'")
            if exit_code is not None:
                sys.exit(exit_code)
            raise SpecPulseError(f"Command '{command_name}' failed: {str(e)}")

    # Core functionality methods (moved from main CLI class)
    def update(self) -> None:
        """Update SpecPulse to latest version"""
        return self.project_commands.update()

    def validate(self, component: str = "all", fix: bool = False, verbose: bool = False) -> None:
        """Validate project components"""
        if not self.validator:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.validator.validate(
            self.project_root,
            component=component,
            fix=fix,
            verbose=verbose or self.verbose,
            console=self.console
        )

    def doctor(self) -> None:
        """Check project health and diagnose issues"""
        return self.project_commands.doctor()

    def template_list(self, category: Optional[str] = None) -> None:
        """List available templates"""
        if not self.template_manager:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.template_manager.list_templates(category)

    def template_validate(self, template_name: Optional[str] = None, fix: bool = False) -> None:
        """Validate template syntax and structure"""
        if not self.template_manager:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.template_manager.validate_template(template_name, fix=fix)

    def decompose(self, spec_id: Optional[str] = None,
                   components: Optional[str] = None,
                   output_format: str = "markdown") -> None:
        """Decompose specifications into components"""
        if not self.specpulse:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.specpulse.decompose(
            spec_id=spec_id,
            components=components,
            output_format=output_format,
            console=self.console
        )

    def sync(self) -> None:
        """Synchronize project state with memory"""
        if not self.memory_manager:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.memory_manager.sync_with_memory(self.console)

    def list_specs(self) -> None:
        """List all specifications"""
        if not self.memory_manager:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.memory_manager.list_specs(self.console)

    def expand(self, feature_id: str, to_tier: str, show_diff: bool = False) -> None:
        """Expand specification to next tier"""
        if not self.specpulse:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        return self.specpulse.expand_spec(feature_id, to_tier, show_diff, self.console)

    # Additional methods can be added here as needed
    # This keeps the main class focused on initialization and routing