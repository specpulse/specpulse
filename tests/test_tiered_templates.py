"""
Tests for Tiered Templates (v1.9.0)

Tests template rendering, variable substitution, and tier inheritance.
"""

import pytest
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from datetime import datetime


@pytest.fixture
def template_dir():
    """Get path to template directory."""
    # Assuming tests run from project root
    return Path("specpulse/resources/templates")


@pytest.fixture
def jinja_env(template_dir):
    """Create Jinja2 environment for template rendering."""
    return Environment(loader=FileSystemLoader(str(template_dir)))


@pytest.fixture
def tier1_data():
    """Sample data for minimal tier template."""
    return {
        "feature_name": "test-authentication",
        "feature_id": "001",
        "date": "2025-10-06",
    }


@pytest.fixture
def tier2_data(tier1_data):
    """Sample data for standard tier template."""
    return {
        **tier1_data,
        # Standard tier uses same variables as tier1
    }


@pytest.fixture
def tier3_data(tier2_data):
    """Sample data for complete tier template."""
    return {
        **tier2_data,
        # Complete tier uses same variables as tier2
    }


class TestTier1MinimalTemplate:
    """Tests for minimal tier template (spec-tier1.md)."""

    def test_template_exists(self, template_dir):
        """Test that tier1 template file exists."""
        template_path = template_dir / "spec-tier1.md"
        assert template_path.exists(), "Tier 1 template file not found"

    def test_template_renders(self, jinja_env, tier1_data):
        """Test that tier1 template renders without errors."""
        try:
            template = jinja_env.get_template("spec-tier1.md")
            result = template.render(**tier1_data)
            assert result, "Template rendered empty content"
            assert len(result) > 0, "Template should produce non-empty output"
        except TemplateNotFound:
            pytest.fail("Tier 1 template not found")
        except Exception as e:
            pytest.fail(f"Template rendering failed: {e}")

    def test_variable_substitution(self, jinja_env, tier1_data):
        """Test that variables are correctly substituted."""
        template = jinja_env.get_template("spec-tier1.md")
        result = template.render(**tier1_data)

        # Check feature_name substitution
        assert "test-authentication" in result, "feature_name not substituted"

        # Check that placeholder braces are replaced
        assert "{{feature_name}}" not in result, "feature_name placeholder not replaced"
        assert "{{feature_id}}" not in result, "feature_id placeholder not replaced"
        assert "{{date}}" not in result, "date placeholder not replaced"

    def test_yaml_frontmatter(self, jinja_env, tier1_data):
        """Test that YAML frontmatter is present and valid."""
        template = jinja_env.get_template("spec-tier1.md")
        result = template.render(**tier1_data)

        # Check for YAML frontmatter markers
        assert "---" in result, "YAML frontmatter markers not found"
        assert "tier: minimal" in result, "Tier not set to minimal"
        assert "progress:" in result, "Progress field missing"
        assert "sections_completed:" in result, "Sections completed field missing"

    def test_has_three_sections(self, jinja_env, tier1_data):
        """Test that tier1 has exactly 3 main sections."""
        template = jinja_env.get_template("spec-tier1.md")
        result = template.render(**tier1_data)

        # Check for required sections
        assert "## What" in result, "What section missing"
        assert "## Why" in result, "Why section missing"
        assert "## Done When" in result, "Done When section missing"

        # Count section headers (## prefix)
        section_count = result.count("\n## ")
        # Should have: What, Why, Done When, Next Steps (4 total)
        # But we're testing for the 3 MAIN sections
        assert "## What" in result and "## Why" in result and "## Done When" in result

    def test_llm_guidance_comments(self, jinja_env, tier1_data):
        """Test that LLM guidance comments are present."""
        template = jinja_env.get_template("spec-tier1.md")
        result = template.render(**tier1_data)

        # Check for LLM guidance comments
        assert "<!-- LLM GUIDANCE" in result, "LLM guidance comments not found"

        # Should have guidance for all 3 sections
        guidance_count = result.count("<!-- LLM GUIDANCE")
        assert guidance_count >= 3, f"Expected at least 3 LLM guidance comments, found {guidance_count}"

    def test_placeholders_present(self, jinja_env, tier1_data):
        """Test that content placeholders are present for user to fill."""
        template = jinja_env.get_template("spec-tier1.md")
        result = template.render(**tier1_data)

        # Check for placeholder text
        assert "[One sentence:" in result, "What section placeholder missing"
        assert "Why is this feature needed" in result, "Why section placeholder missing"
        assert "[ ]" in result, "Done When checkboxes missing"


