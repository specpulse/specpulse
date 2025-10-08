"""
Pytest configuration and fixtures for SpecPulse tests.
"""
import pytest
from pathlib import Path


# Validation Test Fixtures

@pytest.fixture
def valid_spec_path():
    """Path to a complete, valid specification fixture."""
    return Path(__file__).parent / "fixtures" / "validation" / "valid_spec.md"


@pytest.fixture
def partial_spec_path():
    """Path to a partial (incomplete) specification fixture."""
    return Path(__file__).parent / "fixtures" / "validation" / "partial_spec.md"


@pytest.fixture
def invalid_spec_path():
    """Path to an invalid specification fixture."""
    return Path(__file__).parent / "fixtures" / "validation" / "invalid_spec.md"


@pytest.fixture
def valid_spec_content(valid_spec_path):
    """Content of the valid specification fixture."""
    return valid_spec_path.read_text()


@pytest.fixture
def partial_spec_content(partial_spec_path):
    """Content of the partial specification fixture."""
    return partial_spec_path.read_text()


@pytest.fixture
def invalid_spec_content(invalid_spec_path):
    """Content of the invalid specification fixture."""
    return invalid_spec_path.read_text()


@pytest.fixture
def validation_fixtures_dir():
    """Directory containing validation test fixtures."""
    return Path(__file__).parent / "fixtures" / "validation"


# Validation Test Markers

def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "validation: mark test as a validation test"
    )
    config.addinivalue_line(
        "markers", "partial_validation: mark test as a partial validation test"
    )
    config.addinivalue_line(
        "markers", "custom_rules: mark test as a custom validation rules test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance/benchmark test"
    )
