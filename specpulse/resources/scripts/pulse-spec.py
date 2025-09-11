#!/usr/bin/env python3
"""
SpecPulse Specification Generation Script
Cross-platform Python equivalent of pulse-spec.sh
"""

import os
import sys
import re
from pathlib import Path
import datetime

class SpecPulseSpec:
    def __init__(self):
        self.script_name = Path(__file__).name
        self.project_root = Path(__file__).parent.parent.parent
        self.memory_dir = self.project_root / "memory"
        self.context_file = self.memory_dir / "context.md"
        self.templates_dir = self.project_root / "resources" / "templates"
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.script_name}: {message}", file=sys.stderr)
        
    def error_exit(self, message):
        """Exit with error message"""
        self.log(f"ERROR: {message}")
        sys.exit(1)
        
    def sanitize_feature_dir(self, feature_dir):
        """Sanitize feature directory name"""
        if not feature_dir:
            self.error_exit("Feature directory cannot be empty")
            
        # Remove non-alphanumeric characters except hyphens and underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', feature_dir)
        
        if not sanitized:
            self.error_exit(f"Invalid feature directory: '{feature_dir}'")
            
        return sanitized
        
    def find_feature_directory(self):
        """Find feature directory from context file"""
        if not self.context_file.exists():
            self.error_exit("No context file found and no feature directory provided")
            
        try:
            content = self.context_file.read_text(encoding='utf-8')
            # Look for "Active Feature" section
            match = re.search(r'Active Feature:\s*(.+)', content)
            if match:
                feature_dir = match.group(1).strip()
                self.log(f"Using active feature from context: {feature_dir}")
                return feature_dir
            else:
                self.error_exit("No active feature found in context file")
        except Exception as e:
            self.error_exit(f"Failed to read context file: {e}")
            
    def get_current_feature_dir(self, provided_dir):
        """Get current feature directory"""
        if provided_dir:
            return self.sanitize_feature_dir(provided_dir)
        else:
            return self.find_feature_directory()
            
    def validate_specification(self, spec_file):
        """Validate specification structure"""
        if not spec_file.exists():
            self.error_exit(f"Specification file does not exist: {spec_file}")
            
        # Required sections
        required_sections = [
            "## Specification:",
            "## Metadata", 
            "## Functional Requirements",
            "## Acceptance Scenarios"
        ]
        
        missing_sections = []
        content = spec_file.read_text(encoding='utf-8')
        
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
                
        if missing_sections:
            self.log(f"WARNING: Missing required sections: {', '.join(missing_sections)}")
            
        # Check for clarifications needed
        clarification_matches = re.findall(r'NEEDS CLARIFICATION', content)
        if clarification_matches:
            clarification_count = len(clarification_matches)
            self.log(f"WARNING: Specification has {clarification_count} clarifications needed")
            return clarification_count
            
        return 0
        
    def main(self, args):
        """Main execution function"""
        if len(args) < 1:
            self.error_exit("Usage: python pulse-spec.py <feature-dir> [spec-content]")
            
        feature_dir = args[0]
        spec_content = args[1] if len(args) > 1 else None
        
        self.log("Processing specification...")
        
        # Get and sanitize feature directory
        sanitized_dir = self.get_current_feature_dir(feature_dir)
        
        # Set file paths
        spec_file = self.project_root / "specs" / sanitized_dir / "spec.md"
        template_file = self.templates_dir / "spec.md"
        
        # Ensure specs directory exists
        spec_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle specification content
        if spec_content:
            self.log(f"Updating specification: {spec_file}")
            try:
                spec_file.write_text(spec_content, encoding='utf-8')
            except Exception as e:
                self.error_exit(f"Failed to write specification content: {e}")
        else:
            # Ensure specification exists from template
            if not spec_file.exists():
                if not template_file.exists():
                    self.error_exit(f"Template not found: {template_file}")
                    
                self.log(f"Creating specification from template: {spec_file}")
                try:
                    spec_file.write_text(template_file.read_text(encoding='utf-8'))
                except Exception as e:
                    self.error_exit(f"Failed to copy specification template: {e}")
            else:
                self.log(f"Specification already exists: {spec_file}")
                
        # Validate specification
        self.log("Validating specification...")
        clarification_count = self.validate_specification(spec_file)
        
        # Check for missing sections
        required_sections = [
            "## Specification:",
            "## Metadata", 
            "## Functional Requirements",
            "## Acceptance Scenarios"
        ]
        
        content = spec_file.read_text(encoding='utf-8')
        missing_sections = [s for s in required_sections if s not in content]
        
        self.log("Specification processing completed successfully")
        
        # Output results
        print(f"SPEC_FILE={spec_file}")
        print(f"CLARIFICATIONS_NEEDED={clarification_count}")
        print(f"MISSING_SECTIONS={len(missing_sections)}")
        print("STATUS=updated")

if __name__ == "__main__":
    spec = SpecPulseSpec()
    spec.main(sys.argv[1:])