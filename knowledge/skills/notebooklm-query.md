# NotebookLM MCP Tool Reference

Query notebooks, manage sources, configure chat, and generate artifacts — all without loading content into context.

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

See `~/.config/notebooklm/notebooks.yaml` for full registry (11 notebooks as of 2026-02-08).

Key notebooks for arterial project:

| Name | ID | Keywords | Sources |
|------|----|----------|---------|
| taiwan-arterial | 2b000f61 | arterial, stiffness, PWV | 21 |
| stability-selection | d2c53446 | features, lasso, high-dim | 16 |
| arterial-waveform | 72569268 | waveform, features | 7 |
| pareto-model-selection | e7b3cc25 | pareto, stability, CV, small sample | 7 |
| cross-validation | 58ea2b83 | CV, model selection | 4 |
| ml-science | 16a6da78 | ML, science, methodology | 10 |
| interpretability | 6f6df8fe | XAI, explainability | 4 |

## Query Prompting Best Practices (tested 2026-02-08)

### Query Style Comparison

| Style | Example | Result Quality | When to Use |
|-------|---------|---------------|-------------|
| **Comparative** | "What are the key methodological differences between X and Y? Cite specific sources." | Excellent — structured with numbered sections, [1]-[4] citations | Comparing methods, understanding trade-offs |
| **Applied/contextual** | "For a dataset with N=179, p=545 highly correlated features, what does the literature recommend for feature selection with Ridge?" | Excellent — actionable recommendations with literature backing, 3-stage answer | Getting advice grounded in your specific problem |
| **Exhaustive enumeration** | "List all feature selection methods mentioned across all sources. For each, note model families and limitations." | Outstanding — comprehensive table-like output, dozens of methods with citations per entry | Building inventories, mapping the landscape |
| **Scope-testing** | "Is stability selection appropriate for tree-based models? What does the literature say about applying it beyond LASSO?" | Excellent — honestly reports what sources DO and DON'T cover, fills gaps with related evidence | Checking if your sources cover a topic |
| **Constrained format** | "Summarize in 3 bullet points: what is the irrepresentable condition and why does it matter?" | Good — respects the format constraint, still includes citations | Quick answers, specific facts |
| **Vague/broad** | "stability selection" | Surprisingly comprehensive — 40 citations, full structured overview | Exploring what your notebook knows about a topic |

### Key Findings

1. **Citation forcing works**: Adding "Cite specific sources" to any query increases citation density. But NLM cites well even without being asked.

2. **Contextual queries are the killer feature**: Giving your exact data characteristics (N, p, correlation structure) in the query produces advice that is both grounded in literature AND tailored to your problem. This is better than asking a generic question and applying it yourself.

3. **Enumeration queries are powerful**: "List all X mentioned across all sources" produces comprehensive inventories that would take hours to compile manually. Use these for landscape mapping.

4. **Vague queries still work**: Even a 2-word query like "stability selection" produces a structured, well-cited response. NLM doesn't need perfect prompts. But specific queries get more targeted answers.

5. **Honest about coverage gaps**: When sources don't explicitly cover something (e.g., stability selection for trees), NLM says so rather than hallucinating — then provides the closest related evidence.

6. **Conversation threading**: Pass `conversation_id` from a previous response for follow-up questions within the same context.

### Recommended Query Patterns for Research

| Research Phase | Query Pattern | Example |
|---------------|--------------|---------|
| **Landscape mapping** | "List all [X] mentioned. For each, note [Y] and [Z]." | "List all feature selection methods. For each, note model families and limitations." |
| **Method comparison** | "What are the key differences between [A] and [B]? Cite sources." | "Differences between stability selection and nested CV for feature selection?" |
| **Applied recommendation** | "For [your data characteristics], what does the literature recommend for [task]?" | "For N=179, p=545, correlated features, what FS approach for Ridge?" |
| **Gap detection** | "Does the literature address [specific question]?" | "Is there evidence on stability selection for tree-based models?" |
| **Synthesis** | "What consensus emerges across sources about [topic]?" | "What consensus on handling correlated features in high-dimensional selection?" |

### Anti-Patterns

- **Don't ask about things not in sources**: NLM only queries uploaded sources. If you need external knowledge, use WebSearch or Paper Search first, upload to NLM, then query.
- **Don't ask yes/no questions**: Open-ended questions produce richer responses.
- **Don't combine too many sub-questions**: One focused question per query works better than "tell me about A, B, C, and D".

