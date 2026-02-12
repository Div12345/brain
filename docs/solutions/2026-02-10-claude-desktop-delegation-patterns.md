---
tags: [delegation, claude-desktop, obsidian, mcp]
date: 2026-02-10
---

# Claude Desktop Delegation Patterns

Reliable patterns for delegating work from Claude Code to Claude Desktop.

## Quick Reference

**Use Claude Desktop when:**
- Need desktop context (browser, screenshots)
- Want to offload work from CC context window
- Need MCPs that CC doesn't have loaded

**Use Claude Code direct when:**
- Fastest path for Obsidian read/write (has MCP directly)
- File operations in /home/div/brain
- LSP operations, code analysis

## Reliable Pattern

```python
# 1. Toggle connector on (if needed)
mcp__claude-desktop__claude_desktop_toggle_connector(
    connector_name="obsidian", enable=True
)

# 2. Reload MCP to apply changes
mcp__claude-desktop__claude_desktop_reload_mcp()

# 3. Start fresh conversation
mcp__claude-desktop__claude_desktop_new()

# 4. Send task and wait for response
response = mcp__claude-desktop__claude_desktop_send(
    message="Read Dashboard/HOME.md and summarize it",
    wait_for_response=True,
    timeout=30
)

# 5. Read the response
result = mcp__claude-desktop__claude_desktop_read()
```

## What Works

**Claude Desktop:**
- ✅ Obsidian MCP access (via connector toggle)
- ✅ Direct MCP access to registered connectors
- ✅ Persistent connection across operations
- ✅ Reliable for 30s timeout operations

**Claude Code:**
- ✅ Fastest Obsidian operations (direct MCP)
- ✅ File operations in /home/div/brain
- ✅ LSP, AST-grep, code analysis

## What Doesn't Work

**OpenCode (sisyphus):**
- ❌ MCP sandboxing blocks Obsidian access
- ❌ Error: `undefined is not an object evaluating output.output.toLowerCase`
- ✅ Use for: code analysis, LSP operations only

**Gemini CLI:**
- ⏱️ Timeout issues on multi-step MCP operations
- ⏱️ 60s insufficient for: toggle → reload → send → wait
- ✅ Use for: quick queries, text processing only

## Timeout Guidelines

| Operation | Timeout | Notes |
|-----------|---------|-------|
| Simple read | 15s | Single note read |
| Complex read | 30s | Multiple notes or search |
| Write operation | 30s | Note update with validation |
| Multi-step task | 60s | Requires multiple MCP calls |

## Common Patterns

### Read Obsidian Note
```python
response = mcp__claude-desktop__claude_desktop_send(
    message="Read 'Dashboard/State.md' and report current status",
    wait_for_response=True,
    timeout=30
)
```

### Update Obsidian Note
```python
content = "# New Status\n\nProcessing complete."
response = mcp__claude-desktop__claude_desktop_send(
    message=f"""Update 'Dashboard/State.md' with:

{content}

Use obsidian_update_note tool.""",
    wait_for_response=True,
    timeout=30
)
```

### Search Vault
```python
response = mcp__claude-desktop__claude_desktop_send(
    message="Search for 'throttlestop' in Dashboard/ folder",
    wait_for_response=True,
    timeout=30
)
```

## Bulk Mining / Research Tasks

Long-running CD tasks (like mining daily notes) need explicit instructions to avoid waste.

### What Went Wrong (2026-02-11 mining session)

| Issue | Wasted | Fix |
|-------|--------|-----|
| CD didn't know it had Obsidian tools | 1 full round-trip | Explicitly name available tools |
| ~20 sequential searches with commentary | Token waste + latency | Batch all keywords upfront |
| Doc generated 3 times (artifact → paste → vault) | 2 extra round-trips | Specify output destination in initial prompt |
| No truncation handling | Cut-off content | Tell it to continue if truncated |

### Better Prompt Template for Mining Tasks

