---
module: Arterial Analysis
date: 2026-02-12
problem_type: best_practice
component: tooling
symptoms:
  - "No defined tooling stack for research pipeline development"
  - "Pure CLI interaction insufficient for pipeline architecture design"
  - "Unclear what visual planning tools integrate with CC without burning extra API tokens"
  - "Multiple tool options across planning, data management, and orchestration layers with no clear recommendation"
root_cause: missing_tooling
resolution_type: tooling_addition
severity: medium
tags: [tooling-stack, research-pipeline, visual-planning, markmap, mermaid, dvc, obsidian, matlab-python, local-first, open-source, hamilton, wandb, pandera, testing, validation]
---

# Best Practice: Research Pipeline Tooling Stack (MATLAB + Python + CC)

## Problem

Starting a fresh research pipeline project (arterial waveform analysis) with no defined tooling stack. Needed to determine: visual design/planning tools, data management, pipeline orchestration, code organization, and knowledge management — all fitting the philosophy of open source, local-first, minimal token cost, and integration with existing tools (Obsidian, Zotero, CC).

## Environment
- Module: Arterial Analysis (research pipeline)
- Languages: MATLAB (Windows) + Python (WSL)
- AI: Claude Code (CLI) — primary execution interface
- Knowledge: Obsidian vault, Zotero, brain repo
- Date: 2026-02-12

## Research Process

### Sources consulted
1. **awesome-context MCP** — awesome-reproducible-research, awesome-matlab, awesome-production-machine-learning, awesome-code-ai, awesome-claude-code
2. **GitHub MCP** — searched repos for open-source AI canvas/visual tools, checked stars/activity/READMEs
3. **Web search** — visual AI planning interfaces, Obsidian mindmap plugins, collaborative canvas tools
4. **CE best-practices-researcher agent** — produced 620-line guide at `knowledge/research/biomedical-signal-processing-codebase-organization.md`
5. **CE explorer agent** — mapped full project history across 7+ repos and Obsidian

### Tools evaluated and rejected

| Tool | Why rejected |
|------|-------------|
| **CodeGraph Context MCP** | Doesn't parse MATLAB; codebase too small to benefit |
| **Project Nodal** | Brand new (2 weeks old), no Claude API, burns separate API tokens |
| **flowith** | SaaS, burns separate API tokens |
| **Cove** | SaaS, burns separate API tokens |
| **Open Canvas (LangChain)** | Heavy deps (Supabase, LangGraph, LangSmith) — not local-first |
| **Tersa** | Heavy deps (Supabase, Stripe) — platform, not thinking tool |
| **Excalidraw** | JSON format is extremely token-heavy (~500 lines for simple diagram) |
| **Obsidian Canvas** | .canvas JSON is verbose (~150-200 lines for 6-node pipeline), expensive to generate via CC |
| **Kedro** | Overkill for single-researcher pipeline |
| **DataLad** | DVC covers the same use case more simply |

### Key decision criteria
1. **Open source and local-first** — no SaaS dependencies
2. **No extra API token cost** — visual layer driven by CC writing markdown, not separate AI calls
3. **Integrates with existing stack** — Obsidian, CC, Git
4. **Minimal token overhead** — Mermaid (10 lines) vs Canvas JSON (200 lines) vs Excalidraw (500 lines)

## Solution

### Recommended Stack

**Design & Planning Layer:**
- **Markmap** via Obsidian plugins (Mindmap Nextgen + Lovely Mindmap) — CC writes normal markdown with headings/lists, plugin renders interactive zoomable mind map. Token cost = identical to writing any markdown.
- **Mermaid** (native Obsidian) — for flow diagrams, data lineage, sequence diagrams when mind map isn't the right shape. Also minimal token cost.
- **Mehrmaid plugin** (optional) — renders `[[Obsidian links]]` inside Mermaid nodes, connecting diagrams to knowledge base.

**Data Management:**
- **DVC** (`pip install dvc`) — data versioning + pipeline DAG definition. Consensus pick across awesome-reproducible-research and awesome-production-ML.
- **`.gitignore` + DVC remote** — large raw data (580MB Control_Data) pushed to DVC remote, git stays lean.

