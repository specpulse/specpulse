"""
Spec management commands for SpecPulse CLI v2.1.0
"""

from pathlib import Path
from datetime import datetime
import re
from typing import Optional


class SpecCommands:
    """Specification lifecycle management"""

    def __init__(self, console, project_root: Path):
        self.console = console
        self.project_root = project_root
        # Import PathManager for centralized path management
        from ...core.path_manager import PathManager
        self.path_manager = PathManager(project_root)

        self.specs_dir = self.path_manager.specs_dir
        self.templates_dir = self.path_manager.templates_dir
        self.memory_dir = self.path_manager.memory_dir

    def spec_create(self, description: str, feature_id: Optional[str] = None, **kwargs) -> bool:
        """
        Create a new specification.

        Args:
            description: Spec description (used by AI to generate content)
            feature_id: Feature ID or auto-detect from context

        Returns:
            bool: Success status
        """
        try:
            # Detect feature if not provided
            if not feature_id:
                feature_id = self._detect_current_feature()
                if not feature_id:
                    self.console.error("No active feature. Run: specpulse feature init <name>")
                    return False

            # Find feature directory
            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                self.console.error(f"Feature not found: {feature_id}")
                return False

            spec_dir = self.specs_dir / feature_dir.name

            # Find next spec number
            spec_number = self._get_next_spec_number(spec_dir)
            spec_file = spec_dir / f"spec-{spec_number:03d}.md"

            # Load template
            template_file = self.templates_dir / "spec.md"
            if not template_file.exists():
                self.console.error(f"Template not found: {template_file}")
                return False

            template_content = template_file.read_text(encoding='utf-8')

            # Create spec with template + description placeholder
            spec_content = f"""# Specification: {description}

<!-- FEATURE_DIR: {feature_dir.name} -->
<!-- FEATURE_ID: {feature_id} -->
<!-- SPEC_NUMBER: {spec_number:03d} -->
<!-- CREATED: {datetime.now().isoformat()} -->

## Description
{description}

## [LLM: Expand this specification using the template below]

---

{template_content}
"""

            spec_file.write_text(spec_content, encoding='utf-8')

            self.console.success(f"Spec created: {spec_file.relative_to(self.project_root)}")
            self.console.info(f"  Feature: {feature_dir.name}")
            self.console.info(f"  Description: {description}")
            self.console.info("\nNext: LLM will expand this spec using the template")

            return True

        except Exception as e:
            self.console.error(f"Spec creation failed: {e}")
            return False

    def spec_update(self, spec_id: str, description: str, feature_id: Optional[str] = None, **kwargs) -> bool:
        """
        Update existing specification (add metadata for LLM).

        Args:
            spec_id: Spec number (e.g., "001")
            description: Update description
            feature_id: Feature ID or auto-detect

        Returns:
            bool: Success status
        """
        try:
            # Detect feature if not provided
            if not feature_id:
                feature_id = self._detect_current_feature()
                if not feature_id:
                    self.console.error("No active feature")
                    return False

            # Find feature and spec
            feature_dir = self._find_feature_dir(feature_id)
            if not feature_dir:
                self.console.error(f"Feature not found: {feature_id}")
                return False

            spec_dir = self.specs_dir / feature_dir.name
            spec_file = spec_dir / f"spec-{spec_id}.md"

            if not spec_file.exists():
                self.console.error(f"Spec not found: {spec_file}")
                return False

            # Append update marker for LLM
            content = spec_file.read_text(encoding='utf-8')
            update_marker = f"""

---
## [UPDATE REQUEST - {datetime.now().isoformat()}]
{description}

[LLM: Apply this update to the specification above]
---
"""
            content += update_marker
            spec_file.write_text(content, encoding='utf-8')

            self.console.success(f"Update marker added: {spec_file.relative_to(self.project_root)}")
            self.console.info(f"  Request: {description}")
            self.console.info("\nNext: LLM will process the update request")

            return True

        except Exception as e:
            self.console.error(f"Spec update failed: {e}")
            return False

    def spec_validate(self, spec_id: Optional[str] = None, feature_id: Optional[str] = None, **kwargs) -> bool:
        """
        Validate specification (calls existing validator).

        Args:
            spec_id: Spec number or validate all
            feature_id: Feature ID or auto-detect

        Returns:
            bool: Success status
        """
        try:
            # This delegates to existing validate command
            from ..core.validator import Validator

            validator = Validator()

            if not feature_id:
                feature_id = self._detect_current_feature()

            if feature_id:
                feature_dir = self._find_feature_dir(feature_id)
                if feature_dir:
                    spec_dir = self.specs_dir / feature_dir.name

                    if spec_id:
                        # Validate specific spec
                        spec_file = spec_dir / f"spec-{spec_id}.md"
                        if spec_file.exists():
                            result = validator.validate_spec(spec_file)
                            self._display_validation_result(result, spec_file)
                            return result.is_valid
                    else:
                        # Validate all specs in feature
                        specs = list(spec_dir.glob("spec-*.md"))
                        if not specs:
                            self.console.warning("No specs found")
                            return False

                        all_valid = True
                        for spec_file in specs:
                            result = validator.validate_spec(spec_file)
                            self._display_validation_result(result, spec_file)
                            all_valid = all_valid and result.is_valid

                        return all_valid

            self.console.error("Could not determine which spec to validate")
            return False

        except Exception as e:
            self.console.error(f"Validation failed: {e}")
            return False

    def _get_next_spec_number(self, spec_dir: Path) -> int:
        """Get next available spec number"""
        if not spec_dir.exists():
            return 1

        specs = list(spec_dir.glob("spec-*.md"))
        if not specs:
            return 1

        max_num = 0
        for spec_file in specs:
            match = re.search(r'spec-(\d{3})\.md', spec_file.name)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)

        return max_num + 1

    def _detect_current_feature(self) -> Optional[str]:
        """Detect current feature from context"""
        context_file = self.memory_dir / "context.md"
        if not context_file.exists():
            return None

        content = context_file.read_text(encoding='utf-8')

        # Look for last active feature in workflow history
        matches = re.findall(r'### Active Feature:.*?\n- Feature ID: (\d{3})', content)
        if matches:
            return matches[-1]

        return None

    def _find_feature_dir(self, feature_id: str) -> Optional[Path]:
        """Find feature directory by ID"""
        if not self.specs_dir.exists():
            return None

        pattern = f"{feature_id}*" if len(feature_id) == 3 else f"*{feature_id}*"
        matches = list(self.specs_dir.glob(pattern))

        return matches[0] if matches else None

    def _display_validation_result(self, result, spec_file: Path):
        """Display validation result"""
        if result.is_valid:
            self.console.success(f"✓ {spec_file.name}: Valid")
        else:
            self.console.error(f"✗ {spec_file.name}: {len(result.errors)} errors")
            for error in result.errors:
                self.console.warning(f"  - {error}")
