"""
Project Type Detection for SpecPulse.

Automatically detects project type from files and configuration.
"""
from pathlib import Path
from typing import Optional
import yaml

from ..core.custom_validation import ProjectType


class ProjectDetector:
    """
    Detects project type from configuration and file structure.

    Uses multiple detection strategies:
    1. Check .specpulse/project_context.yaml (from v1.7.0)
    2. Check common project files (package.json, pyproject.toml, etc.)
    3. Manual override support
    """

    # Class-level cache
    _cached_project_type: Optional[ProjectType] = None
    _cache_path: Optional[Path] = None

    @classmethod
    def detect_project_type(cls, project_root: Optional[Path] = None, use_cache: bool = True) -> ProjectType:
        """
        Detect project type from configuration or file structure.

        Args:
            project_root: Root directory of project (defaults to cwd)
            use_cache: Whether to use cached result (default: True)

        Returns:
            Detected ProjectType
        """
        if project_root is None:
            project_root = Path.cwd()

        # Check cache
        if use_cache and cls._cached_project_type and cls._cache_path == project_root:
            return cls._cached_project_type

        # Strategy 1: Check project_context.yaml (v1.7.0)
        project_type = cls._detect_from_context(project_root)
        if project_type != ProjectType.UNKNOWN:
            cls._cached_project_type = project_type
            cls._cache_path = project_root
            return project_type

        # Strategy 2: Check common project files
        project_type = cls._detect_from_files(project_root)

        # Cache result
        cls._cached_project_type = project_type
        cls._cache_path = project_root

        return project_type

    @classmethod
    def _detect_from_context(cls, project_root: Path) -> ProjectType:
        """Detect from project_context.yaml if it exists."""
        context_file = project_root / ".specpulse" / "project_context.yaml"

        if not context_file.exists():
            return ProjectType.UNKNOWN

        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                context_data = yaml.safe_load(f)

            # Check for project.type field
            project_data = context_data.get('project', {})
            type_str = project_data.get('type', '').lower()

            # Map common type strings to ProjectType
            type_map = {
                'web-app': ProjectType.WEB_APP,
                'web': ProjectType.WEB_APP,
                'webapp': ProjectType.WEB_APP,
                'api': ProjectType.API,
                'rest-api': ProjectType.API,
                'graphql': ProjectType.API,
                'microservice': ProjectType.API,
                'mobile-app': ProjectType.MOBILE_APP,
                'mobile': ProjectType.MOBILE_APP,
                'ios': ProjectType.MOBILE_APP,
                'android': ProjectType.MOBILE_APP,
                'desktop': ProjectType.DESKTOP,
                'desktop-app': ProjectType.DESKTOP,
                'cli': ProjectType.CLI,
                'command-line': ProjectType.CLI,
                'library': ProjectType.LIBRARY,
                'package': ProjectType.LIBRARY,
            }

            return type_map.get(type_str, ProjectType.UNKNOWN)

        except Exception:
            return ProjectType.UNKNOWN

    @classmethod
    def _detect_from_files(cls, project_root: Path) -> ProjectType:
        """Detect from common project files."""
        # Web App indicators
        if (project_root / "package.json").exists():
            # Check package.json content for more specific detection
            try:
                with open(project_root / "package.json", 'r') as f:
                    import json
                    pkg_data = json.load(f)

                    # Check for web frameworks
                    deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}

                    if any(fw in deps for fw in ['react', 'vue', 'angular', 'svelte', 'next']):
                        return ProjectType.WEB_APP

                    if any(fw in deps for fw in ['express', 'fastify', 'koa', 'nest']):
                        return ProjectType.API

            except Exception:
                pass

            # Default to web-app for package.json
            return ProjectType.WEB_APP

        # API indicators (Python)
        if (project_root / "pyproject.toml").exists() or (project_root / "requirements.txt").exists():
            # Check for API frameworks
            if (project_root / "requirements.txt").exists():
                try:
                    reqs = (project_root / "requirements.txt").read_text().lower()
                    if any(fw in reqs for fw in ['fastapi', 'flask', 'django', 'tornado']):
                        return ProjectType.API
                except Exception:
                    pass

            # Default to API for Python projects (common use case)
            return ProjectType.API

        # Mobile App indicators
        if (project_root / "android").exists() or (project_root / "ios").exists():
            return ProjectType.MOBILE_APP

        if (project_root / "pubspec.yaml").exists():  # Flutter
            return ProjectType.MOBILE_APP

        # Desktop App indicators
        if (project_root / "electron.js").exists() or (project_root / "main.js").exists():
            # Could be Electron app
            return ProjectType.DESKTOP

        # Go projects
        if (project_root / "go.mod").exists():
            # Could be API or CLI
            # Default to API for Go
            return ProjectType.API

        # Ruby projects
        if (project_root / "Gemfile").exists():
            try:
                gemfile = (project_root / "Gemfile").read_text().lower()
                if 'rails' in gemfile:
                    return ProjectType.WEB_APP
                if 'sinatra' in gemfile or 'grape' in gemfile:
                    return ProjectType.API
            except Exception:
                pass

        # Rust projects
        if (project_root / "Cargo.toml").exists():
            try:
                cargo = (project_root / "Cargo.toml").read_text()
                if '[lib]' in cargo:
                    return ProjectType.LIBRARY
            except Exception:
                pass
            # Default to CLI for Rust
            return ProjectType.CLI

        # Could not determine
        return ProjectType.UNKNOWN

    @classmethod
    def clear_cache(cls):
        """Clear the cached project type."""
        cls._cached_project_type = None
        cls._cache_path = None


# Convenience function
def detect_project_type(project_root: Optional[Path] = None) -> ProjectType:
    """
    Detect project type.

    Args:
        project_root: Root directory (defaults to cwd)

    Returns:
        Detected ProjectType
    """
    return ProjectDetector.detect_project_type(project_root)
