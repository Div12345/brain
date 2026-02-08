---
status: idea
created: 2026-02-05
priority: medium
tags: [scheduler, budget, hooks, capacity]
---

# Capacity Enforcement & Awareness System

## Problem
The cc-scheduler's internal budget tracker only sees scheduler-executed tasks (10% this week), while real API usage is 67%. Interactive Claude Code sessions are invisible to the budget system. The internal budget is a fiction — the real API capacity check is the only safety net.

## Ideas to Explore

### A. Hook warnings (lightweight)
- PreToolUse hook checks `capacity.check_capacity()` periodically
- Warns at 70%, 85%, 95% thresholds
- Injects capacity awareness into active sessions

### B. Budget sync with real API
- Budget tracker calls usage API on session start
- Reconciles internal ledger with actual usage
- Makes budget display reflect reality

### C. Capacity-aware steering (ambitious)
- Active suggestions: switch to haiku, trim scope, wrap up
- Graceful degradation: 80% = "finish up", 90% = "critical only"
- Could integrate with scheduler to reserve capacity for overnight tasks

## Context
- Real capacity check: `lib/capacity.py` calls `https://api.anthropic.com/api/oauth/usage`
- Internal budget: `.omc/state/weekly-budget.json` — only tracks ccq executions
- Token estimation uses `len(output) // 4` and `percent * 5000` — both rough
- A+B are complementary and probably the right starting point
