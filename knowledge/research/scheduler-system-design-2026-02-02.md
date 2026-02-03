# Scheduler System Design Research - 2026-02-02

> From Claude Desktop conversation: Building a task scheduler for Claude Code usage windows

## Goal

Build a scheduler that:
1. Triggers Claude Code tasks when usage resets (midnight)
2. Self-improving with structured logging
3. Feedback loop for continuous improvement
4. Smart token budgeting
5. Mobile accessible (termux+tailscale potential)

## Core Principles (From User)

- Minimal but functional - don't overcomplicate
- Self-referential loop for improvement
- Quantifiable metrics from day 1
- Mix and match from existing tools, don't reinvent wheels
- Obsidian-style documentation with wikilinks
- Feedback logged for retriggers and planning

## GitHub Repos Researched

### Tier 1 - Direct Scheduling
| Repo | Stars | Key Feature | Adopt? |
|------|-------|-------------|--------|
| **ClaudeNightsWatch** (aniketkarne) | New | Autonomous task execution, usage monitoring | Maybe - too new |
| **claude-code-scheduler** (jshchnz) | ? | Autopilot scheduling | Review |
| **claude-squad** (smtg-ai) | Active | tmux sessions, git worktrees, parallel tasks | Yes - isolation |

### Tier 2 - Orchestration
| Repo | Key Feature | Adopt? |
|------|-------------|--------|
| **claude-flow** | Orchestration with scheduling | Review patterns |
| **oh-my-claudecode** | Already installed - has ralph-loop, continuation | Use existing |

### awesome-claude-code
- To be checked for additional scheduling tools

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SCHEDULER SYSTEM                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │ Usage Monitor│────▶│ Task Queue   │────▶│ Executor    │ │
│  │ (ccusage)    │     │ (SQLite/file)│     │ (tmux+cc)   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                    │                    │         │
│         │                    │                    │         │
│         ▼                    ▼                    ▼         │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │ Reset Timer  │     │ Plan Store   │     │ Feedback    │ │
│  │ (cron/watch) │     │ (brain/tasks)│     │ Logger      │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│                              │                    │         │
│                              └────────────────────┘         │
│                                      │                      │
│                              ┌───────▼──────┐               │
│                              │ Self-Improve │               │
│                              │ Loop         │               │
│                              └──────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Components to Build

### 1. Usage Monitor
- Check `ccusage` for remaining tokens and reset time
- Available in both Windows terminal and WSL
- Trigger when reset detected

### 2. Task Queue
- Simple file-based (brain/tasks/pending/)
- Or SQLite for atomic operations
- Priority ordering

### 3. Executor
- Use tmux for session isolation (from claude-squad)
- Git worktrees for code isolation
- omc's ralph-loop for persistence

### 4. Feedback Logger
- Structured logs in brain/logs/
- Metrics: success rate, token usage, time to complete
- A/B testing of prompt styles

### 5. Self-Improvement Loop
- Analyze logs after each run
- Identify failure patterns
- Adjust plans automatically
- Quantifiable metrics from day 1

## Metrics to Track

| Metric | Definition | Target |
|--------|------------|--------|
| Task completion rate | Completed / Attempted | > 80% |
| Token efficiency | Useful output / Tokens used | Increasing |
| Retry rate | Retriggers needed / Tasks | Decreasing |
| Plan quality score | Tasks needing revision | Decreasing |

## Implementation Priority

1. **Tonight (1 hour):** Basic scheduler that triggers on usage reset
2. **Tomorrow:** Add feedback logging
3. **This week:** Self-improvement loop
4. **Later:** Mobile access, smart budgeting

## Key Decisions

1. **Orchestration layer:** WSL (already has omc, mcps, etc.) not Windows
2. **Session isolation:** tmux (from claude-squad)
3. **Persistence:** Use existing ralph-loop
4. **Logging:** brain/logs/ with obsidian format

## Open Questions

- [ ] Exact ccusage integration method
- [ ] Plan format specification
- [ ] Token budget allocation algorithm
- [ ] Phone access implementation

## References

- ClaudeNightsWatch: https://github.com/aniketkarne/ClaudeNightsWatch
- claude-code-scheduler: https://github.com/jshchnz/claude-code-scheduler
- claude-squad: https://github.com/smtg-ai/claude-squad
- claude-flow: (check awesome-claude-code)
- awesome-claude-code: https://github.com/anthropics/awesome-claude-code
