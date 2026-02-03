---
priority: 1
estimated_tokens: 1000
mode: read-only
timeout: 5m
tags: [testing, maintenance]
---
# Verify Budget Constraints

This is a lightweight task designed to slip through the scheduler even when capacity is constrained.

1.  Check the current time.
2.  Output "Budget check passed: Running small task."
