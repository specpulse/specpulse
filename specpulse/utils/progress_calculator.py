"""
Progress Calculator for Specification Validation.

Calculates completion percentage and section status for progressive validation.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import re


class SectionStatus(Enum):
    """Status of a specification section."""
    COMPLETE = "complete"  # ✓
    PARTIAL = "partial"    # ⚠️
    MISSING = "missing"    # ⭕


@dataclass
class ProgressResult:
    """Result of progress calculation."""
    completion_percentage: int
    section_statuses: Dict[str, SectionStatus]
    total_weight: float
    completed_weight: float


# Section weights configuration (must sum to ~100%)
SECTION_WEIGHTS = {
    "Executive Summary": 5,
    "Problem Statement": 10,
    "Proposed Solution": 10,
    "Functional Requirements": 15,
    "Non-Functional Requirements": 10,
    "User Stories": 15,
    "Acceptance Criteria": 10,
    "Technical Constraints": 5,
    "Dependencies": 5,
    "Risks and Mitigations": 5,
    "Success Criteria": 10,
}

# Thresholds for section status determination
SECTION_THRESHOLDS = {
    "Executive Summary": {"min_chars": 100, "min_lines": 2},
    "Problem Statement": {"min_chars": 200, "min_lines": 3},
    "Proposed Solution": {"min_chars": 150, "min_lines": 2},
    "Functional Requirements": {"min_items": 3, "min_chars": 150},
    "Non-Functional Requirements": {"min_subsections": 1, "min_chars": 100},
    "User Stories": {"min_stories": 2, "min_chars": 200},
    "Acceptance Criteria": {"min_items": 3, "min_chars": 100},
    "Technical Constraints": {"min_items": 2, "min_chars": 50},
    "Dependencies": {"min_items": 1, "min_chars": 50},
    "Risks and Mitigations": {"min_risks": 2, "min_chars": 150},
    "Success Criteria": {"min_items": 3, "min_chars": 100},
}


class ProgressCalculator:
    """Calculate specification completion progress."""

    def __init__(self):
        self.section_weights = SECTION_WEIGHTS
        self.thresholds = SECTION_THRESHOLDS

    def calculate_completion_percentage(self, spec_content: str) -> ProgressResult:
        """
        Calculate overall completion percentage for a specification.

        Args:
            spec_content: Full content of the specification

        Returns:
            ProgressResult with completion percentage and section statuses
        """
        sections = self._extract_sections(spec_content)
        section_statuses = {}
        completed_weight = 0.0
        total_weight = 0.0

        for section_name, weight in self.section_weights.items():
            total_weight += weight
            section_content = sections.get(section_name, "")
            status = self.calculate_section_status(section_name, section_content)
            section_statuses[section_name] = status

            if status == SectionStatus.COMPLETE:
                completed_weight += weight
            elif status == SectionStatus.PARTIAL:
                # Partial sections contribute 50% of their weight
                completed_weight += weight * 0.5

        completion_pct = int((completed_weight / total_weight) * 100) if total_weight > 0 else 0

        return ProgressResult(
            completion_percentage=completion_pct,
            section_statuses=section_statuses,
            total_weight=total_weight,
            completed_weight=completed_weight
        )

    def calculate_section_status(self, section_name: str, section_content: str) -> SectionStatus:
        """
        Determine the status of a single section.

        Args:
            section_name: Name of the section
            section_content: Content of the section

        Returns:
            SectionStatus (COMPLETE, PARTIAL, or MISSING)
        """
        if not section_content or len(section_content.strip()) == 0:
            return SectionStatus.MISSING

        threshold = self.thresholds.get(section_name, {})

        # Check character count
        min_chars = threshold.get("min_chars", 0)
        if min_chars > 0 and len(section_content.strip()) < min_chars:
            return SectionStatus.PARTIAL

        # Check line count
        min_lines = threshold.get("min_lines", 0)
        if min_lines > 0:
            lines = [line for line in section_content.split("\n") if line.strip()]
            if len(lines) < min_lines:
                return SectionStatus.PARTIAL

        # Check item count (lines starting with -, *, or numbered)
        min_items = threshold.get("min_items", 0)
        if min_items > 0:
            items = self._count_list_items(section_content)
            if items == 0:
                return SectionStatus.PARTIAL
            elif items < min_items:
                return SectionStatus.PARTIAL

        # Check story count (for User Stories)
        min_stories = threshold.get("min_stories", 0)
        if min_stories > 0:
            stories = self._count_user_stories(section_content)
            if stories == 0:
                return SectionStatus.PARTIAL
            elif stories < min_stories:
                return SectionStatus.PARTIAL

        # Check risk count (for Risks)
        min_risks = threshold.get("min_risks", 0)
        if min_risks > 0:
            risks = self._count_risks(section_content)
            if risks == 0:
                return SectionStatus.PARTIAL
            elif risks < min_risks:
                return SectionStatus.PARTIAL

        # Check subsection count (for Non-Functional Requirements)
        min_subsections = threshold.get("min_subsections", 0)
        if min_subsections > 0:
            subsections = self._count_subsections(section_content)
            if subsections == 0:
                return SectionStatus.PARTIAL
            elif subsections < min_subsections:
                return SectionStatus.PARTIAL

        return SectionStatus.COMPLETE

    def _extract_sections(self, spec_content: str) -> Dict[str, str]:
        """
        Extract all sections from spec content.

        Args:
            spec_content: Full specification content

        Returns:
            Dictionary mapping section names to their content
        """
        sections = {}
        current_section = None
        current_content = []

        for line in spec_content.split("\n"):
            stripped_line = line.strip()
            # Check if this is a level-2 heading (## Section Name)
            if stripped_line.startswith("## "):
                # Save previous section if exists
                if current_section:
                    sections[current_section] = "\n".join(current_content)

                # Start new section
                current_section = stripped_line.replace("## ", "").strip()
                current_content = []
            elif current_section:
                # Add line to current section
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content)

        return sections

    def _count_list_items(self, content: str) -> int:
        """Count list items (lines starting with -, *, or numbers)."""
        count = 0
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith(("-", "*")) or re.match(r"^\d+\.", stripped):
                count += 1
        return count

    def _count_user_stories(self, content: str) -> int:
        """Count user stories (sections with 'As a' pattern)."""
        return content.count("**As a**")

    def _count_risks(self, content: str) -> int:
        """Count risks (sections with 'Risk' pattern)."""
        return len(re.findall(r"\*\*Risk \d+:", content))

    def _count_subsections(self, content: str) -> int:
        """Count subsections (### or ####)."""
        count = 0
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("###"):
                count += 1
        return count

    def suggest_next_section(self, current_sections: Dict[str, SectionStatus]) -> Optional[str]:
        """
        Suggest which section to work on next.

        Args:
            current_sections: Current section statuses

        Returns:
            Name of suggested next section, or None if spec is complete
        """
        # Recommended section order
        recommended_order = [
            "Executive Summary",
            "Problem Statement",
            "Proposed Solution",
            "Functional Requirements",
            "User Stories",
            "Acceptance Criteria",
            "Non-Functional Requirements",
            "Technical Constraints",
            "Dependencies",
            "Risks and Mitigations",
            "Success Criteria",
        ]

        # Find first incomplete section in recommended order
        for section in recommended_order:
            status = current_sections.get(section, SectionStatus.MISSING)
            if status != SectionStatus.COMPLETE:
                return section

        return None  # All sections complete


# Convenience function
def calculate_progress(spec_content: str) -> ProgressResult:
    """
    Calculate specification progress.

    Args:
        spec_content: Full specification content

    Returns:
        ProgressResult with completion percentage and section statuses
    """
    calculator = ProgressCalculator()
    return calculator.calculate_completion_percentage(spec_content)
