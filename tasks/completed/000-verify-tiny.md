---
name: verify-tiny
priority: 1
estimated_tokens: 1000
mode: read-only
timeout: 5m
tags: [testing, maintenance]
depends_on: []
---

# Verify Budget Constraints

Lightweight task to confirm scheduler runs.

1. Check the current time
2. Output: Budget check passed - Running small task at {timestamp}
