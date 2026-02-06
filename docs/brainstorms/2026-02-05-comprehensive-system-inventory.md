# Comprehensive System Inventory

> Full inventory of interfaces, tools, existing systems, and gaps
> Based on Desktop session research + this session's analysis
>
> **Obsidian Links:** See also [[00 - Dashboard/State.md]], [[99 - Meta/System/CE Staging Rules]], [[99 - Meta/System/How Work Flows]]

---

## Part 1: Complete Interface & Execution Environment Inventory

### Interfaces (What You Interact With)

| Interface | Type | Location | Auto-Context | Status |
|-----------|------|----------|--------------|--------|
| **Claude Code (CLI)** | CLI | WSL terminal | CLAUDE.md + rules/ | ✅ Primary |
| **Claude Code (Cloud)** | Web | claude.ai/code, `&` prefix, `--remote` | CLAUDE.md from repo | ⚠️ Different capabilities |
| **Claude Desktop** | App | Windows native | userMemories only | ✅ Active |
| **Gemini CLI** | CLI | WSL terminal | GEMINI.md | ✅ Overnight |
| **Antigravity CLI** | CLI | WSL terminal | ? | ⚠️ Not evaluated |
| **OpenCode (OC)** | CLI | ? | ? | ⚠️ Not evaluated |

### Execution Environments (Where Code Actually Runs)

**ONLY TWO CC ENVIRONMENTS:**

| Environment | Where It Runs | Filesystem | MCPs | Use Case |
|-------------|---------------|------------|------|----------|
| **CC Local** | Your WSL Linux | `/home/div/...` full access | All local MCPs | Primary dev work |
| **CC Cloud** | Anthropic VMs | GitHub clone only | Remote MCP servers (HTTP) only | Parallel delegation, async PRs |
| **Desktop** | Windows native | `C:\Users\din18\...` | Desktop-configured MCPs | Windows-only work, iPad via sync |
| **Gemini CLI** | Your WSL Linux | `/home/div/...` | ~/.gemini/settings.json MCPs | Overnight automation |
| **Scheduler** | Your WSL Linux | `/home/div/...` | Orchestrates CC/Gemini | Task dispatch |
| **Human** | Any device | Via Obsidian app | N/A | Manual thinking/review |

**IMPORTANT: There is NO "Web UI tunneling to local".** The `&` prefix and `--remote` flag create **new cloud sessions**, not tunneled connections. `/teleport` pulls cloud sessions down to local (one-way).

**Key Differences:**

| Capability | CC Local | CC Cloud | Desktop |
|------------|----------|----------|---------|
| Local filesystem | ✅ Full | ❌ None (GitHub clone) | ✅ Windows only |
| WSL access | ✅ | ❌ | ❌ |
| Git commits | ✅ Direct | ✅ Via GitHub proxy | ⚠️ GitHub MCP |
| Local MCPs | ✅ All | ❌ Remote only | ✅ Desktop MCPs |
| Parallel tasks | ⚠️ Sequential | ✅ Multiple sandboxes | ⚠️ One conversation |
| Requires supervision | Yes | No (async PRs) | Yes |
| Network access | Full | Allowlist only | Full |
| Session teleport | ✅ Pull from cloud | ✅ Push not supported | ❌ |

**CC Cloud (claude.ai/code, `&`, `--remote`) Details:**
- Runs in Anthropic-managed isolated VMs
- Repository cloned from GitHub to sandbox
- No permission prompts (contained blast radius)
- Creates PRs automatically when done
- Can run multiple tasks in parallel (each gets own sandbox)
- Limited network (allowlist), GitHub proxy for credentials
- MCPs: Only Remote MCP servers over HTTP (not local)
- `/teleport` pulls cloud session to local terminal (one-way)
- `/remote-env` selects which cloud environment config to use

**How to access CC Cloud:**
1. **claude.ai/code** - Web interface directly
2. **`& <task>`** - From local CLI, creates new cloud session with context
3. **`claude --remote "<task>"`** - From command line, same as `&`

