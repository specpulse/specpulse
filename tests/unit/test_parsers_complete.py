"""
Comprehensive tests for CLI parsers.

This module provides thorough testing of all CLI argument parsers,
including subcommands, argument validation, and help text generation.

NOTE: This test file is currently skipped due to missing implementation.
BUG-010: Required parser setup functions and argument_validators module
are not implemented. This is a test template that needs implementation.
"""

import pytest

pytestmark = pytest.mark.skip(reason="BUG-010: Missing parser setup functions and argument_validators module")

# Commented out imports until implementation is added
# from specpulse.cli.parsers.subcommand_parsers import (
#     create_argument_parser, setup_feature_parser, setup_spec_parser,
#     setup_plan_parser, setup_task_parser, setup_execute_parser,
#     setup_template_parser, setup_checkpoint_parser
# )
# from specpulse.cli.parsers.argument_validators import (
#     validate_positive_integer, validate_feature_id_input,
#     validate_feature_name_input, validate_file_exists,
#     validate_directory_exists
# )


class TestArgumentValidators:
    """Test argument validation functions"""

    def test_validate_positive_integer_valid(self):
        """Test validation of valid positive integers"""
        valid_values = ["1", "42", "999", "1000"]

        for value in valid_values:
            assert validate_positive_integer(value) == int(value)

    def test_validate_positive_integer_invalid(self):
        """Test validation of invalid positive integers"""
        invalid_values = [
            "0",      # Zero
            "-1",     # Negative
            "1.5",    # Float
            "abc",    # Non-numeric
            "",       # Empty
            "1a",     # Mixed
            " 5 ",    # With spaces
        ]

        for value in invalid_values:
            with pytest.raises(argparse.ArgumentTypeError):
                validate_positive_integer(value)

    def test_validate_feature_id_input_valid(self):
        """Test validation of valid feature IDs"""
        valid_ids = ["001", "123", "999", "000"]

        for feature_id in valid_ids:
            result = validate_feature_id_input(feature_id)
            assert result == feature_id

    def test_validate_feature_id_input_invalid(self):
        """Test validation of invalid feature IDs"""
        invalid_ids = ["1", "1234", "abc", "12a", "01", "12"]

        for feature_id in invalid_ids:
            with pytest.raises(argparse.ArgumentTypeError):
                validate_feature_id_input(feature_id)

    def test_validate_feature_name_input_valid(self):
        """Test validation of valid feature names"""
        valid_names = [
            "user-auth",
            "data-processing",
            "api-integration",
            "simple",
            "a",  # Minimum length
        ]

        for name in valid_names:
            result = validate_feature_name_input(name)
            assert result == name

    def test_validate_feature_name_input_invalid(self):
        """Test validation of invalid feature names"""
        invalid_names = [
            "", "Feature Name", "feature_name", "123feature",
            "feature$", "feature@domain", "a" * 51, "-feature",
            "feature-", "feature--name", "FEATURE"
        ]

        for name in invalid_names:
            with pytest.raises(argparse.ArgumentTypeError):
                validate_feature_name_input(name)

    def test_validate_file_exists_valid(self, temp_dir):
        """Test validation of existing files"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        result = validate_file_exists(str(test_file))
        assert result == str(test_file)

    def test_validate_file_exists_invalid(self, temp_dir):
        """Test validation of non-existing files"""
        non_existent = str(temp_dir / "nonexistent.txt")

        with pytest.raises(argparse.ArgumentTypeError):
            validate_file_exists(non_existent)

    def test_validate_directory_exists_valid(self, temp_dir):
        """Test validation of existing directories"""
        result = validate_directory_exists(str(temp_dir))
        assert result == str(temp_dir)

    def test_validate_directory_exists_invalid(self, temp_dir):
        """Test validation of non-existing directories"""
        non_existent = str(temp_dir / "nonexistent")

        with pytest.raises(argparse.ArgumentTypeError):
            validate_directory_exists(non_existent)

    def test_validate_directory_exists_file(self, temp_dir):
        """Test validation when path exists but is a file"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        with pytest.raises(argparse.ArgumentTypeError):
            validate_directory_exists(str(test_file))


