"""
Subcommand Parsers - Argument parsing for different CLI commands

This module provides argument parsers for different CLI commands,
centralizing parsing logic and maintaining consistency.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create the main argument parser for SpecPulse CLI

    Returns:
        Configured ArgumentParser instance
    """
    # Import version dynamically
    from ... import __version__

    parser = argparse.ArgumentParser(
        prog='specpulse',
        description='SpecPulse - AI-Enhanced Specification-Driven Development (SDD) Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  specpulse init my-project              Initialize a new SpecPulse project
  specpulse feature init user-auth      Initialize a new feature
  specpulse doctor --fix               Check and fix project health
  specpulse template list               List available templates
  specpulse list-specs                 List all specifications

  AI Commands (for Claude/Gemini integration):
  specpulse sp-pulse "New feature"     Initialize feature
  specpulse sp-spec "Authentication"    Create specification
  specpulse sp-plan "Implement auth"    Create implementation plan
  specpulse sp-task breakdown 001      Break down into tasks
        """,
    )

    # Version argument (dynamic from __version__)
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s v{__version__}',
        help='Show version information and exit'
    )

    # Global options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed information'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='COMMAND',
        title='commands',
        description='SpecPulse commands'
    )

    # Project Commands
    _add_project_commands(subparsers)

    # Feature Commands
    _add_feature_commands(subparsers)

    # Specification Commands (commented out until templates are fixed)
    # _add_spec_commands(subparsers)

    # Utility Commands (working ones only)
    _add_utility_commands_working(subparsers)

    # Slash Commands (v2.1.3+)
    _add_slash_commands(subparsers)

    return parser


def _add_project_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add project-level commands"""

    # Init command
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize a new SpecPulse project',
        description='Initialize a new SpecPulse project with templates and configuration'
    )
    init_parser.add_argument(
        'project_name',
        nargs='?',
        help='Name of the project to initialize'
    )
    init_parser.add_argument(
        '--here',
        action='store_true',
        help='Initialize in current directory instead of creating a subdirectory'
    )
    init_parser.add_argument(
        '--ai',
        choices=['claude', 'gemini'],
        help='AI assistant to use for generated commands (claude or gemini)'
    )
    init_parser.add_argument(
        '--template-source',
        choices=['local', 'remote'],
        default='local',
        help='Source for templates (local or remote)'
    )

    # Update command
    update_parser = subparsers.add_parser(
        'update',
        help='Update SpecPulse to latest version',
        description='Check for and update to the latest version of SpecPulse'
    )
    update_parser.add_argument(
        '--force',
        action='store_true',
        help='Force update without confirmation'
    )

    # Doctor command
    doctor_parser = subparsers.add_parser(
        'doctor',
        help='Check project health and diagnose issues',
        description='Comprehensive health check for SpecPulse projects'
    )
    doctor_parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix detected issues where possible'
    )
    doctor_parser.add_argument(
        '--component',
        choices=['all', 'templates', 'memory', 'git', 'ai-commands'],
        default='all',
        help='Specific component to check (default: all)'
    )


