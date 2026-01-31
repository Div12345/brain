# Claude Code Ecosystem Deep Dive

> Research compiled 2026-01-31 for brain orchestration system

## Summary

This document catalogs the best tools, patterns, and resources for Claude Code development workflows, specifically for building a self-evolving AI assistant system.

---

## 1. Usage Monitoring Tools

### ccusage (RECOMMENDED)
**GitHub:** ryoppippi/ccusage  
**Install:** `npx ccusage@latest`

The most comprehensive CLI tool for tracking Claude Code token usage.

**Key Commands:**
```bash
npx ccusage                      # Daily report (default)
npx ccusage daily --breakdown    # Per-model cost breakdown
npx ccusage monthly              # Monthly aggregated
npx ccusage blocks               # 5-hour billing windows
npx ccusage session              # Per-conversation
npx ccusage statusline           # Compact for hooks
npx ccusage --json               # JSON export for automation
```

**Why It Works:**
- Reads local JSONL files from `~/.config/claude/logs/`
- No network calls needed
- Supports date filtering, timezone, locale
- Has MCP server built-in

### Claude-Code-Usage-Monitor
**GitHub:** Maciek-roboblog/Claude-Code-Usage-Monitor  
**Install:** `pip install` or clone + `python ccusage_monitor.py`

Real-time dashboard with predictions and warnings.

**Features:**
- Live token burn rate
- Predictive warnings before hitting limits
- Color-coded progress bars
- Multi-plan support (Pro 44k, Max5 88k, Max20 220k)

**Integration:**
```bash
# Run in tmux while working
tmux new-session -d -s monitor 'python ccusage_monitor.py --plan max5'
```

### Token Limits Reference

| Plan | Tokens/5hr | ~Prompts | Cost/mo |
|------|-----------|----------|---------|
| Pro | 44,000 | 10-40 | $20 |
| Max5 | 88,000 | 20-80 | $100 |
| Max20 | 220,000 | 50-200 | $200 |
| API | Pay-as-go | Unlimited | Variable |

**Session Rules:**
- 5-hour rolling window
- Starts on first message
- Can have multiple overlapping sessions
- Resets independently per session

---

## 2. Project Configuration Patterns

### Directory Structure (Best Practice)
```
project/
├── CLAUDE.md                    # Project memory (< 150 lines!)
├── .mcp.json                    # MCP servers (team-shared)
├── .claude/
│   ├── settings.json            # Hooks, permissions
│   ├── settings.local.json      # Personal (gitignored)
│   ├── agents/                  # Subagents
│   │   └── code-reviewer.md
│   ├── commands/                # Slash commands
│   │   └── ticket.md
│   ├── hooks/                   # Hook scripts
│   │   └── skill-eval.sh
│   ├── skills/                  # Domain knowledge
│   │   └── testing/SKILL.md
│   └── rules/                   # Modular instructions
│       └── code-style.md
└── .github/
    └── workflows/
        └── pr-review.yml        # Claude-powered CI
```

### CLAUDE.md Guidelines
- **Max ~150 lines** (otherwise context rot)
- Include: stack, key commands, critical rules
- Avoid: verbose documentation (use skills instead)
- Use `/memory` to manage interactively

### Skills Format
```markdown
---
name: skill-name
description: When to use. Include trigger keywords.
allowed-tools: Read, Grep, Glob
---

# Skill Title

## When to Use
- Condition 1
- Condition 2

## Core Patterns
### Pattern Name
```code example```

## Anti-Patterns
### What NOT to Do
```bad example```
```

### Agent Format
```markdown
---
name: code-reviewer
description: Reviews code after changes
model: opus
tools: Read, Grep, Bash(git:*)
---

You are a senior code reviewer...

## Your Process
1. Run `git diff`
2. Apply checklist
3. Provide feedback
```

---

## 3. Hook System

### Hook Events

| Event | When | Use Case |
|-------|------|----------|
| `PreToolUse` | Before tool | Block edits on main |
| `PostToolUse` | After tool | Auto-format, run tests |
| `UserPromptSubmit` | Prompt sent | Suggest skills |
| `Stop` | Session end | Sync to Obsidian |

### Hook Response Format
```json
{
  "block": true,         // Block action (PreToolUse only)
  "message": "Reason",   // Show to user
  "feedback": "Info",    // Non-blocking
  "continue": false      // Whether to continue
}
```

### Exit Codes
- `0` = Success
- `2` = Blocking error (PreToolUse)
- Other = Non-blocking error

