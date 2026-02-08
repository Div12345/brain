# NotebookLM Knowledge System Design

**Date:** 2026-02-04
**Status:** Ready for implementation
**Brainstormed with:** Claude Desktop + Claude Code

## Goal

Use NotebookLM as a vetted, canonical knowledge base that agents query to prevent hallucinations. Only curated knowledge goes in - Div is the curator.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│ CLAUDE.md          → "What to do" (instructions)    │
│ knowledge-graph    → "What's true" (facts)          │
│ canonical-decisions→ "Why it's true" (rationale)    │
│ NotebookLM         → Deep queries with citations    │
└─────────────────────────────────────────────────────┘
```

## Notebook Taxonomy

| Type | Examples | Content |
|------|----------|---------|
| Per-project | `arterial-compliance`, `cardiac-output` | 5-10 canonical papers, project-specific methodology |
| Per-domain | `ml-validation-methods`, `biomedical-signal-processing` | Stable reference material, shared across projects |
| Canonical-decisions | Single notebook | Cross-project methodology decisions with rationale |

## Files to Create

### Phase 0: Registry Enhancement

**File:** `~/.config/notebooklm/registry.yaml`

Enhance existing notebooks.yaml with source tracking:

```yaml
notebooks:
  taiwan-arterial:
    id: "2b000f61-d126-4ad7-b61b-61ebde9538de"
    title: "Taiwan Group - Arterial Stiffness & Central BP Literature"
    keywords: [arterial, stiffness, PWV, Taiwan]
    sources:
      - source_id: "src_abc123"
        origin: "zotero://item/XYZ789"
        title: "Smith 2019 - Arterial Stiffness Methods"
        synced_at: "2026-02-04T10:00:00Z"
        local_hash: "sha256:..."
```

### Phase 1: Routing Config

**File:** `~/.config/notebooklm/routing.yaml`

```yaml
# Project → Notebook routing for agents
projects:
  arterial-compliance:
    primary: "taiwan-arterial"
    also_query:
      - "canonical-decisions"
      - "ml-validation-methods"
    zotero_fallback: "Arterial-Compliance"

  cardiac-output:
    primary: "cardiac-output"  # TBD - create notebook
    also_query:
      - "canonical-decisions"
      - "biomedical-signal-processing"
    zotero_fallback: "Cardiac-Output"

  brain:
    primary: "brain-system"  # TBD - create notebook
    also_query:
      - "canonical-decisions"
    zotero_fallback: null

# Default for unknown projects
default:
  primary: "canonical-decisions"
  also_query: []
```

### Phase 1: Grounded Query Skill

**File:** `~/.claude/skills/grounded-query/SKILL.md`

```markdown
---
name: grounded-query
description: Query NotebookLM for grounded answers before making methodology decisions
triggers: ["ground this", "check canonical", "what does the literature say"]
---

# Grounded Query Skill

Query the NotebookLM knowledge base for vetted answers.

## Usage

When making methodology decisions, query first:

1. Load routing.yaml to find relevant notebooks
2. Query primary notebook
3. If no answer, cascade to also_query notebooks
4. If still no answer, check Zotero (flag as unvetted)
5. Log gaps for unanswered queries

## Implementation

[Agent follows this pattern when needing grounded answers]
```

### Phase 2: Gap Tracking

**File:** `~/.config/notebooklm/gaps.yaml`

```yaml
# Automatically populated by grounded_query skill
gaps:
  - query: "What order ARX model for brachial-to-carotid TF?"
    count: 1
    first_seen: "2026-02-04"
    last_seen: "2026-02-04"
    contexts:
      - "arterial-compliance/src/transfer_function.py"
```

### Phase 3-4: NLM Sync Skill

**File:** `~/.claude/skills/nlm-sync/SKILL.md`

```markdown
---
name: nlm-sync
description: Review and sync candidates to NotebookLM
triggers: ["/nlm-sync", "sync to notebooklm", "update knowledge base"]
---

# NLM Sync Skill

## Commands

- `/nlm-sync check` - Show candidates and gaps (read-only)
- `/nlm-sync push` - Push approved candidates to NotebookLM

## Candidate Sources

1. Obsidian: Files in `vetted/` folder or with `#notebooklm` tag
2. Git: CLAUDE.md changes on main branch
3. Zotero: Items tagged `#notebooklm`

## Review Flow

1. Show each candidate with preview
2. User approves/rejects/edits
3. Approved items pushed via source_add
4. Registry updated with source tracking
```

## Curation Workflow

**"Ready" signals:**

| Source | Detection | Ready Signal |
|--------|-----------|--------------|
| Obsidian | mtime + path | In `vetted/` folder or `#notebooklm` tag |
| Git repos | git diff main | CLAUDE.md committed to main |
| Zotero | API | Tagged `#notebooklm` or in Curated collection |

## Agent Query Cascade

```
NotebookLM query (primary → also_query)
    │
    ├─ Has citations? → GROUNDED, proceed
    │
    └─ No answer? → Zotero search (show as unvetted)
                        │
                        └─ Nothing? → Log to gaps.yaml + proceed with caveat
```

## Gap Detection Rules

- Only log during "grounding mode" (methodology decisions)
- Min query length 20 chars
- Dedupe within 24h (increment count instead)
- Surface only gaps with count ≥ 2

## MVP Implementation Order

| Phase | What | Files | Est. Time |
|-------|------|-------|-----------|
| 0 | Registry enhancement | registry.yaml | 30 min |
| 1 | Routing + grounded_query | routing.yaml, SKILL.md | 2-3 hrs |
| 2 | Gap logging | gaps.yaml (auto) | Built-in |
| 3 | /nlm-sync check | nlm-sync/SKILL.md | 2 hrs |
| 4 | /nlm-sync push | (extend skill) | 2 hrs |

## Decision Log

- **Standalone CLI vs Claude Code skill:** Skill wins - matches how Div works
- **Auto-sync vs manual curation:** Manual - Div is the vetter
- **Per-project vs per-domain notebooks:** Hybrid - both serve different purposes
- **Raw PDFs vs synthesized notes:** Both - PDFs for "what did X say", synthesis for "what's the consensus"
