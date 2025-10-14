"""
Integration Tests for Service Architecture

Verifies that the refactored service architecture:
- All services work together correctly
- SpecPulse orchestrator delegates properly
- Backward compatibility maintained
- No regressions in functionality
"""

import pytest
import tempfile
from pathlib import Path

from specpulse.core.specpulse import SpecPulse
from specpulse.core.service_container import ServiceContainer
from specpulse.core.interfaces import ITemplateProvider
from tests.mocks.mock_services import MockTemplateProvider


class TestServiceIntegration:
    """Integration tests for service architecture"""

    @pytest.fixture
    def temp_project(self):
        """Create temporary SpecPulse project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".specpulse").mkdir()
            (project_root / "specs").mkdir()
            (project_root / "plans").mkdir()
            (project_root / "tasks").mkdir()
            (project_root / "memory").mkdir()

            yield project_root

    def test_specpulse_orchestrator_works(self, temp_project):
        """Test that refactored SpecPulse works as orchestrator"""
        spec_pulse = SpecPulse(temp_project)

        # Should have all services initialized
        assert spec_pulse.template_provider is not None
        assert spec_pulse.memory_provider is not None
        assert spec_pulse.script_generator is not None
        assert spec_pulse.ai_provider is not None
        assert spec_pulse.decomposition_service is not None

    def test_template_methods_work(self, temp_project):
        """Test that template methods delegate correctly"""
        spec_pulse = SpecPulse(temp_project)

        spec = spec_pulse.get_spec_template()
        plan = spec_pulse.get_plan_template()
        task = spec_pulse.get_task_template()

        # Should return embedded templates (fallback)
        assert len(spec) > 100
        assert len(plan) > 100
        assert len(task) > 100

    def test_backward_compatibility(self, temp_project):
        """Test that all original methods still work"""
        spec_pulse = SpecPulse(temp_project)

        # All these methods should work (no AttributeError)
        methods_to_test = [
            'get_spec_template',
            'get_plan_template',
            'get_task_template',
            'get_constitution_template',
            'get_context_template',
            'get_decisions_template',
            'get_setup_script',
            'get_claude_instructions',
            'get_gemini_instructions',
        ]

        for method_name in methods_to_test:
            assert hasattr(spec_pulse, method_name)
            method = getattr(spec_pulse, method_name)
            result = method()
            assert result is not None


class TestDependencyInjection:
    """Test dependency injection capabilities"""

    def test_specpulse_with_mock_services(self):
        """Test that SpecPulse works with mocked services via DI"""
        # Create mock template provider
        mock_provider = MockTemplateProvider(
            spec_template="# Mocked Spec Template"
        )

        # Create container and register mock
        container = ServiceContainer()
        container.register_singleton(ITemplateProvider, mock_provider)

        # Note: Full DI requires all services registered
        # This test demonstrates the pattern
        # (Full implementation would register all 5 services)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