**Pipeline Validation & Experiment Tracking:**
- **Hamilton** (`pip install sf-hamilton`) — Python function-level DAG with runtime validation. Uses `@check_output` decorator for range/type validation, `@config.when` for experiment variant switching, lifecycle adapters for W&B integration, `hamilton lint` for static DAG checking. Lightest Python DAG framework without plumbing overhead. Rejected alternatives: Kedro (heavier infrastructure, overkill for single researcher), Luigi (plumbing without validation), sklearn Pipelines (can't express complex DAG shapes), Prefect/Airflow (cloud-oriented, massive overhead).
- **W&B** (Weights & Biases) — experiment tracking and comparison for 180+ arterial experiments. Best comparison UI with automatic logging via Hamilton lifecycle adapter (custom WandbTracker class), config/metric/artifact tracking in one place. Rejected alternatives: MLflow (self-hosted complexity), Neptune (comparable but smaller ecosystem), DVC metrics only (too primitive for multi-experiment comparison).
- **Pandera** (`pip install pandera`) — DataFrame schema validation at data boundaries (MATLAB→Python handoff, feature matrix assembly). 12 dependencies vs Great Expectations' 107, first-class Hamilton integration via `@check_output(schema=...)`, lightweight for research use. Rejected alternatives: Great Expectations (massive dependency tree, enterprise-oriented), manual assertions (no reusable schemas, no integration).

**Pipeline Orchestration:**
- **`dvc.yaml`** — pipeline stages, dependencies, outputs. The pipeline definition IS the config.
- **JSON config** — shared settings between MATLAB and Python (both read natively).
- **File handoff pattern** — MATLAB writes `.mat` → `data/interim/` → Python reads. No cross-language calls.

**Code Organization:**
- **Pipeline-stage directories** (not language-based) — rejected `matlab/`, `python/` separation in favor of stage-based layout.
- **MATLAB +packages** — `+sigproc`, `+calib`, `+util` for namespace isolation instead of `addpath`.
- **Three-tier output management** — Tier 1: always save (averaged waveforms, features). Tier 2: save with cleanup (all beats). Tier 3: never save (debug/temp).

**Knowledge & Literature:**
- **Obsidian** — notes, decisions, methodology, pipeline maps (via Markmap)
- **Zotero + MCP** — papers, references
- **brain repo** — compound engineering docs, learnings
- **NotebookLM + MCP** — grounded queries against sources

**AI:**
- **Claude Code (CLI only)** — all execution, orchestration, research, planning
- **No separate API tools** — all visual output via Obsidian, not token-burning canvas apps

**Only new install required:** DVC (`pip install dvc`). Everything else is existing tools or Obsidian plugin toggles.

## Why This Works

1. **Token-minimal visual planning** — Markmap renders normal markdown as mind maps. Writing a pipeline architecture costs the same tokens as writing any text. Compare: Mermaid ~10 lines, Canvas JSON ~200 lines, Excalidraw ~500 lines.
2. **CC drives everything** — no separate AI backend consuming API credits. CC writes markdown → Obsidian renders visuals.
3. **Already integrated** — Obsidian is the existing knowledge base, DVC works with git, JSON config is readable by both MATLAB and Python.
4. **Local-first** — nothing leaves the machine. No SaaS, no cloud dependencies.
5. **One new tool** — DVC is the only net-new install. Low adoption friction.
6. **Full coverage from function to pipeline** — Hamilton validates within Python, DVC validates across languages, Pandera validates at boundaries, W&B tracks experiment results. Every layer is covered.

## Prevention

- **Evaluate token cost of visual formats before adopting** — JSON-heavy formats (Canvas, Excalidraw) are expensive for AI to generate
- **Prefer text-first visual tools** — Markmap and Mermaid take plain text input, making them ideal for AI-driven workflows
- **Don't add tools that burn separate API tokens** — visual planning should use the same AI context, not a parallel connection
- **Research before committing** — use awesome-context MCP, GitHub MCP, and web search to evaluate tools before installing

## Related Issues

- See also: [Arterial Analysis Data Provenance and Pipeline Rebuild](../workflow-issues/2026-02-12-arterial-analysis-data-provenance-rebuild.md) — the project context that led to this tooling decision
- Reference: `knowledge/research/biomedical-signal-processing-codebase-organization.md` — CE researcher agent's 620-line best practices guide
