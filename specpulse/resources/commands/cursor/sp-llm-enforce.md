---
name: /sp-llm-enforce
id: sp-llm-enforce
category: SpecPulse
description: Enforce strict LLM compliance rules for SpecPulse operations
---

# /sp-llm-enforce Command

Enforce strict LLM compliance rules for SpecPulse operations without CLI dependencies. Works completely independently through validated operations.

<!-- SPECPULSE:START -->
**Guardrails**
- CLI-first approach: Always try SpecPulse CLI commands before file operations
- Keep changes tightly scoped to the compliance enforcement outcome
- Only validate files in specs/, plans/, tasks/, memory/ directories - NEVER modify templates/ or internal config

**Critical Rules**
- **PRIMARY**: Use file operations (CLI-independent mode)
- **PROTECTED DIRECTORIES**: templates/, .specpulse/, specpulse/, .claude/, .gemini/, .windsurf/, .cursor/
- **EDITABLE ONLY**: specs/, plans/, tasks/, memory/

**Steps**
Track these steps as TODOs and complete them one by one.

1. **Parse arguments to determine enforcement action**:
   - If action provided: Use specific enforcement action
   - If "status": Show current compliance status and violations
   - If "validate": Validate operations against compliance rules
   - If "end": End enforcement session
   - If no argument: Default to "start"

2. **CLI-First Compliance Enforcement**:
   - **Step 1**: Try SpecPulse CLI commands before file operations
   - **Step 2**: Validate file operations against protected directories
   - **Step 3**: Enforce atomic file operations with proper validation
   - **Step 4**: Prevent directory traversal attacks

3. **Protected Directory Validation**:
   - **NEVER modify**: templates/, .specpulse/, specpulse/, AI config directories
   - **EDITABLE ONLY**: specs/, plans/, tasks/, memory/
   - **Check**: All file paths are within allowed directories
   - **Verify**: No directory traversal attempts (../, absolute paths)

4. **Operation Compliance Check**:
   - **File Operation Validation**: Verify file permissions before operations
   - **Content Validation**: Validate markdown syntax and structure
   - **Malicious Content Check**: Check for harmful patterns
   - **Naming Convention**: Verify SpecPulse naming conventions

5. **Real-time Monitoring**:
   - **Monitor**: All file operations for compliance
   - **Track**: Violations and provide corrections
   - **Log**: Enforcement actions for audit trail
   - **Report**: Compliance status and recommendations

6. **Error Prevention and Recovery**:
   - **Safe Operations**: Validate inputs before processing
   - **Atomic Operations**: Use with rollback capability
   - **Error Handling**: Provide clear error messages and corrections
   - **Data Integrity**: Maintain throughout operations

7. **Session Management**:
   - **Start/Stop**: Compliance enforcement sessions
   - **State Management**: Session persistence and configuration
   - **History**: Session tracking and reporting
   - **Configuration**: Rule severity and monitoring options

8. **Status Reporting**:
   - **Compliance Check**: Validate operations against rules
   - **Violation Report**: Categorize and report violations
   - **Metrics**: Compliance score and improvement recommendations
   - **Risk Assessment**: Identify and mitigate compliance risks

**Usage**
Arguments should be provided as: `[action] [context]`

**CLI-Independent Benefits:**
- Works completely without SpecPulse CLI installation
- Real-time violation prevention and monitoring
- Comprehensive compliance reporting and metrics
- Atomic operations with guaranteed integrity

**Advanced Features:**
- Real-time violation detection and automated corrections
- Comprehensive monitoring with audit trail generation
- Customizable rule enforcement and severity levels
- Session-based compliance management

**Error Handling:**
- Input validation and sanitization for all operations
- File operation error recovery with rollback mechanisms
- Permission issue resolution with detailed guidance
- Directory structure validation and compliance checking

**Safety Features:**
- Path validation and sanitization to prevent traversal
- Directory traversal protection with secure file access
- Atomic operation rollback for failed operations
- Comprehensive error handling and recovery procedures

**Reference**
- Monitor file operations for compliance violations
- Validate directory structure against protected directory rules
- Maintain audit trail of all enforcement actions and corrections
<!-- SPECPULSE:END -->