"""
Tier Constants for SpecPulse Tiered Templates (v1.9.0)

This module defines the mapping between specification sections and their corresponding tiers.
Used by TierManager and IncrementalBuilder to validate tier requirements and determine
section ordering during tier expansion and incremental building.

Tiers:
    1 (minimal): Quick-start specs (3 sections, 2-3 minutes to complete)
    2 (standard): Implementation-ready specs (7-8 sections, 10-15 minutes)
    3 (complete): Production-grade specs (15+ sections, 30-45 minutes)
"""

from typing import Dict, List, Set

# Section names to tier number mapping
# Lower tier number = appears in earlier/simpler tiers
SECTION_TIER_MAP: Dict[str, int] = {
    # Tier 1: Minimal (Quick Start)
    "what": 1,
    "why": 1,
    "done_when": 1,
    # Tier 2: Standard (Implementation Ready)
    "user_stories": 2,
    "functional_requirements": 2,
    "technical_approach": 2,
    "api_design": 2,
    "dependencies": 2,
    "risks_and_mitigations": 2,
    # Tier 3: Complete (Production Grade)
    "security_considerations": 3,
    "performance_requirements": 3,
    "monitoring_and_alerts": 3,
    "rollback_strategy": 3,
    "operational_runbook": 3,
    "compliance_requirements": 3,
    "cost_analysis": 3,
    "migration_strategy": 3,
}

# Tier to sections mapping (for quick lookups)
# Each tier includes ALL sections from previous tiers
TIER_SECTIONS: Dict[int, List[str]] = {
    1: [  # Minimal tier
        "what",
        "why",
        "done_when",
    ],
    2: [  # Standard tier (includes tier 1 + new sections)
        "what",
        "why",
        "done_when",
        "user_stories",
        "functional_requirements",
        "technical_approach",
        "api_design",
        "dependencies",
        "risks_and_mitigations",
    ],
    3: [  # Complete tier (includes tier 2 + new sections)
        "what",
        "why",
        "done_when",
        "user_stories",
        "functional_requirements",
        "technical_approach",
        "api_design",
        "dependencies",
        "risks_and_mitigations",
        "security_considerations",
        "performance_requirements",
        "monitoring_and_alerts",
        "rollback_strategy",
        "operational_runbook",
        "compliance_requirements",
        "cost_analysis",
        "migration_strategy",
    ],
}

# Tier names for display
TIER_NAMES: Dict[int, str] = {
    1: "minimal",
    2: "standard",
    3: "complete",
}

# Reverse mapping: tier name to number
TIER_NAME_TO_NUMBER: Dict[str, int] = {
    "minimal": 1,
    "standard": 2,
    "complete": 3,
}

# Section display names (for user-facing output)
SECTION_DISPLAY_NAMES: Dict[str, str] = {
    "what": "What",
    "why": "Why",
    "done_when": "Done When",
    "user_stories": "User Stories",
    "functional_requirements": "Functional Requirements",
    "technical_approach": "Technical Approach",
    "api_design": "API Design",
    "dependencies": "Dependencies",
    "risks_and_mitigations": "Risks and Mitigations",
    "security_considerations": "Security Considerations",
    "performance_requirements": "Performance Requirements",
    "monitoring_and_alerts": "Monitoring & Alerts",
    "rollback_strategy": "Rollback Strategy",
    "operational_runbook": "Operational Runbook",
    "compliance_requirements": "Compliance Requirements",
    "cost_analysis": "Cost Analysis",
    "migration_strategy": "Migration Strategy",
}

# Section order (defines insertion order when adding sections incrementally)
# This is the canonical order sections should appear in specifications
SECTION_ORDER: List[str] = [
    # Tier 1
    "what",
    "why",
    "done_when",
    # Tier 2
    "user_stories",
    "functional_requirements",
    "technical_approach",
    "api_design",
    "dependencies",
    "risks_and_mitigations",
    # Tier 3
    "security_considerations",
    "performance_requirements",
    "monitoring_and_alerts",
    "rollback_strategy",
    "operational_runbook",
    "compliance_requirements",
    "cost_analysis",
    "migration_strategy",
]

# Tier completion times (in minutes)
TIER_COMPLETION_TIME: Dict[int, tuple] = {
    1: (2, 3),    # 2-3 minutes
    2: (10, 15),  # 10-15 minutes
    3: (30, 45),  # 30-45 minutes
}

# Tier section counts
TIER_SECTION_COUNT: Dict[int, int] = {
    1: 3,   # Minimal
    2: 9,   # Standard (includes all tier 1)
    3: 17,  # Complete (includes all tier 2)
}


