# NotebookLM Upload Skill

Add sources to NotebookLM notebooks. Works with URL, text, or file uploads.

## Quick Reference

```python
# 1. Find notebook ID from registry
import yaml
with open("~/.config/notebooklm/notebooks.yaml") as f:
    reg = yaml.safe_load(f)
notebook_id = reg["notebooks"]["taiwan-arterial"]["id"]

# 2. Add source
mcp__notebooklm-mcp__source_add(
    notebook_id=notebook_id,
    source_type="url",  # or "text" or "file"
    url="https://example.com/paper",
    wait=True  # Wait for processing
)
```

## Source Types

### URL (Web pages, YouTube)
```python
source_add(
    notebook_id="<uuid>",
    source_type="url",
    url="https://arxiv.org/abs/...",
    wait=True
)
```

### Text (Markdown, notes)
```python
source_add(
    notebook_id="<uuid>",
    source_type="text",
    text="# Title\n\nContent here...",
    title="My Note",
    wait=True
)
```

### File (PDF, audio, text files)
```python
source_add(
    notebook_id="<uuid>",
    source_type="file",
    file_path="/path/to/paper.pdf",
    wait=True
)
```

## Notebook Registry

| Name | ID | Keywords |
|------|----|---------|
| taiwan-arterial | 2b000f61-d126-4ad7-b61b-61ebde9538de | arterial, PWV, stiffness |
| stability-selection | d2c53446-43ca-4714-832d-5e1730b98938 | features, lasso, high-dim |
| ml-science | 16a6da78-82f5-49f6-b672-a123baa34bc1 | ML, methodology |
| cross-validation | 58ea2b83-d94a-41f9-89ac-54ae690c446f | CV, model selection |
| arterial-waveform | 72569268-4408-4117-a70b-8bad8ee24d64 | waveform, features |
| interpretability | 6f6df8fe-4544-4598-adfb-993013445c63 | XAI, explainability |

## Batch Upload Pattern

```python
urls = [
    "https://arxiv.org/abs/paper1",
    "https://arxiv.org/abs/paper2",
]
for url in urls:
    result = source_add(
        notebook_id=notebook_id,
        source_type="url",
        url=url,
        wait=True,
        wait_timeout=180
    )
    print(f"{url}: {result}")
```

## Error Handling

- **Auth error**: Run `nlm login` or `/mnt/c/Users/din18/.local/bin/notebooklm-mcp-auth.exe`
- **Timeout**: Increase `wait_timeout` for large files
- **Invalid URL**: NotebookLM can't scrape all sites; try PDF download instead

## Integration with Zotero

```python
# Get PDF path from Zotero attachment
attachments = mcp__zotero__zotero_get_item_children(item_key="ABC123")
pdf_path = next(a["path"] for a in attachments if a["contentType"] == "application/pdf")

# Upload to NotebookLM
source_add(
    notebook_id=notebook_id,
    source_type="file",
    file_path=pdf_path,
    wait=True
)
```
