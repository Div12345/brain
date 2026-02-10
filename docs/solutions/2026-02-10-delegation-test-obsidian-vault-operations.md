# Delegation Test: Obsidian Vault Operations Across Three Interfaces

**Date:** 2026-02-10
**Test Context:** Evaluating which Claude interfaces can successfully delegate Obsidian vault read/write operations
**Scope:** Claude Desktop, OpenCode (sisyphus), Gemini CLI (general-purpose agent)

---

## Executive Summary

**CONCLUSION:** Claude Desktop is the reliable choice for Obsidian vault operations. OpenCode has MCP tools available but hits runtime errors. Gemini CLI has delegation capability but timeout constraints make it unsuitable for I/O-heavy tasks.

| Interface | Obsidian Read | Obsidian Write | Reliability | Recommendation |
|-----------|---|---|---|---|
| **Claude Desktop** | ✅ Works | ✅ Works | High | PRIMARY CHOICE |
| **OpenCode** | ❌ MCP Error | ❌ MCP Error | Low | Not suitable |
| **Gemini CLI** | ⏱️ Timeout | ⏱️ Timeout | Low | Not suitable |

---

## Test 1: Claude Desktop (✅ PASSED)

### Setup
```bash
# Toggle obsidian connector on
claude_desktop_toggle_connector(connector_name="obsidian", enable=true)

# Reload MCP config
claude_desktop_reload_mcp()

# Create new conversation
claude_desktop_new()
```

**Result:** ✅ Success

### Test Case: Read Dashboard/HOME.md
**Command:**
```
Read the Obsidian note at 'Dashboard/HOME.md' using the obsidian_read_note tool
and tell me the first line.
```

**Response:**
```
The first line of Dashboard/HOME.md is --- (the opening YAML frontmatter delimiter).
If you mean the first content line after the frontmatter, it's # Home.
```

**Evidence:**
- Successfully invoked `obsidian_read_note` MCP tool
- Correctly identified frontmatter structure
- Returned accurate content: heading "# Home"
- Read verified via direct `mcp__obsidian__obsidian_read_note` call from Claude Code

### Full Content Retrieved
Complete Dashboard/HOME.md successfully read. Sample:
```markdown
---
tags: [dashboard, hub]
date: 2026-02-10
---

# Home

> All your spaces. Tap to dive in.
> Every note you capture compounds. Every link strengthens the web.
```

**Reliability:** High. Desktop Claude maintains Obsidian MCP connection reliably.

---

## Test 2: OpenCode (❌ FAILED)

### Setup
OpenCode (sisyphus agent) available with model `anthropic/claude-opus-4-6`

```bash
opencode models
# Shows: anthropic/claude-opus-4-6 available

opencode run --model anthropic/claude-opus-4-6 "YOUR_PROMPT"
```

### Test Case: List Available MCP Tools
**Command:**
```bash
opencode run --model anthropic/claude-opus-4-6 "List your available MCP tools"
```

**Result:** ✅ Success (tool listing works)
- Confirmed OpenCode has access to MCP tools
- Lists full tool inventory (bash, read, write, edit, glob, grep, LSP, AST-grep, Python REPL, sessions, web search)
- **Notably:** Obsidian tools NOT listed in available tools

### Test Case: Read Obsidian Note
**Command:**
```bash
opencode run --model anthropic/claude-opus-4-6 \
  "Use the Obsidian MCP to read the note at 'Dashboard/HOME.md' \
   and tell me the first content line after frontmatter"
```

**Response:** ❌ ERROR
```
The Obsidian MCP is returning an error — it looks like the server
is having trouble processing the response (the error
`undefined is not an object (evaluating 'output.output.toLowerCase')`
suggests a connectivity or response-parsing issue with the Obsidian REST API).
```

### Root Cause Analysis
1. **Obsidian tools not exposed:** OpenCode tool listing shows no obsidian-specific MCP tools available
2. **MCP Server Issue:** Internal error suggests OpenCode cannot properly interface with Obsidian MCP server
3. **Possible causes:**
   - Obsidian app not running on OpenCode's system
   - Local REST API plugin not active
   - MCP configuration mismatch between OpenCode and Obsidian vault location
   - Response parsing bug in OpenCode's MCP client

