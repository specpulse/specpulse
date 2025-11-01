"""
SpecPulse Error Handler - Enhanced error handling and user feedback
Provides comprehensive error handling with recovery suggestions and user-friendly messages
"""

import sys
import traceback
from pathlib import Path
from typing import Optional, Dict, List, Any
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SpecPulseError(Exception):
    """Base class for SpecPulse errors"""

    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 recovery_suggestions: Optional[List[str]] = None,
                 technical_details: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.recovery_suggestions = recovery_suggestions or []
        self.technical_details = technical_details


class ValidationError(SpecPulseError):
    """Validation related errors"""

    def __init__(self, message: str, validation_type: str = "general",
                 missing_items: Optional[List[str]] = None):
        suggestions = [
            f"Run 'specpulse validate --fix' to automatically fix common issues",
            f"Check the {validation_type} structure against documentation",
            "Ensure all required sections are present"
        ]
        if missing_items:
            suggestions.insert(0, f"Add missing items: {', '.join(missing_items)}")

        super().__init__(
            message=message,
            severity=ErrorSeverity.MEDIUM,
            recovery_suggestions=suggestions,
            technical_details=f"Validation failed for {validation_type}"
        )
        self.validation_type = validation_type
        self.missing_items = missing_items or []


class ProjectStructureError(SpecPulseError):
    """Project structure related errors"""

    def __init__(self, message: str, missing_dirs: Optional[List[str]] = None):
        suggestions = [
            "Run 'specpulse init' to initialize project structure",
            "Ensure you're in a SpecPulse project directory",
            "Check that all required directories exist"
        ]
        if missing_dirs:
            suggestions.insert(0, f"Create missing directories: {', '.join(missing_dirs)}")

        super().__init__(
            message=message,
            severity=ErrorSeverity.HIGH,
            recovery_suggestions=suggestions,
            technical_details=f"Missing directories: {missing_dirs or []}"
        )
        self.missing_dirs = missing_dirs or []


class TemplateError(SpecPulseError):
    """Template related errors"""

    def __init__(self, message: str, template_name: Optional[str] = None):
        suggestions = [
            "Run 'specpulse update' to refresh templates",
            "Ensure templates directory exists and contains required files",
            "Check template permissions"
        ]
        if template_name:
            suggestions.insert(0, f"Verify template file: {template_name}")

        super().__init__(
            message=message,
            severity=ErrorSeverity.HIGH,
            recovery_suggestions=suggestions,
            technical_details=f"Template error: {template_name or 'unknown'}"
        )
        self.template_name = template_name


class GitError(SpecPulseError):
    """Git operation errors"""

    def __init__(self, message: str, operation: Optional[str] = None):
        suggestions = [
            "Check if Git is installed and accessible",
            "Ensure you're in a Git repository",
            "Verify Git configuration"
        ]
        if operation:
            suggestions.insert(0, f"Check Git permissions for: {operation}")

        super().__init__(
            message=message,
            severity=ErrorSeverity.MEDIUM,
            recovery_suggestions=suggestions,
            technical_details=f"Git operation failed: {operation or 'unknown'}"
        )
        self.operation = operation


class ResourceError(SpecPulseError):
    """Resource loading errors with specific recovery"""

    def __init__(self, resource_type: str, resource_path: Path):
        suggestions = [
            f"Reinstall SpecPulse: pip install --force-reinstall specpulse",
            f"Check package integrity: pip check specpulse",
            f"Verify resource exists: {resource_path}",
            f"Try development install: pip install -e .",
        ]
        super().__init__(
            message=f"Failed to load {resource_type} from {resource_path}",
            severity=ErrorSeverity.CRITICAL,
            recovery_suggestions=suggestions,
            technical_details=f"Resource path: {resource_path}"
        )
        self.resource_type = resource_type
        self.resource_path = resource_path


