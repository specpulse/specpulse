"""
Command Registry - Centralized command registration and routing

This module provides a cleaner command routing system using a registry pattern
instead of massive if-elif chains.
"""

from typing import Dict, List, Callable, Optional, Any, Type
from dataclasses import dataclass, field
from functools import wraps


@dataclass
class CommandConfig:
    """Configuration for a registered command"""
    name: str
    aliases: List[str] = field(default_factory=list)
    requires_project: bool = True
    subcommand_key: Optional[str] = None  # e.g., 'feature_command', 'spec_command'
    default_subcommand: Optional[str] = None
    handler_attr: Optional[str] = None  # Attribute name on CommandHandler
    method_prefix: Optional[str] = None  # Prefix for subcommand methods


class CommandRegistry:
    """
    Registry for CLI commands with simplified routing.

    Usage:
        registry = CommandRegistry()

        @registry.register('feature', aliases=['f'], subcommand_key='feature_command')
        def handle_feature(handler, **kwargs):
            ...
    """

    _instance: Optional['CommandRegistry'] = None
    _commands: Dict[str, CommandConfig] = {}
    _handlers: Dict[str, Callable] = {}

    def __new__(cls) -> 'CommandRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._commands = {}
            cls._instance._handlers = {}
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset registry (for testing)"""
        cls._instance = None
        cls._commands = {}
        cls._handlers = {}

    def register(
        self,
        name: str,
        aliases: Optional[List[str]] = None,
        requires_project: bool = True,
        subcommand_key: Optional[str] = None,
        default_subcommand: Optional[str] = None,
        handler_attr: Optional[str] = None,
        method_prefix: Optional[str] = None
    ) -> Callable:
        """
        Decorator to register a command handler.

        Args:
            name: Primary command name
            aliases: Alternative command names
            requires_project: Whether command requires SpecPulse project
            subcommand_key: Kwargs key for subcommand (e.g., 'feature_command')
            default_subcommand: Default subcommand if none specified
            handler_attr: Attribute name on CommandHandler for the commands object
            method_prefix: Prefix for subcommand method names
        """
        def decorator(func: Callable) -> Callable:
            config = CommandConfig(
                name=name,
                aliases=aliases or [],
                requires_project=requires_project,
                subcommand_key=subcommand_key,
                default_subcommand=default_subcommand,
                handler_attr=handler_attr,
                method_prefix=method_prefix
            )

            # Register under primary name and all aliases
            self._commands[name] = config
            self._handlers[name] = func
            for alias in (aliases or []):
                self._commands[alias] = config
                self._handlers[alias] = func

            return func
        return decorator

    def get_config(self, command_name: str) -> Optional[CommandConfig]:
        """Get configuration for a command"""
        return self._commands.get(command_name)

    def get_handler(self, command_name: str) -> Optional[Callable]:
        """Get handler function for a command"""
        return self._handlers.get(command_name)

    def list_commands(self) -> List[str]:
        """List all registered primary command names"""
        seen = set()
        result = []
        for config in self._commands.values():
            if config.name not in seen:
                seen.add(config.name)
                result.append(config.name)
        return result


# Global registry instance
command_registry = CommandRegistry()


# ============================================================================
# COMMAND ROUTING HELPERS
# ============================================================================

def route_subcommand(
    commands_obj: Any,
    method_prefix: str,
    subcommand: str,
    kwargs: Dict[str, Any],
    param_mappings: Optional[Dict[str, str]] = None
) -> Any:
    """
    Route to a subcommand method on a commands object.

    Args:
        commands_obj: Object containing command methods
        method_prefix: Prefix for method names (e.g., 'feature' for feature_init)
        subcommand: Subcommand name (e.g., 'init')
        kwargs: Command arguments
        param_mappings: Map of kwarg keys to method parameter names

    Returns:
        Result of the command method

    Raises:
        AttributeError: If method not found
    """
    method_name = f"{method_prefix}_{subcommand}"

    if not hasattr(commands_obj, method_name):
        raise AttributeError(f"Unknown {method_prefix} command: {subcommand}")

    method = getattr(commands_obj, method_name)

    # Filter out common kwargs that shouldn't be passed to methods
    excluded_keys = {'verbose', 'no_color', 'command', f'{method_prefix}_command'}
    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in excluded_keys}

    # Apply parameter mappings if provided
    if param_mappings:
        for src_key, dst_key in param_mappings.items():
            if src_key in filtered_kwargs:
                filtered_kwargs[dst_key] = filtered_kwargs.pop(src_key)

    return method(**filtered_kwargs)


def check_project_requirement(handler: 'CommandHandler', command_name: str) -> None:
    """
    Check if current directory is a SpecPulse project.

    Args:
        handler: CommandHandler instance
        command_name: Name of command being executed

    Raises:
        SpecPulseError: If not in a SpecPulse project
    """
    from ..utils.error_handler import SpecPulseError

    if handler.project_root is None:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )


# ============================================================================
# COMMAND DEFINITIONS
# ============================================================================

# Project commands (don't require existing project)
@command_registry.register('init', requires_project=False)
def handle_init(handler, **kwargs):
    """Handle init command"""
    return handler.project_commands.init(**kwargs)


@command_registry.register('doctor', requires_project=False)
def handle_doctor(handler, **kwargs):
    """Handle doctor command"""
    return handler.project_commands.doctor(**kwargs)


# Feature commands
@command_registry.register('feature', aliases=['f'], subcommand_key='feature_command')
def handle_feature(handler, **kwargs):
    """Handle feature command with subcommands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.feature_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    subcommand = kwargs.get('feature_command')
    if subcommand:
        return route_subcommand(handler.feature_commands, 'feature', subcommand, kwargs)
    elif 'feature_name' in kwargs:
        return handler.feature_commands.feature_init(kwargs['feature_name'])
    else:
        raise SpecPulseError("Feature command requires a subcommand or feature name")