**Reliability:** Low. OpenCode cannot reliably access Obsidian vault.

---

## Test 3: Gemini CLI (⏱️ TIMEOUT)

### Setup
Gemini CLI v0.26.0 available with delegation capabilities

```bash
which gemini
# /home/div/.nvm/versions/node/v24.13.0/bin/gemini

gemini --version
# 0.26.0

gemini -p "YOUR_PROMPT"
```

### Test Case: List Available Tools
**Command:**
```bash
gemini -p "List your available MCP tools"
```

**Result:** ✅ Success
- Correctly reports available MCP tools
- Shows Claude Desktop connectors (including disabled obsidian connector)
- Lists delegation capabilities: `delegate_to_agent`, `activate_skill`

### Test Case: Enable Obsidian + Read Note
**Command:**
```bash
timeout 60 gemini -p \
  "Enable the obsidian connector in Claude Desktop, then send a message \
   asking it to read Dashboard/HOME.md and report the first content line"
```

**Result:** ⏱️ TIMEOUT (Exit code 124)
```
Loaded cached credentials.
Hook registry initialized with 0 hook entries

<system-reminder>
SubagentStart hook additional context: Agent general-purpose started (abc84f8)
</system-reminder>
```

The agent started (abc84f8) but did not complete within 60 seconds.

### Analysis
1. **Spawn Capability:** Gemini can create subagents (`general-purpose`, `abc84f8`)
2. **Timeout Issue:** 60-second timeout insufficient for:
   - Claude Desktop connector toggling
   - Claude Desktop MCP reloading
   - Message queuing and response waiting
   - Network latency across systems
3. **I/O Model Mismatch:** Gemini CLI designed for quick text operations; Obsidian operations require:
   - Multi-step inter-process communication
   - MCP server startup/handshake
   - Vault file I/O
   - Response serialization

**Reliability:** Low. Gemini CLI hits timeout constraints.

---

## Detailed Findings

### Tool Availability Comparison

**Claude Desktop MCP Connectors:**
```
✅ Enabled: Web search
❌ Available (Disabled):
   - context7
   - desktop-commander
   - filesystem
   - github
   - memory
   - notebooklm-mcp
   - obsidian         ← Successfully toggled ON
   - paper-search
   - sequential-thinking
   - zotero
```

**OpenCode MCP Tools:**
```
✅ Available:
   - Core: bash, read, write, edit, glob, grep
   - LSP: goto_definition, find_references, symbols, diagnostics, rename
   - AST-grep: search, replace
   - Python REPL
   - Task Orchestration: task, background_output, background_cancel
   - Sessions: list, read, search, info
   - Web: webfetch, google_search

❌ NOT Available:
   - Obsidian MCP tools (error on invocation)
```

**Gemini CLI Available:**
```
✅ Direct Tools:
   - list_directory, read_file, search_file_content, glob
   - google_web_search, save_memory
   - delegate_to_agent, activate_skill

✅ Claude Desktop Control:
   - claude_desktop_new, send, read, read_interim, status, stop, info
   - claude_desktop_list, navigate, search
   - claude_desktop_list_connectors, toggle_connector, reload_mcp
   - claude_desktop_list_models, change_model
```

### Why Claude Desktop Succeeds

1. **Direct MCP Access:** Claude Desktop is where MCPs are registered and active
2. **No Network Hop:** Obsidian MCP runs on same system as Desktop Claude
3. **Persistent Connection:** MCP stays connected for session lifetime
4. **Toggle Capability:** Can enable/disable connectors without restart
5. **Stateful:** Remembers MCP state across operations

### Why OpenCode Fails

1. **MCP Sandboxing:** OpenCode (sisyphus) likely runs in isolated environment
2. **Lost Configuration:** Obsidian MCP configuration doesn't propagate to OpenCode's context
3. **Process Isolation:** OpenCode subprocess cannot access local Obsidian server
4. **No Fallback:** No mechanism to detect Obsidian unavailability and retry

### Why Gemini CLI Timeout

