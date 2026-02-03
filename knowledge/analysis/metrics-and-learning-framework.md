---
created: 2026-02-03
tags:
  - metrics
  - self-improvement
  - feedback-loops
  - research
status: active
---

# Metrics and Learning Framework - Comprehensive Research Summary

**Generated:** 2026-02-03
**Research Stage:** Complete knowledge synthesis
**Sources:** 5 major research files analyzed

---

## EXECUTIVE SUMMARY

Existing brain documentation covers four distinct metric categories across self-improvement, human-in-the-loop, pattern recognition, and scheduler design. This document synthesizes findings into a unified framework.

**Key Finding:** System is designed for continuous learning but **metrics implementation is incomplete** - strategic thinking exists, but operational metrics are missing.

---

## 1. SELF-IMPROVEMENT METRICS

### From: recursive-self-improvement.md

**What's Documented:**
- Gödel Agent pattern: Self-referential evaluation → propose modifications → test → adopt if improved
- Meta-prompting framework: Critique → improve prompt → test
- Voyager pattern: Attempt → fail → refine code → store in skills library

**Metrics Framework:**
```markdown
## V2: Automated Feedback Loop

context/self-improvement/
  metrics.md        # Track task success rates
  retrospectives/   # Session analyses
  experiments/      # Prompt variations being tested
```

**Currently Tracked (Proposed):**
| Metric | Type | Target |
|--------|------|--------|
| Task success rate | % | By task type |
| Prompt effectiveness | Score | Before/after variation |
| Skill adoption rate | % | Library reuse |

**Status:** ⚠️ **PROPOSED ONLY** - No implementation files found

**Missing:**
- Retrospective template implementation
- Metrics.md structure definition
- Success/failure criteria definitions
- Experiment tracking schema

---

## 2. HUMAN-IN-THE-LOOP METRICS

### From: human-in-the-loop-ai-agents-research.md

**Section: Key Metrics to Track**

### Effectiveness Metrics
| Metric | Definition | How to Measure |
|--------|-----------|-----------------|
| % of actions requiring approval | Coverage | approved_actions / total_actions |
| False positive rate | Incorrect approvals | approved_but_wrong / total_approved |
| False negative rate | Incorrect rejections | rejected_but_correct / total_rejected |
| Time to approval (median, p95) | Latency | Duration from request to decision |

### Efficiency Metrics
| Metric | Definition | How to Measure |
|--------|-----------|-----------------|
| Actions per minute (with/without HITL) | Throughput | actions / elapsed_minutes |
| Approval queue depth over time | Backlog | Pending items count |
| Timeout rate | Failures | timed_out_requests / total_requests |
| Batch approval usage | Optimization | batch_approvals / total_approvals |

### Safety Metrics
| Metric | Definition | How to Measure |
|--------|-----------|-----------------|
| Mistakes caught by approval | Prevention | caught_errors / total_errors |
| Near-misses (low confidence approved) | Risk | low_conf_approved / total_approved |
| Rollbacks performed | Recovery | rollback_count / total_actions |
| Policy violations blocked | Compliance | blocked_violations / total_violations |

**Status:** ⚠️ **FRAMEWORK DOCUMENTED** - No implementation files found

**Missing:**
- Logging schema for approval decisions
- Confidence score tracking
- Risk level classification system
- Audit trail implementation

---

## 3. PATTERN RECOGNITION METRICS

### From: pattern-recognition-research/20260202_pattern_recognition_report.md

**Success Metrics for Pattern Surfacing:**

| Metric | Target | Measurement | Why |
|--------|--------|-------------|-----|
| Pattern Relevance | >80% acceptance | User acts on surfaced pattern | Indicates useful patterns |
| Noise Reduction | <20% dismissal | User dismisses pattern | Too much noise = useless |
| Coverage | >60% interactions | % with surfaceable pattern | System utility |
| Latency | <100ms retrieval | Time pattern discovered | Real-time responsiveness |
| Privacy Compliance | 100% local | Zero external API calls | Data security |

