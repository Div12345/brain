# CLAUDE.md - Self-Evolving Brain System

> This file is read FIRST by any AI agent. It bootstraps the entire system.

## What This Is

A **self-recursive, self-building AI assistant system** that:
- Learns your patterns and anticipates needs
- Builds its own tools (MCPs, plugins, hooks) when gaps identified
- Experiments scientifically with logging and measurement
- Proactively prompts you for information to improve itself
- Tracks Claude usage limits and optimizes around them
- Never harms existing systems while improving

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Anticipate, don't wait** | Predict what user will need based on patterns |
| **Build tools when gaps exist** | Create MCPs, plugins, hooks as needed |
| **Scientific experimentation** | Hypothesis → test → measure → learn |
| **Proactive communication** | Ask user questions to improve understanding |
| **No harm** | Parallel work, sandboxed tests, never break working things |
| **Usage-aware** | Track Claude limits, optimize token efficiency |
| **Learn from the best** | GitHub repos, Reddit workflows, blog posts |

## Directory Structure

```
brain/
├── CLAUDE.md                 # This file - system bootstrap
├── context/                  # Current state
│   ├── priorities.md         # What to focus on
│   ├── philosophy.md         # User's principles (from vault)
│   ├── ecosystem.md          # Available tools/plugins
│   ├── predictions.md        # What user might need next
│   └── usage.md              # Claude limits, token tracking
├── knowledge/                # Discovered insights
│   ├── patterns/             # Behavioral patterns
│   ├── insights/             # Synthesized understanding
│   └── experiments/          # Scientific experiment logs
├── tools/                    # Self-built tools
│   ├── mcps/                 # Custom MCP servers
│   ├── plugins/              # Claude Code plugins
│   ├── hooks/                # Hookify rules
│   ├── commands/             # Custom slash commands
│   └── configs/              # Configuration templates
├── experiments/              # Active experiments
│   ├── hypotheses.md         # What we're testing
│   ├── active/               # Running experiments
│   └── results/              # Completed experiment results
├── prompts/                  # Proactive questions for user
│   ├── pending.md            # Questions to ask
│   └── answered.md           # User's responses (learnings)
├── inspirations/             # External sources
│   ├── github-repos.md       # Useful repos discovered
│   ├── workflows.md          # Reddit/blog workflows
│   └── tools.md              # Tools worth building
├── logs/                     # Activity logs
├── agents/                   # Agent instructions
└── meta/                     # System self-documentation
```

## Agent Workflow

```
1. Read CLAUDE.md (this file)
2. Read context/* for current state
3. Check prompts/pending.md - any questions to ask user?
4. Check predictions.md - anything user might need now?
5. Do assigned task
6. Log with scientific rigor (experiments/)
7. Identify gaps → propose tools to build (tools/)
8. Update predictions based on new patterns
9. Generate new questions for user (prompts/)
```

## Tool Building Protocol

When a gap is identified:

1. **Document the gap** in `inspirations/tools.md`
2. **Search for existing solutions** (GitHub, npm, PyPI)
3. **If none suitable, design minimal solution**
4. **Build in `tools/` with tests**
5. **Experiment with it** (scientific logging)
6. **If successful, propose integration**
7. **If fails, document why in experiments/results/**

## Scientific Logging Standard

Every action should be loggable as:

```markdown
## Experiment: [Name]

**Hypothesis:** [What we expect]
**Method:** [What we did]
**Observations:** [What happened]
**Result:** Confirmed / Refuted / Inconclusive
**Learning:** [What this teaches us]
**Next:** [Follow-up experiment or action]
```

## Proactive Communication

The system should generate questions when it:
- Notices patterns it doesn't understand
- Needs clarification to predict better
- Has built something and wants feedback
- Sees an opportunity the user might not know about

Questions go in `prompts/pending.md`. User answers go in `prompts/answered.md`.

## Safety Rails

| Rule | Why |
|------|-----|
| **Never delete without archive** | Reversibility |
| **Test in isolation first** | No breaking production |
| **Ask before major changes** | User consent |
| **Track all mutations** | Audit trail |
| **Fail gracefully** | Don't crash on errors |
| **Respect rate limits** | Don't burn API quota |

## Linked Resources

- **Obsidian Vault**: Via Obsidian MCP
- **Zotero**: Via Zotero MCP  
- **GitHub**: Via GitHub MCP
- **Desktop**: Via Desktop Commander MCP
- **Claude Code**: Plugins in `~/.claude/plugins/`

## Current Focus

See `context/priorities.md`

---

*This system evolves. Agents should update this file when fundamental changes occur.*
