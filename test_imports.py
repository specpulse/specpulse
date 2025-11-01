#!/usr/bin/env python3
"""Test imports to find Unicode issue"""

import sys
import os

# Set UTF-8 encoding
if sys.platform == "win32":
    os.system('chcp 65001 > nul')

print("Testing imports...")

try:
    print("1. Importing command_handler...")
    from specpulse.cli.handlers.command_handler import CommandHandler
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

try:
    print("2. Importing subcommand_parsers...")
    from specpulse.cli.parsers.subcommand_parsers import create_argument_parser
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("Done testing imports.")