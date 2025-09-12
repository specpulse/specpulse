#!/usr/bin/env python3
"""
SpecPulse Decomposition Orchestrator
Validates decomposition request and returns status for AI processing
"""

import sys
import os
from pathlib import Path

def main():
    spec_id = sys.argv[1] if len(sys.argv) > 1 else None
    action = sys.argv[2] if len(sys.argv) > 2 else "validate"
    
    print(f"[SpecPulse Decompose] Processing spec: {spec_id or 'current'}")
    
    # Find specification
    specs_dir = Path("specs")
    if not specs_dir.exists():
        print("ERROR: No specifications directory")
        print("SUGGESTION: Run /sp-spec create first")
        sys.exit(1)
    
    if spec_id:
        spec_dirs = list(specs_dir.glob(f"{spec_id}*"))
        spec_dir = spec_dirs[0] if spec_dirs else None
    else:
        spec_dirs = sorted(specs_dir.glob("*"), reverse=True)
        spec_dir = spec_dirs[0] if spec_dirs else None
    
    if not spec_dir:
        print("ERROR: No specification found")
        print("SUGGESTION: Run /sp-spec create first")
        sys.exit(1)
    
    # Check complexity
    spec_files = list(spec_dir.glob("spec-*.md"))
    if spec_files:
        spec_file = sorted(spec_files)[-1]
        line_count = len(spec_file.read_text(encoding='utf-8').splitlines())
        
        print(f"SPEC_FILE={spec_file}")
        print(f"COMPLEXITY={line_count} lines")
        
        if line_count > 100:
            print("RECOMMENDATION=Decomposition advised (complex spec)")
        else:
            print("RECOMMENDATION=Single service may suffice")
    
    # Check for existing decomposition
    decomp_dir = spec_dir / "decomposition"
    if decomp_dir.exists():
        print("STATUS=Decomposition exists")
        print(f"PATH={decomp_dir}")
    else:
        print("STATUS=Ready for decomposition")
        print(f"PATH={spec_dir}")
    
    # Return template paths for AI
    print("TEMPLATES_DIR=templates/decomposition")
    print("MEMORY_FILE=memory/context.md")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())