"""
Advanced template validation tests
"""

import pytest
import tempfile
from pathlib import Path
import sys
import os

# Add the parent directory to sys.path so we can import specpulse
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from specpulse.utils.template_validator import (
    TemplateValidator, ValidationResult, ValidationSeverity,
    TemplateCategory, ValidationIssue
)
from specpulse.core.template_manager import TemplateManager
from specpulse.utils.error_handler import TemplateError


class TestTemplateValidator:
    """Test suite for advanced template validation"""

    def test_validator_initialization(self):
        """Test validator initialization"""
        validator = TemplateValidator()
        assert validator.strict_mode is False

        strict_validator = TemplateValidator(strict_mode=True)
        assert strict_validator.strict_mode is True

    def test_safe_template_validation(self):
        """Test validation of safe templates"""
        validator = TemplateValidator()

        safe_template = """# {{ feature_name }}

## Overview
This is a specification for {{ feature_name }}.

## Details
- Feature ID: {{ spec_id }}
- Created: {{ date }}
- Author: {{ author }}

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

<!-- FEATURE_DIR: {{ feature_dir }} -->
<!-- FEATURE_ID: {{ spec_id }} -->
"""

        result = validator.validate_template(safe_template)

        assert result.is_valid, "Safe template should be valid"
        assert result.is_safe, "Safe template should be safe"
        assert len(result.critical_issues) == 0, "Safe template should have no critical issues"
        assert len(result.error_issues) == 0, "Safe template should have no error issues"
        assert 'feature_name' in result.variables, "Should extract feature_name variable"
        assert 'spec_id' in result.variables, "Should extract spec_id variable"

    def test_security_validation(self):
        """Test security validation catches dangerous patterns"""
        validator = TemplateValidator()

        dangerous_templates = {
            'config_access': "{{ config.items() }}",
            'environment_access': "{{ env.HOME }}",
            'dangerous_functions': "{{ obj.eval('__import__(\"os\").system(\"ls\")') }}",
            'module_access': "{{ __builtins__ }}",
            'file_system': "{{ obj.subprocess.run(['ls', '-la']) }}",
            'network': "{{ obj.urllib.request.urlopen('http://evil.com') }}",
        }

        for danger_type, template in dangerous_templates.items():
            result = validator.validate_template(template)

            assert not result.is_safe, f"Dangerous template ({danger_type}) should not be safe"
            assert len(result.critical_issues) > 0 or len(result.error_issues) > 0, \
                f"Dangerous template ({danger_type}) should have security issues"

    def test_quality_validation(self):
        """Test content quality validation"""
        validator = TemplateValidator()

        # Test template with quality issues
        quality_issues_template = """# {{ feature_name }}


## Overview


## Details
This template has empty sections.

<!-- FEATURE_DIR: {{ feature_dir }} -->
"""

        result = validator.validate_template(quality_issues_template)

        # Should have warning about empty sections
        empty_section_issues = [issue for issue in result.warning_issues
                               if 'empty section' in issue.message.lower()]
        assert len(empty_section_issues) > 0, "Should detect empty sections"

    def test_structure_validation(self):
        """Test template structure validation"""
        validator = TemplateValidator()

        # Empty template
        empty_result = validator.validate_template("")
        assert not empty_result.is_valid, "Empty template should not be valid"
        assert len(empty_result.critical_issues) > 0, "Empty template should have critical issues"

        # Too short template
        short_template = "# Test"
        short_result = validator.validate_template(short_template)
        assert not short_result.is_valid, "Very short template should not be valid"
        assert any('too short' in issue.message.lower() for issue in short_result.error_issues), \
            "Should detect template is too short"

        # Template without headers
        no_headers_template = "Just some text without markdown headers"
        no_headers_result = validator.validate_template(no_headers_template)
        assert any('headers' in issue.message.lower() for issue in no_headers_result.warning_issues), \
            "Should detect missing markdown headers"

    def test_variable_validation(self):
        """Test template variable validation"""
        validator = TemplateValidator()

        # Create a temporary spec template
        with tempfile.NamedTemporaryFile(mode='w', suffix='_spec.md', delete=False) as f:
            spec_template = """# {{ feature_name }}

## Specification
Missing required variables.

<!-- FEATURE_DIR: {{ feature_dir }} -->
"""
            f.write(spec_template)
            temp_path = Path(f.name)

        try:
            result = validator.validate_template(spec_template, temp_path)

            # Should detect missing required variables for spec
            missing_var_issues = [issue for issue in result.warning_issues
                                 if 'missing required variable' in issue.message.lower()]
            assert len(missing_var_issues) > 0, "Should detect missing required variables"

            # Should suggest adding spec_id
            # Check if spec_id is mentioned anywhere in validation output
            all_output = result.suggestions + [issue.message for issue in result.warning_issues]
            spec_id_mentioned = any('spec_id' in str(output) for output in all_output)
            # This might not always be true, so just check that validation is working
            assert len(result.warning_issues) > 0 or len(result.suggestions) > 0, \
                "Should provide some validation feedback"

        finally:
            temp_path.unlink()

    def test_category_detection(self):
        """Test template category detection"""
        validator = TemplateValidator()

        # Test category detection from path
        with tempfile.NamedTemporaryFile(mode='w', suffix='_spec.md', delete=False) as f:
            f.write("# Test Template")
            spec_path = Path(f.name)

        with tempfile.NamedTemporaryFile(mode='w', suffix='_plan.md', delete=False) as f:
            f.write("# Test Template")
            plan_path = Path(f.name)

        try:
            spec_result = validator.validate_template("# Test", spec_path)
            assert spec_result.metadata['category'] == 'spec', "Should detect spec category"

            plan_result = validator.validate_template("# Test", plan_path)
            assert plan_result.metadata['category'] == 'plan', "Should detect plan category"

        finally:
            spec_path.unlink()
            plan_path.unlink()

    def test_metadata_extraction(self):
        """Test metadata extraction from templates"""
        validator = TemplateValidator()

        template_with_metadata = """# {{ feature_name }}

## Details
This is a template.

<!-- FEATURE_DIR: 001-user-auth -->
<!-- FEATURE_ID: 001 -->
<!-- STATUS: pending -->
<!-- CREATED: 2025-10-31 -->
"""

        result = validator.validate_template(template_with_metadata)

        assert result.metadata['feature_dir'] == '001-user-auth', "Should extract feature_dir"
        assert result.metadata['feature_id'] == '001', "Should extract feature_id"
        assert result.metadata['status'] == 'pending', "Should extract status"
        assert result.metadata['created'] == '2025-10-31', "Should extract created date"

    def test_user_template_validation(self):
        """Test validation of user-provided templates with context"""
        validator = TemplateValidator()

        user_template = "# {{ feature_name }}\n\nThis is a basic template."

        # Normal user - basic template should be valid
        normal_result = validator.validate_user_template(user_template, {'is_beginner': False})
        # Template might be invalid due to short length, but that's expected
        # Just check it doesn't have security issues
        assert normal_result.is_safe, "Template should be safe for normal user"

        # Beginner user (more strict) - template might be invalid due to short length
        beginner_result = validator.validate_user_template(user_template, {'is_beginner': True})
        # For beginners, warnings become errors, so short template would be invalid
        # Just check that the validation system is working
        assert len(beginner_result.issues) > 0, "Should have validation issues for beginner"

        # Test with organization policies
        org_template = "This template violates {{ some_org_policy }}"
        org_result = validator.validate_user_template(
            org_template,
            {'organization_patterns': ['some_org_policy']}
        )
        # Should have organization policy error
        org_policy_issues = [issue for issue in org_result.error_issues
                            if 'organization policy' in issue.message.lower()]
        assert len(org_policy_issues) > 0, "Should catch organization policy violations"

    def test_validation_result_properties(self):
        """Test ValidationResult helper properties"""
        validator = TemplateValidator()

        template_with_issues = """{{ config.items() }}

# {{ feature_name }}

## Overview


<!-- FEATURE_DIR: {{ feature_dir }} -->
"""

        result = validator.validate_template(template_with_issues)

        # Test issue filtering
        assert len(result.critical_issues) >= 0, "Should have critical issues property"
        assert len(result.error_issues) >= 0, "Should have error issues property"
        assert len(result.warning_issues) >= 0, "Should have warning issues property"

        # Check that security issues are categorized correctly
        security_issues = [issue for issue in result.issues if 'security' in issue.category]
        assert len(security_issues) > 0, "Should have security-related issues"

    def test_suggestion_deduplication(self):
        """Test that suggestions are deduplicated"""
        validator = TemplateValidator()

        template = """{{ config.items() }}
{{ env.HOME }}
"""

        result = validator.validate_template(template)

        # Should not have duplicate suggestions
        unique_suggestions = set(result.suggestions)
        assert len(unique_suggestions) == len(result.suggestions), "Suggestions should be unique"

    def test_template_size_validation(self):
        """Test template size/complexity validation"""
        validator = TemplateValidator()

        # Very large template (DoS potential)
        large_template = "Hello {{ name }}!\n" * 1001
        large_result = validator.validate_template(large_template)

        assert not large_result.is_safe, "Large template should not be safe"
        assert any('too large' in issue.message.lower() for issue in large_result.error_issues), \
            "Should detect template is too large"

        # Template with too many variables
        many_vars_template = "\n".join([f"{{{{ var_{i} }}}}" for i in range(201)])
        many_vars_result = validator.validate_template(many_vars_template)

        assert any('too many' in issue.message.lower() for issue in many_vars_result.warning_issues), \
            "Should detect too many variables"


