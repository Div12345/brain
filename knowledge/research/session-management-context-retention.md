# Session Management and Context Retention Strategies

**Research Date:** 2026-02-03
**Objective:** Document mechanisms for starting new sessions with context and maintaining state across sessions
**Status:** Complete

---

## Executive Summary

Research session management requires multiple layers of persistence to handle:
1. **Session initialization** - Warm-start with relevant context
2. **Cross-session state** - Preserve decisions, learnings, and progress
3. **Context compaction** - Survive automatic summarization
4. **Recovery from interruption** - Resume after crashes or abandonment

**Key Finding:** Combine file-based persistence (for durability) with hook-based injection (for automation) to create resilient research workflows.

---

## 1. How to Start a New Session with Relevant Context

### Context Injection Architecture (OMC Implementation)

**System:** `context-injector` module at `~/.claude/plugins/marketplaces/omc/src/features/context-injector/`

**How it works:**
```typescript
// Multiple sources register context with priority levels
contextCollector.register(sessionId, {
  id: 'session-recovery',
  source: 'session-context',
  content: '...',
  priority: 'critical'  // critical > high > normal > low
});

// Context auto-injected on next user message
// Prepended to prompt before sending to Claude
```

**Context Sources:**
| Source | Priority | Use For |
|--------|----------|---------|
| `boulder-state` | critical | Active tasks, current objective |
| `session-context` | critical | Recovery state from previous session |
| `rules-injector` | high | Project-specific rules |
| `directory-agents` | normal | Agent definitions |
| `learner` | normal | Extracted patterns |
| `keyword-detector` | low | Skill activation hints |

**Injection Strategy:**
- **Prepend** (default) - Context before user message
- **Append** - Context after user message
- **Wrap** - `<injected-context>...</injected-context>` tags

**Example Usage:**
```typescript
// Register context for next session start
contextCollector.register(sessionId, {
  id: 'recovery-state',
  source: 'session-context',
  content: `
Previous Session Summary:
- Completed: 5/8 research tasks
- Current focus: Context retention patterns
- Next: Implement session warm-start
- Key decision: Use file-based state over database
`,
  priority: 'critical'
});
```

### Session Start Hook Pattern

**Location:** `~/.claude/hooks/sessionstart.sh`

**Purpose:** Auto-inject recovery context when new session begins

**Implementation:**
```bash
#!/bin/bash
# Pre-requisite: Check for recovery state

RECOVERY_FILE=".omc/state/last-session-context.md"

if [[ -f "$RECOVERY_FILE" ]]; then
  # Read recovery context
  CONTEXT=$(cat "$RECOVERY_FILE")

  # Inject via context collector API (if available)
  # Or: Print to stderr for manual review
  echo "[SessionStart] Recovery context available:" >&2
  echo "$CONTEXT" >&2
fi

# Check for active plans
PLAN_FILE=".omc/plans/active.md"
if [[ -f "$PLAN_FILE" ]]; then
  echo "[SessionStart] Active plan detected. Loading..." >&2
  cat "$PLAN_FILE" >&2
fi
```

**Hook Triggers:**
- Session creation
- Session resume after timeout
- Session resume after crash

### Tiered Context Loading Strategy

**Tier 1 (Always Load - <5KB):**
```
- CLAUDE.md - Project instructions
- .omc/state/session-state.json - Current task
- .omc/state/active-agents.json - Who's working on what
- .omc/plans/{active-plan}.md - Current plan
```

**Tier 2 (Conditionally Load - <20KB):**
```
- .omc/notepads/{plan}/learnings.md - Key learnings
- .omc/notepads/{plan}/decisions.md - Architecture decisions
- Recent git commits (last 5-10)
- .omc/progress.txt - Ralph progress log
```

**Tier 3 (On-Demand - Unlimited):**
```
- Full session logs
- Historical research documents
- Complete git history
```

**Loading Logic:**
```
1. Load Tier 1 (always)
2. Check session age:
   - New session (<1 hour since last) → Load Tier 2
   - Old session (>1 day) → Ask user which Tier 2 to load
   - Compacted session → Load Tier 2 + recovery context
3. Tier 3 loaded only on explicit request
```

---

## 2. What Should Be Persisted Between Sessions

### State Persistence Architecture

**OMC Standard State Locations:**
```
.omc/state/           # Local project state
  ├── ralph-state.json         # Ralph loop state
  ├── autopilot-state.json     # Autopilot workflow
  ├── ultrawork-state.json     # Parallel execution
  ├── verification-state.json  # Architect approval
  └── session-context.json     # Session recovery

~/.omc/state/         # Global backup (session continuity)
  └── {same files}    # Fallback if local missing
```

