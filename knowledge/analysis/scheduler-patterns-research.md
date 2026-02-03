# Claude Code Task Scheduler - Patterns Research

**Research Date:** 2026-02-03
**Repos Analyzed:** ClaudeNightsWatch, claude-code-scheduler, claude-squad, claude-flow

---

## Executive Summary

Four battle-tested projects provide reusable patterns for building a Claude Code task scheduler with hooks, observability, and metrics. Key findings:

1. **Hooks** - Use Claude Code's hook system (SessionStart, SessionEnd, PostToolUse) for lightweight, silent monitoring
2. **Observability** - JSONL append-only logs for execution history + per-task log rotation
3. **Metrics** - Track execution stats (success/failure/timeout) + task timings + resource usage
4. **Scheduling** - OS-native schedulers (launchd/cron/Task Scheduler) + isolated git worktrees
5. **Memory** - Hybrid backend (SQLite + in-memory) for cross-session context

---

## 1. HOOKS PATTERN (ClaudeNightsWatch)

### Hook Configuration

**File:** `.claude-plugin/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "description": "Check daemon status on session start",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-daemon-status.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "description": "Optionally prompt to start daemon on session end",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/session-end-prompt.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "description": "Log significant file modifications for task tracking",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/log-file-changes.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Types We Should Use

| Hook | Trigger | Use Case | Example |
|------|---------|----------|---------|
| `SessionStart` | When Claude Code starts | Check if scheduler is running, show status | Verify daemon health, display pending tasks |
| `SessionEnd` | When Claude Code closes | Prompt to enable scheduler if tasks pending | "Start scheduler? 5 tasks pending" |
| `PostToolUse` | After any tool execution | Audit file modifications during task execution | Log what files were changed by scheduler |

### Hook Script Pattern (Bash)

```bash
#!/bin/bash

# Hook: Check daemon status on session start
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PID_FILE="$PLUGIN_ROOT/logs/scheduler.pid"

# Check if PID file exists and process is alive
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "✓ Scheduler running (PID: $PID)"
        exit 0
    fi
fi

# Silent if not configured
exit 0
```

**Key Principles:**
- Exit code 0 (silent success)
- Use environment variables like `${CLAUDE_PLUGIN_ROOT}`
- Store PIDs in files for quick status checks
- Run silently - don't interrupt workflow

---

## 2. OBSERVABILITY PATTERN (claude-code-scheduler)

### Logging Architecture

**Three-tier logging:**

1. **Per-task logs** - `~/.claude/logs/{task-id}.log`
2. **Execution history** - `~/.claude/execution-history.jsonl` (append-only)
3. **Activity tracking** - Project-specific logs in `.omc/logs/`

### Log Management Module

```typescript
// Append to task log with timestamp
async function appendToLog(taskId: string, message: string): Promise<void> {
  const logPath = getTaskLogPath(taskId);
  await fs.ensureDir(path.dirname(logPath));

  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;

  await fs.appendFile(logPath, logLine, 'utf-8');
}

// Rotate log if exceeds max size (10MB default)
async function rotateLogIfNeeded(
  taskId: string,
  maxSizeBytes: number = 10 * 1024 * 1024
): Promise<void> {
  const logPath = getTaskLogPath(taskId);
  const size = await getLogSize(taskId);

  if (size > maxSizeBytes) {
    const backupPath = `${logPath}.1`;
    if (await fs.pathExists(backupPath)) {
      await fs.remove(backupPath);
    }
    await fs.move(logPath, backupPath);
  }
}

// Clean up old logs after 30 days
async function cleanupOldLogs(retentionDays: number = 30): Promise<number> {
  const logsDir = getLogsDir();
  let cleaned = 0;

  const files = await fs.readdir(logsDir);
  const now = Date.now();
  const maxAge = retentionDays * 24 * 60 * 60 * 1000;

  for (const file of files) {
    const filePath = path.join(logsDir, file);
    const stats = await fs.stat(filePath);

    if (now - stats.mtime.getTime() > maxAge) {
      await fs.remove(filePath);
      cleaned++;
    }
  }

  return cleaned;
}
```

### Execution History (JSONL)

**File Format:** `~/.claude/execution-history.jsonl` (one JSON object per line)

```typescript
// Record structure
type ExecutionHistoryRecord = {
  id: string;                    // UUID
  taskId: string;
  taskName: string;
  project: string;               // Working directory
  startedAt: string;             // ISO timestamp
  completedAt?: string;          // ISO timestamp
  status: ExecutionStatus;       // 'success' | 'failure' | 'timeout' | 'skipped' | 'running'
  triggeredBy: string;           // 'cron' | 'manual' | 'file-watch'
  duration?: number;             // milliseconds
  output?: string;               // Truncated output
  error?: string;                // Error message if failed
  exitCode?: number;
  cronExpression?: string;
  worktreePath?: string;         // If using git worktree
  worktreeBranch?: string;
  worktreePushed?: boolean;
}

