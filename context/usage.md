---
created: 2026-01-31
tags:
  - context
  - usage
  - limits
  - optimization
updated: 2026-01-31T09:55
---

# Usage & Limits Tracking

> Be aware of Claude usage limits and optimize accordingly.

## Philosophy

**"Don't burn the budget on meta-work."**

Track usage to:
- Avoid hitting limits unexpectedly
- Optimize token efficiency
- Prioritize high-value operations
- Schedule heavy work appropriately

## Claude.ai Max Limits (as of Jan 2026)

| Model | Messages/Day | Context Window | Notes |
|-------|-------------|----------------|-------|
| Opus 4.5 | Limited | 200K tokens | Most capable, use for complex |
| Sonnet 4.5 | Higher | 200K tokens | Good balance |
| Haiku 4.5 | Generous | 200K tokens | Fast, use for simple |

**Note:** Limits change. Agent should search current limits if uncertain.

## Usage Optimization Strategies

| Strategy | When | Why |
|----------|------|-----|
| **Batch similar tasks** | Multiple small ops | Reduce overhead |
| **Context compaction** | Long sessions | Stay under window |
| **Model selection** | By task complexity | Match tool to job |
| **Time shifting** | Heavy analysis | Run overnight when limits reset |
| **Caching** | Repeated queries | Don't re-fetch known data |

## Session Tracking

(Agents log session usage here)

| Date | Session | Model | Est. Tokens | Task | Notes |
|------|---------|-------|-------------|------|-------|
| 2026-01-31 | setup | Opus | ~50K | Initial brain setup | - |

## Token Efficiency Tips

**Reduce input tokens:**
- Summarize context before loading
- Use targeted file reads (not entire vault)
- Reference by path, not content

**Reduce output tokens:**
- Structured formats (tables > prose)
- Incremental updates (not full rewrites)
- Append over replace

## Limit-Aware Scheduling

| Task Type | When to Run | Why |
|-----------|-------------|-----|
| **Deep analysis** | Overnight/early morning | Limits may have reset |
| **Quick queries** | Anytime | Low cost |
| **Tool building** | Dedicated session | Needs focused attention |
| **Exploration** | End of day | Use remaining budget |

## Alerts

(Agent should note when approaching limits)

| Alert | Trigger | Action |
|-------|---------|--------|
| Limit warning | 80% of estimated daily | Prioritize remaining work |
| Context warning | 150K tokens in session | Compact or summarize |
| Efficiency warning | High token:value ratio | Reconsider approach |

## Cost-Benefit Framework

Before expensive operations, ask:
1. What's the value if this works?
2. What's the token cost?
3. Is there a cheaper way?
4. Should this wait for reset?

---

*Usage awareness enables sustained operation without interruption.*
