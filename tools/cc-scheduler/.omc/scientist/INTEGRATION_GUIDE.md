# Priority Scoring System - Integration Guide

## Quick Start

Add the priority scoring system to CC scheduler in 3 steps:

### 1. Add scoring module to lib/

```bash
cp .omc/scientist/analysis.py lib/priority.py
```

### 2. Update lib/queue.py to use scoring

```python
# lib/queue.py
from lib.priority import PriorityScorer, PriorityLevel
from lib.capacity import check_capacity

def get_next_task(capacity_available: int):
    """Get highest-priority task that fits in capacity"""
    
    # Load all pending tasks
    tasks = load_pending_tasks()  # From lib/tasks.py
    
    # Initialize scorer with current capacity
    scorer = PriorityScorer(capacity_available=capacity_available)
    
    # Score all tasks
    scored_tasks = [(task, scorer.score(task)) for task in tasks]
    
    # Sort by score (lower = higher priority)
    scored_tasks.sort(key=lambda x: x[1])
    
    # Return highest-priority task
    if scored_tasks:
        best_task, best_score = scored_tasks[0]
        return best_task
    
    return None
```

### 3. Update ccq run command

```python
# ccq (main CLI)
def run_command(args):
    """Execute tasks from queue"""
    
    # Check capacity
    capacity_info = check_capacity()
    tokens_available = capacity_info['tokens_remaining']
    
    if args.all:
        # Run all tasks in priority order
        while True:
            task = get_next_task(tokens_available)
            if task is None:
                break
            
            result = execute_task(task)
            tokens_available -= result.tokens_used
            
            if tokens_available < 10000:  # Reserve minimum
                break
    else:
        # Run next task only
        task = get_next_task(tokens_available)
        if task:
            execute_task(task)
```

## Configuration

Add priority weights to `config.yaml`:

```yaml
# Priority scoring configuration
priority:
  # Scoring weights (sum = 210)
  weights:
    user_priority: 100      # User intent (primary signal)
    urgency: 50              # Deadline proximity
    cost_efficiency: 30      # Token cost vs capacity
    project_boost: 20        # Multi-project balancing
    dependency_penalty: 10   # Blocking dependencies
  
  # Project priorities (lower = higher priority)
  projects:
    brain: 0        # Primary
    vault: 10       # Secondary
    auditing: 20    # Tertiary
    default: 50     # Unknown projects
  
  # Cost estimation (tokens)
  default_estimates:
    research: 80000
    automation: 50000
    analysis: 120000
    quick: 10000
    writing: 30000
    bugfix: 25000
    maintenance: 40000
```

## Task Schema Updates

No changes needed! Existing schema already supports all required fields:

```yaml
---
created: 2026-02-03
priority: high              # ← Used by scorer
deadline: 2026-02-03T12:00  # ← Used for urgency
estimated_tokens: 50000     # ← Used for cost efficiency
timeout: 30m
tags: [research, weekly]
requires: []                # ← Used for dependency checking
---
```

## API Reference

### PriorityScorer Class

```python
class PriorityScorer:
    def __init__(self, capacity_available: int = 1000000):
        """
        Initialize scorer with available capacity.
        
        Args:
            capacity_available: Remaining tokens in current block
        """
    
    def score(self, task: Task) -> float:
        """
        Calculate priority score for task.
        
        Returns:
            float: Priority score (lower = higher priority)
        """
```

### Task Dataclass

```python
@dataclass
class Task:
    name: str
    created: datetime
    priority: PriorityLevel  # HIGH, MEDIUM, LOW
    timeout: int             # minutes
    deadline: Optional[datetime] = None
    estimated_tokens: int = 50000
    project: str = "brain"
    requires: List[str] = None
    tags: List[str] = None
```

### PriorityLevel Enum

```python
class PriorityLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

## Migration Path

### Phase 1: Add Without Breaking (Week 1)
- Add `lib/priority.py` module
- Keep existing FIFO queue as fallback
- Log priority scores alongside tasks
- Compare FIFO vs priority ordering

### Phase 2: Enable for Testing (Week 2)
- Add config flag: `priority.enabled: true`
- Use priority scoring when enabled
- Collect execution metrics
- Validate score predictions vs outcomes

### Phase 3: Tune Weights (Week 3)
- Analyze execution logs
- Identify deadline misses
- Adjust weights in config
- Re-test with new weights

### Phase 4: Enable Learning (Week 4)
- Add cost model updates after execution
- Track prediction errors
- Auto-adjust estimates using EMA
- Report learned models in logs

## Testing

### Unit Tests

```python
# tests/test_priority.py
import pytest
from lib.priority import PriorityScorer, Task, PriorityLevel
from datetime import datetime, timedelta