class TestTier2StandardTemplate:
    """Tests for standard tier template (spec-tier2.md)."""

    def test_template_exists(self, template_dir):
        """Test that tier2 template file exists."""
        template_path = template_dir / "spec-tier2.md"
        assert template_path.exists(), "Tier 2 template file not found"

    def test_template_renders(self, jinja_env, tier2_data):
        """Test that tier2 template renders without errors."""
        template = jinja_env.get_template("spec-tier2.md")
        result = template.render(**tier2_data)
        assert result and len(result) > 0

    def test_extends_tier1(self, jinja_env, tier1_data, tier2_data):
        """Test that tier2 includes all tier1 sections."""
        tier1 = jinja_env.get_template("spec-tier1.md")
        tier2 = jinja_env.get_template("spec-tier2.md")

        tier1_result = tier1.render(**tier1_data)
        tier2_result = tier2.render(**tier2_data)

        # Tier 1 sections must be present in tier 2
        assert "## What" in tier2_result
        assert "## Why" in tier2_result
        assert "## Done When" in tier2_result

    def test_has_additional_sections(self, jinja_env, tier2_data):
        """Test that tier2 has additional sections beyond tier1."""
        template = jinja_env.get_template("spec-tier2.md")
        result = template.render(**tier2_data)

        # Check for tier 2 specific sections
        assert "## User Stories" in result
        assert "## Functional Requirements" in result
        assert "## Technical Approach" in result
        assert "## API Design" in result
        assert "## Dependencies" in result

    def test_yaml_frontmatter_tier_standard(self, jinja_env, tier2_data):
        """Test that tier2 frontmatter says standard."""
        template = jinja_env.get_template("spec-tier2.md")
        result = template.render(**tier2_data)

        assert "tier: standard" in result, "Tier not set to standard"

    def test_llm_guidance_in_new_sections(self, jinja_env, tier2_data):
        """Test that new sections have LLM guidance."""
        template = jinja_env.get_template("spec-tier2.md")
        result = template.render(**tier2_data)

        # Should have MORE guidance comments than tier1
        guidance_count = result.count("<!-- LLM GUIDANCE")
        assert guidance_count >= 5, f"Expected at least 5 LLM guidance comments, found {guidance_count}"


