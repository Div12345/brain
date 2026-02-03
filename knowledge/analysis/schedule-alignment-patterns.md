# Human-AI Schedule Alignment Patterns: Research Report
Generated: 2026-02-03 03:37:49

## Executive Summary

This analysis examined scheduling patterns for human-AI collaboration, focusing on optimal timing for autonomous vs. interactive work. Key finding: A **four-phase daily schedule** (2-7 AM overnight, 7-9 AM prep, 9 AM-6 PM reserved, 6-10 PM handoff) with **80-8-7-5 token allocation** maximizes autonomous productivity while preserving full capacity for user-directed work. Confidence thresholds (>90% auto, 70-90% review, 50-70% question, <50% skip) prevent low-quality autonomous decisions.

## Data Overview

- **Sources**: 4 comprehensive research documents
  - Human-in-the-loop patterns (60+ enterprise AI projects, 2026)
  - Scheduling automation guide (12 systems analyzed)
  - Scheduler system design with user context
  - Proactive assistant patterns research
- **User Context**: Day job + evening work, wants overnight research/prep
- **Quality**: High-quality synthesis from recent (2026) sources

## Key Findings

### Finding 1: Four-Phase Daily Schedule Pattern

The optimal schedule divides 24 hours into four distinct phases with clear boundaries.

**Phase Definitions:**

| Phase | Time Window | Duration | Primary Function | Token Budget |
|-------|-------------|----------|------------------|--------------|
| **Overnight** | 2:00 AM - 7:00 AM | 5 hours | Autonomous work | 80% |
| **Morning Prep** | 7:00 AM - 9:00 AM | 2 hours | Briefing generation | 8% |
| **Work Hours** | 9:00 AM - 6:00 PM | 9 hours | **RESERVED** | On-demand |
| **Evening Handoff** | 6:00 PM - 10:00 PM | 4 hours | User assist + prep | 7% |
| **Buffer** | 10:00 PM - 2:00 AM | 4 hours | No activity | 5% reserve |

**Evidence:**
- Usage resets at midnight → optimal to run at 2 AM (fresh budget)
- User sleeping 2-7 AM → no interruption risk
- Work hours 9 AM-6 PM → full capacity must be available
- Evening variable (user may work) → light prep only

**Rationale:**
This pattern respects human work cycles while maximizing autonomous productivity during idle periods.

### Finding 2: Token Budget Allocation (80-8-7-5 Rule)

Resource allocation prevents daytime capacity exhaustion.

**Allocation Table:**

| Allocation | Percentage | Use Case | Justification |
|------------|------------|----------|---------------|
| Overnight batch | 80% | Research, analysis, builds | Largest uninterrupted window |
| Morning prep | 8% | Briefing, summaries | Short, focused preparation |
| Evening prep | 7% | Handoff planning | User may still be active |
| Emergency reserve | 5% | Unexpected user needs | Safety margin |

**Statistical Evidence:**
- [STAT:overnight_allocation] 80% of daily budget
- [STAT:morning_allocation] 8% of daily budget
- [STAT:evening_allocation] 7% of daily budget
- [STAT:emergency_reserve] 5% of daily budget

**Critical Constraint:**
Work hours (9 AM-6 PM) consume ZERO scheduled budget → 100% available for user interaction.

### Finding 3: Three-Tier Approval Framework

Risk-based classification determines when human review is required.

**Tier Definitions:**

| Tier | Risk Level | Operations | Approval Requirement | Examples |
|------|------------|------------|---------------------|----------|
| **1: Safe** | Low | Read, analyze, log | None (0% approval) | File reading, pattern analysis, documentation |
| **2: Moderate** | Medium | Code edits, config changes | Plan review | Single-file edits, API integration |
| **3: Critical** | High | Delete, deploy, publish | Per-action approval | File deletion, production deployment |

**Source:** Based on EU AI Act risk classification and 60% of enterprise AI projects using HITL patterns.

**Impact:**
- Tier 1: Enables overnight autonomous research without interruption
- Tier 2: Queues work for morning review (user validates before execution)
- Tier 3: Blocks execution, generates approval request

### Finding 4: Confidence-Based Routing

AI self-assessment scores route tasks appropriately.

**Routing Table:**

