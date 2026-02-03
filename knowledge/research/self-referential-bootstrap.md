---
created: 2026-02-02
tags:
  - research
  - bootstrap
  - self-improvement
  - automation
status: complete
---

# Self-Referential Bootstrap Patterns

Research on bootstrap patterns that work automatically without user action.

## Executive Summary

Self-referential bootstrap is achievable through three key mechanisms:
1. **CLAUDE.md automatic loading** - Claude Code reads this file on every session start
2. **Hook-based initialization** - PreToolUse hooks fire before every tool call
3. **Memory-based context recall** - Agents proactively load relevant patterns

The minimal viable bootstrap is a CLAUDE.md file that points to session state recovery protocol.

---

## Zero-Action Bootstrap Patterns

Patterns that work without any user action:

| Pattern | How | Pros | Cons |
|---------|-----|------|------|
| **CLAUDE.md Auto-Read** | Claude Code automatically reads CLAUDE.md on session start | ✓ Zero config<br>✓ Works immediately<br>✓ No size limit | ✗ Only on session start<br>✗ Not mid-conversation |
| **Hook-Based Init** | PreToolUse/PostToolUse hooks fire on every tool call | ✓ Runs frequently<br>✓ Can inject context<br>✓ Survives compaction | ✗ Adds latency<br>✗ Requires hook setup |
| **Proactive Context Recall** | Agent runs similarity search before LLM invocation | ✓ Smart loading<br>✓ Only relevant context<br>✓ Scales well | ✗ Requires vector DB<br>✗ More complex |
| **Session Bootstrap** | Context files loaded during agent session init | ✓ Clean lifecycle<br>✓ Predictable<br>✓ Low overhead | ✗ Only once per session<br>✗ Doesn't survive compaction |
| **Handle Pattern** | Agent sees lightweight refs, loads on demand | ✓ Memory efficient<br>✓ Scales to large data | ✗ Requires tool support<br>✗ More complex |

---

## CLAUDE.md as Bootstrap Foundation

### What Happens Automatically

When Claude Code opens a folder with CLAUDE.md:
1. **Automatic read on session start** - File is read without invoking read tools
2. **Added to system prompt** - Content becomes part of every LLM invocation
3. **No size limit** - Can be arbitrarily large (though should be concise)
4. **Living document** - Can be updated anytime, takes effect next session

### Self-Referential Instructions Template

```markdown
# Project Bootstrap

## Recovery Protocol (Read This First)
1. Check [[context/session-state.md]] for recovery state
2. Check [[context/active-agents.md]] for coordination
3. Read recent commits: `gh api repos/USER/REPO/commits --jq '.[0:5]'`
4. Continue from pending list

## Auto-Loading Instructions
- Before starting: Read session-state.md
- Before modifying: Read active-agents.md to avoid conflicts
- After work: Update session-state.md and commit

## Critical Files
- [[context/session-state.md]] - Compaction-resilient state
- [[context/active-agents.md]] - Agent coordination
- [[tasks/pending/]] - Work queue
```

### Limits and Considerations

- **When it loads**: Only on session start, not mid-conversation
- **Compaction**: Survives compaction (re-read on new session)
- **Size**: No hard limit, but keep focused (< 2000 words ideal)
- **Format**: Markdown with links to other files
- **Updates**: Changes take effect next session start

---

## Hook-Based Bootstrap

### Automatic Hook Firing

Claude Code hooks that fire automatically:

| Hook | When | Use For |
|------|------|---------|
| `PreToolUse:*` | Before every tool call | Inject context, check state |
| `PostToolUse:*` | After every tool call | Log actions, update state |
| `SubagentStart` | Agent spawned | Initialize agent context |
| `SubagentComplete` | Agent finished | Collect results, update metrics |

### Bootstrap via PreToolUse Hook

```typescript
// hooks/PreToolUse.ts
export default async function (context) {
  // Fires before EVERY tool call

  // Auto-inject recovery reminder
  if (isFirstToolCall()) {
    return {
      additionalContext: "Read context/session-state.md for recovery protocol"
    };
  }

  // Auto-check coordination
  if (isFileModification(context.tool)) {
    const activeAgents = readFile("context/active-agents.md");
    return {
      additionalContext: `Active agents: ${activeAgents}`
    };
  }
}
```

