# Scheduler Patterns - Executive Summary

**Quick Reference for Task Scheduler Implementation**

---

## Three Core Patterns to Adopt

### 1. HOOKS (Silent Monitoring)

```json
{
  "hooks": {
    "SessionStart": "Check scheduler status",
    "SessionEnd": "Prompt to enable scheduler",
    "PostToolUse": "Log file changes during task execution"
  }
}
```

**Benefits:** Zero UI friction, background observability, automatic status checks

---

### 2. JSONL HISTORY (Queryable Logs)

**File:** `~/.claude/execution-history.jsonl` (one JSON record per line)

```typescript
type ExecutionRecord = {
  id: string;              // UUID
  taskId: string;
  taskName: string;
  project: string;
  startedAt: string;       // ISO timestamp
  completedAt?: string;
  status: 'success' | 'failure' | 'timeout' | 'skipped' | 'running';
  duration?: number;       // milliseconds
  error?: string;
  cronExpression?: string;
  worktreeBranch?: string;
}
```

**Benefits:** Append-only (no corruption), queryable by status/date, no schema migrations, handles billions of records

---

### 3. PER-TASK LOGGING + ROTATION

```typescript
// Append with timestamp
await fs.appendFile(logPath, `[${timestamp}] ${message}\n`);

// Rotate when > 10MB
if (size > 10 * 1024 * 1024) {
  await fs.move(logPath, logPath + '.1');
}

// Cleanup after 30 days
await cleanupOldLogs(30);
```

**Benefits:** Bounded log files, queryable history, automatic cleanup

---

## Metrics to Track

| Metric | Location | Query |
|--------|----------|-------|
| Success rate | `execution-history.jsonl` | `status === 'success' / total` |
| Average duration | `taskTimings` | `sum(durations) / count` |
| Recent failures | `execution-history.jsonl` | `status === 'failure' && since(24h)` |
| Task execution order | `eventLog` | Replay from log |

---

## File Structure (What We Need)

```
.claude-plugin/
├── hooks.json
└── hooks/scripts/
    ├── check-scheduler-status.sh
    ├── prompt-scheduler-start.sh
    └── log-file-changes.sh

.omc/scheduler/
├── config.json              # Task definitions
└── logs/
    ├── execution-history.jsonl
    ├── {task-id}.log
    └── {task-id}.error.log

~/.claude/
└── logs/
    └── execution-history.jsonl  # Global (all projects)
```

---

## What We Can Copy Directly

| From | File | What to Copy |
|------|------|--------------|
| claude-code-scheduler | `src/logs/index.ts` | Log rotation + append functions |
| claude-code-scheduler | `src/history/index.ts` | History queries + stats |
| claude-code-scheduler | `src/types.ts` | ExecutionHistoryRecordSchema (Zod) |
| ClaudeNightsWatch | `hooks/hooks.json` | Hook structure |
| claude-flow | `WorkflowEngine.ts` | Event + timing tracking |

---

## Implementation Priorities

### Phase 1: Hooks + Logging
- [ ] hooks.json with SessionStart/SessionEnd/PostToolUse
- [ ] Append-only JSONL history
- [ ] Per-task log rotation

### Phase 2: Metrics + Queries
- [ ] Query interface (filter by status/date/project)
- [ ] Stats aggregation (success rate, avg duration)
- [ ] Formatting utilities (formatDuration, formatTimeAgo)

### Phase 3: Isolation + Safety
- [ ] Git worktree creation/cleanup
- [ ] Execution with --dangerously-skip-permissions
- [ ] Rollback on failure

### Phase 4: Memory Backend
- [ ] SQLite backend for cross-session state
- [ ] Plugin system for extensions
- [ ] Event bus for decoupling

---

## Code Patterns to Implement

**Hook Script Pattern (Bash)**
```bash
#!/bin/bash
PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG="$PLUGIN_ROOT/.omc/scheduler/config.json"

ENABLED=$(jq '[.tasks[] | select(.enabled)] | length' "$CONFIG")
echo "✓ Scheduler: $ENABLED tasks active"
exit 0
```

**Log Append Pattern (TypeScript)**
```typescript
const timestamp = new Date().toISOString();
const logLine = `[${timestamp}] ${message}\n`;
await fs.appendFile(logPath, logLine, 'utf-8');
```

**History Query Pattern (TypeScript)**
```typescript
const records = await fs.readFile(historyPath, 'utf-8')
  .then(c => c.trim().split('\n'))
  .then(lines => lines.map(l => JSON.parse(l)))
  .then(rs => rs.filter(r => r.status === 'failure' && r.since > cutoff))
  .then(rs => rs.sort((a,b) => new Date(b.startedAt) - new Date(a.startedAt)))
  .then(rs => rs.slice(0, limit));
```

---

## Testing Checklist

- [ ] Hook fires on SessionStart
- [ ] Hook fires on SessionEnd
- [ ] PostToolUse logs file changes
- [ ] Log rotation triggers at 10MB
- [ ] History query filters work
- [ ] Stats calculation is accurate
- [ ] Cleanup removes files > 30 days old
- [ ] Worktree isolation works
- [ ] Rollback on failure works

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| Hook latency | < 100ms | `time ./hook-script.sh` |
| Query time | < 500ms for 1000 records | Benchmark getRecentExecutions |
| Log growth | < 50MB/year per task | Monitor disk usage |
| Success rate visibility | Real-time | Query JSONL without restart |
| Task isolation | 100% file separation | No conflicts across worktrees |

---

## Gotchas to Avoid

1. **Don't parse JSONL in a loop** - Load once, iterate
2. **Don't forget to close/rotate logs** - Set 10MB limit
3. **Don't block on hooks** - They run during user session
4. **Don't skip cleanup** - History grows unbounded
5. **Don't store plaintext secrets** - Sanitize logs
6. **Don't use timestamps without timezone** - Use ISO 8601
7. **Don't execute tasks in main process** - Always use worktree

---

## Next Steps

1. Read full research: `/home/div/brain/knowledge/analysis/scheduler-patterns-research.md`
2. Copy log rotation code from claude-code-scheduler
3. Implement hooks.json + hook scripts
4. Add JSONL history tracking
5. Build query/stats interface
6. Add git worktree isolation
7. Wire up memory backend (later)

