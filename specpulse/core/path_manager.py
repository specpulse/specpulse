"""
Path Manager for SpecPulse v2.1.2

Centralized path management for all SpecPulse directories.
This class provides a single source of truth for all path resolutions,
supporting both legacy and new directory structures.

New Structure (v2.2.0+):
- .specpulse/specs/
- .specpulse/plans/
- .specpulse/tasks/
- .specpulse/memory/
- .specpulse/templates/
- .claude/ (root)
- .gemini/ (root)
"""

from pathlib import Path
from typing import Optional, Dict, Any
import warnings


class PathManager:
    """
    Centralized path management for SpecPulse projects.

    This class handles all path resolutions for both the new .specpulse/
    consolidated structure and legacy directory structures for backward compatibility.
    """

    def __init__(self, project_root: Path, use_legacy_structure: bool = False):
        """
        Initialize path manager.

        Args:
            project_root: Root directory of the project
            use_legacy_structure: If True, use legacy paths (specs/, plans/, etc.)
                                If False, use new .specpulse/ structure
        """
        self.project_root = Path(project_root)
        self.use_legacy_structure = use_legacy_structure

        # Core .specpulse directory
        self.specpulse_dir = self.project_root / ".specpulse"

        # AI integration directories (always at root)
        self.claude_dir = self.project_root / ".claude"
        self.gemini_dir = self.project_root / ".gemini"

        # System directories
        self.cache_dir = self.specpulse_dir / "cache"
        self.checkpoints_dir = self.specpulse_dir / "checkpoints"

        if use_legacy_structure:
            self._init_legacy_paths()
        else:
            self._init_new_paths()

    def _init_new_paths(self):
        """Initialize new consolidated .specpulse/ structure paths."""
        self.specs_dir = self.specpulse_dir / "specs"
        self.plans_dir = self.specpulse_dir / "plans"
        self.tasks_dir = self.specpulse_dir / "tasks"
        self.memory_dir = self.specpulse_dir / "memory"
        self.templates_dir = self.specpulse_dir / "templates"
        self.notes_dir = self.memory_dir / "notes"

    def _init_legacy_paths(self):
        """Initialize legacy structure paths for backward compatibility."""
        self.specs_dir = self.project_root / "specs"
        self.plans_dir = self.project_root / "plans"
        self.tasks_dir = self.project_root / "tasks"
        self.memory_dir = self.project_root / "memory"
        self.templates_dir = self.project_root / "templates"
        self.notes_dir = self.memory_dir / "notes"

    def get_all_directories(self) -> Dict[str, Path]:
        """
        Get all managed directories as a dictionary.

        Returns:
            Dictionary mapping directory names to Path objects
        """
        return {
            'specs': self.specs_dir,
            'plans': self.plans_dir,
            'tasks': self.tasks_dir,
            'memory': self.memory_dir,
            'templates': self.templates_dir,
            'notes': self.notes_dir,
            'cache': self.cache_dir,
            'checkpoints': self.checkpoints_dir,
            'claude': self.claude_dir,
            'gemini': self.gemini_dir,
            'specpulse': self.specpulse_dir,
        }

    def ensure_directories(self, directories: Optional[list] = None) -> bool:
        """
        Ensure specified directories exist, creating them if needed.

        Args:
            directories: List of directory names to create. If None, creates all.

        Returns:
            True if all directories were created successfully, False otherwise
        """
        if directories is None:
            directories = ['specs', 'plans', 'tasks', 'memory', 'templates',
                          'cache', 'checkpoints', 'notes']

        failed_dirs = []
        for dir_name in directories:
            dir_path = getattr(self, f"{dir_name}_dir", None)
            if dir_path is None:
                failed_dirs.append(dir_name)
                continue

            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                failed_dirs.append(dir_name)

        if failed_dirs:
            warnings.warn(f"Failed to create directories: {', '.join(failed_dirs)}")
            return False
        return True

    def get_feature_dir(self, feature_id: str, feature_name: str, dir_type: str) -> Path:
        """
        Get feature-specific directory path.

        Args:
            feature_id: Feature ID (e.g., "001")
            feature_name: Feature name (e.g., "user-auth")
            dir_type: Type of directory ('specs', 'plans', 'tasks')

        Returns:
            Path to feature directory
        """
        if dir_type not in ['specs', 'plans', 'tasks']:
            raise ValueError(f"Invalid directory type: {dir_type}")

        base_dir = getattr(self, f"{dir_type}_dir")
        return base_dir / f"{feature_id}-{feature_name}"

    def get_spec_file(self, feature_id: str, feature_name: str, spec_number: int) -> Path:
        """
        Get specification file path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name
            spec_number: Specification number

        Returns:
            Path to specification file
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'specs')
        return feature_dir / f"spec-{spec_number:03d}.md"

    def get_plan_file(self, feature_id: str, feature_name: str, plan_number: int) -> Path:
        """
        Get plan file path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name
            plan_number: Plan number

        Returns:
            Path to plan file
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'plans')
        return feature_dir / f"plan-{plan_number}.md"

    def get_task_file(self, feature_id: str, feature_name: str, task_number: int) -> Path:
        """
        Get task file path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name
            task_number: Task number

        Returns:
            Path to task file
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'tasks')
        return feature_dir / f"task-{task_number}.md"

    def get_memory_file(self, filename: str) -> Path:
        """
        Get memory file path.

        Args:
            filename: Memory filename (e.g., "context.md")

        Returns:
            Path to memory file
        """
        return self.memory_dir / filename

    def get_template_file(self, filename: str) -> Path:
        """
        Get template file path.

        Args:
            filename: Template filename (e.g., "spec.md")

        Returns:
            Path to template file
        """
        return self.templates_dir / filename

    def get_decomposition_dir(self, feature_id: str, feature_name: str) -> Path:
        """
        Get decomposition directory path.

        Args:
            feature_id: Feature ID
            feature_name: Feature name

        Returns:
            Path to decomposition directory
        """
        feature_dir = self.get_feature_dir(feature_id, feature_name, 'specs')
        return feature_dir / "decomposition"

    def detect_structure(self) -> str:
        """
        Auto-detect which directory structure is being used.

        Returns:
            'new' if .specpulse/ structure is detected,
            'legacy' if legacy structure is detected,
            'mixed' if both are present,
            'none' if no SpecPulse structure is detected
        """
        has_new_structure = self.specpulse_dir.exists() and any([
            (self.specpulse_dir / "specs").exists(),
            (self.specpulse_dir / "plans").exists(),
            (self.specpulse_dir / "tasks").exists()
        ])

        has_legacy_structure = any([
            (self.project_root / "specs").exists(),
            (self.project_root / "plans").exists(),
            (self.project_root / "tasks").exists()
        ])

        if has_new_structure and has_legacy_structure:
            return "mixed"
        elif has_new_structure:
            return "new"
        elif has_legacy_structure:
            return "legacy"
        else:
            return "none"

    def migrate_to_new_structure(self, backup: bool = True) -> bool:
        """
        Migrate from legacy to new directory structure.

        Args:
            backup: If True, create backup before migration

        Returns:
            True if migration was successful, False otherwise
        """
        structure = self.detect_structure()
        if structure == "new":
            return True  # Already using new structure
        elif structure == "none":
            raise ValueError("No SpecPulse structure detected to migrate")

        # Implementation would go here for actual migration
        # This is a placeholder for the migration logic
        raise NotImplementedError("Migration functionality not yet implemented")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert path manager configuration to dictionary.

        Returns:
            Dictionary representation of path configuration
        """
        return {
            'project_root': str(self.project_root),
            'use_legacy_structure': self.use_legacy_structure,
            'structure_detected': self.detect_structure(),
            'directories': {name: str(path) for name, path in self.get_all_directories().items()}
        }