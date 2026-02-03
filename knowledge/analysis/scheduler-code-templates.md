# Claude Code Scheduler - Code Templates & Examples

Ready-to-use code snippets from the research.

---

## Template 1: Hook Configuration

**File:** `.claude-plugin/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "description": "Check scheduler status on session start",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-scheduler-status.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "description": "Prompt to enable scheduler if tasks pending",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/prompt-scheduler-start.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "description": "Log file modifications during task execution",
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

---

## Template 2: Hook Scripts (Bash)

### `check-scheduler-status.sh`

```bash
#!/bin/bash

# Hook: SessionStart - Check scheduler status
# Displays helpful message if scheduler running or has pending tasks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

CONFIG_FILE="$PROJECT_ROOT/.omc/scheduler/config.json"
PID_FILE="$PROJECT_ROOT/.omc/scheduler/scheduler.pid"
HISTORY_FILE="$PROJECT_ROOT/.omc/scheduler/logs/execution-history.jsonl"

# Exit silently if scheduler not configured in this project
if [ ! -f "$CONFIG_FILE" ]; then
  exit 0
fi

# Check if scheduler daemon is running
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE" 2>/dev/null)
  if kill -0 "$PID" 2>/dev/null; then
    echo "✓ Scheduler running (PID: $PID)"

    # Show count of enabled tasks
    if command -v jq &> /dev/null; then
      ENABLED_COUNT=$(jq '[.tasks[] | select(.enabled == true)] | length' "$CONFIG_FILE" 2>/dev/null || echo "?")
      echo "  $ENABLED_COUNT task(s) active"
    fi

    # Check last execution status
    if [ -f "$HISTORY_FILE" ] && command -v jq &> /dev/null; then
      LAST_STATUS=$(tail -1 "$HISTORY_FILE" 2>/dev/null | jq -r '.status' 2>/dev/null || echo "unknown")
      if [ "$LAST_STATUS" = "failure" ]; then
        echo "  ⚠️  Last execution failed"
      fi
    fi

    exit 0
  fi
fi

# Scheduler configured but not running - suggest starting
ENABLED_COUNT=$(jq '[.tasks[] | select(.enabled == true)] | length' "$CONFIG_FILE" 2>/dev/null || echo "?")
if [ "$ENABLED_COUNT" != "0" ]; then
  echo "ℹ️  Scheduler configured with $ENABLED_COUNT task(s) but not running"
  echo "  Use: scheduler start"
fi

exit 0
```

### `prompt-scheduler-start.sh`

```bash
#!/bin/bash

# Hook: SessionEnd - Prompt to start scheduler if tasks pending
# Helps user remember to enable scheduler when leaving session

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CONFIG_FILE="$PROJECT_ROOT/.omc/scheduler/config.json"

# Exit if scheduler not configured
if [ ! -f "$CONFIG_FILE" ]; then
  exit 0
fi

# Count enabled but not-running tasks
if ! command -v jq &> /dev/null; then
  exit 0
fi

ENABLED_COUNT=$(jq '[.tasks[] | select(.enabled == true)] | length' "$CONFIG_FILE" 2>/dev/null || echo "0")

if [ "$ENABLED_COUNT" -gt 0 ]; then
  echo ""
  echo "📋 Reminder: $ENABLED_COUNT scheduler task(s) configured"
  echo "   Run: scheduler start"
fi

exit 0
```

### `log-file-changes.sh`

```bash
#!/bin/bash

# Hook: PostToolUse - Log file modifications during task execution
# Tracks what files were changed (audit trail for autonomous tasks)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ACTIVITY_LOG="$PROJECT_ROOT/.omc/scheduler/logs/file-changes.log"

# Only log if we're in a scheduler execution context
# Check for environment variable set by scheduler when running tasks
if [ -z "$SCHEDULER_EXECUTION_ID" ]; then
  exit 0
fi

mkdir -p "$(dirname "$ACTIVITY_LOG")"

# Log the file operation
# $CLAUDE_TOOL_USE contains the tool name (Write, Edit, etc)
# Access via environment - this is provided by Claude Code hooks
{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $CLAUDE_TOOL_USE"
} >> "$ACTIVITY_LOG" 2>/dev/null