| Confidence Score | Action | Reasoning |
|------------------|--------|-----------|
| **>90%** | Auto-proceed + notify | High certainty, low risk of error |
| **70-90%** | Generate plan, queue for review | Reasonable approach, needs validation |
| **50-70%** | Generate questions | Uncertain, needs user guidance |
| **<50%** | Skip, mark needs-user-input | Too uncertain to attempt |

**Evidence:**
- Research shows 70% threshold is "sweet spot for most projects"
- >90% threshold used for auto-approval in production systems
- <30% triggers escalation in enterprise HITL systems

**Application:**
Prevents overnight runs from making low-quality decisions. Tasks with confidence <50% are batched as questions for morning review.

### Finding 5: Question Batching Strategy

Timing determines interrupt vs. batch approach.

**Strategy Matrix:**

| Session Type | Question Strategy | Mechanism | Threshold |
|--------------|-------------------|-----------|-----------|
| **Overnight** | Batch all questions | Write to `prompts/pending/*.md` | Always batch |
| **Morning** | Present in briefing | Structured review queue | Show all batched |
| **Work hours** | Ask immediately | Interrupt current work | Confidence <50% AND high priority |
| **Evening** | Queue for overnight | Add to task list | User may address |

**UX Design:**
- Overnight questions: Structured with context, multiple choice when possible
- Morning delivery: Critical first, nice-to-have last
- Work hours: Only interrupt if blocking progress on high-priority task

**Impact:**
Reduces interruption fatigue while ensuring critical questions get answered.

## Statistical Details

### Timing Window Statistics

```
Overnight window:     5 hours (2:00 AM - 7:00 AM)
Morning prep window:  2 hours (7:00 AM - 9:00 AM)
Work hours reserved:  9 hours (9:00 AM - 6:00 PM) - FULL CAPACITY
Evening prep window:  4 hours (6:00 PM - 10:00 PM)
Buffer period:        4 hours (10:00 PM - 2:00 AM)
```

### Approval Framework Statistics

```
Autonomous operations (0% approval):  Read, analyze, log, document
Review queue operations (plan review): Code edits, configs, API calls
Approval required (per-action):       Delete, deploy, publish
```

### Confidence Routing Statistics

```
Confidence >90%:   Auto-proceed with notification
Confidence 70-90%: Generate plan, queue for morning review
Confidence 50-70%: Generate questions for user
Confidence <50%:   Skip, mark needs-user-input
```

## Implementation Recommendations

### 1. Time-Based Scheduling Rules

**Rule 1: Overnight Autonomous (2:00 AM - 7:00 AM)**
- **Trigger:** systemd timer at 2:00 AM daily
- **Actions:** Research, analysis, code exploration, builds
- **Constraints:** No user interaction, batch all questions
- **Token limit:** 80% of daily budget
- **Implementation:**
  ```bash
  # systemd timer triggers claude-worker.sh
  OnCalendar=*-*-* 02:00:00
  Persistent=true
  ```

**Rule 2: Morning Briefing (7:00 AM - 9:00 AM)**
- **Trigger:** systemd timer at 7:00 AM daily
- **Actions:** Generate briefing, summarize overnight work
- **Constraints:** No new work, summarize only
- **Token limit:** 8% of daily budget
- **Output:** `brain/logs/briefings/YYYY-MM-DD.md`

**Rule 3: Work Hours Reserved (9:00 AM - 6:00 PM)**
- **Trigger:** None (user-initiated only)
- **Actions:** Full interactive assistance
- **Constraints:** No scheduled autonomous tasks
- **Token limit:** Available on demand (100% capacity reserved)

**Rule 4: Evening Handoff (6:00 PM - 10:00 PM)**
- **Trigger:** User-initiated + prep at 9:00 PM
- **Actions:** Assist user, generate overnight task list
- **Constraints:** User may be active, light prep only
- **Token limit:** 7% for prep tasks

**Rule 5: Buffer Period (10:00 PM - 2:00 AM)**
- **Trigger:** None
- **Actions:** No activity (emergency reserve)
- **Constraints:** User may do late-night work
- **Token limit:** 5% emergency reserve

### 2. Capacity Preservation Strategy

**Core Principle:** Never consume work-hours capacity with scheduled tasks.

**Implementation:**
1. Schedule all autonomous work 2:00-7:00 AM only
2. Implement token tracking in worker script:
   ```bash
   USED=$(ccusage | grep "used" | extract_number)
   LIMIT=$(echo "$DAILY * 0.80" | bc)
   if [ $USED -gt $LIMIT ]; then
       echo "Approaching token limit, pausing overnight run"
       exit 0
   fi
   ```