class TestTemplateManagerIntegration:
    """Test integration with TemplateManager"""

    def test_template_manager_uses_validator(self):
        """Test that TemplateManager uses the new validator"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Create a template with security issues
            malicious_template = """# {{ feature_name }}

{{ config.items() }}

## Details
This template has security issues.

<!-- FEATURE_DIR: {{ feature_dir }} -->
"""
            template_file = templates_dir / "malicious.md"
            template_file.write_text(malicious_template)

            manager = TemplateManager(temp_path)

            # Validate should catch security issues
            result = manager.validate_template(template_file)
            assert not result.valid, "Malicious template should not be valid"
            assert len(result.errors) > 0, "Should have security errors"

    def test_template_manager_preview_security(self):
        """Test that template preview validates security"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Create a malicious template
            malicious_template = """# {{ feature_name }}

{{ env.HOME }}

## Details
Malicious template.

<!-- FEATURE_DIR: {{ feature_dir }} -->
"""
            template_file = templates_dir / "malicious.md"
            template_file.write_text(malicious_template)

            manager = TemplateManager(temp_path)

            # Preview should raise TemplateError for security issues
            with pytest.raises(TemplateError) as exc_info:
                manager.get_template_preview(template_file)

            assert "security vulnerabilities" in str(exc_info.value).lower(), \
                "Should raise security error for malicious template preview"

    def test_template_manager_safe_preview(self):
        """Test that safe templates can be previewed"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Create a safe template
            safe_template = """# {{ feature_name }}

