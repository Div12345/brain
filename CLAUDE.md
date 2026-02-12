---
created: 2026-01-31
tags:
  - meta
  - claude-code
  - entry-point
status: active
aliases:
  - Claude entry
  - CC entry
---

# Brain - Self-Evolving AI Assistant System

## Quick Facts
- **Purpose:** Multi-interface Claude coordination for anticipatory assistance
- **Interfaces:** Desktop Claude, Claude Code, Overnight Agent
- **Coordination:** File-based via GitHub (blackboard pattern)

## Session Start Protocol

**Always do this first:**
1. Read [[context/State.md]] — current focus, recent decisions, next actions
2. Check [[dashboards/BOARD.md]] — visual CE pipeline status
3. Check [[tasks/pending/]] — queued work

**On session end:** Update State.md with decisions made and next actions.

## Key Commands
```bash
# Check state (quick)
cat context/State.md

# Check full context
cat context/State.md && cat context/active-agents.md && ls tasks/pending/

# Commit work
git add -A && git commit -m "[type]: description"
```

## Directory Map
| Dir | Purpose |
|-----|---------|
| [[context/]] | Shared state, priorities, predictions |
| [[tasks/]] | Task queue (pending→active→completed) |
| [[knowledge/]] | Learned patterns, research |
| [[agents/]] | Agent definitions |
| [[tools/]] | Configs, scripts |
| [[prompts/]] | User Q&A |

## Critical Rules
1. Check [[context/active-agents]] before starting
2. Log to [[logs/]]
3. Check [[context/off-limits]] before modifications
4. Commit frequently for coordination
5. Generate questions → [[prompts/pending]]
6. Follow [[meta/contribution-workflow]] for PRs

## Task Claiming
1. Check [[tasks/pending/]]
2. Move to tasks/active/ with agent suffix
3. Update [[context/active-agents]]
4. Work
5. Move to completed/ or failed/

## Coordination
- **State:** [[context/session-state]] - Recovery state
- **Agents:** [[context/active-agents]] - Who's working on what
- **Handoffs:** [[context/handoff]] - Agent transitions
- **Questions:** [[prompts/pending]] / [[prompts/answered]]

## Git Workflow

```bash
# Start: create branch from main
git checkout -b claude/<task>-<session-suffix> origin/main

# Work: commit and push frequently
git add -A && git commit -m "[type]: description"
git push -u origin claude/<branch>

# Coordinate: send messages to other agents
echo "..." > messages/outbox/MSG-<timestamp>-<from>-<to>.md

# Finish: create PR or request merge
# See [[meta/contribution-workflow]] for details
```

## Compound Engineering Loop

This repo follows the compound engineering methodology: each task should make the next task easier.

### Core Principles
> Source: [Compound Engineering — How Every Codes With Agents](https://every.to/guides/compound-engineering)

- **Minimalism with necessity.** Add only what's needed. Three similar lines > premature abstraction. Delete what isn't used.
- **Systems over artifacts.** Build things that make future work easier, not one-off deliverables.
- **80/20 planning.** Plan enough to start confidently, not exhaustively. The work teaches you what the plan couldn't.
- **Each unit of work compounds.** If it doesn't make the next task easier, ask why you're doing it.
- **Taste in infrastructure.** The system should feel good to use. If it doesn't, fix the system, not the user.

### Key Directories
- `docs/plans/` — CE plan files (persistent across sessions)
- `docs/brainstorms/` — CE brainstorm files
- `docs/solutions/` — CE compound output (categorized learnings)
- `knowledge/frameworks/` — Capability registry and evaluation framework (read on demand)

### The Loop
1. **Plan** — Query past solutions → research codebase → research external → structure plan
2. **Work** — Delegate to agents, verify as you go
3. **Assess** — Multi-perspective review, evidence before claims
4. **Compound** — Capture learnings, update rules, feed back into next Plan

## Knowledge Base Auto-Triggers

When the user mentions these topics, **always search `docs/solutions/` first** before investigating:

| Keywords | Search For | Key Doc |
|----------|-----------|---------|
| throttlestop, CPU throttling, power limits, BD PROCHOT, speed shift, PL1, PL2 | `grep -r "throttlestop\|PROCHOT\|LockPowerLimits" docs/solutions/` | `2026-02-07-throttlestop-dell-non-dell-charger-fix.md` |
| Dell power, charger, battery throttle | same as above | same |

This prevents re-investigating solved problems. Read the doc, apply known fixes, THEN investigate if the issue is new.

## Obsidian Vault (via MCP)

The Obsidian vault is the user's knowledge base, accessed via MCP tools (`obsidian_read_note`, `obsidian_update_note`, etc.).

**The 3 Rules:**
1. Capture to Inbox — anything, no tags needed
2. Active interests get a Home — Command Centers in `Projects/`
3. Link when you touch — add one `[[link]]` when you open a note

**Key locations in vault:**
- `Dashboard/HOME.md` — unified hub linking all spaces
- `Meta/Vault Rules.md` — the 3 rules
- `Dashboard/State.md` — current state (all interfaces read/write)
- `Projects/{name}/Command Center.md` — home base per space

**Active spaces:** arterial analysis, phd, cooking, brain system, cardiac output estimation, room redesign

**Inbox:** ~152 notes awaiting processing (delegate to overnight agent)

## See Also
- [[meta/contribution-workflow]] - Full PR/contribution guide
- [[messages/README]] - Inter-agent messaging
- [[agents/overnight]] - Overnight agent definition
- [[HOME]] - Obsidian home page