def _add_feature_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add feature-related commands"""

    # Feature init command
    feature_parser = subparsers.add_parser(
        'feature',
        help='Feature development commands',
        description='Commands for feature initialization and management'
    )
    feature_subparsers = feature_parser.add_subparsers(
        dest='feature_command',
        help='Feature subcommands',
        metavar='SUBCOMMAND'
    )

    # Feature init subcommand
    feature_init_parser = feature_subparsers.add_parser(
        'init',
        help='Initialize a new feature',
        description='Initialize a new feature with proper directory structure and templates'
    )
    feature_init_parser.add_argument(
        'feature_name',
        help='Name of the feature to initialize (e.g., "user-auth", "payment-api")'
    )
    feature_init_parser.add_argument(
        '--force',
        action='store_true',
        help='Force initialization even if feature directory exists'
    )

    # Feature continue subcommand
    feature_continue_parser = feature_subparsers.add_parser(
        'continue',
        help='Continue working on existing feature',
        description='Switch context to an existing feature and continue development'
    )
    feature_continue_parser.add_argument(
        'feature_id',
        help='ID of the feature to continue (e.g., "001")'
    )

    # Feature list subcommand
    feature_list_parser = feature_subparsers.add_parser(
        'list',
        help='List all features',
        description='List all features in the project with their current status'
    )


def _add_spec_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add specification-related commands"""

    # Spec command
    spec_parser = subparsers.add_parser(
        'spec',
        help='Specification commands',
        description='Commands for creating and managing specifications'
    )
    spec_subparsers = spec_parser.add_subparsers(
        dest='spec_command',
        help='Specification subcommands',
        metavar='SUBCOMMAND'
    )

    # Spec create subcommand
    spec_create_parser = spec_subparsers.add_parser(
        'create',
        help='Create a new specification',
        description='Create a new specification for a feature or component'
    )
    spec_create_parser.add_argument(
        'spec_description',
        help='Description of the specification to create'
    )
    spec_create_parser.add_argument(
        '--template',
        help='Template to use for the specification'
    )
    spec_create_parser.add_argument(
        '--tier',
        choices=['basic', 'detailed', 'technical'],
        default='detailed',
        help='Specification tier/complexity level'
    )

    # Spec validate subcommand
    spec_validate_parser = spec_subparsers.add_parser(
        'validate',
        help='Validate specifications',
        description='Validate specifications against project standards'
    )
    spec_validate_parser.add_argument(
        'spec_id',
        nargs='?',
        help='ID of specification to validate (default: all)'
    )
    spec_validate_parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix validation issues where possible'
    )

    # Spec list subcommand
    spec_list_parser = spec_subparsers.add_parser(
        'list',
        help='List specifications',
        description='List all specifications in the project'
    )
    spec_list_parser.add_argument(
        '--status',
        choices=['all', 'pending', 'in_progress', 'completed'],
        default='all',
        help='Filter specifications by status'
    )


def _add_plan_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add plan-related commands"""

    # Plan command
    plan_parser = subparsers.add_parser(
        'plan',
        help='Planning commands',
        description='Commands for creating and managing implementation plans'
    )
    plan_subparsers = plan_parser.add_subparsers(
        dest='plan_command',
        help='Planning subcommands',
        metavar='SUBCOMMAND'
    )

    # Plan create subcommand
    plan_create_parser = plan_subparsers.add_parser(
        'create',
        help='Create an implementation plan',
        description='Create a detailed implementation plan for specifications'
    )
    plan_create_parser.add_argument(
        'plan_description',
        help='Description of the plan to create'
    )
    plan_create_parser.add_argument(
        '--spec-id',
        help='Specification ID to create plan for'
    )
    plan_create_parser.add_argument(
        '--template',
        help='Template to use for the plan'
    )

    # Plan list subcommand
    plan_list_parser = plan_subparsers.add_parser(
        'list',
        help='List implementation plans',
        description='List all implementation plans in the project'
    )

    # Plan validate subcommand
    plan_validate_parser = plan_subparsers.add_parser(
        'validate',
        help='Validate implementation plans',
        description='Validate implementation plans against project standards'
    )
    plan_validate_parser.add_argument(
        'plan_id',
        nargs='?',
        help='ID of plan to validate (default: all)'
    )


def _add_task_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add task-related commands"""

    # Task command
    task_parser = subparsers.add_parser(
        'task',
        help='Task management commands',
        description='Commands for creating and managing development tasks'
    )
    task_subparsers = task_parser.add_subparsers(
        dest='task_command',
        help='Task subcommands',
        metavar='SUBCOMMAND'
    )

    # Task breakdown subcommand
    task_breakdown_parser = task_subparsers.add_parser(
        'breakdown',
        help='Break down specifications into tasks',
        description='Break down specifications into manageable development tasks'
    )
    task_breakdown_parser.add_argument(
        'plan_id',
        help='ID of the plan to break down into tasks'
    )
    task_breakdown_parser.add_argument(
        '--template',
        help='Task template to use'
    )

    # Task list subcommand
    task_list_parser = task_subparsers.add_parser(
        'list',
        help='List tasks',
        description='List all tasks in the project with their status'
    )
    task_list_parser.add_argument(
        '--status',
        choices=['all', 'pending', 'in_progress', 'completed', 'blocked'],
        default='all',
        help='Filter tasks by status'
    )