exit 0
```

---

## Template 3: Logging Module (TypeScript)

**File:** `lib/logging.ts`

```typescript
import * as fs from 'fs-extra';
import * as path from 'path';

interface LoggerOptions {
  logsDir: string;
  maxLogSize?: number;        // Default: 10MB
  retentionDays?: number;     // Default: 30
}

export class TaskLogger {
  private logsDir: string;
  private maxLogSize: number;
  private retentionDays: number;

  constructor(options: LoggerOptions) {
    this.logsDir = options.logsDir;
    this.maxLogSize = options.maxLogSize ?? 10 * 1024 * 1024;
    this.retentionDays = options.retentionDays ?? 30;
  }

  /**
   * Ensure logs directory exists
   */
  async ensureLogsDir(): Promise<void> {
    await fs.ensureDir(this.logsDir);
  }

  /**
   * Get path for task log file
   */
  getTaskLogPath(taskId: string): string {
    return path.join(this.logsDir, `${taskId}.log`);
  }

  /**
   * Get path for task error log file
   */
  getErrorLogPath(taskId: string): string {
    return path.join(this.logsDir, `${taskId}.error.log`);
  }

  /**
   * Append message to task log with timestamp
   */
  async append(taskId: string, message: string): Promise<void> {
    const logPath = this.getTaskLogPath(taskId);
    await fs.ensureDir(path.dirname(logPath));

    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] ${message}\n`;

    await fs.appendFile(logPath, logLine, 'utf-8');

    // Check if rotation needed
    await this.rotateIfNeeded(taskId);
  }

  /**
   * Append error message to error log
   */
  async appendError(taskId: string, error: string): Promise<void> {
    const errorPath = this.getErrorLogPath(taskId);
    await fs.ensureDir(path.dirname(errorPath));

    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] ERROR: ${error}\n`;

    await fs.appendFile(errorPath, logLine, 'utf-8');
  }

  /**
   * Read task log file
   */
  async read(taskId: string, tailLines?: number): Promise<string> {
    const logPath = this.getTaskLogPath(taskId);

    try {
      if (!(await fs.pathExists(logPath))) {
        return '';
      }

      const content = await fs.readFile(logPath, 'utf-8');

      if (tailLines && tailLines > 0) {
        const lines = content.split('\n');
        return lines.slice(-tailLines).join('\n');
      }

      return content;
    } catch (error) {
      return `Error reading log: ${error}`;
    }
  }

  /**
   * Rotate log if exceeds max size
   */
  private async rotateIfNeeded(taskId: string): Promise<void> {
    const logPath = this.getTaskLogPath(taskId);

    try {
      const stats = await fs.stat(logPath);

      if (stats.size > this.maxLogSize) {
        const backupPath = `${logPath}.1`;

        // Remove old backup if exists
        if (await fs.pathExists(backupPath)) {
          await fs.remove(backupPath);
        }

        // Move current to backup
        await fs.move(logPath, backupPath);
      }
    } catch (error) {
      // Ignore rotation errors
    }
  }

  /**
   * Clear task log
   */
  async clear(taskId: string): Promise<void> {
    const logPath = this.getTaskLogPath(taskId);
    if (await fs.pathExists(logPath)) {
      await fs.remove(logPath);
    }
  }

  /**
   * Get log file size in bytes
   */
  async getSize(taskId: string): Promise<number> {
    const logPath = this.getTaskLogPath(taskId);

    try {
      const stats = await fs.stat(logPath);
      return stats.size;
    } catch {
      return 0;
    }
  }

  /**
   * Clean up old log files
   */
  async cleanup(): Promise<number> {
    try {
      if (!(await fs.pathExists(this.logsDir))) {
        return 0;
      }

      const files = await fs.readdir(this.logsDir);
      const now = Date.now();
      const maxAge = this.retentionDays * 24 * 60 * 60 * 1000;
      let cleaned = 0;

      for (const file of files) {
        const filePath = path.join(this.logsDir, file);
        const stats = await fs.stat(filePath);

        if (now - stats.mtime.getTime() > maxAge) {
          await fs.remove(filePath);
          cleaned++;
        }
      }

      return cleaned;
    } catch (error) {
      console.error('Cleanup error:', error);
      return 0;
    }
  }
}
```

---

## Template 4: History Tracking (TypeScript)

**File:** `lib/history.ts`

```typescript
import * as fs from 'fs-extra';
import * as path from 'path';

