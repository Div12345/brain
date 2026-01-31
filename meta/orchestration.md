# Orchestration Architecture

> The brain coordinates multiple AI interfaces, routes work intelligently, and evolves its own coordination capabilities.

## Vision

A **meta-orchestration layer** that:
- Coordinates multiple AI interfaces (Claude Code, Claude Desktop, Gemini CLI, etc.)
- Routes work based on capability, availability, and rate limits
- Allows new agents/interfaces to self-register
- Optimizes across all available compute
- Self-extends its orchestration capabilities

## Interface Inventory

### Current

| Interface | Access | Capabilities | Limits | Status |
|-----------|--------|--------------|--------|--------|
| **Claude.ai (Opus)** | Web/API | Full reasoning, MCPs, tools | Message limits | ✅ Active |
| **Claude Code** | Terminal | Code execution, file ops, MCPs | Token/time limits | ✅ Active |
| **Desktop Commander MCP** | Via Claude | System access | None | ✅ Active |

### Planned

| Interface | Access | Capabilities | Limits | Status |
|-----------|--------|--------------|--------|--------|
| **Claude Desktop (Enterprise)** | App | Projects, artifacts, MCPs | Enterprise quota | 🔜 Planned |
| **Gemini CLI (WSL)** | Terminal | Google models, different strengths | API limits | 🔜 Planned |
| **Local LLMs** | Ollama/LMStudio | Unlimited, private, weaker | Hardware | 🔜 Future |

## Orchestration Plugins to Evaluate

| Plugin | What It Does | Link |
|--------|--------------|------|
| **Ralph Wiggum** | Claude Code orchestration, task management | Research needed |
| **Oh My Claude Code** | Enhanced Claude Code workflows | Research needed |
| **claude-flow** | Multi-agent orchestration | GitHub |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BRAIN REPO (GitHub)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   context/  │  │  knowledge/ │  │    logs/    │            │
│  │   state     │  │   insights  │  │   activity  │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                         │                                      │
│              ┌──────────┴──────────┐                          │
│              │   ORCHESTRATOR      │                          │
│              │   (routing logic)   │                          │
│              └──────────┬──────────┘                          │
└─────────────────────────┼───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Claude Code   │ │ Claude Desktop│ │  Gemini CLI   │
│ (Terminal)    │ │ (Enterprise)  │ │  (WSL)        │
│               │ │               │ │               │
│ • Code exec   │ │ • Projects    │ │ • Different   │
│ • MCPs        │ │ • Artifacts   │ │   strengths   │
│ • File ops    │ │ • Memory      │ │ • Google APIs │
└───────────────┘ └───────────────┘ └───────────────┘
```

## Routing Logic

### By Task Type

| Task Type | Best Interface | Fallback |
|-----------|---------------|----------|
| Code execution | Claude Code | - |
| Deep analysis | Opus (web) | Desktop |
| Quick queries | Haiku/Gemini | Any |
| File operations | Claude Code + DC | Desktop |
| Research | Opus + web search | Gemini |
| Long-running | Overnight agent | - |

### By Availability

```
1. Check rate limits across all interfaces
2. Check current task queue
3. Match task to capable interface with availability
4. Route with context from brain repo
5. Collect output back to brain repo
6. Update usage metrics
```

### By Cost/Efficiency

| Priority | Use |
|----------|-----|
| Free/included quota first | Claude Desktop Enterprise |
| Then API with budget | Claude Code |
| Then fallback | Gemini, local |

## Usage Metrics Tracking

### What to Track

| Metric | Where | Why |
|--------|-------|-----|
| Messages sent per interface | `context/usage.md` | Avoid hitting limits |
| Tokens used | `context/usage.md` | Cost awareness |
| Success rate per task type | `logs/metrics/` | Route to best interface |
| Latency | `logs/metrics/` | User experience |
| Errors | `logs/errors/` | Reliability |

### Metrics Schema

```yaml
# context/usage.md - updated by orchestrator
interfaces:
  claude_code:
    messages_today: N
    tokens_today: N
    limit_remaining: N
    last_error: null
  claude_desktop:
    messages_today: N
    limit_remaining: N
  gemini_cli:
    requests_today: N
    quota_remaining: N
