# /plan

Generate implementation plans using SpecPulse methodology.

## Usage
```
/plan generate
/plan validate
```

## Commands

### generate
Create implementation plan from specification:
1. Run Phase Gates checks:
   - Constitutional compliance
   - Simplicity check (≤3 modules)
   - Test-first strategy defined
   - Framework selection complete
   - Research completed

2. Generate plan sections:
   - Technology stack
   - Architecture overview
   - Implementation phases
   - API contracts
   - Data models
   - Testing strategy

3. Track complexity:
   - If >3 modules, document justification
   - Create simplification roadmap

4. Write to plans/[feature]/plan.md

### validate
Check plan against constitution:
1. Verify Phase Gates passed
2. Check complexity tracking
3. Ensure test-first approach
4. Validate framework choices

## Phase Gates (Phase -1)
Must pass before implementation:
- ✅ Using ≤3 projects/modules
- ✅ Tests defined before code
- ✅ Using framework features directly
- ✅ No premature abstractions
- ✅ Research completed

## Example
```
/plan generate
```