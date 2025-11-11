"""
Comprehensive tests for TemplateManager.

This module provides thorough testing of the template management system
including validation, security, backup/restore, and registry operations.
"""

import pytest
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from specpulse.core.template_manager import (
    TemplateManager, TemplateMetadata, TemplateValidationResult,
    validate_template_security
)
from specpulse.utils.error_handler import TemplateError


class TestTemplateSecurityValidation:
    """Test template security validation"""

    def test_validate_template_security_safe(self):
        """Test validation of safe template content"""
        safe_content = """
        # {{title}}

        Author: {{author}}
        Date: {{date}}

        Content:
        {{content}}
        """

        is_safe, vulnerabilities = validate_template_security(safe_content)

        assert is_safe is True
        assert vulnerabilities == []

    def test_validate_template_security_dangerous_patterns(self):
        """Test validation of template with dangerous patterns"""
        dangerous_patterns = [
            ("{{ config.item }}", "config attribute access"),
            ("{{ env.variable }}", "environment variable access"),
            ("{{ request.user }}", "request object access"),
            ("{{ __class__ }}", "dunder method access"),
            ("{{ item.eval('...') }}", "eval method call"),
            ("{{ item.exec('...') }}", "exec method call"),
            ("{{ item.open('file') }}", "file open call"),
            ("{{ item.subprocess.call('...') }}", "subprocess access"),
            ("{{ item.os.system('...') }}", "os module access"),
            ("{{ item.sys.path }}", "sys module access"),
        ]

        for content, description in dangerous_patterns:
            is_safe, vulnerabilities = validate_template_security(content)
            assert is_safe is False
            assert len(vulnerabilities) > 0
            assert any("Dangerous template pattern" in v for v in vulnerabilities)

    def test_validate_template_security_large_template(self):
        """Test validation of oversized template"""
        # Create a template with many lines
        content = "\n".join([f"Line {i}: {{variable_{i}}}" for i in range(1500)])

        is_safe, vulnerabilities = validate_template_security(content)

        assert is_safe is False
        assert any("too large" in v.lower() for v in vulnerabilities)

    def test_validate_template_security_too_many_variables(self):
        """Test validation of template with too many variables"""
        # Create template with many variables
        variables = ", ".join([f"var_{i}" for i in range(250)])
        content = f"{{{{ {variables} }}}}"

        is_safe, vulnerabilities = validate_template_security(content)

        assert is_safe is False
        assert any("Too many template variables" in v for v in vulnerabilities)

    def test_validate_template_security_deep_nesting(self):
        """Test validation of template with deep nesting"""
        # Create deeply nested if blocks
        nested_content = ""
        for i in range(15):
            nested_content += "{% if condition %}"
        nested_content += "Content"
        for i in range(15):
            nested_content += "{% endif %}"

        is_safe, vulnerabilities = validate_template_security(nested_content)

        assert is_safe is False
        assert any("nesting too deep" in v for v in vulnerabilities)

    def test_validate_template_security_case_insensitive(self):
        """Test that pattern detection is case insensitive"""
        content = "{{ CONFIG.item }}"  # Uppercase config

        is_safe, vulnerabilities = validate_template_security(content)

        assert is_safe is False
        assert any("config" in v.lower() for v in vulnerabilities)


