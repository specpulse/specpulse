"""
Mock Service Implementations for Testing

Provides mock implementations of all service interfaces for unit testing.

Usage in tests:
    >>> from tests.mocks.mock_services import MockTemplateProvider
    >>> mock_provider = MockTemplateProvider()
    >>> container.register(ITemplateProvider, mock_provider)
    >>> # Now test CLI commands with mocked services
"""

from typing import Dict, List, Optional
from pathlib import Path


class MockTemplateProvider:
    """Mock implementation of ITemplateProvider"""

    def __init__(self, spec_template: str = "# Mock Spec", plan_template: str = "# Mock Plan"):
        self.spec_template = spec_template
        self.plan_template = plan_template
        self.task_template = "# Mock Task"
        self.call_log = []

    def get_spec_template(self) -> str:
        self.call_log.append('get_spec_template')
        return self.spec_template

    def get_plan_template(self) -> str:
        self.call_log.append('get_plan_template')
        return self.plan_template

    def get_task_template(self) -> str:
        self.call_log.append('get_task_template')
        return self.task_template

    def get_template(self, template_name: str, variables: Optional[Dict] = None) -> str:
        self.call_log.append(f'get_template:{template_name}')
        return f"# Mock {template_name}"

    def get_decomposition_template(self, template_type: str) -> str:
        return "# Mock Decomposition"

    def get_microservice_template(self) -> str:
        return "# Mock Microservice"

    def get_api_contract_template(self) -> str:
        return "# Mock API Contract"

    def get_interface_template(self) -> str:
        return "# Mock Interface"

    def get_service_plan_template(self) -> str:
        return "# Mock Service Plan"

    def get_integration_plan_template(self) -> str:
        return "# Mock Integration Plan"


class MockMemoryProvider:
    """Mock implementation of IMemoryProvider"""

    def __init__(self):
        self.call_log = []

    def get_constitution_template(self) -> str:
        self.call_log.append('get_constitution_template')
        return "# Mock Constitution"

    def get_context_template(self) -> str:
        self.call_log.append('get_context_template')
        return "# Mock Context"

    def get_decisions_template(self) -> str:
        self.call_log.append('get_decisions_template')
        return "# Mock Decisions"


class MockScriptGenerator:
    """Mock implementation of IScriptGenerator"""

    def __init__(self):
        self.call_log = []

    def get_setup_script(self) -> str:
        return "#!/bin/bash\necho 'mock setup'"

    def get_spec_script(self) -> str:
        return "#!/bin/bash\necho 'mock spec'"

    def get_plan_script(self) -> str:
        return "#!/bin/bash\necho 'mock plan'"

    def get_task_script(self) -> str:
        return "#!/bin/bash\necho 'mock task'"

    def get_validate_script(self) -> str:
        return "#!/bin/bash\necho 'mock validate'"

    def get_generate_script(self) -> str:
        return "#!/bin/bash\necho 'mock generate'"


class MockAIInstructionProvider:
    """Mock implementation of IAIInstructionProvider"""

    def __init__(self):
        self.call_log = []

    def get_claude_instructions(self) -> str:
        return "# Mock Claude Instructions"

    def get_gemini_instructions(self) -> str:
        return "# Mock Gemini Instructions"

    def get_claude_pulse_command(self) -> str:
        return "# Mock Claude Pulse"

    def get_claude_spec_command(self) -> str:
        return "# Mock Claude Spec"

    def get_claude_plan_command(self) -> str:
        return "# Mock Claude Plan"

    def get_claude_task_command(self) -> str:
        return "# Mock Claude Task"

    def get_claude_execute_command(self) -> str:
        return "# Mock Claude Execute"

    def get_claude_validate_command(self) -> str:
        return "# Mock Claude Validate"

    def get_claude_decompose_command(self) -> str:
        return "# Mock Claude Decompose"

    def get_gemini_pulse_command(self) -> str:
        return "# Mock Gemini Pulse"

    def get_gemini_spec_command(self) -> str:
        return "# Mock Gemini Spec"

    def get_gemini_plan_command(self) -> str:
        return "# Mock Gemini Plan"

    def get_gemini_task_command(self) -> str:
        return "# Mock Gemini Task"

    def get_gemini_execute_command(self) -> str:
        return "# Mock Gemini Execute"

    def get_gemini_validate_command(self) -> str:
        return "# Mock Gemini Validate"

    def get_gemini_decompose_command(self) -> str:
        return "# Mock Gemini Decompose"

    def generate_claude_commands(self) -> List[Dict]:
        return [{"name": "mock-command", "description": "Mock", "content": "# Mock"}]

    def generate_gemini_commands(self) -> List[Dict]:
        return [{"name": "mock-command", "description": "Mock", "content": "# Mock"}]


class MockDecompositionService:
    """Mock implementation of IDecompositionService"""

    def __init__(self):
        self.call_log = []

    def decompose_specification(self, spec_dir: Path, spec_content: str) -> Dict:
        self.call_log.append('decompose_specification')
        return {
            "services": ["mock-service-1", "mock-service-2"],
            "api_contracts": [],
            "interfaces": [],
            "integration_points": [],
            "status": "success"
        }

    def get_microservice_template(self) -> str:
        return "# Mock Microservice"

    def get_api_contract_template(self) -> str:
        return "# Mock API"

    def get_interface_template(self) -> str:
        return "# Mock Interface"

    def get_service_plan_template(self) -> str:
        return "# Mock Service Plan"

    def get_integration_plan_template(self) -> str:
        return "# Mock Integration"

    def get_decomposition_template(self, template_name: str) -> str:
        return f"# Mock {template_name}"


__all__ = [
    'MockTemplateProvider',
    'MockMemoryProvider',
    'MockScriptGenerator',
    'MockAIInstructionProvider',
    'MockDecompositionService',
]
