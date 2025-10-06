# Specification: {{feature_name}}

---
tier: minimal
progress: 0.0
sections_completed: []
sections_partial: []
last_updated: {{date}}
---

## What

<!-- LLM GUIDANCE:
Write ONE sentence describing what this feature does.

Format: "[Feature name] allows users to [action] so that [benefit]"

Examples (GOOD):
- "User authentication allows users to securely log in and access protected resources"
- "Payment processing enables customers to purchase products using credit cards"
- "Real-time notifications inform users of important events as they happen"

Examples (BAD):
- "This feature implements OAuth2 with JWT tokens and session management" (too technical)
- "A system for handling user login" (too vague)
- "Multiple features for authentication" (not one feature)

Keep it simple: What does it do? Why does it exist?
Length: 1 sentence, 10-20 words ideal
-->

[One sentence: What does this feature do?]

---

## Why

<!-- LLM GUIDANCE:
Write ONE sentence explaining the business value or user benefit.

Format: Focus on WHY this matters, not HOW it works.

Examples (GOOD):
- "Without secure authentication, unauthorized users could access sensitive customer data"
- "Manual payment processing delays orders and frustrates customers"
- "Users miss important updates when they're not actively checking the app"

Examples (BAD):
- "To implement industry-standard security protocols" (too technical)
- "Because the product manager requested it" (not user-focused)
- "It's a common feature in similar products" (not specific)

Think: What problem does this solve? What happens if we DON'T build it?
Length: 1 sentence, 10-25 words ideal
-->

[One sentence: Why is this feature needed?]

---

## Done When

<!-- LLM GUIDANCE:
List 3 TESTABLE acceptance criteria that define "done."

Format: Each criterion should be:
- Specific (not vague)
- Testable (can verify it works)
- User-focused (what users can do)
- Independent (can test separately)

Examples (GOOD):
- [ ] Users can log in with email and password
- [ ] Invalid credentials show an error message
- [ ] Successful login redirects to dashboard
- [ ] Users can pay with Visa, Mastercard, or Amex
- [ ] Payment confirmation email sent within 30 seconds
- [ ] Failed payments show clear error messages

Examples (BAD):
- [ ] Authentication works (too vague)
- [ ] Code is written and tested (not user-focused)
- [ ] System handles edge cases (not specific)
- [ ] Performance is good (not measurable)

Think: How will we KNOW this feature is done and working?
Count: Exactly 3 checkboxes
Format: Each starts with "Users can..." or "System does..."
-->

- [ ] [First acceptance criterion - what users can do]
- [ ] [Second acceptance criterion - what users can do]
- [ ] [Third acceptance criterion - what users can do]

---

## Next Steps

<!--
This is a MINIMAL tier specification (Tier 1 of 3).
It's designed for quick starts - you can fill this out in 2-3 minutes.

When you're ready for implementation:
1. Expand to STANDARD tier (adds User Stories, Requirements, Technical Approach, API Design)
   Command: specpulse expand {{feature_id}} --to-tier standard

2. Or jump to COMPLETE tier (adds Security, Performance, Monitoring, Compliance)
   Command: specpulse expand {{feature_id}} --to-tier complete

Want to add just one section?
   Command: specpulse spec add-section {{feature_id}} <section-name>

Check your progress:
   Command: specpulse spec progress {{feature_id}}
-->

**Current Tier**: Minimal (3 sections)
**Time to Complete**: 2-3 minutes
**Ready for Planning**: Once all 3 sections are filled

💡 **Tip**: Start minimal, expand when ready. It's faster to iterate!