# Spec commands
@command_registry.register('spec', aliases=['s'], subcommand_key='spec_command')
def handle_spec(handler, **kwargs):
    """Handle spec command with subcommands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.spec_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    subcommand = kwargs.get('spec_command')
    if subcommand:
        if subcommand == 'create' and 'spec_description' in kwargs:
            return handler.spec_commands.spec_create(
                kwargs['spec_description'],
                **{k: v for k, v in kwargs.items()
                   if k not in ['spec_description', 'spec_command', 'verbose', 'no_color', 'command']}
            )
        return route_subcommand(handler.spec_commands, 'spec', subcommand, kwargs)
    elif 'spec_description' in kwargs:
        return handler.spec_commands.spec_create(kwargs['spec_description'])
    elif 'description' in kwargs:
        return handler.spec_commands.spec_create(kwargs['description'])
    else:
        raise SpecPulseError("Spec command requires a subcommand or description")


# Plan commands
@command_registry.register('plan', aliases=['p'], subcommand_key='plan_command')
def handle_plan(handler, **kwargs):
    """Handle plan command with subcommands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.plan_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    subcommand = kwargs.get('plan_command')
    if subcommand:
        if subcommand == 'create' and 'plan_description' in kwargs:
            return handler.plan_commands.plan_create(
                kwargs['plan_description'],
                **{k: v for k, v in kwargs.items()
                   if k not in ['plan_description', 'plan_command', 'verbose', 'no_color', 'command', 'spec_id', 'template']}
            )
        return route_subcommand(handler.plan_commands, 'plan', subcommand, kwargs)
    elif 'plan_description' in kwargs:
        return handler.plan_commands.plan_create(kwargs['plan_description'])
    elif 'description' in kwargs:
        return handler.plan_commands.plan_create(kwargs['description'])
    else:
        raise SpecPulseError("Plan command requires a subcommand or description")


# Task commands
@command_registry.register('task', aliases=['t'], subcommand_key='task_command')
def handle_task(handler, **kwargs):
    """Handle task command with subcommands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.task_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    subcommand = kwargs.get('task_command')
    if subcommand:
        if subcommand == 'breakdown' and 'plan_id' in kwargs:
            return handler.task_commands.task_breakdown(
                kwargs['plan_id'],
                **{k: v for k, v in kwargs.items()
                   if k not in ['plan_id', 'task_command', 'verbose', 'no_color', 'command', 'template']}
            )
        return route_subcommand(handler.task_commands, 'task', subcommand, kwargs)
    else:
        raise SpecPulseError("Task command requires a subcommand (list, breakdown)")


# Execute commands
@command_registry.register('execute', aliases=['exec', 'e'], subcommand_key='execute_command')
def handle_execute(handler, **kwargs):
    """Handle execute command with subcommands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.execute_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    subcommand = kwargs.get('execute_command')
    if subcommand:
        if subcommand in ['start', 'status'] and 'target' in kwargs:
            method = getattr(handler.execute_commands, f'execute_{subcommand}')
            return method(
                kwargs['target'],
                **{k: v for k, v in kwargs.items()
                   if k not in ['target', 'execute_command', 'verbose', 'no_color', 'command']}
            )
        return route_subcommand(handler.execute_commands, 'execute', subcommand, kwargs)
    else:
        raise SpecPulseError("Execute command requires a subcommand (start, status)")