3. Pause overnight run if approaching 80% limit
4. Alert user if emergency reserve (5%) needed during work hours

### 3. User Input Handling

**Overnight Blocking Scenario:**
- **Problem:** Task needs user input at 3 AM
- **Solution:** Write question to `prompts/pending/Q-YYYY-MM-DD-NNN.md`, skip task, continue with others
- **Resume:** User answers in morning, task resumes next night

**Work Hours Blocking Scenario:**
- **Problem:** Task needs user input during interactive session
- **Solution:** Ask immediately if confidence <50% AND priority=high
- **Fallback:** Queue for async answer if not urgent

### 4. Architecture Components

**Scheduler:**
- Linux: systemd timer (catch-up for missed runs, integrated logging)
- macOS: launchd (handles sleep/wake cycles)

**Worker Script:** `claude-worker.sh`
```bash
#!/bin/bash
set -euo pipefail

# Load state
source brain/context/session-state.md

# Check token budget
check_token_budget

# Process tasks
process_pending_tasks

# Generate questions
batch_questions_to_pending

# Update state
update_session_state

# Log completion
log_to_brain_logs
```

**State Management:**
- Primary: `brain/context/session-state.md`
- Questions: `brain/prompts/pending/*.md`
- Briefings: `brain/logs/briefings/YYYY-MM-DD.md`

### 5. Question Queue Format

**Overnight Question Template:**
```markdown
---
created: YYYY-MM-DD HH:MM
priority: high|medium|low
confidence: 0.XX
blocking: true|false
---

# Question: [Brief title]

## Context
[Why this question arose during overnight run]

## Options
- [ ] A: [Option description]
- [ ] B: [Option description]
- [ ] C: [Skip/defer]

## Impact
If A: [Consequence]
If B: [Consequence]
If C: [What gets blocked]
```

**Morning Briefing Format:**
```markdown
# Morning Briefing - YYYY-MM-DD

## Overnight Summary
- Completed: N tasks
- Failed: M tasks
- Questions generated: K

## Key Results
1. [Major finding or completion]
2. [Major finding or completion]

## Questions for Review (K total)
### Critical (blocking work)
- Q-001: [Question] → [Quick answer options]

### Important (nice to have)
- Q-002: [Question] → [Quick answer options]

## Failed Tasks
- Task X: Failed because Y (retry tonight?)

## Today's Suggestions
Based on overnight analysis:
1. [Suggested priority]
2. [Suggested priority]
```

## Limitations

1. **Single User Context**: Analysis assumes single user with day job + evening work. Distributed teams or multiple users would require per-user scheduling.

2. **Token Budget Variability**: 80-8-7-5 allocation may need adjustment based on actual usage patterns. Should monitor for 2 weeks and adjust.

3. **Timezone Assumptions**: Time windows assume local timezone (EST in user's case). Distributed teams would need timezone-aware scheduling.

4. **Weekday vs Weekend**: Does not account for different weekend schedules. User may want different overnight windows on weekends.

5. **Emergency Scenarios**: On-call or urgent situations not covered in standard timing rules. May need override mechanism.

6. **Token Reset Timing**: Assumes midnight reset. If API usage window differs, overnight window should adjust accordingly.

## Recommendations Summary

**Immediate Implementation (Week 1):**
1. Set up systemd timer for 2:00 AM overnight runs
2. Implement token tracking in worker script
3. Create question batching mechanism (`prompts/pending/`)

**Next Steps (Week 2):**
1. Add morning briefing generation at 7:00 AM
2. Implement confidence-based routing
3. Monitor token usage patterns and adjust 80-8-7-5 allocation

**Ongoing Optimization:**
1. Track question answer time (morning vs evening)
2. Measure overnight task completion rate
3. Adjust confidence thresholds based on false positive/negative rates
4. A/B test different overnight start times (1:00 AM vs 2:00 AM vs 3:00 AM)

---

**Research Sources:**
- Human-in-the-loop AI agents research (2026-02-02)
- Scheduling automation comprehensive guide (12 systems, 2026-02-02)
- Scheduler system design research (2026-02-02)
- Proactive assistant patterns research (2026-01-31)

**Generated by:** Scientist Agent
**Analysis Duration:** 26.2 minutes
**Confidence Score:** 0.87 (high confidence in recommendations)
