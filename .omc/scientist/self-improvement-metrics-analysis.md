# Self-Recursive Improvement Metrics for AI Task Schedulers

**Analysis Date:** 2026-02-03
**Research Stage:** 4 - Self-Improvement Feedback Loops

## Executive Summary

Self-recursive improvement requires metrics that create **closed feedback loops** where system performance data automatically drives scheduling decisions, prompt refinement, and resource allocation without human intervention. Based on recent RL-based scheduler research (2024-2026), the most effective metrics balance **immediate optimization signals** with **long-term learning signals**.

---

## Tier 1: Core Feedback Loop Enablers (Critical)

### 1. Task Success Rate by Context
**Why Enables Self-Improvement:**
- **Direct optimization signal**: Failed tasks reveal which contexts/prompts/agents need refinement
- **Automatic adaptation**: Success rate drops trigger prompt rewriting, agent reselection, or strategy changes
- **Pattern recognition**: Clustering failures by task type reveals systematic weaknesses

**Measurement:**
```
Success Rate = Completed Tasks / (Completed + Failed Tasks)
Segmented by: task_type, agent_type, time_of_day, complexity_score
```

**Feedback Loop:**
```
Low success rate (< 80%) in context X
→ Analyze failure logs
→ Regenerate prompts for context X
→ Retry with new strategy
→ Measure improvement
```

### 2. Token Efficiency (Cost per Successful Outcome)
**Why Enables Self-Improvement:**
- **Economic pressure**: Forces system to find cheaper solutions over time
- **Prompt optimization**: High token usage signals bloated prompts needing compression
- **Model selection**: Reveals when cheaper models (haiku) can replace expensive ones (opus)

**Measurement:**
```
Token Efficiency = Total Tokens Used / Successful Tasks Completed
Track: tokens_per_task, model_cost_per_task, cumulative_token_savings
```

**Feedback Loop:**
```
Token usage increases for task type Y
→ A/B test compressed vs. original prompts
→ Adopt winner based on (success_rate, token_cost) Pareto frontier
→ Update prompt templates
```

### 3. Time-to-Completion Distribution
**Why Enables Self-Improvement:**
- **Scheduling optimization**: Reveals task duration patterns for better queue management
- **Parallelization opportunities**: Long-tail tasks should run concurrently
- **Timeout tuning**: Automatically adjusts timeouts based on historical data

**Measurement:**
```
P50, P90, P99 completion times by task_type
Variance: completion_time_std_dev
Trend: completion_time_slope (improving or degrading?)
```

**Feedback Loop:**
```
P90 completion time increases for task Z
→ Identify bottleneck (agent slow? dependencies?)
→ Split task Z into parallel subtasks
→ Measure new P90
→ Adopt if faster
```

---

## Tier 2: Learning Signal Metrics (High Priority)

### 4. Retry Pattern Analysis
**Why Enables Self-Improvement:**
- **Failure mode detection**: Categorizes WHY tasks fail (timeout, error, verification failure)
- **Strategy learning**: Discovers which retry strategies work (immediate retry vs. prompt rewrite)
- **Resource allocation**: Identifies tasks needing more powerful models

**Measurement:**
```
Retry Success Rate = (Retries Succeeded) / (Total Retries)
First-Attempt Success Rate = (Succeeded First Try) / (Total Tasks)
Mean Retries to Success by Task Type
```

**Feedback Loop:**
```
Task W requires 3+ retries consistently
→ Classify failure: verification_failed, timeout, syntax_error
→ If verification_failed: strengthen acceptance criteria
→ If timeout: increase timeout OR split task
→ If syntax_error: add linting step to prompt
→ Measure retry reduction
```

### 5. Error Category Distribution
**Why Enables Self-Improvement:**
- **Root cause analysis**: Groups errors into actionable categories (syntax, logic, timeout, resource)
- **Preventive learning**: High-frequency errors trigger proactive fixes (e.g., add validation steps)
- **Prompt engineering**: Error patterns reveal missing instructions

**Measurement:**
```
Error Categories:
- syntax_error: malformed code
- logic_error: wrong behavior
- timeout: exceeded time limit
- resource_exhaustion: OOM, rate limit
- verification_failed: tests failed
- dependency_missing: import errors

Track frequency, trend, cost per category
```

**Feedback Loop:**
```
Syntax errors spike for task type V
→ Extract common syntax mistakes
→ Add linting step or syntax examples to prompt
→ Measure syntax_error rate drop
```

### 6. Agent Performance Differential
**Why Enables Self-Improvement:**
- **Model selection optimization**: Reveals which agent tier (haiku/sonnet/opus) is best per task
- **Cost/quality tradeoff**: Identifies over-provisioning (opus for simple tasks) or under-provisioning (haiku for complex)
- **Automatic routing**: Builds routing rules: "Task type X → sonnet, Task type Y → haiku"

