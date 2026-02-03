# Experiment Plan: Self-Recursive AI Assistant System

> Hypothesis-driven development with daily feedback cycles

**Principal Investigator**: User + Claude
**Start Date**: 2026-02-02
**Methodology**: Scientific method - hypothesize, test, measure, iterate

---

## Research Question

**Can a Claude-based system learn user patterns and proactively improve workflows, measured by reduced friction and increased validated output?**

---

## Experiment 1: Context Persistence

### Hypothesis H1
> If Claude has access to session handoff context at startup, then session productivity will increase because context-switching overhead is eliminated.

### Justification
- Current state: Every Claude session starts from zero
- User reported: "you're asking from the beginning each time"
- Literature: Context-switching costs 23 minutes to recover (Gloria Mark, UC Irvine)
- Expected impact: Eliminate first 5-10 minutes of re-orientation per session

### Experimental Design

| Variable | Definition |
|----------|------------|
| **Independent** | Presence/absence of context injection at session start |
| **Dependent** | Time-to-first-useful-output (TTFUO) |
| **Control** | Same user, same task types, alternating days |

### Test Protocol

**Day 1 (Control - No injection):**
1. Start fresh Claude session
2. Timestamp when session starts
3. Timestamp when first useful output delivered
4. Record: What context did you have to re-explain?

**Day 2 (Treatment - With injection):**
1. Run context injection hook before session
2. Timestamp session start
3. Timestamp first useful output
4. Record: Did Claude already know relevant context?

### Measurement

| Metric | How to Measure | Success Threshold |
|--------|----------------|-------------------|
| TTFUO | Timestamps in session log | Treatment < Control by >30% |
| Re-explanation count | Tally "I already told you" moments | Treatment = 0 |
| User friction rating | 1-5 scale at session end | Treatment >= 4 |

### Implementation (Tonight)

```
1. Create: context/session-handoff.md
   - Current focus (from vault analysis)
   - Recent decisions
   - Open questions
   - Pattern triggers

2. Create: .claude/hooks/session-start-inject.sh
   - Reads session-handoff.md
   - Injects into Claude context

3. Test tomorrow morning:
   - Does Claude know what you're working on?
   - Did you have to re-explain anything?
```

### Data Collection

File: `context/metrics/experiment-1-context.md`
```
## Session Log
| Date | Condition | TTFUO (min) | Re-explains | Friction (1-5) | Notes |
|------|-----------|-------------|-------------|----------------|-------|
| 2026-02-03 | treatment | ? | ? | ? | |
| 2026-02-04 | control | ? | ? | ? | |
```

### Decision Criteria

| Outcome | Action |
|---------|--------|
| H1 supported (>30% TTFUO reduction) | Proceed to Experiment 2, keep injection |
| H1 not supported | Analyze why - wrong context? Too much context? Revise and retest |
| Inconclusive | Extend to 5 days each condition |

---

## Experiment 2: Pattern Recognition

### Hypothesis H2
> If Claude analyzes vault history to identify recurring patterns, then it can surface relevant patterns when similar contexts arise, reducing repeated friction.

### Justification
- User has 1+ year of vault data (untapped resource)
- Recurring patterns observed: `arterial_analysis` across 18/20 notes, ML methodology questions persist
- User stated: "use my old patterns and design ways to add one additional tool or flow that will solve a problem I'm going to hit"

### Prerequisite
Experiment 1 must show context injection works (otherwise pattern surfacing has no delivery mechanism)

### Experimental Design

| Variable | Definition |
|----------|------------|
| **Independent** | Pattern scan depth (none / 30 days / 90 days) |
| **Dependent** | Pattern relevance score (user-rated) |
| **Control** | Same task types, randomized pattern presentation |

### Test Protocol

1. Run pattern extraction on vault (30-day window)
2. Store patterns in `knowledge/patterns/extracted-YYYY-MM-DD.md`
3. When user mentions topic X, surface related patterns
4. User rates: "Was this pattern relevant?" (yes/no/partially)

### Measurement

| Metric | How to Measure | Success Threshold |
|--------|----------------|-------------------|
| Pattern precision | Relevant / Total surfaced | > 60% |
| Novel insight rate | "I didn't think of that" count | > 1 per day |
| Friction prevented | "This saved me from X" count | > 0 per week |

### Implementation (Day 2-3)

```
1. Run: Vault pattern scan
   - Extract: recurring topics, unresolved tasks, time patterns
   - Store: knowledge/patterns/vault-scan-YYYY-MM-DD.md

2. Create: Pattern trigger index
   - "When user says X, surface pattern Y"
   - Store in session-handoff.md

3. Test: Does Claude surface relevant patterns?
```

### Decision Criteria

| Outcome | Action |
|---------|--------|
| H2 supported (>60% precision) | Expand pattern vocabulary, proceed to H3 |
| H2 not supported | Patterns too generic? Narrow extraction criteria |
| Partially supported | Identify which pattern types work, focus there |

---

## Experiment 3: Proactive Workflow Suggestion

### Hypothesis H3
> If Claude recognizes task type from patterns and suggests a workflow, then task completion rate will increase because structure reduces decision fatigue.

### Justification
- User wants: "help me construct workflows of any tasks I'm doing"
- PhD work is unstructured - methodology uncertainty is real
- Workflows reduce "what do I do next?" overhead

### Prerequisite
Experiments 1 & 2 must show context + patterns work

### Experimental Design

| Variable | Definition |
|----------|------------|
| **Independent** | Workflow suggestion (none / passive / proactive) |
| **Dependent** | Task completion rate, user satisfaction |
| **Control** | Same task complexity, alternating conditions |

### Test Protocol

**Condition A (None):** Claude responds but doesn't suggest workflow
**Condition B (Passive):** Claude suggests workflow only if asked
**Condition C (Proactive):** Claude suggests workflow when task type recognized