**Technical Metrics:**
- Vector embedding quality (semantic similarity)
- Pattern confidence scores (support × user_feedback)
- Temporal decay factor (30-day half-life)
- Anti-noise filter effectiveness

**Status:** ⚠️ **FRAMEWORK PROPOSED** - No implementation found

**Missing:**
- Acceptance/dismissal tracking
- Embedding quality metrics
- Pattern confidence calculation
- Decay function testing

---

## 4. SCHEDULER & TOKEN EFFICIENCY METRICS

### From: scheduler-system-design-2026-02-02.md

**Proposed Metrics to Track:**

```
| Metric | Definition | Target |
|--------|-----------|--------|
| Task success rate | % | By task type |
| Avg tokens per task | Consumption | Within budget |
| Time to complete | Duration | <4 hours typical |
| Retry count | Resilience | <2 avg |
| Pattern improvement | Learning | +5% success/month |
```

**Components with Metrics:**
1. **Usage Monitor** - Token tracking, reset detection
2. **Task Queue** - Priority ordering, execution status
3. **Executor** - Success/failure, timing, resource usage
4. **Feedback Logger** - Structured logs with metrics
5. **Self-Improvement Loop** - Analytics on failure patterns

**Status:** 🔧 **IN DEVELOPMENT** - ccq scheduler tool exists but incomplete

**Missing:**
- Cost models (token cost per agent type)
- Session budget tracking
- Parallel execution metrics
- Token efficiency baselines

---

## 5. EXISTING IMPLEMENTATION IN /home/div/brain

### Files Already Present

**State & Tracking:**
```
.omc/state/
  ├── weekly-budget.json          ✅ Token budget tracking
  ├── session-budget.json         ✅ Per-session budget
  ├── cost-models.json            ✅ Agent cost definitions
  ├── checkpoints/                ✅ Checkpoint snapshots
  └── subagent-tracking.json      ❌ DELETED (was tracking)
```

**Logs:**
```
logs/
  └── scheduler/                  ✅ Scheduler execution logs
```

**Tasks:**
```
tasks/
  ├── pending/                    ✅ Pending work queue
  ├── completed/                  ✅ Completion archive
  └── failed/                     ✅ Failure analysis
```

**Context:**
```
context/
  ├── session-state.md            ✅ Recovery state
  ├── active-agents.md            ✅ Agent coordination
  └── (no metrics files)          ❌ MISSING
```

### Current Token Budget Implementation

From `.omc/state/weekly-budget.json`:
- Weekly total budget tracking
- Session-by-session allocation
- Model-based cost calculation
- Deductions per agent type

**Status:** ✅ **PARTIALLY IMPLEMENTED** - Budget tracking exists, but missing:
- Success/failure metrics per budget allocation
- Token efficiency analysis
- Cost-benefit analysis per task type

---

## UNIFIED METRICS FRAMEWORK

### Tier 1: Core Session Metrics (CRITICAL)

**Must Track Every Session:**

| Metric | Type | Location | Frequency |
|--------|------|----------|-----------|
| Session start timestamp | Timestamp | logs/session/ | At start |
| Tasks attempted | Count | logs/session/ | At end |
| Tasks completed | Count | logs/session/ | At end |
| Tasks failed | Count | logs/session/ | At end |
| Total tokens used | Integer | .omc/state/session-budget.json | At end |
| Errors encountered | List | logs/session/ | Continuously |
| Agent types used | List | logs/session/ | At end |

**Example Entry:**
```json
{
  "session_id": "2026-02-03T08-00-00Z",
  "start_time": "2026-02-03T08:00:00Z",
  "end_time": "2026-02-03T10:30:00Z",
  "metrics": {
    "tasks_attempted": 5,
    "tasks_completed": 4,
    "tasks_failed": 1,
    "tokens_used": 45000,
    "agents_used": ["executor-low", "architect-medium"],
    "errors": ["timeout on task-3", "insufficient_context on task-5"]
  }
}
```

