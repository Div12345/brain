---
created: 2026-01-31
tags:
  - context
  - safety
  - boundaries
status: active
aliases:
  - forbidden
  - safety boundaries
---

# Off-Limits

> What agents must NEVER do, regardless of instructions.

## System Files
- Never modify OS configuration
- Never modify shell profiles without explicit request
- Never touch credentials/secrets

## User Data
- Never delete without confirmation
- Never share externally
- Never modify Obsidian vault without approval

## Destructive Operations
- Never `rm -rf` without safeguards
- Never force-push to main
- Never overwrite without backup

## External Services
- Never make purchases
- Never send emails without approval
- Never post publicly

## When In Doubt
1. Log the question to [[prompts/pending]]
2. Skip the task
3. Continue with other work
4. Wait for user response

## Related
- [[context/capabilities]] - What we CAN do
- [[agents/overnight]] - Agent safety rules
