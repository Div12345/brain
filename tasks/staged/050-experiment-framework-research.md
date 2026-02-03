---
name: experiment-framework-research
bead_id: brain-19s
priority: 2
estimated_tokens: 20000
mode: plan-first
timeout: 30m
skill: research
model_hint: sonnet
tags: [infrastructure, research]
depends_on: []
---

# Experiment/Feedback Framework Research

## Goal
Research existing frameworks for AI agent experiments with transcript review, to inform the self-improving brain system.

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **MCP tools needed:** web_search, github search
- **Working dir:** ~/brain

## Context
The brain system needs to:
1. Run experiments (tasks with variations)
2. Capture transcripts/logs
3. Enable review of what worked/failed
4. Learn from feedback to improve future runs

## Research Questions

| Question | Why It Matters |
|----------|----------------|
| How do existing agent frameworks handle experiment tracking? | Don't reinvent the wheel |
| What transcript formats enable easy review? | Need human-readable logs |
| How is feedback incorporated into future runs? | Core of self-improvement |
| What metrics matter for agent task quality? | Need to measure improvement |

## Frameworks to Investigate
- LangSmith / LangChain tracing
- Weights & Biases for LLMs
- Braintrust
- Humanloop
- Custom approaches in agent repos (ralph, claude-flow, etc.)

## Deliverables
- `knowledge/research/experiment-frameworks.md` - Framework comparison
- `knowledge/proposals/brain-experiment-design.md` - Proposed design for brain system

## Success Criteria
- [ ] 3+ frameworks researched
- [ ] Comparison table created
- [ ] Proposed design for brain system documented
- [ ] Key patterns identified (what to adopt vs build)
