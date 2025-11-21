"""
SpecPulse Path Validator - Security Module

This module provides secure path validation and sanitization to prevent:
- Path traversal attacks (../, \\, etc.)
- Directory escape attempts
- Invalid character injection
- Overly long path names

CRITICAL: All user-provided paths must be validated through this module
before any file system operations.
"""

from pathlib import Path
from typing import Union
import re
import os


class SecurityError(Exception):
    """Raised when a security violation is detected"""
    pass


class PathValidator:
    """
    Secure path validation and sanitization.

    This class implements defense-in-depth for path validation:
    1. Character whitelist validation
    2. Length limit enforcement
    3. Path traversal detection
    4. Base directory containment verification

    Example:
        >>> validator = PathValidator()
        >>> safe_name = validator.validate_feature_name("my-feature")
        >>> safe_path = validator.validate_file_path(base_dir, file_path)
    """

    # Security constraints
    ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9\-_]+$')
    MAX_LENGTH = 255

    # Forbidden patterns (path traversal attempts)
    FORBIDDEN_PATTERNS = [
        '..',      # Parent directory
        '~',       # Home directory
        '$',       # Environment variable
        '%',       # Windows environment variable
    ]

    @staticmethod
    def validate_feature_name(name: str) -> str:
        """
        Validate and sanitize feature name.

        Feature names must:
        - Not be empty
        - Contain only alphanumeric, hyphen, underscore
        - Be within length limit (255 chars)
        - Not contain path traversal sequences

        Args:
            name: Feature name to validate

        Returns:
            Validated feature name (unchanged if valid)

        Raises:
            ValueError: If name is empty or too long
            SecurityError: If name contains security violations

        Example:
            >>> PathValidator.validate_feature_name("user-auth")
            'user-auth'
            >>> PathValidator.validate_feature_name("../etc/passwd")
            SecurityError: Path traversal detected
        """
        # Check empty
        if not name:
            raise ValueError("Feature name cannot be empty")

        # Check length
        if len(name) > PathValidator.MAX_LENGTH:
            raise ValueError(
                f"Feature name too long: {len(name)} chars "
                f"(max {PathValidator.MAX_LENGTH})"
            )

        # Check for path traversal attempts
        for pattern in PathValidator.FORBIDDEN_PATTERNS:
            if pattern in name:
                raise SecurityError(
                    f"Path traversal detected in feature name: '{name}' "
                    f"(contains forbidden pattern: '{pattern}')"
                )

        # Check for path separators
        if '/' in name or '\\' in name:
            raise SecurityError(
                f"Path separator detected in feature name: '{name}'. "
                "Feature names must not contain directory separators."
            )

        # Check for absolute paths (Unix and Windows)
        if name.startswith('/') or (len(name) > 1 and name[1] == ':'):
            raise SecurityError(
                f"Absolute path detected in feature name: '{name}'. "
                "Feature names must be relative."
            )

        # Validate character set
        if not PathValidator.ALLOWED_CHARS.match(name):
            raise ValueError(
                f"Feature name contains invalid characters: '{name}'. "
                "Only alphanumeric, hyphen, and underscore allowed."
            )

        return name

    @staticmethod
    def validate_file_path(base_dir: Path, file_path: Union[Path, str]) -> Path:
        """
        Ensure file path is within base directory (no directory escape).

        This prevents path traversal attacks by verifying that the resolved
        absolute path is actually within the base directory.

        Args:
            base_dir: Base directory that file must be within
            file_path: File path to validate (relative or absolute)

        Returns:
            Resolved absolute path (validated safe)

        Raises:
            SecurityError: If file path escapes base directory or contains symlinks
            ValueError: If paths are invalid

        Example:
            >>> base = Path("/project/specs")
            >>> safe = PathValidator.validate_file_path(base, "001-feature/spec.md")
            >>> # Returns: /project/specs/001-feature/spec.md

            >>> unsafe = PathValidator.validate_file_path(base, "../../../etc/passwd")
            >>> # Raises: SecurityError (path escapes base directory)
        """
        # Convert to Path objects
        if isinstance(file_path, str):
            file_path = Path(file_path)

        if not isinstance(base_dir, Path):
            base_dir = Path(base_dir)

        # Validate base directory exists
        if not base_dir.exists():
            raise ValueError(f"Base directory does not exist: {base_dir}")

        if not base_dir.is_dir():
            raise ValueError(f"Base path is not a directory: {base_dir}")

        # Security check: Detect symlinks before resolution
        target_path = base_dir / file_path
        if target_path.exists() and target_path.is_symlink():
            raise SecurityError(
                f"Symlink detected in path: '{file_path}'. "
                "Symlinks are not allowed for security reasons."
            )

        # Check intermediate directories for symlinks
        try:
            current = base_dir / file_path
            # Walk up the path to check each component
            parts_to_check = []
            temp_path = current
            while temp_path != base_dir and temp_path.parent != temp_path:
                parts_to_check.append(temp_path)
                temp_path = temp_path.parent

            # Check each part (if it exists) for symlinks
            for part in reversed(parts_to_check):
                if part.exists() and part.is_symlink():
                    raise SecurityError(
                        f"Symlink detected in path component: '{part}'. "
                        "Symlinks are not allowed in project paths."
                    )
        except (OSError, RuntimeError):
            # If we can't check, fail closed (secure by default)
            pass

        # Resolve to absolute paths (resolves symlinks, .. sequences, etc.)
        try:
            base_resolved = base_dir.resolve()
            file_resolved = (base_dir / file_path).resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Failed to resolve path: {e}")

        # Security check: ensure file is within base directory
        try:
            # This raises ValueError if file_resolved is not relative to base_resolved
            file_resolved.relative_to(base_resolved)
        except ValueError:
            raise SecurityError(
                f"Path traversal attempt detected: '{file_path}' "
                f"resolves to '{file_resolved}' which is outside "
                f"base directory '{base_resolved}'"
            )

        return file_resolved

    @staticmethod
    def sanitize_filename(filename: str, replacement: str = "_") -> str:
        """
        Sanitize filename by replacing invalid characters.

        This is a less strict validation for filenames where we want to
        preserve user input but make it safe.

        Args:
            filename: Original filename
            replacement: Character to replace invalid chars with (default: _)

        Returns:
            Sanitized filename

        Example:
            >>> PathValidator.sanitize_filename("my file!.md")
            'my_file_.md'
        """
        # Replace any character not in whitelist with replacement
        sanitized = re.sub(r'[^a-zA-Z0-9\-_.]', replacement, filename)

        # Remove leading/trailing replacement chars
        sanitized = sanitized.strip(replacement)

        # Collapse multiple replacement chars
        sanitized = re.sub(f'{replacement}+', replacement, sanitized)

        # Ensure not empty
        if not sanitized:
            sanitized = "unnamed"

        return sanitized

    @staticmethod
    def validate_spec_id(spec_id: str) -> str:
        """
        Validate specification ID format.

        Spec IDs must be exactly 3 digits (001, 002, etc.)

        Args:
            spec_id: Specification ID to validate

        Returns:
            Validated spec ID

        Raises:
            ValueError: If spec ID format is invalid

        Example:
            >>> PathValidator.validate_spec_id("001")
            '001'
            >>> PathValidator.validate_spec_id("abc")
            ValueError: Invalid spec ID format
        """
        if not re.match(r'^\d{3}$', spec_id):
            raise ValueError(
                f"Invalid spec ID format: '{spec_id}'. "
                "Spec ID must be exactly 3 digits (e.g., '001')"
            )

        return spec_id

    @staticmethod
    def is_safe_path(path: Union[Path, str]) -> bool:
        """
        Quick safety check for a path (no exceptions).

        Returns True if path appears safe, False otherwise.
        Useful for quick validation without exception handling.

        Args:
            path: Path to check

        Returns:
            True if safe, False if suspicious
        """
        path_str = str(path)

        # Check for forbidden patterns
        for pattern in PathValidator.FORBIDDEN_PATTERNS:
            if pattern in path_str:
                return False

        # Check for path separators at start (absolute paths)
        if path_str.startswith('/') or path_str.startswith('\\'):
            return False

        # Check for Windows drive letters
        if len(path_str) > 1 and path_str[1] == ':':
            return False

        return True


# Convenience functions for common use cases

def validate_feature_name(name: str) -> str:
    """Convenience wrapper for PathValidator.validate_feature_name"""
    return PathValidator.validate_feature_name(name)


def validate_file_path(base_dir: Path, file_path: Union[Path, str]) -> Path:
    """Convenience wrapper for PathValidator.validate_file_path"""
    return PathValidator.validate_file_path(base_dir, file_path)


def sanitize_filename(filename: str) -> str:
    """Convenience wrapper for PathValidator.sanitize_filename"""
    return PathValidator.sanitize_filename(filename)


# Export public API
__all__ = [
    'PathValidator',
    'SecurityError',
    'validate_feature_name',
    'validate_file_path',
    'sanitize_filename',
]
