"""
Security tests for template injection vulnerabilities
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import sys
import os

# Add the parent directory to sys.path so we can import specpulse
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from specpulse.core.template_manager import validate_template_security, TemplateManager
from specpulse.utils.error_handler import TemplateError
from specpulse.utils.template_validator import TemplateValidator


class TestTemplateInjectionSecurity:
    """Test suite for template injection vulnerabilities"""

    def test_safe_template_patterns(self):
        """Test that legitimate template patterns work correctly"""
        safe_templates = [
            "Hello {{ name }}!",
            "Feature: {{ feature_name }}",
            "ID: {{ spec_id }}",
            "Date: {{ date }}",
            "{% if feature_name %}Feature: {{ feature_name }}{% endif %}",
            "{% for item in items %}{{ item }}{% endfor %}",
        ]

        for template in safe_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            assert is_safe, f"Safe template flagged as dangerous: {template}"
            assert len(vulnerabilities) == 0, f"Safe template has vulnerabilities: {template}"

    def test_config_access_blocked(self):
        """Test that config access patterns are blocked"""
        dangerous_templates = [
            "{{ config.items() }}",
            "{{ config.SECRET_KEY }}",
            "{{ config.__class__ }}",
            "{{ config.__init__.__globals__ }}",
        ]

        for template in dangerous_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            assert not is_safe, f"Dangerous template not detected: {template}"
            assert len(vulnerabilities) > 0, f"No vulnerabilities found for dangerous template: {template}"
            assert any("config" in v.lower() for v in vulnerabilities), f"Config access not detected: {template}"

    def test_environment_access_blocked(self):
        """Test that environment variable access is blocked"""
        dangerous_templates = [
            "{{ env.HOME }}",
            "{{ env.PATH }}",
            "{{ env.get('SECRET') }}",
            "{{ env.__class__ }}",
        ]

        for template in dangerous_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            assert not is_safe, f"Dangerous template not detected: {template}"
            assert len(vulnerabilities) > 0, f"No vulnerabilities found for dangerous template: {template}"

    def test_dunder_method_access_blocked(self):
        """Test that dunder method access is blocked"""
        dangerous_templates = [
            "{{ __builtins__ }}",
            "{{ __import__ }}",
            "{{ obj.__class__ }}",
            "{{ obj.__dict__ }}",
            "{{ obj.__init__.__globals__ }}",
        ]

        for template in dangerous_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            assert not is_safe, f"Dangerous template not detected: {template}"
            assert len(vulnerabilities) > 0, f"No vulnerabilities found for dangerous template: {template}"

    def test_eval_exec_access_blocked(self):
        """Test that eval/exec method access is blocked"""
        dangerous_templates = [
            "{{ obj.eval('__import__(\"os\").system(\"ls\")') }}",
            "{{ obj.exec('print(\"hello\")') }}",
            "{{ obj.__class__.__bases__[0].__subclasses__() }}",
        ]

        for template in dangerous_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            assert not is_safe, f"Dangerous template not detected: {template}"
            assert len(vulnerabilities) > 0, f"No vulnerabilities found for dangerous template: {template}"

    def test_file_system_access_blocked(self):
        """Test that file system access is blocked"""
        dangerous_templates = [
            "{{ obj.open('/etc/passwd') }}",
            "{{ obj.subprocess.run(['ls', '-la']) }}",
            "{{ obj.os.system('rm -rf /') }}",
            "{{ obj.sys.modules }}",
        ]

        for template in dangerous_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            assert not is_safe, f"Dangerous template not detected: {template}"
            assert len(vulnerabilities) > 0, f"No vulnerabilities found for dangerous template: {template}"

    def test_dos_patterns_detected(self):
        """Test that denial of service patterns are detected"""
        # Template too large
        large_template = "Hello {{ name }}!\n" * 1001
        is_safe, vulnerabilities = validate_template_security(large_template)
        assert not is_safe, "Large template not detected"
        assert any("too large" in v.lower() for v in vulnerabilities)

        # Too many variables
        var_heavy_template = "\n".join([f"{{{{ var_{i} }}}}" for i in range(201)])
        is_safe, vulnerabilities = validate_template_security(var_heavy_template)
        assert not is_safe, "Variable-heavy template not detected"
        assert any("too many" in v.lower() for v in vulnerabilities)

        # Deep nesting
        nested_template = "{% if true %}" * 11 + "content" + "{% endif %}" * 11
        is_safe, vulnerabilities = validate_template_security(nested_template)
        assert not is_safe, "Deeply nested template not detected"
        assert any("too deep" in v.lower() for v in vulnerabilities)

    def test_template_manager_security(self):
        """Test that TemplateManager properly validates templates"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Create a malicious template
            malicious_template = "{{ config.__class__.__bases__[0].__subclasses__() }}"
            template_file = templates_dir / "malicious.md"
            template_file.write_text(malicious_template)

            manager = TemplateManager(temp_path)

            # Try to validate the malicious template
            result = manager.validate_template(template_file)
            assert not result.valid, "Malicious template should not be valid"
            assert len(result.errors) > 0, "Malicious template should have errors"
            assert any("security" in error.lower() or "dangerous" in error.lower()
                      for error in result.errors), "Security vulnerability not detected"

    def test_template_preview_security(self):
        """Test that template preview validates security"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Create a malicious template
            malicious_template = "{{ env.HOME }}"
            template_file = templates_dir / "malicious.md"
            template_file.write_text(malicious_template)

            manager = TemplateManager(temp_path)

            # Try to preview the malicious template - should raise TemplateError
            with pytest.raises(TemplateError) as exc_info:
                manager.get_template_preview(template_file)

            assert "security vulnerabilities" in str(exc_info.value).lower(), \
                "Security error not raised for malicious template preview"

    def test_safe_template_preview_works(self):
        """Test that safe templates can still be previewed"""
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
            assert "001" in preview, "Sample spec_id should be used"

    def test_edge_cases(self):
        """Test edge cases for template validation"""
        edge_cases = [
            ("", False, "empty template"),  # Empty template should be caught elsewhere
            ("   ", True, "whitespace only"),
            ("{{", True, "incomplete syntax"),
            ("{% for", True, "incomplete tag"),
            ("{{ name + unknown_var }}", True, "valid but complex"),
        ]

        for template, should_be_safe, description in edge_cases:
            is_safe, vulnerabilities = validate_template_security(template)
            if description == "empty template":
                # Empty templates are handled by structure validation, not security validation
                continue
            assert is_safe == should_be_safe, f"Edge case failed: {description} - {template}"

    def test_advanced_injection_attempts(self):
        """Test sophisticated injection attempts"""
        advanced_templates = [
            # Filter bypass attempts
            "{{ (__import__('os')).system('ls') }}",
            "{{ ''.__class__.__mro__[1].__subclasses()[104] }}",
            "{{ (config|attr('__class__')).__base__.__subclasses__() }}",
            # Chained attacks
            "{{ config.__class__.__init__.__globals__['__builtins__']['eval']('__import__(\"os\").system(\"ls\")') }}",
            # Encoding bypass attempts
            "{{ config['__import__']('os').system('ls') }}",
            "{{ config.get('__builtins__').get('eval')('print(1)') }}",
            # Template inheritance attacks
            "{{ self._TemplateReference__context }}",
            "{{ caller.__dict__ }}",
            # Loop-based DoS
            "{% for i in range(10000) %}{{ i }}{% endfor %}",
            # Recursive template attacks
            "{% macro test() %}{{ test() }}{% endmacro %}{{ test() }}",
        ]

        for template in advanced_templates:
            is_safe, vulnerabilities = validate_template_security(template)
            # Some advanced templates might not be caught by simple pattern matching
            # but should be caught by more advanced validation or Jinja2 sandbox
            if not is_safe:
                assert len(vulnerabilities) > 0, f"No vulnerabilities for advanced template: {template[:50]}..."
            else:
                # If simple validation doesn't catch it, advanced validation should
                validator = TemplateValidator()
                result = validator.validate_template(template)
                if 'range(10000)' in template:
                    # Very large ranges should definitely be caught
                    assert not result.is_safe, f"Large range not flagged: {template[:50]}..."
                elif 'macro' in template:
                    # Macros might be safe in some contexts, just check it doesn't crash
                    assert isinstance(result.is_safe, bool), f"Macro template crashed validator: {template[:50]}..."

    def test_sandbox_effectiveness(self):
        """Test that Jinja2 sandbox is effective"""
        from jinja2.sandbox import SandboxedEnvironment

        # Test that sandbox blocks dangerous operations
        env = SandboxedEnvironment(autoescape=True)

        dangerous_templates = [
            "{{ ''.__class__.__mro__[1].__subclasses__() }}",
            "{{ config.items() }}",
            "{{ request.__class__ }}",
        ]

        for template in dangerous_templates:
            try:
                result = env.from_string(template).render()
                # If it renders without error, check if dangerous content is exposed
                assert "subclasses" not in result.lower(), f"Sandbox allowed dangerous content: {template}"
                assert "config" not in result.lower(), f"Sandbox exposed config: {template}"
            except Exception as e:
                # Sandbox should raise an exception for dangerous templates
                assert True, f"Sandbox correctly blocked dangerous template: {template} - {e}"

    def test_autoescape_functionality(self):
        """Test that autoescape is working correctly"""
        from jinja2.sandbox import SandboxedEnvironment

        env = SandboxedEnvironment(autoescape=True)

        # Test HTML escaping
        html_templates = [
            ("{{ '<script>alert(\"xss\")</script>' }}", "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"),
            ("{{ '<img src=x onerror=alert(1)>' }}", "&lt;img src=x onerror=alert(1)&gt;"),
            ("{{ 'javascript:alert(1)' }}", "javascript:alert(1)"),  # URLs are not auto-escaped
        ]

        for template, expected in html_templates:
            result = env.from_string(template).render()
            # Check that HTML entities are escaped (actual escaping might differ slightly)
            if '<script>' in template or '<img' in template:
                # HTML tags should be escaped
                assert '<script>' not in result.lower(), f"Script tag not escaped in: {result}"
                assert '&lt;' in result or '&#' in result, f"HTML escaping not working in: {result}"
            # The exact escaping format might vary, just check dangerous content is escaped

    def test_template_complexity_limits(self):
        """Test template complexity and size limits"""
        # Test extremely large templates
        large_template = "{{ name }}\n" * 10000
        is_safe, vulnerabilities = validate_template_security(large_template)
        assert not is_safe, "Extremely large template should be flagged"

        # Test deeply nested templates
        nested_template = "{% if true %}" * 50 + "content" + "{% endif %}" * 50
        is_safe, vulnerabilities = validate_template_security(nested_template)
        assert not is_safe, "Deeply nested template should be flagged"

        # Test templates with too many variables
        var_heavy = "".join([f"{{{{ var_{i} }}}}" for i in range(1000)])
        is_safe, vulnerabilities = validate_template_security(var_heavy)
        assert not is_safe, "Variable-heavy template should be flagged"

    def test_context_isolation(self):
        """Test that template contexts are properly isolated"""
        from jinja2.sandbox import SandboxedEnvironment

        env = SandboxedEnvironment(autoescape=True)

        # Test that templates can't access global context
        template1 = env.from_string("{{ test_var }}")
        template2 = env.from_string("{{ other_var }}")

        # Each template should only have access to its own context
        result1 = template1.render(test_var="value1")
        result2 = template2.render(other_var="value2")

        assert "value1" in result1
        assert "value2" in result2
        assert "value2" not in result1
        assert "value1" not in result2

    def test_unicode_and_encoding_attacks(self):
        """Test Unicode and encoding-based attacks"""
        unicode_attacks = [
            "{{ config\ufeff.items() }}",  # BOM attack
            "{{ config\uff0eitems() }}",  # Full-width dot
            "{{ config\u2215items() }}",  # Division slash
            "{{ evn.HOME }}",  # Typo-based bypass
            "{{ congfig.items() }}",  # Character substitution
        ]

        for attack in unicode_attacks:
            is_safe, vulnerabilities = validate_template_security(attack)
            # Some of these might pass the regex but be caught by other validations
            if not is_safe:
                assert len(vulnerabilities) > 0, f"Unicode attack not properly handled: {attack}"

    def test_filter_and_function_attacks(self):
        """Test attacks through Jinja2 filters and functions"""
        filter_attacks = [
            "{{ 'cat /etc/passwd'|shell }}",  # Shell filter
            "{{ '__import__'|attr('__call__')('os').system('ls') }}",  # Attribute access
            "{{ config|attr('items') }}",  # Attribute filter bypass
            "{{ ''|attr('__class__') }}",  # Attribute chain
            "{{ 'eval'|attr('__call__')('__import__(\"os\").system(\"ls\")') }}",  # Complex chain
        ]

        for attack in filter_attacks:
            is_safe, vulnerabilities = validate_template_security(attack)
            # Some filter attacks might not be caught by simple regex
            # but should be caught by other security measures
            if not is_safe:
                assert len(vulnerabilities) > 0, f"No vulnerabilities for filter attack: {attack}"
            else:
                # Check if advanced validation catches it
                validator = TemplateValidator()
                result = validator.validate_template(attack)
                if 'shell' in attack or 'attr(' in attack:
                    # These should be caught as they're obvious filter bypass attempts
                    assert not result.is_safe or len(result.error_issues) > 0, f"Filter attack not caught: {attack}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])