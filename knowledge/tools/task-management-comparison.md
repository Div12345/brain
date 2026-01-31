---
created: 2026-01-31
tags:
  - knowledge
  - comparison
  - tools
  - task-management
updated: 2026-01-31T10:40
agent: claude-code-web
---

# Task Management Alternatives Comparison

> Comparing options before choosing a task management approach.

## Alternatives Evaluated

### 1. Current File-Based System (tasks/)

**What:** Markdown files in `tasks/{pending,active,completed,failed}/`

| Pros | Cons |
|------|------|
| Simple, no dependencies | No structured IDs |
| Human-readable | Manual priority management |
| Works anywhere | No dependency tracking |
| Zero setup | Context loss on agent compaction |

**Best for:** Simple workflows, getting started

### 2. Beads (bd) by Steve Yegge

**What:** Git-backed JSONL issue tracker for AI agents

| Pros | Cons |
|------|------|
| Agent-optimized (JSON output) | Requires installation |
| Git-backed (survives compaction) | Learning curve |
| Dependency tracking | New tool to maintain |
| Hash-based IDs (no conflicts) | May be overkill for simple use |
| Active development (1K+ stars) | Young project (weeks old) |

**Best for:** Long-horizon agent work, multi-agent coordination

### 3. GitHub Issues via CLI

**What:** Use `gh issue` commands for tracking

| Pros | Cons |
|------|------|
| Standard, well-known | Requires internet |
| Good GitHub integration | Slower than local |
| Labels, milestones, projects | Limited offline use |
| API access | API rate limits |

**Best for:** Public projects, team collaboration

### 4. Linear/Jira via MCP

**What:** External issue trackers via MCP servers

| Pros | Cons |
|------|------|
| Enterprise features | External dependency |
| Team collaboration | More setup |
| Rich workflows | Cost for some |

**Best for:** Enterprise teams, existing workflows

### 5. TodoWrite (Built-in)

**What:** Claude Code's built-in todo tracking

| Pros | Cons |
|------|------|
| Zero setup | Session-scoped |
| Always available | Lost on compaction |
| Simple interface | No persistence |

**Best for:** Single session tracking

## Comparison Matrix

| Feature | File-based | Beads | GitHub | Linear/Jira | TodoWrite |
|---------|------------|-------|--------|-------------|-----------|
| Setup | None | Install | None | Account | None |
| Dependencies | ❌ | ✅ | ✅ | ✅ | ❌ |
| Survives compaction | ✅ | ✅ | ✅ | ✅ | ❌ |
| Offline | ✅ | ✅ | ❌ | ❌ | ✅ |
| Agent-optimized | ❌ | ✅ | ❌ | ❌ | ✅ |
| Git integration | ✅ | ✅ | ✅ | ❌ | ❌ |
| Learning curve | Low | Medium | Low | High | None |
| Multi-agent safe | ❌ | ✅ | ✅ | ✅ | ❌ |

## Auto-Continuation Alternatives

For keeping agents running after compaction/errors:

### 1. Ralph Wiggum Pattern (Simple Loop)

```bash
while :; do
    cat PROMPT.md | claude-code
    sleep 5
done
```

| Pros | Cons |
|------|------|
| Dead simple | No state tracking |
| Works immediately | Blind restarts |
| Universal | No error handling |

### 2. Scheduled Task + State File

```bash
# Check state, continue if needed
if [ -f "state/in_progress" ]; then
    claude -p "Continue from state/current_task.md"
fi
```

| Pros | Cons |
|------|------|
| State-aware | Custom script needed |
| Can resume mid-work | More complexity |
| Error logging | Maintenance burden |

### 3. ccswarm (Rust Orchestrator)

| Pros | Cons |
|------|------|
| High performance | Rust dependency |
| Channel-based messaging | Steeper learning |
| Worktree isolation | More infrastructure |

### 4. Claude Flow (Enterprise)

| Pros | Cons |
|------|------|
| 60+ agents | Complex setup |
| Built-in recovery | Enterprise-focused |
| MCP native | May be overkill |

## Recommendation

### For Brain System (Current Stage)

**Task Management:**
1. **Keep file-based** for now (simple, working)
2. **Evaluate Beads** when multi-agent coordination needed
3. **Consider GitHub Issues** if team grows

**Auto-Continuation:**
1. **Start with Ralph pattern** (simple loop)
2. **Add state checking** (check session-state.md)
3. **Graduate to ccswarm** if performance needed

### Migration Path

```
Current (file-based)
    ↓ (when needed)
Beads (for dependencies)
    ↓ (when needed)
ccswarm/Claude Flow (for scale)
```

## Decision Criteria

Before switching, answer:
1. Is current approach causing friction? (If no, keep it)
2. Is the new tool actively maintained?
3. Can we easily migrate back?
4. Is setup time justified?

## Related

- [[knowledge/tools/beads-integration]] - Beads details
- [[inspirations/multi-agent-tools]] - Orchestration options
- [[inspirations/orchestration-research]] - Previous research
