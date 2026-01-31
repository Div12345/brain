---
created: 2026-01-31
tags:
  - research
  - context
  - memory
  - architecture
status: active
agent: overnight
---

# Context Window Management Patterns

Strategies for managing context in long-running agent sessions.

## Core Problem

LLMs have fixed context windows. Long conversations exceed limits. Need to:
- Preserve important information
- Evict less relevant content
- Maintain coherence across sessions

## Key Patterns

### 1. Hierarchical Memory (MemGPT)
[Paper](https://arxiv.org/abs/2310.08560)

OS-inspired memory tiers:
- **Main context** (RAM) - Active conversation, within context window
- **External context** (Disk) - Archival storage, unlimited
- Agent autonomously "pages" information between tiers

For brain: session-state.md = main context, logs/ = archival

### 2. Summarization Buffer
```
ConversationSummaryBufferMemory:
- Keep last N messages verbatim
- Summarize older messages progressively
- Trigger summarization when token limit exceeded
```

Pros: Preserves recent detail + older context
Cons: Information loss, latency from summarization

### 3. Observation Masking
Hide older, less important information rather than summarize.

- Faster than summarization (no LLM call)
- Skip failed retry turns
- Window size hyperparameter needs tuning

### 4. Selective Context Injection
Only include context segments relevant to current query.

Methods:
- Keyword matching (fast, imprecise)
- Semantic similarity (embeddings)
- Learned ranking models (best quality)

### 5. Knowledge Graph Memory
Extract entities + relations from conversations.

```python
ConversationKGMemory:
- Store facts as graph
- Retrieve relevant subgraph per query
- Compress vs raw history
```

## Brain System Application

### Current Approach
- session-state.md = compaction-resilient recovery state
- logs/ = full session history
- Compaction summaries in transcripts

### Improvement Ideas

**Tiered Context:**
```
Tier 1 (Always): CLAUDE.md, session-state.md, active-agents.md
Tier 2 (Relevant): Recent commits, related research docs
Tier 3 (On-demand): Full logs, archived sessions
```

**Session Compression:**
After each session, generate:
- Key facts extracted
- Decisions made
- Patterns learned
Store in knowledge/patterns/

**Smart Retrieval:**
When starting new session:
1. Load Tier 1 context
2. Query knowledge base for relevant docs
3. Inject only what's needed

## Metrics to Track

| Metric | Description |
|--------|-------------|
| Token efficiency | Tokens used vs information retained |
| Recovery time | How fast can agent resume after compaction |
| Information loss | What important details are lost |
| Coherence | Does agent maintain consistent behavior |

## Tools & Libraries

- **LangChain** - ConversationSummaryBufferMemory
- **Mem0** - Hierarchical memory system
- **MemGPT/Letta** - OS-style memory management
- **Zep** - Graph-based memory (high token overhead)

## Anti-Patterns

1. **Unbounded history** - Context grows until failure
2. **Aggressive truncation** - Loses critical info
3. **Over-summarization** - Cumulative errors compound
4. **No eviction strategy** - Random loss at limit

## Related
- [[knowledge/research/ai-memory-systems]]
- [[knowledge/research/recursive-self-improvement]]
- [[context/session-state]]