## Full NLM MCP Tool Inventory (tested 2026-02-08)

### Querying & Analysis

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `notebook_query` | Ask AI about sources in a notebook | Yes | Primary tool. Returns grounded answers with [N] citations. Supports `conversation_id` for follow-ups, `source_ids` to scope. |
| `notebook_describe` | AI-generated notebook summary | Yes | Returns brief summary + suggested topics. Good for quick "what's in this notebook?" |
| `source_describe` | AI-generated source summary + keywords | Yes | Returns summary paragraph + keyword chips. Good for cataloging individual papers. |
| `source_get_content` | Raw indexed text of a source | Yes | Returns the text NLM indexed (not AI-processed). For URL sources, returns the web page text, not linked PDFs. |
| `chat_configure` | Set notebook chat persona/length | Yes | `goal`: default/learning_guide/custom. `custom_prompt` up to 10K chars. `response_length`: default/longer/shorter. Persists per notebook. Reset after use. |

### Source Management

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `source_add` | Add URL, text, file, or Drive source | Yes | `source_type`: url/text/file/drive. `wait=True` blocks until processed. URL sources index the page + linked content. |
| `source_delete` | Remove a source permanently | No | Requires `confirm=True`. Irreversible. |
| `source_list_drive` | List Drive sources for sync | No | For Google Drive-linked sources. |
| `source_sync_drive` | Re-sync Drive sources | No | Requires `confirm=True`. |

### Research (Web/Drive Search → New Sources)

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `research_start` | Search web or Drive for new sources | No | `mode`: fast (~30s, ~10 sources) or deep (~5min, ~40 sources). Creates or adds to a notebook. |
| `research_status` | Poll research progress | No | Blocks until complete or timeout. Use `compact=True` to save tokens. |
| `research_import` | Import discovered sources into notebook | No | Call after `research_status` shows completed. Can select specific `source_indices`. |

**Research workflow**: `research_start` → poll `research_status` → `research_import`. This is NLM's built-in web search — finds and adds sources automatically. Potentially very powerful for literature discovery but untested.

### Notes

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `note` | Create/list/update/delete notes in notebook | Partial | `action`: create/list/update/delete. Notes are user-created content within a notebook (not source-derived). Tested list (returned empty). |

### Artifact Generation (Studio)

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `studio_create` | Generate artifacts from notebook sources | No | Types: audio (podcast), video, infographic, slide_deck, report, flashcards, quiz, data_table, mind_map. Each has sub-options (format, length, difficulty). Requires `confirm=True`. |
| `studio_status` | Poll artifact generation progress | No | Must poll after `studio_create`. |
| `download_artifact` | Download generated artifacts | No | Supports all artifact types. Output formats: PDF, PNG, MP3/MP4, JSON/markdown/HTML for quizzes. |

### Notebook Management

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `notebook_list` | List all notebooks | Yes | Returns IDs, titles. Used for auth verification. |
| `notebook_get` | Get notebook details with sources | Yes | Returns source list with IDs, titles. |
| `notebook_create` | Create new notebook | No | Returns notebook_id. |
| `notebook_rename` | Rename a notebook | No | |
| `notebook_delete` | Delete notebook permanently | No | |
| `notebook_share_*` | Share settings | No | Public sharing, invites, status check. |

### Auth

| Tool | Purpose | Tested | Notes |
|------|---------|--------|-------|
| `save_auth_tokens` | Save cookies for auth | Yes | Fallback method. See `knowledge/tools/notebooklm-auth-notes.md`. |
| `refresh_auth` | Refresh authentication | No | |
| `server_info` | MCP server status | No | |

## Tool Combinations for Research Workflows

### 1. Literature-Grounded Q&A (primary workflow)
```
source_add (upload paper) → notebook_query (ask questions) → get cited answers
```

### 2. Landscape Discovery
```
research_start(query="topic", mode="deep") → research_status → research_import → notebook_query
```

### 3. Paper Cataloging
```
source_add (upload) → source_describe (get summary + keywords) → log to paper-registry.yaml
```

### 4. Custom Research Advisor
```
chat_configure(goal="custom", custom_prompt="You are a...") → notebook_query → reset chat_configure
```

### 5. Study Material Generation
```
studio_create(artifact_type="report", report_format="Study Guide") → studio_status → download_artifact
```