**Measurement:**
```
Per agent: success_rate, avg_tokens, avg_time, cost_per_success
Differential: (opus_success_rate - haiku_success_rate) for same task type
```

**Feedback Loop:**
```
Haiku succeeds 95% on task type T (vs opus 96%)
→ Route T to haiku by default
→ Fallback to opus only on haiku failure
→ Track cost savings
```

---

## Tier 3: Optimization Metrics (Medium Priority)

### 7. Queue Wait Time vs. Execution Time Ratio
**Why Enables Self-Improvement:**
- **Concurrency tuning**: High wait times signal need for more parallelism
- **Priority optimization**: Identifies tasks that should jump the queue
- **Resource allocation**: Reveals CPU/memory bottlenecks

**Measurement:**
```
Wait Ratio = Queue Wait Time / Execution Time
Ideal: < 0.2 (spend 80%+ time executing, not waiting)
```

**Feedback Loop:**
```
Wait ratio > 0.5 for task category U
→ Increase max_parallel_tasks
→ OR split U into smaller subtasks
→ Measure throughput improvement
```

### 8. Dependency Graph Efficiency
**Why Enables Self-Improvement:**
- **Parallelization optimization**: Reveals unnecessary sequential dependencies
- **Critical path identification**: Focuses optimization on longest chain
- **Batching opportunities**: Groups independent tasks

**Measurement:**
```
Parallelization Factor = Total Task Time / Critical Path Time
Ideal: > 3.0 (high parallelism)
Dependency Depth: max depth of task graph
```

**Feedback Loop:**
```
Parallelization factor < 2.0
→ Analyze dependency graph
→ Identify false dependencies (tasks marked sequential but actually independent)
→ Rewrite task decomposition to remove false deps
→ Measure parallelization factor increase
```

### 9. Context Window Utilization
**Why Enables Self-Improvement:**
- **Prompt efficiency**: Detects wasted context (irrelevant files loaded)
- **Chunking strategy**: Optimizes when to split vs. consolidate context
- **Memory management**: Prevents context overflow errors

**Measurement:**
```
Context Utilization = Used Tokens / Available Context Window
Sweet spot: 60-80% (enough context, room for response)
```

**Feedback Loop:**
```
Context utilization > 90% for task S
→ Identify redundant context (duplicate files, verbose logs)
→ Implement smart context filtering
→ Measure token savings + success rate maintained
```

---

## Tier 4: Meta-Learning Metrics (Advanced)

### 10. Prompt Evolution Fitness
**Why Enables Self-Improvement:**
- **Automated prompt engineering**: Tracks which prompt mutations improve outcomes
- **A/B testing framework**: Compares prompt variants head-to-head
- **Version control for prompts**: Maintains lineage of successful prompts

**Measurement:**
```
Prompt Fitness = (success_rate × token_efficiency × speed) / cost
Track across prompt versions for same task type
```

**Feedback Loop:**
```
Prompt v2 has 10% higher fitness than v1 for task R
→ Promote v2 to default
→ Use v1 as baseline for next mutation
→ Genetic algorithm: combine best features of v1 and v2
```

### 11. Verification Accuracy
**Why Enables Self-Improvement:**
- **Quality gate optimization**: Ensures verification isn't too strict (false negatives) or too loose (false positives)
- **Test quality**: Detects when tests don't catch real bugs
- **Confidence calibration**: Aligns agent confidence with actual success

**Measurement:**
```
False Positive Rate = Tasks Passed Verification But Failed Later / Total Passed
False Negative Rate = Tasks Failed Verification But Were Correct / Total Failed
```

**Feedback Loop:**
```
High false negative rate for task Q
→ Verification too strict
→ Analyze borderline failures
→ Relax overly rigid checks
→ Measure false negative rate drop + false positive rate stable
```

### 12. Learning Curve Slope
**Why Enables Self-Improvement:**
- **Meta-metric**: Measures rate of improvement itself
- **Convergence detection**: Identifies when system has plateaued (needs new strategy)
- **ROI calculation**: Quantifies value of self-improvement investments

**Measurement:**
```
Improvement Rate = d(performance_metric)/d(time)
Performance metric = weighted_sum(success_rate, token_efficiency, speed)
```

**Feedback Loop:**
```
Learning curve flattens (slope → 0)
→ System has optimized current strategy space
→ Trigger exploration: test radical new approaches
→ If new approach shows steeper slope, adopt it
```

---

## Implementation Priority

### Phase 1 (Immediate): Core Feedback Loops
1. **Task Success Rate by Context** - Enables prompt/agent optimization
2. **Token Efficiency** - Drives cost reduction
3. **Retry Pattern Analysis** - Identifies failure modes

