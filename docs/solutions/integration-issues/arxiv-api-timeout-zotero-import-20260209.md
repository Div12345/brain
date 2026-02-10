---
module: System
date: 2026-02-09
problem_type: integration_issue
component: tooling
symptoms:
  - "TimeoutError: The read operation timed out on arXiv API query"
  - "zotero-import.py --arxiv hangs for 15s then fails for arXiv ID 2106.02521"
  - "DOI imports via CrossRef work fine, only arXiv imports fail"
root_cause: config_error
resolution_type: code_fix
severity: medium
tags: [arxiv, api-timeout, http-redirect, zotero-import, paper-pipeline]
---

# Troubleshooting: arXiv API Timeout in zotero-import.py

## Problem
The `zotero-import.py` script's arXiv import function timed out consistently when fetching metadata from the arXiv API. DOI imports via CrossRef worked fine, isolating the issue to arXiv API communication.

## Environment
- Module: System (tooling)
- Script: `tools/scripts/zotero-import.py`
- Python: 3.12
- Date: 2026-02-09

## Symptoms
- `TimeoutError: The read operation timed out` on `urllib.request.urlopen`
- Only arXiv imports affected (DOI/CrossRef imports work)
- Consistent failure on arXiv ID `2106.02521` (Bodinier 2023)
- First arXiv import (`2201.00494`) sometimes succeeded, second always failed

## What Didn't Work

**Attempted Solution 1:** Retrying the same request multiple times
- **Why it failed:** The timeout was structural (HTTP→HTTPS redirect consuming the 15s budget), not transient network issues.

## Solution

Two changes to `tools/scripts/zotero-import.py`:

**Code changes:**
```python
# Before (broken):
ARXIV_URL = "http://export.arxiv.org/api/query?id_list={}"
# ... later in fetch_arxiv():
with urllib.request.urlopen(req, timeout=15) as resp:

# After (fixed):
ARXIV_URL = "https://export.arxiv.org/api/query?id_list={}"
# ... later in fetch_arxiv():
with urllib.request.urlopen(req, timeout=30) as resp:
```

**Line references:**
- `tools/scripts/zotero-import.py:34` — URL scheme change
- `tools/scripts/zotero-import.py:93` — timeout increase

## Why This Works

1. **ROOT CAUSE:** The arXiv API URL used `http://` which triggers a 301 redirect to `https://`. Python's `urllib.request` follows redirects but the redirect handshake consumes a significant portion of the 15-second timeout budget. The actual API response from arXiv can take 5-10s for large papers, leaving insufficient time after the redirect.

2. **Fix 1 (https URL):** Eliminates the redirect entirely by going directly to the HTTPS endpoint. This saves 2-5s of redirect overhead.

3. **Fix 2 (30s timeout):** arXiv's API has variable response times depending on server load and paper complexity. 15s was marginal even without the redirect. 30s provides sufficient headroom.

## Prevention

- **Always use HTTPS URLs for API endpoints** — never rely on HTTP→HTTPS redirects in automated scripts. The redirect overhead is unpredictable and wastes timeout budget.
- **Set API timeouts to at least 2x the expected response time** — arXiv can take 5-15s, so 30s is appropriate.
- **Test with multiple IDs** — the first import may succeed if arXiv has the result cached, masking timeout issues that appear on subsequent uncached requests.

## Related Issues

No related issues documented yet.
