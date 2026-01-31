---
created: 2026-01-31
tags:
  - research
  - memory
  - architecture
  - autonomous
status: active
agent: overnight
aliases:
  - memory architecture
  - L0-L1-L2
  - LPM
---

# AI Agent Memory Systems

Memory is the foundation for autonomous AI systems that can evolve and personalize over time. Three-layer architecture emerging as standard.

## Memory Architecture (L0-L1-L2)

### L0: Raw Data Layer
- Direct capture from interactions
- Logs, transcripts, observations
- Unprocessed, high-volume
- **Brain equivalent:** [[logs/]]

### L1: Abstracted Knowledge
- Patterns extracted from L0
- Structured facts, preferences
- Retrieved via semantic search
- **Brain equivalent:** [[knowledge/]]

### L2: Model-Level Integration
- "Lifelong Personal Model" (LPM)
- Knowledge encoded in parameters
- Enables reasoning, not just retrieval
- **Brain equivalent:** Not yet implemented

## Memory Types

| Type | Purpose | Implementation |
|------|---------|----------------|
| **Short-term** | Session context | Context window |
| **Long-term** | Cross-session persistence | DB, vector store |
| **Episodic** | Specific past events | Event logs |
| **Semantic** | Structured facts | Knowledge graphs |

## Key Patterns

### Self-Assessment Loop
Agent evaluates own memory quality:
- Relevance scoring
- Freshness tracking
- Accuracy verification
- Auto-pruning low-value

### Autonomous Curation
- Categorize by priority
- Surface high-priority
- Archive/prune low-value
- No human intervention needed

### Continuous Learning
- Integrate new data in real-time
- Balance learning vs. forgetting
- Handle distribution shifts

## Relevance to Brain System

### Current Implementation (L0-L1)
- `knowledge/` = L1 abstractions
- `logs/` = L0 raw data
- [[context/]] = working memory
- Vector search not yet implemented

### Future Additions
- Self-assessment metrics → see [[experiments/]]
- Auto-curation rules
- Relevance scoring
- Pattern decay/refresh

### Design Principles
1. "Don't over-engineer" - keep minimal
2. "Quality not quantity" - curate actively
3. "AI as partner" - augment, don't replace thinking
4. Review weekly/monthly

## Sources
- IBM: AI Agent Memory concepts
- arXiv: LTM and self-evolution (2410.15665)
- FourWeekMBA: Automated memory management
- Personal.ai: Memory stacks architecture

## Related
- [[agents/overnight]] - Uses these patterns
- [[inspirations/claude-code-ecosystem]] - Tools context
- [[tools/orchestration/DESIGN]] - System design