export type ExecutionStatus = 'success' | 'failure' | 'timeout' | 'skipped' | 'running';

export interface ExecutionRecord {
  id: string;                      // UUID
  taskId: string;
  taskName: string;
  project: string;
  startedAt: string;               // ISO 8601
  completedAt?: string;            // ISO 8601
  status: ExecutionStatus;
  triggeredBy: 'cron' | 'manual' | 'file-watch';
  duration?: number;               // milliseconds
  output?: string;
  error?: string;
  exitCode?: number;
  cronExpression?: string;
  worktreePath?: string;
  worktreeBranch?: string;
  worktreePushed?: boolean;
}

export interface ExecutionQueryOptions {
  limit?: number;
  status?: ExecutionStatus | ExecutionStatus[];
  taskName?: string;
  project?: string;
  since?: Date;
}

export class ExecutionHistory {
  private historyPath: string;

  constructor(historyPath: string) {
    this.historyPath = historyPath;
  }

  /**
   * Record an execution to the history file
   */
  async record(record: ExecutionRecord): Promise<void> {
    await fs.ensureDir(path.dirname(this.historyPath));

    // Validate required fields
    if (!record.id || !record.taskId || !record.status) {
      throw new Error('Invalid execution record');
    }

    const line = JSON.stringify(record) + '\n';
    await fs.appendFile(this.historyPath, line, 'utf-8');
  }

  /**
   * Create execution record
   */
  static createRecord(
    taskId: string,
    taskName: string,
    project: string,
    triggeredBy: 'cron' | 'manual' | 'file-watch'
  ): ExecutionRecord {
    return {
      id: crypto.randomUUID(),
      taskId,
      taskName,
      project,
      startedAt: new Date().toISOString(),
      status: 'running',
      triggeredBy,
    };
  }

  /**
   * Complete an execution record
   */
  static completeRecord(
    record: ExecutionRecord,
    result: {
      status: ExecutionStatus;
      output?: string;
      error?: string;
      exitCode?: number;
    }
  ): ExecutionRecord {
    const completedAt = new Date().toISOString();
    const startTime = new Date(record.startedAt).getTime();
    const endTime = new Date(completedAt).getTime();

    return {
      ...record,
      completedAt,
      status: result.status,
      duration: endTime - startTime,
      output: result.output,
      error: result.error,
      exitCode: result.exitCode,
    };
  }

  /**
   * Get recent executions with optional filters
   */
  async getRecent(options: ExecutionQueryOptions = {}): Promise<ExecutionRecord[]> {
    if (!(await fs.pathExists(this.historyPath))) {
      return [];
    }

    const content = await fs.readFile(this.historyPath, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);

    let records: ExecutionRecord[] = [];

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

    if (options.taskName) {
      const searchTerm = options.taskName.toLowerCase();
      records = records.filter(r =>
        r.taskName.toLowerCase().includes(searchTerm)
      );
    }

    if (options.project) {
      const searchTerm = options.project.toLowerCase();
      records = records.filter(r =>
        r.project.toLowerCase().includes(searchTerm)
      );
    }

    if (options.since) {
      const sinceTime = options.since.getTime();
      records = records.filter(r =>
        new Date(r.startedAt).getTime() >= sinceTime
      );
    }

    // Sort newest first
    records.sort((a, b) =>
      new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime()
    );

    // Apply limit
    const limit = options.limit ?? 10;
    return records.slice(0, limit);
  }

