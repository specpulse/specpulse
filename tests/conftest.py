"""
SpecPulse Test Configuration and Fixtures

This module provides shared fixtures and configuration for all SpecPulse tests.
Designed for 100% coverage and comprehensive testing.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import yaml
import json
from datetime import datetime

from specpulse.core.specpulse import SpecPulse
from specpulse.core.service_container import ServiceContainer
from specpulse.core.path_manager import PathManager
from specpulse.models.project_context import ProjectContext


@pytest.fixture(scope="session")
def test_data_dir():
    """Get the test data directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing"""
    temp_dir = Path(tempfile.mkdtemp(prefix="specpulse_test_"))

    # Create basic SpecPulse structure
    specpulse_dir = temp_dir / ".specpulse"
    specpulse_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    for subdir in ["specs", "plans", "tasks", "memory", "templates", "docs", "cache"]:
        (specpulse_dir / subdir).mkdir(exist_ok=True)

    # Create config file
    config = {
        "version": "2.6.0",
        "created": datetime.now().isoformat(),
        "project": {
            "name": "test-project",
            "type": "web",
            "created": datetime.now().isoformat()
        },
        "ai": {
            "primary": "claude"
        },
        "conventions": {
            "branch_naming": "{number:03d}-{feature-name}",
            "plan_naming": "plan-{number:03d}.md",
            "spec_naming": "spec-{number:03d}.md",
            "task_naming": "task-{number:03d}.md"
        },
        "templates": {
            "spec": ".specpulse/templates/spec.md",
            "plan": ".specpulse/templates/plan.md",
            "task": ".specpulse/templates/task.md"
        }
    }

    with open(specpulse_dir / "config.yaml", "w") as f:
        yaml.dump(config, f)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_spec_content():
    """Sample specification content for testing"""
    return """# Specification: User Authentication System

<!-- FEATURE_DIR: 001-user-auth -->
<!-- FEATURE_ID: 001 -->
<!-- SPEC_NUMBER: 001 -->
<!-- STATUS: pending -->
<!-- CREATED: 2025-01-01T00:00:00 -->

## Description
Implement a comprehensive user authentication system with secure login, registration, and password management.

## Requirements

### Functional Requirements

#### 1. User Registration
- Users can register with email and password
- Email verification required
- Password strength validation
- Duplicate email prevention

#### 2. User Authentication
- Secure login with email/password
- Session management
- Password reset functionality
- Remember me option

#### 3. Security Features
- Password hashing (bcrypt)
- Rate limiting on login attempts
- Account lockout after failed attempts
- CSRF protection

## Acceptance Criteria

1. Users can register with valid email and strong password
2. Users can login with correct credentials
3. Invalid login attempts are rate limited
4. Password reset emails are sent securely
5. Sessions expire after inactivity
"""


@pytest.fixture
def sample_plan_content():
    """Sample plan content for testing"""
    return """# Implementation Plan: User Authentication System

## Overview
This plan outlines the implementation of a secure user authentication system following Specification 001.

## Implementation Phases

### Phase 1: Database Setup (Days 1-2)
1. Design user table schema
2. Create database migration
3. Set up database indexes
4. Implement password hashing utilities

### Phase 2: Backend API (Days 3-5)
1. Implement user registration endpoint
2. Implement login endpoint
3. Add password reset functionality
4. Add session management

## Success Criteria
1. All API endpoints respond correctly
2. Security tests pass
3. Performance benchmarks met
4. Documentation is complete
5. Code coverage > 90%
"""


@pytest.fixture
def sample_task_content():
    """Sample task content for testing"""
    return """# Task List: User Authentication System

## Phase 1: Database Setup

### Task 1.1: Design Database Schema
**Priority:** High
**Estimated:** 4 hours

#### Description
Design and implement the database schema for user authentication.

#### Subtasks
- [ ] Create users table with required fields
- [ ] Add indexes for email and username
- [ ] Create password reset tokens table
- [ ] Set up database constraints
"""


# Validation Test Fixtures (keep existing)

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


@pytest.fixture
def project_context(temp_project_dir):
    """Create a project context for testing"""
    return ProjectContext(temp_project_dir)


@pytest.fixture
def path_manager(temp_project_dir):
    """Create a path manager for testing"""
    return PathManager(temp_project_dir, use_legacy_structure=False)


@pytest.fixture
def service_container():
    """Create a service container for testing"""
    container = ServiceContainer()

    # Register mock services
    container.register('template_provider', Mock())
    container.register('memory_provider', Mock())
    container.register('script_generator', Mock())
    container.register('ai_instruction_provider', Mock())

    return container


@pytest.fixture
def specpulse_instance(temp_project_dir):
    """Create a SpecPulse instance for testing"""
    return SpecPulse(project_path=temp_project_dir)


@pytest.fixture
def mock_template_provider():
    """Mock template provider for testing"""
    mock = Mock()
    mock.get_spec_template.return_value = sample_spec_content()
    mock.get_plan_template.return_value = sample_plan_content()
    mock.get_task_template.return_value = sample_task_content()
    return mock


# Helper functions for testing
def create_spec_file(project_dir: Path, feature_id: str, spec_num: int, content: str = None):
    """Create a specification file for testing"""
    if not content:
        content = sample_spec_content()

    specs_dir = project_dir / ".specpulse" / "specs" / f"{feature_id}-test-feature"
    specs_dir.mkdir(parents=True, exist_ok=True)

    spec_file = specs_dir / f"spec-{spec_num:03d}.md"
    with open(spec_file, "w") as f:
        f.write(content)

    return spec_file


def create_plan_file(project_dir: Path, feature_id: str, plan_num: int, content: str = None):
    """Create a plan file for testing"""
    if not content:
        content = sample_plan_content()

    plans_dir = project_dir / ".specpulse" / "plans" / f"{feature_id}-test-feature"
    plans_dir.mkdir(parents=True, exist_ok=True)

    plan_file = plans_dir / f"plan-{plan_num}.md"
    with open(plan_file, "w") as f:
        f.write(content)

    return plan_file


# Test markers configuration
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "security: mark test as a security test")


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
