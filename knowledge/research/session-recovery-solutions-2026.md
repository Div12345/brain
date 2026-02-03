# Session Recovery Solutions for Claude Code

**Research Date:** 2026-02-02
**Objective:** Document mechanisms for recovering from incomplete/cut-off Claude Code sessions

---

## Executive Summary

Claude Code sessions can be interrupted unexpectedly (browser crashes, compaction issues, user abandonment). Recovery mechanisms exist at multiple layers:

1. **Built-in Auto-Save:** JSONL format with line-by-line persistence
2. **Checkpointing:** Automatic code state snapshots before edits
3. **Hook-Based Capture:** PreCompact and SessionEnd hooks for state preservation
4. **Third-Party Tools:** Session restore, context preservation, and recovery tools

**Critical Gap:** Auto-compaction can lose context without proper hooks configured.

---

## Session Recovery Solutions

### Existing Tools

| Tool | Recovery Mechanism | Auto-Save? | Works on Cutoff? | Link |
|------|-------------------|------------|------------------|------|
| **claude-session-restore** | Analyzes JSONL + git history, multi-vector extraction | No | Yes (reads existing files) | [GitHub](https://github.com/ZENG3LD/claude-session-restore) |
| **cc-sessions** | Fast CLI to list/resume sessions across projects | No | Yes (scans existing sessions) | [GitHub](https://github.com/chronologos/cc-sessions) |
| **claude-code-tools** | Full-text search + resume with lineage tracking | No | Yes (Tantivy search index) | [GitHub](https://github.com/pchalasani/claude-code-tools) |
| **claude-session-saver** | Auto-saves uncommitted changes/stashes to GitHub | Yes (on close) | Partial (needs clean exit) | [GitHub](https://github.com/ybouhjira/claude-session-saver) |
| **c0ntextKeeper** | 7 hooks + 187 patterns for context preservation | Yes (via hooks) | Yes (PreCompact hook) | [GitHub](https://github.com/Capnjbrown/c0ntextKeeper) |
| **ccheckpoints** | Timeline of coding sessions with web dashboard | Yes (every interaction) | Yes | [GitHub](https://github.com/p32929/ccheckpoints) |
| **Built-in Checkpointing** | Auto-captures code state before each edit | Yes (automatic) | Yes (survives crashes) | [Docs](https://code.claude.com/docs/en/checkpointing) |

### Key Findings

**Best for Unexpected Cutoffs:**
- **c0ntextKeeper** - PreCompact hook captures state before auto-compaction
- **Built-in JSONL** - Line-by-line writes survive crashes (only last incomplete line lost)
- **Built-in Checkpointing** - Code state preserved even if conversation lost

**Best for Manual Recovery:**
- **claude-session-restore** - Analyzes existing sessions with AI summarization
- **claude-code-tools** - Full-text search across all historical sessions

---

## Auto-Save Patterns

### 1. JSONL Line-by-Line Persistence

**How it works:**
- Each message written as separate line immediately to `~/.claude/projects/<project>/<session-id>.jsonl`
- No outer JSON wrapper - crash-resistant by design
- Only last incomplete message potentially lost on sudden termination

**Structure:**
```jsonl
{"role":"user","content":[{"type":"text","text":"..."}],"sessionId":"...","timestamp":"..."}
{"role":"assistant","content":[{"type":"text","text":"..."}],"sessionId":"..."}
{"role":"tool_use","content":[...],"toolName":"..."}
{"role":"tool_result","content":[...],"toolCallId":"..."}
```

**Survival:** Excellent - survives all crash types except filesystem corruption

**Sources:**
- [How Claude Code Manages Local Storage](https://milvus.io/blog/why-claude-code-feels-so-stable-a-developers-deep-dive-into-its-local-storage-design.md)
- [Analyzing Claude Code Logs with DuckDB](https://liambx.com/blog/claude-code-log-analysis-with-duckdb)

### 2. Built-in Checkpointing

**How it works:**
- Automatic snapshots before each file edit
- Tracks conversation position + file states
- `/rewind` command or double-tap ESC to restore

**Limitations:**
- Does NOT track bash command modifications
- Only captures Claude's direct edits via tools

**Survival:** Excellent for code state, but conversation context depends on JSONL

**Sources:**
- [Checkpointing - Claude Code Docs](https://code.claude.com/docs/en/checkpointing)
- [Claude Code Checkpoints Guide](https://skywork.ai/skypage/en/claude-code-checkpoints-ai-coding/1976917740735229952)

### 3. Hook-Based Checkpointing

**PreCompact Hook Pattern:**
```bash
#!/bin/bash
# ~/.claude/hooks/pre-compact.sh

SESSION_FILE="$CLAUDE_SESSION_FILE"
BACKUP_DIR="$HOME/.claude/recovery/$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BACKUP_DIR"
cp "$SESSION_FILE" "$BACKUP_DIR/session.jsonl"

# Extract critical context
jq -c 'select(.role=="user" or .role=="assistant") | {role, content}' \
  "$SESSION_FILE" > "$BACKUP_DIR/conversation.jsonl"

echo "[PreCompact] Backed up to $BACKUP_DIR" >&2
```

**Hooks Available:**
| Hook | When Triggered | Use for Recovery |
|------|---------------|------------------|
| `precompact` | Before context compaction | Save full state before summarization |
| `sessionend` | Session closes cleanly | Final checkpoint (won't fire on crash) |
| `sessionstart` | Session begins | Restore from previous backup |
| `posttool` | After each tool execution | Continuous incremental saves |
| `stop` | Agent stops (including crashes) | Emergency checkpoint |

**c0ntextKeeper Implementation:**
- Triggers on PreCompact to archive full context
- Creates searchable archives (< 10ms overhead)
- Auto-redacts sensitive data (API keys, PII)
- MCP tools for retrieval: `retrieve-context`, `search-archives`

**Sources:**
- [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [c0ntextKeeper GitHub](https://github.com/Capnjbrown/c0ntextKeeper)
- [Claude Code Hooks Guide](https://www.datacamp.com/tutorial/claude-code-hooks)

---

## Compaction Handling

### What Survives Compaction

**Preserved:**
- Summary of conversation (lossy)
- Critical facts if explicitly marked
- Task list structure (if using todo system)
- File paths and recent changes

**Lost Without Hooks:**
- Detailed reasoning chains
- Intermediate exploration results
- Skill procedures and methodologies
- User preferences and decisions

**Sources:**
- [Claude Code Context Recovery](https://medium.com/@sonuyadav1/claude-code-context-recovery-stop-losing-progress-when-context-compacts-772830ee7863)
- [Understanding Conversation Compacting](https://www.ajeetraina.com/understanding-claudes-conversation-compacting-a-deep-dive-into-context-management/)

### Manual vs Auto-Compact

| Type | Control | Preservation Instructions | Recovery Difficulty |
|------|---------|--------------------------|-------------------|
| Manual `/compact` | Full | Can specify what to keep | Easy (you know it happened) |
| Auto-compact | None | No customization | Hard (silent, ~25% context remaining) |

**Auto-compact triggers at:**
- ~75% context window usage
- Reserves ~20% for compaction process itself
- No user notification in CLI (notification in Desktop app)

**Manual compact examples:**
```
/compact preserve the API patterns we established
/compact only keep file paths and task list
/compact keep architectural decisions and constraints
```

**Sources:**
- [Claude Code Compaction](https://stevekinney.com/courses/ai-development/claude-code-compaction)
- [Context Compaction | Forge Code](https://forgecode.dev/docs/context-compaction/)

### Critical Compaction Bugs (2026)

**Skill Amnesia After Auto-Compaction:**
- Claude forgets which skills were loaded
- Does NOT re-read skill files after compaction
- System prompts may be incorrectly included in lossy compression

**Workaround:** PreCompact hook to save active skill list, SessionStart hook to re-inject

**Sources:**
- [Issue #13919: Skills context lost after auto-compaction](https://github.com/anthropics/claude-code/issues/13919)
- [Issue #7533: Context preservation prioritized over correctness](https://github.com/anthropics/claude-code/issues/7533)

---

## Recommended Approach

### For Sessions That Get Cut Off Unexpectedly

**Immediate (Zero Configuration):**
1. **Trust JSONL auto-save** - All messages already persisted to disk
2. **Use built-in resume** - `claude --resume` loads full JSONL history
3. **Check checkpoints** - `/rewind` if code state corrupted

**Enhanced (5-Minute Setup):**
1. **Install c0ntextKeeper:**
   ```bash
   npm install -g c0ntextkeeper
   c0ntextkeeper setup
   ```
2. **Configure PreCompact hook** - Auto-saves before context loss
3. **Enable SessionEnd hook** - Checkpoint on clean exits

**Advanced (10-Minute Setup):**
1. **Install claude-session-restore** for AI-powered recovery:
   ```bash
   npm install -g claude-session-restore
   ```
2. **Install cc-sessions** for fast cross-project resume:
   ```bash
   cargo install cc-sessions
   ```
3. **Set up periodic backups:**
   ```bash
   # Cron job: backup sessions daily
   0 2 * * * rsync -a ~/.claude/projects/ ~/.claude/backups/$(date +\%Y\%m\%d)/
   ```

### Recovery Workflow After Cutoff

```
1. Identify session:
   cc-sessions list | grep <project-name>

2. Check session integrity:
   wc -l ~/.claude/projects/<project>/<session-id>.jsonl
   tail -n 1 ~/.claude/projects/<project>/<session-id>.jsonl | jq

3. Recover with context:
   claude-session-restore --session <session-id>
   # Or: claude --resume --session <session-id>

4. If compaction occurred during session:
   c0ntextkeeper retrieve --session <session-id> --before-compact

5. Resume with recovered context:
   claude --resume --session <session-id>
   # Manually provide context summary from step 4
```

### Prevention Strategy

**Layer 1: Built-in Protection (Always Active)**
- JSONL line-by-line persistence
- Automatic checkpointing before edits

**Layer 2: Hook-Based Capture (5 min setup)**
- PreCompact hook for state preservation
- PostTool hook for incremental saves

**Layer 3: External Archival (10 min setup)**
- c0ntextKeeper for searchable archives
- Periodic filesystem backups

**Layer 4: Recovery Tools (Install as needed)**
- claude-session-restore for analysis
- cc-sessions for fast resume
- claude-code-tools for historical search

---

## State Management Tools

### cchistory

**Purpose:** Track Claude Code system prompt and tool definition changes across versions

**How it works:**
- Enumerates all Claude Code versions from 1.0.0 onwards
- Downloads each version, runs through claude-trace
- Extracts system prompts, tool definitions, first-message augmentations

**Use for recovery:** Understand version differences if resuming session from older Claude Code version

**Web Interface:** https://cchistory.mariozechner.at/

**Sources:**
- [cchistory: Tracking Claude Code Changes](https://mariozechner.at/posts/2025-08-03-cchistory/)

### Session State Location

**Primary storage:**
- Session files: `~/.claude/projects/<project>/<session-id>.jsonl`
- Session index: `~/.claude/projects/<project>/sessions-index.json`
- Global state: Internal object called `r0` (not directly accessible)

**Backup storage (if configured):**
- c0ntextKeeper archives: `~/.c0ntextkeeper/archives/`
- checkpoint backups: Varies by tool

**Working directory tracking:**
- Session manager tracks `cwd` where session created
- `--resume` by name matches current directory context
- Supports git worktrees correctly

**Sources:**
- [Claude Code Internals Part 6: Session State Management](https://kotrotsos.medium.com/claude-code-internals-part-6-session-state-management-e729f49c8bb9)
- [Session Management | anthropics/claude-code](https://deepwiki.com/anthropics/claude-code/2.4-session-management)

### Real-Time Monitoring

**Claude HUD:**
- Displays real-time session info below input
- Context usage, tool activity, agent status, todo progress
- Updates every ~300ms
- No separate window required

**Claude Code UI:**
- Dashboard for monitoring sessions across projects
- See active work, pending approvals, PR/CI status
- Built on Durable Streams for real-time updates

**Sources:**
- [Claude HUD: Real-Time Session Visibility](https://www.vibesparking.com/en/blog/ai/claude-code/2026-01-04-claude-hud-real-time-session-monitor/)
- [Claude Code UI by KyleAMathews](https://github.com/KyleAMathews/claude-code-ui)

---

## Implementation Priorities

### Tier 1: Essential (Do First)
1. **Verify built-in recovery works:** Test `claude --resume` on existing sessions
2. **Install c0ntextKeeper:** Best ROI for auto-compaction protection
3. **Create PreCompact backup hook:** 5-line script for manual backup

### Tier 2: Recommended (Do Soon)
4. **Install claude-session-restore:** For when things go wrong
5. **Set up periodic backups:** Daily rsync of `~/.claude/projects/`
6. **Monitor with Claude HUD:** Awareness prevents issues

### Tier 3: Advanced (Optional)
7. **Install cc-sessions:** If working across many projects
8. **Set up claude-code-tools:** If need to search historical sessions
9. **Custom PostTool hooks:** For domain-specific state preservation

---

## Critical Insights

### What Actually Survives Crashes

| Event Type | JSONL Survives | Checkpoints Survive | Conversation Context | Code State |
|------------|---------------|-------------------|-------------------|-----------|
| Browser crash | ✅ Yes | ✅ Yes | ⚠️ Last message incomplete | ✅ Yes |
| Force quit | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Auto-compaction | ✅ Yes | ✅ Yes | ❌ Summarized (lossy) | ✅ Yes |
| Manual `/clear` | ✅ Yes (file intact) | ❌ Reset | ❌ Cleared | ✅ Yes (files on disk) |
| Session timeout | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

**Key takeaway:** Code state highly resilient, conversation context most vulnerable to auto-compaction.

### The Auto-Compaction Problem

**Why it's dangerous:**
- Silent operation (no warning in CLI)
- Lossy summarization loses nuance
- Skills forgotten entirely
- No built-in pre-compaction backup

**Why hooks are critical:**
- Only way to capture state before loss
- PreCompact hook runs before summarization
- <10ms overhead per hook call
- c0ntextKeeper does this automatically

### Recovery vs Prevention

**Recovery tools (reactive):**
- claude-session-restore
- cc-sessions
- Manual JSONL parsing

**Prevention tools (proactive):**
- c0ntextKeeper (PreCompact hooks)
- ccheckpoints (continuous saves)
- Manual backup scripts

**Recommendation:** Invest in prevention (hooks) > recovery (manual restore)

---

## Tools Comparison Matrix

| Tool | Install Time | Learning Curve | Auto-Recovery | Manual Recovery | Crash-Resistant | Compaction-Resistant |
|------|-------------|----------------|---------------|-----------------|----------------|-------------------|
| Built-in JSONL | 0s (included) | None | ✅ | ✅ | ✅ | ⚠️ Partial |
| Built-in Checkpoints | 0s (included) | Low | ✅ | ✅ | ✅ | ✅ |
| c0ntextKeeper | 2 min | Low | ✅ | ✅ | ✅ | ✅ |
| claude-session-restore | 1 min | Medium | ❌ | ✅ | ✅ | ⚠️ Limited |
| cc-sessions | 3 min (Rust) | Low | ❌ | ✅ | ✅ | ❌ |
| claude-code-tools | 5 min | High | ❌ | ✅ | ✅ | ❌ |
| ccheckpoints | 2 min | Medium | ✅ | ✅ | ✅ | ⚠️ Limited |
| claude-session-saver | 1 min | Low | ⚠️ Partial | ❌ | ⚠️ Needs clean exit | ❌ |

**Legend:**
- ✅ Full support
- ⚠️ Partial support
- ❌ Not supported

---

## Recommendations Summary

### For Developers Who Want Zero-Config Recovery
**Use built-in features only:**
1. Trust JSONL auto-save
2. Use `claude --resume` for recovery
3. Use `/rewind` for code state issues

**Limitations:** Vulnerable to auto-compaction context loss

### For Developers Who Want Robust Recovery
**Install minimal tooling:**
1. `c0ntextKeeper` (handles auto-compaction)
2. `claude-session-restore` (for manual recovery)
3. Daily backup script (for disaster recovery)

**Time investment:** 10 minutes setup, zero ongoing maintenance

### For Power Users Managing Multiple Projects
**Full stack:**
1. c0ntextKeeper (prevention)
2. claude-session-restore (AI recovery)
3. cc-sessions (fast cross-project switching)
4. claude-code-tools (historical search)
5. Claude HUD (real-time monitoring)
6. Custom hooks for domain-specific state

**Time investment:** 30 minutes setup, high ongoing value

---

## Sources

### Official Documentation
- [Checkpointing - Claude Code Docs](https://code.claude.com/docs/en/checkpointing)
- [Hooks Reference - Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Session Management - Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/sessions)

### Key GitHub Projects
- [ZENG3LD/claude-session-restore](https://github.com/ZENG3LD/claude-session-restore)
- [chronologos/cc-sessions](https://github.com/chronologos/cc-sessions)
- [pchalasani/claude-code-tools](https://github.com/pchalasani/claude-code-tools)
- [Capnjbrown/c0ntextKeeper](https://github.com/Capnjbrown/c0ntextKeeper)
- [p32929/ccheckpoints](https://github.com/p32929/ccheckpoints)
- [ybouhjira/claude-session-saver](https://github.com/ybouhjira/claude-session-saver)

### Community Resources
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Code Usage Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)
- [claude-JSONL-browser](https://github.com/withLinda/claude-JSONL-browser)
- [claude-code-log](https://github.com/daaain/claude-code-log)

### Analysis & Tutorials
- [How Claude Code Manages Local Storage](https://milvus.io/blog/why-claude-code-feels-so-stable-a-developers-deep-dive-into-its-local-storage-design.md)
- [Claude Code Context Recovery (Medium)](https://medium.com/@sonuyadav1/claude-code-context-recovery-stop-losing-progress-when-context-compacts-772830ee7863)
- [Teaching Claude To Remember Part 3](https://medium.com/@porter.nicholas/teaching-claude-to-remember-part-3-sessions-and-resumable-workflow-1c356d9e442f)
- [Understanding Conversation Compacting](https://www.ajeetraina.com/understanding-claudes-conversation-compacting-a-deep-dive-into-context-management/)
- [Claude Code Hooks Tutorial (DataCamp)](https://www.datacamp.com/tutorial/claude-code-hooks)
- [cchistory Analysis](https://mariozechner.at/posts/2025-08-03-cchistory/)

### Tools & Monitoring
- [cchistory Web Interface](https://cchistory.mariozechner.at/)
- [Claude HUD](https://www.vibesparking.com/en/blog/ai/claude-code/2026-01-04-claude-hud-real-time-session-monitor/)
- [Analyzing Logs with DuckDB](https://liambx.com/blog/claude-code-log-analysis-with-duckdb)

---

**Last Updated:** 2026-02-02
**Researcher:** Scientist Agent
**Status:** Complete
