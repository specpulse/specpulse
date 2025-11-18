#!/usr/bin/env python3
"""
SpecPulse CLI - Main entry point (Refactored)

This is the main entry point for the SpecPulse CLI application.
It uses the CommandHandler for actual functionality while keeping
the main module small and focused on initialization and command routing.
"""

import sys
from pathlib import Path

from .handlers.command_handler import CommandHandler
from .parsers.subcommand_parsers import create_argument_parser


def main():
    """Main entry point for SpecPulse CLI"""
    try:
        # Debug: Set UTF-8 encoding first
        # BUG-005 FIX: Removed duplicate sys import (already imported at module level line 10)
        import os
        if sys.platform == "win32":
            os.system('chcp 65001 > nul')

        # Create argument parser
        from .parsers.subcommand_parsers import create_argument_parser
        parser = create_argument_parser()

        # Parse arguments
        args = parser.parse_args()

        # Create command handler
        handler = CommandHandler(
            no_color=args.no_color,
            verbose=args.verbose
        )

        # Execute the command
        if hasattr(args, 'command') and args.command:
            result = handler.execute_command(args.command, **vars(args))
            # Print result if available
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'feature_command') and args.feature_command:
            result = handler.execute_command('feature', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'spec_command') and args.spec_command:
            result = handler.execute_command('spec', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'plan_command') and args.plan_command:
            result = handler.execute_command('plan', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'task_command') and args.task_command:
            result = handler.execute_command('task', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'execute_command') and args.execute_command:
            result = handler.execute_command('execute', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'template_command') and args.template_command:
            result = handler.execute_command('template', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        elif hasattr(args, 'checkpoint_command') and args.checkpoint_command:
            # Handle checkpoint subcommands
            result = handler.execute_command('checkpoint', **vars(args))
            if result is not None and hasattr(result, '__str__'):
                print(result)
        else:
            # Unknown command or no command
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)
    except SystemExit:
        # Re-raise SystemExit to maintain exit codes
        raise
    except Exception as e:
        try:
            sys.stdout.write(f"Error: {e}\n")
        except UnicodeEncodeError:
            sys.stdout.write("Error: Unicode encoding issue - try setting UTF-8 encoding (chcp 65001 on Windows)\n")
        sys.exit(1)


if __name__ == "__main__":
    main()