"""Test AI command files are properly formatted and functional."""
import os
import yaml
import toml
from pathlib import Path


def test_claude_commands_have_frontmatter():
    """Test that Claude command files have proper frontmatter."""
    claude_commands_dir = Path("specpulse/resources/commands/claude")
    
    required_fields = ["name", "description", "allowed_tools"]
    
    for cmd_file in claude_commands_dir.glob("*.md"):
        with open(cmd_file, 'r') as f:
            content = f.read()
            
        # Check for frontmatter
        assert content.startswith("---\n"), f"{cmd_file.name} missing frontmatter"
        
        # Extract frontmatter
        parts = content.split("---\n", 2)
        assert len(parts) >= 3, f"{cmd_file.name} invalid frontmatter format"
        
        # Parse YAML frontmatter
        frontmatter = yaml.safe_load(parts[1])
        
        # Check required fields
        for field in required_fields:
            assert field in frontmatter, f"{cmd_file.name} missing {field} in frontmatter"
        
        # Check allowed_tools is a list
        assert isinstance(frontmatter["allowed_tools"], list), f"{cmd_file.name} allowed_tools must be a list"
        
        # Check implementation section mentions $ARGUMENTS
        if "Implementation" in content:
            assert "$ARGUMENTS" in content or "no arguments" in content.lower(), \
                f"{cmd_file.name} should document how arguments are handled"


def test_gemini_commands_have_proper_structure():
    """Test that Gemini command files have proper TOML structure."""
    gemini_commands_dir = Path("specpulse/resources/commands/gemini")
    
    for cmd_file in gemini_commands_dir.glob("*.toml"):
        with open(cmd_file, 'r') as f:
            content = toml.load(f)
        
        # Check for the official Gemini format
        assert "prompt" in content, f"{cmd_file.name} missing required 'prompt' field"
        
        # Optional description field
        if "description" in content:
            assert isinstance(content["description"], str), f"{cmd_file.name} description must be a string"


def test_command_scripts_exist():
    """Test that referenced shell scripts exist."""
    scripts_to_check = [
        "scripts/pulse-init.sh",
        "scripts/pulse-spec.sh", 
        "scripts/pulse-plan.sh",
        "scripts/pulse-task.sh"
    ]
    
    # Check from Claude command files
    claude_commands_dir = Path("specpulse/resources/commands/claude")
    for cmd_file in claude_commands_dir.glob("*.md"):
        with open(cmd_file, 'r') as f:
            content = f.read()
        
        # Look for script references
        if "scripts/" in content:
            # Extract script paths
            import re
            scripts = re.findall(r'scripts/[a-z-]+\.sh', content)
            for script in scripts:
                # Note: Scripts would be created when initializing a project
                # This test just ensures they're properly referenced
                assert script in scripts_to_check or "example" in content.lower(), \
                    f"{cmd_file.name} references unknown script: {script}"


def test_command_usage_examples():
    """Test that command files have usage examples."""
    claude_commands_dir = Path("specpulse/resources/commands/claude")
    
    for cmd_file in claude_commands_dir.glob("*.md"):
        with open(cmd_file, 'r') as f:
            content = f.read()
        
        # Check for usage section
        assert "## Usage" in content or "## Example" in content, \
            f"{cmd_file.name} missing usage examples"
        
        # Check for command examples with /
        assert f"/{cmd_file.stem}" in content, \
            f"{cmd_file.name} should include example with /{cmd_file.stem}"


def test_command_argument_handling():
    """Test that commands properly document argument handling."""
    claude_commands_dir = Path("specpulse/resources/commands/claude")
    
    # Commands that should accept arguments
    commands_with_args = {
        "pulse": ["<feature-name>"],
        "spec": ["[action]", "[description]"],
        "plan": ["[action]"],
        "task": ["[action]"]
    }
    
    for cmd_name, expected_args in commands_with_args.items():
        cmd_file = claude_commands_dir / f"{cmd_name}.md"
        if cmd_file.exists():
            with open(cmd_file, 'r') as f:
                content = f.read()
            
            # Check that usage shows arguments
            for arg in expected_args:
                assert arg in content or "arguments" in content.lower(), \
                    f"{cmd_file.name} should document argument: {arg}"
            
            # Check $ARGUMENTS is used in implementation
            if "bash" in content.lower():
                assert "$ARGUMENTS" in content, \
                    f"{cmd_file.name} should use $ARGUMENTS for passing arguments to scripts"


if __name__ == "__main__":
    test_claude_commands_have_frontmatter()
    test_gemini_commands_have_proper_structure()
    test_command_scripts_exist()
    test_command_usage_examples()
    test_command_argument_handling()
    print("✅ All AI command tests passed!")