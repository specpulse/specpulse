"""
Entry point for running SpecPulse as a module.

This allows running: python -m specpulse
"""

from .cli.main import main

if __name__ == "__main__":
    main()