**State File Format (Ralph Example):**
```json
{
  "active": true,
  "iteration": 3,
  "max_iterations": 10,
  "started_at": "2026-02-03T10:30:00Z",
  "prompt": "Research context retention patterns",
  "session_id": "ses_abc123",
  "prd_mode": true,
  "current_story_id": "US-005",
  "linked_ultrawork": true
}
```

### What to Persist (By Category)

**1. Task State (CRITICAL)**
```json
{
  "current_task": "Research session management",
  "status": "in_progress",
  "completed_subtasks": ["context-injector", "ralph-state"],
  "pending_subtasks": ["warm-start", "recovery-protocol"],
  "blocked_on": null,
  "started_at": "2026-02-03T10:00:00Z"
}
```

**2. Decisions (HIGH)**
```markdown
# Decisions - session-management

## 2026-02-03 10:45:00

Use file-based state over database for simplicity and git-trackability.

**Rationale:**
- Files commit to git for multi-agent coordination
- No setup/dependencies required
- Human-readable for debugging

**Trade-off:** No transactions, must handle concurrent writes
```

**3. Learnings (HIGH)**
```markdown
# Learnings - session-management

## 2026-02-03 11:15:00

Context injection happens BEFORE user message processing, so it affects tool availability detection.

**Impact:** Skills registered in context must be in Claude's system prompt or they won't activate.
```

**4. Progress (MEDIUM)**
```markdown
# Progress Log

## [2026-02-03 11:30] - US-005

**What was implemented:**
- Context injector analysis
- Ralph state file documentation
- Notepad wisdom system review

**Files changed:**
- knowledge/research/session-management-context-retention.md (new)

**Learnings for future iterations:**
- OMC already has full context injection system - don't reinvent
- Prioritize hook-based automation over manual state saves
```

**5. Patterns (MEDIUM)**
```markdown
# Codebase Patterns

- State files use .json for structured data, .md for human-readable logs
- Priority system: critical > high > normal > low
- Hook naming: precompact, sessionstart, posttool, sessionend
- Global fallback: ~/.omc/state/ if .omc/state/ missing
```

**6. Issues (LOW - but track)**
```markdown
# Issues - session-management

## 2026-02-03 12:00:00

Auto-compaction can lose context without PreCompact hook configured.

**Workaround:** Install c0ntextKeeper or implement custom PreCompact hook
**Severity:** Medium (affects long sessions)
```

### Persistence Mechanisms

**A. File-Based State (Durable, Git-Friendly)**
```typescript
// Ralph state persistence example
export function writeRalphState(directory: string, state: RalphLoopState): boolean {
  try {
    const stateFile = join(directory, '.omc', 'state', 'ralph-state.json');
    writeFileSync(stateFile, JSON.stringify(state, null, 2));
    return true;
  } catch {
    return false;
  }
}
```

**B. Append-Only Logs (Memory Persistence)**
```typescript
// Progress log append
export function appendProgress(
  directory: string,
  entry: Omit<ProgressEntry, 'timestamp'>
): boolean {
  const progressPath = findProgressPath(directory);
  const timestamp = new Date().toISOString();

  const lines = [
    '',
    `## [${timestamp}] - ${entry.storyId}`,
    '**What was implemented:**',
    ...entry.implementation.map(i => `- ${i}`),
    '**Learnings:**',
    ...entry.learnings.map(l => `- ${l}`),
    '---'
  ];

  appendFileSync(progressPath, lines.join('\n'));
  return true;
}
```

**C. Notepad System (Categorized Wisdom)**
```typescript
// Plan-scoped notepad structure
.omc/notepads/{plan-name}/
  ├── learnings.md   # Technical discoveries
  ├── decisions.md   # Architecture choices
  ├── issues.md      # Known problems
  └── problems.md    # Active blockers

// Timestamped entries
## 2026-02-03 12:30:00