def _add_execute_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add execution-related commands"""

    # Execute command
    execute_parser = subparsers.add_parser(
        'execute',
        help='Task execution commands',
        description='Commands for executing tasks and tracking progress'
    )
    execute_subparsers = execute_parser.add_subparsers(
        dest='execute_command',
        help='Execution subcommands',
        metavar='SUBCOMMAND'
    )

    # Execute start subcommand
    execute_start_parser = execute_subparsers.add_parser(
        'start',
        help='Start executing tasks',
        description='Start executing a plan or specific tasks'
    )
    execute_start_parser.add_argument(
        'target',
        help='Plan ID or task ID to execute (default: all pending tasks)'
    )

    # Execute status subcommand
    execute_status_parser = execute_subparsers.add_parser(
        'status',
        help='Show execution status',
        description='Show current execution status and progress'
    )
    execute_status_parser.add_argument(
        'target',
        nargs='?',
        help='Plan ID or task ID to show status for (default: all)'
    )


def _add_utility_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add utility commands"""

    # Decompose command
    decompose_parser = subparsers.add_parser(
        'decompose',
        help='Decompose specifications',
        description='Decompose specifications into microservices or components'
    )
    decompose_parser.add_argument(
        'spec_id',
        nargs='?',
        help='Specification ID to decompose (default: latest)'
    )
    decompose_parser.add_argument(
        '--components',
        help='Comma-separated list of components to extract'
    )
    decompose_parser.add_argument(
        '--format',
        choices=['markdown', 'yaml', 'json'],
        default='markdown',
        help='Output format for decomposition'
    )

    # Sync command
    sync_parser = subparsers.add_parser(
        'sync',
        help='Synchronize project state',
        description='Synchronize project state with memory and Git repository'
    )

    # List specs command
    list_specs_parser = subparsers.add_parser(
        'list-specs',
        help='List specifications',
        description='List all specifications in the project with metadata'
    )

    # Expand command
    expand_parser = subparsers.add_parser(
        'expand',
        help='Expand specifications',
        description='Expand specifications to the next tier or format'
    )
    expand_parser.add_argument(
        'feature_id',
        help='Feature ID to expand'
    )
    expand_parser.add_argument(
        '--to-tier',
        required=True,
        choices=['basic', 'detailed', 'technical', 'microservices'],
        help='Target tier for expansion'
    )
    expand_parser.add_argument(
        '--show-diff',
        action='store_true',
        help='Show diff between current and expanded specification'
    )

    # Template commands
    template_parser = subparsers.add_parser(
        'template',
        help='Template management commands',
        description='Commands for managing templates'
    )
    template_subparsers = template_parser.add_subparsers(
        dest='template_command',
        help='Template subcommands',
        metavar='SUBCOMMAND'
    )

    # Template list subcommand
    template_list_parser = template_subparsers.add_parser(
        'list',
        help='List templates',
        description='List available templates by category'
    )
    template_list_parser.add_argument(
        '--category',
        choices=['all', 'spec', 'plan', 'task', 'decomposition'],
        default='all',
        help='Filter templates by category'
    )

    # Template validate subcommand
    template_validate_parser = template_subparsers.add_parser(
        'validate',
        help='Validate templates',
        description='Validate template syntax and structure'
    )
    template_validate_parser.add_argument(
        'template_name',
        nargs='?',
        help='Template name to validate (default: all)'
    )
    template_validate_parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix template issues where possible'
    )

    # Template preview subcommand
    template_preview_parser = template_subparsers.add_parser(
        'preview',
        help='Preview template rendering',
        description='Preview how a template will render with sample data'
    )
    template_preview_parser.add_argument(
        'template_name',
        help='Template name to preview'
    )

    # Checkpoint commands
    checkpoint_parser = subparsers.add_parser(
        'checkpoint',
        help='Checkpoint management commands',
        description='Commands for managing development checkpoints'
    )
    checkpoint_subparsers = checkpoint_parser.add_subparsers(
        dest='checkpoint_command',
        help='Checkpoint subcommands',
        metavar='SUBCOMMAND'
    )

    # Checkpoint create subcommand
    checkpoint_create_parser = checkpoint_subparsers.add_parser(
        'create',
        help='Create a checkpoint',
        description='Create a development checkpoint for current state'
    )
    checkpoint_create_parser.add_argument(
        'feature_id',
        help='Feature ID for the checkpoint'
    )
    checkpoint_create_parser.add_argument(
        'description',
        help='Description of the checkpoint'
    )

    # Checkpoint list subcommand
    checkpoint_list_parser = checkpoint_subparsers.add_parser(
        'list',
        help='List checkpoints',
        description='List all checkpoints for a feature'
    )
    checkpoint_list_parser.add_argument(
        'feature_id',
        help='Feature ID to list checkpoints for'
    )

    # Checkpoint restore subcommand
    checkpoint_restore_parser = checkpoint_subparsers.add_parser(
        'restore',
        help='Restore a checkpoint',
        description='Restore project state from a checkpoint'
    )
    checkpoint_restore_parser.add_argument(
        'feature_id',
        help='Feature ID for the checkpoint'
    )
    checkpoint_restore_parser.add_argument(
        'checkpoint_name',
        help='Name of the checkpoint to restore'
    )
    checkpoint_restore_parser.add_argument(
        '--force',
        action='store_true',
        help='Force restoration without confirmation'
    )

    # Checkpoint cleanup subcommand
    checkpoint_cleanup_parser = checkpoint_subparsers.add_parser(
        'cleanup',
        help='Clean up old checkpoints',
        description='Remove old checkpoints to save space'
    )
    checkpoint_cleanup_parser.add_argument(
        'feature_id',
        help='Feature ID to clean up checkpoints for'
    )
    checkpoint_cleanup_parser.add_argument(
        '--older-than',
        type=int,
        default=30,
        help='Remove checkpoints older than this many days (default: 30)'
    )

    # Spec progress command
    spec_progress_parser = subparsers.add_parser(
        'spec-progress',
        help='Show specification progress',
        description='Show progress of specification development'
    )
    spec_progress_parser.add_argument(
        'feature_id',
        help='Feature ID to show progress for'
    )


