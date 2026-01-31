---
created: 2026-01-31
tags:
  - research
  - orchestration
  - tools
  - claude-code
updated: 2026-01-31T09:50
agent: desktop-architect
aliases:
  - claude-flow research
  - ralph pattern
---

# Orchestration Research

> Desktop agent: document research findings here.

## Executive Summary

Three major orchestration approaches exist for Claude Code coordination:

1. **Claude-Flow** — Full enterprise orchestration platform with MCP integration
2. **Oh-My-ClaudeCode** — Multi-agent parallel execution modes
3. **Ralph Wiggum Pattern** — Simple bash loop + file-based state

**Recommendation:** Start with Ralph pattern for simplicity, evaluate claude-flow for multi-agent needs.

---

## Tools Evaluated

### 1. Claude-Flow (ruvnet/claude-flow)
**URL:** https://github.com/ruvnet/claude-flow  
**Stars:** High activity, recently updated  
**Type:** Enterprise AI orchestration platform

**Key Features:**
- 60+ specialized agents in coordinated swarms
- MCP protocol integration (native Claude Code support)
- 5 execution modes: Autopilot, Ultrapilot (3-5x parallel), Swarm, Pipeline, Ecomode
- Self-learning architecture with RuVector intelligence
- Memory via AgentDB with HNSW vector search
- Hooks system for lifecycle events
- Q-Learning router for intelligent task distribution

**Architecture:**
```
User → CLI/MCP → Router → Swarm → Agents → Memory → LLM Providers
                    ↑                    ↓
                    └──── Learning Loop ←┘
```

**Installation:**
```bash
npx claude-flow@v3alpha init --wizard
```

**Best For:** Complex multi-agent coordination, enterprise use, self-optimizing systems

**Complexity:** High (steep learning curve)

---

### 2. Oh-My-ClaudeCode (Yeachan-Heo/oh-my-claudecode)
**URL:** https://github.com/Yeachan-Heo/oh-my-claudecode  
**Stars:** Active development  
**Type:** Multi-agent orchestration framework

**Key Features:**
- 5 execution modes:
  - **Autopilot** — Autonomous single agent
  - **Ultrapilot** — 3-5x parallel agents
  - **Swarm** — Coordinated agent teams
  - **Pipeline** — Sequential chains
  - **Ecomode** — Token-efficient operation
- 31+ skills, 32 specialized agents
- Zero learning curve (claims)
- Direct Claude Code integration

**Best For:** Quick parallel execution, skill-based tasks

**Complexity:** Medium

---

### 3. Ralph Wiggum Pattern (Ecosystem)
**Origin:** Geoffrey Huntley (ghuntley.com/ralph/)  
**Type:** Autonomous loop pattern

**Core Concept:**
```bash
while :; do cat PROMPT.md | claude-code ; done
```

**Key Principles:**
- Run agent repeatedly until spec complete
- Progress persists in files/git, NOT context
- Each iteration starts fresh (clean context)
- Use "backpressure" (tests, lints) to validate
- Philosophy: "Sit on the loop, not in it"

**Ecosystem Implementations:**

| Repo | Features |
|------|----------|
| `schniggie/ralph-wiggum-agent-loop` | Universal loop, any LLM |
| `KLIEBHAN/ralph-loop` | Fresh context each iteration |
| `michaelshimeles/ralphy` | Multi-agent (Claude, Codex, Cursor, Qwen) |
| `frankbria/ralph-claude-code` | Rate limiting, circuit breaker |
| `CipherScout/Ralph` | Opinionated CC harness |

**File Structure:**
```
project-root/
├── loop.sh                    # Ralph loop script
├── PROMPT_build.md            # Build mode instructions
├── PROMPT_plan.md             # Plan mode instructions
├── AGENTS.md                  # Operational guide (~60 lines max)
├── IMPLEMENTATION_PLAN.md     # Task list (generated)
└── specs/                     # Requirements
```

**Best For:** Overnight autonomous runs, simple coordination, learning

**Complexity:** Low

---

## Usage Tracking Tools

| Tool | Description | Metrics |
|------|-------------|---------|
| `ca-srg/tosage` | Go app, CLI + daemon mode | Tokens/day, Prometheus export |
| `juanjperez/claude-pulse` | Local dashboard | Costs, tokens, productivity |
| `axiomantic/heads-up-claude` | Statusline (Nim) | Real-time token tracking |

**Recommendation:** Start with `tosage` for Prometheus integration or `claude-pulse` for visual dashboard.

---

## Windows Scheduling Solutions

### Option 1: Windows Task Scheduler
**Best for:** Simple scheduled runs

```xml
<!-- See tools/configs/nightly-brain.xml -->
```

### Option 2: WSL + cron
**Best for:** Unix-like scheduling with bash scripts

```bash
# WSL crontab
0 2 * * * cd /mnt/c/brain && ./run-overnight.sh
```

### Option 3: GitHub Actions (Self-hosted runner)
**Best for:** Cloud-triggered with local execution

### Option 4: PowerShell scheduled jobs
**Best for:** Native Windows without WSL

```powershell
$trigger = New-JobTrigger -Daily -At 2am
Register-ScheduledJob -Name "BrainNightly" -Trigger $trigger -ScriptBlock {
    cd C:\brain
    claude --dangerously-skip-permissions -p "Run overnight tasks"
}
```

---

## Coordination Patterns

### Pattern 1: File-Based Task Queue (Recommended for Start)
```
brain/tasks/
├── pending/      # Tasks waiting
├── active/       # Being worked on
├── completed/    # Done
└── failed/       # Errors
```

Each task is a markdown file with YAML frontmatter.

### Pattern 2: Git Branch Coordination
- CC works on `cc-overnight` branch
- Desktop works on `desktop-tasks` branch
- Merge to main after review

### Pattern 3: Shared Context Files
```
brain/context/
├── active-agent.md    # Who's currently working
├── handoff-notes.md   # Notes between agents
└── blocking-issues.md # Problems for user
```

---

## Questions Answered

### How to schedule overnight runs on Windows?
**Answer:** Windows Task Scheduler with PowerShell launcher script is simplest. See `tools/configs/` for templates.

### How to track Claude usage/limits?
**Answer:** Use `tosage` or `claude-pulse`. These read Claude's local logs/API responses for metrics.

### How can Desktop and CC coordinate?
**Answer:** Via this repo! File-based task queue + context files. Both read CLAUDE.md, both write to shared locations.

### Self-registration protocol?
**Answer:** Already defined in `meta/orchestration.md`. Create interface file in `tools/interfaces/[name].md`.

---

## Next Steps

1. [ ] Implement simple task queue in `tasks/`
2. [ ] Create Windows Task Scheduler XML config
3. [ ] Set up CC hookify rule to check pending tasks
4. [ ] Test overnight Ralph loop
5. [ ] Evaluate claude-flow if multi-agent needed later

---

*Research completed by Desktop Orchestration Architect Agent*
