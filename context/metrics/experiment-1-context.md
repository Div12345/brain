# Experiment 1: Context Persistence

> Hypothesis: Context injection reduces time-to-first-useful-output (TTFUO)

## Experiment Design

| Variable | Definition |
|----------|------------|
| **Independent** | Presence of session-handoff.md injection |
| **Dependent** | Time-to-first-useful-output (TTFUO) |
| **Control** | Alternating days with/without injection |

## Success Threshold

- **TTFUO reduction**: >30% faster with injection
- **Re-explanation count**: 0 with injection
- **Friction rating**: >=4/5 with injection

---

## Session Log

| Date | Condition | TTFUO (min) | Re-explains | Friction (1-5) | Notes |
|------|-----------|-------------|-------------|----------------|-------|
| 2026-02-03 | treatment | | | | First test with injection |
| 2026-02-04 | control | | | | Baseline without injection |
| 2026-02-05 | treatment | | | | |
| 2026-02-06 | control | | | | |

---

## How to Measure

### TTFUO (Time to First Useful Output)
1. Note timestamp when session starts
2. Note timestamp when Claude produces first output you actually use
3. Difference = TTFUO

### Re-explanation Count
Tally each time you have to explain something Claude should have known from:
- session-handoff.md
- Previous context in this session
- Obvious from the codebase

### Friction Rating
At session end, rate 1-5:
- 5: Claude knew everything, felt seamless
- 4: Minor gaps but mostly smooth
- 3: Some re-explanation needed
- 2: Significant friction, had to repeat myself
- 1: Felt like starting from scratch

---

## Analysis (After 4+ Sessions)

### Treatment vs Control Comparison
| Metric | Treatment Avg | Control Avg | Difference | Significant? |
|--------|---------------|-------------|------------|--------------|
| TTFUO | | | | |
| Re-explains | | | | |
| Friction | | | | |

### Decision
- [ ] H1 supported (>30% TTFUO reduction) → Keep injection, proceed to E2
- [ ] H1 not supported → Analyze why, revise handoff content
- [ ] Inconclusive → Extend experiment

---

## Notes & Observations

(Add observations after each session)

### 2026-02-03


### 2026-02-04