def test_high_priority_beats_low():
    scorer = PriorityScorer()
    
    high = Task("high-task", datetime.now(), PriorityLevel.HIGH, 30)
    low = Task("low-task", datetime.now(), PriorityLevel.LOW, 30)
    
    assert scorer.score(high) < scorer.score(low)

def test_urgent_deadline_boosts_priority():
    scorer = PriorityScorer()
    
    urgent = Task("urgent", datetime.now(), PriorityLevel.MEDIUM, 30,
                  deadline=datetime.now() + timedelta(hours=1))
    normal = Task("normal", datetime.now(), PriorityLevel.MEDIUM, 30,
                  deadline=datetime.now() + timedelta(days=7))
    
    assert scorer.score(urgent) < scorer.score(normal)

def test_overcapacity_task_deprioritized():
    scorer = PriorityScorer(capacity_available=100000)
    
    fits = Task("fits", datetime.now(), PriorityLevel.HIGH, 30,
                estimated_tokens=50000)
    huge = Task("huge", datetime.now(), PriorityLevel.HIGH, 30,
                estimated_tokens=200000)
    
    assert scorer.score(fits) < scorer.score(huge)
```

### Integration Test

```python
# tests/test_queue_integration.py
def test_queue_ordering():
    """Test that queue returns tasks in correct priority order"""
    
    # Create test tasks
    create_test_task("urgent-bug.md", priority="high", deadline="2h")
    create_test_task("research.md", priority="high", deadline=None)
    create_test_task("cleanup.md", priority="low", deadline=None)
    
    # Get next task
    capacity = 500000
    next_task = get_next_task(capacity)
    
    # Should return urgent-bug (high + deadline)
    assert next_task.name == "urgent-bug"
```

## Performance Considerations

### Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Score single task | O(1) | O(1) |
| Score all tasks | O(n) | O(n) |
| Sort by score | O(n log n) | O(n) |
| Get next task | O(n log n) | O(n) |

Where n = number of pending tasks.

### Optimization for Large Queues

If pending queue grows large (>100 tasks), optimize with:

```python
# Use heap for efficient top-k retrieval
import heapq

def get_top_k_tasks(k: int, capacity_available: int):
    """Get top k highest-priority tasks efficiently"""
    
    scorer = PriorityScorer(capacity_available)
    
    # Score and heap-ify
    scored = [(scorer.score(task), task) for task in load_pending_tasks()]
    heapq.heapify(scored)  # O(n)
    
    # Extract top k
    top_k = [heapq.heappop(scored) for _ in range(min(k, len(scored)))]  # O(k log n)
    
    return [task for score, task in top_k]
```

## Monitoring & Observability

### Log Priority Scores

Add to execution logs:

```yaml
---
task: zotero-digest
priority_score: 4000.0
score_breakdown:
  user_priority: 0      # high
  urgency: 2500.0       # no deadline (mid-range)
  cost_efficiency: 1500.0  # good fit
  project_boost: 0      # primary project
  dependency_penalty: 0  # no blockers