def _add_slash_commands(subparsers: argparse._SubParsersAction) -> None:
    """Add v2.1.3+ slash commands for Claude/Gemini integration"""

    # sp-pulse command
    sp_pulse_parser = subparsers.add_parser(
        'sp-pulse',
        help='Initialize new feature (slash command)',
        description='Initialize a new feature with full structure - equivalent to "feature init"'
    )
    sp_pulse_parser.add_argument(
        'feature_description',
        help='Description of the feature (e.g., "User Authentication System")'
    )
    sp_pulse_parser.add_argument(
        '--name',
        help='Feature name (auto-generated if not provided)'
    )
    sp_pulse_parser.add_argument(
        '--tier',
        choices=['basic', 'detailed', 'technical'],
        default='detailed',
        help='Initial specification tier'
    )

    # sp-spec command
    sp_spec_parser = subparsers.add_parser(
        'sp-spec',
        help='Create new specification (slash command)',
        description='Create a new specification - equivalent to "spec create"'
    )
    sp_spec_parser.add_argument(
        'spec_description',
        help='Description of the specification to create'
    )
    sp_spec_parser.add_argument(
        '--tier',
        choices=['basic', 'detailed', 'technical'],
        default='detailed',
        help='Specification tier/complexity level'
    )

    # sp-plan command
    sp_plan_parser = subparsers.add_parser(
        'sp-plan',
        help='Create new implementation plan (slash command)',
        description='Create an implementation plan - equivalent to "plan create"'
    )
    sp_plan_parser.add_argument(
        'plan_description',
        help='Description of the plan to create'
    )
    sp_plan_parser.add_argument(
        '--spec-id',
        help='Specification ID to create plan for'
    )

    # sp-task command
    sp_task_parser = subparsers.add_parser(
        'sp-task',
        help='Break down into tasks (slash command)',
        description='Break down specifications into tasks - equivalent to "task breakdown"'
    )
    sp_task_parser.add_argument(
        'target',
        help='Plan ID or specification to break down'
    )
    sp_task_parser.add_argument(
        '--template',
        help='Task template to use'
    )


def _add_utility_commands_working(subparsers: argparse._SubParsersAction) -> None:
    """Add only working utility commands"""

    # List specs command (working)
    list_specs_parser = subparsers.add_parser(
        'list-specs',
        help='List all specifications',
        description='List all specifications in the project with their status'
    )
    list_specs_parser.add_argument(
        '--format',
        choices=['table', 'json', 'markdown'],
        default='table',
        help='Output format for the list'
    )

    # Template commands (partially working)
    template_parser = subparsers.add_parser(
        'template',
        help='Template management commands',
        description='Commands for managing templates'
    )
    template_subparsers = template_parser.add_subparsers(
        dest='template_command',
        help='Template subcommands',
        metavar='SUBCOMMAND'
    )

    # Template list subcommand (working)
    template_list_parser = template_subparsers.add_parser(
        'list',
        help='List templates',
        description='List available templates by category'
    )
    template_list_parser.add_argument(
        '--category',
        choices=['all', 'spec', 'plan', 'task', 'decomposition'],
        default='all',
        help='Filter templates by category'
    )