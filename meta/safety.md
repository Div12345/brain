---
created: 2026-01-31
tags:
  - meta
  - safety
  - constraints
  - boundaries
updated: 2026-01-31T10:00
aliases:
  - safety rules
  - harm prevention
---

# Safety Constraints

> What can NEVER be harmed. Read this before ANY write operation.

## Philosophy

**"First, do no harm."**

The system can evolve aggressively within safe boundaries. But some things are sacred.

## Protected Resources (NEVER modify without explicit user approval)

| Resource | Why Protected | Safe Actions |
|----------|---------------|--------------|
| **Obsidian vault content** | User's primary knowledge base | READ only, propose changes |
| **Zotero library** | Research corpus, irreplaceable | READ only |
| **Git history** | Audit trail, versioning | Commit, never rewrite history |
| **API keys / credentials** | Security | Never read, log, or transmit |
| **Production code** | Could break working systems | Propose PRs, never direct edit |
| **System configs** | Could break machine | Propose, never apply directly |
| **User's existing workflows** | Trust built over time | Enhance, never replace without consent |

## Safe to Create/Modify

| Resource | Constraints |
|----------|-------------|
| **This brain repo** | Full write access |
| **knowledge/** | Append-only preferred |
| **logs/** | Append-only |
| **tools/** | Create new, modify own creations |
| **experiments/** | Full access |
| **Proposed configs** | In brain repo, user applies manually |

## Modification Protocol

### For Protected Resources

```
1. Identify change needed
2. Document in knowledge/proposals/
3. Create preview of change
4. Add to prompts/pending.md: "Approve change to X?"
5. Wait for explicit approval
6. Only then: execute with rollback plan
7. Log the change
```

### For Safe Resources

```
1. Identify change needed
2. Check it doesn't cascade to protected resources
3. Make change
4. Log the change
5. Verify no harm
```

## Rollback Requirements

Every modification must have:
- **Previous state captured** (git commit or archive)
- **Rollback command documented** 
- **Verification that rollback works**

## Harm Detection

If any of these occur, STOP and alert user:

| Signal | Response |
|--------|----------|
| Error during protected resource access | Stop, log, alert |
| Unexpected file deletion | Restore from archive, alert |
| API rate limit hit | Pause, reschedule, alert |
| Circular dependency in tools | Halt tool execution, debug |
| User data leaving expected paths | Block, alert |

## Parallel Execution Safety

When running multiple agents/tasks:
- **Lock files** for exclusive write
- **Check before write** that file hasn't changed
- **Atomic operations** where possible
- **Idempotent design** - running twice = same result

## Testing Protocol

Before any tool goes live:

```
1. Test in isolation (not connected to protected resources)
2. Test with mock data
3. Test failure modes (what if X fails?)
4. Test rollback
5. Limited deployment (one use case)
6. Monitor for issues
7. Gradual rollout
```

## Audit Trail

All modifications logged with:
- Timestamp
- What changed
- Why
- Who/what agent
- Rollback command

Logs in `logs/mutations/`

---

## Emergency Stop

If something goes wrong:

1. Stop all running agents
2. Check `logs/` for what happened
3. Check `archive/` for previous states
4. Rollback if needed
5. Investigate before resuming

---

*Safety enables aggression. By protecting what matters, we can move fast on everything else.*
