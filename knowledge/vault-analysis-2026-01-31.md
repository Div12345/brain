# Vault Analysis - 2026-01-31

> First overnight analysis run. Analyzed 20 daily notes from 2025-12-31 to 2026-01-30.

## Executive Summary

The vault reveals a research-focused grad student working intensively on ML/biomedical research, heavily leveraging AI tools, with patterns of late-night work and unfilled self-care templates.

---

## Pattern 1: Dominant Project Focus

### arterial_analysis (Primary)
| Metric | Value |
|--------|-------|
| Mentions | 18/20 notes |
| Status | Active, prolonged |
| Core work | Feature selection, ML modelling, pycaret |

**Technical themes:**
- Stability selection framework
- Nested cross-validation methodology
- Small dataset ML (bias-variance tradeoff)
- cfpwv feature extraction
- Taiwan dataset (death outcomes, IMT, LVM-2D)

**Pattern:** Project mentioned almost daily with phrases like "wrap up", "finish", "get conclusions" - suggests desired closure but ongoing complexity.

### cardiac output estimation (Secondary)
- Mentioned ~3 times
- Collaborator: Anand
- Less active currently

---

## Pattern 2: Tool Ecosystem

| Tool | Frequency | Context |
|------|-----------|---------|
| **Claude (Desktop/Code)** | Very high | Primary coding assistant |
| **Zotero** | Medium | Literature management |
| **Obsidian** | High | Notes, daily workflow |
| **Pycaret** | High | ML experiments |
| **NotebookLM** | Low | Paper analysis |
| **Gemini CLI** | Medium | Alternative LLM, "stubborn" |
| **WandB** | Mentioned | Integration lost |

**Friction observed:**
- "gemini is too stubborn sometimes"
- "I don't like my dependency on claude this much for coding"
- WandB integration functionality lost

---

## Pattern 3: Energy & Sleep

| Signal | Evidence |
|--------|----------|
| Late night work | "slept at 7am", "worked all night", "3 hours of sleep" |
| Template avoidance | Wellbeing metrics NEVER filled |
| Energy language | "so sleepy", "drained", "eepy" |
| Recovery awareness | "good sleep helped", yoga as grounding |

**Critical finding:** The daily note template has sections for:
- Sleep/Energy/Mood/Productivity ratings (0/20 notes filled)
- Habits checkboxes (0/20 notes checked)
- Gratitude (0/20 notes filled)
- Tomorrow's Intent (0/20 notes filled)

This suggests the template structure is **aspirational but not behavioral**.

---

## Pattern 4: Task Completion

### Recurring Incomplete Tasks
| Task | Days mentioned | Status |
|------|----------------|--------|
| Credit card payment | 3+ | Unchecked, mentioned with `!!!` |
| Course registration | 5+ | Eventually resolved |
| Uber One cancellation | 1 | Unknown |

### Task Notation Patterns
- Uses `!`, `!!`, `!!!` for urgency (works well)
- Uses `[ ]` checkboxes (inconsistent checking)
- Uses `[x]` when completed (some follow-through)
- Narrative style mixing with tasks

---

## Pattern 5: Academic Context

| Detail | Value |
|--------|-------|
| Institution | University of Pittsburgh |
| Department | Bioengineering |
| Degree | Master's (track course requirements) |
| Advisor | Dr. Hahn |
| Collaborators | Anand, Taiwan research group |

**Current semester concerns:**
- Track course requirements (DSP/signals vs. alternatives)
- Ethics course registered
- Preference to focus on research over coursework

---

## Pattern 6: Meta-Work Patterns

Significant interest in:
1. Building custom AI tools/workflows
2. Knowledge base systems
3. Agent orchestration (compound engineering, recursive self-improvement)
4. Reddit/GitHub research on AI workflows

**Quotes:**
- "I want to do some more research on building more custom tools, structures etc for the agents"
- "building trusted knowledge base systems"
- "market agent set through reddit access to crawl through claude code"

---

## Pattern 7: Wellbeing Signals

### Positive
- Yoga practice (Miami retreat) was grounding
- Social connection valued ("need for supportive community")
- Beach/nature as restoration

### Concerning
- "existential dread" prompt at every note start
- Sleep deprivation patterns
- Template sections for self-care entirely unused

---

## Structural Observations

### Template Utilization

| Section | Usage Rate | Notes |
|---------|------------|-------|
| Today's Focus | ~90% | Primary use case |
| How I'm Feeling | ~30% | When emotionally relevant |
| Wellbeing Metrics | 0% | Never filled |
| Habits | 0% | Never checked |
| Gratitude | 0% | Never filled |
| Tomorrow's Intent | 0% | Never filled |
| Papers Skimmed | ~5% | Rarely used |

**Implication:** Template has too many sections. Only "Today's Focus" and occasional journaling are actual behaviors.

### Wikilink Usage
- Active: `[[arterial_analysis]]`, `[[LLM AI tools]]`, `[[Stability Selection]]`
- Cross-referencing is natural behavior

---

## Recommendations

Based on philosophy.md principles ("minimal viable structure", "match your brain", "low friction"):

### 1. Simplify Daily Template
Remove sections that are never used. Keep only:
- Today's Focus
- Notes (freeform)

### 2. Surface Recurring Stuck Tasks
`[credit card payment]` mentioned 3+ times without completion = systemic blocker. Consider:
- Hook to warn on 3+ day uncompleted tasks
- Or accept that recurring mention = reminder system that works

### 3. Research Methodology Clarity Needed
Many notes discuss nested CV, stability selection, validation approaches - suggests genuine uncertainty. Consider:
- Creating a dedicated methodology note synthesizing learnings
- Or using claude to create a decision tree for these ML decisions

### 4. Tool Dependency Awareness
Self-noted: "I don't like my dependency on claude this much for coding"
- This is self-aware friction
- Could be addressed by scheduling deliberate non-AI coding sessions

---

## Metrics

| Metric | Value |
|--------|-------|
| Daily notes analyzed | 20 |
| Date range | 2025-12-31 to 2026-01-30 |
| Primary project | arterial_analysis |
| Template fill rate | ~15% of sections |
| Recurring tasks | 3 identified |
| Friction points | 4 identified |

---

*First overnight run. Establishing baseline patterns for future comparison.*
