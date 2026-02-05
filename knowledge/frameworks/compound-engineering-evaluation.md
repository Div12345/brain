# Compound Engineering Evaluation Framework

## Summary
A principled methodology for evaluating tools, plugins, MCPs, and workflow components. Derived from Every.to's compound engineering philosophy: each unit of work should make the next unit easier.

## The Core Test
> Does this component make the system compound — does its output feed back into future iterations to reduce friction?

## The Four-Step Loop
Every component in the system should serve one of these steps:

| Step | Purpose | Examples |
|------|---------|----------|
| **Plan** | Research before code. Query past solutions, codebase history, framework docs, best practices. | Context7, Paper Search, learnings query, brainstorm persistence |
| **Work** | Execute the plan. Agents write code, self-test via browser/simulator, iterate. | Execution agents, Playwright MCP, parallelism modes |
| **Assess** | Multi-perspective quality evaluation. Security, performance, complexity, patterns — in parallel. | Review agents, LSP diagnostics, linters, testing |
| **Compound** | Capture learnings so the next Plan step is better. Auto-extract problem/root-cause/fix/prevention. | Knowledge capture skills, hookify rules, CLAUDE.md updates, AIM Memory |

## Evaluation Checklist (5 Questions)

For any new tool/plugin/MCP, answer these:

### 1. Which loop step does it serve?
- Plan / Work / Assess / Compound / None
- If **None** → probably overhead. Strong justification needed.

### 2. Does it compound?
- Does its output feed back into future iterations, or is it one-shot?
- **Compounds:** Output persists and is queryable by future agents (knowledge docs, memory graphs, hookify rules, updated CLAUDE.md)
- **One-shot:** Output is consumed once and discarded (stdout, terminal logs, review comments that aren't captured)
- One-shot tools are acceptable only if friction cost is very low

### 3. What does it overlap with?
- List every existing component serving the same loop step
- If >50% overlap with something installed → don't add unless strictly better
- If adding, disable the weaker overlapping component

### 4. What's the friction cost?
Quantify across these dimensions:
- **Context window:** How many lines of CLAUDE.md instructions does it inject?
- **Agent count:** How many agent definitions are parsed per session?
- **Routing confusion:** Does it compete with another component for the same task type?
- **Hook overhead:** How many hooks fire per tool call?
- **Cognitive load:** Does the human need to remember which system does what?

### 5. Is it the thinnest implementation?
Could the same function be achieved with:
- A 20-line hookify rule instead of a plugin?
- A single agent prompt instead of 5 specialized agents?
- A bash script instead of an MCP server?
- A CLAUDE.md section instead of a skill?

The thinnest implementation that serves the loop step wins.

## Decision Matrix Template

| Component | Loop Step | Compounds? | Overlap | Friction | Thinnest? | Verdict |
|-----------|-----------|------------|---------|----------|-----------|---------|
| *name* | Plan/Work/Assess/Compound | Yes/No/Partially | *list overlaps* | Low/Med/High | Yes/No | Keep/Add/Remove/Replace |

## Scoring Guide

| Score | Meaning | Action |
|-------|---------|--------|
| Compounds + Low friction + No overlap | Strong add/keep | Install immediately |
| Compounds + Medium friction + Some overlap | Conditional | Add only if overlap component is removed |
| One-shot + Low friction + No overlap | Acceptable | Keep if already installed, low priority to add |
| One-shot + Any friction + Overlap | Overhead | Remove or don't install |
| Doesn't serve any loop step | Dead weight | Remove |

## Application History

*Record each evaluation here so future decisions reference past reasoning:*

### 2026-02-05: Full Stack Evaluation
- Evaluated: 10 plugins, 9 MCPs, compound-engineering plugin, claude-code-action
- Method: Applied CE 5-question framework for first time
- Key decisions:
  - Restructured ~/.claude/CLAUDE.md from 718→208 lines (71% reduction). Moved reference material to on-demand omc-reference.md. Created modular rules/ directory.
  - Disabled ralph-loop (strict subset of OMC ralph, zero unique value)
  - Kept superpowers, feature-dev, code-simplifier (zero per-session cost, community-maintained, useful as experimental alternatives)
  - Built compound-capture skill (Compound step) and learnings-query skill (Plan←Compound feedback)
  - Built capability registry mapping all tools to loop steps
  - Installed Context7 MCP (Plan step: framework docs)
  - Deferred: claude-code-action (set up on first active code repo), Playwright MCP (not needed now), full CE plugin (extracted core ideas instead)
- Learnings:
  - Plugin overhead is mostly zero (on-demand loading). The real token cost is CLAUDE.md, not plugins.
  - The CE philosophy matters more than the CE plugin. The compound loop can be implemented with 2 skills + a directory.
  - Boris's vanilla approach validates: Plan mode + shared CLAUDE.md + verification loops + slash commands covers 90% of needs.
  - Keeping competing tools (OMC plan vs superpowers brainstorming) is a feature, not a bug — the compound loop can track which works better over time.

## Source
- Dan Shipper & Kieran Klaassen, "Compound Engineering: How Every Codes With Agents" (Every.to, 2025-12-11)
- Will Larson, "Learning from Every's Compound Engineering" (lethain.com)
- Agentic Patterns, "Compounding Engineering Pattern"

## Tags
compound-engineering, evaluation, methodology, tools, meta-framework

---
*Generated: 2026-02-05 by claude-code*
