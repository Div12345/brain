# Claude Code Transcript Mapping

**Created:** 2026-02-03
**Purpose:** Map Claude Code's transcript files for scheduler feedback processing

---

## Transcript Location

```
~/.claude/projects/{project-path-slug}/{session-id}.jsonl
```

| Project | Path |
|---------|------|
| brain | `~/.claude/projects/-home-div-brain/*.jsonl` |
| Any project | Replace `/` with `-` in path, prefix with `-` |

**Session Index:** `~/.claude/projects/{slug}/sessions-index.json`

---

## Entry Types

| Type | Count (typical) | Contains |
|------|-----------------|----------|
| `progress` | Many | Tool execution progress, streaming output |
| `assistant` | Per turn | Claude's responses, tool calls |
| `user` | Per turn | User messages, todos, permission mode |
| `system` | Few | Hook results, stop reasons |
| `file-history-snapshot` | Periodic | File backup states |
| `queue-operation` | Few | Task queue operations |

---

## Key Fields by Type

### `assistant` Entry
```json
{
  "type": "assistant",
  "message": { "role": "assistant", "content": [...] },
  "timestamp": "2026-02-03T18:38:47.350Z",
  "sessionId": "e86c9cad-...",
  "uuid": "unique-id",
  "cwd": "/home/div/brain",
  "gitBranch": "claude/..."
}
```

### `user` Entry
```json
{
  "type": "user",
  "message": { "role": "user", "content": "..." },
  "timestamp": "...",
  "todos": [...],
  "permissionMode": "..."
}
```

### `progress` Entry
```json
{
  "type": "progress",
  "data": { "tool": "...", "status": "..." },
  "toolUseID": "...",
  "parentToolUseID": "..."
}
```

### `system` Entry
```json
{
  "type": "system",
  "subtype": "hook-result",
  "slug": "SessionStart",
  "hookCount": 2,
  "stopReason": "...",
  "hasOutput": true
}
```

---

## Useful Queries

### Get Session Duration
```python
import json
from datetime import datetime

def get_session_duration(transcript_path):
    first_ts = last_ts = None
    with open(transcript_path) as f:
        for line in f:
            d = json.loads(line)
            ts = d.get("timestamp")
            if ts:
                if not first_ts:
                    first_ts = ts
                last_ts = ts
    return first_ts, last_ts
```

### Count Tool Calls
```python
def count_tools(transcript_path):
    from collections import Counter
    tools = Counter()
    with open(transcript_path) as f:
        for line in f:
            d = json.loads(line)
            if d.get("type") == "assistant":
                msg = d.get("message", {})
                for content in msg.get("content", []):
                    if isinstance(content, dict) and content.get("type") == "tool_use":
                        tools[content.get("name")] += 1
    return tools
```

### Check for Errors
```python
def find_errors(transcript_path):
    errors = []
    with open(transcript_path) as f:
        for line in f:
            d = json.loads(line)
            if d.get("type") == "system" and d.get("hookErrors"):
                errors.append(d)
            # Also check for tool errors in progress entries
            if d.get("type") == "progress":
                data = d.get("data", {})
                if "error" in str(data).lower():
                    errors.append(d)
    return errors
```

### Live Monitoring (tail transcript)
```bash
# Watch transcript in real-time during scheduled task
TRANSCRIPT=~/.claude/projects/-home-div-brain/${SESSION_ID}.jsonl
tail -f "$TRANSCRIPT" | jq -r 'select(.type=="progress") | .data'
```

---

## Mapping: Scheduler → Transcript

| Scheduler Concept | Transcript Location |
|-------------------|---------------------|
| Task started | First `user` entry timestamp |
| Task ended | Last entry timestamp |
| Success/failure | Check for errors, `system.stopReason` |
| Token usage | Count content length in `assistant` entries |
| Tool calls | `assistant.message.content[].type == "tool_use"` |
| Tool results | `progress` entries with matching `toolUseID` |
| Duration | Last timestamp - first timestamp |

---

## Integration Points

### 1. Feedback Processing (Post-Execution)
Instead of our `history.jsonl`, we could parse the transcript:
```python
def extract_metrics_from_transcript(session_id):
    path = f"~/.claude/projects/-home-div-brain/{session_id}.jsonl"
    # Parse and extract: duration, tool_count, errors, etc.
```

### 2. Live Monitoring (During Execution)
```python
import subprocess
# Tail the transcript file
proc = subprocess.Popen(
    ["tail", "-f", transcript_path],
    stdout=subprocess.PIPE
)
for line in proc.stdout:
    entry = json.loads(line)
    if entry.get("type") == "progress":
        print(f"Tool: {entry.get('data', {}).get('tool')}")
```

### 3. Session Discovery
```python
def find_recent_sessions(project_slug):
    import os
    from pathlib import Path

    project_dir = Path.home() / ".claude" / "projects" / project_slug
    sessions = []
    for f in project_dir.glob("*.jsonl"):
        if f.name != "sessions-index.json":
            stat = f.stat()
            sessions.append((f, stat.st_mtime))
    return sorted(sessions, key=lambda x: -x[1])  # Most recent first
```

---

## When to Use Transcript vs Our Logs

| Use Case | Use Transcript | Use Our Logs |
|----------|----------------|--------------|
| Detailed debugging | ✓ (full context) | |
| Quick success rate | | ✓ (history.jsonl) |
| Token estimation | ✓ (accurate) | ✓ (rough) |
| Error classification | ✓ (detailed) | ✓ (categorized) |
| Live monitoring | ✓ (tail -f) | |
| Cross-session queries | | ✓ (single file) |
| Capacity tracking | | ✓ (index.jsonl) |

---

## Environment Variables for Correlation

The scheduler passes these env vars so transcripts can be correlated:

```
CCQ_TASK_ID     → Task name
CCQ_RUN_ID      → Unique run identifier
CCQ_LOG_FILE    → Path to our markdown log
CCQ_TASK_FILE   → Path to task definition
```

To find transcript for a scheduled task:
1. Task runs with `CCQ_RUN_ID=run-2026-02-03-1430`
2. Find transcript by timestamp match in `sessions-index.json`
3. Or: Store `sessionId` in our log for direct lookup

---

## Future Enhancement: Direct Correlation

Add to executor.py to capture sessionId:
```python
# After execution, find the transcript that was just created
# by matching timestamp to our run_id
# Store sessionId in history.jsonl for direct lookup
```

This would allow:
```python
history_entry = {
    "task_id": "...",
    "session_id": "e86c9cad-...",  # Claude's session ID
    ...
}
```

Then queries can directly access the rich transcript data.