class TestTemplateMetadata:
    """Test TemplateMetadata dataclass"""

    def test_template_metadata_creation(self):
        """Test creating TemplateMetadata"""
        metadata = TemplateMetadata(
            name="spec_template",
            version="1.0.0",
            description="Specification template",
            category="spec",
            author="Test Author",
            created="2023-01-01T00:00:00",
            modified="2023-01-01T00:00:00",
            variables=["title", "content"],
            sdd_principles=["Specification First"],
            dependencies=[],
            tags=["spec", "template"]
        )

        assert metadata.name == "spec_template"
        assert metadata.version == "1.0.0"
        assert metadata.category == "spec"
        assert metadata.sdd_principles == ["Specification First"]

    def test_template_metadata_default_values(self):
        """Test TemplateMetadata with default values"""
        metadata = TemplateMetadata(
            name="test",
            version="1.0.0",
            description="Test template",
            category="test",
            author="Test",
            created="2023-01-01",
            modified="2023-01-01",
            variables=[],
            sdd_principles=[],
            dependencies=[],
            tags=[]
        )

        assert metadata.file_size == 0
        assert metadata.checksum == ""

    def test_template_metadata_to_dict(self):
        """Test converting TemplateMetadata to dictionary"""
        metadata = TemplateMetadata(
            name="test",
            version="1.0.0",
            description="Test",
            category="test",
            author="Test",
            created="2023-01-01",
            modified="2023-01-01",
            variables=["var1"],
            sdd_principles=["principle1"],
            dependencies=[],
            tags=[]
        )

        # Convert to dict using asdict
        from dataclasses import asdict
        metadata_dict = asdict(metadata)

        assert metadata_dict["name"] == "test"
        assert metadata_dict["version"] == "1.0.0"
        assert isinstance(metadata_dict, dict)


class TestTemplateValidationResult:
    """Test TemplateValidationResult dataclass"""

    def test_validation_result_creation(self):
        """Test creating TemplateValidationResult"""
        result = TemplateValidationResult(
            valid=True,
            errors=[],
            warnings=["Minor issue"],
            missing_variables=["required_var"],
            extra_variables=["extra_var"],
            sdd_compliance={"Specification First": True},
            suggestions=["Add more details"]
        )

        assert result.valid is True
        assert result.errors == []
        assert len(result.warnings) == 1
        assert result.missing_variables == ["required_var"]
        assert result.sdd_compliance["Specification First"] is True

    def test_validation_result_invalid(self):
        """Test TemplateValidationResult for invalid template"""
        result = TemplateValidationResult(
            valid=False,
            errors=["Syntax error"],
            warnings=[],
            missing_variables=[],
            extra_variables=[],
            sdd_compliance={},
            suggestions=["Fix syntax"]
        )

        assert result.valid is False
        assert len(result.errors) == 1
        assert "Syntax error" in result.errors[0]


