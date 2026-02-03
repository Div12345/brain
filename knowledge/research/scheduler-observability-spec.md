# CC-Scheduler Observability Specification

**Created:** 2026-02-03
**Status:** Ready for implementation

## Problem

The scheduler executes tasks but has no feedback mechanism to:
- Track success/failure rates
- Identify patterns in failures
- Optimize token usage
- Enable self-improvement loops

## Solution: Minimal Feedback Loop

### Data Schema (6 fields)

```jsonl
{"task_id":"X","success":true,"error_type":null,"tokens":12000,"duration_s":45,"log_file":"logs/scheduler/2026-02-03/X-abc123.md"}
```

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Task name from filename |
| `success` | boolean | Exit code == 0 |
| `error_type` | string | null, "timeout", "exit_error", "exception" |
| `tokens` | number | Estimated from output length (rough) |
| `duration_s` | number | End - start time |
| `log_file` | string | Path to full session output |

### Storage

- **History index:** `logs/scheduler/history.jsonl` (append-only)
- **Session logs:** `logs/scheduler/YYYY-MM-DD/{task}-{run_id}.md` (existing)

### Derived Metrics (computed at analysis time)

| Metric | Calculation |
|--------|-------------|
| Success rate | `sum(success) / count(*)` |
| Token efficiency | `sum(tokens) / sum(success)` |
| Failure patterns | `group by error_type` |
| Duration trends | `avg(duration_s) by task_id` |

## Implementation

### 1. Executor Changes (`executor.py`)

Add to env vars (line 127):
```python
env={
    **os.environ,
    "CLAUDE_CODE_ENTRYPOINT": "ccq-scheduler",
    "CCQ_TASK_ID": task.name,
    "CCQ_RUN_ID": run_id,
    "CCQ_LOG_FILE": log_file_path,
}
```

After execution, append to history:
```python
history_entry = {
    "task_id": task.name,
    "success": result.success,
    "error_type": classify_error(result),
    "tokens": estimate_tokens(result.output),
    "duration_s": result.duration_seconds,
    "log_file": log_file_path,
    "timestamp": result.started_at.isoformat(),
}
append_to_history(history_entry)
```

### 2. Log Utils Changes (`log_utils.py`)

Add function:
```python
def append_to_history(entry: dict) -> None:
    history_path = LOGS_DIR / "history.jsonl"
    with open(history_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

### 3. Error Classification

```python
def classify_error(result: ExecutionResult) -> Optional[str]:
    if result.success:
        return None
    if result.error and "timeout" in result.error.lower():
        return "timeout"
    if result.exit_code != 0:
        return "exit_error"
    return "exception"
```

### 4. Token Estimation (rough)

```python
def estimate_tokens(output: str) -> int:
    # Rough estimate: ~4 chars per token
    return len(output) // 4
```

## Future Enhancements (Not Now)

- Hook-based live status updates
- Agent performance tracking
- Automatic prompt optimization
- Retry with adjusted parameters

## Sources

- claude-code-scheduler JSONL history pattern
- ClaudeNightsWatch hooks.json structure
- claude-flow $TOOL_SUCCESS variables
- Existing brain research in knowledge/research/