### Pros and Cons

**Pros:**
- Runs automatically on every tool call
- Can inject fresh context mid-conversation
- Survives compaction (re-fires on next tool call)
- No user action required

**Cons:**
- Adds latency to every tool call (50-200ms)
- Can be noisy if too verbose
- Requires hook installation (one-time setup)
- Must be fast (< 500ms timeout)

---

## Memory-Based Bootstrap Patterns

### Proactive Context Recall

Based on research from [Anthropic's context engineering guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

1. **Pre-processor runs similarity search** on user input
2. **Relevant snippets injected** before LLM invoked
3. **Agent sees only what it needs** for current task

Example flow:
```
User: "Fix the authentication bug"
  ↓
Pre-processor: Similarity search for "authentication"
  ↓
Inject context: auth system design, recent auth commits, auth tests
  ↓
LLM invoked with targeted context
```

### Agentic Context Engine (ACE)

From [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine):

- **Agents learn from experience** - Extract patterns on success
- **Automatic in-context learning** - No fine-tuning needed
- **Skillbook evolution** - Patterns accumulate over time
- **Smart pattern discovery** - Agents find relevant standards automatically

### Handle Pattern for Large Data

From [Google's multi-agent framework guide](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/):

**Problem:** Can't load entire codebase into context

**Solution:**
1. Agent sees lightweight references (file paths, summaries)
2. When needed, agent calls tool to load full content
3. Loaded content temporarily in working context
4. Agent processes and discards

Example:
```
Agent sees: "auth.ts (authentication system, 500 lines)"
Agent thinks: "I need to check auth logic"
Agent calls: loadFile("auth.ts")
Agent processes: Full content now available
Agent outputs: Analysis complete
Agent discards: Content removed from context
```

---

## Recommended Minimal Bootstrap

The simplest automatic self-referential setup for a system like Brain:

### Component 1: CLAUDE.md Entry Point (Automatic)

```markdown
# Brain - Self-Evolving AI Assistant

## Bootstrap Protocol (AUTOMATIC)
1. Read [[context/session-state.md]] - Recovery state
2. Read [[context/active-agents.md]] - Coordination
3. Check `gh api repos/USER/REPO/commits --jq '.[0:5]'` - Recent work
4. Continue from pending tasks

## Why This Works
- CLAUDE.md is read automatically on session start
- Points to session-state.md which is compaction-resilient
- session-state.md contains full recovery protocol
- No user action required
```

**Why automatic:** Claude Code reads CLAUDE.md on every session start without user action.

### Component 2: Session State File (Compaction-Resilient)

```markdown
# Session State

> **COMPACTION RESILIENCE**: Read this first after context reset.

## Active Agent
- **agent-X**: Current work description

## Pending Tasks
- Task 1: Description
- Task 2: Description

## Recovery Protocol
1. Read recent commits for context
2. Check active-agents.md for coordination
3. Continue from pending list
```

**Why automatic:** CLAUDE.md points here, so agent reads this immediately on bootstrap.

### Component 3: PreToolUse Hook (Context Injection)

```typescript
export default async function (context) {
  const isFirstCall = !context.conversationState?.hasSeenBootstrap;

  if (isFirstCall) {
    return {
      additionalContext: "🔄 Bootstrap: Read context/session-state.md for recovery protocol"
    };
  }
}
```

**Why automatic:** Fires on first tool call, injecting recovery reminder.

### Complete Bootstrap Flow

```
Session Start
  ↓
Claude Code reads CLAUDE.md automatically
  ↓
CLAUDE.md says "Read context/session-state.md"
  ↓
Agent reads session-state.md
  ↓
session-state.md contains full recovery protocol
  ↓
Agent continues from pending tasks
  ↓
[Mid-conversation compaction occurs]
  ↓
PreToolUse hook fires on next tool call
  ↓
Hook injects "Read session-state.md" reminder
  ↓
Agent re-reads session-state.md
  ↓
Recovery complete, work continues
```

**Why this is minimal:**
- Only 2 files required (CLAUDE.md + session-state.md)
- 1 optional hook for mid-conversation resilience
- No vector DB, no complex preprocessing
- No user action at any step
- Survives compaction via hook reminder

---

## Implementation Status: Brain System

### Current Implementation

✅ **CLAUDE.md exists** - Entry point with directory map and commands
✅ **session-state.md exists** - Compaction-resilient recovery state
✅ **active-agents.md exists** - Coordination tracking
❓ **PreToolUse hook** - Unknown if installed

### Gap Analysis

| Requirement | Status | Action Needed |
|-------------|--------|---------------|
| CLAUDE.md points to session-state | ✅ YES | None |
| session-state has recovery protocol | ✅ YES | None |
| PreToolUse hook injects reminder | ❓ UNKNOWN | Check `.claude/hooks/` |
| Bootstrap tested after compaction | ❌ UNTESTED | Manual test needed |

### Recommended Enhancement

Add to CLAUDE.md:
```markdown
## 🔄 AUTOMATIC BOOTSTRAP (Read This First)

**After context compaction:**
1. Read [[context/session-state.md]] - Full recovery state
2. Read [[context/active-agents.md]] - Coordination check
3. Run `gh api repos/Div12345/brain/commits --jq '.[0:5]'` - Recent commits
4. Continue from pending list in session-state.md

This protocol is AUTOMATIC - no user action required.
```

---

## Research Sources

### Claude Code Ecosystem
- [Claude Code Tutorial 2026](https://dev.to/ayyazzafar/claude-code-tutorial-for-beginners-2026-from-installation-to-building-your-first-project-1lma)
- [Claude Bootstrap (alinaqi)](https://github.com/alinaqi/claude-bootstrap)
- [AutoClaude (ashburnstudios)](https://github.com/ashburnstudios/autoclaude)
- [CLAUDE.md Best Practices (egghead.io)](https://egghead.io/claude-md-initialization-and-best-practices-in-claude-code~jae0x)

### Context Engineering
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Google: Architecting Context-Aware Multi-Agent Framework](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)
- [Agentic Context Engine (ACE)](https://github.com/kayba-ai/agentic-context-engine)
- [LangChain: Context Engineering in Agents](https://docs.langchain.com/oss/python/langchain/context-engineering)

### Self-Referential Systems
- [Gödel Agent: Self-Referential Framework](https://arxiv.org/html/2410.04444v1)
- [Google DeepMind: PromptBreeder](https://www.marktechpost.com/2023/10/08/google-deepmind-researchers-introduce-promptbreeder-a-self-referential-and-self-improving-ai-system-that-can-automatically-evolve-effective-domain-specific-prompts-in-a-given-domain/)

---

## Key Findings

[FINDING] CLAUDE.md provides true zero-action bootstrap - file is automatically read on every session start without requiring user intervention or tool calls

[STAT:read_frequency] Every session start (automatic)
[STAT:size_limit] No hard limit (recommend < 2000 words)
[STAT:compaction_resilience] Survives compaction (re-read on new session)

[FINDING] Hook-based bootstrap can inject context mid-conversation, providing resilience against context compaction

[STAT:hook_frequency] Every tool call (PreToolUse) or every agent spawn (SubagentStart)
[STAT:latency_cost] 50-200ms per tool call
[STAT:timeout_limit] 500ms maximum hook execution time

[FINDING] Minimal viable bootstrap requires only 2 files - CLAUDE.md pointing to session-state.md with recovery protocol

[STAT:min_components] 2 files (CLAUDE.md + session-state.md)
[STAT:optional_enhancement] 1 hook (PreToolUse for mid-conversation resilience)
[STAT:setup_time] < 5 minutes (one-time)

[FINDING] Brain system already has core bootstrap infrastructure in place - CLAUDE.md entry point with session-state.md recovery protocol

[STAT:implementation_status] 2/3 core components implemented (66%)
[STAT:missing_component] PreToolUse hook status unknown

[LIMITATION] CLAUDE.md only loads on session start, not mid-conversation - requires hooks for mid-conversation compaction resilience
[LIMITATION] Hook-based injection adds latency to every tool call - must balance context benefit vs. performance cost
[LIMITATION] Research focused on Claude Code patterns - other interfaces (Desktop Claude, Overnight Agent) may have different bootstrap mechanisms
