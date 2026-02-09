# Paper Acquisition Workflow

**Date:** 2026-02-08
**Status:** Tested and documented

## Decision Tree

For any paper you need to download:

```
1. Is it open access? (PLOS ONE, BMC, Nature Comms, etc.)
   YES → curl direct from publisher (fastest, most reliable)
   NO  → continue to step 2

2. Is it on arXiv?
   YES → download_paper(paperId="<arxiv_id>", platform="arxiv")
   NO  → continue to step 3

3. Try sci-hub via search_scihub (NOT download_paper)
   search_scihub(doiOrUrl="<DOI>", downloadPdf=true)
   If fails → try with https://doi.org/ prefix:
   search_scihub(doiOrUrl="https://doi.org/<DOI>", downloadPdf=true)
   If still fails → continue to step 4

4. Fallback: Chrome manual download
   → Use Claude Desktop MCP or manual browser
   → Publisher sites (OUP, Wiley, Springer) block curl and sci-hub for older papers
```

## Key Findings from Testing

### What Works

| Method | Tool | Format | Reliability |
|--------|------|--------|------------|
| **arXiv download** | `download_paper(platform="arxiv")` | arXiv ID (e.g., "2201.00494") | HIGH — always works |
| **Open access curl** | `curl -sL -o file.pdf "<publisher_url>"` | Direct PDF URL | HIGH — for truly open access |
| **Sci-hub search** | `search_scihub(doiOrUrl=..., downloadPdf=true)` | DOI or `https://doi.org/DOI` | MEDIUM — works for some papers |

### What Does NOT Work

| Method | Why |
|--------|-----|
| `download_paper(platform="scihub")` | **BROKEN** — always returns "Cannot find PDF". Use `search_scihub` instead. |
| `search_papers(platform="scihub")` | Returns 0 results for direct searches |
| `search_papers(platform="semantic")` | Semantic Scholar API appears down/rate-limited |
| `curl` on OUP/Wiley/Springer | Cloudflare blocks → returns HTML error page |
| Sci-hub for old Biometrika/JRSSB | Many pre-2010 stats papers not indexed |

### URL Format Matters for Sci-Hub

| Format | Example | Result |
|--------|---------|--------|
| Bare DOI | `10.1111/j.1467-9868.2010.00740.x` | WORKED |
| `https://doi.org/` prefix | `https://doi.org/10.1198/106186005X59630` | WORKED (bare DOI failed!) |
| Sci-hub mirror URL | `https://sci-hub.ru/10.1371/...` | FAILED |
| Publisher abstract URL | `https://academic.oup.com/...` | FAILED |

**Rule:** Always try bare DOI first, then `https://doi.org/` prefix. The prefix format finds some papers the bare format misses.

## Discovery Tools

| Tool | Best for | Notes |
|------|----------|-------|
| `search_papers(platform="crossref")` | Finding DOIs, metadata, citation counts | Most reliable search. No full text. |
| `search_papers(platform="scholar")` | Finding papers when DOI unknown | Returns Google Scholar results. May find preprint URLs. |
| `search_papers(platform="arxiv")` | Finding arXiv preprints | Also gives direct PDF URLs |
| `search_papers(platform="pubmed")` | Biomedical papers | Good for clinical/medical literature |

## Working Sci-Hub Mirrors (as of 2026-02-08)

| Mirror | Response Time |
|--------|--------------|
| sci-hub.ru | 1075ms |
| sci-hub.st | 1089ms |
| sci-hub.ren | 1499ms |
| sci-hub.ee | 2026ms |
| sci-hub.mksa.top | 6340ms |

Check with `check_scihub_mirrors(forceCheck=true)` before assuming mirrors are down.

## Test Results (2026-02-08)

| Paper | Method Used | Result |
|-------|------------|--------|
| Vabalas 2019 (PLOS ONE) | curl direct (open access) | ✅ 1.3MB |
| Meinshausen 2010 (JRSSB) | search_scihub bare DOI | ✅ 11.5MB |
| Faletto & Bien 2022 | download_paper arxiv 2201.00494 | ✅ |
| Bodinier 2023 (sharp) | download_paper arxiv 2106.02521v2 | ✅ |
| Tibshirani 2005 (Fused LASSO) | All methods failed | ❌ Need Chrome |
| Chen & Chen 2008 (EBIC) | All methods failed | ❌ Need Chrome |

## Saved PDFs Location

`/home/div/brain/downloads/`

## Integration with Zotero

After downloading, import to Zotero:
```python
# Search Zotero first to check if already exists
zotero_search_items(query="Author Year Title")

# If not found, add via Zotero's web importer or manual import
# PDFs at /home/div/brain/downloads/ can be attached manually
```

## Integration with NotebookLM

After Zotero import:
```python
# Upload PDF to relevant notebook
source_add(
    notebook_id="<uuid>",
    source_type="file",
    file_path="/home/div/brain/downloads/paper.pdf",
    wait=True
)

# Or upload via URL if available
source_add(
    notebook_id="<uuid>",
    source_type="url",
    url="https://arxiv.org/abs/2201.00494",
    wait=True
)
```