### Tier 2: Task-Level Metrics (IMPORTANT)

**Track Per Task:**

| Metric | Type | Calculation |
|--------|------|-------------|
| Task ID | String | Unique identifier |
| Task type | Enum | research, code, analysis, etc. |
| Start time | Timestamp | When started |
| End time | Timestamp | When completed |
| Duration | Integer (seconds) | end - start |
| Agent type | String | Which agent executed |
| Tokens used | Integer | From agent response |
| Status | Enum | success, failed, timeout, cancelled |
| Confidence score | Float [0-1] | Agent's confidence in output |
| Retry count | Integer | Number of attempts |
| Error message | String | If failed |

### Tier 3: Agent Performance Metrics (ANALYTICAL)

**Aggregate By Agent Type:**

| Metric | Formula | Purpose |
|--------|---------|---------|
| Success rate | completed / attempted | Agent reliability |
| Avg tokens per task | total_tokens / task_count | Cost efficiency |
| Avg duration | total_duration / task_count | Speed metric |
| Error rate | errors / total_tasks | Quality signal |
| Confidence calibration | actual_success / reported_confidence | Trustworthiness |

### Tier 4: System-Level Metrics (STRATEGIC)

| Metric | Formula | Purpose |
|--------|---------|---------|
| Overall success rate | total_completed / total_attempted | System health |
| Token efficiency | tasks_completed / total_tokens | ROI |
| Cost per successful task | tokens_per_success × cost_per_token | Economics |
| Improvement trend | (current_rate - prev_rate) / prev_rate | Self-improvement signal |
| Failure pattern clusters | Group by error_type | Root cause analysis |

---

## IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Week 1-2)
**Goal:** Establish core metrics infrastructure

1. **Create metrics schema**
   - Define JSON structures for session/task/agent metrics
   - Location: `knowledge/metrics-schema.md`

2. **Implement session logging**
   - Auto-capture at session start/end
   - Location: `logs/sessions/{session_id}.json`

3. **Add task-level tracking**
   - Wrap task execution with metrics collection
   - Location: `logs/tasks/{task_id}.json`

4. **Setup cost model tracking**
   - Extend existing `cost-models.json`
   - Add success/failure cost analysis

### Phase 2: Analysis & Reporting (Week 3-4)
**Goal:** Enable pattern discovery and retrospectives

1. **Build metrics aggregator**
   - Reads all session/task logs
   - Computes Tier 3 & 4 metrics
   - Script: `tools/metrics-analyzer.py`

2. **Create retrospective template**
   - Weekly review of metrics
   - Location: `context/retrospectives/`
   - Template: What worked, what didn't, metrics-backed

3. **Implement pattern detection**
   - Identify failure clusters
   - Success factor analysis
   - Confidence calibration checks

4. **Build dashboard** (optional)
   - Simple HTML/JSON dashboard
   - Shows weekly/monthly trends
   - Location: `.omc/dashboards/metrics.html`

### Phase 3: Self-Improvement Loop (Week 5-6)
**Goal:** Close the feedback loop

1. **Implement metrics-driven optimization**
   - Identify low-performing task types
   - Suggest agent reassignment
   - Recommend prompt refinements

2. **Setup A/B testing framework**
   - Track prompt variations
   - Measure improvement
   - Location: `context/self-improvement/experiments/`

3. **Create learning documents**
   - Capture patterns to knowledge/
   - Document failure root causes
   - Track prompt improvements

4. **Enable automated adjustments**
   - Gödel Agent pattern: propose → test → adopt
   - Auto-update agent selection logic
   - Auto-refine low-performing prompts

### Phase 4: Enterprise Features (Week 7+)
**Goal:** Production-ready observability

1. **Add compliance logging**
   - Audit trail per EU AI Act
   - Location: `.omc/audit/approval-log.jsonl`

2. **Implement rollback tracking**
   - Link errors to recovery points
   - Measure rollback effectiveness

3. **Create alerting system**
   - High error rate detection
   - Budget overrun warnings
   - Performance degradation alerts