class TestMainParser:
    """Test main argument parser"""

    def test_create_argument_parser_structure(self):
        """Test parser structure and subcommands"""
        parser = create_argument_parser()

        assert parser.prog == "specpulse"
        assert parser.description is not None
        assert len(parser._subparsers._group_actions) > 0

    def test_parser_help_output(self):
        """Test parser help output"""
        parser = create_argument_parser()

        # Capture help output
        help_text = parser.format_help()

        assert "specpulse" in help_text
        assert "subcommands:" in help_text.lower() or "commands:" in help_text.lower()

    def test_parser_version_option(self):
        """Test version option"""
        parser = create_argument_parser()

        with pytest.raises(SystemExit):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                parser.parse_args(['--version'])

    def test_parser_global_options(self):
        """Test global options"""
        parser = create_argument_parser()

        # Test with verbose flag
        args = parser.parse_args(['spec', '--verbose', '001', 'test'])
        assert args.verbose is True

        # Test with no-color flag
        args = parser.parse_args(['spec', '--no-color', '001', 'test'])
        assert args.no_color is True

        # Test with both flags
        args = parser.parse_args(['spec', '--verbose', '--no-color', '001', 'test'])
        assert args.verbose is True
        assert args.no_color is True

    def test_parser_no_arguments(self):
        """Test parser with no arguments"""
        parser = create_argument_parser()

        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_invalid_subcommand(self):
        """Test parser with invalid subcommand"""
        parser = create_argument_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid_command'])


class TestFeatureParser:
    """Test feature subcommand parser"""

    def test_setup_feature_parser(self):
        """Test feature parser setup"""
        parser = setup_feature_parser()

        assert parser.prog == "specpulse feature"
        assert hasattr(parser, 'add_argument')

    def test_feature_create_arguments(self):
        """Test feature create arguments"""
        parser = setup_feature_parser()
        args = parser.parse_args(['create', '--name', 'user-auth', '--id', '001'])

        assert args.feature_command == 'create'
        assert args.name == 'user-auth'
        assert args.id == '001'

    def test_feature_create_with_decomposition(self):
        """Test feature create with decomposition option"""
        parser = setup_feature_parser()
        args = parser.parse_args([
            'create', '--name', 'user-auth', '--id', '001', '--decomposition'
        ])

        assert args.feature_command == 'create'
        assert args.name == 'user-auth'
        assert args.id == '001'
        assert args.decomposition is True

    def test_feature_list_arguments(self):
        """Test feature list arguments"""
        parser = setup_feature_parser()
        args = parser.parse_args(['list'])

        assert args.feature_command == 'list'

    def test_feature_list_with_format(self):
        """Test feature list with format option"""
        parser = setup_feature_parser()
        args = parser.parse_args(['list', '--format', 'json'])

        assert args.feature_command == 'list'
        assert args.format == 'json'

    def test_feature_show_arguments(self):
        """Test feature show arguments"""
        parser = setup_feature_parser()
        args = parser.parse_args(['show', '001'])

        assert args.feature_command == 'show'
        assert args.feature_id == '001'

    def test_feature_invalid_command(self):
        """Test feature parser with invalid command"""
        parser = setup_feature_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])

    def test_feature_create_missing_required_args(self):
        """Test feature create with missing required arguments"""
        parser = setup_feature_parser()

        # Missing name
        with pytest.raises(SystemExit):
            parser.parse_args(['create', '--id', '001'])

        # Missing id
        with pytest.raises(SystemExit):
            parser.parse_args(['create', '--name', 'user-auth'])

        # Missing both
        with pytest.raises(SystemExit):
            parser.parse_args(['create'])

    def test_feature_validation_invalid_id(self):
        """Test feature with invalid ID"""
        parser = setup_feature_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['create', '--name', 'test', '--id', 'invalid'])

    def test_feature_validation_invalid_name(self):
        """Test feature with invalid name"""
        parser = setup_feature_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['create', '--name', 'Invalid Name', '--id', '001'])