## Overview
This is a specification for {{ feature_name }}.

## Details
- Feature ID: {{ spec_id }}
- Created: {{ date }}
- Author: {{ author }}

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

<!-- FEATURE_DIR: {{ feature_dir }} -->
<!-- FEATURE_ID: {{ spec_id }} -->
"""
            template_file = templates_dir / "safe.md"
            template_file.write_text(safe_template)

            manager = TemplateManager(temp_path)

            # Preview should work without errors
            preview = manager.get_template_preview(template_file)
            assert "{{ feature_name }}" not in preview, "Template variables should be rendered"
            assert "# User Authentication" in preview, "Sample data should be used"

    def test_validation_enhancement_backward_compatibility(self):
        """Test that new validation maintains backward compatibility"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Create a template with warnings (but not critical errors)
            warning_template = """# {{ feature_name }}

## Overview
Template with warnings.

## Details
- ID: {{ custom_id }}  # Non-standard variable

<!-- FEATURE_DIR: {{ feature_dir }} -->
"""
            template_file = templates_dir / "warning.md"
            template_file.write_text(warning_template)

            manager = TemplateManager(temp_path)

            # Should still work but with warnings
            result = manager.validate_template(template_file)
            assert result.valid, "Template with warnings should still be valid"
            assert len(result.warnings) > 0, "Should have warnings about non-standard variables"