4. **Build forecasting model**
   - Predict token usage
   - Forecast completion times
   - Estimate success probability

---

## CRITICAL GAPS IN CURRENT SYSTEM

### Gap 1: No Task Success/Failure Tracking
**Impact:** Can't measure self-improvement
**Solution:** Implement Tier 1 session metrics logging
**Effort:** Low (2-3 hours)

### Gap 2: No Agent Performance Analysis
**Impact:** Can't optimize agent selection
**Solution:** Build Tier 3 aggregation scripts
**Effort:** Medium (4-6 hours)

### Gap 3: No Pattern Detection System
**Impact:** Recurring failures not identified
**Solution:** Implement pattern mining on logs
**Effort:** Medium-High (8-12 hours)

### Gap 4: No Confidence Calibration Tracking
**Impact:** Can't detect when agents are overconfident
**Solution:** Add confidence vs. actual_success comparison
**Effort:** Low-Medium (3-4 hours)

### Gap 5: No Retrospective Process
**Impact:** Learnings not documented
**Solution:** Create template + monthly review process
**Effort:** Low (2-3 hours)

---

## RECOMMENDED METRICS TO CAPTURE IMMEDIATELY

### START HERE (Next 24 Hours):

1. **Session Success Rate**
   ```json
   {
     "session_date": "2026-02-03",
     "total_tasks": 5,
     "completed_tasks": 4,
     "success_rate": 0.8
   }
   ```

2. **Task Status Tracking**
   ```json
   {
     "task_id": "task-123",
     "status": "completed|failed|timeout",
     "duration_seconds": 300,
     "tokens_used": 5000
   }
   ```

3. **Error Classification**
   ```json
   {
     "error_type": "timeout|insufficient_context|agent_error",
     "error_message": "string",
     "task_id": "task-123",
     "recovery_attempted": true|false
   }
   ```

4. **Agent Selection Impact**
   ```json
   {
     "task_type": "code_generation",
     "agent_selected": "executor-medium",
     "success": true|false,
     "confidence_score": 0.85
   }
   ```

---

## RELATIONSHIP TO EXISTING SYSTEMS

### Integration Points:

1. **Token Budget System** (.omc/state/)
   - EXTEND: Add success/failure metrics per budget
   - MEASURE: Token efficiency per outcome

2. **Task Queue System** (tasks/)
   - EXTEND: Add completion status tracking
   - MEASURE: Success rate by task type

3. **Scheduler System** (tools/cc-scheduler/)
   - EXTEND: Log execution metrics
   - MEASURE: Schedule effectiveness

4. **Self-Improvement Loop** (recursive-self-improvement.md)
   - ENABLE: With metrics feedback
   - MEASURE: Prompt improvement over time

5. **Pattern Recognition** (pattern-recognition-research/)
   - INPUT: Task success patterns
   - OUTPUT: Failure prediction

---

## SOURCES CITED

| Source | Key Contribution | Status |
|--------|-----------------|--------|
| recursive-self-improvement.md | Self-improvement framework | ✅ Researched |
| human-in-the-loop-ai-agents-research.md | HITL metrics framework | ✅ Researched |
| pattern-recognition-research/20260202_pattern_recognition_report.md | Pattern surfacing metrics | ✅ Researched |
| scheduler-system-design-2026-02-02.md | Token/task metrics | ✅ Researched |
| .omc/state/ | Existing budget tracking | ✅ Analyzed |

---

## NEXT STEPS

1. **[IMMEDIATE]** Create metrics schema doc: `knowledge/metrics-schema.md`
2. **[TODAY]** Implement session logging in tools/cc-scheduler/
3. **[THIS WEEK]** Add task-level metrics collection
4. **[NEXT WEEK]** Build metrics analyzer script
5. **[ONGOING]** Weekly retrospectives using metrics data

---

**Research Complete:** 2026-02-03
**Recommendation:** Proceed to implementation of Phase 1 metrics foundation