class TestSpecParser:
    """Test spec subcommand parser"""

    def test_setup_spec_parser(self):
        """Test spec parser setup"""
        parser = setup_spec_parser()

        assert parser.prog == "specpulse spec"
        assert hasattr(parser, 'add_argument')

    def test_spec_create_arguments(self):
        """Test spec create arguments"""
        parser = setup_spec_parser()
        args = parser.parse_args([
            'create', '--feature', '001', 'user-auth',
            '--input', 'input.md', '--number', '1'
        ])

        assert args.spec_command == 'create'
        assert args.feature == '001'
        assert args.user_auth == 'user-auth'  # Converted from feature name
        assert args.input == 'input.md'
        assert args.number == 1

    def test_spec_create_with_template(self):
        """Test spec create with template option"""
        parser = setup_spec_parser()
        args = parser.parse_args([
            'create', '--feature', '001', 'user-auth',
            '--input', 'input.md', '--template', 'custom.md'
        ])

        assert args.template == 'custom.md'

    def test_spec_create_without_optional_args(self):
        """Test spec create without optional arguments"""
        parser = setup_spec_parser()
        args = parser.parse_args([
            'create', '--feature', '001', 'user-auth', '--input', 'input.md'
        ])

        assert args.number is None  # Default
        assert args.template is None  # Default

    def test_spec_list_arguments(self):
        """Test spec list arguments"""
        parser = setup_spec_parser()
        args = parser.parse_args(['list', '--feature', '001', 'user-auth'])

        assert args.spec_command == 'list'
        assert args.feature == '001'

    def test_spec_show_arguments(self):
        """Test spec show arguments"""
        parser = setup_spec_parser()
        args = parser.parse_args([
            'show', '--feature', '001', 'user-auth', '--number', '2'
        ])

        assert args.spec_command == 'show'
        assert args.feature == '001'
        assert args.number == 2

    def test_spec_invalid_command(self):
        """Test spec parser with invalid command"""
        parser = setup_spec_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])

    def test_spec_create_missing_required_args(self):
        """Test spec create with missing required arguments"""
        parser = setup_spec_parser()

        # Missing feature
        with pytest.raises(SystemExit):
            parser.parse_args(['create', '--input', 'test.md'])

        # Missing input
        with pytest.raises(SystemExit):
            parser.parse_args(['create', '--feature', '001', 'user-auth'])


class TestPlanParser:
    """Test plan subcommand parser"""

    def test_setup_plan_parser(self):
        """Test plan parser setup"""
        parser = setup_plan_parser()

        assert parser.prog == "specpulse plan"
        assert hasattr(parser, 'add_argument')

    def test_plan_create_arguments(self):
        """Test plan create arguments"""
        parser = setup_plan_parser()
        args = parser.parse_args([
            'create', '--feature', '002', 'data-processing',
            '--input', 'input.md'
        ])

        assert args.plan_command == 'create'
        assert args.feature == '002'
        assert args.data_processing == 'data-processing'
        assert args.input == 'input.md'

    def test_plan_create_with_options(self):
        """Test plan create with optional arguments"""
        parser = setup_plan_parser()
        args = parser.parse_args([
            'create', '--feature', '002', 'data-processing',
            '--input', 'input.md', '--template', 'plan_template.md',
            '--implementation', 'yes'
        ])

        assert args.template == 'plan_template.md'
        assert args.implementation == 'yes'

    def test_plan_list_arguments(self):
        """Test plan list arguments"""
        parser = setup_plan_parser()
        args = parser.parse_args(['list'])

        assert args.plan_command == 'list'

    def test_plan_show_arguments(self):
        """Test plan show arguments"""
        parser = setup_plan_parser()
        args = parser.parse_args([
            'show', '--feature', '002', 'data-processing', '--number', '1'
        ])

        assert args.plan_command == 'show'
        assert args.feature == '002'

    def test_plan_invalid_command(self):
        """Test plan parser with invalid command"""
        parser = setup_plan_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])


