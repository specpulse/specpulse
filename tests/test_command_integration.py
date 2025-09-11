"""Integration test for AI command workflow."""
import os
import tempfile
import shutil
from pathlib import Path
import yaml


def test_command_workflow_simulation():
    """Simulate the complete AI command workflow."""
    
    # Create a temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Copy command files to test directory
        claude_src = Path("specpulse/resources/commands/claude")
        claude_dst = test_dir / ".claude" / "commands"
        claude_dst.mkdir(parents=True)
        
        for cmd_file in claude_src.glob("*.md"):
            shutil.copy(cmd_file, claude_dst / cmd_file.name)
        
        # Verify command files are in place
        assert (claude_dst / "pulse.md").exists()
        assert (claude_dst / "spec.md").exists()
        assert (claude_dst / "plan.md").exists()
        assert (claude_dst / "task.md").exists()
        
        # Simulate reading pulse command with arguments
        pulse_cmd = claude_dst / "pulse.md"
        with open(pulse_cmd, 'r') as f:
            content = f.read()
        
        # Verify it can handle arguments
        assert "$ARGUMENTS" in content
        assert "bash scripts/pulse-init.sh" in content
        
        # Parse frontmatter
        parts = content.split("---\n", 2)
        frontmatter = yaml.safe_load(parts[1])
        
        # Verify command metadata
        assert frontmatter["name"] == "pulse"
        assert "Bash" in frontmatter["allowed_tools"]
        
        # Simulate spec command with different actions
        spec_cmd = claude_dst / "spec.md"
        with open(spec_cmd, 'r') as f:
            content = f.read()
        
        # Verify action handling
        assert "create" in content.lower()
        assert "update" in content.lower()
        assert "validate" in content.lower()
        assert "$ARGUMENTS" in content
        
        # Test plan command
        plan_cmd = claude_dst / "plan.md"
        with open(plan_cmd, 'r') as f:
            content = f.read()
        
        # Verify phase gates are documented
        assert "Phase Gates" in content
        assert "generate" in content.lower()
        assert "validate" in content.lower()
        
        # Test task command
        task_cmd = claude_dst / "task.md"
        with open(task_cmd, 'r') as f:
            content = f.read()
        
        # Verify task actions
        assert "breakdown" in content.lower()
        assert "update" in content.lower()
        assert "status" in content.lower()
        assert "T001" in content  # Task format example


def test_argument_parsing_examples():
    """Test that command documentation includes clear argument examples."""
    
    command_examples = {
        "pulse": [
            "/pulse user-authentication",
            "/pulse payment-integration"
        ],
        "spec": [
            "/spec create user login with OAuth2",
            "/spec update",
            "/spec validate"
        ],
        "plan": [
            "/plan generate",
            "/plan validate"
        ],
        "task": [
            "/task breakdown",
            "/task update",
            "/task status"
        ]
    }
    
    claude_dir = Path("specpulse/resources/commands/claude")
    
    for cmd_name, examples in command_examples.items():
        cmd_file = claude_dir / f"{cmd_name}.md"
        with open(cmd_file, 'r') as f:
            content = f.read()
        
        # Check that at least one example is present
        has_example = any(
            example.replace(f"/{cmd_name}", "").strip() in content 
            or f"/{cmd_name}" in content
            for example in examples
        )
        assert has_example, f"{cmd_name}.md should include usage examples"


def test_frontmatter_consistency():
    """Test that all command files have consistent frontmatter structure."""
    
    claude_dir = Path("specpulse/resources/commands/claude")
    commands = []
    
    for cmd_file in sorted(claude_dir.glob("*.md")):
        with open(cmd_file, 'r') as f:
            content = f.read()
        
        parts = content.split("---\n", 2)
        frontmatter = yaml.safe_load(parts[1])
        commands.append({
            "file": cmd_file.name,
            "name": frontmatter.get("name"),
            "tools": frontmatter.get("allowed_tools", [])
        })
    
    # Verify all commands have names matching their filenames
    for cmd in commands:
        expected_name = cmd["file"].replace(".md", "")
        assert cmd["name"] == expected_name, \
            f"{cmd['file']} name should be {expected_name}"
    
    # Verify all commands can use Bash (for script execution)
    for cmd in commands:
        assert "Bash" in cmd["tools"], \
            f"{cmd['file']} should include Bash in allowed_tools"
    
    # Verify all commands can Read (for reading specs/plans)
    for cmd in commands:
        assert "Read" in cmd["tools"], \
            f"{cmd['file']} should include Read in allowed_tools"


def test_readme_command_documentation():
    """Test that README accurately documents the commands."""
    
    with open("README.md", 'r', encoding='utf-8') as f:
        readme = f.read()
    
    # Check that README shows commands accept arguments
    assert "/pulse user-authentication" in readme
    assert "/spec create" in readme
    assert "/plan generate" in readme
    assert "/task breakdown" in readme
    
    # Check that $ARGUMENTS is documented
    assert "$ARGUMENTS" in readme
    
    # Check both Claude and Gemini are mentioned
    assert "Claude" in readme
    assert "Gemini" in readme
    assert ".claude/commands/*.md" in readme
    assert ".gemini/commands/*.toml" in readme


if __name__ == "__main__":
    test_command_workflow_simulation()
    test_argument_parsing_examples()
    test_frontmatter_consistency()
    test_readme_command_documentation()
    print("✅ All command integration tests passed!")