class ErrorHandler:
    """Enhanced error handler for SpecPulse CLI"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.error_counts = {
            ErrorSeverity.LOW: 0,
            ErrorSeverity.MEDIUM: 0,
            ErrorSeverity.HIGH: 0,
            ErrorSeverity.CRITICAL: 0
        }

    def handle_error(self, error: Exception, context: Optional[str] = None) -> int:
        """Handle an error with user-friendly output and return exit code"""

        # Count error by severity
        if isinstance(error, SpecPulseError):
            self.error_counts[error.severity] += 1
            return self._handle_specpulse_error(error, context)
        else:
            self.error_counts[ErrorSeverity.HIGH] += 1
            return self._handle_generic_error(error, context)

    def _handle_specpulse_error(self, error: SpecPulseError, context: Optional[str] = None) -> int:
        """Handle SpecPulse-specific errors"""

        from .console import Console
        console = Console()

        # Print error header
        console.error(error.message)

        if context:
            console.info(f"Context: {context}")

        # Print recovery suggestions
        if error.recovery_suggestions:
            console.warning("Recovery suggestions:")
            for i, suggestion in enumerate(error.recovery_suggestions, 1):
                console.info(f"   {i}. {suggestion}")

        # Print technical details if verbose
        if self.verbose and error.technical_details:
            console.warning(f"Technical details: {error.technical_details}")

        # Suggest getting help
        console.info("Need more help? Run 'specpulse --help' or visit docs")

        # Return appropriate exit code based on severity
        exit_codes = {
            ErrorSeverity.LOW: 0,
            ErrorSeverity.MEDIUM: 1,
            ErrorSeverity.HIGH: 2,
            ErrorSeverity.CRITICAL: 3
        }

        return exit_codes[error.severity]

    def _handle_generic_error(self, error: Exception, context: Optional[str] = None) -> int:
        """Handle generic Python errors"""

        from .console import Console
        console = Console()

        # Print error header
        console.error(f"Unexpected error: {str(error)}")

        if context:
            console.info(f"Context: {context}")

        # Common recovery suggestions for unexpected errors
        suggestions = [
            "Check file permissions and disk space",
            "Ensure all required directories exist",
            "Try running with --verbose for more details",
            "Report this issue if it persists"
        ]

        console.warning("Recovery suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            console.info(f"   {i}. {suggestion}")

        # Print traceback if verbose
        if self.verbose:
            console.warning("Full error traceback:")
            traceback_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            for line in traceback_str.split('\n'):
                if line.strip():
                    console.info(f"   {line}")

        console.info("Need more help? Run 'specpulse --help' or visit docs")

        return 2  # High severity exit code for unexpected errors

    def suggest_command_correction(self, command: str, available_commands: List[str]) -> Optional[str]:
        """Suggest correction for mistyped commands using Levenshtein distance"""

        def levenshtein_distance(s1: str, s2: str) -> int:
            """Calculate Levenshtein distance between two strings"""
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        # Find closest matches
        best_match = None
        best_distance = float('inf')

        for available in available_commands:
            distance = levenshtein_distance(command.lower(), available.lower())
            if distance < best_distance and distance <= 2:  # Allow up to 2 character differences
                best_distance = distance
                best_match = available

        return best_match

    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of errors by severity"""
        return {
            severity.value: count
            for severity, count in self.error_counts.items()
            if count > 0
        }

    def reset_error_counts(self):
        """Reset error counters"""
        for severity in self.error_counts:
            self.error_counts[severity] = 0


# Global error handler instance
_global_error_handler: Optional[ErrorHandler] = None


def get_error_handler(verbose: bool = False) -> ErrorHandler:
    """Get or create global error handler"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler(verbose=verbose)
    return _global_error_handler


def handle_specpulse_error(error: Exception, context: Optional[str] = None, verbose: bool = False) -> int:
    """Convenience function to handle errors"""
    handler = get_error_handler(verbose=verbose)
    return handler.handle_error(error, context)


def validate_project_directory(path: Path) -> None:
    """Validate that the given path is a valid SpecPulse project"""

    # Check for new structure (v2.2.0+)
    specpulse_dir = path / ".specpulse"
    if specpulse_dir.exists():
        required_dirs = ['.specpulse/specs', '.specpulse/plans', '.specpulse/tasks', '.specpulse/memory', '.specpulse/templates']
        missing_dirs = []

        for dir_name in required_dirs:
            dir_path = path / dir_name
            if not dir_path.exists() or not dir_path.is_dir():
                missing_dirs.append(dir_name)

        if missing_dirs:
            raise ProjectStructureError(
                f"Invalid SpecPulse project directory: {path}",
                missing_dirs=missing_dirs
            )
        return

    # Check for legacy structure (pre-v2.2.0)
    required_dirs = ['specs', 'plans', 'tasks', 'memory', 'templates']
    missing_dirs = []

    for dir_name in required_dirs:
        dir_path = path / dir_name
        if not dir_path.exists() or not dir_path.is_dir():
            missing_dirs.append(dir_name)

    if missing_dirs:
        raise ProjectStructureError(
            f"Invalid SpecPulse project directory: {path}",
            missing_dirs=missing_dirs
        )


def validate_templates(template_dir: Path) -> None:
    """Validate that required templates exist"""

    required_templates = ['spec.md', 'plan.md', 'task.md']
    missing_templates = []

    for template in required_templates:
        template_path = template_dir / template
        if not template_path.exists() or not template_path.is_file():
            missing_templates.append(template)

    if missing_templates:
        raise TemplateError(
            f"Missing required templates in {template_dir}",
            template_name=', '.join(missing_templates)
        )


def suggest_recovery_for_error(error_message: str) -> List[str]:
    """Suggest recovery actions based on error message patterns"""

    suggestions = []

    # Common error patterns and their suggestions
    error_patterns = {
        r'permission.*denied': [
            "Check file and directory permissions",
            "Try running with appropriate privileges",
            "Ensure the script files are executable"
        ],
        r'no such file.*directory': [
            "Check that the project directory exists",
            "Ensure you're in the correct directory",
            "Run 'specpulse init' if this is a new project"
        ],
        r'template.*not found': [
            "Run 'specpulse update' to refresh templates",
            "Check templates directory exists",
            "Verify template files are present"
        ],
        r'git.*not found': [
            "Install Git if not present",
            "Check Git is in your PATH",
            "Ensure Git repository is initialized"
        ],
        r'validation.*failed': [
            "Run 'specpulse validate --fix' to auto-fix issues",
            "Check project structure requirements",
            "Review validation error details"
        ]
    }

    import re
    for pattern, pattern_suggestions in error_patterns.items():
        if re.search(pattern, error_message, re.IGNORECASE):
            suggestions.extend(pattern_suggestions)
            break

    # Add general suggestions if no specific matches
    if not suggestions:
        suggestions = [
            "Try running with --verbose for more details",
            "Check the documentation for troubleshooting",
            "Report this issue if it persists"
        ]

    return suggestions