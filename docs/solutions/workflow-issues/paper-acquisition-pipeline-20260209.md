---
module: System
date: 2026-02-09
problem_type: workflow_issue
component: tooling
symptoms:
  - "No established workflow for acquiring papers from discovery through to grounded Q&A"
  - "Manual steps between paper search, download, Zotero import, and NLM upload"
  - "No tracking of paper acquisition status across pipeline stages"
root_cause: missing_workflow_step
resolution_type: workflow_improvement
severity: high
tags: [paper-pipeline, zotero, notebooklm, paper-search, research-workflow, literature-review]
---

# Troubleshooting: Paper Acquisition Pipeline — End-to-End Workflow

## Problem
No established automated workflow existed for moving papers from discovery (search) through to grounded Q&A in NotebookLM. Each step was manual and disconnected, making batch literature reviews inefficient.

## Environment
- Module: System (research tooling)
- Tools: Paper Search MCP, Zotero MCP, NotebookLM MCP, zotero-import.py
- Date: 2026-02-09

## Symptoms
- Papers discovered via search but not systematically tracked
- No connection between Zotero library and NLM notebooks
- Manual file management for PDFs in downloads/
- No registry tracking which papers are at which pipeline stage

## What Didn't Work

**Attempted Solution 1:** Chaining Zotero→NLM (using Zotero file paths as NLM input)
- **Why it failed:** Zotero stores files in its own internal directory structure with hashed paths. NLM's `source_add(type=file)` needs a direct file path. The two systems are parallel consumers of the same staging directory, not sequential.

## Solution

**Architecture: Parallel pipeline from shared staging directory.**

```
Discovery (Paper Search MCP / WebSearch)
    ↓
  downloads/          ← staging directory
    ↓                ↓
  Zotero             NotebookLM
  (metadata)         (grounded Q&A)
    ↑                ↑
  zotero-import.py   source_add(type=file)
```

**Three components established:**

### 1. Paper Registry (`knowledge/tools/paper-registry.yaml`)
Tracks every paper through pipeline stages:
```yaml
papers:
  author-year:
    title: "..."
    doi: "..."
    download:
      method: curl_direct|arxiv_download|search_scihub|needs_chrome
      file: filename.pdf
      verified: true|false
    zotero:
      status: not_imported|imported|exists
      item_key: XXXXXXXX
    nlm:
      status: not_uploaded|uploaded
      notebook: notebook-name
      source_id: uuid
    tags: [tag1, tag2]
```

### 2. Zotero Import Script (`tools/scripts/zotero-import.py`)
```bash
# By DOI (fetches metadata from CrossRef):
python3 tools/scripts/zotero-import.py --doi "10.1371/journal.pone.0224365"

# By arXiv ID:
python3 tools/scripts/zotero-import.py --arxiv "2201.00494"

# Manual entry:
python3 tools/scripts/zotero-import.py --manual --title "Paper" --authors "Last,First"

# With tags:
python3 tools/scripts/zotero-import.py --doi "10.xxxx/yyyy" --tags "tag1,tag2"
```
Requires Zotero desktop running (connector at localhost:23119).

### 3. NLM Upload (via MCP tool)
```
source_add(notebook_id="...", source_type="file",
           file_path="/home/div/brain/downloads/paper.pdf", wait=True)
```
Returns source_id for tracking in registry.

**Batch acquisition workflow:**
1. Search → collect DOIs/arXiv IDs
2. Download PDFs to `downloads/`
3. Run `zotero-import.py` for metadata (parallel with step 4)
4. Run `source_add(type=file)` for each PDF to target NLM notebook
5. Update `paper-registry.yaml` with status at each stage
6. Query NLM notebook for grounded answers

## Why This Works

1. **ROOT CAUSE:** The tools (Paper Search, Zotero, NLM) are independent systems with no native integration. The pipeline needed explicit orchestration with a shared staging directory and a tracking registry.

2. **Parallel not sequential:** Zotero and NLM serve different purposes (metadata/citation management vs. grounded Q&A). They both consume PDFs from the staging directory independently, so chaining them sequentially would add latency with no benefit.

3. **Registry as single source of truth:** The YAML registry makes pipeline state visible and resumable. If a session is interrupted, the next session can check the registry and resume from where each paper left off.

## Prevention

- **Always update paper-registry.yaml** when adding papers at any stage. The registry prevents duplicate work and enables batch operations.
- **Use the review document pattern** (`knowledge/research/model-family-papers-review.md`) for large literature searches: organize by model/topic, tier by importance, get user checkpoint before batch acquiring.
- **Rate limit awareness:** Paper Search MCP (Semantic Scholar) has a free-tier limit of ~20 req/min. Google Scholar rate-limits after 3-4 parallel calls. Stagger searches or use WebSearch as fallback.
- **arXiv IDs:** Always use HTTPS URLs for arXiv API. See `integration-issues/arxiv-api-timeout-zotero-import-20260209.md`.

## Related Issues

- See also: [arxiv-api-timeout-zotero-import-20260209.md](../integration-issues/arxiv-api-timeout-zotero-import-20260209.md)
