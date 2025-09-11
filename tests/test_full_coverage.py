"""Full 100% coverage test for SpecPulse"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open, call
from pathlib import Path
import tempfile
import shutil
import os
import sys
import subprocess
import yaml
import json

from specpulse import __version__
from specpulse.cli.main import SpecPulseCLI, main
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils


class TestFullCoverage(unittest.TestCase):
    """Test for 100% code coverage"""
    
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
    
    def test_cli_main_all_paths(self):
        """Test all CLI main paths"""
        cli = SpecPulseCLI(no_color=True, verbose=True)
        
        # Test init with all options
        result = cli.init("test", here=False, ai="claude", template="web")
        self.assertTrue(result)
        
        # Test init in existing directory
        os.chdir("test")
        result = cli.doctor()
        self.assertTrue(result)
        
        # Test all validate options
        result = cli.validate()
        self.assertTrue(result)
        
        result = cli.validate(component="spec", verbose=True, auto_fix=True)
        self.assertTrue(result)
        
        result = cli.validate(component="plan")
        self.assertTrue(result)
        
        result = cli.validate(component="task")
        self.assertTrue(result)
        
        result = cli.validate(component="constitution")
        self.assertTrue(result)
        
        # Test sync
        result = cli.sync()
        self.assertTrue(result)
        
        # Test update
        result = cli.update()
        self.assertTrue(result)
    
    def test_cli_error_paths(self):
        """Test CLI error handling paths"""
        cli = SpecPulseCLI()
        
        # Test doctor without project
        result = cli.doctor()
        self.assertFalse(result)
        
        # Test validate without project
        result = cli.validate()
        self.assertFalse(result)
        
        # Test sync without project
        result = cli.sync()
        self.assertFalse(result)
        
        # Test update without project
        result = cli.update()
        self.assertFalse(result)
        
        # Test init with permission error
        with patch('pathlib.Path.mkdir', side_effect=OSError("Permission denied")):
            result = cli.init("test")
            self.assertFalse(result)
        
        # Test init with file write error
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            result = cli.init("test2")
            self.assertFalse(result)
    
    @patch('sys.argv', ['specpulse', '--version'])
    def test_main_version(self):
        """Test main with version flag"""
        with self.assertRaises(SystemExit):
            main()
    
    @patch('sys.argv', ['specpulse', '--help'])
    def test_main_help(self):
        """Test main with help flag"""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
    
    @patch('sys.argv', ['specpulse', 'init', 'test', '--ai', 'gemini', '--template', 'api'])
    def test_main_init_with_options(self):
        """Test main init with all options"""
        main()
        self.assertTrue(Path("test").exists())
    
    @patch('sys.argv', ['specpulse', 'init', '--here', '--ai', 'claude'])
    def test_main_init_here(self):
        """Test main init here"""
        main()
        self.assertTrue(Path(".specpulse").exists())
    
    @patch('sys.argv', ['specpulse', '--no-color', '-v', 'doctor'])
    def test_main_with_flags(self):
        """Test main with global flags"""
        # Init first
        cli = SpecPulseCLI()
        cli.init(here=True)
        
        main()
    
    def test_specpulse_core_all_methods(self):
        """Test all SpecPulse core methods"""
        sp = SpecPulse()
        
        # Test config
        config = sp.get_config()
        self.assertIsNotNone(config)
        
        # Test all template methods
        path = sp.get_template_path("spec")
        self.assertIsNotNone(path)
        
        # Test resource paths
        path = sp.get_resource_path("memory/constitution.md")
        self.assertIsNotNone(path)
        
        # Test all command getters
        cmds = [
            sp.get_claude_pulse_command(),
            sp.get_claude_spec_command(),
            sp.get_claude_plan_command(),
            sp.get_claude_task_command(),
            sp.get_gemini_pulse_command(),
            sp.get_gemini_spec_command(),
            sp.get_gemini_plan_command(),
            sp.get_gemini_task_command(),
        ]
        for cmd in cmds:
            self.assertIsNotNone(cmd)
        
        # Test all script getters
        scripts = [
            sp.get_pulse_init_script(),
            sp.get_pulse_spec_script(),
            sp.get_pulse_plan_script(),
            sp.get_pulse_task_script(),
        ]
        for script in scripts:
            self.assertIsNotNone(script)
        
        # Test memory templates
        memory = [
            sp.get_constitution_template(),
            sp.get_context_template(),
            sp.get_decisions_template(),
        ]
        for mem in memory:
            self.assertIsNotNone(mem)
        
        # Test manifest
        manifest = sp.get_pulse_manifest()
        self.assertIsNotNone(manifest)
        
        # Test resource content with missing file
        with patch('pathlib.Path.exists', return_value=False):
            content = sp.get_resource_content("missing.txt")
            self.assertEqual(content, "")
        
        # Test read_file with missing file
        with patch('pathlib.Path.exists', return_value=False):
            content = sp.read_file(Path("missing.txt"))
            self.assertEqual(content, "")
    
    def test_validator_all_methods(self):
        """Test all Validator methods"""
        validator = Validator()
        
        # Create test structure
        os.makedirs(".specpulse")
        os.makedirs("memory")
        os.makedirs("specs")
        os.makedirs("plans")
        os.makedirs("tasks")
        os.makedirs("templates")
        os.makedirs("scripts")
        
        # Create test files
        with open(".specpulse/config.yaml", "w") as f:
            yaml.dump({"version": "1.0.0"}, f)
        
        with open("memory/constitution.md", "w") as f:
            f.write("# Constitution\nTest content")
        
        with open("memory/context.md", "w") as f:
            f.write("# Context")
        
        with open("memory/decisions.md", "w") as f:
            f.write("# Decisions")
        
        # Test all validation methods
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
        
        # Test with string path (should convert to Path)
        result = validator.validate_all(os.getcwd())
        self.assertIsNotNone(result)
        
        # Test check methods
        self.assertTrue(validator.check_directory_exists(".specpulse"))
        self.assertFalse(validator.check_directory_exists("nonexistent"))
        
        self.assertTrue(validator.check_file_exists("memory/constitution.md"))
        self.assertFalse(validator.check_file_exists("nonexistent.txt"))
        
        self.assertTrue(validator.check_file_not_empty("memory/constitution.md"))
        
        # Test empty file
        with open("empty.txt", "w") as f:
            pass
        self.assertFalse(validator.check_file_not_empty("empty.txt"))
        
        # Test has_needs_clarification
        content_with = "[NEEDS CLARIFICATION: test]"
        content_without = "No markers here"
        self.assertTrue(validator.has_needs_clarification(content_with))
        self.assertFalse(validator.has_needs_clarification(content_without))
        
        # Test auto_fix
        validator.auto_fix(".")
        
        # Test with missing directories
        shutil.rmtree("specs")
        validator.auto_fix(".")
        self.assertTrue(Path("specs").exists())
    
    def test_console_all_methods(self):
        """Test all Console methods"""
        console = Console(no_color=True, verbose=True)
        console_color = Console(no_color=False, verbose=False)
        
        # Test all display methods
        console.show_banner(mini=False)
        console.show_banner(mini=True)
        console_color.show_banner(mini=False)
        
        console.info("Info")
        console.success("Success")
        console.warning("Warning")
        console.error("Error")
        console.debug("Debug")
        
        console.header("Header", style="bright_green")
        console.section("Section")
        console.subsection("Subsection")
        
        console.code_block("print('test')", "python")
        console.code_block("test")  # No language
        
        console.table(["Col1", "Col2"], [["Val1", "Val2"]], title="Table", style="green")
        console.tree({"root": {"child": None}}, title="Tree")
        
        console.divider()
        console.divider(char="=", width=50, style="blue")
        
        console.json({"key": "value"}, indent=2)
        console.columns(["Item1", "Item2"], columns=2)
        
        console.panel("Panel", title="Title", subtitle="Sub", style="green")
        console.rule()
        console.rule("Title", style="blue")
        
        # Test formatting
        console.format_success("Msg")
        console.format_error("Msg")
        console.format_warning("Msg")
        console.format_info("Msg")
        
        # Test animations with mocked sleep
        with patch('time.sleep'):
            console.spinner("Loading", 0.1)
            console.pulse_animation("Pulse", 0.1)
            console.celebration()
        
        # Test progress bar
        with patch('specpulse.utils.console.track', return_value=[1, 2, 3]):
            list(console.progress_bar([1, 2, 3], "Test"))
        
        # Test prompts
        with patch('builtins.input', return_value='test'):
            result = console.prompt("Enter", "default")
            self.assertEqual(result, 'test')
        
        with patch('builtins.input', return_value=''):
            result = console.prompt("Enter", "default")
            self.assertEqual(result, "default")
        
        # Test prompt with choices
        with patch('builtins.input', side_effect=['invalid', 'valid']):
            result = console.prompt("Choose", choices=['valid'])
            self.assertEqual(result, 'valid')
        
        # Test confirm variations
        test_inputs = ['y', 'Y', 'yes', 'YES', 'n', 'N', 'no', 'NO', '', 'invalid']
        expected = [True, True, True, True, False, False, False, False, True, False]
        
        for inp, exp in zip(test_inputs, expected):
            with patch('builtins.input', return_value=inp):
                result = console.confirm("Test?", default=True)
                self.assertEqual(result, exp)
        
        with patch('builtins.input', return_value=''):
            result = console.confirm("Test?", default=False)
            self.assertFalse(result)
        
        # Test status context manager
        with console.status("Processing"):
            pass
        
        # Test clear
        with patch('os.system') as mock_system:
            console.clear()
            mock_system.assert_called()
        
        # Test print_exception
        try:
            raise ValueError("Test error")
        except:
            console.print_exception()
        
        # Test debug with verbose off
        console_quiet = Console(verbose=False)
        console_quiet.debug("Should not print")
    
    def test_git_utils_all_methods(self):
        """Test all GitUtils methods"""
        git = GitUtils()
        
        # Test all methods with success
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="output\n")
            
            self.assertTrue(git.check_git_installed())
            self.assertTrue(git.is_git_repo())
            self.assertTrue(git.init_repo())
            self.assertTrue(git.add_files("test.txt"))
            self.assertTrue(git.add_files(["file1.txt", "file2.txt"]))
            self.assertTrue(git.commit("Message"))
            self.assertEqual(git.get_current_branch(), "output")
            self.assertTrue(git.create_branch("feature"))
            self.assertTrue(git.checkout_branch("main"))
            self.assertEqual(git.get_status(), "output")
            self.assertEqual(git.get_log(n=10), "output")
            self.assertTrue(git.push("origin", "main"))
            self.assertTrue(git.pull("origin", "main"))
            self.assertEqual(git.get_remote_url("origin"), "output")
            self.assertTrue(git.add_remote("origin", "url"))
            self.assertTrue(git.tag("v1.0.0", "Message"))
            self.assertEqual(git.get_tags(), ["output"])
            self.assertTrue(git.stash("Message"))
            self.assertTrue(git.stash_pop())
        
        # Test all methods with failure
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=1, stdout="")
            
            self.assertFalse(git.is_git_repo())
            self.assertFalse(git.init_repo())
            self.assertFalse(git.add_files("test.txt"))
            self.assertFalse(git.commit("Message"))
            self.assertEqual(git.get_current_branch(), "main")
            self.assertFalse(git.create_branch("feature"))
            self.assertFalse(git.checkout_branch("main"))
            self.assertEqual(git.get_status(), "")
            self.assertEqual(git.get_log(), "")
            self.assertFalse(git.push())
            self.assertFalse(git.pull())
            self.assertEqual(git.get_remote_url(), "")
            self.assertFalse(git.add_remote("origin", "url"))
            self.assertFalse(git.tag("v1.0.0"))
            self.assertEqual(git.get_tags(), [])
            self.assertFalse(git.stash())
            self.assertFalse(git.stash_pop())
        
        # Test with FileNotFoundError
        with patch('subprocess.run', side_effect=FileNotFoundError()):
            self.assertFalse(git.check_git_installed())
        
        # Test with CalledProcessError
        with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'git')):
            self.assertFalse(git.is_git_repo())
    
    def test_cli_init_with_git(self):
        """Test CLI init with git integration"""
        with patch('specpulse.cli.main.GitUtils') as mock_git:
            mock_git_instance = mock_git.return_value
            mock_git_instance.check_git_installed.return_value = True
            mock_git_instance.is_git_repo.return_value = False
            mock_git_instance.init_repo.return_value = True
            
            cli = SpecPulseCLI()
            result = cli.init("test")
            self.assertTrue(result)
    
    def test_cli_sync_with_git(self):
        """Test CLI sync with git"""
        cli = SpecPulseCLI()
        cli.init(here=True)
        
        with patch('specpulse.cli.main.GitUtils') as mock_git:
            mock_git_instance = mock_git.return_value
            mock_git_instance.is_git_repo.return_value = True
            mock_git_instance.get_current_branch.return_value = "main"
            mock_git_instance.get_status.return_value = "modified: test.txt"
            
            result = cli.sync()
            self.assertTrue(result)
    
    def test_validator_validate_with_specs(self):
        """Test validator with spec files"""
        validator = Validator()
        
        # Create structure
        os.makedirs(".specpulse")
        os.makedirs("specs/001-feature")
        os.makedirs("plans/001-feature")
        
        # Create spec with NEEDS CLARIFICATION
        with open("specs/001-feature/spec.md", "w") as f:
            f.write("# Spec\n[NEEDS CLARIFICATION: something]")
        
        # Create plan
        with open("plans/001-feature/plan.md", "w") as f:
            f.write("# Plan\nContent")
        
        result = validator.validate_specifications(".")
        self.assertIsNotNone(result)
        self.assertFalse(result['valid'])  # Has NEEDS CLARIFICATION
        
        result = validator.validate_plans(".")
        self.assertIsNotNone(result)
        self.assertTrue(result['valid'])
    
    def test_cli_init_gemini(self):
        """Test CLI init with Gemini"""
        cli = SpecPulseCLI()
        result = cli.init("test", ai="gemini", template="cli")
        self.assertTrue(result)
        
        # Check Gemini files
        self.assertTrue(Path("test/.gemini/commands/pulse.toml").exists())
    
    def test_cli_validate_verbose_auto_fix(self):
        """Test CLI validate with verbose and auto-fix"""
        cli = SpecPulseCLI(verbose=True)
        cli.init(here=True)
        
        # Remove a directory to test auto-fix
        shutil.rmtree("specs")
        
        result = cli.validate(verbose=True, auto_fix=True)
        self.assertTrue(result)
        self.assertTrue(Path("specs").exists())  # Auto-fixed
    
    @patch('sys.argv', ['specpulse', 'validate', '--component', 'spec', '--verbose', '--auto-fix'])
    def test_main_validate_with_options(self):
        """Test main validate with all options"""
        cli = SpecPulseCLI()
        cli.init(here=True)
        main()
    
    @patch('sys.argv', ['specpulse', 'update'])
    def test_main_update(self):
        """Test main update command"""
        cli = SpecPulseCLI()
        cli.init(here=True)
        main()
    
    @patch('sys.argv', ['specpulse', 'sync'])  
    def test_main_sync(self):
        """Test main sync command"""
        cli = SpecPulseCLI()
        cli.init(here=True)
        main()
    
    def test_validator_path_conversion(self):
        """Test validator with string path conversion"""
        validator = Validator()
        
        # Create minimal structure
        os.makedirs(".specpulse")
        
        # Test with string path
        result = validator.validate_structure(os.getcwd())
        self.assertIsNotNone(result)
        
        # Test with Path object
        result = validator.validate_structure(Path.cwd())
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()