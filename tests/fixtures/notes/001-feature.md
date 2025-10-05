# Notes for Feature 001

### Note 20241006120000
Timestamp: 2024-10-06 12:00:00
Status: Active

Need to add rate limiting to the authentication API. Should be 5 attempts per 15 minutes to prevent brute force attacks.

---

### Note 20241006130000
Timestamp: 2024-10-06 13:00:00
Status: Active

Consider using bcrypt with cost factor of 12 for password hashing. Argon2 might be overkill for this use case.

---

### Note 20241006140000
Timestamp: 2024-10-06 14:00:00
Status: Merged

JWT tokens should have 15-minute expiration for access tokens and 7-day expiration for refresh tokens.

---