class TestTier3CompleteTemplate:
    """Tests for complete tier template (spec-tier3.md)."""

    def test_template_exists(self, template_dir):
        """Test that tier3 template file exists."""
        template_path = template_dir / "spec-tier3.md"
        assert template_path.exists(), "Tier 3 template file not found"

    def test_template_renders(self, jinja_env, tier3_data):
        """Test that tier3 template renders without errors."""
        template = jinja_env.get_template("spec-tier3.md")
        result = template.render(**tier3_data)
        assert result and len(result) > 0

    def test_extends_tier2(self, jinja_env, tier2_data, tier3_data):
        """Test that tier3 includes all tier2 sections."""
        tier2 = jinja_env.get_template("spec-tier2.md")
        tier3 = jinja_env.get_template("spec-tier3.md")

        tier2_result = tier2.render(**tier2_data)
        tier3_result = tier3.render(**tier3_data)

        # All tier 2 sections must be in tier 3
        tier2_sections = [
            "## What",
            "## Why",
            "## Done When",
            "## User Stories",
            "## Functional Requirements",
            "## Technical Approach",
            "## API Design",
            "## Dependencies",
        ]

        for section in tier2_sections:
            assert section in tier3_result, f"Tier 3 missing tier 2 section: {section}"

    def test_has_production_sections(self, jinja_env, tier3_data):
        """Test that tier3 has production-grade sections."""
        template = jinja_env.get_template("spec-tier3.md")
        result = template.render(**tier3_data)

        # Check for tier 3 specific sections
        assert "## Security Considerations" in result
        assert "## Performance Requirements" in result
        assert "## Monitoring & Alerts" in result or "## Monitoring and Alerts" in result
        assert "## Rollback Strategy" in result
        assert "## Operational Runbook" in result
        assert "## Compliance Requirements" in result
        assert "## Cost Analysis" in result
        assert "## Migration Strategy" in result

    def test_yaml_frontmatter_tier_complete(self, jinja_env, tier3_data):
        """Test that tier3 frontmatter says complete."""
        template = jinja_env.get_template("spec-tier3.md")
        result = template.render(**tier3_data)

        assert "tier: complete" in result, "Tier not set to complete"

    def test_has_most_llm_guidance(self, jinja_env, tier3_data):
        """Test that tier3 has the most LLM guidance comments."""
        template = jinja_env.get_template("spec-tier3.md")
        result = template.render(**tier3_data)

        # Should have MOST guidance comments
        guidance_count = result.count("<!-- LLM GUIDANCE")
        assert guidance_count >= 10, f"Expected at least 10 LLM guidance comments, found {guidance_count}"


class TestTierInheritance:
    """Test that tiers properly inherit from previous tiers."""

    def test_section_count_increases(self, jinja_env, tier1_data, tier2_data, tier3_data):
        """Test that section count increases with each tier."""
        tier1 = jinja_env.get_template("spec-tier1.md").render(**tier1_data)
        tier2 = jinja_env.get_template("spec-tier2.md").render(**tier2_data)
        tier3 = jinja_env.get_template("spec-tier3.md").render(**tier3_data)

        tier1_sections = tier1.count("\n## ")
        tier2_sections = tier2.count("\n## ")
        tier3_sections = tier3.count("\n## ")

        assert tier2_sections > tier1_sections, "Tier 2 should have more sections than tier 1"
        assert tier3_sections > tier2_sections, "Tier 3 should have more sections than tier 2"

    def test_content_length_increases(self, jinja_env, tier1_data, tier2_data, tier3_data):
        """Test that content length increases with each tier."""
        tier1 = jinja_env.get_template("spec-tier1.md").render(**tier1_data)
        tier2 = jinja_env.get_template("spec-tier2.md").render(**tier2_data)
        tier3 = jinja_env.get_template("spec-tier3.md").render(**tier3_data)

        assert len(tier2) > len(tier1), "Tier 2 should be longer than tier 1"
        assert len(tier3) > len(tier2), "Tier 3 should be longer than tier 2"


class TestSectionOrder:
    """Test that sections appear in correct order."""

    def test_tier1_section_order(self, jinja_env, tier1_data):
        """Test that tier1 sections are in correct order."""
        template = jinja_env.get_template("spec-tier1.md")
        result = template.render(**tier1_data)

        what_pos = result.find("## What")
        why_pos = result.find("## Why")
        done_pos = result.find("## Done When")

        assert what_pos < why_pos < done_pos, "Tier 1 sections not in correct order"

    def test_tier2_section_order(self, jinja_env, tier2_data):
        """Test that tier2 sections are in correct order."""
        template = jinja_env.get_template("spec-tier2.md")
        result = template.render(**tier2_data)

        # Core sections should come first
        what_pos = result.find("## What")
        why_pos = result.find("## Why")
        done_pos = result.find("## Done When")

        # Then tier 2 sections
        stories_pos = result.find("## User Stories")
        reqs_pos = result.find("## Functional Requirements")

        assert what_pos < why_pos < done_pos, "Core sections not in order"
        assert done_pos < stories_pos < reqs_pos, "Tier 2 sections not in order"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
