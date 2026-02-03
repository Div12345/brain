# Implementation Plan: Bidirectional Claude Bridge

## Phase 1: Foundation [PARALLEL - 4 tasks]

### Step 1.1: Create bridge package
- **File:** `bridge/__init__.py`
- **Test:** `python -c "from bridge import *"`

### Step 1.2: Create Pydantic schema models
- **File:** `bridge/schema.py`
- **Models:** Task, TaskPayload, TaskSource, Response, ResponseError
- **Test:** Instantiate, serialize to JSON

### Step 1.3: Create configuration module
- **File:** `bridge/config.py`
- **Config:** BridgeConfig with queue_path, poll_interval_ms, max_concurrent_tasks, etc.
- **Test:** Load config, verify defaults

### Step 1.4: Update dependencies
- **File:** `pyproject.toml`
- **Add:** pydantic>=2.0.0, watchdog>=3.0.0
- **Test:** `pip install -e .`

## Phase 2: Directory Setup [SEQUENTIAL after 1.3]

### Step 2.1: Create queue directories
- **File:** `bridge/config.py` (add `ensure_directories()`)
- **Dirs:** queue/, processing/, responses/, dead-letter/, archive/, logs/, context/
- **Test:** All directories exist at /mnt/c/Users/din18/.claude-bridge/

### Step 2.2: Create default config.json
- **File:** `bridge/config.py` (add `write_default_config()`)
- **Test:** config.json exists with valid JSON

## Phase 3: Core Logic [PARTIAL PARALLEL]

### Step 3.1: Implement hybrid watcher [after 1.2, 1.3]
- **File:** `bridge/watcher.py`
- **Classes:** HybridWatcher, TaskFileHandler, ConcurrencyController
- **Features:**
  - inotify via watchdog + polling fallback
  - Auto-detect inotify failures on WSL2
  - Concurrency control (max 5 tasks)
- **Test:** Create file in queue/, verify callback within 500ms

### Step 3.2: Implement task processor [after 1.2]
- **File:** `bridge/processor.py`
- **Class:** TaskProcessor with handlers for:
  - `message`: Log to context file, return ack
  - `command`: Execute predefined safe commands (status, read_file, list_tasks)
  - `query`: Return state data
  - `delegate`: Re-queue with updated chain, max 3 hops
- **Test:** Process each task type, verify correct behavior

### Step 3.3: Implement response delivery [after 3.2]
- **File:** `bridge/notify.py`
- **Function:** `notify_desktop(response)` - use existing server.py DevTools
- **File:** `bridge/processor.py` (add ResponseWriter)
- **Features:**
  - Atomic write to responses/{task_id}.json
  - Push notification via DevTools
  - Fallback: Desktop polls responses/
- **Test:** Write response, verify Desktop notification

## Phase 4: Entry Point [SEQUENTIAL after 3.1, 3.3]

### Step 4.1: Create watch_queue.py script
- **File:** `scripts/watch_queue.py`
- **Features:**
  - Initialize config
  - Ensure directories
  - Start hybrid watcher
  - Handle SIGINT/SIGTERM
- **Test:** Start with `python scripts/watch_queue.py`, Ctrl+C stops cleanly

### Step 4.2: Add script entry point
- **File:** `pyproject.toml`
- **Add:** `watch-queue = "scripts.watch_queue:main"`
- **Test:** After `pip install -e .`, `watch-queue` command works

## Phase 5: Integration Testing [SEQUENTIAL after 4.1]

### Step 5.1: End-to-end test
- Write task to queue/
- Verify watcher detects within 5 seconds
- Verify response within 10 seconds total

### Step 5.2: TTL expiration test
- Task with ttl_seconds=1 moves to dead-letter after expiry

### Step 5.3: Circular delegation test
- Task with 3-hop chain is rejected

### Step 5.4: Concurrency limit test
- Submit 6 tasks, verify 5 process, 1 waits

## Dependency Graph

```
1.1 ──┐
1.2 ──┼──> 3.1 ──┐
1.3 ──┼──> 2.1 ──> 2.2    ├──> 4.1 ──> 4.2 ──> 5.x
1.4 ──┘           │       │
                  └──> 3.2 ──> 3.3 ──┘
```

## Task Type Semantics

| Type | Action | Response |
|------|--------|----------|
| `message` | Log to context file | `{acknowledged: true}` |
| `command` | Execute safe command | `{output: "..."}` |
| `query` | Read state | `{data: {...}}` |
| `delegate` | Re-queue with chain | `{delegated: true}` |

## Acceptance Criteria

- [ ] Desktop can write task to queue
- [ ] Code watcher detects task within 5 seconds
- [ ] Code processes task and writes response
- [ ] Response available within 10 seconds total
- [ ] Expired tasks move to dead-letter
- [ ] Circular delegation prevented (max 3 hops)
- [ ] Concurrency limit enforced (max 5 tasks)
- [ ] WSL2 inotify fallback to polling works
