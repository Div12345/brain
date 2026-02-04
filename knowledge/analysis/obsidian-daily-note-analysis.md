# Obsidian Daily Note Pattern Analysis

**Date:** 2026-02-03
**Sample Size:** 360 daily notes (Dec 2024 - Feb 2026)
**Bead:** brain-4aq

## Key Findings

### Section Fill Rates

| Section | Fill Rate | Notes |
|---------|-----------|-------|
| Today's Focus | ~80% | Primary usage - free-form task dumps, planning |
| How I'm Feeling | ~30% | Occasional journaling when time permits |
| Wellbeing Metrics | 0% | Never filled in any sample |
| Habits checkboxes | 0% | Never checked |
| Gratitude | 0% | Never filled |
| Learnings & Insights | 0% | Never filled |
| Papers Skimmed | <5% | Rarely used |
| Tomorrow's Intent | 0% | Never filled |
| Connected Notes | 0% | Never filled |

### Actual Usage Patterns

1. **"Today's Focus" is the workhorse**
   - Used for: task lists, planning, quick notes, meeting prep
   - Free-form, unstructured dumps work best
   - Often includes nested checkboxes, links, detailed planning

2. **"How I'm Feeling" gets used when there's emotional content**
   - Journaling about conversations, relationships, mood
   - Not metrics-based, narrative-based

3. **Structured sections are ignored**
   - Numeric ratings (Sleep: _/10) - never used
   - Checkbox habits - never checked
   - Gratitude prompts - never filled
   - These represent aspirational tracking, not actual behavior

### Root Cause Analysis

The template suffers from **aspiration-reality mismatch**:
- Template designed for ideal daily practice
- Actual usage is quick capture and planning
- Friction of filling structured fields > perceived value

### Usage Archetypes

Looking at actual notes, the user has 3 modes:

1. **Planning Mode** (most common)
   - Dump tasks, decisions, follow-ups
   - Nested structure with checkboxes
   - Links to other notes/projects

2. **Reflection Mode** (occasional)
   - Process emotions, relationships
   - Narrative journaling
   - Usually after significant events

3. **Quick Capture Mode** (frequent)
   - One-liner notes
   - Names, references, reminders
   - Often just in Focus section

## Proposed Optimized Template

Based on actual behavior:

```markdown
---
date: {{date}}
tags: [type/daily]
---

# {{date}}

## Focus
<!-- What's on your mind? Tasks, plans, whatever. -->


## Notes
<!-- Capture anything: thoughts, meetings, links -->


## Reflection
<!-- Optional: How are you feeling? What happened? -->

```

### Why This Works

1. **Minimal friction** - 3 sections instead of 10
2. **Matches actual usage** - Focus + Notes + optional Reflection
3. **No guilt** - Removes never-used sections
4. **Flexible** - Each section can expand as needed

### Alternative: Two-Template System

If metrics tracking is still desired, use separate templates:

1. **Daily Capture** (daily use) - minimal as above
2. **Weekly Review** (Sunday) - metrics, gratitude, patterns

This separates quick capture from deliberate reflection.

## Implementation Recommendations

1. **Update template** at `99 - Meta/Templates/(TEMPLATE) Daily.md`
2. **Don't migrate old notes** - they work as historical record
3. **Consider Weekly Review template** for structured reflection
4. **Remove "existential dread" prompt** - appears to not serve its purpose

## Metrics That Might Work

If tracking is desired, consider:
- **Single daily rating**: "How was today? 1-5" (lower friction)
- **Weekly aggregation**: More natural reflection point
- **Habit tracking via plugin**: Dedicated tools work better than in-note checkboxes