```
You have Obsidian MCP tools: obsidian_global_search, obsidian_read_note,
obsidian_list_notes, obsidian_update_note. Use them directly.

TASK: [describe what to mine/search for]

SEARCH STRATEGY:
- Run obsidian_global_search for EACH of these keywords: [list all]
- Search in path: "Daily/"
- After ALL searches complete, read the top matches for context
- Do NOT stop between searches to discuss — batch them

OUTPUT:
- Save results DIRECTLY to Obsidian vault at: [exact path]
- Use obsidian_update_note with targetType "filePath"
- If the content is too long for one update, split into parts and append
- Do NOT create file artifacts or paste inline — vault only

FORMAT: [describe expected structure]

If output gets truncated, continue in your next message and append to the
same vault file.
```

### CD Delegation System (v2)

The goal: **one blocking haiku agent, no polling, with guidance and logging.**

#### Architecture

```
CC (Opus) → spawns haiku agent → haiku sends to CD → blocks on response → returns result
                                                  ↓
                                          logs saved to brain repo
```

#### Haiku Agent Prompt Template

```
You are controlling Claude Desktop to complete a task. Follow this exactly:

1. SEND the task using claude_desktop_send with wait_for_response=true, timeout=300
2. READ the response with claude_desktop_read
3. EVALUATE: Did CD complete the task?
   - If CD says "I don't have X tools": send a follow-up telling it to check
     its tools list, then wait again (wait_for_response=true, timeout=120)
   - If CD's output is truncated/incomplete: send "Continue from where you
     stopped and append to the same file" and wait again
   - If CD completed successfully: return the result
4. SAVE a log of what happened (success/failure/retries) to stdout
5. Return the final result or failure reason

MAX RETRIES: 3 guidance messages before giving up.
DO NOT poll with claude_desktop_read in a loop.
DO NOT use Bash sleep commands.
Each interaction should be a send(wait=true) → evaluate → respond cycle.
```

#### Log Storage

After haiku returns, CC saves a summary to:
`brain/logs/cd-delegations/YYYY-MM-DD-<task-slug>.md`

Format:
```markdown
# CD Delegation: <task name>
- Date: YYYY-MM-DD HH:MM
- Haiku agent ID: <id>
- CD model: <model>
- Task: <one-line summary>
- Result: success/partial/failed
- Retries: N
- Guidance sent: <what corrections were needed>
- Output location: <where results were saved>
- Token cost: <from subagent audit>
```

#### Compounding

At end of session or during compound step:
1. Run `cc-session-audit.sh --subagents` to get per-agent token costs
2. Review `logs/cd-delegations/` for patterns (recurring failures, common guidance needed)
3. Feed failures back into:
   - The prompt template (prevent the same confusion)
   - `docs/solutions/` if it's a new pattern
   - Routing rules if CD isn't the right target

#### Persistence & Recovery Rules

CD can lose context mid-task. Defend against this:

1. **Checkpoint results** — tell CD to save partial results to vault after each major scan/step, not only at the end
2. **Save scripts first** — if CD generates a PowerShell or shell script, tell it to save the script to a file before executing, so it survives context loss
3. **Recovery-friendly output** — vault file should have clear section headers so CD (or a new CD session) can read the partial file and continue from where it left off
4. **Idempotent appends** — use `modificationType: "append"` for incremental results, not `"wholeFile"` overwrite mid-task

Add to the task prompt:
```
PERSISTENCE: After each major scan step, save results immediately to the vault
file using obsidian_update_note (append mode). Do NOT wait until the end.
If you generate any scripts, save them to a file before executing.
```

#### Token-Saving Rules

1. **Block, don't poll** — one `send(wait=true, timeout=300)` instead of read loops
2. Tell CD to minimize commentary between tool calls
3. Specify "save to vault" not "share with me" — avoids paste round-trips
4. Give the full plan upfront so CD doesn't ask clarifying questions
5. Name the MCP tools explicitly in the prompt — CD doesn't always know what it has
6. **Don't use monitoring agents** — CC can check CD status directly with `claude_desktop_status` + `claude_desktop_read`; a polling subagent wastes tokens on sleep loops

## Source

Full test results: `/home/div/brain/docs/solutions/2026-02-10-delegation-test-obsidian-vault-operations.md`
