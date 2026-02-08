---
module: System
date: 2026-02-08
problem_type: workflow_issue
component: tooling
symptoms:
  - "settings.local.json is gitignored and won't travel to CC Web remote sessions"
  - "Obsidian/Zotero MCP context unavailable in remote environment"
  - "claude --remote flag not available in CLI v2.1.37"
  - "SessionStart hooks run both locally and remotely by default"
root_cause: incomplete_setup
resolution_type: workflow_improvement
severity: medium
tags: [cc-web, remote-execution, settings, mcp-context, audit]
---

# Troubleshooting: Preparing a Repository for CC Web Remote Execution

## Problem
When delegating a complex task (codebase audit) to CC Web, the remote session clones from GitHub into an isolated VM with no access to local filesystem, Obsidian MCP, Zotero MCP, or other local services. Multiple configuration gaps prevented successful remote execution.

## Environment
- Module: System (cross-project workflow)
- Claude Code Version: 2.1.37
- Affected Component: CC Web remote sessions, settings.json, SessionStart hooks
- Date: 2026-02-08

## Symptoms
- `settings.local.json` is gitignored — permissions defined there don't travel to CC Web
- Obsidian and Zotero MCPs are unavailable remotely — project context stored only in those tools is invisible to the auditor
- `claude --remote "prompt"` fails with "Error: Input must be provided either through stdin or as a prompt argument when using --print" (flag doesn't exist in v2.1.37)
- SessionStart hook installs beads CLI which may fail on CC Web (no local tooling)

## What Didn't Work

**Attempted Solution 1:** `claude --remote "prompt"` from Bash tool
- **Why it failed:** The `--remote` flag is documented in official docs but not available in CLI v2.1.37. No alternative programmatic launch exists.

**Attempted Solution 2:** Sending `&` prefix from within a tool call
- **Why it failed:** The `&` prefix is intercepted by the Claude Code CLI input parser before reaching the AI. It can only be typed by the user interactively.

## Solution

A reusable checklist for preparing any repo for CC Web execution:

### 1. Move permissions to tracked settings

```json
// .claude/settings.json (tracked, travels to CC Web)
{
  "permissions": {
    "allow": [
      "Bash(python:*)",
      "Bash(python -m pytest:*)",
      "Bash(python -m:*)",
      "Bash(pip install:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(ruff:*)",
      "Bash(tree:*)",
      "Bash(wc:*)",
      "Bash(find:*)"
    ]
  }
}
```

Local CC already has `settings.local.json` which overrides project settings, so no conflict.

### 2. Make SessionStart hooks remote-safe

Use `CLAUDE_CODE_REMOTE` env var for conditional execution:

```bash
#!/bin/bash
# Only run heavy setup in remote
if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
  pip install -q -r requirements.txt
fi

# Non-critical installs should be non-fatal
curl -sSL https://example.com/installer.sh | bash || true
```

For simpler cases, just make failures non-fatal with `|| true`.

### 3. Extract MCP context into tracked files

CC Web has NO access to Obsidian, Zotero, or other local MCPs. Any context stored only in those tools must be explicitly extracted:

```bash
# Read from Obsidian MCP, write to repo
# docs/context/audit-context-from-obsidian.md
```

Include: experiment design, known issues, expected results, owner concerns — anything the remote session needs to do its job without asking questions.

### 4. Add CC Web notes to CLAUDE.md

```markdown
## CC Web (Remote Execution) Notes

When running on CC Web (`CLAUDE_CODE_REMOTE=true`):
- **Obsidian and Zotero MCPs** are unavailable
- Use **system Python** (not conda)
- **Localhost services** are unavailable
- All data files must be committed to git
```

### 5. Put plan files in tracked location

`docs/plans/` (tracked) NOT `.claude/plans/` (often gitignored).

### 6. Commit data files

CC Web clones from GitHub. Any data files the task needs must be `git add`'d and pushed.

### 7. Add methodology plugins

```json
{
  "enabledPlugins": {
    "compound-engineering@every-marketplace": true
  }
}
```

### 8. Push everything, then launch

All config, context, data, and plan must be committed and pushed before launching.

**Launch options:**
- **Best:** Go to claude.ai/code, select repo, paste prompt
- **From terminal:** Open `claude` in the repo directory, type `& <prompt>`
- **Not available (v2.1.37):** `claude --remote "prompt"`

## Why This Works

CC Web runs in an isolated Anthropic-managed VM that clones from GitHub. It has:
- No local filesystem access
- No local MCP servers
- No conda environments
- Its own `settings.json` from the repo (but NOT `settings.local.json`)
- SessionStart hooks that run automatically after clone

By moving all configuration, context, and data into tracked files and making hooks robust, the remote session is self-sufficient.

## Prevention

**Before any CC Web delegation:**
1. Run the checklist above
2. Ask: "What does the remote session need to know that's only in my head or my local tools?"
3. Extract that context into a tracked document
4. Verify with `git status` — nothing untracked that's needed

**Permanent CLAUDE.md addition:** Add CC Web notes section to any repo that might use remote execution.

**Hook pattern:** Always use `|| true` for non-critical installs in SessionStart hooks.

## Related Issues

No related issues documented yet.
