"""
Command Handler - Centralized command execution and routing

This module provides a centralized way to execute CLI commands,
handling initialization, error handling, and command routing.

REFACTORED: Uses registry pattern instead of massive if-elif chains.
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
from ..commands.safe_commands import SafeCommands
from ..monitor import MonitorCommands

# Import registry - this triggers command registration
from ..registry import command_registry

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

            # Safe command modules (NEW)
            self.safe_commands = SafeCommands(self.console, project_root)

            # Monitor commands
            self.monitor_commands = MonitorCommands(project_root, self.verbose, self.console.no_color)
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
            self.safe_commands = None
            self.monitor_commands = None

    def _check_for_updates(self) -> None:
        """Check for available updates on PyPI (non-blocking)"""
        try:
            if not should_check_version():
                return

            from ...utils.version_check import check_pypi_version, get_update_message

            latest = check_pypi_version(timeout=1)
            if latest:
                from ... import __version__
                is_outdated, is_major = compare_versions(latest, __version__)
                if is_outdated:
                    message, color = get_update_message(__version__, latest, is_major)
                    self.console.info(message)
        except Exception:
            # Version check should never block CLI functionality
            pass

    def _is_specpulse_project(self, path: Path) -> bool:
        """Check if the given path is a SpecPulse project"""
        try:
            from ...utils.error_handler import validate_project_directory
            validate_project_directory(path)
            return True
        except Exception as e:
            if self.verbose:
                self.console.warning(f"Project validation failed: {e}")
            return False

    def execute_command(self, command_name: str, **kwargs) -> Any:
        """
        Execute a command by name with given arguments.

        REFACTORED: Now uses registry pattern for cleaner routing.
        The massive if-elif chain has been replaced with a registry lookup.

        Args:
            command_name: Name of the command to execute
            **kwargs: Command-specific arguments

        Returns:
            Result of command execution

        Raises:
            SpecPulseError: If command execution fails
        """
        try:
            # Try to execute via registry first (covers most commands)
            handler = command_registry.get_handler(command_name)
            if handler:
                return handler(self, **kwargs)

            # Fallback: check for method on self (e.g., update, validate)
            method_name = command_name.replace('-', '_')
            if hasattr(self, method_name):
                return getattr(self, method_name)(**kwargs)

            raise SpecPulseError(f"Unknown command: {command_name}")

        except (UnicodeEncodeError, UnicodeError) as e:
            # Handle Unicode encoding issues
            import traceback
            self.console.error(f"Encoding error: {str(e)}")
            if self.verbose:
                traceback.print_exc()
            self.console.info("Try setting UTF-8 encoding: chcp 65001 (Windows)")
            sys.exit(1)
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
    def update(self, **kwargs) -> None:
        """Update SpecPulse to latest version"""
        return self.project_commands.update()

    def sync(self, **kwargs) -> None:
        """Synchronize project state with memory and Git repository"""
        if not self.project_commands:
            raise SpecPulseError("This command must be run from within a SpecPulse project directory")
        # Implementation would go here
        self.console.info("Sync command - implementation needed")
        return True

    def list_specs(self, **kwargs) -> None:
        """List all specifications in the project with metadata"""
        if not self.project_commands:
            raise SpecPulseError("This command must be run from within a SpecPulse project directory")
        # Implementation would go here
        self.console.info("List specs command - implementation needed")
        return True

    def template(self, template_command: Optional[str] = None, **kwargs) -> None:
        """Template management commands"""
        if template_command == 'list':
            category = kwargs.get('category', 'all')
            self.console.info(f"Template list command - implementation needed for category: {category}")
        elif template_command:
            self.console.warning(f"Template command '{template_command}' not implemented. Use AI commands for template operations.")
        else:
            self.console.info("Template command - subcommand needed")
        return True

    def validate(self, component: str = "all", fix: bool = False, verbose: bool = False) -> bool:
        """Validate project components"""
        if not self.validator:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        results = self.validator.validate_all(
            self.project_root,
            fix=fix,
            verbose=verbose or self.verbose
        )
        # Return True if all validations passed (no errors)
        return len([r for r in results if r.get('status') == 'error']) == 0

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

    
    def list_specs(self, **kwargs) -> None:
        """List all specifications"""
        if not self.memory_manager:
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory",
                "Run 'specpulse init' to create a new project or navigate to an existing one"
            )
        self.console.info("Listing specifications...")
        specs_dir = None
        if self.project_root:
            from ...core.path_manager import PathManager
            path_manager = PathManager(self.project_root)
            specs_dir = path_manager.specs_dir

        if specs_dir and specs_dir.exists():
            specs = list(specs_dir.rglob("spec-*.md"))
            if specs:
                for spec in specs:
                    self.console.info(f"  {spec.relative_to(self.project_root)}")
            else:
                self.console.warning("  No specifications found")
        else:
            self.console.warning("  No specs directory found")
        return True

    # Additional methods can be added here as needed
    # This keeps the main class focused on initialization and routing