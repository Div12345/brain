# NotebookLM Source Patterns

**Date:** 2026-02-03
**Bead:** brain-qms
**Status:** Verified working

## Auth Setup

Auth requires headless Chrome on Windows. The auth script is at:
```
/mnt/c/Users/din18/.local/bin/notebooklm-mcp-auth.exe
```

**Important:** Port 9222 conflict with Claude Desktop debug mode. To refresh auth:
1. Stop Claude Desktop
2. Run `notebooklm-mcp-auth.exe`
3. Relaunch Claude Desktop with debug flags

Auth tokens cached to: `C:\Users\din18\.notebooklm-mcp-cli\auth.json`

## Source Types

### URL Source
```
source_add(
    notebook_id="<uuid>",
    source_type="url",
    url="https://example.com/page",
    wait=true  # waits for processing
)
```
**Works with:** Web pages, documentation sites
**Returns:** source_id, title (auto-extracted)

### Text Source
```
source_add(
    notebook_id="<uuid>",
    source_type="text",
    text="Your content here...",
    title="Display Title",
    wait=true
)
```
**Works with:** Any plain text content
**Returns:** source_id, title

### File Source (not tested yet)
```
source_add(
    notebook_id="<uuid>",
    source_type="file",
    file_path="/path/to/file.pdf",
    wait=true
)
```

### Drive Source (not tested yet)
```
source_add(
    notebook_id="<uuid>",
    source_type="drive",
    document_id="<google-doc-id>",
    doc_type="doc|slides|sheets|pdf"
)
```

## Querying

```
notebook_query(
    notebook_id="<uuid>",
    query="Your question here"
)
```
Returns grounded answer with citations [1], [2], etc.

## Test Results

| Operation | Status | Notes |
|-----------|--------|-------|
| notebook_list | ✓ | Returns all 27 notebooks |
| notebook_create | ✓ | Created "system-test" |
| source_add (url) | ✓ | PyCaret docs added |
| source_add (text) | ✓ | Custom text added |
| notebook_query | ✓ | Cross-references both sources |

## Notebooks Available

27 notebooks including:
- Taiwan Group - Arterial Stiffness & Central BP Literature (21 sources)
- Stability Selection for High-Dimensional Variable Identification (16 sources)
- Machine Learning: The Architecture of Scientific Discovery (10 sources)
- And more...

## Next Steps

- brain-jtj: Build registry system with notebook IDs
- brain-djh: Build upload script for batch operations