def get_tier_number(tier_name: str) -> int:
    """
    Convert tier name to tier number.

    Args:
        tier_name: Tier name (minimal, standard, complete)

    Returns:
        Tier number (1, 2, or 3)

    Raises:
        ValueError: If tier name is invalid
    """
    tier_name_lower = tier_name.lower()
    if tier_name_lower not in TIER_NAME_TO_NUMBER:
        raise ValueError(
            f"Invalid tier name: {tier_name}. Must be one of: minimal, standard, complete"
        )
    return TIER_NAME_TO_NUMBER[tier_name_lower]


def get_tier_name(tier_number: int) -> str:
    """
    Convert tier number to tier name.

    Args:
        tier_number: Tier number (1, 2, or 3)

    Returns:
        Tier name (minimal, standard, complete)

    Raises:
        ValueError: If tier number is invalid
    """
    if tier_number not in TIER_NAMES:
        raise ValueError(f"Invalid tier number: {tier_number}. Must be 1, 2, or 3")
    return TIER_NAMES[tier_number]


def get_sections_for_tier(tier: int) -> List[str]:
    """
    Get list of sections for a given tier.

    Args:
        tier: Tier number (1, 2, or 3)

    Returns:
        List of section names in order

    Raises:
        ValueError: If tier is invalid
    """
    if tier not in TIER_SECTIONS:
        raise ValueError(f"Invalid tier: {tier}. Must be 1, 2, or 3")
    return TIER_SECTIONS[tier].copy()


def get_new_sections_for_tier(from_tier: int, to_tier: int) -> List[str]:
    """
    Get sections added when expanding from one tier to another.

    Args:
        from_tier: Starting tier number
        to_tier: Target tier number

    Returns:
        List of NEW section names (not in from_tier but in to_tier)

    Raises:
        ValueError: If tiers are invalid or from_tier >= to_tier
    """
    if from_tier not in TIER_SECTIONS or to_tier not in TIER_SECTIONS:
        raise ValueError("Invalid tier numbers")
    if from_tier >= to_tier:
        raise ValueError(f"Cannot expand from tier {from_tier} to {to_tier}")

    from_sections = set(TIER_SECTIONS[from_tier])
    to_sections = set(TIER_SECTIONS[to_tier])
    new_sections = to_sections - from_sections

    # Return in canonical order
    return [s for s in SECTION_ORDER if s in new_sections]


def validate_section_name(section_name: str) -> bool:
    """
    Check if a section name is valid.

    Args:
        section_name: Section name to validate

    Returns:
        True if valid, False otherwise
    """
    return section_name in SECTION_TIER_MAP


def get_section_tier(section_name: str) -> int:
    """
    Get the tier number for a section.

    Args:
        section_name: Section name

    Returns:
        Tier number (1, 2, or 3)

    Raises:
        ValueError: If section name is invalid
    """
    if section_name not in SECTION_TIER_MAP:
        raise ValueError(f"Unknown section: {section_name}")
    return SECTION_TIER_MAP[section_name]


def get_section_display_name(section_name: str) -> str:
    """
    Get display name for a section.

    Args:
        section_name: Section name (snake_case)

    Returns:
        Display name (Title Case)

    Raises:
        ValueError: If section name is invalid
    """
    if section_name not in SECTION_DISPLAY_NAMES:
        raise ValueError(f"Unknown section: {section_name}")
    return SECTION_DISPLAY_NAMES[section_name]


def get_completion_time(tier: int) -> tuple:
    """
    Get estimated completion time range for a tier.

    Args:
        tier: Tier number (1, 2, or 3)

    Returns:
        Tuple of (min_minutes, max_minutes)

    Raises:
        ValueError: If tier is invalid
    """
    if tier not in TIER_COMPLETION_TIME:
        raise ValueError(f"Invalid tier: {tier}")
    return TIER_COMPLETION_TIME[tier]


# Type hints for exports
__all__ = [
    "SECTION_TIER_MAP",
    "TIER_SECTIONS",
    "TIER_NAMES",
    "TIER_NAME_TO_NUMBER",
    "SECTION_DISPLAY_NAMES",
    "SECTION_ORDER",
    "TIER_COMPLETION_TIME",
    "TIER_SECTION_COUNT",
    "get_tier_number",
    "get_tier_name",
    "get_sections_for_tier",
    "get_new_sections_for_tier",
    "validate_section_name",
    "get_section_tier",
    "get_section_display_name",
    "get_completion_time",
]
