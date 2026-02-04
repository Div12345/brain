---
name: notebooklm-agent-tools
priority: 3
estimated_tokens: 12000
mode: autonomous
timeout: 15m
skill: ecomode
model_hint: sonnet
tags: [infrastructure, notebooklm, tools]
depends_on: [notebooklm-library-pipeline]
bead_id: brain-jtj
---

# NotebookLM Agent Query Tools

## Goal
Create token-efficient, repeatable workflows for agents to query NotebookLM notebooks.

## Environment Constraints
- **Execution env:** Any Claude Code session (WSL or Windows)
- **Depends on:** brain-qms / notebooklm-library-pipeline (notebooks must exist)
- **Working dir:** ~/brain
- **MCP tools needed:** notebook_query, notebook_list
- **Config location:** ~/.config/notebooklm/

## Known Blockers
1. **ID discovery overhead:** Without registry, each session wastes tokens finding notebook IDs
2. **Keyword matching complexity:** Simple grep vs semantic search tradeoff
3. **Stale registry:** Notebooks may be added/removed, registry gets outdated

## Workarounds Available
- YAML registry is human-editable and git-trackable
- Can add `last_verified` timestamp to detect staleness
- Simple keyword matching is good enough for small notebook count

## User Decisions Needed
- [ ] Registry format: YAML (readable) vs JSON (standard)?
- [ ] Query interface: Obsidian skill doc vs Claude Code skill vs bash script?
- [ ] Include auto-refresh of registry on first query?

## Proposed Solution

### Deliverable 1: Notebook Registry

Create `~/.config/notebooklm/notebooks.yaml`:
```yaml
# NotebookLM Notebook Registry
# Updated: 2026-02-03
# Use: Agents load this to avoid ID discovery overhead

notebooks:
  arterial-research:
    id: "abc123-..."
    description: "Arterial analysis research papers from Zotero"
    keywords: [arterial, vascular, blood flow, stenosis, carotid]
    source_count: 5
    last_verified: "2026-02-03"

  python-libs:
    id: "def456-..."
    description: "Python library documentation"
    keywords: [pycaret, pandas, sklearn, numpy, feature selection]
    source_count: 3
    last_verified: "2026-02-03"

default_notebook: arterial-research
```

### Deliverable 2: Query Workflow

Create `knowledge/skills/notebooklm-query.md`:
```markdown
# NotebookLM Query Workflow

1. Load ~/.config/notebooklm/notebooks.yaml
2. Match query keywords to notebook (or use default)
3. Call: notebook_query(notebook_id=<id>, query=<question>)
4. Return answer with citations
```

### Deliverable 3: Optional CLI Helper

Create `tools/scripts/nlm-query`:
```bash
#!/bin/bash
# Usage: nlm-query "keyword" "question"
# Routes to correct notebook based on keyword
```

## Success Criteria
- [ ] Registry file exists at ~/.config/notebooklm/notebooks.yaml
- [ ] Registry contains all notebooks from previous task
- [ ] Query workflow documented in knowledge/skills/
- [ ] Test query via workflow succeeds (verified in logs)
- [ ] Token cost per query: <500 tokens (no discovery overhead)

## Fallback
If complex matching fails:
- Simple hardcoded notebook ID in workflow
- User specifies notebook name explicitly
- Minimum: documented IDs that agents can reference

## Output
- ~/.config/notebooklm/notebooks.yaml (registry)
- knowledge/skills/notebooklm-query.md (workflow)
- tools/scripts/nlm-query (optional CLI)
