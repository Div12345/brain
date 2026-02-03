# Bidirectional Claude Code ↔ Desktop Bridge Specification

## Overview

A communication bridge enabling WSL Claude Code (CLI) and Windows Claude Desktop (Electron app) to delegate tasks to each other.

## Architecture

```
+------------------+                                  +------------------+
|  Claude Desktop  |                                  |   Claude Code    |
|    (Windows)     |                                  |     (WSL2)       |
+------------------+                                  +------------------+
         |                                                     |
         |  [Desktop-to-Code: File Queue]                      |
         |  ========================================>          |
         |  writes to C:\Users\din18\.claude-bridge\queue\     |
         |                                                     |
         |  [Code-to-Desktop: DevTools MCP]                    |
         |  <========================================          |
         |  existing server.py via CDP port 9222               |
         |                                                     |
+--------+---------+                                  +--------+---------+
         |                                                     |
         v                                                     v
+------------------+                                  +------------------+
| C:\Users\din18\  |  <-------- Shared Path --------> | /mnt/c/Users/    |
| .claude-bridge\  |      (NTFS via Plan9/9p)         | din18/.claude-   |
|                  |                                  | bridge/          |
+------------------+                                  +------------------+
```

## Queue Directory Structure

```
/mnt/c/Users/din18/.claude-bridge/
├── config.json           # Bridge configuration
├── queue/                # Incoming tasks (Desktop writes)
├── processing/           # Tasks being processed (Code claims)
├── responses/            # Completed task responses
├── dead-letter/          # Failed/expired tasks
├── archive/              # Completed tasks (debugging)
└── logs/                 # Operation logs
```

## Task Schema

```json
{
  "id": "uuid-v4",
  "type": "message|command|query|delegate",
  "payload": {
    "message": "string",
    "context": "optional string"
  },
  "source": {
    "agent": "desktop|code",
    "conversation_id": "optional",
    "session_id": "optional"
  },
  "created_at": "ISO8601",
  "ttl_seconds": 300,
  "priority": 5,
  "delegation_chain": [],
  "response_required": true
}
```

## Response Schema

```json
{
  "task_id": "uuid",
  "status": "success|error|timeout|rejected",
  "result": {},
  "error": {"code": "", "message": "", "details": {}},
  "completed_at": "ISO8601",
  "processing_ms": 0
}
```

## Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Queue format | JSON files | Human-readable, debuggable |
| Watcher | Python watchdog | Battle-tested, inotify |
| Schema validation | Pydantic v2 | Type-safe, fast |
| Atomic writes | .tmp + rename | POSIX-guaranteed |
| Task IDs | UUIDv4 | Collision-free |

## File Structure

```
claude-desktop-mcp/
├── server.py              # Existing MCP (Code→Desktop)
├── pyproject.toml
├── bridge/
│   ├── __init__.py
│   ├── schema.py          # Pydantic models
│   ├── watcher.py         # File watcher
│   ├── processor.py       # Task dispatcher
│   └── config.py          # Configuration
└── scripts/
    └── watch_queue.py     # Entry point
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| queue_path | /mnt/c/Users/din18/.claude-bridge/ | Base path |
| poll_interval_ms | 500 | Watcher interval |
| default_ttl_seconds | 300 | Task TTL (5 min) |
| max_concurrent_tasks | 5 | Parallel limit |
| archive_retention_days | 7 | Archive cleanup |

## Key Design Decisions

1. **Asymmetric architecture**: Desktop→Code via files, Code→Desktop via DevTools
2. **File-based queue**: Avoids WSL2 named pipe issues, SQLite locking issues
3. **Atomic writes**: .tmp + rename pattern prevents partial reads
4. **TTL enforcement**: Stale tasks auto-expire to dead-letter
5. **Delegation chain**: Prevents circular delegation (max 3 hops)

## Acceptance Criteria

- [ ] Desktop can write task to queue
- [ ] Code watcher detects task within 5 seconds
- [ ] Code processes task and writes response
- [ ] Response available for Desktop within 10 seconds total
- [ ] Expired tasks move to dead-letter
- [ ] Circular delegation prevented
- [ ] Atomic operations prevent corruption
