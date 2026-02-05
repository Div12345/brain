# Capability Registry

> Every capability mapped to its compound engineering loop step. Use this to find the right tool for each phase of work.

## How to Use This Registry
- Before starting a loop step, consult the relevant section
- Prefer capabilities marked **compounds** — their output feeds future iterations
- Substeps are ordered by typical execution sequence within each step

---

## PLAN

### Plan > Research Past Solutions
*Check what the system already knows before researching from scratch.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| `learnings-query` skill | Skill (local) | Yes — reads from knowledge/solutions/ | Invoke at start of every planning session |
| `aim_memory_search` | MCP (AIM Memory) | Yes — queries knowledge graph | Search by problem category, technology |
| `obsidian_global_search` | MCP (Obsidian) | Yes — queries vault | Broader knowledge search |
| `knowledge/solutions/*.md` | Files | Yes — accumulated solution docs | Direct grep/glob when skill isn't invoked |

### Plan > Research Codebase
*Understand the current codebase before proposing changes.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| OMC `explore` agent (haiku) | Agent | No | Quick file/pattern search |
| OMC `explore-medium` agent (sonnet) | Agent | No | Thorough search with reasoning |
| OMC `explore-high` agent (opus) | Agent | No | Complex architectural search |
| `lsp_document_symbols` | MCP (OMC bridge) | No | File symbol outline |
| `lsp_workspace_symbols` | MCP (OMC bridge) | No | Cross-workspace symbol search |
| `ast_grep_search` | MCP (OMC bridge) | No | Structural code pattern matching |
| `lsp_goto_definition` | MCP (OMC bridge) | No | Navigate to symbol definition |
| `lsp_find_references` | MCP (OMC bridge) | No | Find all usages of a symbol |
| `git log` / `git diff` | Bash | No | Commit history analysis |
| feature-dev `code-explorer` | Agent (plugin) | No | Traces execution paths, maps architecture |

### Plan > Research External
*Consult framework docs, best practices, academic literature.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| Context7 MCP | MCP | Yes — prevents re-researching known APIs | `resolve-library-id` → `query-docs` |
| OMC `researcher` agent (sonnet) | Agent | No | General doc/API research |
| OMC `researcher-low` agent (haiku) | Agent | No | Quick doc lookups |
| Paper Search MCP | MCP | No | arXiv, PubMed, Semantic Scholar, etc. |
| Zotero MCP | MCP | Partially — papers persist in library | Citation management, fulltext search |
| NotebookLM MCP | MCP | Yes — sources persist in notebooks | Grounded research with source management |
| `grounded-query` skill | Skill | Yes — uses NotebookLM for canonical answers | Prevents methodology hallucination |
| WebSearch / WebFetch | Built-in | No | General web research |
| `ask-gemini` command | Command | No | Alternative LLM perspective |

### Plan > Structure the Plan
*Organize research into an actionable plan.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| OMC `plan` skill | Skill (OMC) | No — plan is consumed, not persisted for reuse | Interview-based planning |
| OMC `ralplan` skill | Skill (OMC) | No | Planner + Architect + Critic consensus |
| superpowers `writing-plans` skill | Skill (plugin) | No | Structured plan writing |
| superpowers `brainstorming` skill | Skill (plugin) | No | Explore WHAT before HOW |
| OMC `planner` agent (opus) | Agent | No | Strategic planning |
| OMC `analyst` agent (opus) | Agent | No | Pre-planning requirements analysis |
| feature-dev `code-architect` | Agent (plugin) | No | Architecture blueprints |
| `gemini-brainstorm` command | Command | No | Brainstorming via Gemini |

---

## WORK

