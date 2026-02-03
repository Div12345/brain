---
created: 2026-02-03
tags:
  - patterns
  - session-management
  - context-retention
  - recovery
status: active
agent: scientist
---

# Session Management Patterns

Quick reference for session management and context retention patterns.

> **See also:** [[knowledge/research/session-management-context-retention]] for full documentation

---

## Pattern 1: Context Injection (Priority-Based)

**Problem:** New sessions lack context from previous work

**Solution:** Priority-based collector registers context from multiple sources

**Implementation:**
```typescript
contextCollector.register(sessionId, {
  id: 'session-recovery',
  source: 'session-context',
  content: recoveryContext,
  priority: 'critical'  // critical > high > normal > low
});
```

**When to use:** Session start, after compaction, agent handoffs

**OMC Location:** `~/.claude/plugins/marketplaces/omc/src/features/context-injector/`

---

## Pattern 2: State Persistence (File-Based)

**Problem:** State lost between sessions or after crashes

**Solution:** JSON files for structured data, markdown for human-readable logs

**Directory Structure:**
```
.omc/
├── state/           # Structured state (JSON)
│   ├── ralph-state.json
│   ├── autopilot-state.json
│   └── session-context.json
├── notepads/        # Human-readable wisdom (markdown)
│   └── {plan-name}/
│       ├── learnings.md
│       ├── decisions.md
│       ├── issues.md
│       └── problems.md
└── backups/         # Pre-compaction backups
    └── compaction/{timestamp}/
```

**When to use:** After significant work, before long operations, at session end

**Why files over DB:** Git-trackable, no dependencies, human-debuggable

---

## Pattern 3: Append-Only Memory

**Problem:** Context compaction loses reasoning and learnings

**Solution:** Timestamped entries that never overwrite, survive compaction

**Format:**
```markdown
## 2026-02-03 12:30:00

Context injection must run before tool availability check,
otherwise skills won't be detected.

**Impact:** Skills registered in context won't activate if registered after prompt processing.
```

**Examples:**
- Ralph progress.txt - work history
- Notepad wisdom files - learnings/decisions/issues
- Session logs - full interaction history

**When to use:** Capturing insights, tracking progress, documenting decisions

**OMC Location:** `~/.claude/plugins/marketplaces/omc/src/hooks/ralph/progress.ts`

---

## Pattern 4: Hook-Based Automation

**Problem:** Manual state saves forgotten under pressure

**Solution:** Bash hooks triggered automatically by Claude Code lifecycle events

**Critical Hooks:**

### PreCompact Hook
```bash
#!/bin/bash
# ~/.claude/hooks/precompact.sh
BACKUP_DIR=".omc/backups/compaction/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$CLAUDE_SESSION_FILE" "$BACKUP_DIR/session.jsonl"
cp -r .omc/state "$BACKUP_DIR/" 2>/dev/null || true
echo "[PreCompact] Backed up to $BACKUP_DIR" >&2
```

### SessionStart Hook
```bash
#!/bin/bash
# ~/.claude/hooks/sessionstart.sh
LATEST_BACKUP=$(ls -td .omc/backups/compaction/* 2>/dev/null | head -1)

if [[ -n "$LATEST_BACKUP" ]] && [[ $(find "$LATEST_BACKUP" -mmin -60 2>/dev/null) ]]; then
  echo "[SessionStart] Recent compaction - recovery context available" >&2
  jq -r 'select(.role=="assistant") | .content[]?.text' \
    "$LATEST_BACKUP/session.jsonl" | tail -5 >&2
fi
```

**When to use:** Always (set up once, runs automatically)

**Why critical:** PreCompact is only way to capture state before lossy summarization

---

## Pattern 5: Tiered Loading

**Problem:** Loading too much context wastes tokens, too little loses coherence

**Solution:** Load critical context always, secondary context conditionally

**Tiers:**

| Tier | Size | When Loaded | Contents |
|------|------|-------------|----------|
| **Tier 1** | <5KB | Always | CLAUDE.md, session-state, active-agents, current plan |
| **Tier 2** | <20KB | Recent sessions (<1 day) | Notepad wisdom, progress log, git commits (5-10) |
| **Tier 3** | Unlimited | On-demand only | Full logs, historical docs, complete git history |

**Loading Logic:**
```typescript
// Always load Tier 1
const tier1 = loadCriticalContext();

// Conditionally load Tier 2
const sessionAge = Date.now() - lastActiveTimestamp;
if (sessionAge < 24 * 60 * 60 * 1000) {  // < 1 day
  const tier2 = loadRecentContext();
}

// Tier 3 only on explicit request
// "Show me all logs from last week" → load tier3
```

**When to use:** Session initialization, after compaction

**Trade-off:** Context completeness vs. token efficiency

---

## Pattern 6: Session Warm-Up

**Problem:** Cold starts require re-explaining context

**Solution:** Auto-inject recovery context on session start

**Implementation Steps:**

1. **Assemble Recovery Context**
```typescript
function assembleRecoveryContext(directory: string): string {
  return [
    getCurrentTask(),
    getCompletedWork(),
    getRecentCommits(5),
    getKeyDecisions(3),
    getNextSteps()
  ].join('\n\n');
}
```

2. **Register for Injection**
```typescript
contextCollector.register(sessionId, {
  id: 'warm-start',
  source: 'session-context',
  content: assembleRecoveryContext(process.cwd()),
  priority: 'critical'
});
```

3. **Auto-Trigger via Hook**
```bash
# sessionstart.sh
if [[ -f ".omc/state/session-context.json" ]]; then
  node .omc/lib/warm-start.js
fi
```

**When to use:** New sessions, resume after timeout, post-compaction recovery

---

