# Current Capabilities

> What the system can actually do right now. Updated as tools are built/integrated.

## MCPs Available

| MCP | Capabilities | Status |
|-----|--------------|--------|
| **Obsidian** | Read/write vault, search, manage frontmatter, tags | ✅ Active |
| **Zotero** | Search papers, get fulltext, annotations, semantic search | ✅ Active |
| **GitHub** | Repos, issues, PRs, file operations, search | ✅ Active |
| **Desktop Commander** | File system, processes, search, execute commands | ✅ Active |

## Claude Code Plugins

| Plugin | Capabilities | Scope |
|--------|--------------|-------|
| **superpowers** | Brainstorming, planning, subagents, TDD, code review | Project |
| **hookify** | Custom behavioral hooks via markdown | Project |
| **claude-md-management** | Audit/improve CLAUDE.md files | Project |
| **code-simplifier** | Simplify code | User |
| **commit-commands** | Git commit workflows | Project |

## Agents Defined

| Agent | Purpose | Location |
|-------|---------|----------|
| **overnight** | Learn patterns, analyze vault, generate insights | `agents/overnight.md` |
| **architect** | Build tools, MCPs, plugins when gaps found | `agents/architect.md` |
| **oracle** | Predict needs, prepare resources, surface info | `agents/oracle.md` |

## Built-In Capabilities

| Capability | How |
|------------|-----|
| Web search | Native Claude capability |
| Code execution | Claude Code container |
| File creation | Native + Desktop Commander |
| Git operations | GitHub MCP + bash |
| Process management | Desktop Commander |

## Knowledge Bases

| Source | Access | Contents |
|--------|--------|----------|
| Obsidian vault | Via MCP | 356+ daily notes, projects, knowledge |
| Zotero library | Via MCP | Research papers, annotations |
| This brain repo | Direct | System state, logs, knowledge |
| Web | Search | Current information |

---

## What The System CAN Do

| Category | Specific Capabilities |
|----------|----------------------|
| **Analyze** | Read vault, extract patterns, identify friction |
| **Synthesize** | Combine information, generate insights |
| **Predict** | Anticipate needs based on patterns |
| **Build** | Create MCPs, plugins, hooks, scripts |
| **Document** | Write knowledge files, logs, proposals |
| **Search** | Web, vault, Zotero, GitHub |
| **Propose** | Suggest changes for user approval |
| **Question** | Ask user for missing context |

## What The System CANNOT Do (Yet)

| Gap | Potential Solution | Priority |
|-----|-------------------|----------|
| Calendar integration | Google Calendar MCP | Medium |
| Email access | Gmail MCP | Low |
| Automated scheduling | Cron/scheduler tool | Medium |
| Voice interaction | Whisper integration | Low |
| Mobile notifications | Push notification service | Low |
| Real-time monitoring | Watchdog process | Medium |

## What The System SHOULD NOT Do

| Forbidden | Why |
|-----------|-----|
| Modify vault without approval | Protected resource |
| Delete files permanently | Irreversible |
| Access credentials | Security |
| Auto-integrate tools | User must approve |
| Run untested code in production | Safety |

---

## Capability Roadmap

### Phase 1: Foundation (Current)
- [x] Basic analysis of vault
- [x] Pattern extraction
- [x] Knowledge documentation
- [x] Agent architecture defined
- [ ] First overnight run completed
- [ ] First predictions validated

### Phase 2: Prediction
- [ ] Morning summaries working
- [ ] Prediction accuracy >70%
- [ ] Resource pre-fetching
- [ ] Friction warnings

### Phase 3: Tool Building
- [ ] First custom hook created
- [ ] First custom command created
- [ ] Tool successfully integrated
- [ ] Build-test-integrate loop proven

### Phase 4: Autonomy
- [ ] Multi-agent coordination
- [ ] Self-triggered runs
- [ ] Automatic pattern updates
- [ ] Proactive user prompting

---

## Adding New Capabilities

When a new capability is added:
1. Update this file
2. Document in relevant agent instructions
3. Add to `context/ecosystem.md` if tool-related
4. Test before marking as ✅ Active
5. Log the addition

---

*Capabilities compound. Each new tool enables others.*