// Append execution record
async function recordExecution(record: ExecutionHistoryRecord): Promise<void> {
  const historyPath = getHistoryPath();
  await fs.ensureDir(path.dirname(historyPath));

  const line = JSON.stringify(record) + '\n';
  await fs.appendFile(historyPath, line, 'utf-8');
}

// Query with filters
async function getRecentExecutions(options: {
  limit?: number;
  status?: ExecutionStatus | ExecutionStatus[];
  taskName?: string;
  project?: string;
  since?: Date;
}): Promise<ExecutionHistoryRecord[]> {
  const content = await fs.readFile(historyPath, 'utf-8');
  const lines = content.trim().split('\n').filter(Boolean);

  let records: ExecutionHistoryRecord[] = [];
  for (const line of lines) {
    try {
      records.push(JSON.parse(line));
    } catch {
      continue; // Skip malformed lines
    }
  }

  // Apply filters
  if (options.status) {
    const statuses = Array.isArray(options.status)
      ? options.status
      : [options.status];
    records = records.filter(r => statuses.includes(r.status));
  }

  if (options.since) {
    records = records.filter(r =>
      new Date(r.startedAt).getTime() >= options.since!.getTime()
    );
  }

  // Sort by startedAt descending, apply limit
  records.sort((a, b) =>
    new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime()
  );

  return records.slice(0, options.limit ?? 10);
}
```

### Log Scanning (Reconstruct History from Files)

```typescript
// Scan existing log files to reconstruct execution history
async function scanExecutionLogs(options: {
  limit?: number;
  status?: 'success' | 'failure' | 'unknown';
}): Promise<ScannedExecution[]> {
  const logsDir = getLogsDir();
  const files = await fs.readdir(logsDir);
  const logFiles = new Map<string, { log?: string; error?: string }>();

  // Group files by task ID
  for (const file of files) {
    if (file.endsWith('.error.log')) {
      const taskId = file.replace('.error.log', '');
      const existing = logFiles.get(taskId) || {};
      existing.error = file;
      logFiles.set(taskId, existing);
    } else if (file.endsWith('.log')) {
      const taskId = file.replace('.log', '');
      const existing = logFiles.get(taskId) || {};
      existing.log = file;
      logFiles.set(taskId, existing);
    }
  }

  // Determine status based on error log presence/content
  const executions: ScannedExecution[] = [];
  for (const [taskId, logPaths] of logFiles.entries()) {
    if (!logPaths.log) continue;

    const logPath = path.join(logsDir, logPaths.log);
    const errorLogPath = logPaths.error ? path.join(logsDir, logPaths.error) : undefined;

    const logStats = await fs.stat(logPath);
    let status: 'success' | 'failure' | 'unknown' = 'unknown';

    if (errorLogPath && await fs.pathExists(errorLogPath)) {
      const errorContent = await fs.readFile(errorLogPath, 'utf-8');
      status = (errorContent.toLowerCase().includes('error') ||
                errorContent.includes('Exit code'))
        ? 'failure'
        : 'success';
    } else if (logStats.size > 0) {
      status = 'success';
    }

    executions.push({
      taskId,
      executedAt: logStats.mtime,
      status,
      logPath,
      errorLogPath,
      logSize: logStats.size,
    });
  }

  // Sort most recent first
  executions.sort((a, b) =>
    b.executedAt.getTime() - a.executedAt.getTime()
  );

  return executions.slice(0, options.limit ?? 20);
}
```

---

## 3. METRICS PATTERN (claude-code-scheduler)

### Execution Statistics

```typescript
// Get stats for time period
async function getExecutionStats(options: {
  since?: Date
} = {}): Promise<{
  total: number;
  success: number;
  failure: number;
  timeout: number;
  skipped: number;
  running: number;
}> {
  const records = await getRecentExecutions({
    limit: 10000, // Get all for stats
    since: options.since,
  });

  return {
    total: records.length,
    success: records.filter(r => r.status === 'success').length,
    failure: records.filter(r => r.status === 'failure').length,
    timeout: records.filter(r => r.status === 'timeout').length,
    skipped: records.filter(r => r.status === 'skipped').length,
    running: records.filter(r => r.status === 'running').length,
  };
}
```

### Time Formatting Utilities

```typescript
// Format duration: 1234ms → "1s", 65000ms → "1m 5s"
function formatDuration(ms: number | undefined): string {
  if (ms === undefined) return '-';

  if (ms < 1000) return `${ms}ms`;

  const seconds = Math.floor(ms / 1000);
  if (seconds < 60) return `${seconds}s`;

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return remainingSeconds > 0
    ? `${minutes}m ${remainingSeconds}s`
    : `${minutes}m`;
}

