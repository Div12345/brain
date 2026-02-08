---
created: 2026-02-08
tags:
  - solution
  - orchestration
  - fallback
  - infrastructure
---

# Multi-Provider Fallback Orchestration

> How to keep working continuously across OpenCode, Claude Desktop, and Gemini CLI with proper knowledge persistence.

## The Problem

Different providers have different limits:
- **CC Web/API**: 5-hour session limits, weekly caps
- **Claude Desktop**: Session limits only, NO weekly caps
- **Gemini CLI**: Large free tier, fast
- **OpenCode + Antigravity**: Unknown limits (Google-provided)

When one exhausts, work shouldn't stop.

## The Solution: Layered Fallback with Shared Knowledge

### Knowledge Layer (Always Accessible)

All interfaces read/write to the same sources:

| Source | Purpose | Access |
|--------|---------|--------|
| `Dashboard/State.md` (Obsidian) | Current focus, what just happened, next actions | Obsidian MCP |
| `Projects/brain system/compound-log.md` | Accumulated learnings across sessions | Obsidian MCP |
| `brain/docs/solutions/` | Reusable patterns and solutions | Filesystem (Git) |
| Zotero library | Paper references, annotations | Zotero MCP |

### Execution Layer (Prioritized Fallback)

```
Primary:   OpenCode + Antigravity
           ↓ (if exhausted)
Fallback:  Claude Desktop (session-only limit, ideal for overnight)
           ↓ (if session done)
Fallback:  Gemini CLI (can control Desktop via MCP!)
           ↓ (if all fail)
Fallback:  New OpenCode session
```

## Key Patterns

### 1. Staged Work via Claude Desktop

From any terminal:
```bash
cd /home/div/brain/tools/mcps/claude-desktop-mcp
source .venv/bin/activate
python -c "
from server import *
ws = get_main_process_ws()
ensure_debugger_attached(ws)
create_new_chat(ws)
send_message(ws, 'Your task here...')
ws.close()
"
```

Check back later:
```bash
python -c "
from server import *
ws = get_main_process_ws()
ensure_debugger_attached(ws)
messages = get_messages(ws)
print(messages[-1].get('text', '')[:2000] if messages else 'No response yet')
ws.close()
"
```

### 2. Gemini CLI as Orchestrator

Gemini CLI has `claude-desktop` MCP configured. From Gemini:
```
Use claude_desktop_send to ask Claude Desktop to research X
```

### 3. Session Handoff Protocol

Before ending any session:
1. Update `Dashboard/State.md` via Obsidian MCP
2. If learnings: append to `compound-log.md`
3. If reusable: create `brain/docs/solutions/` file
4. Commit brain repo: `git add -A && git commit -m "[compound]: session learnings"`

## Provider Capabilities Matrix

| Capability | OpenCode | Claude Desktop | Gemini CLI |
|------------|----------|----------------|------------|
| Obsidian MCP | ✅ | ✅ | ✅ |
| Zotero MCP | ✅ | ✅ | ⚠️ (disconnected) |
| Paper Search | ✅ | ✅ | ✅ |
| Claude Desktop Control | N/A | N/A | ✅ |
| Context7 | ✅ | ✅ | ❌ |
| Subagents | ✅ | ❌ | ❌ |
| Background tasks | ✅ | ❌ | ❌ |

## When to Use Which

| Scenario | Use |
|----------|-----|
| Complex multi-file coding | OpenCode |
| Long research, reading papers | Claude Desktop (no weekly limit!) |
| Quick orchestration, delegation | Gemini CLI |
| Overnight autonomous work | Claude Desktop via MCP |
| Parallel exploration | OpenCode subagents |

## Setup Requirements

1. **Claude Desktop debugger enabled**: Help > Enable Main Process Debugger
2. **Gemini CLI authenticated**: `gemini` should work without prompts
3. **OpenCode config**: `~/.config/opencode/opencode.json` with Antigravity models
4. **All MCPs pointing to same Obsidian vault**: OneVault via local REST API

## Troubleshooting

### Claude Desktop not responding to MCP
```bash
curl -s http://127.0.0.1:9229/json  # Should show debugger targets
```
If empty: restart Claude Desktop with debugger enabled.

### Obsidian MCP errors
Check Obsidian is running and Local REST API plugin enabled (port 27124).

### Gemini CLI sandbox errors
Use `GEMINI_SANDBOX=false` prefix or configure in settings.

---

*Created during session: OpenCode + Antigravity Opus 4.5, 2026-02-08*
