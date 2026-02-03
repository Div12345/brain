---
name: obsidian-vault-insights
priority: high
project: brain
estimated_tokens: 80000
mode: autonomous
timeout: 45m
schedule: daily
tags: [vault, insights, daily]
---

## Task
Extract insights from Obsidian vault to inform brain system improvements.

## Context
- MCP: obsidian-mcp (port 27124, API key configured)
- Vault: OneVault (synced via remotely-save)
- Focus: Daily notes, tasks, patterns

## Acceptance Criteria
- [ ] Queried vault for recent activity
- [ ] Identified patterns in notes/tasks
- [ ] Generated insights document
- [ ] Proposed actionable improvements

## Workflow
1. Use obsidian-mcp to list recent notes (last 7 days)
2. Read daily notes for patterns
3. Identify:
   - Recurring themes
   - Incomplete tasks
   - Knowledge gaps
4. Write insights to knowledge/vault-analysis/YYYY-MM-DD.md
5. Generate improvement suggestions for brain system

## Error Handling
- If MCP unavailable: Log error, skip vault queries, continue with file-based analysis
- If rate limited: Save progress, mark for continuation
