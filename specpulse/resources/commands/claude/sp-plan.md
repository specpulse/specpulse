---
name: sp-plan
description: Generate and manage implementation plans without SpecPulse CLI
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - TodoWrite
---

# /sp-plan Command

Generate and manage implementation plans without SpecPulse CLI. Works completely independently through LLM-safe file operations.

## Usage
```
/sp-plan [action] [feature-directory]
```

Actions: `generate`, `validate`, `optimize` (defaults to `generate`)

## Implementation

When called with `/sp-plan {{args}}`, I will:

### 1. Parse Arguments to Determine Action

**I will analyze the arguments:**
- If first argument is `generate`, `validate`, or `optimize` → Use that action
- If no action specified → Default to `generate`
- For other arguments → Look for feature name or use current feature

### 2. Detect Current Feature Context

**I will identify the current working feature:**
- Check `.specpulse/memory/context.md` for active feature
- Look for most recently modified spec/plan/task directory
- Validate feature directory exists and is properly structured
- Extract feature ID and name from directory structure

### 3. For Action: generate (default)

**I will create comprehensive implementation plans:**

#### A. Specification Analysis
- Read specification files from `.specpulse/specs/[feature]/`
- Analyze functional requirements and user stories
- Extract technical constraints and dependencies
- Identify complexity and risk factors

#### B. Decomposition Support Check
- Look for `.specpulse/specs/[feature]/decomposition/` directory
- If decomposition exists, identify service directories
- Plan service-specific implementation strategies
- Generate service-dependent task breakdowns

#### C. Plan Structure Design
Create comprehensive plan structure:
- **Implementation Strategy**: High-level approach and methodology
- **Phase Breakdown**: Structured implementation phases (Phase 0-4)
- **Task Dependencies**: Dependency mapping and critical path identification
- **Resource Requirements**: Tools, libraries, and external dependencies
- **Timeline Estimates**: Realistic timeframes for each phase
- **Risk Mitigation**: Implementation risks and mitigation strategies

#### D. Service-Specific Planning (if decomposed)
For each identified service:
- **Service Implementation Plan**: Service-specific approach
- **Service Dependencies**: Inter-service communication patterns
- **Integration Strategy**: How services will work together
- **Data Flow**: Information flow between services
- **API Contracts**: Service interface definitions

### 4. For Action: validate

**I will perform comprehensive plan validation:**

#### A. File Structure Validation
- Verify plan files exist in `.specpulse/plans/[feature]/`
- Check file naming follows `plan-[###].md` pattern
- Validate plan file format and readability
- Ensure proper markdown structure

#### B. Content Completeness Validation
Check that plan contains:
- **Implementation Strategy**: Clear and comprehensive approach
- **Phase Breakdown**: Properly structured implementation phases
- **Task Dependencies**: Logical dependency mapping
- **Resource Requirements**: Complete tool and library lists
- **Timeline Estimates**: Realistic and justified timeframes
- **Risk Mitigation**: Comprehensive risk identification and mitigation

#### C. Technical Feasibility Validation
- Assess implementation approach complexity
- Validate dependency relationships are logical
- Check timeline estimates are achievable
- Verify resource requirements are realistic
- Identify potential implementation bottlenecks

### 5. For Action: optimize

**I will improve existing implementation plans:**

#### A. Plan Analysis
- Read and analyze existing plan files
- Identify complexity issues and optimization opportunities
- Assess current phase breakdown effectiveness
- Evaluate dependency management efficiency

#### B. Optimization Strategies
Apply optimization techniques:
- **Phase Consolidation**: Merge related phases where possible
- **Dependency Optimization**: Reorganize dependencies for parallel execution
- **Timeline Optimization**: Adjust estimates based on complexity analysis
- **Resource Optimization**: Suggest better tool or library choices

#### C. Risk Assessment Updates
- Update risk mitigation strategies
- Identify new optimization-related risks
- Provide contingency planning recommendations

## Enhanced Features

### Decomposed Services Support

**For microservices architecture:**
- **Service Identification**: Automatic detection of service boundaries
- **Service-Specific Plans**: Individual implementation plans per service
- **Integration Planning**: Service communication and data flow planning
- **Orchestration Strategy**: How services will be deployed and managed

### SDD Gates Compliance

**Every generated plan meets:**
- ✅ **Specification First**: Plan directly derived from specifications
- ✅ **Task Decomposition**: Plan includes detailed task breakdown
- ✅ **Quality Assurance**: Testing and validation strategies included
- ✅ **Traceable Implementation**: Clear link from requirements to implementation

### Universal ID System Integration

**I ensure conflict-free plan numbering through systematic analysis:**