---
```

### Metrics to Track

1. **Score Prediction Accuracy**
   - Did high-priority tasks actually complete?
   - Were low-priority tasks deferred correctly?

2. **Deadline Miss Rate**
   - % of tasks with deadlines that timeout
   - Correlation with urgency factor

3. **Capacity Utilization**
   - % of capacity used per block
   - Wasted capacity from poor task selection

4. **Score Distribution**
   - Histogram of scores over 7 days
   - Outlier detection

### Dashboard Queries

```sql
-- Deadline miss rate by priority
SELECT 
  priority,
  COUNT(*) as total_tasks,
  SUM(CASE WHEN ended > deadline THEN 1 ELSE 0 END) as missed_deadlines,
  (SUM(CASE WHEN ended > deadline THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as miss_rate_pct
FROM scheduler_logs
WHERE deadline IS NOT NULL
  AND started >= datetime('now', '-7 days')
GROUP BY priority
ORDER BY miss_rate_pct DESC;

-- Average score by outcome
SELECT
  status,
  AVG(priority_score) as avg_score,
  COUNT(*) as count
FROM scheduler_logs
WHERE started >= datetime('now', '-7 days')
GROUP BY status;
```

## Troubleshooting

### Issue: High-priority tasks not running first

**Symptoms:**
- Low-priority tasks execute before high-priority
- Queue order doesn't match expected priority

**Diagnosis:**
```python
# Debug script
scorer = PriorityScorer(capacity_available=500000)
for task in load_pending_tasks():
    score = scorer.score(task)
    print(f"{task.name}: {score} (priority={task.priority})")
```

**Fixes:**
- Check if `user_priority` weight is too low (increase to 150+)
- Verify task frontmatter has correct `priority:` field
- Check for dependency penalties blocking high-priority tasks

### Issue: Deadline misses increasing

**Symptoms:**
- Tasks with deadlines timing out or completing late
- Urgency factor not strong enough

**Diagnosis:**
```sql
SELECT name, priority, deadline, ended, 
       (julianday(ended) - julianday(deadline)) * 24 as hours_late
FROM scheduler_logs
WHERE deadline IS NOT NULL
  AND ended > deadline
ORDER BY hours_late DESC
LIMIT 10;
```

**Fixes:**
- Increase `urgency` weight from 50 to 70-80
- Add slack time to deadlines (buffer 20% of estimated duration)
- Review timeout values (may be underestimated)

### Issue: Capacity thrashing

**Symptoms:**
- Starting tasks that don't complete within block
- Repeated timeouts on large tasks

**Diagnosis:**
- Check ratio of estimated_tokens to actual tokens_used
- Review cost_efficiency factor distribution

**Fixes:**
- Increase `cost_efficiency` weight from 30 to 50
- Improve token estimation (see Learning section)
- Set stricter capacity thresholds (e.g., reserve 20% buffer)

## Advanced: Weight Optimization

### A/B Testing Framework

```python
# experiments/weight_optimization.py
import json
from datetime import datetime, timedelta

def run_experiment(weights_a, weights_b, duration_days=7):
    """
    Compare two weight configurations.
    
    Metrics:
    - Deadline miss rate
    - Capacity utilization
    - Task completion rate
    """
    
    results = {
        "config_a": {"weights": weights_a, "metrics": {}},
        "config_b": {"weights": weights_b, "metrics": {}},
    }
    
    # Run both configs alternately
    start = datetime.now()
    current_config = "a"
    
    while datetime.now() - start < timedelta(days=duration_days):
        # Use config_a or config_b
        weights = weights_a if current_config == "a" else weights_b
        
        # Run scheduler with these weights
        metrics = run_scheduler_with_weights(weights)
        
        # Record metrics
        config_key = f"config_{current_config}"
        results[config_key]["metrics"] = aggregate_metrics(
            results[config_key]["metrics"], 
            metrics
        )
        
        # Alternate
        current_config = "b" if current_config == "a" else "a"
    
    # Compare results
    return analyze_experiment(results)
```

### Automated Weight Tuning

```python
def auto_tune_weights(target_metric="deadline_miss_rate", target_value=0.05):
    """
    Gradient descent on weights to minimize target metric.
    
    Args:
        target_metric: Metric to optimize (deadline_miss_rate, capacity_waste, etc.)
        target_value: Target value for metric (e.g., <5% deadline miss rate)
    """
    
    current_weights = load_weights_from_config()
    learning_rate = 5  # Weight adjustment step size
    
    for iteration in range(10):
        # Run scheduler for 24 hours with current weights
        metrics = run_scheduler_for_period(hours=24, weights=current_weights)
        
        current_value = metrics[target_metric]
        
        if current_value <= target_value:
            print(f"Target achieved: {current_value:.2%} <= {target_value:.2%}")
            break
        
        # Adjust weights based on metric
        if target_metric == "deadline_miss_rate":
            # Increase urgency weight to reduce misses
            current_weights["urgency"] += learning_rate
        elif target_metric == "capacity_waste":
            # Increase cost_efficiency to pack better
            current_weights["cost_efficiency"] += learning_rate
        
        print(f"Iteration {iteration}: {target_metric}={current_value:.2%}, adjusting weights")
    
    save_weights_to_config(current_weights)
    return current_weights
```

## Next Steps

1. **Implement basic integration** (lib/priority.py + lib/queue.py updates)
2. **Add logging** (score breakdown in execution logs)
3. **Collect baseline metrics** (run for 1 week with scoring but FIFO fallback)
4. **Enable priority scheduling** (switch from FIFO to score-based)
5. **Monitor & tune** (adjust weights based on metrics)
6. **Add learning** (auto-update cost models from actual usage)

---
*Integration guide for CC Scheduler priority scoring system*