### Example: Block Main Branch
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "[ \"$(git branch --show-current)\" != \"main\" ] || { echo '{\"block\": true, \"message\": \"Cannot edit main\"}' >&2; exit 2; }",
        "timeout": 5
      }]
    }]
  }
}
```

---

## 4. Obsidian Integration

### claude-obsidian-sync
**GitHub:** Pgooone/claude-obsidian-sync

Syncs Claude Code sessions to Obsidian via hooks.

**Setup:**
1. Config at `~/.claude/obsidian-sync.json`:
```json
{
  "vaultPath": "D:/YourVault",
  "baseFolder": "ClaudeCode",
  "syncObservations": true,
  "syncSummaries": true
}
```

2. Add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": ".*",
      "hooks": [{
        "type": "command",
        "command": "npx ts-node hook-handler.ts",
        "async": true
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command", 
        "command": "npx ts-node hook-handler.ts"
      }]
    }]
  }
}
```

**Output Structure:**
```
Vault/ClaudeCode/
├── Observations/2026-01/
│   └── obs_123_title.md
└── Summaries/2026-01/
    └── sum_456_request.md
```

---

## 5. GitHub Actions Integration

### PR Review Workflow
```yaml
name: Claude PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-opus-4-5-20251101
          prompt: |
            Review this PR using code-reviewer.md standards.
            Run `git diff origin/main...HEAD`
```

### Scheduled Maintenance
- **Weekly code quality:** Review random dirs, auto-fix
- **Monthly docs sync:** Align docs with code changes  
- **Biweekly dependency audit:** Safe updates with tests

**Cost Estimate:** ~$10-50/month depending on PR volume

---

## 6. MCP Servers

### Essential MCPs

| MCP | Purpose | Config |
|-----|---------|--------|
| GitHub | PR, Issues, Commits | `@anthropic/mcp-github` |
| JIRA/Linear | Ticket workflows | `@anthropic/mcp-jira` |
| Slack | Notifications | `@anthropic/mcp-slack` |
| Postgres | DB queries | `@anthropic/mcp-postgres` |
| Playwright | Browser automation | `mcp-playwright` |

### MCP Token Warning
> "If you're using more than 20k tokens of MCPs, you're crippling Claude. That would only give you a measly 20k tokens left of actual work before context is cooked." - Community wisdom

Keep MCP footprint small. Favor focused, single-purpose servers.

---

## 7. Plugin Marketplace

### ccplugins/awesome-claude-code-plugins
The main plugin registry. Install via:
```bash
/plugin marketplace add ccplugins/marketplace
/plugin install analyze-codebase
```

### Notable Plugins

**Workflow:**
- `ultrathink` - Extended reasoning
- `lyra` - Orchestration
- `ceo-quality-controller-agent` - QA

**Code Quality:**
- `code-review` - Review checklist
- `double-check` - Verification
- `optimize` - Performance

**Documentation:**
- `analyze-codebase` - Project analysis
- `update-claudemd` - Memory management
- `changelog-generator` - Release notes

**Git:**
- `fix-github-issue` - Issue → PR workflow
- `create-pr` - PR automation
- `pr-review` - Review workflow

---

## 8. Best Practices Summary

### The "Holy Trinity"
Skills + Agents + Hooks working together:
- **Skills:** Domain knowledge (progressive disclosure)
- **Agents:** Specialized assistants (focused tools)
- **Hooks:** Automation (deterministic scripts)

### Anti-Patterns to Avoid
- Long CLAUDE.md (> 150 lines)
- Many complex slash commands
- Heavy MCP usage (> 20k tokens)
- Vibe coding without planning
- Accepting multi-file diffs when you asked for one test

### Context Management
- "It's the primary failure mode"
- Plan rigorously before coding
- Keep systems simple
- Implement quality gates
- Iterate continuously

### Workflow Pattern: Explore → Plan → Code
1. **Explore:** Read files, use subagents, don't code yet
2. **Plan:** Ask Claude to plan, use "think" / "ultrathink"
3. **Code:** Implement, verify as you go

---

## 9. Resources

### Comprehensive Guides
- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) - Full config example
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Curated list
- [zebbern/claude-code-guide](https://github.com/zebbern/claude-code-guide) - Setup guide
- [awattar/claude-code-best-practices](https://github.com/awattar/claude-code-best-practices) - Patterns

### Official Docs
- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

### Community Terms
- **Context Rot:** Degraded performance from too much context
- **Vibe Coding:** Coding without planning (creates debt)
- **Token Burn:** High consumption rate
- **Rate Limit Jail:** Hitting limits repeatedly

---

## 10. Relevance to Brain System

### Immediate Applications
1. **Usage tracking:** Deploy ccusage in context/metrics.md
2. **Hooks:** Sync sessions to brain repo via PostToolUse
3. **Skills:** Create brain-system skill for CC
4. **Overnight agent:** Use Stop hook to generate summaries

### Architecture Alignment
- Task queue = similar to /ticket workflow
- Context files = like CLAUDE.md hierarchy
- Agents = subagents pattern
- Orchestration = Ralph Wiggum or oh-my-claudecode

### Next Steps
1. Set up ccusage MCP or statusline hook
2. Create brain-specific SKILL.md
3. Configure Obsidian sync for vault analysis
4. Test overnight run with usage monitoring
