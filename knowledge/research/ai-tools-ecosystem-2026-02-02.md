# AI Tools Ecosystem Research - 2026-02-02

> Comprehensive research on context persistence, orchestration, scheduling, and self-improvement tools

## Your Current Setup

### Installed Plugins
| Plugin | Source | Purpose |
|--------|--------|---------|
| oh-my-claudecode (3.8.17) | omc | Multi-agent orchestration, 32 specialized agents |
| hookify | official | Custom hooks via markdown files |
| ralph-loop | official | Persistence until completion |
| superpowers (4.1.1) | official | Extended capabilities |
| claude-md-management | official | CLAUDE.md handling |
| code-simplifier | official | Code simplification |
| commit-commands | official | Git commits |
| feature-dev | official | Feature development |
| claude-code-setup | official | Setup utilities |

### Installed MCPs
| MCP | Connection | Purpose |
|-----|------------|---------|
| oh-my-claudecode MCP | Local | Agent tools, LSP, AST |
| paper-search | Local | Academic paper search |
| obsidian | → OneVault | Note access |
| memory (mcp-knowledge-graph) | → OneVault/.aim | Persistent knowledge graph |
| zotero | Local | Citation management |
| claude-desktop | Custom | Desktop Claude control via DevTools |
| notebooklm-mcp | Local | NotebookLM integration |

### Custom Built
- **claude-desktop MCP** (`tools/mcps/claude-desktop-mcp/`) - Controls Desktop Claude via Chrome DevTools
- **Overnight agent** (`agents/overnight.md`) - Autonomous overnight work definition
- **Multi-agent coordination** - Git-based blackboard pattern

---

## Memory & Context Persistence Tools

### 1. claude-mem (thedotmack/claude-mem) ⭐ 18k stars
- **How it works:** Automatic session capture + compression via agent-sdk
- **Storage:** Token-efficient 3-layer workflow
- **Claude Code compatible:** ✅ Yes - built as plugin
- **Best for:** Automatic capture, no manual work
- **Features:** Web viewer UI at localhost:37777, "Endless Mode" for extended sessions
- **Link:** https://github.com/thedotmack/claude-mem

### 2. Anthropic Memory MCP (@modelcontextprotocol/server-memory)
- **How it works:** LibSQL knowledge graph, stores entities and relations
- **Storage:** Local `memory.json` or `~/.memory-mcp/memory.db`
- **Claude Code compatible:** ✅ Yes - official MCP
- **Best for:** Structured knowledge, complex reasoning via graph traversal
- **YOU HAVE THIS:** Connected to OneVault/.aim
- **Config:**
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### 3. mcp-memory-service (doobidoo/mcp-memory-service)
- **How it works:** Auto-captures project context, architecture decisions, code patterns
- **Claude Code compatible:** ✅ Yes - multi-tool support
- **Best for:** Zero-intervention context persistence
- **Link:** https://github.com/doobidoo/mcp-memory-service

### 4. claude-cognitive (GMaN1911/claude-cognitive)
- **How it works:** Working memory for multi-instance coordination
- **Storage:** Structured logs with HOT/WARM/COLD file access tiers
- **Claude Code compatible:** ✅ Yes
- **Best for:** YOUR USE CASE - multi-instance coordination, abandoned sessions
- **Link:** https://github.com/GMaN1911/claude-cognitive

### 5. task-orchestrator (jpicklyk/task-orchestrator)
- **How it works:** Summary-based context passing (90% token reduction)
- **Claude Code compatible:** ✅ Yes - MCP server
- **Best for:** Token-efficient task handoffs
- **Link:** https://github.com/jpicklyk/task-orchestrator

---

## Hookify Configuration (IMPORTANT)

Hookify uses **markdown files** in `.claude/` directory - NOT settings.json hooks.

### File Format
```markdown
---
name: rule-name
enabled: true
event: bash|file|stop|prompt|all
pattern: regex_pattern
action: warn|block
---

Message to show when triggered
```

### Event Types
- `bash` - Bash tool commands
- `file` - Edit, Write, MultiEdit tools
- `stop` - When Claude wants to stop
- `prompt` - User prompt submission
- `all` - All events

