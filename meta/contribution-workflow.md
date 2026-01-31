---
created: 2026-01-31
tags:
  - meta
  - workflow
  - git
  - contribution
updated: 2026-01-31T17:55
---

# Contribution Workflow

> How agents (and humans) contribute to the brain system via PRs.

## Philosophy

1. **Branches isolate work** - Each agent/session gets its own branch
2. **PRs are checkpoints** - Merge when work is coherent and tested
3. **Main is stable** - Only merged, reviewed work
4. **Messages coordinate** - Use `messages/` for cross-agent communication

## Branch Naming

```
claude/<task-description>-<session-suffix>
```

Examples:
- `claude/setup-web-hooks-5cMwt`
- `claude/overnight-research-a3f8`
- `claude/fix-predictions-bug-x9kL`

The session suffix comes from the Claude session URL or can be random 5 chars.

## Workflow for Remote Agents

### 1. Start Session

```bash
# Fetch latest
git fetch origin

# Create branch from main
git checkout -b claude/<task>-<suffix> origin/main

# Or continue existing branch
git checkout claude/<existing-branch>
git pull origin claude/<existing-branch>
```

### 2. Claim Work

Update `context/active-agent.md`:
```markdown
| Agent | claude-code-web |
| Task | <what you're doing> |
| Status | Working |
```

### 3. Do Work

- Commit frequently (every coherent change)
- Push after each commit (for visibility)
- Use conventional commit prefixes:

| Prefix | Use |
|--------|-----|
| `Config:` | Configuration changes |
| `Research:` | New research/knowledge |
| `Feature:` | New functionality |
| `Fix:` | Bug fixes |
| `Docs:` | Documentation |
| `Refactor:` | Code restructuring |
| `Log:` | Session logs |
| `MSG:` | Inter-agent messages |

### 4. Request Review / Merge

Option A: **Create PR** (preferred for significant work)
```bash
gh pr create --title "<type>: <description>" --base main
```

Option B: **Fast-forward merge** (for small fixes)
```bash
# Only if you have permission and changes are trivial
git checkout main
git merge --ff-only claude/<branch>
git push origin main
```

Option C: **Leave for human review**
- Push branch
- Add message to `messages/outbox/` requesting review
- Human merges via GitHub UI

### 5. Cleanup

After merge:
```bash
git checkout main
git pull origin main
git branch -d claude/<branch>  # delete local
```

## PR Guidelines

### When to PR

| Scenario | Action |
|----------|--------|
| New feature complete | PR |
| Research batch done | PR |
| Bug fix | PR (or fast-forward if trivial) |
| WIP checkpoint | Push branch, no PR yet |
| Experimental | Push branch, label as draft |

### PR Template

```markdown
## Summary
- Bullet points of what changed

## Test plan
- [ ] How to verify this works

## Related
- Links to issues, messages, or tasks

<session-url>
```

### PR Size

- **Ideal:** 1-10 files, focused on one thing
- **Acceptable:** Up to 20 files if cohesive
- **Split if:** Different concerns mixed together

## Multi-Agent Coordination

### Parallel Work

When multiple agents work simultaneously:

1. Each gets own branch
2. Communicate via `messages/`
3. Merge to main sequentially (resolve conflicts)
4. Or merge branches together first, then PR

### Conflict Resolution

```bash
# Pull latest main
git fetch origin
git merge origin/main

# If conflicts:
# - Prefer keeping both agents' work
# - Use clear merge commit messages
# - Push resolved merge
```

### Handoff Between Agents

1. Push all work to branch
2. Create message in `messages/outbox/`:
   ```markdown
   ---
   from: agent-a
   to: agent-b
   type: handoff
   ---
   # Handoff: <task>

   Branch: claude/<branch>
   Status: <ready for review | needs more work | blocked>

   ## What's done
   - ...

   ## What's left
   - ...
   ```
3. Other agent pulls and continues

## For Humans

You can:
- Merge PRs via GitHub UI
- Push directly to main (you're the owner)
- Create issues for agents to pick up
- Review agent work before merge

## Automation Ideas

Future improvements:
- [ ] GitHub Action to auto-label agent PRs
- [ ] Webhook to notify agents of new tasks
- [ ] Auto-merge if tests pass
- [ ] PR template enforcement

## Related

- [[messages/README]] - Inter-agent messaging
- [[context/active-agent]] - Who's working
- [[tools/orchestration/AUTO-CONTINUE]] - Session recovery
- [[CLAUDE]] - Agent entry point
