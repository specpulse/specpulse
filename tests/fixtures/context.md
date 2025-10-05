# Memory: Context

## Active [tag:current]
Feature: 003-payment-integration
Status: Planning phase
Blockers: None
Last Updated: 2024-10-06

## Decisions [tag:decision]

### DEC-001: Use Stripe over PayPal
Rationale: Better API, easier integration, superior documentation
Date: 2024-10-05
Related: 003

### DEC-002: PostgreSQL for primary database
Rationale: ACID compliance, JSON support, robust ecosystem
Date: 2024-10-04
Related: 001, 002

### DEC-003: React over Vue for frontend
Rationale: Larger community, better TypeScript support, team familiarity
Date: 2024-10-03
Related: 001

## Patterns [tag:pattern]

### PATTERN-001: API Error Handling
Always return: { success: bool, data: any, error: string }
Used in: 001, 002
Date: 2024-10-04

### PATTERN-002: Loading States
All async operations must show loading indicator with minimum 300ms display time
Used in: 001
Date: 2024-10-02

## Constraints [tag:constraint]

### CONST-001: Rate Limiting
All APIs must implement 100 req/min per user
Applies to: All API features
Date: 2024-10-03

### CONST-002: Browser Support
Support last 2 versions of Chrome, Firefox, Safari, Edge
Applies to: All frontend features
Date: 2024-10-01
