"""Test to achieve 100% coverage by covering all missing lines"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import tempfile
import shutil
import os
import subprocess
import sys

# Import all modules to test
from specpulse import __version__
from specpulse.cli.main import SpecPulseCLI, main
from specpulse.core.specpulse import SpecPulse
from specpulse.core.validator import Validator
from specpulse.utils.console import Console
from specpulse.utils.git_utils import GitUtils


class Test100Coverage(unittest.TestCase):
    """Tests specifically targeting missing coverage lines"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        os.chdir(self.original_cwd)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_cli_main_missing_lines(self):
        """Cover missing lines in cli/main.py (lines 40-41, 228-229, etc)"""
        cli = SpecPulseCLI(no_color=True, verbose=True)
        
        # Lines 40-41: Init with template that doesn't exist
        with patch('pathlib.Path.exists', return_value=False):
            cli.init("test", template="nonexistent")
        
        # Lines 228-229, 237-238, etc: Error handling in init
        with patch('os.makedirs', side_effect=OSError("Permission")):
            result = cli.init("test2")
            self.assertFalse(result)
        
        # Lines 246-247, 255-256: File write errors
        with patch('builtins.open', side_effect=IOError("Permission")):
            result = cli.init("test3")
            self.assertFalse(result)
        
        # Create project for further tests
        cli.init(here=True)
        
        # Lines 367-412: Doctor command error paths
        with patch('pathlib.Path.exists', return_value=False):
            result = cli.doctor()
            self.assertFalse(result)
        
        # Lines 425-433: Validate error paths
        with patch('pathlib.Path.exists', return_value=False):
            result = cli.validate()
            self.assertFalse(result)
        
        # Lines 481: Sync with specific error
        with patch('pathlib.Path.exists', return_value=False):
            result = cli.sync()
            self.assertFalse(result)
        
        # Lines 506, 515, 524, 533, 538: Update command paths
        with patch('pathlib.Path.exists', return_value=False):
            result = cli.update()
            self.assertFalse(result)
        
        # Lines 549-550: Update with missing source files
        with patch('shutil.copy2', side_effect=IOError("Error")):
            result = cli.update()
            self.assertFalse(result)
        
        # Lines 567: Main function error handling
        with patch('sys.argv', ['specpulse', 'invalid-command']):
            with patch('sys.exit'):
                main()
    
    def test_cli_main_lines_574_628(self):
        """Cover main function lines 574-628"""
        # Test all main function command paths
        test_cases = [
            (['specpulse', 'init', 'test'], None),
            (['specpulse', 'init', '--here'], None),
            (['specpulse', 'doctor'], None),
            (['specpulse', 'validate'], None),
            (['specpulse', 'validate', '--component', 'spec'], None),
            (['specpulse', 'validate', '--verbose'], None),
            (['specpulse', 'sync'], None),
            (['specpulse', 'update'], None),
        ]
        
        # Create a project first
        cli = SpecPulseCLI()
        cli.init(here=True)
        
        for args, expected in test_cases:
            with patch('sys.argv', args):
                try:
                    main()
                except SystemExit:
                    pass
    
    def test_specpulse_core_missing_lines(self):
        """Cover missing lines in core/specpulse.py"""
        sp = SpecPulse()
        
        # Line 38: Resource path that doesn't exist
        with patch('importlib.resources.files', side_effect=Exception("Error")):
            path = sp.get_resource_path("test.txt")
            self.assertIsNone(path)
        
        # Line 122: Template that doesn't exist
        with patch('pathlib.Path.exists', return_value=False):
            content = sp.get_template_content("nonexistent")
            self.assertEqual(content, "")
        
        # Lines for each command/script method when file doesn't exist
        with patch('pathlib.Path.exists', return_value=False):
            # Line 322
            self.assertEqual(sp.get_claude_pulse_command(), "")
            # Line 412
            self.assertEqual(sp.get_claude_spec_command(), "")
            # Line 492
            self.assertEqual(sp.get_claude_plan_command(), "")
            # Line 536
            self.assertEqual(sp.get_claude_task_command(), "")
            # Line 561
            self.assertEqual(sp.get_gemini_pulse_command(), "")
            # Line 615
            self.assertEqual(sp.get_gemini_spec_command(), "")
            # Line 658
            self.assertEqual(sp.get_gemini_plan_command(), "")
            # Line 705
            self.assertEqual(sp.get_gemini_task_command(), "")
            # Line 750
            self.assertEqual(sp.get_pulse_init_script(), "")
            # Line 801
            self.assertEqual(sp.get_pulse_spec_script(), "")
            # Line 916
            self.assertEqual(sp.get_pulse_plan_script(), "")
            # Line 924
            self.assertEqual(sp.get_pulse_task_script(), "")
            # Line 932
            self.assertEqual(sp.get_constitution_template(), "")
            # Line 940
            self.assertEqual(sp.get_context_template(), "")
            # Line 949
            self.assertEqual(sp.get_decisions_template(), "")
            # Line 957
            self.assertEqual(sp.get_pulse_manifest(), "")
            # Line 965
            self.assertEqual(sp.get_resource_content("nonexistent"), "")
            # Line 973
            self.assertEqual(sp.read_file(Path("nonexistent")), "")
    
    def test_validator_missing_lines(self):
        """Cover missing lines in core/validator.py"""
        validator = Validator()
        
        # Lines 42-46, 49-53: Check methods with missing files
        self.assertFalse(validator.check_directory_exists("nonexistent"))
        self.assertFalse(validator.check_file_exists("nonexistent"))
        self.assertFalse(validator.check_file_not_empty("nonexistent"))
        
        # Create empty file
        with open("empty.txt", "w"):
            pass
        self.assertFalse(validator.check_file_not_empty("empty.txt"))
        
        # Lines 70-97: Validation methods with missing structure
        result = validator.validate_structure(".")
        self.assertFalse(result['valid'])
        
        # Create minimal structure
        os.makedirs(".specpulse")
        os.makedirs("specs")
        os.makedirs("plans")
        os.makedirs("memory")
        
        # Lines 163-167: Validate specs with files
        os.makedirs("specs/001-test")
        with open("specs/001-test/spec.md", "w") as f:
            f.write("[NEEDS CLARIFICATION: test]")
        
        result = validator.validate_specifications(".")
        self.assertFalse(result['valid'])  # Has clarification needed
        
        # Line 192: Validate plans
        os.makedirs("plans/001-test")
        with open("plans/001-test/plan.md", "w") as f:
            f.write("# Plan")
        
        result = validator.validate_plans(".")
        self.assertTrue(result['valid'])
        
        # Lines 199-240: Validate constitution
        with open("memory/constitution.md", "w") as f:
            f.write("# Constitution\n[NEEDS CLARIFICATION: test]")
        
        result = validator.validate_constitution(".")
        self.assertFalse(result['valid'])
        
        # Lines 251-255: Auto fix with missing dirs
        shutil.rmtree("specs")
        validator.auto_fix(".")
        self.assertTrue(Path("specs").exists())
        
        # Lines 269-273: Auto fix with missing files
        os.remove("memory/constitution.md")
        validator.auto_fix(".")
        self.assertTrue(Path("memory/constitution.md").exists())
        
        # Line 329: Validate all
        result = validator.validate_all(".")
        self.assertIsNotNone(result)
    
    def test_console_missing_lines(self):
        """Cover missing lines in utils/console.py"""
        console = Console(no_color=False, verbose=True)
        
        # Line 113: Panel with all options
        console.panel("Content", title="Title", subtitle="Subtitle", style="green")
        
        # Lines 140-143: Status context manager
        with console.status("Processing"):
            pass
        
        # Lines 185-187: Clear screen
        with patch('os.system') as mock_system:
            console.clear()
            mock_system.assert_called()
        
        # Lines 191-200: Print exception
        try:
            raise ValueError("Test error")
        except:
            console.print_exception()
        
        # Lines 294-298: Prompt with choices validation
        with patch('builtins.input', side_effect=['invalid', 'invalid2', 'valid']):
            result = console.prompt("Choose", choices=['valid', 'other'])
            self.assertEqual(result, 'valid')
        
        # Lines 302-303: Confirm with various inputs
        with patch('builtins.input', return_value='maybe'):
            result = console.confirm("Test?")
            self.assertFalse(result)
        
        # Line 308: Debug with verbose off
        console_quiet = Console(verbose=False)
        console_quiet.debug("Should not print")
    
    def test_git_utils_all_missing_lines(self):
        """Cover ALL missing lines in utils/git_utils.py"""
        git = GitUtils()
        
        # Line 14: Check git installed - not found
        with patch('subprocess.run', side_effect=FileNotFoundError()):
            self.assertFalse(git.check_git_installed())
        
        # Lines 18-30: All success paths
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="output\n")
            
            self.assertTrue(git.is_git_repo())
            self.assertTrue(git.init_repo())
            self.assertTrue(git.add_files("file.txt"))
            self.assertTrue(git.add_files(["f1", "f2"]))
            self.assertTrue(git.commit("msg"))
            self.assertEqual(git.get_current_branch(), "output")
            self.assertTrue(git.create_branch("branch"))
            self.assertTrue(git.checkout_branch("main"))
        
        # Lines 34-35, 39-41, etc: All failure paths
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=1, stdout="", stderr="error")
            
            self.assertFalse(git.is_git_repo())
            self.assertFalse(git.init_repo())
            self.assertFalse(git.add_files("file"))
            self.assertFalse(git.commit("msg"))
            self.assertEqual(git.get_current_branch(), "main")
            self.assertFalse(git.create_branch("b"))
            self.assertFalse(git.checkout_branch("b"))
            self.assertEqual(git.get_status(), "")
            self.assertEqual(git.get_log(), "")
            self.assertEqual(git.get_log(5), "")
            self.assertFalse(git.push())
            self.assertFalse(git.push("origin", "main"))
            self.assertFalse(git.pull())
            self.assertFalse(git.pull("origin", "main"))
            self.assertEqual(git.get_remote_url(), "")
            self.assertEqual(git.get_remote_url("upstream"), "")
            self.assertFalse(git.add_remote("origin", "url"))
            self.assertFalse(git.tag("v1"))
            self.assertFalse(git.tag("v1", "msg"))
            self.assertEqual(git.get_tags(), [])
            self.assertFalse(git.stash())
            self.assertFalse(git.stash("msg"))
            self.assertFalse(git.stash_pop())
        
        # Exception handling
        with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'git')):
            self.assertFalse(git.is_git_repo())
        
        # More success cases with different outputs
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="line1\nline2\nline3")
            tags = git.get_tags()
            self.assertEqual(tags, ["line1", "line2", "line3"])
        
        # Empty output
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="")
            self.assertEqual(git.get_tags(), [])
            self.assertEqual(git.get_status(), "")
            self.assertEqual(git.get_log(), "")


if __name__ == '__main__':
    unittest.main()