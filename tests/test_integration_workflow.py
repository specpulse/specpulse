"""
Integration Tests for SpecPulse - Complete Workflow Testing
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import json
import subprocess
import sys
import os
from datetime import datetime, timedelta

from specpulse.cli.main import SpecPulseCLI
from specpulse.core.template_manager import TemplateManager
from specpulse.core.memory_manager import MemoryManager
from specpulse.core.validator import Validator
from specpulse.core.tier_manager import TierManager


class TestIntegration:
    """Integration tests for complete workflows"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.original_cwd = os.getcwd()

        # Change to temp directory
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_complete_workflow_initialization_to_validation(self):
        """Test complete workflow from initialization to validation"""
        # 1. Initialize project
        cli = SpecPulseCLI(no_color=True, verbose=False)
        success = cli.init("test-project", here=True)
        assert success

        # Verify project structure created
        expected_dirs = ["specs", "plans", "tasks", "memory", "templates"]
        for dir_name in expected_dirs:
            assert (self.project_path / dir_name).exists()

        # 2. Initialize components
        template_manager = TemplateManager(self.project_path)
        memory_manager = MemoryManager(self.project_path)
        validator = Validator(self.project_path)

        # 3. Validate initial state
        validation_results = validator.validate_all(self.project_path)
        assert isinstance(validation_results, list)

        # 4. Create a feature using templates
        spec_template = self.project_path / "templates" / "spec.md"
        assert spec_template.exists()

        # 5. Test template system
        templates = template_manager.list_templates()
        assert isinstance(templates, list)

        # 6. Test memory system
        memory_summary = memory_manager.get_memory_summary()
        assert "statistics" in memory_summary
        assert "active_features" in memory_summary

    def test_spec_to_plan_to_task_workflow(self):
        """Test specification to plan to task workflow"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("test-workflow", here=True)

        # Create spec directory and file
        feature_dir = "001-test-feature"
        spec_dir = self.project_path / "specs" / feature_dir
        spec_dir.mkdir(parents=True)

        spec_file = spec_dir / "spec-001.md"
        spec_content = """
# Specification: Test Feature

## Functional Requirements
FR-001: User can create account
- Acceptance: Registration form works correctly
- Priority: MUST

## User Stories
### Story 1: User Registration
**As a** new user
**I want** to create an account
**So that** I can use the system

**Acceptance Criteria:**
- [ ] Form validates email format
- [ ] Password meets requirements
- [ ] Confirmation email sent

## Acceptance Criteria
- [ ] All functional requirements implemented
- [ ] User stories completed
"""
        spec_file.write_text(spec_content)

        # Create plan directory and file
        plan_dir = self.project_path / "plans" / feature_dir
        plan_dir.mkdir(parents=True)

        plan_file = plan_dir / "plan-001.md"
        plan_content = """
# Implementation Plan: Test Feature

## Specification Reference
- **Spec ID**: SPEC-001
- **Generated**: 2024-01-01

## Architecture Overview
```mermaid
graph TD
    A[UI] --> B[API]
    B --> C[Database]
```

## Phase 1: Core Implementation
### Objectives
- Implement user registration
- Set up database schema

### Tasks
- [ ] Create user model
- [ ] Implement registration API
- [ ] Create registration form

## Success Criteria
- Users can register successfully
- Data is persisted correctly
"""
        plan_file.write_text(plan_content)

        # Create task directory and file
        task_dir = self.project_path / "tasks" / feature_dir
        task_dir.mkdir(parents=True)

        task_file = task_dir / "task-001.md"
        task_content = """
# Task Breakdown: Test Feature

### T001: Create User Model
**Status**: [ ]
**Effort**: 4 hours
**Dependencies**: Database setup

**Implementation:**
- Define User schema
- Implement validation rules
- Add migration scripts

### T002: Implement Registration API
**Status**: [ ]
**Effort**: 6 hours
**Dependencies**: T001

**Implementation:**
- Create registration endpoint
- Implement email validation
- Add error handling

### T003: Create Registration Form
**Status**: [ ]
**Effort**: 3 hours
**Dependencies**: T002