### Work > Execute Code Changes
*Implement the plan. Agents write code.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| OMC `executor-low` agent (haiku) | Agent | No | Single-line / simple changes |
| OMC `executor` agent (sonnet) | Agent | No | Standard feature implementation |
| OMC `executor-high` agent (opus) | Agent | No | Complex refactoring, multi-file |
| OMC `autopilot` skill | Skill (OMC) | No | Full autonomous execution |
| OMC `ralph` skill | Skill (OMC) | No | Persistence until verified complete |
| OMC `ultrawork` skill | Skill (OMC) | No | Maximum parallel execution |
| OMC `ecomode` skill | Skill (OMC) | No | Token-efficient parallel execution |
| OMC `ultrapilot` skill | Skill (OMC) | No | Parallel autopilot (3-5x faster) |
| OMC `swarm` skill | Skill (OMC) | No | N coordinated agents on task pool |
| `ast_grep_replace` | MCP (OMC bridge) | No | Structural code transformation |

### Work > Self-Test During Implementation
*Agent uses the app as it builds, iterates until it works.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| `lsp_diagnostics` | MCP (OMC bridge) | No | Single-file error checking |
| `lsp_diagnostics_directory` | MCP (OMC bridge) | No | Project-wide type checking |
| Bash (test runners) | Built-in | No | pytest, jest, cargo test, etc. |
| Bash (build commands) | Built-in | No | npm run build, tsc, make |

### Work > Cross-Interface Coordination
*Delegate to other Claude interfaces.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| Claude Desktop MCP | MCP (custom) | No | Send tasks to Desktop Claude |
| `claude-desktop-orchestration` skill | Skill | No | Coordinate Code ↔ Desktop |
| brain repo blackboard | Files (context/) | Partially — handoffs persist | File-based agent coordination |

### Work > Git Operations
*Branch management, commits, PRs.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| OMC `git-master` skill | Skill (OMC) | No | Atomic commits, rebasing |
| commit-commands `commit` | Skill (plugin) | No | Structured git commit |
| commit-commands `commit-push-pr` | Skill (plugin) | No | Boris's inner-loop pattern |
| commit-commands `clean_gone` | Skill (plugin) | No | Clean deleted remote branches |
| superpowers `using-git-worktrees` | Skill (plugin) | No | Isolated worktree setup |
| superpowers `finishing-a-development-branch` | Skill (plugin) | No | Branch completion workflow |

---

## ASSESS

### Assess > Automated Checks
*Linters, type checkers, test suites.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| `lsp_diagnostics` | MCP (OMC bridge) | No | File-level errors/warnings |
| `lsp_diagnostics_directory` | MCP (OMC bridge) | No | Project-wide type checking |
| Bash (linters, test suites) | Built-in | No | eslint, pytest, etc. |
| OMC `build-fixer` agent (sonnet) | Agent | No | Fix build/type errors |
| OMC `build-fixer-low` agent (haiku) | Agent | No | Simple build fixes |

### Assess > Code Review
*Multi-perspective quality evaluation.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| OMC `code-reviewer` agent (opus) | Agent | No — findings not persisted | Expert code review |
| OMC `code-reviewer-low` agent (haiku) | Agent | No | Quick code check |
| OMC `code-review` skill | Skill (OMC) | No | Comprehensive review workflow |
| superpowers `requesting-code-review` skill | Skill (plugin) | No | Review with requirements check |
| superpowers `receiving-code-review` skill | Skill (plugin) | No | Process review feedback |
| feature-dev `code-reviewer` | Agent (plugin) | No | Confidence-based filtering |
| code-simplifier | Agent (plugin) | No | Dedicated simplification pass |

### Assess > Security Review
*Security-focused evaluation.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| OMC `security-reviewer` agent (opus) | Agent | No | Deep security analysis |
| OMC `security-reviewer-low` agent (haiku) | Agent | No | Quick security scan |
| OMC `security-review` skill | Skill (OMC) | No | Comprehensive security review |

### Assess > Verification
*Evidence-based completion checks.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| superpowers `verification-before-completion` skill | Skill (plugin) | No | Evidence-before-claims checklist |
| OMC mandatory architect verification | Built-in (OMC) | No | Architect agent signoff |
| OMC `qa-tester` agent (sonnet) | Agent | No | Interactive CLI testing |
| OMC `qa-tester-high` agent (opus) | Agent | No | Production-ready QA |

