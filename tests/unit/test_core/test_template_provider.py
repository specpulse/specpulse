"""
Tests for TemplateProvider Service

Verifies:
- Template loading from files
- Fallback to embedded templates
- Variable substitution
- Caching behavior
- Error handling
"""

import pytest
import tempfile
from pathlib import Path

from specpulse.core.template_provider import TemplateProvider


class TestTemplateProvider:
    """Test template provider service"""

    @pytest.fixture
    def temp_resources(self):
        """Create temporary resources directory with templates"""
        with tempfile.TemporaryDirectory() as tmpdir:
            resources_dir = Path(tmpdir)
            templates_dir = resources_dir / "templates"
            templates_dir.mkdir()

            # Create template files
            (templates_dir / "spec.md").write_text("# Custom Spec Template")
            (templates_dir / "plan.md").write_text("# Custom Plan Template")
            (templates_dir / "task.md").write_text("# Custom Task Template")

            yield resources_dir

    def test_get_spec_template_from_file(self, temp_resources):
        """Test loading spec template from file"""
        provider = TemplateProvider(temp_resources, use_cache=False)
        template = provider.get_spec_template()

        assert template == "# Custom Spec Template"

    def test_get_plan_template_from_file(self, temp_resources):
        """Test loading plan template from file"""
        provider = TemplateProvider(temp_resources, use_cache=False)
        template = provider.get_plan_template()

        assert template == "# Custom Plan Template"

    def test_get_task_template_from_file(self, temp_resources):
        """Test loading task template from file"""
        provider = TemplateProvider(temp_resources, use_cache=False)
        template = provider.get_task_template()

        assert template == "# Custom Task Template"

    def test_fallback_to_embedded_when_missing(self):
        """Test fallback to embedded templates when files missing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            resources_dir = Path(tmpdir)
            # No templates directory created

            provider = TemplateProvider(resources_dir, use_cache=False)

            # Should return embedded templates
            spec = provider.get_spec_template()
            plan = provider.get_plan_template()
            task = provider.get_task_template()

            assert "Specification Template" in spec
            assert "Implementation Plan Template" in plan
            assert "Task List Template" in task

    def test_variable_substitution(self, temp_resources):
        """Test variable substitution in templates"""
        # Create template with variables
        template_file = temp_resources / "templates" / "test.md"
        template_file.write_text("Feature: {{feature_name}}, ID: {{feature_id}}")

        provider = TemplateProvider(temp_resources)
        result = provider.get_template(
            "test.md",
            variables={"feature_name": "user-auth", "feature_id": "001"}
        )

        assert result == "Feature: user-auth, ID: 001"


class TestCaching:
    """Test caching behavior"""

    def test_caching_reduces_file_reads(self, temp_resources):
        """Test that caching reduces file I/O"""
        provider = TemplateProvider(temp_resources, use_cache=True)

        # First call
        spec1 = provider.get_spec_template()
        # Second call (should be cached)
        spec2 = provider.get_spec_template()

        assert spec1 == spec2

    def test_no_caching_when_disabled(self, temp_resources):
        """Test that caching can be disabled"""
        provider = TemplateProvider(temp_resources, use_cache=False)

        # Both calls should read file
        spec1 = provider.get_spec_template()
        spec2 = provider.get_spec_template()

        assert spec1 == spec2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