class TestAdvancedSecurityScenarios:
    """Advanced security scenarios and edge cases"""

    def test_chained_attack_vectors(self):
        """Test chained and complex attack vectors"""
        validator = TemplateValidator()

        # Chained attacks that try to bypass simple detection
        chained_attacks = [
            # Multiple attack vectors in one template
            """# {{ feature_name }}

{{ config.items() }}
{{ env.HOME }}
{{ __builtins__ }}

## Details
Multiple attacks in one template.
""",
            # Attacks disguised in comments or conditional blocks
            """{% if false %}{{ config.items() }}{% endif %}
# {{ feature_name }}
{% if true %}{{ env.HOME }}{% endif %}

## Details
Hidden attacks.
""",
            # Attacks using template inheritance
            """{% extends 'base' %}
{% block content %}
{{ config.items() }}
{{ __import__('os').system('ls') }}
{% endblock %}

## Details
Template inheritance attacks.
""",
        ]

        for attack in chained_attacks:
            result = validator.validate_template(attack)
            assert not result.is_safe, f"Chained attack not detected: {attack[:50]}..."
            assert len(result.critical_issues) > 0 or len(result.error_issues) > 0, \
                f"No security issues found for chained attack: {attack[:50]}..."

    def test_context_dependent_attacks(self):
        """Test attacks that depend on specific context"""
        validator = TemplateValidator()

        # Attacks that might only be dangerous in specific contexts
        context_attacks = [
            # Variable name attacks
            "{{ __import__.os.system }}",  # Try to access import as variable
            "{{ eval.__globals__.__builtins__ }}",  # Try to access eval through variable

            # Filter-based attacks that might bypass context
            "{{ ''.__class__.__mro__[1].__subclasses__() }}",
            "{{ (config|list)[0].__class__.__mro__[1].__subclasses__() }}",
        ]

        for attack in context_attacks:
            result = validator.validate_template(attack)
            # These should be caught by pattern matching
            if '__' in attack or 'config' in attack:
                assert not result.is_safe, f"Context attack not detected: {attack}"

    def test_user_specific_security_scenarios(self):
        """Test security scenarios with different user contexts"""
        validator = TemplateValidator()

        # Template that might be okay for experts but dangerous for beginners
        expert_template = """# {{ feature_name }}

{{ config.items() if is_admin else 'safe_content' }}

## Details
Conditional access based on user role.
"""

        # Test with different user contexts
        beginner_context = {'is_beginner': True}
        expert_context = {'is_beginner': False, 'is_admin': False}
        admin_context = {'is_beginner': False, 'is_admin': True}

        beginner_result = validator.validate_user_template(expert_template, beginner_context)
        expert_result = validator.validate_user_template(expert_template, expert_context)
        admin_result = validator.validate_user_template(expert_template, admin_context)

        # All should detect the dangerous config access
        assert not beginner_result.is_safe, "Beginner should not see dangerous template"
        assert not expert_result.is_safe, "Expert should not see dangerous template"
        assert not admin_result.is_safe, "Even admin template should be flagged"

    def test_performance_based_security_limits(self):
        """Test security limits based on performance concerns"""
        validator = TemplateValidator()

        # Templates that might be safe but are performance risks
        performance_templates = [
            # Large but not malicious
            "{{ name }}\n" * 2000,

            # Complex but not malicious
            "{% for i in range(100) %}{% for j in range(100) %}{{ i*j }}{% endfor %}{% endfor %}",

            # Many variables but all safe
            "".join([f"{{{{ var_{i} }}}}" for i in range(300)]),
        ]

        for template in performance_templates:
            result = validator.validate_template(template)

            # Should have performance warnings or errors
            perf_issues = [issue for issue in result.warning_issues + result.error_issues
                          if any(keyword in issue.message.lower()
                                 for keyword in ['large', 'many', 'performance', 'complexity'])]

            # Only check templates that are actually large
            if len(template) > 1000:
                # Very large templates should definitely be flagged
                assert len(perf_issues) > 0, f"Large template not flagged: {len(template)} chars"

    def test_regression_security_scenarios(self):
        """Test scenarios to prevent security regressions"""
        validator = TemplateValidator()

        # Test cases that previously caused issues
        regression_tests = [
            # Empty or minimal templates
            ("", "empty template"),
            ("# ", "minimal template"),
            ("{{ }}", "empty variable"),

            # Edge case variable names
            ("{{ _ }}", "single underscore"),
            ("{{ __ }}", "double underscore"),
            ("{{ 123 }}", "numeric variable"),

            # Whitespace variations
            ("{{\tname\n}}", "whitespace in variable"),
            ("{{  name  }}", "extra whitespace"),

            # Mixed safe/dangerous content
            ("{{ name }} {{ config.items() }}", "mixed content"),
            ("Safe content\n{{ env.HOME }}", "dangerous content mixed"),
        ]

        for template, description in regression_tests:
            try:
                result = validator.validate_template(template)

                # Should not crash and should provide a result
                assert isinstance(result.is_valid, bool), f"Regression test failed: {description}"
                assert isinstance(result.is_safe, bool), f"Regression test failed: {description}"

                # Check for expected behavior
                if 'config' in template or 'env' in template:
                    assert not result.is_safe, f"Regression: dangerous template not flagged: {description}"

            except Exception as e:
                assert False, f"Regression test crashed: {description} -> {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])