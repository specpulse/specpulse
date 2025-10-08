"""
Tests for Template Manager module
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import json

from specpulse.core.template_manager import (
    TemplateManager, TemplateMetadata, TemplateValidationResult
)
from specpulse.core.memory_manager import DecisionRecord


class TestTemplateManager:
    """Test TemplateManager functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)

        # Create basic directory structure
        (self.project_path / "templates").mkdir(exist_ok=True)
        (self.project_path / ".specpulse").mkdir(exist_ok=True)
        (self.project_path / ".specpulse" / "template_backups").mkdir(exist_ok=True)

    def teardown_method(self):
        """Clean up test fixtures"""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_template_manager_initialization(self):
        """Test TemplateManager initialization"""
        manager = TemplateManager(self.project_path)
        assert manager.project_root == self.project_path
        assert manager.templates_dir.exists()
        assert manager.template_registry.exists()
        assert isinstance(manager.registry, dict)
        assert "templates" in manager.registry
        assert "version" in manager.registry

    def test_extract_variables_from_template(self):
        """Test Jinja2 variable extraction"""
        manager = TemplateManager(self.project_path)

        content = """
        # Specification: {{ feature_name }}
        ## ID: SPEC-{{ spec_id }}
        Created: {{ date }}
        Author: {{ author }}
        """

        variables = manager._extract_variables(content)
        expected_vars = {"feature_name", "spec_id", "date", "author"}
        assert variables == expected_vars

    def test_extract_variables_with_conditionals(self):
        """Test variable extraction from conditional blocks"""
        manager = TemplateManager(self.project_path)

        content = """
        {% if author %}
        Created by: {{ author }}
        {% endif %}
        Technology: {{ technology_stack }}
        {% if custom_field %}
        Custom: {{ custom_field }}
        {% endif %}
        """

        variables = manager._extract_variables(content)
        expected_vars = {"author", "technology_stack", "custom_field"}
        assert variables == expected_vars

    def test_validate_template_variables_valid(self):
        """Test template variable validation with valid template"""
        manager = TemplateManager(self.project_path)

        # Create a valid spec template
        template_path = manager.templates_dir / "spec.md"
        content = """
        # Specification: {{ feature_name }}
        ## ID: SPEC-{{ spec_id }}
        ## Functional Requirements
        ## User Stories
        ## Acceptance Criteria
        """
        template_path.write_text(content)

        missing, extra = manager._validate_template_variables(template_path)
        assert not missing  # Should not have missing standard variables
        assert len(extra) > 0  # Should have some variables

    def test_validate_template_variables_missing_required(self):
        """Test template variable validation with missing required variables"""
        manager = TemplateManager(self.project_path)

        # Create an invalid spec template missing required sections
        template_path = manager.templates_dir / "spec.md"
        content = """
        # Basic Template
        This template is missing required sections.
        """
        template_path.write_text(content)

        missing, extra = manager._validate_template_variables(template_path)
        assert len(missing) > 0  # Should have missing standard variables

    def test_validate_template_jinja2_syntax(self):
        """Test template validation with Jinja2 syntax"""
        manager = TemplateManager(self.project_path)

        # Create valid template
        template_path = manager.templates_dir / "valid.md"
        content = """
        # {{ title }}
        {% if description %}
        Description: {{ description }}
        {% endif %}
        """
        template_path.write_text(content)

        result = manager.validate_template(template_path)
        assert result.valid
        assert not result.errors

    def test_validate_template_invalid_jinja2_syntax(self):
        """Test template validation with invalid Jinja2 syntax"""
        manager = TemplateManager(self.project_path)

        # Create invalid template
        template_path = manager.templates_dir / "invalid.md"
        content = """
        # {{ title
        {% if description %}
        Description: {{ description }}
        """
        template_path.write_text(content)

        result = manager.validate_template(template_path)
        assert not result.valid
        assert len(result.errors) > 0

    def test_validate_template_missing_sections(self):
        """Test template validation for missing required sections"""
        manager = TemplateManager(self.project_path)

        # Create template missing required sections
        template_path = manager.templates_dir / "spec.md"
        content = """
        # Basic Specification
        This is missing required sections.
        """
        template_path.write_text(content)

        result = manager.validate_template(template_path)
        assert not result.valid
        assert any("Missing recommended section" in warning for warning in result.warnings)

    def test_register_template_valid(self):
        """Test registering a valid template"""
        manager = TemplateManager(self.project_path)

        # Create valid template
        template_path = manager.templates_dir / "test_spec.md"
        content = """
        # Specification: {{ feature_name }}
        ## Functional Requirements
        ## Acceptance Criteria
        """
        template_path.write_text(content)

        success = manager.register_template(template_path)
        assert success
        assert "spec/test_spec" in manager.registry["templates"]

    def test_register_template_invalid(self):
        """Test registering an invalid template"""
        manager = TemplateManager(self.project_path)

        # Create invalid template (doesn't exist)
        template_path = manager.templates_dir / "nonexistent.md"

        success = manager.register_template(template_path)
        assert not success

    def test_get_template_preview(self):
        """Test template preview generation"""
        manager = TemplateManager(self.project_path)

        # Create template
        template_path = manager.templates_dir / "test_spec.md"
        content = """
        # Specification: {{ feature_name }}
        ## ID: SPEC-{{ spec_id }}
        Created: {{ date }}
        """
        template_path.write_text(content)

        preview = manager.get_template_preview(template_path)
        assert "User Authentication" in preview  # Sample data
        assert "001" in preview
        assert datetime.now().strftime("%Y-%m-%d") in preview

    def test_backup_templates(self):
        """Test template backup functionality"""
        manager = TemplateManager(self.project_path)

        # Create some templates
        (manager.templates_dir / "spec.md").write_text("# Spec Template")
        (manager.templates_dir / "plan.md").write_text("# Plan Template")

        backup_path = manager.backup_templates()
        assert Path(backup_path).exists()
        assert (Path(backup_path) / "spec.md").exists()
        assert (Path(backup_path) / "plan.md").exists()
        assert (Path(backup_path) / "template_registry.json").exists()

    def test_restore_templates(self):
        """Test template restore functionality"""
        manager = TemplateManager(self.project_path)

        # Create original templates
        (manager.templates_dir / "spec.md").write_text("# Original Spec")

        # Create backup
        backup_path = manager.backup_templates()

        # Modify original
        (manager.templates_dir / "spec.md").write_text("# Modified Spec")

        # Restore from backup
        success = manager.restore_templates(backup_path)
        assert success
        assert (manager.templates_dir / "spec.md").read_text() == "# Original Spec"

    def test_list_templates(self):
        """Test listing templates"""
        manager = TemplateManager(self.project_path)

        # Create templates and register them
        spec_path = manager.templates_dir / "spec.md"
        spec_path.write_text("# Spec Template")
        manager.register_template(spec_path)

        plan_path = manager.templates_dir / "plan.md"
        plan_path.write_text("# Plan Template")
        manager.register_template(plan_path)

        templates = manager.list_templates()
        assert len(templates) == 2
        assert any(t["name"] == "spec" for t in templates)
        assert any(t["name"] == "plan" for t in templates)

    def test_list_templates_by_category(self):
        """Test listing templates filtered by category"""
        manager = TemplateManager(self.project_path)

        # Create templates
        spec_path = manager.templates_dir / "spec.md"
        spec_path.write_text("# Spec Template")
        manager.register_template(spec_path)

        plan_path = manager.templates_dir / "plan.md"
        plan_path.write_text("# Plan Template")
        manager.register_template(plan_path)

        spec_templates = manager.list_templates("spec")
        assert len(spec_templates) == 1
        assert spec_templates[0]["category"] == "spec"

    def test_update_template_version(self):
        """Test updating template version"""
        manager = TemplateManager(self.project_path)

        # Create and register template
        template_path = manager.templates_dir / "test.md"
        template_path.write_text("# Test Template")
        manager.register_template(template_path)

        # Update version
        success = manager.update_template_version("spec/test", "1.1.0", "Added new section")
        assert success

        # Check version updated
        template_info = manager.get_template_info("spec/test")
        assert template_info["version"] == "1.1.0"
        assert "change_log" in template_info

    def test_validate_all_templates(self):
        """Test validating all templates"""
        manager = TemplateManager(self.project_path)

        # Create multiple templates
        (manager.templates_dir / "spec.md").write_text("# Valid Spec Template")
        (manager.templates_dir / "plan.md").write_text("# Valid Plan Template")

        results = manager.validate_all_templates()
        assert len(results) == 2
        assert "spec.md" in results
        assert "plan.md" in results

    def test_get_sample_data(self):
        """Test sample data generation for different categories"""
        manager = TemplateManager(self.project_path)

        spec_data = manager._get_sample_data("spec")
        assert "feature_name" in spec_data
        assert "executive_summary" in spec_data

        plan_data = manager._get_sample_data("plan")
        assert "feature_name" in plan_data
        assert "architecture_pattern" in plan_data

        task_data = manager._get_sample_data("task")
        assert "feature_name" in task_data
        assert "complexity" in task_data


class TestTemplateValidationResult:
    """Test TemplateValidationResult dataclass"""

    def test_validation_result_creation(self):
        """Test creating validation result"""
        result = TemplateValidationResult(
            valid=True,
            errors=[],
            warnings=["Minor warning"],
            missing_variables=[],
            extra_variables=["custom_var"],
            sdd_compliance={"Specification First": True},
            suggestions=["Consider adding more sections"]
        )

        assert result.valid
        assert len(result.warnings) == 1
        assert len(result.extra_variables) == 1
        assert result.sdd_compliance["Specification First"]


class TestTemplateMetadata:
    """Test TemplateMetadata dataclass"""

    def test_metadata_creation(self):
        """Test creating template metadata"""
        metadata = TemplateMetadata(
            name="test_template",
            version="1.0.0",
            description="Test template",
            category="spec",
            author="Test Author",
            created="2024-01-01T00:00:00",
            modified="2024-01-01T00:00:00",
            variables=["feature_name", "spec_id"],
            sdd_principles=["Specification First"],
            dependencies=[],
            tags=["test"]
        )

        assert metadata.name == "test_template"
        assert metadata.category == "spec"
        assert "feature_name" in metadata.variables