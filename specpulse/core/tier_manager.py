"""Multi-tier template system for progressive specification building."""

from pathlib import Path
from typing import Dict, Literal, Optional
import re
import shutil
from datetime import datetime

from ..utils.console import Console

TierLevel = Literal["minimal", "standard", "complete"]

TIER_ORDER = {"minimal": 1, "standard": 2, "complete": 3}

# Section counts for tier detection
TIER_SECTIONS = {
    "minimal": 3,  # What, Why, Done When
    "standard": 7,  # + Executive Summary, User Stories, Functional Req, Technical Approach
    "complete": 15,  # + NFRs, Edge Cases, Security, Performance, Testing, Deployment
}


class TierManager:
    """Manages multi-tier template system for progressive spec building."""

    def __init__(self, project_root: Path):
        """Initialize tier manager.

        Args:
            project_root: Root directory of SpecPulse project
        """
        self.project_root = Path(project_root)
        self.specs_dir = self.project_root / "specs"
        self.templates_dir = self.project_root / "templates"
        self.resources_templates = Path(__file__).parent.parent / "resources" / "templates"
        self.console = Console()

    def get_current_tier(self, feature_id: str) -> TierLevel:
        """Detect current tier of a specification.

        Args:
            feature_id: Feature identifier (e.g., "001" or "001-feature-name")

        Returns:
            Current tier level

        Raises:
            FileNotFoundError: If spec file doesn't exist
        """
        spec_path = self._find_spec_file(feature_id)
        if not spec_path.exists():
            raise FileNotFoundError(f"Spec not found for feature: {feature_id}")

        content = spec_path.read_text(encoding="utf-8")

        # Try to extract tier marker first
        tier = self._extract_tier_marker(content)
        if tier:
            return tier

        # Fall back to section counting
        return self._detect_by_sections(content)

    def expand_tier(
        self,
        feature_id: str,
        to_tier: TierLevel,
        preserve_content: bool = True,
        backup: bool = True,
        show_diff: bool = False,
    ) -> bool:
        """Expand specification to higher tier.

        Args:
            feature_id: Feature identifier
            to_tier: Target tier level
            preserve_content: Keep user-written content (default: True)
            backup: Create backup before expansion (default: True)
            show_diff: Show preview of changes (default: False)

        Returns:
            True if successful, False otherwise

        Raises:
            ValueError: If tier transition is invalid
        """
        spec_path = self._find_spec_file(feature_id)
        if not spec_path.exists():
            raise FileNotFoundError(f"Spec not found for feature: {feature_id}")

        current_tier = self.get_current_tier(feature_id)

        # Already at target tier
        if current_tier == to_tier:
            self.console.warning(f"Spec already at {to_tier} tier")
            return False

        # Validate transition
        if not self._valid_transition(current_tier, to_tier):
            raise ValueError(
                f"Invalid tier transition: {current_tier} → {to_tier}. "
                f"Can only expand to higher tiers."
            )

        # Load current content and target template
        current_content = spec_path.read_text(encoding="utf-8")
        target_template = self._load_template(to_tier)

        # Merge templates
        merged_content = self._merge_templates(current_content, target_template)

        # Show diff if requested
        if show_diff:
            self._show_diff(current_content, merged_content)
            response = input("\nProceed with expansion? [y/N]: ")
            if response.lower() != "y":
                return False

        # Create backup
        if backup:
            backup_path = self._create_backup(spec_path)
            self.console.info(f"Backup created: {backup_path}")

        # Write expanded content
        spec_path.write_text(merged_content, encoding="utf-8")

        self.console.success(f"Expanded spec to {to_tier} tier")
        return True

    def validate_tier(self, spec_path: Path) -> Dict:
        """Validate spec against tier requirements.

        Args:
            spec_path: Path to specification file

        Returns:
            Validation result with errors, warnings, tier info
        """
        if not spec_path.exists():
            return {
                "valid": False,
                "tier": None,
                "errors": [f"Spec file not found: {spec_path}"],
                "warnings": [],
            }

        content = spec_path.read_text(encoding="utf-8")
        tier = self.get_current_tier(spec_path.parent.name)

        errors = []
        warnings = []

        # Check for tier marker
        if not self._extract_tier_marker(content):
            warnings.append("No tier marker found (<!-- TIER: ... -->)")

        # Check required sections for tier
        missing_sections = self._check_required_sections(content, tier)
        if missing_sections:
            errors.extend([f"Missing section: {s}" for s in missing_sections])

        # Check for placeholder content
        if "{{ " in content and " }}" in content:
            warnings.append("Contains unfilled template placeholders")

        return {
            "valid": len(errors) == 0,
            "tier": tier,
            "errors": errors,
            "warnings": warnings,
        }

    def _merge_templates(self, current_content: str, target_template: str) -> str:
        """Merge current spec content with target template.

        Preserves user content from existing sections,
        adds new sections from template.

        Args:
            current_content: Current spec file content
            target_template: Target tier template content

        Returns:
            Merged content
        """
        # Extract sections from current content
        current_sections = self._extract_sections(current_content)

        # Parse target template
        result_lines = []
        current_section = None
        in_section_content = False

        for line in target_template.split("\n"):
            # Check if this is a section header (## Something)
            section_match = re.match(r"^##\s+(.+)$", line)

            if section_match:
                section_name = section_match.group(1).strip()
                current_section = section_name
                result_lines.append(line)
                in_section_content = True
                continue

            # If we're in a section and have user content for it, use user content
            if in_section_content and current_section:
                if current_section in current_sections:
                    # Use preserved content for this section
                    user_content = current_sections[current_section]
                    result_lines.append(user_content)
                    current_section = None
                    in_section_content = False
                    continue

            # Check if we hit the next section (stop adding template content)
            if line.startswith("#") and current_section:
                in_section_content = False
                current_section = None

            result_lines.append(line)

        return "\n".join(result_lines)

    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract section content from markdown.

        Returns:
            Dict mapping section names to their content
        """
        sections = {}
        current_section = None
        section_lines = []

        for line in content.split("\n"):
            # Section header (## Something)
            section_match = re.match(r"^##\s+(.+)$", line)

            if section_match:
                # Save previous section
                if current_section and section_lines:
                    sections[current_section] = "\n".join(section_lines).strip()

                # Start new section
                current_section = section_match.group(1).strip()
                section_lines = []
                continue

            # Stop at main header or frontmatter
            if line.startswith("# ") or line.startswith("---"):
                if current_section and section_lines:
                    sections[current_section] = "\n".join(section_lines).strip()
                current_section = None
                section_lines = []
                continue

            # Accumulate section content
            if current_section:
                # Skip LLM guidance comments and expand markers
                if not line.strip().startswith("<!-- LLM GUIDANCE"):
                    if not line.strip().startswith("<!-- EXPAND_NEXT"):
                        if line.strip() != "💡 Ready for more detail?":
                            section_lines.append(line)

        # Save last section
        if current_section and section_lines:
            sections[current_section] = "\n".join(section_lines).strip()

        return sections

    def _extract_tier_marker(self, content: str) -> Optional[TierLevel]:
        """Extract tier marker from spec content."""
        match = re.search(r"<!--\s*TIER:\s*(\w+)\s*-->", content)
        if match:
            tier = match.group(1).lower()
            if tier in ["minimal", "standard", "complete"]:
                return tier  # type: ignore
        return None

    def _detect_by_sections(self, content: str) -> TierLevel:
        """Detect tier by counting sections."""
        # Count ## headers (excluding # main title)
        section_count = len(re.findall(r"^##\s+", content, re.MULTILINE))

        if section_count <= 4:
            return "minimal"
        elif section_count <= 10:
            return "standard"
        else:
            return "complete"

    def _valid_transition(self, from_tier: TierLevel, to_tier: TierLevel) -> bool:
        """Check if tier transition is valid.

        Valid: minimal->standard, standard->complete, minimal->complete
        Invalid: Any reverse direction
        """
        return TIER_ORDER[to_tier] > TIER_ORDER[from_tier]

    def _create_backup(self, spec_path: Path) -> Path:
        """Create backup of spec before expansion."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{spec_path.stem}.backup-{timestamp}{spec_path.suffix}"
        backup_path = spec_path.parent / backup_name
        shutil.copy2(spec_path, backup_path)
        return backup_path

    def _find_spec_file(self, feature_id: str) -> Path:
        """Find the spec file for a feature."""
        # Try to find feature directory
        feature_dirs = list(self.specs_dir.glob(f"*{feature_id}*"))

        if not feature_dirs:
            # Try exact match
            feature_dir = self.specs_dir / feature_id
        else:
            feature_dir = feature_dirs[0]

        # Find latest spec file
        spec_files = sorted(feature_dir.glob("spec-*.md"))
        if not spec_files:
            raise FileNotFoundError(f"No spec files found in {feature_dir}")

        return spec_files[-1]  # Return latest spec

    def _load_template(self, tier: TierLevel) -> str:
        """Load template for given tier."""
        tier_num = TIER_ORDER[tier]
        template_name = f"spec-tier{tier_num}-{tier}.md"

        # Try project templates first
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            # Fall back to resources templates
            template_path = self.resources_templates / template_name

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        return template_path.read_text(encoding="utf-8")

    def _show_diff(self, old_content: str, new_content: str) -> None:
        """Show diff between old and new content."""
        old_sections = set(self._extract_sections(old_content).keys())
        new_sections = set(self._extract_sections(new_content).keys())

        added_sections = new_sections - old_sections

        self.console.info("\nChanges preview:")
        self.console.success(f"Sections to add: {len(added_sections)}")
        for section in sorted(added_sections):
            self.console.info(f" + {section}")

    def _check_required_sections(self, content: str, tier: TierLevel) -> list:
        """Check for required sections based on tier."""
        sections = self._extract_sections(content)
        section_names = set(sections.keys())

        required = {
            "minimal": {"What", "Why", "Done When"},
            "standard": {
                "What",
                "Why",
                "Executive Summary",
                "User Stories",
                "Functional Requirements",
                "Technical Approach",
                "Acceptance Criteria",
            },
            "complete": {
                "What",
                "Why",
                "Executive Summary",
                "User Stories",
                "Functional Requirements",
                "Non-Functional Requirements",
                "Technical Approach",
                "Edge Cases",
                "Security Considerations",
                "Performance Requirements",
                "Testing Strategy",
                "Deployment Considerations",
                "Acceptance Criteria",
            },
        }

        missing = required[tier] - section_names
        return sorted(missing)