class TestTaskParser:
    """Test task subcommand parser"""

    def test_setup_task_parser(self):
        """Test task parser setup"""
        parser = setup_task_parser()

        assert parser.prog == "specpulse task"
        assert hasattr(parser, 'add_argument')

    def test_task_create_arguments(self):
        """Test task create arguments"""
        parser = setup_task_parser()
        args = parser.parse_args([
            'create', '--feature', '003', 'api-integration',
            '--input', 'input.md', '--priority', 'high'
        ])

        assert args.task_command == 'create'
        assert args.feature == '003'
        assert args.api_integration == 'api-integration'
        assert args.input == 'input.md'
        assert args.priority == 'high'

    def test_task_create_with_assignee(self):
        """Test task create with assignee option"""
        parser = setup_task_parser()
        args = parser.parse_args([
            'create', '--feature', '003', 'api-integration',
            '--input', 'input.md', '--assignee', 'developer'
        ])

        assert args.assignee == 'developer'

    def test_task_list_arguments(self):
        """Test task list arguments"""
        parser = setup_task_parser()
        args = parser.parse_args(['list', '--feature', '003'])

        assert args.task_command == 'list'
        assert args.feature == '003'

    def test_task_list_with_status(self):
        """Test task list with status filter"""
        parser = setup_task_parser()
        args = parser.parse_args(['list', '--feature', '003', '--status', 'completed'])

        assert args.status == 'completed'

    def test_task_show_arguments(self):
        """Test task show arguments"""
        parser = setup_task_parser()
        args = parser.parse_args([
            'show', '--feature', '003', 'api-integration', '--number', '2'
        ])

        assert args.task_command == 'show'
        assert args.feature == '003'
        assert args.number == 2

    def test_task_invalid_command(self):
        """Test task parser with invalid command"""
        parser = setup_task_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])


class TestExecuteParser:
    """Test execute subcommand parser"""

    def test_setup_execute_parser(self):
        """Test execute parser setup"""
        parser = setup_execute_parser()

        assert parser.prog == "specpulse execute"
        assert hasattr(parser, 'add_argument')

    def test_execute_plan_arguments(self):
        """Test execute plan arguments"""
        parser = setup_execute_parser()
        args = parser.parse_args([
            'plan', '--feature', '004', 'user-interface',
            '--number', '1'
        ])

        assert args.execute_command == 'plan'
        assert args.feature == '004'
        assert args.user_interface == 'user-interface'
        assert args.number == 1

    def test_execute_task_arguments(self):
        """Test execute task arguments"""
        parser = setup_execute_parser()
        args = parser.parse_args([
            'task', '--feature', '004', 'user-interface',
            '--number', '3'
        ])

        assert args.execute_command == 'task'
        assert args.feature == '004'
        assert args.number == 3

    def test_execute_invalid_command(self):
        """Test execute parser with invalid command"""
        parser = setup_execute_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])


class TestTemplateParser:
    """Test template subcommand parser"""

    def test_setup_template_parser(self):
        """Test template parser setup"""
        parser = setup_template_parser()

        assert parser.prog == "specpulse template"
        assert hasattr(parser, 'add_argument')

    def test_template_list_arguments(self):
        """Test template list arguments"""
        parser = setup_template_parser()
        args = parser.parse_args(['list'])

        assert args.template_command == 'list'

    def test_template_show_arguments(self):
        """Test template show arguments"""
        parser = setup_template_parser()
        args = parser.parse_args(['show', 'spec.md'])

        assert args.template_command == 'show'
        assert args.template_name == 'spec.md'

    def test_template_update_arguments(self):
        """Test template update arguments"""
        parser = setup_template_parser()
        args = parser.parse_args([
            'update', '--template', 'spec.md',
            '--content', 'New content'
        ])

        assert args.template_command == 'update'
        assert args.template == 'spec.md'
        assert args.content == 'New content'

    def test_template_invalid_command(self):
        """Test template parser with invalid command"""
        parser = setup_template_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])


class TestCheckpointParser:
    """Test checkpoint subcommand parser"""

    def test_setup_checkpoint_parser(self):
        """Test checkpoint parser setup"""
        parser = setup_checkpoint_parser()

        assert parser.prog == "specpulse checkpoint"
        assert hasattr(parser, 'add_argument')

    def test_checkpoint_create_arguments(self):
        """Test checkpoint create arguments"""
        parser = setup_checkpoint_parser()
        args = parser.parse_args([
            'create', '--feature', '005', 'data-validation',
            '--description', 'Validation checkpoint'
        ])

        assert args.checkpoint_command == 'create'
        assert args.feature == '005'
        assert args.data_validation == 'data-validation'
        assert args.description == 'Validation checkpoint'

    def test_checkpoint_list_arguments(self):
        """Test checkpoint list arguments"""
        parser = setup_checkpoint_parser()
        args = parser.parse_args(['list'])

        assert args.checkpoint_command == 'list'

    def test_checkpoint_show_arguments(self):
        """Test checkpoint show arguments"""
        parser = setup_checkpoint_parser()
        args = parser.parse_args(['show', 'checkpoint_001'])

        assert args.checkpoint_command == 'show'
        assert args.checkpoint_id == 'checkpoint_001'

    def test_checkpoint_invalid_command(self):
        """Test checkpoint parser with invalid command"""
        parser = setup_checkpoint_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(['invalid'])


