# Task Specification Skill

How to write well-specified tasks that lead to successful autonomous execution.

## Why This Matters

Poorly specified tasks fail because:
- Agent doesn't know environment constraints
- Blockers discovered mid-execution waste tokens
- No fallback strategy when primary approach fails
- Success criteria are vague or unverifiable

## Task Specification Template

```markdown
## Goal
[One sentence: What does "done" look like?]

## Environment Constraints
- **Execution env:** [WSL2 | Windows | macOS | Docker | etc.]
- **Browser access:** [Yes | No - critical for auth flows]
- **Working dir:** [Absolute path]
- **Depends on:** [Other task IDs that must complete first]
- **MCP tools needed:** [List specific tools required]
- **File locations:** [Where inputs live, where outputs go]

## Known Blockers
[List foreseeable problems BEFORE execution]
1. [Blocker 1 - why it's a problem]
2. [Blocker 2 - why it's a problem]

## Workarounds Available
[Research these BEFORE creating the task]
- [Workaround 1 - how it addresses blocker]
- [Workaround 2 - alternative approach]

## User Decisions Needed
[Questions that require human input - gate on these]
- [ ] [Decision 1]
- [ ] [Decision 2]

## Proposed Solution
[Step-by-step plan with specific commands/tools]
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Success Criteria
[Verifiable checkboxes - must be testable]
- [ ] [Criterion 1 - how to verify]
- [ ] [Criterion 2 - how to verify]

## Fallback
[What to do if primary approach fails]
[Document manual steps as minimum viable outcome]

## Output
[Specific files/artifacts this task produces]
- [Output 1: path/to/file]
- [Output 2: path/to/file]
```

## Environment Analysis Checklist

Before creating a task, answer:

| Question | Why It Matters |
|----------|----------------|
| What OS/platform? | Commands differ, paths differ |
| Browser available? | Auth flows often need browser |
| Cross-platform access? | WSL↔Windows file bridging |
| Network access? | Firewall, proxy, VPN issues |
| Credentials available? | API keys, tokens, auth state |
| MCP tools exposed? | Some MCPs need separate auth |
| Disk space? | Large downloads/builds |
| Time constraints? | Timeouts, rate limits |

## Common WSL Blockers

| Blocker | Solution |
|---------|----------|
| No browser | Use `--manual` flags, bridge cookies from Windows |
| Windows paths | Translate via `/mnt/c/Users/...` |
| Auth tokens on Windows | Symlink or copy to WSL |
| GUI needed | Run on Windows side, not WSL |
| Port conflicts | Check both WSL and Windows listeners |

## Dependency Specification

Use beads (bd) for dependency tracking:

```bash
# Create with dependency
bd create "Task B" -d "..." --deps "blocks:brain-xyz"

# View dependency chain
bd show brain-xyz --deps
```

Scheduler respects `depends_on` in task YAML:
```yaml
depends_on: [task-a, task-b]
```

## Token Estimation Guidelines

| Task Type | Typical Tokens |
|-----------|----------------|
| Simple file read/write | 1,000-3,000 |
| Analysis with exploration | 5,000-10,000 |
| Multi-step implementation | 10,000-20,000 |
| Complex debugging | 15,000-30,000 |
| Full feature build | 20,000-50,000 |

## Anti-Patterns

❌ **Vague goal:** "Fix the auth"
✅ **Specific goal:** "Enable NotebookLM MCP auth from WSL without browser"

❌ **Missing constraints:** "Run the script"
✅ **With constraints:** "Run from WSL2, needs /mnt/c/ access, no browser"

❌ **No fallback:** "Automate cookie refresh"
✅ **With fallback:** "If automation fails, document manual steps"

❌ **Unverifiable success:** "Make it work"
✅ **Verifiable success:** "`nlm login --check` returns valid"

## Integration with cc-scheduler

Scheduler task files at `tasks/pending/*.md` should include:

```yaml
---
name: task-name
priority: 1-3
estimated_tokens: 8000
mode: autonomous | plan-first | read-only
timeout: 10m
skill: analyze | plan | ecomode | etc
model_hint: haiku | sonnet | opus
tags: [tag1, tag2]
depends_on: [other-task-name]
---

# Task Title

[Full specification following template above]
```

## Iteration Pattern

1. **Specify** → Write full task spec
2. **Review** → Check for missing constraints/blockers
3. **Execute** → Run via scheduler
4. **Observe** → Check logs, success criteria
5. **Learn** → Update spec if new blockers found
6. **Adjust** → Improve for next similar task