**Implementation:**
- Design form UI
- Implement client-side validation
- Add success/error messages

## Progress Tracking
- Total Tasks: 3
- Completed: 0
- In Progress: 0
- Blocked: 0
"""
        task_file.write_text(task_content)

        # Validate the complete workflow
        validator = Validator(self.project_path)
        validation_results = validator.validate_all(self.project_path, verbose=True)

        # Should have validation results for each component
        assert len(validation_results) > 0

        # Check for successful validations
        successful_validations = [r for r in validation_results if r.get("status") == "success"]
        assert len(successful_validations) > 0

    def test_template_and_memory_integration(self):
        """Test integration between template and memory systems"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("integration-test", here=True)

        template_manager = TemplateManager(self.project_path)
        memory_manager = MemoryManager(self.project_path)

        # Create and register a custom template
        custom_template = self.project_path / "templates" / "custom_spec.md"
        template_content = """
# Custom Specification: {{ feature_name }}

## ID: {{ spec_id }}
## Created: {{ date }}
## Author: {{ author }}

## Custom Requirements
{{ custom_requirements }}

## Custom Sections
{{ custom_sections }}
"""
        custom_template.write_text(template_content)

        # Register template
        success = template_manager.register_template(custom_template)
        assert success

        # Update memory with template creation
        memory_manager.update_context(
            action="template_created",
            details={"template_name": "custom_spec.md"},
            category="template",
        )

        # Add decision about template
        from specpulse.core.memory_manager import DecisionRecord

        decision = DecisionRecord(
            id="001",
            title="Use Custom Template Format",
            status="accepted",
            date="2024-01-01",
            author="Team Lead",
            rationale="Custom templates provide better flexibility",
            alternatives_considered=["Standard templates only"],
            consequences=["More maintenance", "Better customization"],
            related_decisions=[],
            tags=["template", "customization"],
        )
        memory_manager.add_decision_record(decision)

        # Search memory for template-related entries
        template_results = memory_manager.search_memory("template")
        assert len(template_results) >= 2  # Context entry + decision

        # Verify template appears in template list
        templates = template_manager.list_templates()
        template_names = [t["name"] for t in templates]
        assert "custom_spec" in template_names

    def test_cli_memory_commands_integration(self):
        """Test CLI memory commands integration"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("memory-test", here=True)

        # Memory manager should be initialized since we're in a project
        assert hasattr(cli, "memory_manager")
        assert cli.memory_manager is not None

        # Add some context entries
        cli.memory_manager.update_context(
            feature_name="Memory Test Feature",
            feature_id="001",
            action="feature_created",
            details={"test": True},
        )

        cli.memory_manager.update_context(
            action="validation_completed", details={"result": "success"}
        )

        # Test memory summary
        success = cli.memory_summary()
        assert success

        # Test memory search
        success = cli.memory_search("Memory Test")
        assert success

        # Test memory cleanup (with recent entries, shouldn't remove anything)
        success = cli.memory_cleanup(days=30)
        assert success

        # Verify entries still exist
        summary = cli.memory_manager.get_memory_summary()
        assert summary["statistics"]["total_context_entries"] >= 2

    def test_cli_template_commands_integration(self):
        """Test CLI template commands integration"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("template-test", here=True)

        # Template manager should be initialized
        assert hasattr(cli, "template_manager")
        assert cli.template_manager is not None

        # Create a test template
        test_template = self.project_path / "templates" / "test_template.md"
        test_template.write_text(
            """
# Test Template: {{ feature_name }}

## Variables
- feature_name: {{ feature_name }}
- spec_id: {{ spec_id }}
- date: {{ date }}

## Content
This is a test template for {{ feature_name }}.
"""
        )

        # Test template validation
        success = cli.template_validate("test_template.md")
        assert success

        # Test template list
        success = cli.template_list()
        assert success

        # Test template preview
        success = cli.template_preview("test_template.md")
        assert success

        # Test template backup
        success = cli.template_backup()
        assert success

        # Verify backup exists
        backup_dir = self.project_path / ".specpulse" / "template_backups"
        assert backup_dir.exists()
        assert len(list(backup_dir.iterdir())) > 0

    def test_error_handling_integration(self):
        """Test error handling across the system"""
        cli = SpecPulseCLI(no_color=True, verbose=True)

        # Test initialization in non-existent directory
        non_existent = Path("/tmp/non_existent_path_12345")
        success = cli.init("test", here=False, project_name=str(non_existent))
        # Should handle gracefully - either succeed by creating dir or fail gracefully

        # Test template operations on non-SpecPulse project
        os.chdir(self.temp_dir)  # Not a SpecPulse project
        assert hasattr(cli, "template_manager")
        assert cli.template_manager is None  # Should not be initialized

        # Memory operations should also fail gracefully
        assert hasattr(cli, "memory_manager")
        assert cli.memory_manager is None

    def test_validation_integration_with_errors(self):
        """Test validation system with intentional errors"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True, verbose=True)
        cli.init("validation-test", here=True)

        # Create invalid specification file
        spec_dir = self.project_path / "specs" / "001-invalid"
        spec_dir.mkdir(parents=True)

        spec_file = spec_dir / "spec-001.md"
        spec_file.write_text("This is not a valid specification")

        # Create invalid plan file
        plan_dir = self.project_path / "plans" / "001-invalid"
        plan_dir.mkdir(parents=True)

        plan_file = plan_dir / "plan-001.md"
        plan_file.write_text("This is not a valid plan")

        # Create invalid task file
        task_dir = self.project_path / "tasks" / "001-invalid"
        task_dir.mkdir(parents=True)

        task_file = task_dir / "task-001.md"
        task_file.write_text("This is not a valid task breakdown")

        # Validate and check for errors
        validator = Validator(self.project_path)
        results = validator.validate_all(self.project_path, verbose=True)

        # Should find validation issues
        assert len(results) > 0

        # Check for error/warning messages
        error_messages = [r for r in results if r.get("status") == "error"]
        warning_messages = [r for r in results if r.get("status") == "warning"]

        # Should have at least some warnings/errors
        assert len(error_messages) + len(warning_messages) > 0


class TestAICommandIntegration:
    """Test AI command system integration"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_ai_command_directory_structure(self):
        """Test AI command directory structure creation"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("ai-commands-test", here=True)

        # Check AI command directories are created
        claude_dir = self.project_path / ".claude"
        gemini_dir = self.project_path / ".gemini"

        assert claude_dir.exists()
        assert gemini_dir.exists()

        # Check commands subdirectories
        claude_commands = claude_dir / "commands"
        gemini_commands = gemini_dir / "commands"

        assert claude_commands.exists()
        assert gemini_commands.exists()

        # Check scripts directory
        scripts_dir = self.project_path / "scripts"
        assert scripts_dir.exists()

    def test_script_system_integration(self):
        """Test script system integration"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("script-test", here=True)

        # Check script files are created
        scripts_dir = self.project_path / "scripts"

        # Check for common script files
        script_files = [
            "sp-pulse-init.sh",
            "sp-pulse-spec.sh",
            "sp-pulse-plan.sh",
            "sp-pulse-task.sh",
        ]

        for script_file in script_files:
            script_path = scripts_dir / script_file
            assert script_path.exists()

    def test_memory_ai_tracking(self):
        """Test memory system AI tracking capabilities"""
        # Initialize project
        cli = SpecPulseCLI(no_color=True)
        cli.init("ai-memory-test", here=True)

        memory_manager = MemoryManager(self.project_path)

        # Test AI-related context tracking
        memory_manager.update_context(
            action="ai_command_executed",
            details={"ai_assistant": "claude", "command": "sp-pulse", "feature": "test-feature"},
            category="ai",
        )

        # Test search for AI-related entries
        results = memory_manager.search_memory("ai_assistant")
        assert len(results) >= 1

        # Check AI decisions can be tracked
        from specpulse.core.memory_manager import DecisionRecord

        ai_decision = DecisionRecord(
            id="AI-001",
            title="Use Claude for Code Generation",
            status="accepted",
            date="2024-01-01",
            author="Development Team",
            rationale="Claude provides better code generation",
            alternatives_considered=["Manual coding", "Other AI tools"],
            consequences=["Dependency on AI", "Faster development"],
            related_decisions=[],
            tags=["ai", "claude", "code-generation"],
        )
        memory_manager.add_decision_record(ai_decision)

        # Search for AI decisions
        decision_results = memory_manager.search_memory("claude")
        assert len(decision_results) >= 1

    def test_tiered_template_workflow(self):
        """Test full workflow: minimal → standard → complete."""
        # 1. Initialize project
        cli = SpecPulseCLI(no_color=True, verbose=False)
        cli.init("test-project", here=True)

        # 2. Create minimal spec manually
        spec_dir = self.project_path / "specs" / "001-test-feature"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"

        # Write minimal spec
        spec_path.write_text(
            """<!-- TIER: minimal -->
# Feature: Test Feature

## What
Build a payment system for premium features

## Why
Users need to pay for premium features to access exclusive content

## Done When
- [ ] User can enter credit card information securely
- [ ] Payment is processed through payment gateway
- [ ] Receipt is sent via email after successful payment
"""
        )

        # Verify minimal content
        content = spec_path.read_text()
        assert "## What" in content
        assert "## Why" in content
        assert "## Done When" in content
        assert "Build a payment system" in content

        # 3. Expand to standard using TierManager
        tier_manager = TierManager(self.project_path)
        current_tier = tier_manager.get_current_tier("001-test-feature")
        assert current_tier == "minimal"

        # Expand to standard
        success = tier_manager.expand_tier("001-test-feature", "standard")
        assert success

        # Verify expansion
        content = spec_path.read_text()
        assert "Build a payment system" in content  # Preserved
        assert "## Executive Summary" in content  # Added
        assert "## User Stories" in content  # Added
        assert "## Functional Requirements" in content  # Added
        assert "## Technical Approach" in content  # Added

        # Verify tier changed
        new_tier = tier_manager.get_current_tier("001-test-feature")
        assert new_tier == "standard"

        # 4. Expand to complete
        success = tier_manager.expand_tier("001-test-feature", "complete")
        assert success

        # Verify final state
        content = spec_path.read_text()
        assert "Build a payment system" in content  # Still preserved
        assert "## Non-Functional Requirements" in content  # Added
        assert "## Security Considerations" in content  # Added
        assert "## Performance Requirements" in content  # Added
        assert "## Testing Strategy" in content  # Added
        assert "## Deployment Considerations" in content  # Added

        # Verify tier changed
        final_tier = tier_manager.get_current_tier("001-test-feature")
        assert final_tier == "complete"

        # 5. Test validation
        validation = tier_manager.validate_tier(spec_path)
        assert validation["tier"] == "complete"

    def test_tiered_template_cli_workflow(self):
        """Test tiered templates via CLI."""
        # 1. Initialize project
        cli = SpecPulseCLI(no_color=True, verbose=False)
        cli.init("test-project", here=True)

        # 2. Create minimal spec
        spec_dir = self.project_path / "specs" / "002-auth-feature"
        spec_dir.mkdir(parents=True)
        spec_path = spec_dir / "spec-001.md"

        spec_path.write_text(
            """<!-- TIER: minimal -->
# Feature: User Authentication

## What
Implement OAuth2 authentication

## Why
Users need secure login

## Done When
- [ ] OAuth2 implemented
- [ ] Users can log in
- [ ] Tokens are secure
"""
        )

        # 3. Expand via CLI
        success = cli.expand("002-auth-feature", "standard", show_diff=False)
        assert success

        # Verify expansion
        content = spec_path.read_text()
        assert "## Executive Summary" in content
        assert "OAuth2 authentication" in content  # Preserved

        # 4. Expand to complete
        success = cli.expand("002-auth-feature", "complete", show_diff=False)
        assert success

        content = spec_path.read_text()
        assert "## Security Considerations" in content
        assert "OAuth2 authentication" in content  # Still preserved