```

## Self-Registration Protocol

New agents/interfaces can join by:

1. **Create registration file** in `tools/interfaces/[name].md`:

```markdown
---
name: [interface-name]
type: llm | tool | service
status: available | limited | offline
capabilities:
  - capability1
  - capability2
limits:
  messages_per_day: N
  tokens_per_request: N
auth:
  method: api_key | oauth | none
  config_location: [path or env var]
---

# [Interface Name]

## How to Invoke
[Command or API call]

## Best For
[Task types this excels at]

## Limitations
[What it can't do]
```

2. **Orchestrator discovers** new interface on next run
3. **Validates** it can connect
4. **Adds to routing table**

## Communication Channels

### Between Interfaces

| From | To | Method |
|------|-----|--------|
| Any | Brain repo | GitHub API / git |
| Claude Code | Desktop | File drop in shared folder |
| Desktop | Claude Code | File drop / webhook |
| Any | User | prompts/pending.md |
| User | Any | prompts/answered.md |

### Async Task Queue

```
brain/tasks/
├── pending/          # Tasks waiting to be picked up
│   └── task-001.md   # Task spec with requirements
├── active/           # Tasks being worked on
│   └── task-002.md   # Claimed by interface X
├── completed/        # Finished tasks
│   └── task-003.md   # With results
└── failed/           # Failed tasks
    └── task-004.md   # With error info
```

### Task Spec Format

```markdown
---
id: task-[timestamp]-[random]
created: ISO timestamp
priority: high | medium | low
requires:
  - capability1
  - capability2
preferred_interface: [name] | any
timeout: 30m
---

# Task: [Description]

## Input
[What the task needs]

## Expected Output
[What success looks like]

## Context
[Links to relevant brain files]
```

## Scheduling & Automation

### Options to Explore

| Method | Platform | Use Case |
|--------|----------|----------|
| Windows Task Scheduler | Windows | Scheduled overnight runs |
| cron (WSL) | Linux | Periodic tasks |
| GitHub Actions | Cloud | Triggered workflows |
| Watchdog process | Local | File-change triggers |

### Scheduling Integration

```
1. Scheduler triggers at configured time
2. Launches appropriate interface
3. Passes task from brain/tasks/pending/
4. Interface executes, writes to brain repo
5. Scheduler checks completion, handles failures
```

## Authentication & Secrets

### Principles

| Rule | Implementation |
|------|----------------|
| Never store secrets in repo | Use environment variables |
| Never log secrets | Redact in all outputs |
| Rotate regularly | Track in secure location |
| Minimum privilege | Each interface gets only what it needs |

### Auth Config Location

```
# Not in repo - in local secure storage
~/.brain-secrets/
├── claude-api-key
├── github-token
├── gemini-api-key
└── ...
```

Interfaces reference via environment:
```bash
export CLAUDE_API_KEY=$(cat ~/.brain-secrets/claude-api-key)
```

## Evolution Path

### Phase 1: Single Interface (Current)
- [x] Brain repo structure
- [x] Agent definitions
- [ ] First overnight run
- [ ] Validate basic loop

### Phase 2: Usage Awareness
- [ ] Track Claude Code usage
- [ ] Surface limits in context/usage.md
- [ ] Warn before hitting limits

### Phase 3: Multi-Interface
- [ ] Add Claude Desktop Enterprise
- [ ] Add Gemini CLI (WSL)
- [ ] Basic routing logic

### Phase 4: Orchestration
- [ ] Install/evaluate orchestration plugin
- [ ] Implement task queue
- [ ] Cross-interface communication

### Phase 5: Self-Extension
- [ ] Self-registration protocol working
- [ ] New interfaces auto-discovered
- [ ] Routing optimizes based on history

---

*The orchestration layer is itself an agent - it learns and improves how it coordinates.*