### Measurement

| Metric | How to Measure | Success Threshold |
|--------|----------------|-------------------|
| Task completion | Completed / Started | C > A by >20% |
| Workflow adoption | Times workflow followed | > 50% when offered |
| User preference | Which condition preferred? | C or B > A |

### Implementation (Day 4-7)

```
1. Create: 3 workflow templates based on vault patterns
   - Research workflow (lit review → synthesis → application)
   - Debug workflow (reproduce → isolate → fix → verify)
   - Admin workflow (batch similar tasks → execute → verify)

2. Add: Task type recognition triggers
   - "paper" / "literature" → research workflow
   - "bug" / "error" / "not working" → debug workflow
   - "need to" / "should" / admin keywords → admin workflow

3. Test: Does workflow suggestion improve completion?
```

### Decision Criteria

| Outcome | Action |
|---------|--------|
| H3 supported | Expand workflow library, add learning loop |
| H3 not supported | Workflows too rigid? Make them adaptive |
| Proactive annoying | Switch to passive (ask permission first) |

---

## Experiment 4: Self-Improvement Loop

### Hypothesis H4
> If the system tracks which suggestions/patterns/workflows were useful and adjusts accordingly, then system effectiveness will compound over time.

### Justification
- User wants: "self recursive meta system building loop"
- Gödel Agent pattern from knowledge base: system improves itself
- Without feedback, system stagnates

### Prerequisite
Experiments 1-3 establish baseline of what works

### Experimental Design

| Variable | Definition |
|----------|------------|
| **Independent** | Feedback integration (none / weekly review / real-time) |
| **Dependent** | System effectiveness over 2-week period |
| **Control** | Same user, same task distribution |

### Test Protocol

1. Every interaction, log: what was suggested, was it used, was it useful
2. Weekly: analyze logs, identify high/low performers
3. Adjust: promote high performers, demote or remove low performers
4. Measure: does week 2 outperform week 1?

### Measurement

| Metric | How to Measure | Success Threshold |
|--------|----------------|-------------------|
| Suggestion acceptance rate | Accepted / Offered | Increasing week-over-week |
| False positive rate | Unhelpful / Total | Decreasing week-over-week |
| User trust | "Claude gets me" rating (1-5) | >= 4 by week 2 |

### Implementation (Week 2+)

```
1. Create: Feedback log
   - context/metrics/suggestion-log.md
   - Format: timestamp | suggestion | accepted | useful | notes

2. Create: Weekly review ritual
   - Sunday: analyze week's logs
   - Update: pattern weights, workflow templates
   - Prune: remove patterns with <30% usefulness

3. Create: Auto-adjustment mechanism
   - High performers: surface more often
   - Low performers: require higher confidence before surfacing
```

### Decision Criteria

| Outcome | Action |
|---------|--------|
| H4 supported (improving metrics) | System is self-evolving - continue |
| H4 not supported | Feedback loop broken - diagnose where |
| Plateau | Add new signal sources (vault, git, etc.) |

---

## Tonight's Deliverable (Experiment 1 Setup)

### What We Build Now

| Item | Purpose | Time |
|------|---------|------|
| `context/session-handoff.md` | Context to inject at session start | 20 min |
| Populate with current focus, principles, triggers | Give Claude memory | 15 min |
| Create metrics template | Track experiment data | 10 min |
| Test injection manually | Verify it works | 15 min |

### Acceptance Test for Tonight

```
[ ] session-handoff.md exists with:
    [ ] Current focus (arterial_analysis status)
    [ ] Core principles (from research)
    [ ] Open questions
    [ ] Pattern triggers
[ ] Tomorrow's Claude session can read this file
[ ] You (user) can rate tomorrow: "Did Claude know my context?" (Y/N)
```

---

## Experiment Schedule

| Day | Experiment | Focus | Deliverable |
|-----|------------|-------|-------------|
| Today (2/2) | Setup | Create session-handoff.md | File exists, populated |
| Tomorrow (2/3) | E1 Test | Treatment condition | TTFUO measurement |
| Day 3 (2/4) | E1 Control | No injection baseline | TTFUO comparison |
| Day 4-5 | E2 | Pattern extraction | Pattern file + triggers |
| Day 6-7 | E2 Test | Pattern surfacing | Relevance ratings |
| Week 2 | E3 | Workflow templates | 3 workflows + testing |
| Week 3+ | E4 | Self-improvement loop | Feedback mechanism |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Experiment takes too long | Each experiment has 2-day minimum viable test |
| Metrics too complex | Start with binary (useful / not useful) |
| System over-engineered | Each experiment is independent, can stop anytime |
| User abandons logging | Make logging 10 seconds or less |
| Context injection fails | Fallback to manual paste |

---

## Success Criteria (Full System)

After 3 weeks, the system succeeds if:

1. **Context persistence works**: Claude knows what you're working on without re-explanation
2. **Patterns surface usefully**: >60% of surfaced patterns rated relevant
3. **Workflows help**: At least 1 workflow template actively used
4. **System improves**: Week 3 metrics > Week 1 metrics
5. **Low friction maintained**: Total daily overhead < 5 minutes

---

## Null Hypothesis (What Failure Looks Like)

The system fails if after 2 weeks:
- You still have to re-explain context every session
- Patterns surfaced are generic or irrelevant
- Workflows feel rigid and unhelpful
- You stop using it because it's more work than it's worth

**If null hypothesis is true**: Stop, analyze why, pivot or abandon.

---

## Next Action

Create `context/session-handoff.md` now with:
1. Current focus from vault analysis
2. Core principles from research
3. Open questions (ML methodology, arterial_analysis)
4. Pattern triggers for tomorrow

Ready to build?
