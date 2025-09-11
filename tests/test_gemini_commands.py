"""Test Gemini command files follow the official format."""
import toml
from pathlib import Path


def test_gemini_commands_have_correct_format():
    """Test that Gemini command files follow the official format."""
    gemini_commands_dir = Path("specpulse/resources/commands/gemini")
    
    for cmd_file in gemini_commands_dir.glob("*.toml"):
        with open(cmd_file, 'r') as f:
            content = toml.load(f)
        
        # Check required fields according to Gemini docs
        assert "prompt" in content, f"{cmd_file.name} missing 'prompt' field"
        assert isinstance(content["prompt"], str), f"{cmd_file.name} prompt must be a string"
        
        # Check optional description field
        if "description" in content:
            assert isinstance(content["description"], str), f"{cmd_file.name} description must be a string"
        
        # Should NOT have complex nested structures (old format)
        assert "command" not in content, f"{cmd_file.name} uses old complex format, should only have 'prompt' and optional 'description'"
        
        print(f"[PASS] {cmd_file.name} follows official Gemini format")


def test_gemini_commands_handle_arguments():
    """Test that Gemini commands properly handle arguments."""
    gemini_commands_dir = Path("specpulse/resources/commands/gemini")
    
    for cmd_file in gemini_commands_dir.glob("*.toml"):
        with open(cmd_file, 'r') as f:
            content = toml.load(f)
        
        prompt = content.get("prompt", "")
        
        # Check that prompts use {{args}} placeholder for arguments
        assert "{{args}}" in prompt, f"{cmd_file.name} should use {{{{args}}}} placeholder for arguments"
        
        # Check that prompts handle the case appropriately (either mention "no" or have defaults)
        handles_no_args = (
            ("no" in prompt.lower() and "provided" in prompt.lower()) or
            "otherwise" in prompt.lower() or
            "default" in prompt.lower() or
            "if" in prompt.lower()
        )
        assert handles_no_args, \
            f"{cmd_file.name} should explain how arguments are handled"
        
        print(f"[PASS] {cmd_file.name} properly handles arguments")


def test_gemini_commands_have_examples():
    """Test that Gemini commands include usage examples."""
    gemini_commands_dir = Path("specpulse/resources/commands/gemini")
    
    for cmd_file in gemini_commands_dir.glob("*.toml"):
        with open(cmd_file, 'r') as f:
            content = toml.load(f)
        
        prompt = content.get("prompt", "")
        cmd_name = cmd_file.stem
        
        # Check for examples in the prompt
        assert "example" in prompt.lower() or f"/{cmd_name}" in prompt.lower(), \
            f"{cmd_file.name} should include usage examples"
        
        print(f"[PASS] {cmd_file.name} includes examples")


def test_gemini_commands_use_special_syntax():
    """Test that Gemini commands use special syntax features where appropriate."""
    gemini_commands_dir = Path("specpulse/resources/commands/gemini")
    
    special_syntax_used = {
        "pulse": False,  # Should use !{bash ...} for shell commands
        "spec": False,   # Should use @{...} for file injection
        "plan": False,   # Should use @{...} for file injection
        "task": False    # Should use @{...} for file injection
    }
    
    for cmd_file in gemini_commands_dir.glob("*.toml"):
        with open(cmd_file, 'r') as f:
            content = toml.load(f)
        
        prompt = content.get("prompt", "")
        cmd_name = cmd_file.stem
        
        # Check for special syntax
        if cmd_name == "pulse":
            # pulse should use shell command execution
            if "!{" in prompt:
                special_syntax_used[cmd_name] = True
                print(f"[PASS] {cmd_file.name} uses !{{...}} for shell commands")
        else:
            # Other commands should use file injection
            if "@{" in prompt:
                special_syntax_used[cmd_name] = True
                print(f"[PASS] {cmd_file.name} uses @{{...}} for file injection")
    
    # Verify each command uses appropriate special syntax
    assert special_syntax_used["pulse"], "pulse.toml should use !{...} for shell execution"
    assert special_syntax_used["spec"], "spec.toml should use @{...} for file injection"
    assert special_syntax_used["plan"], "plan.toml should use @{...} for file injection"
    assert special_syntax_used["task"], "task.toml should use @{...} for file injection"


def test_claude_and_gemini_parity():
    """Test that Claude and Gemini commands cover the same functionality."""
    claude_dir = Path("specpulse/resources/commands/claude")
    gemini_dir = Path("specpulse/resources/commands/gemini")
    
    claude_commands = {f.stem for f in claude_dir.glob("*.md")}
    gemini_commands = {f.stem for f in gemini_dir.glob("*.toml")}
    
    # Both should have the same commands
    assert claude_commands == gemini_commands, \
        f"Command parity mismatch. Claude: {claude_commands}, Gemini: {gemini_commands}"
    
    print(f"[PASS] Claude and Gemini have parity: {claude_commands}")


if __name__ == "__main__":
    test_gemini_commands_have_correct_format()
    test_gemini_commands_handle_arguments()
    test_gemini_commands_have_examples()
    test_gemini_commands_use_special_syntax()
    test_claude_and_gemini_parity()
    print("\n[SUCCESS] All Gemini command tests passed!")