---
created: 2026-01-31
tags:
  - research
  - orchestration
  - multi-agent
  - coordination
status: active
agent: overnight
aliases:
  - coordination patterns
  - multi-agent patterns
---

# Multi-Agent Coordination Patterns

Research on patterns for coordinating autonomous AI agents, specifically for the brain system.

## Core Patterns

### 1. Blackboard (RECOMMENDED for Brain)
Shared state space all agents read/write to.

**How it works:**
- Central "blackboard" holds current state
- Agents watch for changes, contribute when able
- No central orchestrator required
- Coordination emerges from shared state

**Brain implementation:**
- GitHub repo = blackboard
- `context/` files = shared state
- `context/session-state.md` = current work
- Commit messages = broadcast notifications

**Pros:** Simple, decentralized, async-friendly
**Cons:** Potential race conditions, need conflict resolution

### 2. Orchestrator-Worker
Central coordinator delegates to specialized workers.

**When to use:**
- Clear task decomposition possible
- Need centralized control/monitoring
- Workers have distinct specializations

**Not for brain:** Adds complexity, single point of failure

### 3. Handoff
Sequential passing between specialized agents.

**When to use:**
- Pipeline processing
- Each stage needs different capabilities
- Order matters

**Brain example:** overnight → user review → claude-code implementation

### 4. Swarm/Decentralized
Peer agents coordinate through shared memory, no leader.

**When to use:**
- Agents have similar capabilities
- Need fault tolerance
- Emergent behavior acceptable

## Key Patterns from Anthropic Research

From [How we built our multi-agent research system](https://anthropic.com/engineering/multi-agent-research-system):

### Subagent Output to Filesystem
> "Direct subagent outputs can bypass the main coordinator... implement artifact systems where specialized agents can create outputs that persist independently."

**Principle:** Agents write to shared storage, pass lightweight references.
**Brain:** Push to GitHub, reference paths/commits.

### Immutable Log
> "Every event or command an agent processes is recorded in a log that is permanent and unchangeable."

**Principle:** Single source of truth via append-only history.
**Brain:** Git commits = immutable log.

### Distributed Context
> "This distributed approach prevents context overflow while preserving conversation coherence."

**Principle:** Don't pass everything through coordinator.
**Brain:** Each agent reads repo state directly.

## Brain Coordination Protocol

### Current Implementation (Blackboard)

```
Agent A                    GitHub (Blackboard)                   Agent B
   |                              |                                  |
   |-- read session-state ------->|                                  |
   |-- check recent commits ----->|                                  |
   |                              |<----- read session-state --------|
   |-- do work                    |                                  |
   |-- commit changes ----------->|                                  |
   |-- update session-state ----->|                                  |
   |                              |<----- pull changes --------------|
   |                              |<----- continue different work ---|
```

### Conflict Avoidance
1. Check recent commits before starting
2. Claim work area in commit message prefix
3. Work on different files/topics
4. Update session-state after each task

### Recommended Commit Prefixes
- `Research:` - Adding knowledge/research
- `Obsidian:` - Vault formatting
- `Coordination:` - State updates
- `Task:` - Task queue operations
- `Agent:` - Agent definitions

## Future Improvements

### Phase 1: Claim System
Add to `context/active-agents.md`:
```yaml
agents:
  - id: overnight-A
    claiming: knowledge/research/
    since: 2026-01-31T09:00
```

### Phase 2: Message Queue
Add `context/messages/` for agent-to-agent comms:
```
messages/
  2026-01-31-0901-overnight-A-to-all.md
  2026-01-31-0905-overnight-B-to-overnight-A.md
```

### Phase 3: Orchestrator (if needed)
Only if coordination overhead exceeds value of independence.

## Related
- [[context/session-state]] - Current blackboard state
- [[agents/overnight]] - Agent definition
- [[inspirations/claude-code-ecosystem]] - CC coordination