# Monitor commands
@command_registry.register('monitor', subcommand_key='monitor_command')
def handle_monitor(handler, **kwargs):
    """Handle monitor command with subcommands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.monitor_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    monitor_subcommand = kwargs.get('monitor_command')
    monitor_methods = {
        'status': lambda: handler.monitor_commands.status(
            feature_id=kwargs.get('feature'),
            verbose_mode=kwargs.get('verbose', False)
        ),
        'progress': lambda: handler.monitor_commands.progress(
            feature_id=kwargs.get('feature'),
            detailed=kwargs.get('detailed', False)
        ),
        'history': lambda: handler.monitor_commands.history(
            feature_id=kwargs.get('feature'),
            limit=kwargs.get('limit', 20)
        ),
        'reset': lambda: handler.monitor_commands.reset(
            feature_id=kwargs.get('feature'),
            confirm=kwargs.get('confirm', False)
        ),
        'validate': lambda: handler.monitor_commands.validate(),
        'sync': lambda: handler.monitor_commands.sync(
            feature_id=kwargs.get('feature'),
            direction=kwargs.get('direction', 'full')
        )
    }

    if monitor_subcommand in monitor_methods:
        return monitor_methods[monitor_subcommand]()
    elif monitor_subcommand:
        raise SpecPulseError(f"Unknown monitor command: {monitor_subcommand}")
    else:
        # Default to status
        return handler.monitor_commands.status(
            feature_id=kwargs.get('feature'),
            verbose_mode=kwargs.get('verbose', False)
        )


# Slash commands
@command_registry.register('sp-pulse')
def handle_sp_pulse(handler, **kwargs):
    """Handle sp-pulse slash command"""
    from ..utils.error_handler import SpecPulseError

    if not handler.sp_pulse_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    feature_description = kwargs.get('feature_description')
    if not feature_description:
        raise SpecPulseError("sp-pulse requires a feature description")

    feature_name = feature_description.lower().replace(' ', '-')
    return handler.sp_pulse_commands.init_feature(
        feature_name,
        **{k: v for k, v in kwargs.items()
           if k not in ['feature_description', 'verbose', 'no_color', 'command', 'name', 'tier']}
    )


@command_registry.register('sp-spec')
def handle_sp_spec(handler, **kwargs):
    """Handle sp-spec slash command"""
    from ..utils.error_handler import SpecPulseError

    if not handler.sp_spec_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    spec_description = kwargs.get('spec_description')
    if not spec_description:
        raise SpecPulseError("sp-spec requires a specification description")

    return handler.sp_spec_commands.create(
        spec_description,
        **{k: v for k, v in kwargs.items()
           if k not in ['spec_description', 'verbose', 'no_color', 'command', 'tier']}
    )


@command_registry.register('sp-plan')
def handle_sp_plan(handler, **kwargs):
    """Handle sp-plan slash command"""
    from ..utils.error_handler import SpecPulseError

    if not handler.sp_plan_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    plan_description = kwargs.get('plan_description')
    if not plan_description:
        raise SpecPulseError("sp-plan requires a plan description")

    return getattr(handler.sp_plan_commands, 'create', lambda x, **kw: False)(
        plan_description,
        **{k: v for k, v in kwargs.items()
           if k not in ['plan_description', 'verbose', 'no_color', 'command', 'spec_id', 'template']}
    )


@command_registry.register('sp-task')
def handle_sp_task(handler, **kwargs):
    """Handle sp-task slash command"""
    from ..utils.error_handler import SpecPulseError

    if not handler.sp_task_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    target = kwargs.get('target')
    if not target:
        raise SpecPulseError("sp-task requires a target (plan ID or specification)")

    return getattr(handler.sp_task_commands, 'breakdown', lambda x, **kw: False)(
        target,
        **{k: v for k, v in kwargs.items()
           if k not in ['target', 'verbose', 'no_color', 'command', 'template']}
    )


# Safe commands
@command_registry.register('safe', subcommand_key='safe_command')
def handle_safe(handler, **kwargs):
    """Handle safe commands"""
    from ..utils.error_handler import SpecPulseError

    if not handler.safe_commands:
        raise SpecPulseError(
            "This command must be run from within a SpecPulse project directory",
            "Run 'specpulse init' to create a new project or navigate to an existing one"
        )

    safe_command = kwargs.get('safe_command')
    if not safe_command:
        raise SpecPulseError("Safe command requires a subcommand")

    safe_method_map = {
        'feature-init': lambda: handler.safe_commands.feature_init_safe(kwargs.get('feature_name')),
        'spec-create': lambda: handler.safe_commands.spec_create_safe(
            kwargs.get('description'), kwargs.get('feature_name')
        ),
        'plan-create': lambda: handler.safe_commands.plan_create_safe(
            kwargs.get('description'), kwargs.get('feature_name')
        ),
        'task-create': lambda: handler.safe_commands.task_create_safe(
            kwargs.get('description'), kwargs.get('service_prefix'), kwargs.get('feature_name')
        ),
        'status': lambda: handler.safe_commands.status_report_safe(
            kwargs.get('feature_name'), kwargs.get('verbose', False),
            kwargs.get('ids', False), kwargs.get('validate', False)
        ),
        'validate': lambda: handler.safe_commands.validate_markdown_safe(
            kwargs.get('target', 'all'), kwargs.get('fix', False),
            kwargs.get('strict', False), kwargs.get('format', 'table')
        )
    }

    if safe_command in safe_method_map:
        return safe_method_map[safe_command]()
    else:
        raise SpecPulseError(f"Unknown safe command: {safe_command}")


# ============================================================================
# SIMPLIFIED COMMAND HANDLER MIXIN
# ============================================================================

class CommandRoutingMixin:
    """
    Mixin that provides simplified command routing using the registry.

    Add this to CommandHandler to enable registry-based routing.
    """

    def execute_registered_command(self, command_name: str, **kwargs) -> Any:
        """
        Execute a command using the registry.

        Args:
            command_name: Name of command to execute
            **kwargs: Command arguments

        Returns:
            Result of command execution
        """
        config = command_registry.get_config(command_name)
        handler = command_registry.get_handler(command_name)

        if not config or not handler:
            return None  # Command not in registry

        # Check project requirement
        if config.requires_project:
            check_project_requirement(self, command_name)

        # Execute handler
        return handler(self, **kwargs)


# ============================================================================
# STANDARD COMMAND HANDLERS
# ============================================================================

def create_subcommand_handler(
    handler_attr: str,
    method_prefix: str,
    subcommand_key: str,
    default_action: Optional[Callable] = None,
    param_mappings: Optional[Dict[str, Dict[str, str]]] = None
) -> Callable:
    """
    Factory to create standard subcommand handlers.

    Args:
        handler_attr: Attribute name on CommandHandler (e.g., 'feature_commands')
        method_prefix: Prefix for method names (e.g., 'feature')
        subcommand_key: Kwargs key for subcommand (e.g., 'feature_command')
        default_action: Function to call if no subcommand specified
        param_mappings: Dict mapping subcommand to parameter mappings

    Returns:
        Handler function
    """
    def handler(cmd_handler: Any, **kwargs) -> Any:
        commands_obj = getattr(cmd_handler, handler_attr, None)
        if not commands_obj:
            from ..utils.error_handler import SpecPulseError
            raise SpecPulseError(
                "This command must be run from within a SpecPulse project directory"
            )

        subcommand = kwargs.get(subcommand_key)

        if subcommand:
            mappings = (param_mappings or {}).get(subcommand)
            return route_subcommand(
                commands_obj,
                method_prefix,
                subcommand,
                kwargs,
                mappings
            )
        elif default_action:
            return default_action(cmd_handler, commands_obj, **kwargs)
        else:
            from ..utils.error_handler import SpecPulseError
            raise SpecPulseError(
                f"{method_prefix.title()} command requires a subcommand"
            )

    return handler