## Pattern 7: Multi-Agent Coordination

**Problem:** Multiple agents working concurrently need to avoid conflicts

**Solution:** Shared state file tracking who's working on what

**File:** `.omc/state/active-agents.json`
```json
{
  "claude-code-scientist": {
    "workArea": "knowledge/research/session-management-*",
    "since": "2026-02-03T10:00:00Z",
    "status": "active"
  },
  "overnight-agent": {
    "workArea": "tasks/pending/infrastructure-*",
    "since": "2026-02-03T09:00:00Z",
    "status": "active"
  }
}
```

**Protocol:**
1. Register on start: `registerActiveAgent(agentId, workArea)`
2. Check before claiming work: `isWorkAreaClaimed(pattern)`
3. Update on completion: `markWorkComplete(agentId, workArea)`
4. Clear on exit: `deregisterAgent(agentId)`

**When to use:** Multi-agent systems (Brain repo, ralph multi-instance)

---

## Pattern 8: Notepad Wisdom (Categorized Learning)

**Problem:** Learnings scattered across conversation, lost on compaction

**Solution:** Plan-scoped wisdom files with 4 categories

**Structure:**
```
.omc/notepads/{plan-name}/
├── learnings.md   # Technical discoveries, patterns found
├── decisions.md   # Architecture choices, trade-offs made
├── issues.md      # Known problems, workarounds needed
└── problems.md    # Active blockers, need resolution
```

**Entry Format:**
```markdown
## 2026-02-03 12:00:00

Context injection happens BEFORE tool detection.

**Implication:** Skills won't activate if registered after prompt processing.

**Solution:** Register skills in SessionStart hook, not in agent init.
```

**API:**
```typescript
// Add entries
addLearning(planName, 'Context injection runs before tool detection');
addDecision(planName, 'Use file-based state for git-trackability');
addIssue(planName, 'Auto-compaction loses skill system prompts');
addProblem(planName, 'Race condition in multi-agent file writes');

// Read all wisdom
const wisdom = readPlanWisdom(planName);

// Get summary
const summary = getWisdomSummary(planName);
```

**When to use:** Research tasks, complex implementations, multi-session work

**OMC Location:** `~/.claude/plugins/marketplaces/omc/src/features/notepad-wisdom/`

---

## Quick Start Checklist

### Essential Setup (5 minutes)

- [ ] Create `.omc/state/` directory
- [ ] Create PreCompact hook (`~/.claude/hooks/precompact.sh`)
- [ ] Create SessionStart hook (`~/.claude/hooks/sessionstart.sh`)
- [ ] Make hooks executable (`chmod +x ~/.claude/hooks/*.sh`)
- [ ] Create initial `session-context.json`

### Recommended Setup (10 minutes)

- [ ] Install c0ntextKeeper: `npm install -g c0ntextkeeper`
- [ ] Run setup: `c0ntextkeeper setup`
- [ ] Initialize notepad for current plan
- [ ] Configure active-agents tracking
- [ ] Test hooks: `~/.claude/hooks/precompact.sh`

### Advanced Setup (30 minutes)

- [ ] Set up periodic state snapshots (cron)
- [ ] Configure context collector integration
- [ ] Implement semantic search (if needed)
- [ ] Create custom recovery scripts
- [ ] Set up multi-agent coordination

---

## Common Pitfalls

### ❌ Anti-Pattern: Relying on Conversation Memory
**Problem:** Lost after compaction
**Solution:** Persist to state files instead

### ❌ Anti-Pattern: Storing State in `~/.claude/`
**Problem:** Not git-tracked, hard to coordinate multi-agent
**Solution:** Use `.omc/` for project state, `~/.omc/` for global backup

### ❌ Anti-Pattern: Manual State Saves
**Problem:** Forgotten under deadline pressure
**Solution:** Hook-based automation

### ❌ Anti-Pattern: Single-Tier Context Loading
**Problem:** Either too much (wastes tokens) or too little (loses context)
**Solution:** Tiered loading with conditional logic

### ❌ Anti-Pattern: Assuming Skills Survive Compaction
**Problem:** Skill system prompts often lost in summarization
**Solution:** PreCompact backup + SessionStart re-registration

---

## Decision Matrix

| Scenario | Recommended Pattern | Alternative |
|----------|-------------------|-------------|
| Session interrupted unexpectedly | PreCompact hook + file state | c0ntextKeeper |
| Starting new session next day | Tiered loading + warm-start | Manual context recap |
| Multiple agents on same project | Active-agents tracking | File locking |
| Long research task (>5 sessions) | Notepad wisdom + progress log | Session logs only |
| After auto-compaction | SessionStart recovery hook | claude-session-restore |
| Capturing learnings during work | Append-only notepad | Overwrite state file |
| Coordinating with overnight agent | Handoff protocol + state files | Slack/email |

---

## Metrics to Track

| Metric | How to Measure | Target |
|--------|---------------|--------|
| **Recovery Time** | Time to resume after interruption | <2 minutes |
| **Context Loss** | % of important info lost after compaction | <10% |
| **Token Efficiency** | Tokens used vs info retained | >80% efficiency |
| **Setup Overhead** | Time to configure hooks/state | <10 minutes |
| **Coordination Conflicts** | Multi-agent file conflicts per week | <1 per week |

---

## Related

- [[knowledge/research/session-management-context-retention]] - Full documentation
- [[knowledge/research/ai-memory-systems]] - L0-L1-L2 memory architecture
- [[knowledge/research/context-window-management]] - Compaction strategies
- [[knowledge/patterns/compaction-recovery]] - Recovery protocol
- [[context/session-state]] - Brain repo session state

---

**Last Updated:** 2026-02-03
**Agent:** Scientist
**Status:** Complete
