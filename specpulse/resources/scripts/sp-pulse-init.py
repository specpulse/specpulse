#!/usr/bin/env python3
"""
SpecPulse Feature Initialization Script
Cross-platform Python equivalent of pulse-init.sh
"""

import os
import sys
import subprocess
import re
import datetime
from pathlib import Path

class SpecPulseInit:
    def __init__(self):
        self.script_name = Path(__file__).name
        self.project_root = Path(__file__).parent.parent
        self.memory_dir = self.project_root / "memory"
        self.context_file = self.memory_dir / "context.md"
        self.templates_dir = self.project_root / "templates"
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.script_name}: {message}", file=sys.stderr)
        
    def error_exit(self, message):
        """Exit with error message"""
        self.log(f"ERROR: {message}")
        sys.exit(1)
        
    def sanitize_feature_name(self, feature_name):
        """Sanitize feature name for safe directory naming"""
        if not feature_name:
            self.error_exit("Feature name cannot be empty")
        
        # Convert to lowercase, replace spaces and special chars with hyphens
        sanitized = re.sub(r'[^a-z0-9-]', '-', feature_name.lower())
        sanitized = re.sub(r'-+', '-', sanitized)  # Remove consecutive hyphens
        sanitized = sanitized.strip('-')  # Remove leading/trailing hyphens
        
        if not sanitized:
            self.error_exit(f"Invalid feature name: '{feature_name}'")
            
        return sanitized
        
    def get_feature_id(self, custom_id=None):
        """Get next feature ID"""
        if custom_id:
            return f"{int(custom_id):03d}"
        
        # Find existing feature directories
        specs_dir = self.project_root / "specs"
        if specs_dir.exists():
            existing = [d for d in specs_dir.iterdir() if d.is_dir() and d.name.isdigit()]
            next_id = len(existing) + 1
        else:
            next_id = 1
            
        return f"{next_id:03d}"
        
    def create_directories(self, branch_name):
        """Create feature directories"""
        dirs_to_create = [
            self.project_root / "specs" / branch_name,
            self.project_root / "plans" / branch_name,
            self.project_root / "tasks" / branch_name
        ]
        
        for directory in dirs_to_create:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                self.log(f"Created directory: {directory}")
            except Exception as e:
                self.error_exit(f"Failed to create directory {directory}: {e}")
                
    def copy_templates(self, branch_name):
        """Copy templates to feature directories"""
        templates = {
            "spec.md": self.project_root / "specs" / branch_name / "spec-001.md",
            "plan.md": self.project_root / "plans" / branch_name / "plan-001.md",
            "task.md": self.project_root / "tasks" / branch_name / "task-001.md"
        }
        
        for template_name, target_path in templates.items():
            template_path = self.templates_dir / template_name
            if not template_path.exists():
                self.error_exit(f"Template not found: {template_path}")
                
            try:
                target_path.write_text(template_path.read_text())
                self.log(f"Copied template to: {target_path}")
            except Exception as e:
                self.error_exit(f"Failed to copy template {template_path}: {e}")
                
    def update_context(self, feature_name, feature_id, branch_name):
        """Update context file"""
        try:
            self.memory_dir.mkdir(parents=True, exist_ok=True)
            
            context_entry = f"""

## Active Feature: {feature_name}
- Feature ID: {feature_id}
- Branch: {branch_name}
- Started: {datetime.datetime.now().isoformat()}
"""
            
            with open(self.context_file, 'a', encoding='utf-8') as f:
                f.write(context_entry)
                
            self.log(f"Updated context file: {self.context_file}")
        except Exception as e:
            self.error_exit(f"Failed to update context file: {e}")
            
    def create_git_branch(self, branch_name):
        """Create git branch if in git repository"""
        git_dir = self.project_root / ".git"
        if not git_dir.exists():
            return
            
        try:
            # Check if branch already exists
            result = subprocess.run(
                ["git", "branch", "--list", branch_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if branch_name in result.stdout:
                self.log(f"Git branch '{branch_name}' already exists, checking out")
                subprocess.run(["git", "checkout", branch_name], cwd=self.project_root, check=True)
            else:
                self.log(f"Creating new git branch '{branch_name}'")
                subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            self.error_exit(f"Git operation failed: {e}")
            
    def main(self, args):
        """Main execution function"""
        if len(args) < 1:
            self.error_exit("Usage: python sp-pulse-init.py <feature-name> [feature-id]")
            
        feature_name = args[0]
        custom_id = args[1] if len(args) > 1 else None
        
        self.log(f"Initializing feature: {feature_name}")
        
        # Sanitize and generate identifiers
        sanitized_name = self.sanitize_feature_name(feature_name)
        feature_id = self.get_feature_id(custom_id)
        branch_name = f"{feature_id}-{sanitized_name}"
        
        # Create structure
        self.create_directories(branch_name)
        self.copy_templates(branch_name)
        self.update_context(feature_name, feature_id, branch_name)
        self.create_git_branch(branch_name)
        
        # Output results
        print(f"BRANCH_NAME={branch_name}")
        print(f"SPEC_DIR=specs/{branch_name}")
        print(f"FEATURE_ID={feature_id}")
        print("STATUS=initialized")
        
        self.log(f"Successfully initialized feature '{feature_name}' with ID {feature_id}")

if __name__ == "__main__":
    init = SpecPulseInit()
    init.main(sys.argv[1:])