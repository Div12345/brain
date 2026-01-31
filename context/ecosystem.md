---
created: 2026-01-31
tags:
  - context
  - tools
  - claude-code
status: active
aliases:
  - CC ecosystem
  - plugins
---

# Claude Code Ecosystem

> Available plugins, hooks, and patterns. See also [[inspirations/claude-code-ecosystem]].

## Installed Plugins

| Plugin | Scope | Capabilities |
|--------|-------|-------------|
| **superpowers** | Project | Brainstorming, planning, subagents, TDD |
| **hookify** | Project | Custom hooks via markdown |
| **claude-md-management** | Project | Audit CLAUDE.md files |
| **code-simplifier** | User | Simplify code |
| **commit-commands** | Project | Git workflows |

## Superpowers Skills

Path: `~/.claude/plugins/cache/claude-plugins-official/superpowers/4.1.1/skills/`

| Skill | Use For |
|-------|---------|
| `brainstorming/` | Refine ideas |
| `writing-plans/` | Break work into tasks |
| `executing-plans/` | Execute with checkpoints |
| `dispatching-parallel-agents/` | Concurrent work |
| `subagent-driven-development/` | Fast iteration |
| `systematic-debugging/` | Root cause analysis |
| `verification-before-completion/` | Ensure completion |

## Hookify

Create `.claude/hookify.*.local.md` files:

| Pattern | Action | Example |
|---------|--------|---------|
| Warn on command | Show warning | Block `rm -rf` |
| Block on pattern | Prevent action | Stop debug code |
| Check before stop | Ensure completion | Require tests |

## Custom Agents

Path: `~/.claude/agents/`

| Agent | Purpose |
|-------|---------|
| `code-review.md` | Review workflow |
| `context-gathering.md` | Gather context |
| `logging.md` | Logging standards |

## Integration with Brain

| Opportunity | How |
|-------------|-----|
| Use superpowers brainstorming | Complex analysis |
| Use writing-plans | Break vault analysis |
| Create hookify rules | Based on friction patterns |

## Related
- [[inspirations/claude-code-ecosystem]] - Deep dive research
- [[tasks/pending/task-cc-001-hooks-setup]] - Hook setup task
- [[context/capabilities]] - System capabilities