Sources: [Claude Code on the web - Docs](https://code.claude.com/docs/en/claude-code-on-the-web)

### MCP Connectivity Matrix (Corrected)

| MCP Server | CC Local | CC Cloud | Desktop | Gemini |
|------------|----------|----------|---------|--------|
| **Obsidian** | ✅ | ❌ | ✅ | ✅ |
| **Zotero** | ✅ | ❌ | ✅ | ✅ |
| **Paper Search** | ✅ | ⚠️ if HTTP remote | ✅ | ✅ |
| **NotebookLM** | ✅ | ❌ | ❌ | ❌ |
| **GitHub** | ✅ | ✅ built-in proxy | ✅ | ✅ |
| **Claude Desktop** | ✅ | ❌ | N/A | ✅ |
| **Context7** | ✅ | ❌ | ❌ | ❌ |
| **AIM Memory** | ❌ unused | ❌ | ✅ exists | ❌ |

**Key insight:** CC Cloud cannot access your local MCPs, Obsidian vault, or local filesystem. It's GitHub-only with PR output. Use CC Local for work requiring local tools.

### Interface Access Matrix (Corrected)

| Resource | CC Local | CC Cloud | Desktop | Gemini |
|----------|----------|----------|---------|--------|
| WSL Filesystem | ✅ | ❌ | ❌ | ✅ |
| Windows Filesystem | ⚠️ /mnt/c | ❌ | ✅ | ⚠️ /mnt/c |
| GitHub repos | ✅ | ✅ (clone) | ⚠️ MCP | ✅ |
| Git commits | ✅ direct | ✅ via proxy | ⚠️ MCP | ✅ direct |
| Obsidian MCP | ✅ | ❌ | ✅ | ✅ |
| Zotero MCP | ✅ | ❌ | ✅ | ✅ |
| Paper Search MCP | ✅ | ⚠️ | ✅ | ✅ |
| NotebookLM MCP | ✅ | ❌ | ❌ | ❌ |
| GitHub MCP | ✅ | N/A built-in | ✅ | ✅ |
| Claude Desktop MCP | ✅ | ❌ | N/A | ✅ |
| Context7 MCP | ✅ | ❌ | ❌ | ❌ |
| Run arbitrary code | ✅ | ✅ (sandbox) | ❌ | ⚠️ limited |
| Parallel execution | ⚠️ agents | ✅ native | ❌ | ❌ |

---

## Part 2: Complete MCP Inventory

### Active MCPs (from settings.json + ToolSearch)

| MCP Server | Tools | Best For | Used By |
|------------|-------|----------|---------|
| **obsidian** | read/write/search/list notes, frontmatter, tags, global search | Vault operations | All interfaces |
| **zotero** | search, annotations, fulltext, semantic search, collections | Paper management | All interfaces |
| **paper-search** | search arXiv/PubMed/Semantic Scholar/bioRxiv/etc, download PDF | Paper discovery | All interfaces |
| **notebooklm-mcp** | notebook CRUD, source management, query, studio (audio/video) | Grounded Q&A, synthesis | CC only |
| **github** | repos, issues, PRs, file operations, search | Repo operations | All interfaces |
| **claude-desktop** | new/send/read/navigate/search/status/connectors | Desktop steering | CC, Gemini |
| **context7** | resolve-library-id, query-docs | SDK/framework docs | CC only |
| **memory (AIM)** | store/get/search/link/forget entities & observations | Knowledge graph | Desktop (unused) |

### MCP Tools Detail (Key Ones)

**Obsidian MCP:**
- `obsidian_read_note` - Read file content
- `obsidian_update_note` - Write/append to file
- `obsidian_list_notes` - List directory with tree
- `obsidian_global_search` - Full-text search
- `obsidian_manage_frontmatter` - YAML metadata
- `obsidian_manage_tags` - Tag operations
- `obsidian_search_replace` - Find/replace in files

**Zotero MCP:**
- `zotero_search_items` - Search library
- `zotero_get_item_fulltext` - Get paper text
- `zotero_get_annotations` - Get highlights/notes
- `zotero_semantic_search` - AI-powered search
- `zotero_get_collections` - Browse collections

**NotebookLM MCP:**
- `notebook_create/list/get/delete` - Notebook management
- `source_add` - Add URL/text/file sources
- `notebook_query` - Grounded Q&A with citations
- `grounded-query` skill - Source-backed answers
- `studio_create` - Generate audio/video summaries

**Claude Desktop MCP:**
- `claude_desktop_new` - Start new conversation
- `claude_desktop_send` - Send message, optionally wait
- `claude_desktop_read` - Read conversation
- `claude_desktop_status` - Check if generating
- `claude_desktop_list_connectors` - List MCP connectors
- `claude_desktop_toggle_connector` - Enable/disable MCPs
- `claude_desktop_reload_mcp` - Refresh MCP config

---

## Part 3: Complete Plugin/Skill Inventory

### CC Plugins (from settings.json)

| Plugin | Status | Key Skills |
|--------|--------|------------|
| **oh-my-claudecode** | ✅ Enabled | autopilot, ralph, ultrawork, ecomode, plan, swarm, pipeline, code-review, security-review, tdd, deepsearch, etc. |
| **compound-engineering** | ✅ Enabled | /workflows:brainstorm, /workflows:plan, /workflows:work, /workflows:review, /workflows:compound, git-worktree, skill-creator |
| **commit-commands** | ✅ Enabled | commit, commit-push-pr, clean_gone |
| **hookify** | ✅ Enabled | Create behavior enforcement hooks |
| **claude-md-management** | ✅ Enabled | revise-claude-md |
| **feature-dev** | ✅ Enabled | feature-dev guided workflow |
| **code-simplifier** | ✅ Enabled | Simplify/refine code |
| **claude-code-setup** | ✅ Enabled | claude-automation-recommender |
| **superpowers** | ❌ Disabled | Covered by CE+OMC |
| **ralph-loop** | ❌ Disabled | Subset of OMC ralph |

### Local Skills (brain repo)

| Skill | Location | Purpose |
|-------|----------|---------|
| brain-system | .claude/skills/brain-system/ | Working in brain repo |
| grounded-query | (via NotebookLM) | Source-backed Q&A |
| ask-gemini | (available) | Query Gemini directly |
| gemini-brainstorm | (available) | Brainstorm with Gemini |
| nlm-sync | (available) | NotebookLM sync |
| claude-desktop-orchestration | (available) | Desktop delegation |

### OMC Agents (32 total, key ones)

| Agent | Model | Purpose |
|-------|-------|---------|
| executor | sonnet | Task execution |
| executor-low | haiku | Simple tasks |
| executor-high | opus | Complex tasks |
| architect | opus | Strategic analysis |
| architect-medium | sonnet | Architecture |
| architect-low | haiku | Quick questions |
| designer | sonnet | UI/UX |
| researcher | sonnet | External research |
| explore | haiku | Fast codebase search |
| explore-medium | sonnet | Thorough search |
| explore-high | opus | Deep analysis |
| code-reviewer | sonnet | Code review |
| security-reviewer | opus | Security audit |
| build-fixer | sonnet | Fix build errors |
| tdd-guide | sonnet | Test-driven development |
| scientist | sonnet | Data analysis |
| writer | haiku | Documentation |

---

## Part 4: Three-Layer Architecture (Corrected)

> See [[99 - Meta/System/CE Staging Rules]] for promotion/feedback rules
> See [[99 - Meta/System/How Work Flows]] for session note patterns

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: THINKING (Where ideas form)                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│ Location: OneVault (Obsidian)                                                │
│ Key Files: [[00 - Dashboard/State.md]], [[00 - Dashboard/CE Board.md]]       │
│ Contents: Session notes, decisions, State.md, CE Board                       │
│ Access: Human (any device), all agents via Obsidian MCP                      │
│ Persistence: OneDrive sync + remotely-save                                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ PROMOTE (human decision, see CE Staging Rules)
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: STAGING (Instructions + Queue)                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ Location: Brain repo (git)                                                   │
│ Key Files: CLAUDE.md, tasks/pending/*.md, docs/plans/*.md                    │
│ Contents: Task specs, agent configs, execution plans                         │
│ Access: CC filesystem, Desktop via GitHub MCP, Gemini filesystem             │
│ Persistence: Git (GitHub remote)                                             │
│ NOT execution - instructions waiting to be picked up                         │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ DISPATCH (scheduler, human, or agent picks up)
┌──────────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: EXECUTION (Where work actually happens)                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ CC Local (CLI)  │  │ CC Cloud        │  │ Desktop (Win)   │              │
│  │ - WSL filesystem│  │ - Anthropic VMs │  │ - Windows FS    │              │
│  │ - All local MCPs│  │ - GitHub only   │  │ - Desktop MCPs  │              │
│  │ - Git direct    │  │ - No local MCPs │  │ - No WSL access │              │
│  │ - Full code exec│  │ - Parallel OK   │  │ - Conversation  │              │
│  │ - /teleport in  │  │ - &, --remote   │  │                 │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ Gemini→Desktop  │  │ Scheduler       │  │ Human           │              │
│  │ - Gemini API    │  │ - Orchestrates  │  │ - Any device    │              │
│  │ - MCP steering  │  │ - CC or Gemini  │  │ - Manual work   │              │
│  │ - Desktop exec  │  │ - Task movement │  │ - Obsidian app  │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ FEEDBACK (results written back)
                        ┌───────────────────────┐
                        │ Back to THINKING      │
                        │ - State.md updated    │
                        │ - #ce/feedback tag    │
                        │ - CE Board card moved │
                        └───────────────────────┘
```

### Execution Environment Capabilities (Full Matrix)

| Executor | WSL FS | Win FS | Run Code | Git Commit | MCPs | Parallel |
|----------|--------|--------|----------|------------|------|----------|
| CC Local | ✅ | ⚠️ /mnt/c | ✅ | ✅ direct | ✅ All local | ⚠️ agents |
| CC Cloud | ❌ | ❌ | ✅ sandbox | ✅ via proxy | ⚠️ Remote only | ✅ native |
| Desktop | ❌ | ✅ | ❌ | ⚠️ GitHub MCP | ✅ Desktop | ❌ |
| Gemini CLI | ✅ | ⚠️ /mnt/c | ⚠️ Limited | ✅ | ✅ Configured | ❌ |
| Scheduler | ✅ | ⚠️ /mnt/c | Launches | ✅ | N/A | ✅ |
| Human | via app | via app | ✅ Manual | ✅ Manual | N/A | N/A |

**When to use CC Cloud (`&`, `--remote`, claude.ai/code):**
- Parallel work on multiple independent tasks (each gets isolated sandbox)
- Fire-and-forget delegation (async PR creation)
- Work doesn't need local MCPs (Obsidian, NotebookLM, Zotero)
- Acceptable to wait for PR instead of real-time interaction
- Can `/teleport` results back to local when done

---

## Part 4b: Existing System (Built in Desktop Session)

### What Already Exists in OneVault

| Component | Obsidian Link | Purpose | Status |
|-----------|---------------|---------|--------|
| **State.md** | [[00 - Dashboard/State.md]] | Cross-interface state bridge, read first | ✅ Created |
| **CE Board** | [[00 - Dashboard/CE Board.md]] | Kanban (brainstorm→plan→delegated→doing→review→done) | ✅ Created |
| **CE Staging Rules** | [[99 - Meta/System/CE Staging Rules]] | Obsidian ↔ brain repo bridge rules | ✅ Created |
| **How Work Flows** | [[99 - Meta/System/How Work Flows]] | Session notes pattern (→ ? ! markers) | ✅ Created |
| **Task Dashboard** | [[00 - Dashboard/Tasks.md]] | Dataview task queries | ✅ Exists (Nov 2025) |
| **Session Template** | [[99 - Meta/Templates/(TEMPLATE) CE Session]] | Session capture template | ✅ Created |
| **Project Workbenches** | [[03 - Projects/{project}/Workbench.md]] | Auto-aggregate from sessions via Dataview | ✅ Structure |
| **Project Sessions** | [[03 - Projects/{project}/sessions/]] | Atomic thinking units | ✅ Structure |

**Key Files to Read on Session Start:**
1. [[00 - Dashboard/State.md]] — Current focus, recent decisions, next actions
2. [[00 - Dashboard/CE Board.md]] — Visual pipeline status
3. Project workbench if working on specific project

### What Already Exists in Brain Repo

| Component | Location | Purpose | Status |
|-----------|----------|---------|--------|
| **CLAUDE.md** | CLAUDE.md | CC entry point | ✅ Updated to read State.md |
| **CE Docs** | docs/{brainstorms,plans,solutions}/ | CE artifacts | ✅ Exists, used |
| **Task Queue** | tasks/{pending,active,completed,failed}/ | Overnight tasks | ✅ Exists, used |
| **Scheduler** | tools/cc-scheduler/ | Overnight automation | ⚠️ Broken since Feb 3 |
| **Desktop MCP** | tools/mcps/claude-desktop-mcp/ | Desktop steering | ✅ Works |
| **BOARD.md** | BOARD.md | Dashboard (needs dataview) | ⚠️ Not in Obsidian vault |

### The Designed Flow (from [[99 - Meta/System/CE Staging Rules]])

```
OneVault (Thinking)              Brain Repo (Staging)           Execution
─────────────────                ────────────────────           ─────────
#ce/brainstorm (session note)
       │
       ▼ solidifies
#ce/plan (same note re-tagged)
       │
       ▼ PROMOTE: CC creates task file
                                 tasks/pending/xxx.md
                                        │
                                        ▼ DISPATCH
                                                               CC Local/Cloud
                                                               Gemini→Desktop
                                                               Scheduler
                                        │
                                 tasks/completed/xxx.md  ◄─────┘
                                        │
       ▼ FEEDBACK: agent writes back    │
#ce/feedback on session ◄───────────────┘
       │
       ▼
[[00 - Dashboard/State.md]] updated
[[00 - Dashboard/CE Board.md]] card moved
```

**Session Note Markers** (from [[99 - Meta/System/How Work Flows]]):
- `→` = Decision made (with rationale) — Dataview finds these
- `?` = Open question — aggregates to workbench
- `!` = Action needed — becomes todo
- `!delegate:` = Should become brain repo task

---

## Part 5: Lit Review Pipeline (Specialized)

### Current Tool Chain

| Step | Tool | MCP | Status |
|------|------|-----|--------|
| **Discover** | Paper Search | paper-search | ✅ Works |
| **Store** | Zotero | zotero | ✅ Works |
| **Read** | Zotero fulltext | zotero | ✅ Works |
| **Synthesize** | NotebookLM | notebooklm-mcp | ✅ Works (CC only) |
| **Query** | grounded-query skill | notebooklm-mcp | ✅ Works |
| **Integrate** | Write to Obsidian | obsidian | ✅ Works |

### NotebookLM-Specific Tools

- `notebook_create` - Create research notebook
- `source_add(type=url|text|file)` - Add papers
- `notebook_query` - Ask questions with citations
- `studio_create(type=audio)` - Generate audio summary
- `note_create` - Add notes to notebook

### Lit Review Skill (grounded-query)

Available in CC. Uses NotebookLM to answer questions with source citations.

---

## Part 6: Gap Analysis

### What's Actually Missing (Not Built)

| Gap | Impact | Where It Should Live |
|-----|--------|---------------------|
| **Overnight pipeline broken** | Can't delegate while sleeping | Brain repo scheduler |
| **Multi-model quota fallback** | Single model exhausts quickly | executor.py |
| **Morning briefing** | Manual log checking | New skill or scheduler feature |
| **Dataview not installed** | Dashboards don't render | OneVault Obsidian |
| **Brain repo not pushed** | WSL/Windows desync | Git push to remote |
| **Antigravity/OC evaluation** | Unknown capabilities | Research task |
| **AIM Memory unused** | Wasted capability OR unnecessary | Decision needed |

### What's Built But Not Working

| Issue | Status | Fix |
|-------|--------|-----|
| Scheduler dead since Feb 3 | Rate limited, never recovered | Move failed→pending, fix quotas |
| BOARD.md in brain repo | Not in Obsidian vault, doesn't render | Open brain as vault + install dataview |
| Daily template invalidated | Old design, session-note system now | Simplify template |
| Workbenches for arterial/cardiac | Structure exists, no content | Create session notes |

### What's Built and Working

| Component | Status |
|-----------|--------|
| State.md in OneVault | ✅ Created, designed for all interfaces |
| CE Board kanban | ✅ Created, ready to use |
| CE Staging Rules | ✅ Documented, ready to follow |
| Session note structure | ✅ Designed, template exists |
| Brain repo task queue | ✅ Works, has tasks |
| Desktop MCP | ✅ Works, tested |
| Gemini→Desktop pipeline | ✅ Works when quota available |
| Lit review tools | ✅ All MCPs functional |

---

## Part 7: Recommended Immediate Actions

Based on this inventory:

### Do Now (Unblocks Everything)

1. **Install Dataview in OneVault** - Makes all dashboards work
2. **Push brain repo to remote** - Syncs WSL/Windows

### Do Next (Enables Daily Use)

3. **Open brain repo as Obsidian vault** - See BOARD.md, install dataview there too
4. **Start real work (C1 or C2)** - Test the system by using it
5. **Create session note as you work** - Iterate on template by doing

### Do Later (Improvements)

6. **Fix scheduler** - Move failed→pending, check quotas
7. **Implement A2 (outcome capture)** - Task 080 spec exists
8. **Evaluate Antigravity/OC** - May replace Gemini

---

## Part 8: Tool Decision Matrix

### Should We Keep/Remove Tools?

| Tool | Verdict | Reasoning |
|------|---------|-----------|
| AIM Memory | **REMOVE** | Never used, file-based memory (knowledge.md) matches behavior |
| Sequential Thinking | **REMOVE** | Redundant, built into modern models |
| Obsidian MCP | **KEEP** | Universal access, bridges all interfaces |
| Zotero MCP | **KEEP** | Essential for lit review |
| Paper Search | **KEEP** | Essential for lit review |
| NotebookLM | **KEEP** | Grounded Q&A is unique capability |
| Context7 | **KEEP** | SDK docs when coding |
| Claude Desktop MCP | **KEEP** | Core to overnight pipeline |
| GitHub MCP | **KEEP** | Useful for Desktop→git writes |

---

## Part 9: Execution Environment Decision Matrix

### Which Executor for Which Task?

| Task Type | Best Executor | Why |
|-----------|---------------|-----|
| Interactive coding with context | CC Local | Full MCPs, real-time feedback |
| Lit review (Paper Search → Zotero → NotebookLM) | CC Local | NotebookLM MCP only works locally |
| Parallel feature branches | CC Cloud (`&`) | Native parallel, isolated sandboxes |
| Fire-and-forget refactoring | CC Cloud | Async PR, no supervision needed |
| Windows-only tools | Desktop | Only Windows filesystem access |
| Overnight batch | Gemini→Desktop | Proven pipeline, quota-aware |
| MCP-heavy work (Obsidian, Zotero) | CC Local | CC Cloud can't access local MCPs |
| Quick edits needing iPad review | Desktop | Obsidian sync to iPad |
| Plan locally, execute remotely | CC Local → CC Cloud | Use `&` after planning |

### CC Cloud Limitations to Remember

1. **No local filesystem** — can't access `/home/div/...` or `C:\...`
2. **No Obsidian MCP** — can't read/write OneVault or brain vault
3. **No NotebookLM** — can't do grounded queries
4. **No Zotero** — can't manage paper library
5. **No Claude Desktop MCP** — can't steer Desktop
6. **GitHub-only** — works with repos, outputs PRs
7. **Remote MCPs only** — must be HTTP-accessible, not local

**CC Cloud is ideal for:** Pure code work on GitHub repos where you don't need local tools.

---

## Summary

**The Desktop session built a complete system in OneVault.** Key files:
- [[00 - Dashboard/State.md]] — Cross-interface state (read first)
- [[00 - Dashboard/CE Board.md]] — Visual pipeline kanban
- [[99 - Meta/System/CE Staging Rules]] — Obsidian ↔ brain repo bridge
- [[99 - Meta/System/How Work Flows]] — Session note patterns

**Two CC execution environments (no tunneling):**
1. **CC Local** — CLI in WSL, full power, all MCPs, your filesystem
2. **CC Cloud** — Anthropic VMs, GitHub-only, no local MCPs, parallel sandboxes
   - Access via: claude.ai/code, `& <task>`, `--remote`
   - Pull results back: `/teleport`

**Other executors:**
3. **Desktop** — Windows native, Desktop MCPs, no WSL
4. **Gemini→Desktop** — Overnight automation pipeline

**Remaining gaps:**
1. Dataview not verified installed (dashboards may not render)
2. Scheduler dead since Feb 3 (quota issues)
3. System not tested with real CE work yet

**Next step:** Start C1 or C2 research work to test the flow end-to-end.
