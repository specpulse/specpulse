#!/usr/bin/env python3
"""
SpecPulse Plan Generation Script
Cross-platform Python equivalent of pulse-plan.sh
"""

import os
import sys
import re
from pathlib import Path
import datetime

class SpecPulsePlan:
    def __init__(self):
        self.script_name = Path(__file__).name
        self.project_root = Path(__file__).parent.parent
        self.memory_dir = self.project_root / "memory"
        self.context_file = self.memory_dir / "context.md"
        self.templates_dir = self.project_root / "templates"
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            print(f"[{timestamp}] {self.script_name}: {message}", file=sys.stderr)
        except UnicodeEncodeError:
            # Fallback for Windows console encoding issues
            message = message.encode('cp1252', errors='replace').decode('cp1252')
            print(f"[{timestamp}] {self.script_name}: {message}", file=sys.stderr)
        
    def error_exit(self, message):
        """Exit with error message"""
        self.log(f"ERROR: {message}")
        sys.exit(1)
        
    def sanitize_feature_dir(self, feature_dir):
        """Sanitize feature directory name"""
        if not feature_dir:
            self.error_exit("Feature directory cannot be empty")
            
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
            
    def validate_plan_structure(self, plan_file):
        """Validate plan structure"""
        required_sections = [
            "## Implementation Plan:",
            "## Specification Reference",
            "## Phase -1: Pre-Implementation Gates",
            "## Implementation Phases"
        ]
        
        missing_sections = []
        content = plan_file.read_text(encoding='utf-8')
        
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
                
        if missing_sections:
            self.log(f"WARNING: Missing required sections: {', '.join(missing_sections)}")
            
        return len(missing_sections)
        
    def check_constitutional_gates(self, plan_file):
        """Check constitutional gates"""
        constitutional_gates = [
            "Simplicity Gate",
            "Anti-Abstraction Gate", 
            "Test-First Gate",
            "Integration-First Gate",
            "Research Gate"
        ]
        
        missing_gates = []
        content = plan_file.read_text(encoding='utf-8')
        
        for gate in constitutional_gates:
            if gate not in content:
                missing_gates.append(gate)
                
        if missing_gates:
            self.log(f"WARNING: Missing constitutional gates: {', '.join(missing_gates)}")
            
        # Check gate status
        gate_status_match = re.search(r'Gate Status:\s*\[([^\]]+)\]', content)
        if gate_status_match:
            gate_status = gate_status_match.group(1)
            if gate_status.upper() != "COMPLETED":
                self.log(f"WARNING: Constitutional gates not completed. Status: {gate_status}")
                return gate_status
        else:
            self.log("WARNING: Constitutional gates status not found")
            return "UNKNOWN"
            
        return "COMPLETED"
        
    def main(self, args):
        """Main execution function"""
        if len(args) < 1:
            self.error_exit("Usage: python pulse-plan.py <feature-dir>")
            
        feature_dir = args[0]
        
        self.log("Processing implementation plan...")
        
        # Get and sanitize feature directory
        sanitized_dir = self.get_current_feature_dir(feature_dir)
        
        # Set file paths
        plan_file = self.project_root / "plans" / sanitized_dir / "plan.md"
        template_file = self.templates_dir / "plan.md"
        spec_file = self.project_root / "specs" / sanitized_dir / "spec.md"
        
        # Ensure plans directory exists
        plan_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if specification exists first
        if not spec_file.exists():
            self.error_exit(f"Specification file not found: {spec_file}. Please create specification first.")
            
        # Ensure plan template exists
        if not template_file.exists():
            self.error_exit(f"Template not found: {template_file}")
            
        # Create plan if it doesn't exist
        if not plan_file.exists():
            self.log(f"Creating implementation plan from template: {plan_file}")
            try:
                plan_file.write_text(template_file.read_text(encoding='utf-8'))
            except Exception as e:
                self.error_exit(f"Failed to copy plan template: {e}")
        else:
            self.log(f"Implementation plan already exists: {plan_file}")
            
        # Validate plan structure
        self.log("Validating implementation plan...")
        missing_sections = self.validate_plan_structure(plan_file)
        
        # Check Constitutional Gates
        self.log("Checking Constitutional Gates...")
        gate_status = self.check_constitutional_gates(plan_file)
        
        # Check if specification has clarifications needed
        if spec_file.exists():
            spec_content = spec_file.read_text(encoding='utf-8')
            clarification_matches = re.findall(r'NEEDS CLARIFICATION', spec_content)
            if clarification_matches:
                clarification_count = len(clarification_matches)
                self.log(f"WARNING: Specification has {clarification_count} clarifications needed - resolve before proceeding")
        
        self.log("Implementation plan processing completed successfully")
        
        # Output results
        print(f"PLAN_FILE={plan_file}")
        print(f"SPEC_FILE={spec_file}")
        print(f"MISSING_SECTIONS={missing_sections}")
        print(f"CONSTITUTIONAL_GATES_STATUS={gate_status}")
        print("STATUS=ready")

if __name__ == "__main__":
    plan = SpecPulsePlan()
    plan.main(sys.argv[1:])