### Assess > Debugging
*Systematic problem investigation.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| superpowers `systematic-debugging` skill | Skill (plugin) | No | Hypothesis-before-fix discipline |
| OMC `analyze` skill | Skill (OMC) | No | Deep analysis/investigation |
| OMC `architect` agent (opus) | Agent | No | Complex debugging |
| OMC `architect-medium` agent (sonnet) | Agent | No | Standard debugging |
| OMC `architect-low` agent (haiku) | Agent | No | Simple issue diagnosis |

---

## COMPOUND

### Compound > Capture Knowledge
*Extract and persist learnings from resolved problems.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| `compound-capture` skill | Skill (local) | **Yes** — writes to knowledge/solutions/ + AIM Memory | Core compound mechanism |
| `aim_memory_store` | MCP (AIM Memory) | **Yes** — persistent knowledge graph | Store entities and relations |
| `aim_memory_add_facts` | MCP (AIM Memory) | **Yes** | Add facts to entities |
| `aim_memory_link` | MCP (AIM Memory) | **Yes** | Link related knowledge |
| `obsidian_update_note` | MCP (Obsidian) | **Yes** — persists in vault | Update vault with learnings |

### Compound > Update System Instructions
*Feed learnings back into agent behavior.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| claude-md-management `revise-claude-md` | Skill (plugin) | **Yes** — updates CLAUDE.md | Audit and update instructions |
| claude-md-management `claude-md-improver` | Skill (plugin) | **Yes** | Quality audit of CLAUDE.md |
| hookify `hookify` | Skill (plugin) | **Yes** — creates behavior rules | Turn learnings into enforcement |
| `~/.claude/rules/*.md` | Files | **Yes** — auto-loaded every session | Modular instruction updates |
| CLAUDE.md (direct edit) | File | **Yes** | Manual instruction updates |

### Compound > CI-Based Compounding
*Capture learnings via GitHub automation.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| claude-code-action | GitHub Action (PENDING SETUP) | **Yes** — @claude on PRs → CLAUDE.md updates | Boris's pattern: review → learn → commit. Set up on first active code repo. |
| GitHub MCP (PR comments) | MCP | Partially — knowledge in PR comments | Queryable via gh API |

### Compound > Evaluate Tools & Methods
*Meta-compounding: improve the system itself.*

| Capability | Type | Compounds? | Notes |
|---|---|---|---|
| CE evaluation framework | Knowledge doc | **Yes** — reusable methodology | `knowledge/frameworks/compound-engineering-evaluation.md` |
| Capability registry (this doc) | Knowledge doc | **Yes** — keeps capability map current | Update when adding/removing tools |
| OMC `learner` skill | Skill (OMC) | **Yes** — extracts reusable skills from sessions | Turn repeated patterns into skills |

---

## CROSS-CUTTING (Serve Multiple Steps)

| Capability | Type | Steps Served | Notes |
|---|---|---|---|
| OMC `pipeline` skill | Skill (OMC) | Plan→Work→Assess | Sequential agent chaining with presets |
| OMC `designer` agents (low/med/high) | Agent | Work + Assess | UI/UX implementation + review |
| OMC `scientist` agents (low/med/high) | Agent | Plan + Work | Data analysis and research |
| OMC `writer` agent (haiku) | Agent | Compound | Documentation writing |
| OMC `vision` agent (sonnet) | Agent | Plan + Assess | Visual/media analysis |
| NotebookLM MCP | MCP | Plan + Compound | Research + source persistence |
| brain-system skill | Skill (local) | All | Brain repo coordination protocol |

---

## Maintenance
- **When adding a tool:** Add it to the relevant section with all columns filled
- **When removing a tool:** Delete the row, note removal in evaluation framework Application History
- **Quarterly review:** Check "Compounds?" column — if most of your active tools are "No", the system isn't compounding effectively
- **Experimentation tracking:** When trying different approaches for the same substep (e.g., OMC plan vs. superpowers brainstorming), record results in compound-capture so the registry can note which works better for what

---
*Generated: 2026-02-05 by claude-code*
*Last updated: 2026-02-05*