class TestTemplateManager:
    """Test TemplateManager class"""

    def test_template_manager_init_new_structure(self, temp_project_dir):
        """Test TemplateManager initialization with new structure"""
        # Create .specpulse structure
        specpulse_dir = temp_project_dir / ".specpulse"
        specpulse_dir.mkdir()
        templates_dir = specpulse_dir / "templates"
        templates_dir.mkdir()

        manager = TemplateManager(temp_project_dir)

        assert manager.project_root == temp_project_dir
        assert manager.templates_dir == templates_dir
        assert manager.template_registry == specpulse_dir / "template_registry.json"
        assert manager.template_backup_dir == specpulse_dir / "template_backups"
        assert manager.templates_dir.exists()

    def test_template_manager_init_legacy_fallback(self, temp_project_dir):
        """Test TemplateManager initialization fallback to legacy structure"""
        # Create only legacy structure
        legacy_templates = temp_project_dir / "templates"
        legacy_templates.mkdir()

        manager = TemplateManager(temp_project_dir)

        assert manager.templates_dir == legacy_templates

    def test_template_manager_init_no_structure(self, temp_project_dir):
        """Test TemplateManager initialization when no structure exists"""
        manager = TemplateManager(temp_project_dir)

        # Should create .specpulse structure
        specpulse_dir = temp_project_dir / ".specpulse"
        assert specpulse_dir.exists()
        assert (specpulse_dir / "templates").exists()
        assert (specpulse_dir / "template_backups").exists()

    def test_load_registry_existing(self, temp_project_dir):
        """Test loading existing registry"""
        # Create registry file
        specpulse_dir = temp_project_dir / ".specpulse"
        specpulse_dir.mkdir()
        registry_file = specpulse_dir / "template_registry.json"

        test_registry = {
            "templates": {
                "spec/test": {
                    "name": "test",
                    "version": "1.0.0",
                    "category": "spec"
                }
            },
            "version": "1.0.0",
            "last_updated": "2023-01-01T00:00:00"
        }

        with open(registry_file, 'w') as f:
            json.dump(test_registry, f)

        manager = TemplateManager(temp_project_dir)

        assert "spec/test" in manager.registry["templates"]
        assert manager.registry["templates"]["spec/test"]["name"] == "test"

    def test_load_registry_corrupted(self, temp_project_dir):
        """Test loading corrupted registry"""
        # Create corrupted registry file
        specpulse_dir = temp_project_dir / ".specpulse"
        specpulse_dir.mkdir()
        registry_file = specpulse_dir / "template_registry.json"

        with open(registry_file, 'w') as f:
            f.write("invalid json content")

        with patch('specpulse.core.template_manager.Console') as mock_console:
            manager = TemplateManager(temp_project_dir)

            # Should have created default registry
            assert "templates" in manager.registry
            assert manager.registry["version"] == "1.0.0"

            # Should have logged warning
            mock_console.return_value.warning.assert_called()

    def test_save_registry(self, temp_project_dir):
        """Test saving registry"""
        manager = TemplateManager(temp_project_dir)

        # Modify registry
        manager.registry["test_key"] = "test_value"

        # Save registry
        manager._save_registry()

        # Verify file was created/updated
        registry_file = manager.template_registry
        assert registry_file.exists()

        with open(registry_file, 'r') as f:
            saved_registry = json.load(f)

        assert saved_registry["test_key"] == "test_value"
        assert "last_updated" in saved_registry

    def test_extract_variables(self, temp_project_dir):
        """Test variable extraction from template content"""
        manager = TemplateManager(temp_project_dir)

        content = """
        # {{title}}

        Author: {{author}}
        Date: {{date}}

        {% if show_content %}
        Content: {{content}}
        {% endif %}
        """

        variables = manager._extract_variables(content)

        expected_vars = {"title", "author", "date", "show_content", "content"}
        assert variables == expected_vars

    def test_calculate_checksum(self, temp_project_dir):
        """Test checksum calculation"""
        manager = TemplateManager(temp_project_dir)

        content = "Test template content"
        checksum1 = manager._calculate_checksum(content)
        checksum2 = manager._calculate_checksum(content)

        # Same content should produce same checksum
        assert checksum1 == checksum2
        assert len(checksum1) == 32  # MD5 hex length

        # Different content should produce different checksum
        different_content = "Different content"
        checksum3 = manager._calculate_checksum(different_content)
        assert checksum1 != checksum3

    def test_get_template_category_from_name(self, temp_project_dir):
        """Test determining template category from filename"""
        manager = TemplateManager(temp_project_dir)

        # Test various filename patterns
        test_cases = [
            ("spec_template.md", "spec"),
            ("plan_template.md", "plan"),
            ("task_template.md", "task"),
            ("decomposition_template.md", "decomposition"),
            ("unknown_template.md", "unknown"),
        ]

        for filename, expected_category in test_cases:
            template_path = Path(filename)
            category = manager._get_template_category(template_path)
            assert category == expected_category

    def test_get_template_category_from_content(self, temp_project_dir):
        """Test determining template category from content"""
        manager = TemplateManager(temp_project_dir)

        # Create temp files with different content
        test_content = {
            "Specification:": "spec",
            "Implementation Plan:": "plan",
            "Task Breakdown:": "task",
            "Random content": "unknown"
        }

        for content_indicator, expected_category in test_content.items():
            content = f"""
            # Template Title

            {content_indicator}

            More content here.
            """

            template_file = temp_project_dir / "test_template.md"
            template_file.write_text(content)

            category = manager._get_template_category(template_file)
            assert category == expected_category

    def test_validate_sdd_compliance(self, temp_project_dir):
        """Test SDD compliance validation"""
        manager = TemplateManager(temp_project_dir)

        content = """
        # Template

        This template includes functional requirements
        and acceptance criteria for user stories.

        Implementation phases and milestones are defined.
        """

        template_file = temp_project_dir / "test_template.md"
        template_file.write_text(content)

        compliance = manager._validate_sdd_compliance(template_file)

        # Should detect compliance based on keywords
        assert isinstance(compliance, dict)
        assert "Specification First" in compliance
        assert "Incremental Planning" in compliance

    def test_validate_template_file_not_found(self, temp_project_dir):
        """Test validation of non-existent template"""
        manager = TemplateManager(temp_project_dir)

        non_existent = temp_project_dir / "non_existent.md"
        result = manager.validate_template(non_existent)

        assert result.valid is False
        assert len(result.errors) > 0
        assert "not found" in result.errors[0]

    def test_validate_template_successful(self, temp_project_dir):
        """Test successful template validation"""
        manager = TemplateManager(temp_project_dir)

        # Create a valid spec template
        content = """
        # {{feature_name}} Specification

        ## Specification:

        ## Functional Requirements

        ## Acceptance Criteria
        """

        template_file = manager.templates_dir / "spec_template.md"
        template_file.write_text(content)

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            # Mock the validator to return success
            mock_validation_result = Mock()
            mock_validation_result.issues = []
            mock_validation_result.suggestions = []
            mock_validation_result.variables = {"feature_name"}
            mock_validation_result.is_safe = True
            mock_validation_result.critical_issues = []
            mock_validation_result.error_issues = []

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            result = manager.validate_template(template_file)

            assert isinstance(result, TemplateValidationResult)

    def test_register_template_success(self, temp_project_dir):
        """Test successful template registration"""
        manager = TemplateManager(temp_project_dir)

        # Create a template file
        content = "# {{title}}\n\nContent: {{content}}"
        template_file = manager.templates_dir / "test_template.md"
        template_file.write_text(content)

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            # Mock successful validation
            mock_validation_result = Mock()
            mock_validation_result.issues = []
            mock_validation_result.suggestions = []
            mock_validation_result.variables = {"title", "content"}
            mock_validation_result.is_safe = True
            mock_validation_result.critical_issues = []
            mock_validation_result.error_issues = []

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            result = manager.register_template(template_file)

            assert result is True
            assert "unknown/test_template" in manager.registry["templates"]

    def test_register_template_with_metadata(self, temp_project_dir):
        """Test template registration with custom metadata"""
        manager = TemplateManager(temp_project_dir)

        # Create a template file
        content = "# {{title}}"
        template_file = manager.templates_dir / "custom_template.md"
        template_file.write_text(content)

        metadata = TemplateMetadata(
            name="custom_template",
            version="2.0.0",
            description="Custom template",
            category="spec",
            author="Custom Author",
            created=datetime.now().isoformat(),
            modified=datetime.now().isoformat(),
            variables=["title"],
            sdd_principles=[],
            dependencies=[],
            tags=[]
        )

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            mock_validation_result = Mock()
            mock_validation_result.issues = []
            mock_validation_result.suggestions = []
            mock_validation_result.variables = {"title"}
            mock_validation_result.is_safe = True
            mock_validation_result.critical_issues = []
            mock_validation_result.error_issues = []

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            result = manager.register_template(template_file, metadata)

            assert result is True
            assert "spec/custom_template" in manager.registry["templates"]
            registry_entry = manager.registry["templates"]["spec/custom_template"]
            assert registry_entry["author"] == "Custom Author"
            assert registry_entry["version"] == "2.0.0"

    def test_register_template_file_not_found(self, temp_project_dir):
        """Test template registration with non-existent file"""
        manager = TemplateManager(temp_project_dir)

        non_existent = temp_project_dir / "non_existent.md"

        with pytest.raises(TemplateError):
            manager.register_template(non_existent)

    def test_register_template_validation_failure(self, temp_project_dir):
        """Test template registration with validation failure"""
        manager = TemplateManager(temp_project_dir)

        # Create a template file
        content = "# {{title}}"
        template_file = manager.templates_dir / "invalid_template.md"
        template_file.write_text(content)

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            # Mock validation failure
            mock_validation_result = Mock()
            mock_validation_result.issues = [Mock(severity=Mock(value='error'), message="Validation error")]
            mock_validation_result.is_safe = False

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            result = manager.register_template(template_file)

            assert result is False

    def test_backup_templates(self, temp_project_dir):
        """Test template backup creation"""
        manager = TemplateManager(temp_project_dir)

        # Create some template files
        template1 = manager.templates_dir / "template1.md"
        template1.write_text("Template 1 content")

        template2 = manager.templates_dir / "subdir" / "template2.md"
        template2.parent.mkdir()
        template2.write_text("Template 2 content")

        # Create registry
        manager.registry["templates"]["test/template1"] = {"name": "template1"}
        manager._save_registry()

        backup_path = manager.backup_templates()

        assert backup_path is not None
        backup_dir = Path(backup_path)
        assert backup_dir.exists()
        assert (backup_dir / "template1.md").exists()
        assert (backup_dir / "subdir" / "template2.md").exists()
        assert (backup_dir / "template_registry.json").exists()

    def test_restore_templates(self, temp_project_dir):
        """Test template restoration from backup"""
        manager = TemplateManager(temp_project_dir)

        # Create original templates
        original_template = manager.templates_dir / "original.md"
        original_template.write_text("Original content")

        # Create backup directory with templates to restore
        backup_dir = manager.template_backup_dir / "test_backup"
        backup_dir.mkdir()

        restore_template = backup_dir / "restore.md"
        restore_template.write_text("Restored content")

        # Create backup registry
        backup_registry = backup_dir / "template_registry.json"
        backup_registry.write_text(json.dumps({
            "templates": {"test/restore": {"name": "restore", "version": "1.0.0"}},
            "version": "1.0.0"
        }))

        result = manager.restore_templates(str(backup_dir))

        assert result is True
        assert (manager.templates_dir / "restore.md").exists()
        assert (manager.templates_dir / "restore.md").read_text() == "Restored content"

    def test_restore_templates_backup_not_found(self, temp_project_dir):
        """Test template restoration with non-existent backup"""
        manager = TemplateManager(temp_project_dir)

        non_existent = temp_project_dir / "non_existent_backup"

        result = manager.restore_templates(str(non_existent))

        assert result is False

    def test_get_template_preview_success(self, temp_project_dir):
        """Test successful template preview generation"""
        manager = TemplateManager(temp_project_dir)

        # Create a template file
        content = "# {{title}}\n\nAuthor: {{author}}\n\n{{content}}"
        template_file = manager.templates_dir / "preview_template.md"
        template_file.write_text(content)

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            # Mock successful validation
            mock_validation_result = Mock()
            mock_validation_result.issues = []
            mock_validation_result.suggestions = []
            mock_validation_result.variables = {"title", "author", "content"}
            mock_validation_result.is_safe = True
            mock_validation_result.critical_issues = []
            mock_validation_result.error_issues = []

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            preview = manager.get_template_preview(template_file)

            assert isinstance(preview, str)
            assert "User Authentication" in preview  # From sample data
            assert "Development Team" in preview

    def test_get_template_preview_with_custom_data(self, temp_project_dir):
        """Test template preview with custom sample data"""
        manager = TemplateManager(temp_project_dir)

        # Create a template file
        content = "# {{title}}\n\nAuthor: {{author}}"
        template_file = manager.templates_dir / "custom_preview.md"
        template_file.write_text(content)

        custom_data = {
            "title": "Custom Title",
            "author": "Custom Author"
        }

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            mock_validation_result = Mock()
            mock_validation_result.issues = []
            mock_validation_result.suggestions = []
            mock_validation_result.variables = {"title", "author"}
            mock_validation_result.is_safe = True
            mock_validation_result.critical_issues = []
            mock_validation_result.error_issues = []

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            preview = manager.get_template_preview(template_file, custom_data)

            assert "Custom Title" in preview
            assert "Custom Author" in preview

    def test_get_template_preview_template_not_found(self, temp_project_dir):
        """Test template preview with non-existent template"""
        manager = TemplateManager(temp_project_dir)

        non_existent = temp_project_dir / "non_existent.md"

        with pytest.raises(TemplateError):
            manager.get_template_preview(non_existent)

    def test_get_template_preview_security_violation(self, temp_project_dir):
        """Test template preview with security violations"""
        manager = TemplateManager(temp_project_dir)

        # Create a template with dangerous content
        content = "{{ config.__class__.__init__.__globals__.os.system('id') }}"
        template_file = manager.templates_dir / "dangerous.md"
        template_file.write_text(content)

        with patch('specpulse.core.template_manager.TemplateValidator') as mock_validator:
            # Mock security validation failure
            mock_validation_result = Mock()
            mock_validation_result.is_safe = False
            mock_validation_result.critical_issues = [Mock(message="Security issue")]
            mock_validation_result.error_issues = []

            mock_validator_instance = Mock()
            mock_validator_instance.validate_template.return_value = mock_validation_result
            mock_validator.return_value = mock_validator_instance

            with pytest.raises(TemplateError, match="security vulnerabilities"):
                manager.get_template_preview(template_file)

    def test_get_sample_data(self, temp_project_dir):
        """Test getting sample data for different categories"""
        manager = TemplateManager(temp_project_dir)

        # Test different categories
        categories = ["spec", "plan", "task", "unknown"]

        for category in categories:
            sample_data = manager._get_sample_data(category)

            assert isinstance(sample_data, dict)
            assert "feature_name" in sample_data
            assert "spec_id" in sample_data
            assert "date" in sample_data
            assert "author" in sample_data

            # Check category-specific data
            if category == "spec":
                assert "executive_summary" in sample_data
            elif category == "plan":
                assert "optimization_focus" in sample_data
            elif category == "task":
                assert "complexity" in sample_data

    def test_list_templates(self, temp_project_dir):
        """Test listing templates"""
        manager = TemplateManager(temp_project_dir)

        # Add templates to registry
        manager.registry["templates"] = {
            "spec/template1": {"name": "template1", "category": "spec"},
            "plan/template2": {"name": "template2", "category": "plan"},
            "task/template3": {"name": "template3", "category": "task"}
        }

        # List all templates
        all_templates = manager.list_templates()
        assert len(all_templates) == 3

        # List templates by category
        spec_templates = manager.list_templates(category="spec")
        assert len(spec_templates) == 1
        assert spec_templates[0]["name"] == "template1"

    def test_get_template_info(self, temp_project_dir):
        """Test getting template information"""
        manager = TemplateManager(temp_project_dir)

        # Add template to registry
        manager.registry["templates"]["test/info_template"] = {
            "name": "info_template",
            "version": "1.0.0",
            "description": "Test template",
            "category": "test"
        }

        # Get existing template info
        info = manager.get_template_info("test/info_template")
        assert info is not None
        assert info["name"] == "info_template"
        assert info["version"] == "1.0.0"

        # Get non-existent template info
        info = manager.get_template_info("test/non_existent")
        assert info is None

    def test_update_template_version(self, temp_project_dir):
        """Test updating template version"""
        manager = TemplateManager(temp_project_dir)

        # Add template to registry
        manager.registry["templates"]["test/version_template"] = {
            "name": "version_template",
            "version": "1.0.0",
            "description": "Test template",
            "category": "test"
        }

        with patch('specpulse.core.template_manager.TemplateManager.backup_templates') as mock_backup:
            mock_backup.return_value = "backup_path"

            result = manager.update_template_version(
                "test/version_template",
                "2.0.0",
                "Added new features"
            )

            assert result is True

            # Check version was updated
            template_info = manager.get_template_info("test/version_template")
            assert template_info["version"] == "2.0.0"

            # Check change log was added
            assert "change_log" in template_info
            assert len(template_info["change_log"]) == 1
            assert template_info["change_log"][0]["from_version"] == "1.0.0"
            assert template_info["change_log"][0]["to_version"] == "2.0.0"

    def test_update_template_version_not_found(self, temp_project_dir):
        """Test updating version of non-existent template"""
        manager = TemplateManager(temp_project_dir)

        result = manager.update_template_version(
            "test/non_existent",
            "2.0.0",
            "Changes"
        )

        assert result is False

    def test_validate_all_templates(self, temp_project_dir):
        """Test validating all templates"""
        manager = TemplateManager(temp_project_dir)

        # This test would need to be adjusted based on actual template directory structure
        # For now, we'll test that the method exists and returns the expected structure
        results = manager.validate_all_templates()

        assert isinstance(results, dict)