### Example: Context Injection on Every Tool
Create `.claude/hookify.context-inject.local.md`:
```markdown
---
name: inject-session-context
enabled: true
event: all
action: warn
---

## Session Context (auto-injected)

Current focus: arterial_analysis (PhD ML methodology)
Core principle: Low friction above all
```

### Commands
- `/hookify <instruction>` - Create rule from description
- `/hookify:list` - List all rules
- `/hookify:configure` - Enable/disable interactively

---

## oh-my-claudecode Context Injection

OMC already has sophisticated context injection via `context-injector` feature:

### Context Sources (from types.ts)
- `keyword-detector` - Magic keywords
- `rules-injector` - Delegation rules
- `directory-agents` - AGENTS.md files
- `boulder-state` - Plan tracking (the "boulder never stops" message)
- `session-context` - Session state
- `learner` - Learned patterns
- `custom` - Custom sources

### The "boulder" System
- Files: `.omc/state/boulder.json`
- Purpose: Track plan state, enforce continuation
- Message: "The boulder never stops. Continue until all tasks complete."

---

## Orchestration Comparison

### oh-my-claudecode (YOU HAVE THIS)
- 32 specialized agents
- Smart model routing (haiku/sonnet/opus)
- Modes: autopilot, ralph, ultrawork, ecomode, swarm, pipeline
- Built-in context injection, verification, task decomposition

### Alternatives to Research
- **LangGraph** - Graph-based agent orchestration
- **CrewAI** - Multi-agent collaboration
- **AutoGen** - Microsoft's multi-agent framework
- **Agency Swarm** - Agent swarm coordination

---

## Scheduling Patterns

### For Claude Code
1. **Cron + claude CLI** - Schedule `claude --resume` or `claude --continue`
2. **tmux + watch** - Keep session alive, poll for tasks
3. **Git hooks** - Trigger Claude on commit/push
4. **File watchers** - inotify triggers Claude on file changes

### Your Overnight Agent Pattern
Uses file-based coordination:
1. Check `tasks/pending/`
2. Move to `tasks/active/` with agent suffix
3. Update `context/active-agents.md`
4. Work
5. Move to `completed/` or `failed/`

---

## Self-Referential Systems

### Voyager Pattern (Minecraft AI)
- Learns skills during gameplay
- Stores in skill library
- Retrieves similar skills for new tasks
- **Key:** Skills are CODE, not just descriptions

### Gödel Agent Pattern
- System that modifies its own prompts/code
- Requires safety bounds
- Uses reflection on outcomes

### Self-Refine Loop
1. Generate output
2. Evaluate against criteria
3. Refine based on evaluation
4. Repeat until good enough

---

## Recommended Architecture for Your Brain System

### Layer 1: Context Persistence
```
hookify rule → inject session-handoff.md content
OR
omc context-injector → register custom source
```

### Layer 2: Memory
```
mcp-knowledge-graph (ALREADY HAVE) → long-term facts
claude-mem (CONSIDER) → session capture
```

### Layer 3: Coordination
```
oh-my-claudecode (ALREADY HAVE) → orchestration
claude-desktop MCP (ALREADY HAVE) → cross-interface
Git blackboard (ALREADY HAVE) → file-based sync
```

### Layer 4: Self-Improvement
```
knowledge/patterns/ → extracted patterns
context/session-handoff.md → cross-session state
Experiment tracking → context/metrics/
```

---

## Next Steps

1. **Test hookify context injection** - Create `.claude/hookify.session-context.local.md`
2. **Consider claude-mem** - For automatic session capture
3. **Consider claude-cognitive** - For multi-instance coordination
4. **Document patterns** - Track what works in knowledge/patterns/

---

## References
- claude-mem: https://github.com/thedotmack/claude-mem
- Anthropic Memory MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
- mcp-memory-service: https://github.com/doobidoo/mcp-memory-service
- claude-cognitive: https://github.com/GMaN1911/claude-cognitive
- task-orchestrator: https://github.com/jpicklyk/task-orchestrator
- oh-my-claudecode: https://github.com/Yeachan-Heo/oh-my-claudecode
- Claude Code hooks: https://code.claude.com/docs/en/hooks
