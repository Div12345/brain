---
created: 2026-01-31
tags:
  - research
  - multi-agent
  - orchestration
  - tools
updated: 2026-01-31T10:25
agent: claude-code-web
---

# Multi-Agent Coordination Tools

Research on tools for coordinating multiple Claude Code agents across worktrees.

## Recommended Tools

### 1. ccswarm (nwiizo/ccswarm)
**URL:** https://github.com/nwiizo/ccswarm
**Type:** Rust-native multi-agent orchestration

Key features:
- Git worktree isolation per agent
- Channel-based communication (zero-cost Rust abstractions)
- Connects to Claude Code via ACP (Agent Client Protocol)
- Specialized agent coordination

**Best for:** High-performance, type-safe multi-agent systems

### 2. Claude Flow (ruvnet/claude-flow)
**URL:** https://github.com/ruvnet/claude-flow
**Type:** Enterprise agent orchestration platform

Key features:
- 60+ specialized agents in coordinated swarms
- Native Claude Code support via MCP protocol
- Distributed swarm intelligence
- RAG integration
- Multiple execution modes (Autopilot, Ultrapilot, Swarm)

**Best for:** Complex enterprise workflows, parallel execution

### 3. Claude Squad (smtg-ai/claude-squad)
**URL:** https://github.com/smtg-ai/claude-squad
**Type:** Multi-agent terminal manager

Key features:
- Manages Claude Code, Aider, Codex, OpenCode, Amp
- Git worktrees for branch isolation
- Each agent works on its own branch
- Terminal multiplexing

**Best for:** Managing multiple AI coding assistants

### 4. Custom Worktree Manager Pattern
**Source:** https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees

Simple approach:
```bash
# Custom command opens worktree + Claude Code
w core some-feature claude
```

Creates isolated worktree with Claude Code session instantly.

## Messaging Patterns

### Claude Code Swarm Orchestration (v2.1.19+)

Built-in messaging via `Teammate()` tool:
- `spawnTeam` - Create new agent team
- Task delegation to specialists
- Shutdown requests/approvals
- Idle notifications
- Task completion messages

### File-Based Approach (Our Current)

Simple but universal:
- Git as message bus
- Files in `messages/` directory
- Push to send, pull to receive
- Works across any agent type

### Dapr Agents Pattern (dapr/dapr-agents)

Advanced messaging:
- Direct agent-to-agent communication
- Service discovery built-in
- Shared message bus for events
- Distributed tracing

## Comparison

| Tool | Complexity | Worktree Support | Messaging | Claude Integration |
|------|------------|------------------|-----------|-------------------|
| ccswarm | High | ✅ Native | Channel-based | ACP |
| Claude Flow | Medium | Via MCP | Built-in | MCP native |
| Claude Squad | Low | ✅ Native | Terminal-based | Direct |
| File-based | Low | Any | Git-based | Universal |

## Recommendation for Brain System

### Short Term (Now)
1. Use file-based messaging (`messages/` directory)
2. Git push/pull for synchronization
3. Simple, works with any agent

### Medium Term
1. Evaluate **Claude Squad** for worktree management
2. Consider **ccswarm** if performance needed
3. Keep file-based as fallback

### Long Term
1. Evaluate **Claude Flow** for enterprise features
2. Consider MCP-based messaging if available
3. Build custom solution only if gaps remain

## Related

- [[messages/README]] - Our messaging protocol
- [[tools/orchestration/DESIGN]] - Architecture design
- [[inspirations/orchestration-research]] - Previous research

## Sources

- [ccswarm](https://github.com/nwiizo/ccswarm)
- [Claude Flow](https://github.com/ruvnet/claude-flow)
- [Claude Squad](https://github.com/smtg-ai/claude-squad)
- [Parallel AI Coding Guide](https://docs.agentinterviews.com/blog/parallel-ai-coding-with-gitworktrees/)
- [incident.io Worktrees Blog](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)
