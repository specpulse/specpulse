"""
Incremental Builder for SpecPulse (v1.9.0)

Section-by-section spec building with progress tracking.
"""

from pathlib import Path
from typing import Optional, List, Dict
from dataclasses import dataclass
import re
from datetime import datetime

from specpulse.core.tier_constants import (
    SECTION_TIER_MAP,
    TIER_SECTIONS,
    SECTION_ORDER,
    SECTION_DISPLAY_NAMES,
    get_tier_number,
    get_section_tier,
    validate_section_name,
)


@dataclass
class ProgressInfo:
    """Information about spec progress."""

    tier: str
    total_sections: int
    completed_sections: int
    partial_sections: int
    not_started_sections: int
    percentage: float
    next_recommended: Optional[str]
    section_status: Dict[str, str]  # section_name -> status (complete/partial/empty)


@dataclass
class AddResult:
    """Result of adding a section."""

    success: bool
    section_added: str
    position: int
    message: str
    error: Optional[str] = None


class IncrementalBuilder:
    """
    Manages incremental spec building and progress tracking.

    Responsibilities:
    - Add individual sections to specs
    - Calculate completion percentage
    - Recommend next section to work on
    - Track progress in YAML frontmatter
    """

    def __init__(self, project_root: Path):
        """
        Initialize IncrementalBuilder.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.templates_dir = self.project_root / "templates"
        self.section_map = SECTION_TIER_MAP

    def add_section(self, spec_file: Path, section_name: str) -> AddResult:
        """
        Add individual section to spec.

        Args:
            spec_file: Path to specification file
            section_name: Name of section to add (e.g., "user_stories")

        Returns:
            AddResult with details of operation

        Raises:
            FileNotFoundError: If spec file doesn't exist
            ValueError: If section name is invalid
        """
        if not spec_file.exists():
            raise FileNotFoundError(f"Spec file not found: {spec_file}")

        if not validate_section_name(section_name):
            return AddResult(
                success=False,
                section_added=section_name,
                position=-1,
                message=f"Invalid section name: {section_name}",
                error=f"Section '{section_name}' not recognized",
            )

        # Read current spec
        current_content = spec_file.read_text(encoding="utf-8")

        # Get current tier
        current_tier = self._get_tier_from_content(current_content)
        current_tier_num = get_tier_number(current_tier)

        # Check if section's tier <= current tier
        section_tier = get_section_tier(section_name)
        if section_tier > current_tier_num:
            return AddResult(
                success=False,
                section_added=section_name,
                position=-1,
                message=f"Section '{section_name}' requires tier {section_tier}, but spec is tier {current_tier_num}",
                error=f"Suggest: specpulse expand to tier {section_tier} first",
            )

        # Check if section already exists
        sections = self._parse_sections(current_content)
        if section_name in sections:
            return AddResult(
                success=False,
                section_added=section_name,
                position=-1,
                message=f"Section '{section_name}' already exists",
                error="Section already present in spec",
            )

        # Load section template
        section_template = self._get_section_template(section_name, current_tier_num)

        # Find insertion point
        insertion_pos = self._find_insertion_point(current_content, section_name)

        # Insert section
        lines = current_content.split("\n")
        display_name = SECTION_DISPLAY_NAMES.get(section_name, section_name)

        # Build section content
        section_content = f"\n## {display_name}\n\n{section_template}\n"

        # Insert
        lines.insert(insertion_pos, section_content)
        new_content = "\n".join(lines)

        # Update progress in frontmatter
        new_content = self._update_progress(new_content, section_name, "added")

        # Write updated spec
        spec_file.write_text(new_content, encoding="utf-8")

        return AddResult(
            success=True,
            section_added=section_name,
            position=insertion_pos,
            message=f"Added section: {display_name}",
        )

    def get_progress(self, spec_file: Path) -> ProgressInfo:
        """
        Calculate completion percentage and section status.

        Args:
            spec_file: Path to specification file

        Returns:
            ProgressInfo with detailed progress metrics

        Raises:
            FileNotFoundError: If spec file doesn't exist
        """
        if not spec_file.exists():
            raise FileNotFoundError(f"Spec file not found: {spec_file}")

        content = spec_file.read_text(encoding="utf-8")

        # Get tier
        tier = self._get_tier_from_content(content)
        tier_num = get_tier_number(tier)

        # Get expected sections
        expected_sections = TIER_SECTIONS[tier_num]

        # Parse current sections
        current_sections = self._parse_sections(content)

        # Analyze each section
        section_status = {}
        completed = 0
        partial = 0
        not_started = 0

        for section in expected_sections:
            if section in current_sections:
                status = self._analyze_section_content(current_sections[section])
                section_status[section] = status

                if status == "complete":
                    completed += 1
                elif status == "partial":
                    partial += 1
                else:
                    not_started += 1
            else:
                section_status[section] = "empty"
                not_started += 1

        # Calculate percentage
        total = len(expected_sections)
        percentage = completed / total if total > 0 else 0.0

        # Calculate next recommended section (without recursion)
        next_section = self._calculate_next_section(
            tier, tier_num, percentage, expected_sections, section_status
        )

        return ProgressInfo(
            tier=tier,
            total_sections=total,
            completed_sections=completed,
            partial_sections=partial,
            not_started_sections=not_started,
            percentage=percentage,
            next_recommended=next_section,
            section_status=section_status,
        )

    def get_next_section(self, spec_file: Path) -> Optional[str]:
        """
        Recommend next section to work on.

        Args:
            spec_file: Path to specification file

        Returns:
            Section name to work on next, or None if all complete

        Raises:
            FileNotFoundError: If spec file doesn't exist
        """
        progress = self.get_progress(spec_file)

        # Check if tier is complete
        if progress.percentage == 1.0:
            tier_num = get_tier_number(progress.tier)
            if tier_num == 1:
                return "RECOMMEND: Expand to standard tier"
            elif tier_num == 2:
                return "RECOMMEND: Expand to complete OR ready for planning"
            else:
                return "RECOMMEND: Ready for planning (/sp-plan)"

        # Find first incomplete section
        expected_sections = TIER_SECTIONS[get_tier_number(progress.tier)]

        for section in expected_sections:
            status = progress.section_status.get(section, "empty")
            if status != "complete":
                return section

        return None

    def get_section_template(self, section_name: str) -> str:
        """
        Load section template with LLM guidance.

        Args:
            section_name: Section name

        Returns:
            Section template content

        Raises:
            ValueError: If section name is invalid
        """
        if not validate_section_name(section_name):
            raise ValueError(f"Invalid section name: {section_name}")

        section_tier = get_section_tier(section_name)
        return self._get_section_template(section_name, section_tier)

    # Private helper methods

    def _calculate_next_section(
        self,
        tier: str,
        tier_num: int,
        percentage: float,
        expected_sections: List[str],
        section_status: Dict[str, str],
    ) -> Optional[str]:
        """Calculate next recommended section without recursion."""
        # Check if tier is complete
        if percentage == 1.0:
            if tier_num == 1:
                return "RECOMMEND: Expand to standard tier"
            elif tier_num == 2:
                return "RECOMMEND: Expand to complete OR ready for planning"
            else:
                return "RECOMMEND: Ready for planning (/sp-plan)"

        # Find first incomplete section
        for section in expected_sections:
            status = section_status.get(section, "empty")
            if status != "complete":
                return section

        return None

    def _get_tier_from_content(self, content: str) -> str:
        """Extract tier from YAML frontmatter."""
        lines = content.split("\n")
        in_frontmatter = False

        for line in lines:
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            if in_frontmatter and line.startswith("tier:"):
                # BUG-007 FIX: Add explicit bounds check for defensive programming
                parts = line.split(":", 1)
                if len(parts) >= 2:
                    tier = parts[1].strip()
                    return tier

        # Default to complete if no tier found
        return "complete"

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse spec into sections."""
        sections = {}

        # Skip frontmatter
        parts = content.split("---")
        if len(parts) >= 3:
            content_after_frontmatter = "---".join(parts[2:])
        else:
            content_after_frontmatter = content

        # Split by ## headers
        section_pattern = r"\n## ([^\n]+)\n"
        matches = list(re.finditer(section_pattern, content_after_frontmatter))

        for i, match in enumerate(matches):
            section_title = match.group(1).strip()
            section_name = self._normalize_section_name(section_title)

            # Get content until next section
            start_pos = match.end()
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(content_after_frontmatter)

            section_content = content_after_frontmatter[start_pos:end_pos].strip()
            sections[section_name] = section_content

        return sections

    def _normalize_section_name(self, title: str) -> str:
        """Normalize section title to section name."""
        normalized = title.lower()
        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = re.sub(r"\s+", "_", normalized)
        return normalized.strip("_")

    def _analyze_section_content(self, content: str) -> str:
        """
        Analyze section content to determine status.

        Returns:
            'complete', 'partial', or 'empty'
        """
        content = content.strip()

        # Empty check
        if len(content) == 0:
            return "empty"

        # Remove LLM guidance comments for analysis
        content_no_comments = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        content_no_comments = content_no_comments.strip()

        if len(content_no_comments) == 0:
            return "empty"

        # Template placeholder check
        placeholders = [
            "[placeholder]",
            "[description]",
            "[todo",
            "[one sentence",
            "[requirement",
            "fill this in",
        ]

        content_lower = content_no_comments.lower()
        if any(ph in content_lower for ph in placeholders):
            return "partial" if len(content_no_comments) > 50 else "empty"

        # Length heuristic
        if len(content_no_comments) < 50:
            return "partial"

        # Has substantial content
        return "complete"

    def _find_insertion_point(self, content: str, section_name: str) -> int:
        """Find correct line position to insert section."""
        lines = content.split("\n")

        # Get section order
        section_index = SECTION_ORDER.index(section_name)

        # Find last existing section before target
        for i in range(section_index - 1, -1, -1):
            prior_section = SECTION_ORDER[i]
            display_name = SECTION_DISPLAY_NAMES.get(prior_section, prior_section)

            # Find this section in content
            for line_num, line in enumerate(lines):
                if line.startswith(f"## {display_name}"):
                    # Found prior section, insert after it
                    # Find next ## or end
                    for j in range(line_num + 1, len(lines)):
                        if lines[j].startswith("##") or lines[j].startswith("---"):
                            return j
                    return len(lines)

        # No prior sections found, insert after frontmatter
        in_frontmatter = False
        for line_num, line in enumerate(lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    # End of frontmatter
                    return line_num + 1

        # Fallback: beginning of file
        return 0

    def _get_section_template(self, section_name: str, tier_num: int) -> str:
        """Load section template from tier file."""
        # Try templates dir first (user's project)
        tier_template_path = self.templates_dir / f"spec-tier{tier_num}.md"

        if not tier_template_path.exists():
            # Try resources (installed package)
            import specpulse
            package_root = Path(specpulse.__file__).parent
            tier_template_path = package_root / "resources" / "templates" / f"spec-tier{tier_num}.md"

        if not tier_template_path.exists():
            # Fallback: return basic template
            display_name = SECTION_DISPLAY_NAMES.get(section_name, section_name)
            return f"<!-- LLM GUIDANCE: Fill in {display_name} -->\n\n[Content for {display_name}]"

        template_content = tier_template_path.read_text(encoding="utf-8")

        # Extract just this section from template
        display_name = SECTION_DISPLAY_NAMES.get(section_name, section_name)
        pattern = f"## {display_name}.*?(?=\n## |\n---|\\Z)"
        match = re.search(pattern, template_content, re.DOTALL)

        if match:
            section_text = match.group(0)
            # Remove the ## header (will be added by add_section)
            section_text = re.sub(f"^## {display_name}\n+", "", section_text)
            return section_text.strip()

        return f"[Content for {display_name}]"

    def _update_progress(
        self, content: str, section_name: str, action: str
    ) -> str:
        """Update progress metadata in YAML frontmatter."""
        lines = content.split("\n")
        in_frontmatter = False
        frontmatter_end = -1

        for i, line in enumerate(lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    frontmatter_end = i
                    break

        if frontmatter_end == -1:
            # No frontmatter, add it
            return content

        # Update last_updated
        current_date = datetime.now().strftime("%Y-%m-%d")
        for i in range(frontmatter_end):
            if lines[i].startswith("last_updated:"):
                lines[i] = f"last_updated: {current_date}"
                break

        return "\n".join(lines)
