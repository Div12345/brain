---
created: 2026-01-31
tags:
  - research
  - proactive
  - anticipation
  - autonomous
status: active
agent: overnight
aliases:
  - proactive AI
  - anticipatory assistance
---

# Proactive Assistant Patterns

Research on AI systems that anticipate user needs rather than waiting for prompts.

## Core Concept

**Reactive:** Wait for command → respond
**Proactive:** Monitor context → predict need → offer help before asked

## Key Frameworks

### 1. Proactive Score (ProAgent)
[Paper](https://arxiv.org/pdf/2512.06721)

Rate predicted user need 1-5, only act when above threshold.

```
Proactive Score:
1 = No assistance needed
3 = Might be helpful
5 = User clearly needs help now
```

**For brain:** Generate morning briefing only when there's meaningful content.

### 2. Intervention Decision Framework

Before proactive action, evaluate:
1. **Relevance** - Is this related to user's current/upcoming context?
2. **Importance** - Is this urgent enough to warrant interruption?
3. **User State** - Is interruption acceptable right now?
4. **Confidence** - How certain is the prediction correct?

Only act when all criteria pass threshold.

### 3. Context-Aware Reasoning (ContextAgent)
[Paper](https://arxiv.org/html/2505.14668v1)

Extract hierarchical contexts:
- Sensory context (what's happening now)
- Persona context (user preferences, history)
- Temporal context (time of day, deadlines)

### 4. CHI 2025: Proactive Programming Assistant

Key insight: Shared workspace enables relevant suggestions.

For brain:
- Code context = repo state
- User history = past tasks
- Current work = session-state.md

## Brain Proactive Capabilities

### Tier 1: Information Preparation (Low Intrusion)
- Pre-research topics user will likely need
- Prepare briefings for upcoming meetings
- Summarize relevant news/updates

### Tier 2: Suggestions (Medium Intrusion)
- Suggest next tasks based on patterns
- Recommend files to review
- Propose questions user might want to ask

### Tier 3: Autonomous Action (High Value, High Confidence)
- Auto-commit session logs
- Generate predictions file
- Update coordination state

## Implementation: predictions.md

Each session, generate:

```markdown
## Predictions for Tomorrow

### Likely Needs
- [ ] Based on [[tasks/pending]], user will need...
- [ ] Given recent work on X, might want...

### Pre-researched
- Topic A: Key findings ready in [[knowledge/research/...]]
- Topic B: Initial notes prepared

### Suggested Questions
- Have you considered...?
- Would it help to...?
```

## Anti-Patterns

1. **Interruption fatigue** - Too many suggestions = ignored
2. **Wrong timing** - Don't suggest during focus work
3. **Low confidence actions** - Only act when sure
4. **No explanation** - Always explain why suggesting

## Related
- [[knowledge/research/recursive-self-improvement]]
- [[agents/overnight]]
- [[context/predictions]] (to be created)
