"""Complete coverage test for SpecPulse"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import tempfile
import shutil
import os
import sys

from specpulse import __version__
from specpulse.cli.main import SpecPulseCLI, main
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils


class TestCompleteCoverage(unittest.TestCase):
    """Test for complete code coverage"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_specpulse_complete_flow(self):
        """Test complete SpecPulse flow"""
        # Test CLI initialization
        cli = SpecPulseCLI(no_color=True, verbose=True)
        
        # Test project initialization
        result = cli.init("test-project", ai="claude", template="web")
        self.assertTrue(result)
        
        # Change to project directory
        os.chdir("test-project")
        
        # Test doctor
        result = cli.doctor()
        self.assertTrue(result)
        
        # Test validate
        result = cli.validate()
        self.assertTrue(result)
        
        # Test validate with components
        for component in ["spec", "plan", "task", "constitution"]:
            result = cli.validate(component=component)
            self.assertTrue(result)
        
        # Test validate with auto-fix
        result = cli.validate(auto_fix=True, verbose=True)
        self.assertTrue(result)
        
        # Test sync
        result = cli.sync()
        self.assertTrue(result)
        
        # Test update
        result = cli.update()
        self.assertTrue(result)
        
        # Test SpecPulse core
        sp = SpecPulse()
        
        # Test all SpecPulse methods
        config = sp.get_config()
        self.assertIsNotNone(config)
        
        # Test template methods
        template_path = sp.get_template_path("spec")
        self.assertIsNotNone(template_path)
        
        content = sp.get_template_content("spec")
        self.assertIsNotNone(content)
        
        # Test resource methods
        resource_path = sp.get_resource_path("memory/constitution.md")
        self.assertIsNotNone(resource_path)
        
        # Test command methods
        pulse_cmd = sp.get_claude_pulse_command()
        self.assertIsNotNone(pulse_cmd)
        
        spec_cmd = sp.get_claude_spec_command()
        self.assertIsNotNone(spec_cmd)
        
        plan_cmd = sp.get_claude_plan_command()
        self.assertIsNotNone(plan_cmd)
        
        task_cmd = sp.get_claude_task_command()
        self.assertIsNotNone(task_cmd)
        
        # Test Gemini commands
        pulse_toml = sp.get_gemini_pulse_command()
        self.assertIsNotNone(pulse_toml)
        
        spec_toml = sp.get_gemini_spec_command()
        self.assertIsNotNone(spec_toml)
        
        plan_toml = sp.get_gemini_plan_command()
        self.assertIsNotNone(plan_toml)
        
        task_toml = sp.get_gemini_task_command()
        self.assertIsNotNone(task_toml)
        
        # Test script methods
        init_script = sp.get_pulse_init_script()
        self.assertIsNotNone(init_script)
        
        spec_script = sp.get_pulse_spec_script()
        self.assertIsNotNone(spec_script)
        
        plan_script = sp.get_pulse_plan_script()
        self.assertIsNotNone(plan_script)
        
        task_script = sp.get_pulse_task_script()
        self.assertIsNotNone(task_script)
        
        # Test memory methods
        const = sp.get_constitution_template()
        self.assertIsNotNone(const)
        
        ctx = sp.get_context_template()
        self.assertIsNotNone(ctx)
        
        dec = sp.get_decisions_template()
        self.assertIsNotNone(dec)
        
        # Test manifest
        manifest = sp.get_pulse_manifest()
        self.assertIsNotNone(manifest)
        
        # Test Validator
        validator = Validator()
        
        # Test validation methods
        result = validator.validate_all(".")
        self.assertIsNotNone(result)
        
        result = validator.validate_structure(".")
        self.assertIsNotNone(result)
        
        result = validator.validate_specifications(".")
        self.assertIsNotNone(result)
        
        result = validator.validate_plans(".")
        self.assertIsNotNone(result)
        
        result = validator.validate_constitution(".")
        self.assertIsNotNone(result)
        
        # Test auto-fix
        validator.auto_fix(".")
        
        # Test Console methods
        console = Console(no_color=True, verbose=True)
        
        # Test all display methods
        console.show_banner(mini=False)
        console.show_banner(mini=True)
        
        console.info("Test info")
        console.success("Test success")
        console.warning("Test warning")
        console.error("Test error")
        console.debug("Test debug")
        
        console.header("Test header")
        console.section("Test section")
        console.subsection("Test subsection")
        
        console.code_block("print('test')", "python")
        
        console.table(["Col1", "Col2"], [["Val1", "Val2"]])
        console.tree({"root": {"child": None}})
        
        console.divider()
        console.json({"key": "value"})
        console.columns(["Item1", "Item2"])
        
        console.panel("Test panel")
        console.rule("Test rule")
        
        # Test formatting methods
        console.format_success("Success")
        console.format_error("Error")
        console.format_warning("Warning")
        console.format_info("Info")
        
        # Test animations (with mocked sleep)
        with patch('time.sleep'):
            console.spinner("Loading", 0.1)
            console.pulse_animation("Pulsing", 0.1)
            console.celebration()
        
        # Test prompts (with mocked input)
        with patch('builtins.input', return_value='test'):
            result = console.prompt("Enter value")
            self.assertEqual(result, 'test')
        
        with patch('builtins.input', return_value='y'):
            result = console.confirm("Continue?")
            self.assertTrue(result)
        
        # Test GitUtils
        git = GitUtils()
        
        # Mock subprocess for git commands
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="output")
            
            # Test all git methods
            git.check_git_installed()
            git.is_git_repo()
            git.init_repo()
            git.add_files("test.txt")
            git.commit("Test")
            git.get_current_branch()
            git.create_branch("feature")
            git.checkout_branch("main")
            git.get_status()
            git.get_log()
            git.push()
            git.pull()
            git.get_remote_url()
            git.add_remote("origin", "url")
            git.tag("v1.0.0")
            git.get_tags()
            git.stash()
            git.stash_pop()
    
    @patch('sys.argv', ['specpulse', '--version'])
    def test_main_function_coverage(self):
        """Test main function for coverage"""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('sys.argv', ['specpulse', '--help'])
    def test_main_help(self):
        """Test main help"""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
    
    def test_version(self):
        """Test version is set"""
        self.assertIsNotNone(__version__)
        self.assertEqual(__version__, "1.0.3")
    
    def test_edge_cases(self):
        """Test edge cases for coverage"""
        # Test CLI with existing project
        cli = SpecPulseCLI()
        cli.init(here=True)
        
        # Test with invalid component
        result = cli.validate(component="invalid")
        self.assertTrue(result)  # Should default to 'all'
        
        # Test Console with choices
        console = Console()
        with patch('builtins.input', side_effect=['invalid', 'valid']):
            result = console.prompt("Choose", choices=['valid'])
            self.assertEqual(result, 'valid')
        
        # Test Console status
        with console.status("Processing"):
            pass  # Just test context manager
        
        # Test Console clear
        with patch('os.system'):
            console.clear()
        
        # Test Console print_exception
        try:
            raise ValueError("Test")
        except:
            console.print_exception()
    
    def test_specpulse_file_not_found(self):
        """Test SpecPulse when files don't exist"""
        sp = SpecPulse()
        
        # These should return None or empty when files don't exist
        with patch('pathlib.Path.exists', return_value=False):
            result = sp.get_template_content("nonexistent")
            self.assertEqual(result, "")
        
        with patch('pathlib.Path.exists', return_value=False):
            result = sp.get_resource_content("nonexistent")
            self.assertEqual(result, "")
    
    def test_validator_edge_cases(self):
        """Test Validator edge cases"""
        validator = Validator()
        
        # Test with non-existent path
        result = validator.validate_all("/nonexistent/path")
        self.assertIsNotNone(result)
        self.assertFalse(result['valid'])
        
        # Test check methods
        result = validator.check_directory_exists("/nonexistent")
        self.assertFalse(result)
        
        result = validator.check_file_exists("/nonexistent/file.txt")
        self.assertFalse(result)
        
        result = validator.check_file_not_empty("/nonexistent/file.txt")
        self.assertFalse(result)
        
        # Create empty file and test
        with open("empty.txt", "w") as f:
            pass
        result = validator.check_file_not_empty("empty.txt")
        self.assertFalse(result)
        
        # Test has_needs_clarification
        content = "Test [NEEDS CLARIFICATION: something]"
        result = validator.has_needs_clarification(content)
        self.assertTrue(result)
        
        content = "Test without markers"
        result = validator.has_needs_clarification(content)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()