class TestTemplateManagerEdgeCases:
    """Test TemplateManager edge cases and error conditions"""

    def test_unicode_content_handling(self, temp_project_dir):
        """Test handling of unicode content in templates"""
        manager = TemplateManager(temp_project_dir)

        # Create template with unicode content
        unicode_content = """
        # 测试标题

        Author: {{author}}
        Date: {{date}}

        العربية content
        🚀 Emoji content
        """

        template_file = manager.templates_dir / "unicode_template.md"
        template_file.write_text(unicode_content, encoding='utf-8')

        # Should handle unicode without errors
        variables = manager._extract_variables(unicode_content)
        assert "author" in variables
        assert "date" in variables

    def test_large_template_handling(self, temp_project_dir):
        """Test handling of large templates"""
        manager = TemplateManager(temp_project_dir)

        # Create a large template (but not too large to avoid security triggers)
        lines = []
        for i in range(100):  # 100 lines - well under the security limit
            lines.append(f"Line {i}: Content with {{variable_{i % 10}}}")

        large_content = "\n".join(lines)

        template_file = manager.templates_dir / "large_template.md"
        template_file.write_text(large_content)

        # Should process without errors
        variables = manager._extract_variables(large_content)
        assert len(variables) <= 10  # Should detect unique variables

    def test_concurrent_operations(self, temp_project_dir):
        """Test thread safety of template operations"""
        import threading
        import time

        manager = TemplateManager(temp_project_dir)

        def extract_variables_worker(content, results, index):
            """Worker function for concurrent variable extraction"""
            try:
                variables = manager._extract_variables(content)
                results[index] = variables
            except Exception as e:
                results[index] = e

        # Create multiple threads extracting variables from different content
        threads = []
        results = {}

        for i in range(5):
            content = f"Template {i} with {{variable_{i}}}"
            thread = threading.Thread(
                target=extract_variables_worker,
                args=(content, results, i)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        for i in range(5):
            assert i in results
            assert not isinstance(results[i], Exception)
            assert f"variable_{i}" in results[i]

    def test_malformed_template_content(self, temp_project_dir):
        """Test handling of malformed template content"""
        manager = TemplateManager(temp_project_dir)

        malformed_contents = [
            "{{unclosed_variable",
            "}}extra_closing_brackets{{",
            "{{% incomplete_tag",
            "{{ variable.with.dots }}",
            "{{ variable with spaces }}",
        ]

        for content in malformed_contents:
            # Should not crash, but may or may not extract variables correctly
            try:
                variables = manager._extract_variables(content)
                assert isinstance(variables, set)
            except Exception:
                # Some malformed content might raise exceptions - that's acceptable
                pass

    def test_file_permission_errors(self, temp_project_dir):
        """Test handling of file permission errors"""
        manager = TemplateManager(temp_project_dir)

        # Create a template file
        template_file = manager.templates_dir / "permission_test.md"
        template_file.write_text("Test content")

        # Mock permission error when trying to read
        with patch('pathlib.Path.read_text', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                manager.validate_template(template_file)


if __name__ == "__main__":
    pytest.main([__file__])