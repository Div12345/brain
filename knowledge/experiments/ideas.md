# Experiment Ideas Backlog

Hypothesis-driven experiments for brain system improvement.

## Format
```
## [Priority] Experiment Name
- **Hypothesis:** If X, then Y
- **Method:** How to test
- **Metrics:** What to measure
- **Status:** pending | running | done
```

---

## [HIGH] MCP Tool Latency Comparison
- **Hypothesis:** If we batch MCP calls, response time will decrease by >30%
- **Method:** Compare single vs batched calls to obsidian-mcp
- **Metrics:** Response time (ms), token usage
- **Status:** pending

## [HIGH] Task Estimation Accuracy
- **Hypothesis:** If we track actual vs estimated tokens for 10 tasks, we can improve estimates by >25%
- **Method:** Run 10 tasks, record actual capacity change, compare to estimates
- **Metrics:** Estimation error percentage
- **Status:** pending

## [MEDIUM] Overnight Schedule Optimization
- **Hypothesis:** If we adjust autonomous window based on actual wake times, utilization improves
- **Method:** Log actual briefing access times for 1 week, adjust schedule
- **Metrics:** Tasks completed per day, capacity utilization
- **Status:** pending

## [MEDIUM] Memory MCP Integration
- **Hypothesis:** If we persist learnings to memory-mcp, cross-session recall improves
- **Method:** Store 10 learnings, test recall in new sessions
- **Metrics:** Recall accuracy, retrieval time
- **Status:** pending

## [LOW] Parallel Task Execution
- **Hypothesis:** If we run independent tasks in parallel, throughput increases >50%
- **Method:** Identify parallelizable tasks, run concurrently, measure
- **Metrics:** Total time, token efficiency
- **Status:** pending

---

## Completed Experiments
<!-- Move completed experiments here with results link -->
