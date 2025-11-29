"""
Safe Commands Parser - Argument parsing for LLM-safe commands

This module provides argument parsers for the safe commands,
offering enhanced validation and universal ID system integration.
"""

import argparse
from typing import List


def add_safe_commands(subparsers):
    """Add LLM-safe command parsers to the main subparser"""

    # Safe Commands parent parser
    safe_parser = subparsers.add_parser(
        'safe',
        help='LLM-safe commands with universal ID system',
        description='Safe alternatives to existing commands with enhanced validation and atomic operations'
    )

    safe_subparsers = safe_parser.add_subparsers(
        dest='safe_command',
        help='Safe command subcommands',
        metavar='SUBCOMMAND'
    )

    # Feature initialization safe command
    feature_init_safe_parser = safe_subparsers.add_parser(
        'feature-init',
        help='Initialize a new feature safely (atomic operations, universal IDs)',
        description='Initialize a new feature using the safe system with universal ID generation and validation'
    )
    feature_init_safe_parser.add_argument(
        'feature_name',
        help='Name of the feature to initialize (e.g., "user-authentication")'
    )
    feature_init_safe_parser.add_argument(
        '--feature-id',
        help='Optional feature ID (auto-generated if not provided)'
    )

    # Specification creation safe command
    spec_create_safe_parser = safe_subparsers.add_parser(
        'spec-create',
        help='Create a specification safely (template validation, universal IDs)',
        description='Create a specification using the safe system with template validation and universal ID generation'
    )
    spec_create_safe_parser.add_argument(
        'description',
        help='Description of the specification'
    )
    spec_create_safe_parser.add_argument(
        '--feature-name',
        help='Target feature name (auto-detected if not provided)'
    )

    # Plan creation safe command
    plan_create_safe_parser = safe_subparsers.add_parser(
        'plan-create',
        help='Create an implementation plan safely (universal plan IDs, no conflicts)',
        description='Create an implementation plan using the safe system with universal ID generation and conflict prevention'
    )
    plan_create_safe_parser.add_argument(
        'description',
        help='Description of the implementation plan'
    )
    plan_create_safe_parser.add_argument(
        '--feature-name',
        help='Target feature name (auto-detected if not provided)'
    )

    # Task creation safe command
    task_create_safe_parser = safe_subparsers.add_parser(
        'task-create',
        help='Create a task safely (service prefixes, universal task IDs)',
        description='Create a task using the safe system with universal ID generation and service prefix support'
    )
    task_create_safe_parser.add_argument(
        'description',
        help='Description of the task'
    )
    task_create_safe_parser.add_argument(
        '--service-prefix',
        help='Service prefix for the task (e.g., AUTH, USER, PAYMENT)'
    )
    task_create_safe_parser.add_argument(
        '--feature-name',
        help='Target feature name (auto-detected if not provided)'
    )

    # Status reporting safe command
    status_safe_parser = safe_subparsers.add_parser(
        'status',
        help='Get status report safely (validated operations, ID statistics)',
        description='Get project status using safe operations with universal ID system statistics'
    )
    status_safe_parser.add_argument(
        'feature_name',
        nargs='?',
        help='Feature name to get status for (all features if not specified)'
    )
    status_safe_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed information'
    )
    status_safe_parser.add_argument(
        '--ids',
        action='store_true',
        help='Show universal ID system statistics'
    )
    status_safe_parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate project structure'
    )

    # Markdown validation safe command
    validate_safe_parser = safe_subparsers.add_parser(
        'validate',
        help='Validate markdown files safely (syntax, structure, links)',
        description='Validate all markdown files in the project with comprehensive checks'
    )
    validate_safe_parser.add_argument(
        'target',
        nargs='?',
        choices=['all', 'specs', 'plans', 'tasks', 'memory'],
        default='all',
        help='What to validate (default: all)'
    )
    validate_safe_parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to fix common issues automatically'
    )
    validate_safe_parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict validation mode'
    )
    validate_safe_parser.add_argument(
        '--format',
        choices=['table', 'json', 'summary'],
        default='table',
        help='Output format for validation results'
    )

    return safe_parser