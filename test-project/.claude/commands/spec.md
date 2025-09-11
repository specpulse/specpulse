# /spec

Create or update feature specifications using SpecPulse.

## Usage
```
/spec create <description>
/spec update
/spec validate
```

## Commands

### create
Generate a specification from user requirements:
1. Parse the user's description
2. Identify functional requirements
3. Create user stories
4. Mark uncertainties with [NEEDS CLARIFICATION]
5. Write to specs/[feature]/spec.md

### update
Update existing specification:
1. Read current spec.md
2. Apply changes based on clarifications
3. Remove resolved [NEEDS CLARIFICATION] markers
4. Update acceptance criteria

### validate
Check specification completeness:
1. Ensure all sections are filled
2. Check for remaining [NEEDS CLARIFICATION] markers
3. Verify acceptance criteria are testable
4. Confirm technical specs are defined

## Template Structure
- Project Overview
- Functional Requirements (Must/Should/Could)
- User Stories with Acceptance Criteria
- Technical Specifications
- Clarifications Needed
- Validation Checklist

## Example
```
/spec create "Build a user authentication system with email/password and OAuth2"
```