---
status: idea
created: 2026-02-05
priority: high
tags: [claude-desktop, enterprise, automation, scheduling, gemini]
---

# Leverage Claude Desktop Enterprise as Compute Resource

## Opportunity
Enterprise Claude Desktop account has session-only limits (no weekly cap). Currently underutilized. Could absorb workloads that eat into the Claude Code API weekly quota.

## Known Issues to Solve

### Stability
- Long thinking causes conversation amnesia (Desktop loses context)
- Need workarounds: shorter thinking bursts, checkpointing, or external state management

### DevTools / Node Access
- Remote debugger no longer working on Claude Desktop
- Need to enable Node processes from toolbar → Developer suboption in dropdown
- Could potentially automate this via vision/desktop control (programmatic click)
- This is prerequisite for MCP plugin development and debugging

### Async Notifications
- Current MCP plugin can't notify when Desktop needs input
- Gap: Desktop sits idle waiting for user response, user doesn't know
- Possible solutions:
  - Windows desktop notifications (toast) from an MCP server or background process
  - Polling-based check from external CLI
  - Internal method within Claude Desktop that allows push notifications

### Steering / Orchestration
- Want an external CLI to routinely steer Claude Desktop as an outer loop
- Candidates:
  - **Gemini CLI** from WSL (Google's CLI tool)
  - **Antigravity** on Windows
  - **OpenCode** (supports both Antigravity and Gemini options)
- The steer loop would: assign tasks, monitor progress, handle input requests, rotate sessions when context degrades
- Could integrate with cc-scheduler: scheduler decides WHAT runs, steering layer decides WHERE (Desktop vs Code API)

## Architecture Vision

```
cc-scheduler (brain)
  ├── Claude Code API (weekly-limited, for overnight autonomous + interactive)
  └── Claude Desktop Enterprise (session-limited only, for bulk/research tasks)
        ├── Steered by: Gemini CLI / Antigravity / OpenCode
        ├── MCP plugin: structured communication channel
        └── Notifications: Windows toasts when input needed
```

## Dependencies
- MCP plugin properly structured (see separate idea file)
- DevTools access restored or automated
- Steering CLI chosen and configured
- Session rotation strategy for context degradation

## Open Questions
- Which steering CLI has the best Desktop control? Need to evaluate Gemini CLI vs Antigravity vs OpenCode
- Can we programmatically enable the Developer toolbar option, or is it a one-time manual step?
- What's the actual session limit on the enterprise account? Need to calibrate task sizing
- How to handle the "thinking too long" amnesia — is this a Desktop bug or a prompt issue?