class TestParserIntegration:
    """Test parser integration and edge cases"""

    def test_feature_name_conversion(self):
        """Test feature name conversion to argument name"""
        parser = setup_feature_parser()
        args = parser.parse_args(['create', '--name', 'user-auth', '--id', '001'])

        # The feature name should be converted to a valid argument name
        assert hasattr(args, 'user_auth') is False  # Should not have this
        assert args.name == 'user-auth'

    def test_multiple_feature_names(self):
        """Test parser with different feature names"""
        feature_names = [
            'user-auth',
            'data-processing',
            'api-integration',
            'user-interface',
            'data-validation'
        ]

        for feature_name in feature_names:
            parser = setup_spec_parser()
            args = parser.parse_args([
                'create', '--feature', '001', feature_name,
                '--input', 'input.md'
            ])
            assert hasattr(args, feature_name.replace('-', '_'))

    def test_parser_error_messages(self):
        """Test parser error messages are informative"""
        parser = setup_feature_parser()

        # Capture stderr to check error messages
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            try:
                parser.parse_args(['create', '--name', 'Invalid Name', '--id', '001'])
            except SystemExit:
                pass

        error_output = mock_stderr.getvalue()
        # Should contain some error information
        assert len(error_output) > 0

    def test_parser_with_unicode(self):
        """Test parser handling of unicode characters"""
        parser = setup_feature_parser()

        # Test with unicode in description (if any)
        try:
            args = parser.parse_args(['list'])
            # Should not raise Unicode errors
            assert args.feature_command == 'list'
        except UnicodeError:
            pytest.fail("Parser should handle unicode characters")

    def test_parser_help_encoding(self):
        """Test parser help output encoding"""
        parser = create_argument_parser()

        # Should not raise encoding errors
        try:
            help_text = parser.format_help()
            assert isinstance(help_text, str)
        except UnicodeError:
            pytest.fail("Help text should be properly encoded")

    def test_subparser_help(self):
        """Test subcommand help generation"""
        main_parser = create_argument_parser()

        # Get help for specific subcommand
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                main_parser.parse_args(['spec', '--help'])
            except SystemExit:
                pass

        help_output = mock_stdout.getvalue()
        assert 'spec' in help_output.lower()

    def test_argument_defaults(self):
        """Test argument defaults are properly set"""
        parser = setup_feature_parser()
        args = parser.parse_args(['create', '--name', 'test', '--id', '001'])

        # Check default values
        assert args.decomposition is False  # Default should be False

    def test_argument_choices(self):
        """Test argument choices validation"""
        parser = setup_feature_parser()

        # Test with valid format choice
        args = parser.parse_args(['list', '--format', 'table'])
        assert args.format == 'table'

        # Test with invalid format choice
        with pytest.raises(SystemExit):
            parser.parse_args(['list', '--format', 'invalid'])

    def test_argument_counts(self):
        """Test argument count validation (nargs)"""
        # This would test nargs parameter if any parsers use it
        # Currently, all parsers use single arguments, but this is here for completeness
        pass

    def test_parser_mutability(self):
        """Test that parser objects are not modified unexpectedly"""
        parser1 = setup_feature_parser()
        parser2 = setup_feature_parser()

        # Both parsers should have the same configuration
        assert parser1.prog == parser2.prog

        # Parsing with one shouldn't affect the other
        args1 = parser1.parse_args(['list'])
        args2 = parser2.parse_args(['list'])

        assert args1.feature_command == args2.feature_command


if __name__ == "__main__":
    pytest.main([__file__])