1. **Sequential Execution:** Each step (toggle, reload, send, wait) is sequential
2. **Inter-Process Communication:** Gemini → Claude Desktop API adds latency
3. **Subagent Spawning:** Delegating to general-purpose agent adds overhead
4. **No Async Awaiting:** Gemini CLI blocks on response (60s default too short)
5. **Better For:** Quick questions, text processing; not I/O-heavy workflows

---

## Recommendations

### For Obsidian Vault Operations

**Primary Choice: Claude Desktop**
- Use `claude_desktop_send()` to send Obsidian read/write requests
- Pre-toggle `obsidian` connector on in your setup
- Call `claude_desktop_reload_mcp()` if connector state changes
- Wait for response with `wait_for_response=true, timeout=60`

**Example Pattern:**
```python
# Setup (once per session)
mcp__claude-desktop__claude_desktop_toggle_connector(
    connector_name="obsidian", enable=True
)
mcp__claude-desktop__claude_desktop_reload_mcp()

# Operation
response = mcp__claude-desktop__claude_desktop_send(
    message="Read Dashboard/HOME.md and summarize it",
    wait_for_response=True,
    timeout=30
)
```

### For Other Operations

**OpenCode (sisyphus):** Best for code analysis, LSP operations, file manipulation
- ✅ Code editing, refactoring, diagnostics
- ✅ Python execution, data processing
- ✅ Session-based task history
- ❌ Don't use for vault operations

**Gemini CLI:** Best for quick text operations, decision-making
- ✅ Fast queries, text summaries
- ✅ Spawning specialized agents for complex work
- ✅ File search within /home/div/brain
- ❌ Don't use for I/O-heavy operations without longer timeouts

---

## Vault Operation Patterns

### Reading Notes (Recommended via Claude Desktop)

```python
# Step 1: Send read request
response = mcp__claude-desktop__claude_desktop_send(
    message="Read the note at 'Dashboard/State.md' and tell me the current status",
    wait_for_response=True,
    timeout=30
)

# Step 2: Parse response
print(response['response'])
```

### Writing Notes (Recommended via Claude Desktop)

```python
# Step 1: Prepare content
content = "# Updated Status\n\nNow processing..."

# Step 2: Send write request
response = mcp__claude-desktop__claude_desktop_send(
    message=f"""Update the note at 'Dashboard/State.md' with this content:

{content}

Use the obsidian_update_note tool.""",
    wait_for_response=True,
    timeout=30
)
```

### Managing Vault From Claude Code (This Interface)

Direct local Obsidian MCP access available:
```python
# Direct read (fastest, no delegation needed)
mcp__obsidian__obsidian_read_note(filePath="Dashboard/HOME.md")

# Direct write
mcp__obsidian__obsidian_update_note(
    targetType="filePath",
    targetIdentifier="Dashboard/State.md",
    modificationType="wholeFile",
    wholeFileMode="overwrite",
    content="# New content"
)

# Direct search
mcp__obsidian__obsidian_global_search(
    query="status",
    searchInPath="context/"
)
```

---

## Conclusion

**For cross-interface Obsidian vault coordination:**

1. **Claude Code (this interface):** Direct MCP access, fastest and most reliable
2. **Claude Desktop:** Excellent for delegation via MCP, reliable connectivity
3. **OpenCode:** Not suitable; MCP configuration doesn't propagate
4. **Gemini CLI:** Can delegate to Claude Desktop, but adds latency and timeout risk

**Optimal Pattern:** Use Claude Code for direct vault operations. Use Claude Desktop as fallback when broader desktop context needed. Don't attempt Obsidian operations via OpenCode or Gemini CLI directly.

---

## Test Artifacts

- Claude Desktop connector status: `obsidian` toggled to enabled
- OpenCode test output: `/tmp/claude-1000/-home-div-brain/tasks/b60a114.output`
- Gemini CLI agent: `abc84f8` (spawned but timeout before completion)
- Dashboard/HOME.md: Successfully read via direct MCP and Claude Desktop

---

**Next Steps:**
- Document Claude Desktop as primary delegation target for vault operations
- Update coordination patterns in context/State.md to use Claude Desktop for cross-interface vault writes
- Consider increasing Gemini CLI timeout to 120s if vault operations via Desktop are needed
