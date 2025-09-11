#!/usr/bin/env python3
"""
SpecPulse Task Generation Script
Cross-platform Python equivalent of pulse-task.sh
"""

import os
import sys
import re
from pathlib import Path
import datetime

class SpecPulseTask:
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
            
    def analyze_tasks(self, task_file):
        """Analyze task structure and count statuses"""
        if not task_file.exists():
            return {
                'total': 0,
                'completed': 0,
                'pending': 0,
                'blocked': 0,
                'parallel': 0
            }
            
        content = task_file.read_text(encoding='utf-8')
        
        # Count different task states
        total_tasks = len(re.findall(r'^- \[.\]', content, re.MULTILINE))
        completed_tasks = len(re.findall(r'^- \[x\]', content, re.MULTILINE))
        pending_tasks = len(re.findall(r'^- \[ \]', content, re.MULTILINE))
        blocked_tasks = len(re.findall(r'^- \[!\]', content, re.MULTILINE))
        parallel_tasks = len(re.findall(r'\[P\]', content))
        
        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'blocked': blocked_tasks,
            'parallel': parallel_tasks
        }
        
    def validate_task_structure(self, task_file):
        """Validate task structure"""
        required_sections = [
            "## Task List:",
            "## Task Organization",
            "## Critical Path",
            "## Execution Schedule"
        ]
        
        missing_sections = []
        content = task_file.read_text(encoding='utf-8')
        
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
                
        if missing_sections:
            self.log(f"WARNING: Missing required sections: {', '.join(missing_sections)}")
            
        return len(missing_sections)
        
    def check_constitutional_gates(self, task_file):
        """Check constitutional gates compliance"""
        if not task_file.exists():
            return 0
            
        content = task_file.read_text(encoding='utf-8')
        
        # Find constitutional gates section
        constitutional_section = re.search(
            r'Constitutional Gates Compliance.*?(?=\n##|\Z)', 
            content, 
            re.DOTALL
        )
        
        if constitutional_section:
            gates_text = constitutional_section.group(0)
            pending_gates = len(re.findall(r'\[ \]', gates_text))
            return pending_gates
            
        return 0
        
    def check_plan_gates_status(self, plan_file):
        """Check if plan has constitutional gates completed"""
        if not plan_file.exists():
            return "UNKNOWN"
            
        content = plan_file.read_text(encoding='utf-8')
        gate_status_match = re.search(r'Gate Status:\s*\[([^\]]+)\]', content)
        
        if gate_status_match:
            return gate_status_match.group(1)
        else:
            return "UNKNOWN"
            
    def main(self, args):
        """Main execution function"""
        if len(args) < 1:
            self.error_exit("Usage: python pulse-task.py <feature-dir>")
            
        feature_dir = args[0]
        
        self.log("Processing task breakdown...")
        
        # Get and sanitize feature directory
        sanitized_dir = self.get_current_feature_dir(feature_dir)
        
        # Set file paths
        task_file = self.project_root / "tasks" / sanitized_dir / "tasks.md"
        template_file = self.templates_dir / "task.md"
        plan_file = self.project_root / "plans" / sanitized_dir / "plan.md"
        spec_file = self.project_root / "specs" / sanitized_dir / "spec.md"
        
        # Ensure tasks directory exists
        task_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if specification and plan exist first
        if not spec_file.exists():
            self.error_exit(f"Specification file not found: {spec_file}. Please create specification first.")
            
        if not plan_file.exists():
            self.error_exit(f"Implementation plan not found: {plan_file}. Please create plan first.")
            
        # Ensure task template exists
        if not template_file.exists():
            self.error_exit(f"Template not found: {template_file}")
            
        # Create task file if it doesn't exist
        if not task_file.exists():
            self.log(f"Creating task breakdown from template: {task_file}")
            try:
                task_file.write_text(template_file.read_text(encoding='utf-8'))
            except Exception as e:
                self.error_exit(f"Failed to copy task template: {e}")
        else:
            self.log(f"Task breakdown already exists: {task_file}")
            
        # Validate task structure
        self.log("Validating task breakdown...")
        missing_sections = self.validate_task_structure(task_file)
        
        # Analyze tasks
        task_stats = self.analyze_tasks(task_file)
        
        # Check constitutional gates compliance
        pending_gates = self.check_constitutional_gates(task_file)
        
        # Check if plan has constitutional gates completed
        plan_gate_status = self.check_plan_gates_status(plan_file)
        
        if plan_gate_status != "COMPLETED":
            self.log(f"WARNING: Implementation plan constitutional gates not completed. Status: {plan_gate_status}")
            
        # Calculate completion percentage
        if task_stats['total'] > 0:
            completion_percentage = int((task_stats['completed'] / task_stats['total']) * 100)
        else:
            completion_percentage = 0
            
        self.log(f"Task analysis completed - Total: {task_stats['total']}, Completed: {task_stats['completed']} ({completion_percentage}%), Parallel: {task_stats['parallel']}")
        
        # Output comprehensive status
        print(f"TASK_FILE={task_file}")
        print(f"SPEC_FILE={spec_file}")
        print(f"PLAN_FILE={plan_file}")
        print(f"TOTAL_TASKS={task_stats['total']}")
        print(f"COMPLETED_TASKS={task_stats['completed']}")
        print(f"PENDING_TASKS={task_stats['pending']}")
        print(f"BLOCKED_TASKS={task_stats['blocked']}")
        print(f"PARALLEL_TASKS={task_stats['parallel']}")
        print(f"CONSTITUTIONAL_GATES_PENDING={pending_gates}")
        print(f"COMPLETION_PERCENTAGE={completion_percentage}")
        print(f"MISSING_SECTIONS={missing_sections}")
        print("STATUS=generated")

if __name__ == "__main__":
    task = SpecPulseTask()
    task.main(sys.argv[1:])