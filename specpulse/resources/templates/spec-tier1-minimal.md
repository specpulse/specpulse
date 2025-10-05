<!-- TIER: minimal -->
# Feature: {{ feature_name }}

<!-- LLM GUIDANCE:
Keep this tier minimal - just the essence of what's being built.
Focus on WHAT (1 sentence), WHY (1 sentence), and DONE WHEN (3 items).
User can expand later with /sp-expand command.
-->

## What
{{ what_description }}

<!-- LLM GUIDANCE: One sentence describing what is being built -->

## Why
{{ why_description }}

<!-- LLM GUIDANCE: One sentence explaining the business value or user benefit -->

## Done When
<!-- LLM GUIDANCE: 3 concrete, testable acceptance criteria -->

- [ ] {{ acceptance_1 }}
- [ ] {{ acceptance_2 }}
- [ ] {{ acceptance_3 }}

---
<!-- EXPAND_NEXT: tier2 -->
💡 Ready for more detail? Run: `specpulse expand {{ feature_id }} --to-tier standard`
