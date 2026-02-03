# CC-Scheduler: Prime Principles

**Created:** 2026-02-03
**Purpose:** Don't lose these during long sessions

## Distinct Concerns (Don't Conflate)

| Concern | Purpose | When |
|---------|---------|------|
| **1. Debug/Verbose** | See if stuck during execution | Runtime |
| **2. Metrics Logging** | Feed self-improvement loop | Post-execution |
| **3. Context Injection** | Task knows what it's doing | Pre-execution |
| **4. Tool Utilization** | Use skills/plugins/MCPs properly | Planning |
| **5. Review Scheduling** | Human checkpoints, approval gates | Periodic |
| **6. Task Spec Quality** | Write tasks that work autonomously | Authoring |
| **7. Beads (bd)** | Guide agents through complex tasks | Task design |

## Implementation Priority

**Now:** #2 (Metrics Logging) - enables learning
**Next:** #3 (Context Injection) - enables task awareness
**Later:** #1, #5, #6, #7 - refinements

## Self-Sustainability Principles

1. **Feedback loops require data** - Can't improve what you don't measure
2. **Tasks must be self-contained** - All context in the task file
3. **Review gates prevent drift** - Human approval at key points
4. **Beads structure complex work** - Break into verifiable steps
5. **Draw from existing tools** - Don't reinvent, reuse

## What Makes Tasks Work Autonomously

- Clear objective (what, not how)
- Success criteria (how to verify done)
- Context references (files to read)
- Constraints (what NOT to do)
- Timeout appropriate to scope

## Tools Available (Use These)

| Tool | Purpose |
|------|---------|
| Skills (bd, etc.) | Guide complex task execution |
| MCP Memory | Persist learnings across sessions |
| Obsidian | Store research, patterns |
| Hooks | Inject context, capture metrics |
| Scheduler | Coordinate timing, reviews |

## Context Loss Mitigation

- Write to files, not just conversation
- Use `<remember>` tags for critical info
- Periodic summaries to knowledge/
- Link to sources, don't duplicate

## This Session's Key Insights

1. 6-field minimal metrics schema
2. JSONL append-only history pattern
3. Env vars for context injection
4. Adopt patterns from existing repos (claude-code-scheduler, ClaudeNightsWatch)
5. Separate debug output from metrics logging
6. Review sessions are distinct from autonomous execution

---

*Updated during session to prevent context loss*
