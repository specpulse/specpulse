"""
SpecPulse: Specification-Driven Development Framework
Built for the AI era
"""

__version__ = "1.0.3"
__author__ = "SpecPulse"
__url__ = "https://github.com/specpulse"

from .core.specpulse import SpecPulse
from .cli.main import main

__all__ = ["SpecPulse", "main"]