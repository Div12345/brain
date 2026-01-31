# Claude Code Ecosystem

> Available plugins, hooks, and patterns for agent enhancement.

## Installed Plugins

| Plugin | Scope | Key Capabilities |
|--------|-------|------------------|
| **superpowers** | Project | Brainstorming, planning, subagent-driven-development, TDD |
| **hookify** | Project | Create custom hooks via markdown to prevent/warn behaviors |
| **claude-md-management** | Project | Audit and improve CLAUDE.md files |
| **code-simplifier** | User | Simplify code |
| **commit-commands** | Project | Git commit workflows |

## Superpowers Skills

Available in `~/.claude/plugins/cache/claude-plugins-official/superpowers/4.1.1/skills/`:

| Skill | Use For |
|-------|---------|
| `brainstorming/` | Refine ideas before implementation |
| `writing-plans/` | Break work into bite-sized tasks |
| `executing-plans/` | Execute with checkpoints |
| `dispatching-parallel-agents/` | Concurrent subagent work |
| `subagent-driven-development/` | Fast iteration with two-stage review |
| `systematic-debugging/` | 4-phase root cause process |
| `verification-before-completion/` | Ensure things actually work |
| `writing-skills/` | Create new skills |

## Hookify Capabilities

Create `.claude/hookify.*.local.md` files to:

| Pattern | Action | Example |
|---------|--------|---------|
| Warn on command | Show warning | Block `rm -rf` |
| Block on pattern | Prevent action | Stop debug code |
| Check before stop | Ensure completion | Require tests run |

### Example Hook File

```markdown
---
name: warn-incomplete-task
enabled: true
event: stop
action: warn
conditions:
  - field: transcript
    operator: not_contains
    pattern: Updated priorities.md
---

⚠️ **Remember to update priorities.md before stopping!**
```

## Existing Hooks (settings.json)

```json
{
  "hooks": {
    "PreCompact": [{ "command": "bd prime" }],
    "SessionStart": [{ "command": "bd prime" }]
  }
}
```

The `bd prime` command runs on session start and before compaction.

## Custom Agents

Located in `~/.claude/agents/`:

| Agent | Purpose |
|-------|---------|
| `code-review.md` | Code review workflow |
| `context-gathering.md` | Gather context for tasks |
| `context-refinement.md` | Refine gathered context |
| `logging.md` | Logging standards |
| `service-documentation.md` | Document services |

## Integration Opportunities

### For Overnight Agent

| Opportunity | How |
|-------------|-----|
| Use superpowers brainstorming | For complex analysis decisions |
| Use writing-plans | Break vault analysis into phases |
| Create hookify rules | Based on discovered friction patterns |
| Update CLAUDE.md | Use claude-md-management patterns |

### Proposed Automations

Based on vault analysis, the agent could propose:

1. **Hook for recurring incomplete tasks**
   - Pattern: Task mentioned 3+ times without completion
   - Action: Warn and suggest re-scoping

2. **Hook for late-night work**
   - Pattern: Session active past midnight
   - Action: Warn about sleep

3. **Hook for context switch**
   - Pattern: Switching from research to admin
   - Action: Suggest energy check

---
*Last updated: 2026-01-31*
