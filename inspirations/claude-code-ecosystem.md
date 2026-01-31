---
created: 2026-01-31
tags:
  - research
  - claude-code
  - tools
  - ecosystem
status: active
agent: overnight
aliases:
  - CC ecosystem
  - Claude Code tools
  - ccusage
---

# Claude Code Ecosystem Deep Dive

Catalogs tools, patterns, and resources for Claude Code workflows, specifically for building a self-evolving AI assistant system.

## 1. Usage Monitoring Tools

### ccusage (RECOMMENDED)
**GitHub:** [ryoppippi/ccusage](https://github.com/ryoppippi/ccusage)  
**Install:** `npx ccusage@latest`

```bash
npx ccusage                      # Daily report (default)
npx ccusage daily --breakdown    # Per-model cost breakdown
npx ccusage monthly              # Monthly aggregated
npx ccusage blocks               # 5-hour billing windows
npx ccusage session              # Per-conversation
npx ccusage statusline           # Compact for hooks
npx ccusage --json               # JSON export for automation
```

- Reads local JSONL from `~/.config/claude/logs/`
- No network calls, has MCP server built-in

### Claude-Code-Usage-Monitor
**GitHub:** [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)

Real-time dashboard with live burn rate, predictive warnings, color-coded progress.

### Token Limits Reference

| Plan | Tokens/5hr | ~Prompts | Cost/mo |
|------|-----------|----------|---------|
| Pro | 44,000 | 10-40 | $20 |
| Max5 | 88,000 | 20-80 | $100 |
| Max20 | 220,000 | 50-200 | $200 |

5-hour rolling window, starts on first message, can overlap sessions.

---

## 2. Project Configuration

### Directory Structure
```
project/
├── CLAUDE.md                    # < 150 lines!
├── .mcp.json                    # MCP servers
├── .claude/
│   ├── settings.json            # Hooks, permissions
│   ├── agents/                  # Subagents
│   ├── commands/                # Slash commands
│   ├── hooks/                   # Hook scripts
│   ├── skills/                  # Domain knowledge
│   └── rules/                   # Modular instructions
└── .github/workflows/
```

See [[.claude/skills/brain-system/SKILL|Brain System Skill]] for our implementation.

---

## 3. Hook System

| Event | When | Use Case |
|-------|------|----------|
| `PreToolUse` | Before tool | Block edits on main |
| `PostToolUse` | After tool | Auto-format, run tests |
| `UserPromptSubmit` | Prompt sent | Suggest skills |
| `Stop` | Session end | Sync to Obsidian |

Exit codes: `0` = success, `2` = blocking error

---

## 4. Obsidian Integration

### claude-obsidian-sync
**GitHub:** [Pgooone/claude-obsidian-sync](https://github.com/Pgooone/claude-obsidian-sync)

Syncs CC sessions to Obsidian via hooks → creates observations + summaries.

Relevant for [[agents/overnight]] session logging.

---

## 5. MCP Servers

| MCP | Purpose |
|-----|---------|
| GitHub | PR, Issues, Commits |
| JIRA/Linear | Ticket workflows |
| Slack | Notifications |
| Postgres | DB queries |
| Playwright | Browser automation |

> **Warning:** "If you're using more than 20k tokens of MCPs, you're crippling Claude." Keep footprint small.

---

## 6. Plugin Marketplace

**Registry:** [ccplugins/awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins)

Notable: `ultrathink`, `lyra`, `code-review`, `fix-github-issue`, `analyze-codebase`

---

## 7. Best Practices

### Holy Trinity
- **Skills:** Domain knowledge (progressive disclosure)
- **Agents:** Specialized assistants (focused tools)  
- **Hooks:** Automation (deterministic scripts)

### Anti-Patterns
- Long CLAUDE.md (> 150 lines) → context rot
- Heavy MCP usage (> 20k tokens)
- Vibe coding without planning

### Workflow: Explore → Plan → Code
1. **Explore:** Read files, use subagents
2. **Plan:** "think" / "ultrathink"
3. **Code:** Implement, verify

---

## 8. Resources

- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) - Full config
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### Community Terms
- **Context Rot:** Degraded performance from overloaded context
- **Vibe Coding:** Coding without planning
- **Token Burn:** High consumption rate

---

## Relevance to Brain System

1. **Usage tracking:** Deploy ccusage → [[context/metrics]]
2. **Hooks:** Sync sessions via PostToolUse
3. **Skills:** See [[.claude/skills/brain-system/SKILL]]
4. **Overnight:** Use Stop hook for summaries

Architecture maps to:
- Task queue = /ticket workflow
- Context files = CLAUDE.md hierarchy
- [[agents/overnight]] = subagents pattern

## Related
- [[knowledge/research/ai-memory-systems]] - Memory architecture
- [[tasks/pending/task-cc-001-hooks-setup]] - Implementation task
- [[agents/overnight]] - Uses these patterns