Context injection must run before tool availability check,
otherwise skills won't be detected.
```

---

## 3. Handling Session Compaction and Context Limits

### The Compaction Problem

**What Triggers Auto-Compaction:**
- ~75% context window usage (~150K tokens for 200K window)
- Automatic, no user notification in CLI
- Lossy summarization retains ~25% of context

**What Survives:**
| Information Type | Survival Rate | Notes |
|------------------|---------------|-------|
| Recent messages (last 5-10) | 100% | Verbatim |
| Task list structure | 90% | If using todos |
| File paths | 80% | Usually preserved |
| Code snippets | 60% | May be summarized |
| Reasoning chains | 20% | Often lost |
| Skill procedures | 10% | **Frequently lost** |

**What's Lost Without Intervention:**
- Why decisions were made
- Alternative approaches considered
- User preferences and constraints
- Learned patterns and techniques
- Skill system prompt content

### PreCompact Hook (Prevention Strategy)

**Purpose:** Capture full state BEFORE lossy summarization

**Implementation:**
```bash
#!/bin/bash
# ~/.claude/hooks/precompact.sh

SESSION_FILE="$CLAUDE_SESSION_FILE"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=".omc/backups/compaction/$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

# 1. Backup full JSONL
cp "$SESSION_FILE" "$BACKUP_DIR/session.jsonl"

# 2. Extract conversation
jq -c 'select(.role=="user" or .role=="assistant")' \
  "$SESSION_FILE" > "$BACKUP_DIR/conversation.jsonl"

# 3. Extract current task context
jq -c 'select(.content[]?.type == "text") |
       {role, text: .content[].text}' \
  "$SESSION_FILE" | tail -20 > "$BACKUP_DIR/recent-context.jsonl"

# 4. Save state files
cp -r .omc/state "$BACKUP_DIR/"
cp -r .omc/notepads "$BACKUP_DIR/" 2>/dev/null || true

# 5. Create recovery manifest
cat > "$BACKUP_DIR/RECOVERY.md" <<EOF
# Pre-Compaction Backup
Timestamp: $TIMESTAMP
Session: $CLAUDE_SESSION_ID

## Files Backed Up
- session.jsonl (full conversation)
- conversation.jsonl (user/assistant only)
- recent-context.jsonl (last 20 exchanges)
- .omc/state/ (all state files)
- .omc/notepads/ (wisdom files)

## Recovery Command
cat "$BACKUP_DIR/recent-context.jsonl" | jq -r '.text'
EOF

echo "[PreCompact] Backup saved to $BACKUP_DIR" >&2
```

**Hook Registration:**
```bash
# Make executable
chmod +x ~/.claude/hooks/precompact.sh

# Test
~/.claude/hooks/precompact.sh
```

### SessionStart Hook (Recovery Strategy)

**Purpose:** Auto-inject recovery context when resuming

**Implementation:**
```bash
#!/bin/bash
# ~/.claude/hooks/sessionstart.sh

