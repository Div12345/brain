# NotebookLM Query Skill

Query your NotebookLM notebooks without loading content into context.

## Quick Start

```python
# 1. Load registry
import yaml
with open("~/.config/notebooklm/notebooks.yaml") as f:
    registry = yaml.safe_load(f)

# 2. Find notebook by keyword
def find_notebook(keyword):
    for name, nb in registry["notebooks"].items():
        if keyword.lower() in " ".join(nb["keywords"]).lower():
            return nb["id"]
    return registry["notebooks"][registry["default_notebook"]]["id"]

# 3. Query
notebook_id = find_notebook("arterial")
result = notebook_query(notebook_id=notebook_id, query="Your question")
```

## For Agents

When user asks about research topics:

1. Check if keywords match a notebook in registry
2. Use `notebook_query` tool with that notebook ID
3. Return answer with citations

## Registry Location

`~/.config/notebooklm/notebooks.yaml`

## Available Notebooks

| Name | Keywords | Sources |
|------|----------|---------|
| taiwan-arterial | arterial, stiffness, PWV | 21 |
| stability-selection | features, lasso, high-dim | 16 |
| ml-science | ML, science, methodology | 10 |
| cross-validation | CV, model selection | 4 |
| arterial-waveform | waveform, features | 7 |
| interpretability | XAI, explainability | 4 |

## Query Tips

- Be specific: "What preprocessing steps are recommended for PWV data?"
- Ask follow-ups: Pass `conversation_id` from previous response
- Limit sources: Use `source_ids` to query specific sources only