// Format time ago: "2 hours ago", "Yesterday 3:45 PM"
function formatTimeAgo(date: Date | string): string {
  const now = new Date();
  const then = typeof date === 'string' ? new Date(date) : date;
  const diffMs = now.getTime() - then.getTime();

  const minutes = Math.floor(diffMs / 60000);
  const hours = Math.floor(diffMs / 3600000);
  const days = Math.floor(diffMs / 86400000);

  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
  if (hours < 24) return `${hours} hour${hours === 1 ? '' : 's'} ago`;
  if (days === 1) return `Yesterday ${then.toLocaleTimeString('en-US', { ... })}`;
  if (days < 7) return `${days} day${days === 1 ? '' : 's'} ago`;

  return then.toLocaleDateString('en-US', { month: 'short', day: 'numeric', ... });
}

// Status icon for display: ✓ OK, ✗ FAIL, ⏱ TIMEOUT
function getStatusIcon(status: ExecutionStatus): string {
  const icons: Record<ExecutionStatus, string> = {
    'success': '✓ OK',
    'failure': '✗ FAIL',
    'timeout': '⏱ TIMEOUT',
    'skipped': '⊘ SKIP',
    'running': '▶ RUN',
  };
  return icons[status];
}
```

---

## 4. SCHEDULING PATTERNS (claude-code-scheduler)

### Execution Configuration Schema

```typescript
type ExecutionConfig = {
  // Claude prompt or slash command to execute
  command: string;

  // Working directory for execution
  workingDirectory?: string; // default: '.'

  // Maximum execution time in seconds
  timeout?: number; // default: 300

  // Environment variables
  env?: Record<string, string>;

  // Run with --dangerously-skip-permissions for autonomous execution
  skipPermissions?: boolean; // default: false

  // Git worktree isolation
  worktree?: {
    enabled: boolean; // default: false
    basePath?: string; // where to create worktrees
    branchPrefix?: string; // default: 'claude-task/'
    remoteName?: string; // default: 'origin'
  };
}

type ScheduledTask = {
  id: string;
  name: string;
  description?: string;
  enabled: boolean;

  trigger: {
    type: 'cron';
    expression: string; // e.g., "0 9 * * 1-5" for weekdays at 9am
    timezone?: string; // IANA timezone or 'local'
  };

  execution: ExecutionConfig;
  tags?: string[]; // for organization
  createdAt: string; // ISO timestamp
  updatedAt: string; // ISO timestamp
}
```

### Worktree Isolation Pattern

For autonomous task execution, use git worktrees to isolate changes:

```typescript
// Create isolated worktree for task
async function createTaskWorktree(
  taskId: string,
  baseDir: string,
  branchPrefix: string = 'claude-task/'
): Promise<{
  worktreePath: string;
  branch: string
}> {
  const branch = `${branchPrefix}${taskId}`;
  const worktreePath = path.join(baseDir, `.worktrees/${taskId}`);

  // Create worktree from main
  await exec(`git worktree add ${worktreePath} -b ${branch} origin/main`);

  return { worktreePath, branch };
}

// Push changes after task completion
async function pushTaskWorktree(
  worktreePath: string,
  branch: string,
  remoteName: string = 'origin'
): Promise<boolean> {
  try {
    await exec(`cd ${worktreePath} && git push ${remoteName} ${branch}`);
    return true;
  } catch {
    return false;
  }
}

