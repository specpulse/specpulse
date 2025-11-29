"""
LLM-SAFE File Operations Module

This module provides strict file and folder operations that prevent
LLM from making arbitrary decisions about naming and structure.

CRITICAL RULES:
1. ALL directory names MUST follow strict patterns
2. ALL file names MUST follow strict patterns
3. NO arbitrary naming allowed
4. ALL operations are validated before execution
5. ATOMIC operations to prevent race conditions
"""

import re
import os
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import time
import hashlib
from .universal_id_generator import get_universal_id_generator, IDType

class LLMSafeFileOperations:
    """
    LLM-Safe file operations with strict validation and atomic operations.

    This class enforces strict naming conventions and prevents LLM from
    making arbitrary decisions about file/folder names and structures.
    """

    # STRICT NAMING PATTERNS - NO EXCEPTIONS
    FEATURE_DIR_PATTERN = re.compile(r'^\d{3}-[a-z0-9-]+$')  # 001-feature-name
    SPEC_FILE_PATTERN = re.compile(r'^spec-\d{3}\.md$')     # spec-001.md
    PLAN_FILE_PATTERN = re.compile(r'^plan-\d{3}\.md$')     # plan-001.md
    TASK_FILE_PATTERN = re.compile(r'^T\d{3}\.md$')        # T001.md
    SERVICE_TASK_PATTERN = re.compile(r'^[A-Z]+-T\d{3}\.md$')  # AUTH-T001.md

    # MAX LENGTHS
    MAX_FEATURE_NAME_LENGTH = 50
    MAX_FILE_PATH_LENGTH = 255

    # FORBIDDEN CHARACTERS
    FORBIDDEN_CHARS = '<>:"|?*'
    FORBIDDEN_NAMES = {
        '.', '..', 'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }

    def __init__(self, project_root: Path):
        """
        Initialize LLM-safe operations.

        Args:
            project_root: Project root directory
        """
        self.project_root = Path(project_root).resolve()
        self.specpulse_dir = self.project_root / ".specpulse"

        # Ensure base structure exists
        self._ensure_base_structure()

    def _ensure_base_structure(self):
        """Create required .specpulse directory structure."""
        required_dirs = [
            "specs", "plans", "tasks", "memory", "templates",
            "checkpoints", "cache", "logs"
        ]

        for dir_name in required_dirs:
            (self.specpulse_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def sanitize_feature_name(self, feature_name: str) -> str:
        """
        Sanitize feature name according to strict rules.

        Rules:
        - Convert to lowercase
        - Replace spaces and underscores with hyphens
        - Remove special characters except alphanumeric and hyphens
        - Limit length
        - Remove consecutive hyphens
        - Remove leading/trailing hyphens

        Args:
            feature_name: Raw feature name

        Returns:
            Sanitized feature name

        Raises:
            ValueError: If feature name cannot be sanitized
        """
        if not feature_name or not feature_name.strip():
            raise ValueError("Feature name cannot be empty")

        # Convert to lowercase and trim
        name = feature_name.strip().lower()

        # Replace spaces and underscores with hyphens
        name = re.sub(r'[\s_]+', '-', name)

        # Remove all characters except alphanumeric and hyphens
        name = re.sub(r'[^a-z0-9-]', '', name)

        # Remove consecutive hyphens
        name = re.sub(r'-+', '-', name)

        # Remove leading/trailing hyphens
        name = name.strip('-')

        # Validate minimum length
        if len(name) < 2:
            raise ValueError(f"Feature name too short after sanitization: '{name}'")

        # Validate maximum length
        if len(name) > self.MAX_FEATURE_NAME_LENGTH:
            name = name[:self.MAX_FEATURE_NAME_LENGTH]
            # Ensure we don't end with hyphen after truncation
            name = name.rstrip('-')

        if not name:
            raise ValueError("Feature name became empty after sanitization")

        return name

    def validate_feature_dir_name(self, dir_name: str) -> bool:
        """
        Validate feature directory name follows strict pattern.

        Pattern: XXX-feature-name where XXX is 3-digit number
        Example: 001-user-authentication

        Args:
            dir_name: Directory name to validate

        Returns:
            True if valid, False otherwise
        """
        return bool(self.FEATURE_DIR_PATTERN.fullmatch(dir_name))

    def generate_next_feature_id(self) -> str:
        """
        Generate next available feature ID using universal system.

        Uses the universal ID generator to ensure consistency across
        all numbering systems in the project.

        Returns:
            Next feature ID as 3-digit string (e.g., "001", "042")

        Raises:
            ValueError: If ID generation fails
            TimeoutError: If cannot acquire lock within timeout
        """
        id_generator = get_universal_id_generator(self.project_root)
        return id_generator.get_next_id(IDType.FEATURE)

    def create_feature_directories(self, feature_name: str) -> Tuple[str, Dict[str, Path]]:
        """
        Create feature directories with strict validation.

        This is the ONLY approved way to create feature directories.
        LLM CANNOT create arbitrary directories.

        Args:
            feature_name: Feature name (will be sanitized)

        Returns:
            Tuple of (feature_id, dictionary of created directories)

        Raises:
            ValueError: If validation fails
            OSError: If directory creation fails
        """
        # Sanitize feature name
        safe_name = self.sanitize_feature_name(feature_name)

        # Generate feature ID
        feature_id = self.generate_next_feature_id()

        # Create directory name
        dir_name = f"{feature_id}-{safe_name}"

        # Validate directory name
        if not self.validate_feature_dir_name(dir_name):
            raise ValueError(f"Invalid directory name: {dir_name}")

        # Create directories
        base_dir = self.specpulse_dir
        created_dirs = {}

        for subdir in ["specs", "plans", "tasks"]:
            dir_path = base_dir / subdir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs[subdir] = dir_path

        return feature_id, created_dirs

    def generate_spec_file_path(self, feature_dir: str, spec_number: Optional[int] = None) -> Path:
        """
        Generate validated spec file path using universal system.

        Args:
            feature_dir: Feature directory name (must be validated)
            spec_number: Spec number (auto-generated if None)

        Returns:
            Validated Path object for spec file

        Raises:
            ValueError: If validation fails
        """
        # Validate feature directory
        if not self.validate_feature_dir_name(feature_dir):
            raise ValueError(f"Invalid feature directory: {feature_dir}")

        # Use universal ID generator if not provided
        if spec_number is None:
            id_generator = get_universal_id_generator(self.project_root)
            spec_file = id_generator.get_next_id(IDType.SPECIFICATION)
        else:
            # Use provided number with validation
            if not isinstance(spec_number, int) or spec_number < 1:
                raise ValueError(f"Invalid spec number: {spec_number}")
            spec_file = f"spec-{spec_number:03d}.md"

        spec_path = self.specpulse_dir / "specs" / feature_dir / spec_file

        # Validate file name pattern
        if not self.SPEC_FILE_PATTERN.fullmatch(spec_file):
            raise ValueError(f"Invalid spec file name: {spec_file}")

        return spec_path

    def generate_plan_file_path(self, feature_dir: str, plan_number: Optional[int] = None) -> Path:
        """
        Generate validated plan file path using universal system.
        """
        if not self.validate_feature_dir_name(feature_dir):
            raise ValueError(f"Invalid feature directory: {feature_dir}")

        # Use universal ID generator if not provided
        if plan_number is None:
            id_generator = get_universal_id_generator(self.project_root)
            plan_file = id_generator.get_next_id(IDType.PLAN)
        else:
            # Use provided number with validation
            if not isinstance(plan_number, int) or plan_number < 1:
                raise ValueError(f"Invalid plan number: {plan_number}")
            plan_file = f"plan-{plan_number:03d}.md"

        plan_path = self.specpulse_dir / "plans" / feature_dir / plan_file

        if not self.PLAN_FILE_PATTERN.fullmatch(plan_file):
            raise ValueError(f"Invalid plan file name: {plan_file}")

        return plan_path

    def generate_task_file_path(self, feature_dir: str, task_number: Optional[int] = None,
                              service_prefix: Optional[str] = None) -> Path:
        """
        Generate validated task file path using universal system.

        Args:
            feature_dir: Feature directory name
            task_number: Task number (auto-generated if None)
            service_prefix: Optional service prefix (e.g., "AUTH" for AUTH-T001.md)
        """
        if not self.validate_feature_dir_name(feature_dir):
            raise ValueError(f"Invalid feature directory: {feature_dir}")

        # Use universal ID generator if not provided
        if task_number is None:
            id_generator = get_universal_id_generator(self.project_root)
            if service_prefix:
                if not re.match(r'^[A-Z]+$', service_prefix):
                    raise ValueError(f"Invalid service prefix: {service_prefix}")
                task_file = id_generator.get_next_id(IDType.SERVICE_TASK, service_prefix)
            else:
                task_file = id_generator.get_next_id(IDType.TASK)
        else:
            # Use provided number with validation
            if not isinstance(task_number, int) or task_number < 1:
                raise ValueError(f"Invalid task number: {task_number}")

            if service_prefix:
                if not re.match(r'^[A-Z]+$', service_prefix):
                    raise ValueError(f"Invalid service prefix: {service_prefix}")
                task_file = f"{service_prefix}-T{task_number:03d}.md"
                if not self.SERVICE_TASK_PATTERN.fullmatch(task_file):
                    raise ValueError(f"Invalid service task file name: {task_file}")
            else:
                task_file = f"T{task_number:03d}.md"
                if not self.TASK_FILE_PATTERN.fullmatch(task_file):
                    raise ValueError(f"Invalid task file name: {task_file}")

        return self.specpulse_dir / "tasks" / feature_dir / task_file

    def validate_file_operation(self, file_path: Path, operation: str = "write") -> bool:
        """
        Validate file operation is allowed.

        Args:
            file_path: File path to validate
            operation: Operation type (read, write, delete)

        Returns:
            True if operation is allowed

        Raises:
            ValueError: If operation is not allowed
        """
        # Resolve to absolute path
        abs_path = file_path.resolve()

        # Check if within .specpulse directory
        try:
            abs_path.relative_to(self.specpulse_dir)
        except ValueError:
            raise ValueError(f"File path outside .specpulse directory: {file_path}")

        # Check for forbidden names
        if abs_path.name in self.FORBIDDEN_NAMES:
            raise ValueError(f"Forbidden file name: {abs_path.name}")

        # Check for forbidden characters
        for char in self.FORBIDDEN_CHARS:
            if char in abs_path.name:
                raise ValueError(f"Forbidden character '{char}' in file name: {abs_path.name}")

        # Check path length
        if len(str(abs_path)) > self.MAX_FILE_PATH_LENGTH:
            raise ValueError(f"File path too long: {len(str(abs_path))} > {self.MAX_FILE_PATH_LENGTH}")

        # Check if trying to access protected directories
        protected_dirs = ["templates", "commands", ".claude", ".gemini", "specpulse"]
        for protected in protected_dirs:
            if protected in abs_path.parts and operation in ["write", "delete"]:
                raise ValueError(f"Cannot write/delete in protected directory: {protected}")

        return True

    def atomic_write_file(self, file_path: Path, content: str) -> bool:
        """
        Atomically write file with validation.

        Args:
            file_path: File path (must be validated)
            content: File content

        Returns:
            True if successful

        Raises:
            ValueError: If validation fails
            OSError: If write operation fails
        """
        # Validate operation
        self.validate_file_operation(file_path, "write")

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file first, then move (atomic)
        temp_path = file_path.with_suffix(f".tmp.{int(time.time())}")

        try:
            temp_path.write_text(content, encoding='utf-8')
            temp_path.replace(file_path)  # Atomic move
            return True

        except Exception as e:
            # Clean up temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def validate_project_structure(self) -> Dict[str, List[str]]:
        """
        Validate entire project structure for compliance.

        Returns:
            Dictionary with validation results
        """
        results = {
            "errors": [],
            "warnings": [],
            "valid": True
        }

        # Check base structure
        required_dirs = ["specs", "plans", "tasks", "memory"]
        for dir_name in required_dirs:
            dir_path = self.specpulse_dir / dir_name
            if not dir_path.exists():
                results["errors"].append(f"Missing required directory: {dir_name}")
                results["valid"] = False

        # Validate feature directories
        for category in ["specs", "plans", "tasks"]:
            category_dir = self.specpulse_dir / category
            if not category_dir.exists():
                continue

            for feature_dir in category_dir.iterdir():
                if feature_dir.is_dir():
                    if not self.validate_feature_dir_name(feature_dir.name):
                        results["errors"].append(
                            f"Invalid feature directory name: {category}/{feature_dir.name}"
                        )
                        results["valid"] = False

        return results


# Singleton instance for easy access
_llm_safe_ops = None

def get_llm_safe_operations(project_root: Path) -> LLMSafeFileOperations:
    """Get or create LLM-safe operations instance."""
    global _llm_safe_ops
    if _llm_safe_ops is None or _llm_safe_ops.project_root != Path(project_root).resolve():
        _llm_safe_ops = LLMSafeFileOperations(project_root)
    return _llm_safe_ops