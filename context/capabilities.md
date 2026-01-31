---
created: 2026-01-31
tags:
  - context
  - capabilities
  - tools
status: active
updated: 2026-01-31
aliases:
  - system capabilities
  - what we can do
---

# Current Capabilities

> What the system can actually do right now.

## MCPs Available

| MCP | Capabilities | Status |
|-----|--------------|--------|
| **Obsidian** | Read/write vault, search, frontmatter, tags | ✅ Active |
| **Zotero** | Search papers, fulltext, annotations, semantic search | ✅ Active |
| **GitHub** | Repos, issues, PRs, file operations | ✅ Active |
| **Desktop Commander** | File system, processes, search, execute | ✅ Active |
| **AIM Memory** | Persistent knowledge graphs | ✅ Active |
| **Sequential Thinking** | Multi-step reasoning | ✅ Active |
| **Paper Search** | arXiv, PubMed, Semantic Scholar | ✅ Active |
| **Context7** | Library documentation lookup | ✅ Active |

## Agents Defined

| Agent | Purpose | Location |
|-------|---------|----------|
| **[[agents/overnight\|overnight]]** | Autonomous research, analysis | `agents/overnight.md` |
| **desktop** | Interactive via Claude.ai | Implicit |
| **claude-code** | Code-focused via CC | Implicit |

## What The System CAN Do

| Category | Specific Capabilities |
|----------|----------------------|
| **Analyze** | Read vault, extract patterns, identify friction |
| **Synthesize** | Combine information, generate insights |
| **Predict** | Anticipate needs based on patterns |
| **Build** | Create files, scripts, configs |
| **Document** | Write knowledge files, logs, proposals |
| **Search** | Web, vault, Zotero, GitHub, papers |
| **Remember** | Persistent memory via AIM MCP |

## What The System CANNOT Do (Yet)

| Gap | Potential Solution | Priority |
|-----|-------------------|----------|
| Calendar integration | Google Calendar MCP | Medium |
| Email access | Gmail MCP | Low |
| Automated scheduling | Cron/scheduler | Medium |
| Local code execution | CC hooks | High |

## What The System SHOULD NOT Do

See [[context/off-limits]] for full list.

## Capability Roadmap

### Phase 1: Foundation (Current)
- [x] Basic vault analysis
- [x] Pattern extraction
- [x] Agent architecture defined
- [x] Obsidian format conversion
- [x] CC hooks integrated (`.claude/settings.json`)

### Phase 2: Prediction
- [ ] Morning summaries
- [ ] Prediction accuracy >70%
- [ ] Resource pre-fetching

### Phase 3: Tool Building
- [ ] First custom hook
- [ ] First custom command
- [ ] Build-test-integrate loop

## Related
- [[context/ecosystem]] - Tool ecosystem
- [[context/priorities]] - Current work
- [[inspirations/claude-code-ecosystem]] - CC tools