// Clean up worktree
async function removeTaskWorktree(
  baseDir: string,
  taskId: string
): Promise<void> {
  const worktreePath = path.join(baseDir, `.worktrees/${taskId}`);
  await exec(`git worktree remove ${worktreePath}`);
}
```

---

## 5. WORKFLOW TRACKING PATTERN (claude-flow)

### Task Execution Tracking

```typescript
class WorkflowEngine {
  private workflows: Map<string, WorkflowExecution>;
  private eventBus: EventEmitter;

  // Execution tracking structure
  interface WorkflowExecution {
    id: string;
    state: WorkflowState;
    executionOrder: string[];                    // Order tasks executed
    taskTimings: Record<string, {                // Per-task timing
      start: number;
      end: number;
      duration: number;
    }>;
    eventLog: Array<{                            // Execution trace
      timestamp: number;
      event: string;
      data: unknown;
    }>;
    memorySnapshots: Array<{                     // State snapshots
      timestamp: number;
      snapshot: Record<string, unknown>;
    }>;
  }

  // Execute task and track timing
  async executeTask(task: ITask, agentId: string): Promise<TaskResult> {
    const startTime = Date.now();

    // Store task start in memory backend
    if (this.memoryBackend) {
      await this.memoryBackend.store({
        id: `task-start-${task.id}`,
        agentId,
        content: `Task ${task.id} started`,
        type: 'task-start',
        timestamp: Date.now(),
        metadata: { taskId: task.id, agentId }
      });
    }

    // Execute
    const result = await this.coordinator.executeTask(agentId, task);

    // Store completion
    if (this.memoryBackend) {
      await this.memoryBackend.store({
        id: `task-complete-${task.id}`,
        agentId,
        content: `Task ${task.id} ${result.status}`,
        type: 'task-complete',
        timestamp: Date.now(),
        metadata: {
          taskId: task.id,
          agentId,
          status: result.status,
          duration: Date.now() - startTime
        }
      });
    }

    return result;
  }

  // Track workflow lifecycle
  async executeWorkflow(workflow: WorkflowDefinition): Promise<WorkflowResult> {
    const execution = this.createExecution(workflow);

    // Pre-execute hook
    if (this.pluginManager) {
      await this.pluginManager.invokeExtensionPoint(
        'workflow.beforeExecute',
        workflow
      );
    }

    this.eventBus.emit('workflow:started', {
      workflowId: workflow.id,
      taskCount: workflow.tasks.length
    });

    execution.eventLog.push({
      timestamp: Date.now(),
      event: 'workflow:started',
      data: { workflowId: workflow.id }
    });

    // Execute with error handling
    try {
      const result = await this.runWorkflow(execution, workflow);

      // Post-execute hook
      if (this.pluginManager) {
        await this.pluginManager.invokeExtensionPoint(
          'workflow.afterExecute',
          result
        );
      }

      this.eventBus.emit('workflow:completed', {
        workflowId: workflow.id,
        result
      });

      return result;
    } catch (error) {
      this.eventBus.emit('workflow:failed', {
        workflowId: workflow.id,
        error
      });
      throw error;
    }
  }

  // Get metrics for completed workflow
  async getWorkflowMetrics(workflowId: string): Promise<WorkflowMetrics> {
    const execution = this.workflows.get(workflowId);
    if (!execution) throw new Error(`Workflow ${workflowId} not found`);

    const totalTasks = execution.state.tasks.length;
    const completedTasks = execution.state.completedTasks.length;
    const durations = Object.values(execution.taskTimings)
      .map(t => t.duration);
    const totalDuration = durations.reduce((a, b) => a + b, 0);
    const averageDuration = durations.length > 0
      ? totalDuration / durations.length
      : 0;

    return {
      tasksTotal: totalTasks,
      tasksCompleted: completedTasks,
      totalDuration,
      averageTaskDuration: averageDuration,
      successRate: totalTasks > 0
        ? completedTasks / totalTasks
        : 0
    };
  }

