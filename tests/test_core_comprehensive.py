"""
Comprehensive test suite for SpecPulse Core module.
Tests all core functionality with proper mocking for file I/O operations.
"""

import pytest
import unittest
from unittest.mock import patch, mock_open, MagicMock, call
from pathlib import Path
import tempfile
import shutil
import yaml
import json
import os

from specpulse.core.specpulse import SpecPulse


class TestSpecPulse(unittest.TestCase):
    """Comprehensive tests for SpecPulse core class"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init_with_default_path(self):
        """Test SpecPulse initialization with default path"""
        with patch('specpulse.core.specpulse.Path.cwd', return_value=self.project_path):
            specpulse = SpecPulse()
            self.assertEqual(specpulse.project_path, self.project_path)

    def test_init_with_custom_path(self):
        """Test SpecPulse initialization with custom path"""
        specpulse = SpecPulse(self.project_path)
        self.assertEqual(specpulse.project_path, self.project_path)

    def test_load_config_no_config_file(self):
        """Test loading config when no config file exists"""
        specpulse = SpecPulse(self.project_path)
        config = specpulse._load_config()
        self.assertEqual(config, {})

    def test_load_config_with_existing_file(self):
        """Test loading config with existing YAML file"""
        # Create config structure
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True)
        
        config_data = {
            "version": "1.0.0",
            "project": {"name": "test-project"},
            "ai": {"primary": "claude"}
        }
        
        with open(config_dir / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        specpulse = SpecPulse(self.project_path)
        
        self.assertEqual(specpulse.config["version"], "1.0.0")
        self.assertEqual(specpulse.config["project"]["name"], "test-project")
        self.assertEqual(specpulse.config["ai"]["primary"], "claude")

    def test_load_config_yaml_error(self):
        """Test loading config with malformed YAML"""
        config_dir = self.project_path / ".specpulse"
        config_dir.mkdir(parents=True)
        
        # Write invalid YAML
        with open(config_dir / "config.yaml", 'w', encoding='utf-8') as f:
            f.write("invalid: yaml: content: [")
        
        specpulse = SpecPulse(self.project_path)
        # Should handle YAML error gracefully
        self.assertIsInstance(specpulse.config, dict)

    def test_resources_dir_property(self):
        """Test that resources_dir is set correctly"""
        specpulse = SpecPulse(self.project_path)
        expected_path = Path(specpulse.__class__.__module__.replace(".", "/")).parent.parent / "resources"
        # Just test that it's a Path object since the exact path depends on file structure
        self.assertIsInstance(specpulse.resources_dir, Path)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="template content")
    def test_get_spec_template_from_file(self, mock_file):
        """Test getting spec template from resource file"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, 'exists', return_value=True):
            template_path = specpulse.resources_dir / "templates" / "spec.md"
            with patch.object(template_path, 'exists', return_value=True):
                template = specpulse.get_spec_template()
                
        self.assertEqual(template, "template content")

    def test_get_spec_template_fallback(self):
        """Test getting spec template fallback when file doesn't exist"""
        specpulse = SpecPulse(self.project_path)
        
        # Mock file not existing
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_spec_template()
            
        # Should return fallback template
        self.assertIn("# Specification: [FEATURE_NAME]", template)
        self.assertIn("## Functional Requirements", template)
        self.assertIn("[NEEDS CLARIFICATION]", template)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="plan template content")
    def test_get_plan_template_from_file(self, mock_file):
        """Test getting plan template from resource file"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_plan_template()
            
        self.assertEqual(template, "plan template content")

    def test_get_plan_template_fallback(self):
        """Test getting plan template fallback"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_plan_template()
            
        self.assertIn("# Implementation Plan: [FEATURE_NAME]", template)
        self.assertIn("## Technology Stack", template)
        self.assertIn("## Implementation Phases", template)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="task template content")
    def test_get_task_template_from_file(self, mock_file):
        """Test getting task template from resource file"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_task_template()
            
        self.assertEqual(template, "task template content")

    def test_get_task_template_fallback(self):
        """Test getting task template fallback"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_task_template()
            
        self.assertIn("# Task List: [FEATURE_NAME]", template)
        self.assertIn("## Task Organization", template)
        self.assertIn("TASK-001", template)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="constitution content")
    def test_get_constitution_template_from_file(self, mock_file):
        """Test getting constitution template from resource file"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_constitution_template()
            
        self.assertEqual(template, "constitution content")

    def test_get_constitution_template_fallback(self):
        """Test getting constitution template fallback"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_constitution_template()
            
        self.assertIn("# Project Constitution", template)
        self.assertIn("## Immutable Principles", template)
        self.assertIn("Simplicity First", template)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="context content")
    def test_get_context_template_from_file(self, mock_file):
        """Test getting context template from resource file"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_context_template()
            
        self.assertEqual(template, "context content")

    def test_get_context_template_fallback(self):
        """Test getting context template fallback"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_context_template()
            
        self.assertIn("# Project Context", template)
        self.assertIn("## Current State", template)
        self.assertIn("## Team Preferences", template)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="decisions content")
    def test_get_decisions_template_from_file(self, mock_file):
        """Test getting decisions template from resource file"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_decisions_template()
            
        self.assertEqual(template, "decisions content")

    def test_get_decisions_template_fallback(self):
        """Test getting decisions template fallback"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            template = specpulse.get_decisions_template()
            
        self.assertIn("# Architectural Decisions", template)
        self.assertIn("## Decision Log", template)
        self.assertIn("### ADR-001", template)

    def test_get_all_script_templates(self):
        """Test all script template methods"""
        specpulse = SpecPulse(self.project_path)
        
        # Test setup script
        setup_script = specpulse.get_setup_script()
        self.assertIn("#!/bin/bash", setup_script)
        self.assertIn("SpecPulse Feature Initialization Script", setup_script)
        self.assertIn("FEATURE_NAME", setup_script)
        
        # Test spec script
        spec_script = specpulse.get_spec_script()
        self.assertIn("#!/bin/bash", spec_script)
        self.assertIn("SpecPulse Spec Context Script", spec_script)
        
        # Test plan script
        plan_script = specpulse.get_plan_script()
        self.assertIn("#!/bin/bash", plan_script)
        self.assertIn("SpecPulse Plan Context Script", plan_script)
        
        # Test task script
        task_script = specpulse.get_task_script()
        self.assertIn("#!/bin/bash", task_script)
        self.assertIn("SpecPulse Task Context Script", task_script)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="script content")
    def test_script_templates_from_files(self, mock_file):
        """Test script templates loaded from files"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            # Test each script method
            setup_script = specpulse.get_setup_script()
            self.assertEqual(setup_script, "script content")
            
            spec_script = specpulse.get_spec_script()
            self.assertEqual(spec_script, "script content")
            
            plan_script = specpulse.get_plan_script()
            self.assertEqual(plan_script, "script content")
            
            task_script = specpulse.get_task_script()
            self.assertEqual(task_script, "script content")

    def test_get_validate_script(self):
        """Test validate script generation"""
        specpulse = SpecPulse(self.project_path)
        
        script = specpulse.get_validate_script()
        
        self.assertIn("#!/bin/bash", script)
        self.assertIn("SpecPulse Validation Script", script)
        self.assertIn("validate_spec()", script)
        self.assertIn("Requirements section", script)
        self.assertIn("NEEDS CLARIFICATION", script)

    def test_get_generate_script(self):
        """Test generate script"""
        specpulse = SpecPulse(self.project_path)
        
        script = specpulse.get_generate_script()
        
        self.assertIn("#!/bin/bash", script)
        self.assertIn("SpecPulse Generation Script", script)
        self.assertIn("generate_from_template()", script)
        self.assertIn("[FEATURE_NAME]", script)

    def test_get_claude_instructions(self):
        """Test Claude instructions"""
        specpulse = SpecPulse(self.project_path)
        
        instructions = specpulse.get_claude_instructions()
        
        self.assertIn("# SpecPulse Commands for Claude", instructions)
        self.assertIn("/pulse init", instructions)
        self.assertIn("/spec create", instructions)
        self.assertIn("/plan generate", instructions)
        self.assertIn("/task breakdown", instructions)
        self.assertIn("/validate", instructions)

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="pulse command content")
    def test_claude_command_methods_from_files(self, mock_file):
        """Test Claude command methods loading from files"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            # Test each command method
            pulse_cmd = specpulse.get_claude_pulse_command()
            self.assertEqual(pulse_cmd, "pulse command content")
            
            spec_cmd = specpulse.get_claude_spec_command()
            self.assertEqual(spec_cmd, "pulse command content")
            
            plan_cmd = specpulse.get_claude_plan_command()
            self.assertEqual(plan_cmd, "pulse command content")
            
            task_cmd = specpulse.get_claude_task_command()
            self.assertEqual(task_cmd, "pulse command content")

    def test_claude_command_methods_fallback(self):
        """Test Claude command methods fallback when files don't exist"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            pulse_cmd = specpulse.get_claude_pulse_command()
            self.assertEqual(pulse_cmd, "# /pulse command not found")
            
            spec_cmd = specpulse.get_claude_spec_command()
            self.assertEqual(spec_cmd, "# /spec command not found")
            
            plan_cmd = specpulse.get_claude_plan_command()
            self.assertEqual(plan_cmd, "# /plan command not found")
            
            task_cmd = specpulse.get_claude_task_command()
            self.assertEqual(task_cmd, "# /task command not found")

    @patch('specpulse.core.specpulse.open', new_callable=mock_open, read_data="gemini command content")
    def test_gemini_command_methods_from_files(self, mock_file):
        """Test Gemini command methods loading from files"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            pulse_cmd = specpulse.get_gemini_pulse_command()
            self.assertEqual(pulse_cmd, "gemini command content")
            
            spec_cmd = specpulse.get_gemini_spec_command()
            self.assertEqual(spec_cmd, "gemini command content")
            
            plan_cmd = specpulse.get_gemini_plan_command()
            self.assertEqual(plan_cmd, "gemini command content")
            
            task_cmd = specpulse.get_gemini_task_command()
            self.assertEqual(task_cmd, "gemini command content")

    def test_gemini_command_methods_fallback(self):
        """Test Gemini command methods fallback when files don't exist"""
        specpulse = SpecPulse(self.project_path)
        
        with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
            mock_path = MagicMock()
            mock_path.exists.return_value = False
            mock_div.return_value.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
            
            pulse_cmd = specpulse.get_gemini_pulse_command()
            self.assertEqual(pulse_cmd, "# Gemini pulse command not found")
            
            spec_cmd = specpulse.get_gemini_spec_command()
            self.assertEqual(spec_cmd, "# Gemini spec command not found")
            
            plan_cmd = specpulse.get_gemini_plan_command()
            self.assertEqual(plan_cmd, "# Gemini plan command not found")
            
            task_cmd = specpulse.get_gemini_task_command()
            self.assertEqual(task_cmd, "# Gemini task command not found")

    def test_get_gemini_instructions(self):
        """Test Gemini instructions"""
        specpulse = SpecPulse(self.project_path)
        
        instructions = specpulse.get_gemini_instructions()
        
        self.assertIn("# SpecPulse Commands for Gemini CLI", instructions)
        self.assertIn("/pulse init", instructions)
        self.assertIn("/spec create", instructions)
        self.assertIn("/plan generate", instructions)
        self.assertIn("/task breakdown", instructions)
        self.assertIn("/validate", instructions)
        self.assertIn("Optimization options", instructions)
        self.assertIn("## Constitution Principles", instructions)

    def test_file_io_error_handling(self):
        """Test file I/O error handling in template methods"""
        specpulse = SpecPulse(self.project_path)
        
        # Mock file operations to raise exceptions
        with patch('specpulse.core.specpulse.open', side_effect=IOError("File error")):
            with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
                mock_path = MagicMock()
                mock_path.exists.return_value = True
                mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
                
                # Should fall back to embedded template
                spec_template = specpulse.get_spec_template()
                self.assertIn("# Specification: [FEATURE_NAME]", spec_template)

    def test_encoding_handling(self):
        """Test UTF-8 encoding handling in file operations"""
        specpulse = SpecPulse(self.project_path)
        
        # Test with unicode content
        unicode_content = "Template with unicode: café, naïve, résumé"
        
        with patch('specpulse.core.specpulse.open', mock_open(read_data=unicode_content)) as mock_file:
            with patch.object(specpulse.resources_dir, '__truediv__') as mock_div:
                mock_path = MagicMock()
                mock_path.exists.return_value = True
                mock_div.return_value.__truediv__.return_value.__truediv__.return_value = mock_path
                
                template = specpulse.get_spec_template()
                
        self.assertEqual(template, unicode_content)
        # Verify encoding parameter was used
        mock_file.assert_called_with(mock_path, 'r', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()