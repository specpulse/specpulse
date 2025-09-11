# /plan

Generate implementation plan from specification.

## Usage
```
/plan generate
```

## Description
Creates a detailed implementation plan based on the current feature specification.

## Process
1. Reads the current specification
2. Analyzes requirements
3. Designs architecture
4. Selects technology stack
5. Creates phased implementation approach
6. Generates API contracts
7. Defines data models
8. Plans testing strategy

## Plan Sections
- Architecture Overview (with diagram)
- Technology Stack
- Implementation Phases
- File Structure
- API Contracts
- Data Models
- Testing Strategy
- Risk Assessment
- Success Criteria

## Phases
1. **Phase 0**: Setup and Prerequisites
2. **Phase 1**: Data Layer
3. **Phase 2**: Business Logic
4. **Phase 3**: API/Interface Layer
5. **Phase 4**: Testing and Optimization

## Example
```
/plan generate
```

Reads: `specs/001-user-auth/specification.md`
Creates: `plans/001-user-auth/implementation.md`