  /**
   * Get execution statistics
   */
  async getStats(options: { since?: Date } = {}): Promise<{
    total: number;
    success: number;
    failure: number;
    timeout: number;
    skipped: number;
    running: number;
  }> {
    const records = await this.getRecent({
      limit: 10000,
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

  /**
   * Clean up old history entries
   */
  async cleanup(retentionDays: number = 30): Promise<number> {
    if (!(await fs.pathExists(this.historyPath))) {
      return 0;
    }

    const content = await fs.readFile(this.historyPath, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);

    const cutoffTime = Date.now() - retentionDays * 24 * 60 * 60 * 1000;
    const keptLines: string[] = [];
    let removed = 0;

    for (const line of lines) {
      try {
        const record: ExecutionRecord = JSON.parse(line);
        if (new Date(record.startedAt).getTime() >= cutoffTime) {
          keptLines.push(line);
        } else {
          removed++;
        }
      } catch {
        removed++;
      }
    }

    if (removed > 0) {
      await fs.writeFile(
        this.historyPath,
        keptLines.join('\n') + (keptLines.length > 0 ? '\n' : ''),
        'utf-8'
      );
    }

    return removed;
  }
}
```

---

## Template 5: Utility Functions (TypeScript)

**File:** `lib/format.ts`

```typescript
import * as os from 'os';

export type ExecutionStatus = 'success' | 'failure' | 'timeout' | 'skipped' | 'running';

/**
 * Format duration in milliseconds to human-readable string
 * 1234 → "1s", 65000 → "1m 5s", 3661000 → "1h 1m"
 */
export function formatDuration(ms: number | undefined): string {
  if (ms === undefined || ms === null) {
    return '-';
  }

  if (ms < 1000) {
    return `${Math.round(ms)}ms`;
  }

  const seconds = Math.floor(ms / 1000);

  if (seconds < 60) {
    return `${seconds}s`;
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  if (minutes < 60) {
    return remainingSeconds > 0
      ? `${minutes}m ${remainingSeconds}s`
      : `${minutes}m`;
  }

  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  return remainingMinutes > 0
    ? `${hours}h ${remainingMinutes}m`
    : `${hours}h`;
}

/**
 * Format date to "time ago" format
 * "just now", "2 minutes ago", "Yesterday 3:45 PM", "Feb 3, 2:30 PM"
 */
export function formatTimeAgo(date: Date | string): string {
  const now = new Date();
  const then = typeof date === 'string' ? new Date(date) : date;
  const diffMs = now.getTime() - then.getTime();

  const minutes = Math.floor(diffMs / 60000);
  const hours = Math.floor(diffMs / 3600000);
  const days = Math.floor(diffMs / 86400000);

  if (minutes < 1) {
    return 'just now';
  }

  if (minutes < 60) {
    return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
  }

  if (hours < 24) {
    return `${hours} hour${hours === 1 ? '' : 's'} ago`;
  }

  if (days === 1) {
    return `Yesterday ${then.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    })}`;
  }

  if (days < 7) {
    return `${days} day${days === 1 ? '' : 's'} ago`;
  }

  return then.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
}

/**
 * Get status icon for display
 * "✓ OK", "✗ FAIL", "⏱ TIMEOUT", "⊘ SKIP", "▶ RUN"
 */
export function getStatusIcon(status: ExecutionStatus): string {
  const icons: Record<ExecutionStatus, string> = {
    'success': '✓ OK',
    'failure': '✗ FAIL',
    'timeout': '⏱ TIMEOUT',
    'skipped': '⊘ SKIP',
    'running': '▶ RUN',
  };
  return icons[status] ?? '? UNKNOWN';
}

/**
 * Format project path for display (replace home with ~)
 */
export function formatProjectPath(projectPath: string): string {
  const home = os.homedir();
  if (projectPath.startsWith(home)) {
    return '~' + projectPath.slice(home.length);
  }
  return projectPath;
}

/**
 * Truncate string with ellipsis
 */
export function truncate(str: string, maxLength: number = 80): string {
  if (str.length <= maxLength) {
    return str;
  }
  return str.slice(0, maxLength - 3) + '...';
}
```

---

## Template 6: Task Configuration (Zod Schema)

**File:** `lib/schema.ts`

```typescript
import { z } from 'zod';

// Trigger configuration
export const CronTriggerSchema = z.object({
  type: z.literal('cron'),
  expression: z.string().min(1).describe('Cron expression (e.g., "0 9 * * 1-5")'),
  timezone: z.string().default('local').describe('IANA timezone or "local"'),
});

export type CronTrigger = z.infer<typeof CronTriggerSchema>;

// Execution configuration
export const ExecutionConfigSchema = z.object({
  command: z.string().min(1).describe('Claude prompt or /command'),
  workingDirectory: z.string().default('.'),
  timeout: z.number().positive().default(300),
  env: z.record(z.string()).optional(),
  skipPermissions: z.boolean().default(false),
  worktree: z.object({
    enabled: z.boolean().default(false),
    basePath: z.string().optional(),
    branchPrefix: z.string().default('claude-task/'),
    remoteName: z.string().default('origin'),
  }).optional(),
});

export type ExecutionConfig = z.infer<typeof ExecutionConfigSchema>;

// Scheduled task
export const ScheduledTaskSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  description: z.string().optional(),
  enabled: z.boolean().default(true),
  trigger: CronTriggerSchema,
  execution: ExecutionConfigSchema,
  tags: z.array(z.string()).default([]),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

export type ScheduledTask = z.infer<typeof ScheduledTaskSchema>;

// Schedules config file
export const SchedulesConfigSchema = z.object({
  version: z.literal(1),
  tasks: z.array(ScheduledTaskSchema),
  settings: z.object({
    defaultTimezone: z.string().default('local'),
    logRetentionDays: z.number().positive().default(30),
    maxExecutionHistory: z.number().positive().default(100),
  }).optional(),
});

export type SchedulesConfig = z.infer<typeof SchedulesConfigSchema>;

// Helpers
export function createEmptyConfig(): SchedulesConfig {
  return {
    version: 1,
    tasks: [],
    settings: {
      defaultTimezone: 'local',
      logRetentionDays: 30,
      maxExecutionHistory: 100,
    },
  };
}

export function createTask(
  name: string,
  cronExpression: string,
  command: string,
  options?: Partial<ScheduledTask>
): ScheduledTask {
  const now = new Date().toISOString();
  return {
    id: crypto.randomUUID(),
    name,
    enabled: true,
    trigger: {
      type: 'cron',
      expression: cronExpression,
      timezone: 'local',
    },
    execution: {
      command,
      workingDirectory: '.',
      timeout: 300,
      skipPermissions: false,
    },
    tags: [],
    createdAt: now,
    updatedAt: now,
    ...options,
  };
}
```

---

## Usage Examples

### Using TaskLogger

```typescript
const logger = new TaskLogger({
  logsDir: '/project/.omc/scheduler/logs',
  maxLogSize: 10 * 1024 * 1024,  // 10MB
  retentionDays: 30,
});

await logger.ensureLogsDir();
await logger.append('task-123', 'Task started');
await logger.appendError('task-123', 'Connection timeout');

const logs = await logger.read('task-123', 50);  // Last 50 lines
console.log(logs);
```

### Using ExecutionHistory

```typescript
const history = new ExecutionHistory('~/.claude/execution-history.jsonl');

// Record execution
const record = ExecutionHistory.createRecord(
  'task-123',
  'Daily Lint',
  '/home/user/project',
  'cron'
);

await history.record(record);

// Later, complete it
const completed = ExecutionHistory.completeRecord(record, {
  status: 'success',
  output: 'Linting complete',
});

await history.record(completed);

// Query
const recent = await history.getRecent({
  status: 'failure',
  since: new Date(Date.now() - 24 * 60 * 60 * 1000), // Last 24h
  limit: 10,
});

const stats = await history.getStats();
console.log(`Success rate: ${stats.success}/${stats.total}`);
```

### Using Formatting Utilities

```typescript
console.log(formatDuration(5432));     // "5s"
console.log(formatDuration(125000));   // "2m 5s"
console.log(formatTimeAgo(new Date(Date.now() - 2 * 60 * 60 * 1000))); // "2 hours ago"
console.log(getStatusIcon('success'));  // "✓ OK"
```

---

## File Checklist for Implementation

- [ ] `.claude-plugin/hooks.json` - Hook definitions
- [ ] `.claude-plugin/hooks/scripts/check-scheduler-status.sh` - SessionStart hook
- [ ] `.claude-plugin/hooks/scripts/prompt-scheduler-start.sh` - SessionEnd hook
- [ ] `.claude-plugin/hooks/scripts/log-file-changes.sh` - PostToolUse hook
- [ ] `lib/logging.ts` - TaskLogger class
- [ ] `lib/history.ts` - ExecutionHistory class
- [ ] `lib/format.ts` - Formatting utilities
- [ ] `lib/schema.ts` - Zod schemas
- [ ] `tools/cc-scheduler/lib/log_utils.py` or `.ts` - Integration point