  // Debug info for troubleshooting
  async getWorkflowDebugInfo(workflowId: string): Promise<WorkflowDebugInfo> {
    const execution = this.workflows.get(workflowId);

    return {
      executionTrace: execution.executionOrder.map((taskId, index) => ({
        taskId,
        timestamp: execution.taskTimings[taskId]?.start || Date.now(),
        action: 'execute'
      })),
      taskTimings: execution.taskTimings,
      memorySnapshots: execution.memorySnapshots,
      eventLog: execution.eventLog
    };
  }
}
```

---

## 6. MEMORY BACKEND PATTERN (claude-flow)

### Hybrid Memory System

```typescript
// Memory record structure
type Memory = {
  id: string;
  agentId: string;
  content: string;
  type: string;                    // 'task-start' | 'task-complete' | etc
  timestamp: number;
  metadata?: Record<string, unknown>;
}

// Query interface
interface MemoryQuery {
  agentId?: string;
  type?: string;
  timeRange?: { start: number; end: number };
  metadata?: Record<string, unknown>;
  offset?: number;
  limit?: number;
}

// Backend interface
interface MemoryBackend {
  initialize(): Promise<void>;
  store(memory: Memory): Promise<Memory>;
  retrieve(id: string): Promise<Memory | undefined>;
  update(memory: Memory): Promise<void>;
  delete(id: string): Promise<void>;
  query(query: MemoryQuery): Promise<Memory[]>;
  vectorSearch(embedding: number[], k?: number): Promise<MemorySearchResult[]>;
  clearAgent(agentId: string): Promise<void>;
}

// SQLite implementation
class SQLiteBackend implements MemoryBackend {
  private memories: Map<string, Memory> = new Map();

  async query(query: MemoryQuery): Promise<Memory[]> {
    let results = Array.from(this.memories.values());

    if (query.agentId) {
      results = results.filter(m => m.agentId === query.agentId);
    }

    if (query.type) {
      results = results.filter(m => m.type === query.type);
    }

    if (query.timeRange) {
      results = results.filter(m =>
        m.timestamp >= query.timeRange!.start &&
        m.timestamp <= query.timeRange!.end
      );
    }

    if (query.metadata) {
      results = results.filter(m => {
        if (!m.metadata) return false;
        return Object.entries(query.metadata!).every(
          ([key, value]) => m.metadata![key] === value
        );
      });
    }

    // Sort newest first
    results.sort((a, b) => b.timestamp - a.timestamp);

    // Pagination
    if (query.offset !== undefined) {
      results = results.slice(query.offset);
    }
    if (query.limit !== undefined) {
      results = results.slice(0, query.limit);
    }

    return results;
  }
}
```

---

## 7. PRACTICAL IMPLEMENTATION GUIDE

### File Structure for Claude Code Scheduler

```
.claude-plugin/
├── hooks.json                          # Hook definitions
├── plugin.json                         # Plugin metadata
└── hooks/
    └── scripts/
        ├── check-scheduler-status.sh   # SessionStart hook
        ├── prompt-scheduler-start.sh   # SessionEnd hook
        └── log-file-changes.sh         # PostToolUse hook

.omc/
└── scheduler/
    ├── config.json                     # Task definitions (Zod-validated)
    ├── logs/
    │   ├── {task-id}.log              # Per-task logs
    │   ├── {task-id}.error.log        # Error logs
    │   └── execution-history.jsonl    # Append-only history
    └── state/
        └── metrics.json               # Aggregated stats

~/.claude/
└── logs/
    └── execution-history.jsonl        # Global history (all projects)
```

### Configuration File (Zod Schema)

```typescript
// .omc/scheduler/config.json
{
  "version": 1,
  "tasks": [
    {
      "id": "uuid-here",
      "name": "Daily lint check",
      "description": "Run linter every morning",
      "enabled": true,
      "trigger": {
        "type": "cron",
        "expression": "0 9 * * *",
        "timezone": "America/New_York"
      },
      "execution": {
        "command": "/lint-all",
        "workingDirectory": ".",
        "timeout": 600,
        "skipPermissions": false,
        "worktree": {
          "enabled": true,
          "branchPrefix": "claude-lint/"
        }
      },
      "tags": ["linting", "daily"],
      "createdAt": "2026-02-03T00:00:00Z",
      "updatedAt": "2026-02-03T00:00:00Z"
    }
  ],
  "settings": {
    "defaultTimezone": "local",
    "logRetentionDays": 30,
    "maxExecutionHistory": 100
  }
}
```

### Sample Hook Script

```bash
#!/bin/bash
# .claude-plugin/hooks/scripts/check-scheduler-status.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