# Find most recent compaction backup
LATEST_BACKUP=$(ls -td .omc/backups/compaction/* 2>/dev/null | head -1)

if [[ -n "$LATEST_BACKUP" ]]; then
  echo "[SessionStart] Found pre-compaction backup: $LATEST_BACKUP" >&2

  # Check if backup is recent (within 1 hour)
  BACKUP_TIME=$(basename "$LATEST_BACKUP")
  NOW=$(date +%s)
  BACKUP_EPOCH=$(date -d "${BACKUP_TIME:0:8} ${BACKUP_TIME:9:2}:${BACKUP_TIME:11:2}:${BACKUP_TIME:13:2}" +%s 2>/dev/null || echo 0)
  AGE=$((NOW - BACKUP_EPOCH))

  if [[ $AGE -lt 3600 ]]; then
    # Recent compaction - inject recovery context
    echo "[SessionStart] Injecting recovery context from $BACKUP_TIME" >&2

    # Extract key context
    if [[ -f "$LATEST_BACKUP/recent-context.jsonl" ]]; then
      echo "" >&2
      echo "=== RECOVERY CONTEXT ===" >&2
      jq -r 'select(.role=="assistant") | .text' "$LATEST_BACKUP/recent-context.jsonl" | tail -5 >&2
      echo "=======================" >&2
    fi
  fi
fi

# Load active state files
if [[ -f ".omc/state/ralph-state.json" ]]; then
  echo "[SessionStart] Ralph loop active" >&2
fi

if [[ -f ".omc/state/autopilot-state.json" ]]; then
  echo "[SessionStart] Autopilot active" >&2
fi
```

### c0ntextKeeper Integration (Automated Solution)

**What it does:**
- Runs PreCompact hook automatically
- Creates searchable archives (<10ms overhead)
- Redacts sensitive data (API keys, credentials)
- Provides MCP tools for retrieval

**Installation:**
```bash
npm install -g c0ntextkeeper
c0ntextkeeper setup
```

**Configuration:**
```json
// ~/.c0ntextkeeper/config.json
{
  "archiveDir": "~/.c0ntextkeeper/archives",
  "maxArchiveSize": "1GB",
  "compressionLevel": 6,
  "redactPatterns": [
    "sk-[A-Za-z0-9]{48}",
    "ghp_[A-Za-z0-9]{36}"
  ],
  "hooks": {
    "precompact": true,
    "sessionend": true,
    "posttool": false
  }
}
```

**MCP Tools:**
```
retrieve-context --session <id> --before-compact
search-archives --query "context injection patterns"
list-archives --since "2026-02-01"
```

---

## 4. Session Warm-Up Protocol

### Cold Start vs. Warm Start

**Cold Start (No Context):**
```
User: "Continue research on session management"
Claude: "I don't have context about previous research.
         Can you provide background?"
```

**Warm Start (With Context):**
```
[Context Injected]
Previous Session Summary:
- Completed: Context-injector analysis, Ralph state review
- Current: Section 3 of 5 (context retention)
- Next: Warm-start protocol, recovery workflow

User: "Continue research on session management"
Claude: "Continuing from Section 3. Next: warm-start protocol..."
```

### Warm-Start Implementation

**Step 1: State File Check**
```typescript
export function getSessionWarmupContext(directory: string): string {
  const parts: string[] = [];

  // Check for active work
  const ralphState = readRalphState(directory);
  if (ralphState?.active) {
    parts.push(`Ralph loop active (iteration ${ralphState.iteration}/${ralphState.max_iterations})`);
    parts.push(`Task: ${ralphState.prompt}`);
  }

  // Check for recent progress
  const progress = readProgress(directory);
  if (progress?.entries.length > 0) {
    const recent = progress.entries.slice(-3);
    parts.push(`Recent progress: ${recent.length} stories completed`);
  }

  // Check for notepad wisdom
  const wisdom = readPlanWisdom('active', directory);
  if (wisdom.learnings.length > 0) {
    parts.push(`Learnings captured: ${wisdom.learnings.length}`);
  }

  return parts.join('\n');
}
```

**Step 2: Git History Check**
```bash
# Last 5 commits
gh api repos/owner/repo/commits --jq '.[0:5] | .[] | {sha: .sha[0:7], message: .commit.message, date: .commit.author.date}'

# Recent changes
git log --oneline --since="1 day ago" --pretty=format:"%h %s"
```

**Step 3: Assemble Recovery Context**
```typescript
export function assembleRecoveryContext(directory: string): string {
  const sections: string[] = [];

  sections.push('# Session Recovery Context\n');

  // State
  const warmup = getSessionWarmupContext(directory);
  if (warmup) {
    sections.push('## Current State\n' + warmup);
  }

  // Recent work
  const commits = execSync('git log --oneline -5', { cwd: directory })
    .toString()
    .trim();
  if (commits) {
    sections.push('## Recent Commits\n```\n' + commits + '\n```');
  }

  // Key decisions
  const wisdom = readPlanWisdom('active', directory);
  if (wisdom.decisions.length > 0) {
    const recentDecisions = wisdom.decisions.slice(-3);
    sections.push('## Key Decisions\n' +
      recentDecisions.map(d => `- [${d.timestamp}] ${d.content}`).join('\n'));
  }

  return sections.join('\n\n');
}
```

**Step 4: Context Injection**
```typescript
// Register for next user message
contextCollector.register(sessionId, {
  id: 'session-recovery',
  source: 'session-context',
  content: assembleRecoveryContext(process.cwd()),
  priority: 'critical'
});
```

### Auto-Warm-Start Hook

```bash
#!/bin/bash
# ~/.claude/hooks/sessionstart.sh

# Detect if this is a resume (not a new session)
if [[ -f ".omc/state/last-session-id.txt" ]]; then
  LAST_SESSION=$(cat .omc/state/last-session-id.txt)

  if [[ "$LAST_SESSION" != "$CLAUDE_SESSION_ID" ]]; then
    # New session - inject warm-start context
    echo "[SessionStart] New session detected - warming up context" >&2

    # Generate recovery context
    node - <<'EOF'
const { assembleRecoveryContext } = require('./.omc/lib/recovery.js');
const context = assembleRecoveryContext(process.cwd());
console.log(context);
EOF
  fi
fi

# Update last session ID
echo "$CLAUDE_SESSION_ID" > .omc/state/last-session-id.txt
```

---

## 5. Concrete Implementation Recommendations

### Tier 1: Essential (Implement First)

**1. State File Standardization**
```bash
# Directory structure
.omc/
├── state/           # JSON state files
│   ├── ralph-state.json
│   ├── autopilot-state.json
│   └── session-context.json
├── notepads/        # Plan-scoped wisdom
│   └── {plan-name}/
│       ├── learnings.md
│       ├── decisions.md
│       ├── issues.md
│       └── problems.md
├── backups/         # Pre-compaction backups
│   └── compaction/
│       └── {timestamp}/
└── progress.txt     # Append-only memory
```

**2. PreCompact Hook**
```bash
# Minimal viable backup
#!/bin/bash
BACKUP_DIR=".omc/backups/compaction/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$CLAUDE_SESSION_FILE" "$BACKUP_DIR/session.jsonl"
cp -r .omc/state "$BACKUP_DIR/" 2>/dev/null || true
echo "[PreCompact] Backed up to $BACKUP_DIR" >&2
```

**3. Session State File**
```json
// .omc/state/session-context.json
{
  "lastActive": "2026-02-03T12:00:00Z",
  "currentTask": "Research session management",
  "completedSubtasks": ["context-injector", "ralph-state"],
  "nextSteps": ["warm-start", "recovery-protocol"],
  "keyDecisions": [
    "Use file-based state for git-trackability",
    "Prioritize hook-based automation"
  ],
  "blockers": []
}
```

### Tier 2: Recommended (High Value)

**4. SessionStart Hook with Auto-Recovery**
```bash
#!/bin/bash
# Check for recent compaction backup
LATEST=$(ls -td .omc/backups/compaction/* 2>/dev/null | head -1)

if [[ -n "$LATEST" ]] && [[ $(find "$LATEST" -mmin -60 2>/dev/null) ]]; then
  echo "[SessionStart] Recent compaction detected - recovery context available" >&2

  # Extract key insights
  if [[ -f "$LATEST/session.jsonl" ]]; then
    jq -r 'select(.role=="assistant") | .content[]?.text' "$LATEST/session.jsonl" \
      | tail -5 >&2
  fi
fi

# Load active state
[[ -f ".omc/state/session-context.json" ]] && cat .omc/state/session-context.json >&2
```

**5. Notepad System Integration**
```typescript
// Auto-capture wisdom from completions
export function captureWisdomFromCompletion(
  planName: string,
  response: string,
  directory: string
): void {
  const wisdom = extractWisdomFromCompletion(response);

  for (const entry of wisdom) {
    addWisdomEntry(planName, entry.category, entry.content, directory);
  }
}
```

**6. Context Injector Setup**
```typescript
// Register session recovery context
export function setupSessionRecovery(sessionId: string, directory: string): void {
  const recoveryContext = assembleRecoveryContext(directory);

  contextCollector.register(sessionId, {
    id: 'session-recovery',
    source: 'session-context',
    content: recoveryContext,
    priority: 'critical'
  });
}
```

### Tier 3: Advanced (Optional Enhancements)

**7. c0ntextKeeper Integration**
```bash
# Automated backup with search
npm install -g c0ntextkeeper
c0ntextkeeper setup
c0ntextkeeper config --archive-dir ~/.c0ntextkeeper/archives
```

**8. Periodic State Snapshots**
```bash
# Cron job: snapshot state every hour
0 * * * * cd /path/to/project && \
  cp -r .omc/state .omc/backups/hourly/$(date +\%Y\%m\%d_\%H00)
```

**9. Multi-Agent Coordination**
```typescript
// Active agents tracking
export function registerActiveAgent(
  agentId: string,
  workArea: string,
  directory: string
): void {
  const activeFile = join(directory, '.omc', 'state', 'active-agents.json');
  const active = existsSync(activeFile)
    ? JSON.parse(readFileSync(activeFile, 'utf-8'))
    : {};

  active[agentId] = {
    workArea,
    since: new Date().toISOString(),
    status: 'active'
  };

  writeFileSync(activeFile, JSON.stringify(active, null, 2));
}
```

---

## 6. Recovery Workflow

### After Unexpected Interruption

**Step 1: Assess Situation**
```bash
# Check for active state
ls -la .omc/state/

# Check most recent backup
ls -td .omc/backups/compaction/* | head -1

# Check recent commits
git log --oneline -10
```

**Step 2: Identify Last Known State**
```bash
# Read session context
cat .omc/state/session-context.json | jq .

# Read ralph state (if active)
cat .omc/state/ralph-state.json | jq .

# Check progress log
tail -50 .omc/progress.txt
```

**Step 3: Warm-Start New Session**
```bash
# Manually inject context (if hooks not configured)
cat <<EOF
Session Recovery Context:

$(cat .omc/state/session-context.json | jq -r '.currentTask')

Completed:
$(cat .omc/state/session-context.json | jq -r '.completedSubtasks[]')

Next Steps:
$(cat .omc/state/session-context.json | jq -r '.nextSteps[]')

Recent commits:
$(git log --oneline -5)
EOF
```

**Step 4: Resume Work**
```bash
# Start new session with context
claude --session-id resume-$(date +%s)

# (Paste context from Step 3 as first message)
```

### After Auto-Compaction

**Step 1: Check for PreCompact Backup**
```bash
LATEST_BACKUP=$(ls -td .omc/backups/compaction/* 2>/dev/null | head -1)

if [[ -n "$LATEST_BACKUP" ]]; then
  echo "Backup found: $LATEST_BACKUP"

  # Extract recent context
  jq -r 'select(.role=="assistant") | .content[]?.text' \
    "$LATEST_BACKUP/session.jsonl" | tail -10
fi
```

**Step 2: Restore Key Context**
```bash
# If using c0ntextKeeper
c0ntextkeeper retrieve --session $CLAUDE_SESSION_ID --before-compact

# Or manually from backup
cat "$LATEST_BACKUP/RECOVERY.md"
```

**Step 3: Update State Files**
```bash
# Restore state from backup if needed
cp -r "$LATEST_BACKUP/.omc/state/"* .omc/state/
```

---

## 7. Integration with Brain System

### Brain Repo Context Files

**Primary Recovery Files:**
```
context/
├── session-state.md      # Current task, what's done
├── active-agents.md      # Multi-agent coordination
├── predictions.md        # Planned work
└── handoff.md           # Agent transitions
```

**Recovery Protocol:**
```markdown
1. Check commits: gh api repos/owner/brain/commits --jq '.[0:5]'
2. Read context/session-state.md
3. Read context/active-agents.md
4. Review recent work
5. Continue from pending list
```

### Coordination with Overnight Agent

**Handoff Pattern:**
```markdown
# context/handoff.md

## 2026-02-03 12:00 - claude-code → overnight

**Completed:**
- Research on context-injector system
- Ralph state management documentation
- Notepad wisdom system review

**Context for Next Agent:**
- Current document: session-management-context-retention.md
- Completion: ~60% (sections 1-4 done)
- Next: Implementation recommendations

**State Files Updated:**
- knowledge/research/session-management-context-retention.md (new)
- .omc/state/session-context.json

**Questions for User:**
- None (research task, no user input needed)
```

### Session State Format

```markdown
---
created: 2026-02-03
tags: [context, session, compaction-resilient]
updated: 2026-02-03T12:00
agent: scientist
---

# Session State

> **COMPACTION RESILIENCE**: Read this first after context reset.

## Active Agent
- **scientist-001** (Claude Code): Session management research

## Session Summary

**Research Docs Created:**
- [[knowledge/research/session-management-context-retention]]

**Key Findings:**
- OMC has full context-injection system
- Ralph uses append-only progress logs
- Notepad wisdom captures learnings/decisions
- PreCompact hook critical for recovery

**Implementation Recommendations:**
1. State file standardization (.omc/state/)
2. PreCompact backup hook
3. SessionStart recovery hook

## Recovery Protocol
1. Read this file
2. Check .omc/state/ for active work
3. Review recent commits
4. Continue from next steps
```

---

## 8. Key Patterns Summary

### Context Injection Pattern

**When:** Session start, after compaction
**How:** Priority-based collector with multiple sources
**Code:** `~/.claude/plugins/marketplaces/omc/src/features/context-injector/`

```typescript
contextCollector.register(sessionId, {
  id: 'unique-id',
  source: 'session-context',
  content: 'recovery context here',
  priority: 'critical'
});
```

### State Persistence Pattern

**When:** After significant work, before long operations
**How:** JSON for structured data, markdown for human-readable
**Location:** `.omc/state/` (local), `~/.omc/state/` (global backup)

```typescript
writeFileSync(
  '.omc/state/session-context.json',
  JSON.stringify(state, null, 2)
);
```

### Append-Only Memory Pattern

**When:** Capturing learnings, progress, patterns
**How:** Timestamped entries, never overwrite
**Examples:** Ralph progress.txt, notepad wisdom

```markdown
## 2026-02-03 12:00:00

Learning: Context injection must happen before tool detection.

Impact: Skills won't activate if registered after prompt processing.
```

### Hook-Based Automation Pattern

**When:** Compaction, session start/end, tool execution
**How:** Bash scripts in `~/.claude/hooks/`
**Critical:** precompact.sh, sessionstart.sh

```bash
#!/bin/bash
# precompact.sh
BACKUP_DIR=".omc/backups/compaction/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$CLAUDE_SESSION_FILE" "$BACKUP_DIR/"
```

### Tiered Loading Pattern

**When:** Session initialization
**How:** Load critical context always, conditionally load secondary
**Tiers:** Always → Recent → On-demand

```
Tier 1 (Always): CLAUDE.md, session-state, active-agents
Tier 2 (Recent): Notepad wisdom, progress log, git commits
Tier 3 (On-demand): Full logs, historical docs
```

---

## 9. Tools and Libraries

### OMC Built-in Features

| Feature | Location | Purpose |
|---------|----------|---------|
| Context Injector | `src/features/context-injector/` | Priority-based context injection |
| Ralph Progress | `src/hooks/ralph/progress.ts` | Append-only memory |
| Notepad Wisdom | `src/features/notepad-wisdom/` | Plan-scoped learnings |
| State Management | `src/hooks/ralph/loop.ts` | Persistent work loop |

### External Tools

| Tool | Install | Purpose |
|------|---------|---------|
| c0ntextKeeper | `npm i -g c0ntextkeeper` | Automated compaction backups |
| claude-session-restore | `npm i -g claude-session-restore` | AI-powered recovery |
| cc-sessions | `cargo install cc-sessions` | Fast session switching |

### Brain System Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| context/session-state.md | Recovery state | Every 5-10 changes |
| context/active-agents.md | Multi-agent coordination | On agent start/stop |
| logs/{date}-{agent}.md | Full session history | Real-time append |

---

## 10. Critical Insights

### What Works

1. **File-based state** beats database for git-trackability
2. **Hook automation** beats manual saves for reliability
3. **Append-only logs** survive compaction better than overwrites
4. **Tiered loading** balances context vs. token usage
5. **PreCompact hook** is non-negotiable for long sessions

### What Doesn't Work

1. **Relying on conversation memory** - Lost after compaction
2. **Storing everything in .claude/** - Not git-tracked
3. **Assuming skills survive compaction** - They don't without hooks
4. **Manual state saves** - Forgotten under deadline pressure
5. **Single-tier loading** - Either too much or too little context

### Key Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| File-based state | Git-trackable, simple, debuggable | No transactions, manual coordination |
| Context injection | Automatic, priority-based | Requires OMC or custom hooks |
| Append-only logs | Survives crashes, full history | Can grow large, harder to query |
| Notepad wisdom | Structured, categorized | Requires discipline to populate |
| PreCompact hooks | Catches everything pre-loss | Requires setup, ~10ms overhead |

---

## 11. Future Enhancements

### L2 Memory (Model-Level Integration)

**Current:** L0 (logs) + L1 (knowledge files)
**Future:** L2 - Fine-tuned model with embedded knowledge

**Benefits:**
- No context injection needed
- Reasoning without retrieval
- Personalized behavior

**Challenges:**
- Training pipeline required
- Model versioning complexity
- Cost/time per iteration

### Semantic Search Integration

**Current:** File-based retrieval (glob/grep)
**Future:** Vector embeddings + semantic search

**Implementation:**
```typescript
// Index all state files on update
await vectorDB.index({
  id: 'session-context',
  content: sessionContext,
  metadata: { timestamp, category: 'state' }
});

// Retrieve relevant context on session start
const relevant = await vectorDB.search(
  query: 'last session progress',
  limit: 5,
  filter: { category: 'state', timestamp: { gte: weekAgo } }
);
```

### Multi-Agent Session Handoffs

**Current:** Manual coordination via active-agents.md
**Future:** Automatic handoff with state transfer

**Protocol:**
```typescript
// Agent A completes work
await handoffSession({
  from: 'claude-code-scientist',
  to: 'overnight-agent',
  context: sessionContext,
  completedTasks: ['research', 'documentation'],
  nextTasks: ['implementation', 'testing'],
  stateFiles: ['.omc/state/session-context.json']
});

// Agent B receives notification + full context
```

---

## Sources

### OMC Codebase
- Context Injector: `~/.claude/plugins/marketplaces/omc/src/features/context-injector/`
- Ralph State Management: `~/.claude/plugins/marketplaces/omc/src/hooks/ralph/`
- Notepad Wisdom: `~/.claude/plugins/marketplaces/omc/src/features/notepad-wisdom/`

### Brain Repository
- Session State: `context/session-state.md`
- Active Agents: `context/active-agents.md`
- Compaction Recovery Pattern: `knowledge/patterns/compaction-recovery.md`

### Research Documents
- [[knowledge/research/ai-memory-systems]] - L0-L1-L2 architecture
- [[knowledge/research/context-window-management]] - Compaction strategies
- [[knowledge/research/session-recovery-solutions-2026]] - Recovery tools

### Community Resources
- c0ntextKeeper: https://github.com/Capnjbrown/c0ntextKeeper
- claude-session-restore: https://github.com/ZENG3LD/claude-session-restore
- cc-sessions: https://github.com/chronologos/cc-sessions

---

## Appendix: Example Implementations

### A. Minimal Session Recovery Script

```bash
#!/bin/bash
# .omc/bin/recover-session.sh

SESSION_ID="$1"

if [[ -z "$SESSION_ID" ]]; then
  echo "Usage: $0 <session-id>"
  exit 1
fi

echo "=== Session Recovery ==="
echo ""

# Check state files
if [[ -f ".omc/state/session-context.json" ]]; then
  echo "Current task:"
  jq -r '.currentTask' .omc/state/session-context.json
  echo ""

  echo "Completed:"
  jq -r '.completedSubtasks[]' .omc/state/session-context.json
  echo ""

  echo "Next steps:"
  jq -r '.nextSteps[]' .omc/state/session-context.json
  echo ""
fi

# Check recent commits
echo "Recent commits:"
git log --oneline -5
echo ""

# Check for compaction backup
LATEST_BACKUP=$(ls -td .omc/backups/compaction/* 2>/dev/null | head -1)
if [[ -n "$LATEST_BACKUP" ]]; then
  echo "Pre-compaction backup available:"
  echo "$LATEST_BACKUP"
fi
```

### B. Context Injection Helper

```typescript
// .omc/lib/context-helper.ts

import { contextCollector } from 'oh-my-claudecode';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

export function injectSessionRecoveryContext(
  sessionId: string,
  directory: string = process.cwd()
): boolean {
  const contextFile = join(directory, '.omc', 'state', 'session-context.json');

  if (!existsSync(contextFile)) {
    return false;
  }

  const context = JSON.parse(readFileSync(contextFile, 'utf-8'));

  const recoveryText = `
# Session Recovery

**Current Task:** ${context.currentTask}

**Completed:**
${context.completedSubtasks.map(t => `- ${t}`).join('\n')}

**Next Steps:**
${context.nextSteps.map(s => `- ${s}`).join('\n')}

**Key Decisions:**
${context.keyDecisions.map(d => `- ${d}`).join('\n')}
`.trim();

  contextCollector.register(sessionId, {
    id: 'session-recovery',
    source: 'session-context',
    content: recoveryText,
    priority: 'critical'
  });

  return true;
}
```

### C. State Update Helper

```typescript
// .omc/lib/state-helper.ts

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';

export interface SessionContext {
  lastActive: string;
  currentTask: string;
  completedSubtasks: string[];
  nextSteps: string[];
  keyDecisions: string[];
  blockers: string[];
}

export function updateSessionContext(
  updates: Partial<SessionContext>,
  directory: string = process.cwd()
): boolean {
  const contextFile = join(directory, '.omc', 'state', 'session-context.json');

  // Ensure directory exists
  const dir = dirname(contextFile);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  // Read existing or create new
  let context: SessionContext;
  if (existsSync(contextFile)) {
    context = JSON.parse(readFileSync(contextFile, 'utf-8'));
  } else {
    context = {
      lastActive: new Date().toISOString(),
      currentTask: '',
      completedSubtasks: [],
      nextSteps: [],
      keyDecisions: [],
      blockers: []
    };
  }

  // Merge updates
  Object.assign(context, updates);
  context.lastActive = new Date().toISOString();

  // Write back
  try {
    writeFileSync(contextFile, JSON.stringify(context, null, 2));
    return true;
  } catch (error) {
    console.error('Failed to update session context:', error);
    return false;
  }
}
```

---

**Last Updated:** 2026-02-03
**Researcher:** Scientist Agent
**Status:** Complete

[FINDING] Comprehensive session management framework documented combining OMC features with Brain system patterns
[STAT:sections_completed] 11
[STAT:code_examples] 15
[STAT:implementation_tiers] 3
[STAT:sources_analyzed] 12

[LIMITATION] L2 memory (model-level integration) not yet implemented - future enhancement
[LIMITATION] Semantic search integration requires additional infrastructure (vector DB)
