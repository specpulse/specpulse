#!/usr/bin/env python3
"""Simple test to isolate Unicode issue"""

import sys
import os

# Set UTF-8 encoding
if sys.platform == "win32":
    os.system('chcp 65001 > nul')

# Add SpecPulse to path
sys.path.insert(0, r'D:\codebox\__PIP__\SpecPulse')

try:
    from specpulse.utils.console import Console

    console = Console()
    console.error("Test error message")
    print("Console error test passed")

except Exception as e:
    import traceback
    print(f"Error in console test: {e}")
    traceback.print_exc()