CONFIG_FILE="$PROJECT_ROOT/.omc/scheduler/config.json"
HISTORY_FILE="$PROJECT_ROOT/.omc/scheduler/logs/execution-history.jsonl"

# Check if scheduler config exists
if [ ! -f "$CONFIG_FILE" ]; then
  exit 0  # Silent if not configured
fi

# Count pending/running tasks
ENABLED_TASKS=$(jq '[.tasks[] | select(.enabled == true)] | length' "$CONFIG_FILE" 2>/dev/null || echo 0)

if [ "$ENABLED_TASKS" -gt 0 ]; then
  # Check recent execution status
  if [ -f "$HISTORY_FILE" ]; then
    RECENT_STATUS=$(tail -1 "$HISTORY_FILE" | jq -r '.status' 2>/dev/null)
    if [ "$RECENT_STATUS" = "failure" ]; then
      echo "⚠️  Scheduler: Last execution failed. Check logs: $HISTORY_FILE"
    fi
  fi

  echo "✓ Scheduler: $ENABLED_TASKS task(s) active"
fi

exit 0
```

---

## 8. KEY TAKEAWAYS FOR IMPLEMENTATION

### DO

1. **Use JSONL for history** - Append-only, queryable, no schema migrations needed
2. **Log rotation** - Prevent unbounded log growth (10MB per task default)
3. **Hook into SessionStart/SessionEnd** - Lightweight status checks without UI
4. **Isolate with git worktrees** - Prevent task conflicts and enable atomic cleanup
5. **Store metadata in execution records** - taskName, project, cronExpression for context
6. **Track task timings** - `start` and `end` timestamps for metrics
7. **EventBus pattern** - Decouple components, enable plugin extensions
8. **OS-native scheduling** - Use launchd/cron/Task Scheduler, not custom loop

### DON'T

1. Don't store full logs in memory - Use files, read on-demand
2. Don't use single monolithic log file - Use per-task + history JSONL
3. Don't block hooks - Run silently, exit 0
4. Don't execute tasks in main process - Use isolated worktrees
5. Don't reinvent scheduling - Delegate to OS scheduler
6. Don't skip history cleanup - Set retention policy (default 30 days)

---

## 9. CODE SNIPPETS WE CAN REUSE

### From claude-code-scheduler

- **Log rotation module** (`src/logs/index.ts`) - Copy directly
- **History types** (`src/types.ts`) - Use ExecutionHistoryRecordSchema
- **History tracking** (`src/history/index.ts`) - All query functions
- **Formatting utilities** - `formatDuration`, `formatTimeAgo`, `getStatusIcon`

### From ClaudeNightsWatch

- **Hook configuration** - Copy hooks.json structure + hook scripts
- **Daemon status check** - PID file pattern for health checks
- **File change logging** - PostToolUse hook script pattern

### From claude-flow

- **WorkflowEngine class** - Task timing + event logging pattern
- **Memory backend interface** - SQLite + query interface
- **Plugin system** - Extension point invocation pattern

---

## 10. RECOMMENDED STACK

| Component | Technology | Source |
|-----------|-----------|--------|
| Hooks | Claude Code hooks.json | ClaudeNightsWatch |
| Logging | JSONL append-only | claude-code-scheduler |
| History | Queryable JSONL + per-task logs | claude-code-scheduler |
| Scheduling | OS native (launchd/cron) | claude-code-scheduler |
| Isolation | Git worktrees | claude-code-scheduler |
| Metrics | Event/timing tracking | claude-flow |
| Memory | SQLite + in-memory hybrid | claude-flow |
| Validation | Zod schemas | claude-code-scheduler |

---

## References

1. **ClaudeNightsWatch** - Hook patterns, daemon management
   - https://github.com/aniketkarne/ClaudeNightsWatch
   - Key files: `hooks/hooks.json`, `hooks/scripts/`

2. **claude-code-scheduler** - Logging, history, scheduling
   - https://github.com/jshchnz/claude-code-scheduler
   - Key files: `src/logs/index.ts`, `src/history/index.ts`, `src/types.ts`

3. **claude-squad** - tmux session management (future parallel execution)
   - https://github.com/smtg-ai/claude-squad

4. **claude-flow** - Workflow engine, metrics, memory backend
   - https://github.com/ruvnet/claude-flow
   - Key files: `v3/src/task-execution/`, `v3/src/memory/`