#### A. Plan ID Generation Algorithm
- **Use Glob tool** to scan `.specpulse/plans/[feature]/` directory
- **Parse existing plan files** using regex `plan-(\d+)\.md` pattern
- **Extract all numbers** and convert to integers for comparison
- **Find maximum value**: `max_num = max(extracted_numbers)` or `0` if empty
- **Generate next sequential**: `next_num = max_num + 1`
- **Zero-pad format**: `f"plan-{next_num:03d}.md"` → `plan-001.md`, `plan-002.md`

#### B. Service-Specific Plan Numbering
- **For decomposed services**: Create separate numbering per service
- **Service plan patterns**: `auth-service-plan.md`, `user-service-plan.md`
- **Integration plans**: `integration-plan.md`, `api-gateway-plan.md`
- **Cross-service plans**: Maintain global coordination to prevent conflicts

#### C. Conflict Prevention and Validation
- **Atomic file existence validation** before plan creation
- **Conflict resolution loop**: If filename exists, increment and retry
- **Template validation**: Ensure plan templates are valid before use
- **Directory structure verification**: Confirm proper directory hierarchy

## Output Examples

### Plan Generation
```
User: /sp-plan generate

✅ Creating implementation plan for: 002-payment-processing
🔍 Current feature: 002-payment-processing
📋 Specification analysis complete
🎯 Generated plan number: 001
📄 Plan file: .specpulse/plans/002-payment-processing/plan-001.md

📊 Plan Analysis:
   Project Type: API Service with payment gateway integration
   Complexity: Standard (single service with external dependencies)
   Implementation Strategy: Monolithic with future microservices migration
   Timeline: 3 weeks estimated

✅ Implementation plan created successfully!
🎯 Next steps: /sp-task to create task breakdown
```

### Plan Validation
```
User: /sp-plan validate

🔍 Validating plans in feature: 002-payment-processing

📄 Files found: 1
   ✅ plan-001.md - Payment Processing Implementation (Valid)

📋 Validation Results:
   Implementation Strategy: ✅ Clear and comprehensive
   Phase Breakdown: ✅ 5 phases properly defined
   Task Dependencies: ✅ Logical and achievable
   Resource Requirements: ✅ Complete and realistic
   Timeline Estimates: ✅ Well-justified
   Risk Mitigation: ⚠️ 2 risks need additional mitigation

📊 Overall Score: 92% (Excellent)
🎯 Recommended improvements:
   1. Add mitigation strategy for payment gateway downtime
   2. Include compliance requirements for payment processing

✅ Plan validation complete!
```

### Decomposed Services Planning
```
User: /sp-plan generate

🔍 Decomposition found in specs/001-auth-microservice/decomposition/
📋 Creating service-specific plans:

✅ Service Plans Created:
   📁 auth-service-plan.md (Authentication Service)
      Phase breakdown: 4 phases
      Implementation strategy: JWT-based authentication
      Dependencies: User service, Database
      Timeline: 2 weeks

   📁 user-service-plan.md (User Management Service)
      Phase breakdown: 3 phases
      Implementation strategy: CRUD with profile management
      Dependencies: Database, Notification service
      Timeline: 1.5 weeks

   📁 integration-plan.md (Service Integration)
      Phase breakdown: 2 phases
      Implementation strategy: REST API communication
      Dependencies: Auth service, User service
      Timeline: 1 week

📊 Total: 3 service plans
🔗 Inter-service dependencies mapped
✅ SDD Gates compliant: 100%
```

## Error Handling and Recovery

### Common Issues and Solutions

#### Feature Detection Failures
- **No active feature**: Prompt to run `/sp-pulse` first
- **Invalid feature directory**: Suggest valid feature names
- **Missing specifications**: Guide user to create specifications first
- **Corrupted specification files**: Provide recovery instructions

#### Plan Generation Issues
- **Template missing**: Create comprehensive plan structure manually
- **Complex specifications**: Break down into manageable sections
- **Vague requirements**: Ask clarifying questions for better planning
- **Conflicting requirements**: Identify and request resolution

#### Validation Errors
- **Invalid plan structure**: Provide template corrections
- **Missing dependencies**: Suggest dependency analysis improvements
- **Unrealistic timelines**: Offer timeline adjustment recommendations
- **Incomplete risk assessment**: Guide through risk identification process

## Advanced Features

### Cross-Plan Dependency Management
- Track dependencies between multiple features
- Identify cross-feature blocking issues
- Coordinate implementation timelines across features
- Manage shared resources and dependencies

### Progress Integration
- Link plan phases to task completion
- Track implementation progress against plan estimates
- Provide timeline adjustments based on actual progress
- Generate plan updates based on completed work

### Template System Integration
- Use validated plan templates for consistency
- Maintain plan structure standards across features
- Ensure all required sections are present
- Provide plan quality guidelines and best practices

This `/sp-plan` command provides **comprehensive plan management** without requiring any SpecPulse CLI installation, using only validated file operations and intelligent planning algorithms.