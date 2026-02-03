# Workflow Automation Research - Quick Reference

## TL;DR

**Best automation stack for minimal friction:**
1. Slash commands (keyword detection) - 5min setup, zero maintenance
2. File-based state (.omc/state/*.json) - git coordination
3. Multi-agent parallel (3 agents optimal) - 3.2x speedup
4. Verification-first protocol - 2-3x quality improvement

**ROI Score: 9.2/10**

## Key Numbers

| Metric | Value |
|--------|-------|
| Multi-agent speedup | 3.2x median (range: 2.1x-5.4x) |
| Verification quality boost | 2-3x improvement |
| Slash command adoption | 65% of surveyed tools |
| Setup time (full stack) | 45 minutes |
| Maintenance burden | <1 hour/month |
| Market CAGR | 45.8% (2025-2030) |

## Three Paradigms

1. **Hook-based** (Claude Code Hooks) - Event triggers, medium setup
2. **Slash commands** (oh-my-claudecode) - Keyword triggers, minimal setup
3. **Mention-based** (@claude in GitHub) - CI/CD native, low setup

**Winner:** Slash commands (65% adoption, <5min setup)

## Workflow Patterns (Standard Vocabulary)

| Pattern | Use Case | Automation Level |
|---------|----------|------------------|
| ReAct | Debugging | 85% |
| Reflection | Quality | 70% |
| Planning | Complex features | 60% |
| Multi-Agent | Parallel work | 90% |
| Tool Use | API calls | 95% |

**73% combine 2+ patterns**

## Framework Landscape

| Framework | Market Share | Best For |
|-----------|--------------|----------|
| LangChain | 42% | General purpose |
| AutoGen | 18% | Multi-agent chat |
| LlamaIndex | 15% | RAG/knowledge |
| CrewAI | 12% | Cloud automation |
| Haystack | 8% | Production pipelines |

## Boris Cherny's Workflow (Claude Creator)

- 10-15 parallel sessions daily
- Plan-first → auto-accept ("usually 1-shot it")
- Team CLAUDE.md for compound learning
- Slash commands for daily automation
- Verification-first (2-3x quality)

## MCP Task Servers

15+ production servers provide:
- Structured task + dependency management
- LLM-driven subtask expansion
- Human approval gates
- Session persistence

**Top picks:** TaskFlow MCP, Shrimp Task Manager, Kanban MCP

## Integration Priority

**Phase 1 (Week 1):**
1. Slash command detection
2. File-based state
3. CLAUDE.md knowledge repo

**Phase 2 (Week 2-3):**
4. Multi-agent parallel execution
5. Verification module
6. Task decomposition

**Phase 3 (Week 4+):**
7. GitHub Actions integration
8. Hook system
9. MCP task server

## Tools to Steal From

1. **oh-my-claudecode** - Skill system, verification protocol
2. **AutoGen** - Conversational agent API
3. **TaskFlow MCP** - Approval gates, task structure
4. **Claude Code Hooks** - Event architecture
5. **Cherny's CLAUDE.md** - Knowledge repo pattern
6. **Brain's blackboard** - File-based coordination
7. **GitHub Actions** - @mention triggers

## Sources

Full analysis with 50+ sources: `20260202_workflow_automation_analysis.md`