### Phase 2 (Week 2): Learning Signals
4. **Error Category Distribution** - Root cause analysis
5. **Agent Performance Differential** - Smart routing
6. **Time-to-Completion Distribution** - Scheduling optimization

### Phase 3 (Month 2): Optimization
7. **Queue Wait Time Ratio** - Concurrency tuning
8. **Context Window Utilization** - Memory efficiency

### Phase 4 (Advanced): Meta-Learning
9. **Prompt Evolution Fitness** - Automated prompt engineering
10. **Verification Accuracy** - Quality gate tuning
11. **Learning Curve Slope** - Meta-optimization

---

## Key Insight from RL Research

Recent research (Nature Scientific Reports, 2024-2026) shows that **multi-objective reward functions** are critical:

> "The framework employs a reward function that adapts to real-time resource utilization, task deadlines, and energy metrics, enabling robust performance in heterogeneous cloud environments."

**Application to Task Scheduler:**
```
Reward Function = w1×success_rate + w2×token_efficiency + w3×speed - w4×cost
Weights (w1-w4) adapt based on current system state:
- High failure rate → increase w1 (prioritize success over speed)
- Budget constrained → increase w2, w4 (prioritize efficiency)
- User waiting → increase w3 (prioritize speed)
```

---

## Critical Success Factor: Automatic Iteration Loop

The research shows systems achieve **27% energy reduction and 18% cost improvement** through continuous learning. Key requirement:

**Retrain Controller Pattern:**
> "MasterPlan leverages a retrain controller to monitor real-time performance, triggering a retraining process when performance metrics fall below thresholds."

**For Task Scheduler:**
```python
def should_retrain(metrics):
    return (
        metrics.success_rate < 0.80 or  # Quality degraded
        metrics.token_efficiency_trend < -0.1 or  # Costs rising
        metrics.p90_completion_time > 2 * historical_p90  # Slowdown
    )

if should_retrain(current_metrics):
    # Trigger automatic optimization cycle
    optimize_prompts()
    retune_agent_routing()
    adjust_parallelism()
```

---

## Data Requirements for Self-Improvement

To enable these feedback loops, the system needs to log:

### Task Execution Log
```json
{
  "task_id": "unique_id",
  "task_type": "executor|explore|architect|...",
  "agent_tier": "haiku|sonnet|opus",
  "prompt_version": "v2.3.1",
  "outcome": "success|failed|timeout",
  "retry_count": 3,
  "error_category": "syntax_error|logic_error|...",
  "tokens_used": 15234,
  "time_queued": 12.3,
  "time_executing": 45.2,
  "cost_usd": 0.023,
  "context_tokens": 8000,
  "verification_passed": true,
  "timestamp": "2026-02-03T08:30:00Z"
}
```

### Aggregation Rules
- **Real-time**: 1-minute windows for immediate feedback
- **Historical**: Daily rollups for trend analysis
- **Retention**: Keep raw logs 30 days, aggregates 1 year

---

## Conclusion

Self-recursive improvement requires metrics that create **closed loops** from measurement → analysis → action → measurement. The research shows systems can achieve 18-28% efficiency gains through continuous learning.

**The minimal viable feedback loop:**
1. **Measure**: Task success rate, token efficiency, retry patterns
2. **Analyze**: Cluster failures, identify high-cost task types
3. **Act**: Rewrite prompts, adjust agent routing, tune parallelism
4. **Validate**: A/B test changes, measure improvement
5. **Adopt**: Deploy winners, archive losers, iterate

**Critical insight:** The system must **automatically trigger optimization** when metrics degrade, not wait for human intervention. This is the difference between monitoring (passive) and self-improvement (active).

---

## Sources

- [Efficient deep reinforcement learning based task scheduler in multi cloud environment | Scientific Reports](https://www.nature.com/articles/s41598-024-72774-5)
- [Reinforcement learning based multi objective task scheduling for energy efficient and cost effective cloud edge computing | Scientific Reports](https://www.nature.com/articles/s41598-025-25666-1)
- [Dynamic multi objective task scheduling in cloud computing using reinforcement learning for energy and cost optimization | Scientific Reports](https://www.nature.com/articles/s41598-025-29280-z)
- [An intelligent job scheduling and real-time resource optimization for edge-cloud continuum in next generation networks | Scientific Reports](https://www.nature.com/articles/s41598-025-25452-z)
- [An efficient deep reinforcement learning based task scheduler in cloud-fog environment | Cluster Computing](https://link.springer.com/article/10.1007/s10586-024-04712-z)
- [Deep reinforcement learning task scheduling method based on server real-time performance - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11232600/)
