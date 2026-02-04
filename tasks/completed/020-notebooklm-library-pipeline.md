---
name: notebooklm-library-pipeline
priority: 3
estimated_tokens: 15000
mode: plan-first
timeout: 20m
skill: plan
model_hint: sonnet
tags: [infrastructure, notebooklm, documentation]
depends_on: []
bead_id: brain-qms
---

# NotebookLM Library Documentation Pipeline

## Goal
Create queryable NotebookLM notebooks from user's library sources (Zotero, docs, notes).

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **Depends on:** None (auth resolved via shared Windows auth)
- **MCP tools needed:** notebook_create, notebook_list, source_add, notebook_query
- **Working dir:** ~/brain
- **Source locations:**
  - Zotero: Unknown - need to locate data directory
  - Obsidian: ~/div-vault/ or Windows path
  - Library docs: URLs or Context7 export

## Known Blockers
1. **File path translation:** Zotero PDFs likely on Windows, need /mnt/c/ paths
2. **Upload limits:** Large PDFs may timeout on source_add
3. **Source processing time:** NotebookLM processes async, need to poll
4. **User input required:** Don't know which sources to prioritize

## Workarounds Available
- `source_add` has `wait=True` and `wait_timeout` params for sync processing
- Can add URLs directly (no file path issues)
- Context7 MCP already provides library docs (may not need NotebookLM for those)

## User Decisions Needed
- [ ] Which Zotero collections/tags to include?
- [ ] Notebook structure: Single "Research Brain" vs domain-specific?
- [ ] Priority order: Research papers → Library docs → Notes?
- [ ] Start small (2-3 sources) or bulk import?

## Proposed Solution

### Phase 1: Inventory
1. List existing NotebookLM notebooks (avoid duplicates)
2. Locate Zotero data directory
3. List available Obsidian export candidates

### Phase 2: Structure Decision
Based on user input, create either:
- **Option A:** Single notebook "Research Brain" with all sources
- **Option B:** Domain notebooks: "Arterial Research", "ML/Feature Selection", "Python Libs"

### Phase 3: Source Ingestion
For each source type:

**Zotero PDFs:**
```
source_add(notebook_id, source_type="file", file_path="/mnt/c/...", wait=True)
```

**Library docs:**
```
source_add(notebook_id, source_type="url", url="https://docs.pycaret.org/...")
```

**Obsidian notes:**
```
source_add(notebook_id, source_type="text", text="...", title="Note: ...")
```

### Phase 4: Validation
- Query each notebook to verify sources indexed
- Test citation grounding

## Success Criteria
- [ ] At least 1 notebook created with 3+ sources
- [ ] `notebook_query` returns grounded answer with citations
- [ ] Notebook IDs documented in registry file
- [ ] Ingestion workflow documented for adding future sources

## Fallback
If bulk import fails:
- Create single test notebook with 1 URL source
- Verify query works
- Document issues for iteration

## Output
- knowledge/config/notebooklm-notebooks.yaml (notebook registry)
- knowledge/research/notebooklm-pipeline.md (workflow docs)
