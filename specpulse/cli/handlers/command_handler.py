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
from ..monitor import MonitorCommands

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
                # Handle subcommands: feature <subcommand>
                feature_subcommand = kwargs.get('feature_command')
                if feature_subcommand:
                    method_name = f"feature_{feature_subcommand}"
                    if hasattr(self.feature_commands, method_name):
                        return getattr(self.feature_commands, method_name)(**kwargs)
                    else:
                        raise SpecPulseError(f"Unknown feature command: {feature_subcommand}")
                else:
                    # Default to feature_init if no subcommand specified
                    # Remove command-specific kwargs that aren't part of method signature
                    method_kwargs = {k: v for k, v in kwargs.items() if k not in ['verbose', 'no_color']}
                    if 'feature_name' in method_kwargs:
                        return self.feature_commands.feature_init(method_kwargs['feature_name'])
                    else:
                        raise SpecPulseError("Feature command requires a subcommand or feature name")

            elif command_name in ['spec', 's']:
                if not self.spec_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Handle subcommands: spec <subcommand>
                spec_subcommand = kwargs.get('spec_command')
                if spec_subcommand:
                    method_name = f"spec_{spec_subcommand}"
                    if hasattr(self.spec_commands, method_name):
                        # Extract spec_description for create subcommand
                        if spec_subcommand == 'create' and 'spec_description' in kwargs:
                            return getattr(self.spec_commands, method_name)(kwargs['spec_description'], **{k: v for k, v in kwargs.items() if k not in ['spec_description', 'spec_command', 'verbose', 'no_color', 'command']})
                        else:
                            return getattr(self.spec_commands, method_name)(**kwargs)
                    else:
                        raise SpecPulseError(f"Unknown spec command: {spec_subcommand}")
                else:
                    # Default to spec_create if no subcommand specified
                    # Remove command-specific kwargs that aren't part of method signature
                    method_kwargs = {k: v for k, v in kwargs.items() if k not in ['verbose', 'no_color']}
                    if 'spec_description' in method_kwargs:
                        return self.spec_commands.spec_create(method_kwargs['spec_description'])
                    elif 'description' in method_kwargs:
                        return self.spec_commands.spec_create(method_kwargs['description'])
                    else:
                        raise SpecPulseError("Spec command requires a subcommand or description")

            elif command_name in ['plan', 'p']:
                if not self.plan_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Handle subcommands: plan <subcommand>
                plan_subcommand = kwargs.get('plan_command')
                if plan_subcommand:
                    method_name = f"plan_{plan_subcommand}"
                    if hasattr(self.plan_commands, method_name):
                        # Extract plan_description for create subcommand
                        if plan_subcommand == 'create' and 'plan_description' in kwargs:
                            return getattr(self.plan_commands, method_name)(kwargs['plan_description'], **{k: v for k, v in kwargs.items() if k not in ['plan_description', 'plan_command', 'verbose', 'no_color', 'command', 'spec_id', 'template']})
                        else:
                            return getattr(self.plan_commands, method_name)(**kwargs)
                    else:
                        raise SpecPulseError(f"Unknown plan command: {plan_subcommand}")
                else:
                    # Default to plan_create if no subcommand specified
                    method_kwargs = {k: v for k, v in kwargs.items() if k not in ['verbose', 'no_color']}
                    if 'plan_description' in method_kwargs:
                        return self.plan_commands.plan_create(method_kwargs['plan_description'])
                    elif 'description' in method_kwargs:
                        return self.plan_commands.plan_create(method_kwargs['description'])
                    else:
                        raise SpecPulseError("Plan command requires a subcommand or description")

            elif command_name == 'monitor':
                if not self.monitor_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Handle subcommands: monitor <subcommand>
                monitor_subcommand = kwargs.get('monitor_command')
                if monitor_subcommand:
                    if monitor_subcommand == 'status':
                        return self.monitor_commands.status(
                            feature_id=kwargs.get('feature'),
                            verbose_mode=kwargs.get('verbose', False)
                        )
                    elif monitor_subcommand == 'progress':
                        return self.monitor_commands.progress(
                            feature_id=kwargs.get('feature'),
                            detailed=kwargs.get('detailed', False)
                        )
                    elif monitor_subcommand == 'history':
                        return self.monitor_commands.history(
                            feature_id=kwargs.get('feature'),
                            limit=kwargs.get('limit', 20)
                        )
                    elif monitor_subcommand == 'reset':
                        return self.monitor_commands.reset(
                            feature_id=kwargs.get('feature'),
                            confirm=kwargs.get('confirm', False)
                        )
                    elif monitor_subcommand == 'validate':
                        return self.monitor_commands.validate()
                    elif monitor_subcommand == 'sync':
                        return self.monitor_commands.sync(
                            feature_id=kwargs.get('feature'),
                            direction=kwargs.get('direction', 'full')
                        )
                    else:
                        raise SpecPulseError(f"Unknown monitor command: {monitor_subcommand}")
                else:
                    # Default to monitor status
                    return self.monitor_commands.status(
                        feature_id=kwargs.get('feature'),
                        verbose_mode=kwargs.get('verbose', False)
                    )

            elif command_name in ['task', 't']:
                if not self.task_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Handle subcommands: task <subcommand>
                task_subcommand = kwargs.get('task_command')
                if task_subcommand:
                    method_name = f"task_{task_subcommand}"
                    if hasattr(self.task_commands, method_name):
                        # Extract plan_id for breakdown subcommand
                        if task_subcommand == 'breakdown' and 'plan_id' in kwargs:
                            return getattr(self.task_commands, method_name)(kwargs['plan_id'], **{k: v for k, v in kwargs.items() if k not in ['plan_id', 'task_command', 'verbose', 'no_color', 'command', 'template']})
                        else:
                            return getattr(self.task_commands, method_name)(**kwargs)
                    else:
                        raise SpecPulseError(f"Unknown task command: {task_subcommand}")
                else:
                    # Default behavior for task commands
                    method_kwargs = {k: v for k, v in kwargs.items() if k not in ['verbose', 'no_color']}
                    raise SpecPulseError("Task command requires a subcommand (list, breakdown)")

            elif command_name in ['execute', 'exec', 'e']:
                if not self.execute_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Handle subcommands: execute <subcommand>
                execute_subcommand = kwargs.get('execute_command')
                if execute_subcommand:
                    method_name = f"execute_{execute_subcommand}"
                    if hasattr(self.execute_commands, method_name):
                        # Extract target for start/status subcommands
                        if execute_subcommand in ['start', 'status'] and 'target' in kwargs:
                            return getattr(self.execute_commands, method_name)(kwargs['target'], **{k: v for k, v in kwargs.items() if k not in ['target', 'execute_command', 'verbose', 'no_color', 'command']})
                        else:
                            return getattr(self.execute_commands, method_name)(**kwargs)
                    else:
                        raise SpecPulseError(f"Unknown execute command: {execute_subcommand}")
                else:
                    # Default behavior for execute commands
                    method_kwargs = {k: v for k, v in kwargs.items() if k not in ['verbose', 'no_color']}
                    raise SpecPulseError("Execute command requires a subcommand (start, status)")

            # Slash commands
            elif command_name in ['sp-pulse']:
                if not self.sp_pulse_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Extract feature_description from kwargs
                feature_description = kwargs.get('feature_description')
                if not feature_description:
                    raise SpecPulseError("sp-pulse requires a feature description")

                # Convert feature description to feature name
                feature_name = feature_description.lower().replace(' ', '-')

                # Call init_feature method
                return self.sp_pulse_commands.init_feature(feature_name, **{k: v for k, v in kwargs.items() if k not in ['feature_description', 'verbose', 'no_color', 'command', 'name', 'tier']})

            elif command_name in ['sp-spec']:
                if not self.sp_spec_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Extract spec_description from kwargs
                spec_description = kwargs.get('spec_description')
                if not spec_description:
                    raise SpecPulseError("sp-spec requires a specification description")

                # Call create method
                return self.sp_spec_commands.create(spec_description, **{k: v for k, v in kwargs.items() if k not in ['spec_description', 'verbose', 'no_color', 'command', 'tier']})

            elif command_name in ['sp-plan']:
                if not self.sp_plan_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Extract plan_description from kwargs
                plan_description = kwargs.get('plan_description')
                if not plan_description:
                    raise SpecPulseError("sp-plan requires a plan description")

                # Call create method (assuming it exists)
                return getattr(self.sp_plan_commands, 'create', lambda x: False)(plan_description, **{k: v for k, v in kwargs.items() if k not in ['plan_description', 'verbose', 'no_color', 'command', 'spec_id', 'template']})

            elif command_name in ['sp-task']:
                if not self.sp_task_commands:
                    raise SpecPulseError(
                        "This command must be run from within a SpecPulse project directory",
                        "Run 'specpulse init' to create a new project or navigate to an existing one"
                    )
                # Extract target from kwargs
                target = kwargs.get('target')
                if not target:
                    raise SpecPulseError("sp-task requires a target (plan ID or specification)")

                # Call breakdown method (assuming it exists)
                return getattr(self.sp_task_commands, 'breakdown', lambda x: False)(target, **{k: v for k, v in kwargs.items() if k not in ['target', 'verbose', 'no_color', 'command', 'template']})

            # Other commands (update, validate, decompose, etc.)
            elif hasattr(self, command_name.replace('-', '_')):
                method_name = command_name.replace('-', '_')
                return getattr(self, method_name)(**kwargs)
            else:
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
            path_manager = PathManager(self.project_root, use_legacy_structure=False)
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