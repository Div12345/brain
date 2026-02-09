---
date: 2026-02-08
topic: arterial-search-space-constraints
tags: [ce/brainstorm, project/arterial, theme/methodology, theme/evaluation]
status: complete
related_plan: "docs/plans/2026-02-08-feat-arterial-methodology-framework-plan.md"
---

# Constraining the Arterial Analysis Search Space

## What We're Figuring Out

How to define, explore, and evaluate the prediction problem (N=179, p=545, correlated waveform features, 10 interpretable models) so that whatever we find is scientifically defensible — not an artifact of how we searched.

This is NOT a methods contribution. The core claim is **prediction performance** (cPP R²=0.858). The methodology framework exists as the **defense** — proving the result isn't cherry-picked, unstable, or an artifact of arbitrary choices.

## The Problem With the Current Approach

Every choice in the current pipeline is weakly justified:

| Choice | Current justification | Problem |
|--------|----------------------|---------|
| 10 interpretable models | "PyCaret had them" | Arbitrary threshold, no principled inclusion/exclusion |
| 5 PyCaret filters | Package defaults | No data-driven reason for these specific filters |
| Stepwise OLS | Convention | p-value ties resolved arbitrarily, unstable at p>>N |
| RMSE/R² only | Convention | Doesn't capture stability, parsimony, or Rashomon breadth |
| 545 features unstructured | "All extracted" | Ignores waveform topology, doesn't address collinearity |

A reviewer could ask: "Would different arbitrary choices give different results?" The answer is probably yes, and we can't defend against that without a principled framework.

## Key Insight: The Model Family Is the Fundamental Unit

Don't build one universal pipeline. Each model family has its own:
- Feature selection approach (B↔C entanglement differs)
- Appropriate meta-estimator (stability selection may not be right for all)
- Evaluation dimensions (coefficient stability for linear ≠ split stability for trees)
- Justification for inclusion

The framework should be **derived per family from data characteristics + model properties**, not assumed universal.

## Research Questions

### Structure: Two Layers

**Shared layer** (researched once):
- Universal evaluation dimensions that apply regardless of model family
- Data-driven constraints that all families must respect (N=179, p>>N, collinearity, topology)
- Cross-family comparison methodology
- Search boundary justification ("why these families and not others," "when is enough exploration enough")

**Per-family layer** (researched ×4 for MVP):
- Complete estimation strategy: FS approach + hyperparameter tuning + meta-estimator
- Family-specific evaluation dimensions beyond the shared set
- Family-specific metrics
- Justification: why this meta-estimator for this family? (Don't assume stability selection everywhere)

### The Per-Family Research Question (×4 MVP families)

> "For [model family], given data characteristics (N=179, p=545, ρ>0.9 adjacent features, waveform topology, interpretability required): what is the appropriate complete estimation strategy (feature selection + hyperparameter tuning + meta-estimator that ties them together), and what evaluation dimensions capture whether the result is good?"

Asked for:
1. **Linear (no regularization)** — OLS, Bayesian Ridge, Huber
2. **L1-regularized** — LASSO, Elastic Net
3. **L2-regularized** — Ridge, Kernel Ridge
4. **Tree-based** — Decision Tree

Deferred (future work): Non-parametric (KNN, SVM), Interpretable ML (imodels)

### The Cross-Cutting Research Question

> "How do you compare results across model families that use different estimation strategies and evaluation metrics? How do you justify the boundaries of your exploration (which families, how many methods per family, when is 'enough')? What does the literature say about systematic vs exhaustive exploration in small-sample clinical prediction?"

### Known Sub-Questions (confident these matter)

| Sub-question | Why confident | Existing knowledge |
|-------------|---------------|-------------------|
| Feature selection stability metrics | Core to the collinearity problem | Nogueira 2018 already in hand |
| Clinical prediction reporting guidelines | TRIPOD exists, may constrain evaluation | Not yet reviewed |
| Collinearity → FS constraints | Well-established in literature | Irrepresentable condition, cluster stability covered |
| B↔C entanglement per family | Already mapped in plan | Needs validation — is this our construction or established? |

### Unknown Sub-Questions (let research reveal)

- How to characterize Rashomon sets — is this standard practice or frontier?
- Whether there's a formal method to derive FS requirements from data characteristics
- What meta-estimators beyond stability selection exist per family
- How comparable biomedical ML papers justify their model/method scope
- Whether "sufficient exploration" has formal criteria or is always judgment
- Parsimony metrics beyond feature count
- Physiological coherence — formal or qualitative?

## Research Plan

### Phase 0: Tool Stack Hardening (separate session, ~2 hours)

**Goal:** Make the paper discovery → acquisition → grounded querying pipeline reliable.

**Components to fix:**

| Component | Current state | Target |
|-----------|--------------|--------|
| Paper Search → Sci-Hub download | Flaky. DOI/URL format inconsistencies | Decision tree: DOI → doi.org URL → sci-hub mirror variants → Chrome fallback |
| NotebookLM auth | Manual Windows cookie extraction | Scripted: one command refreshes auth, confirms working |
| NLM source upload | Untested for this session's papers | Verified: upload paper URL/PDF, confirm queryable |
| NLM query quality | Basic queries sometimes vague | Tested prompting patterns: citation-forcing, specific vs broad, multi-source |
| Zotero gaps | 5 key papers missing | All imported, tagged, full text attached |
| End-to-end | Never done | One paper: search → download → Zotero → NLM → grounded answer with citation |

**Critical first step:** Inventory existing docs in brain repo that already document parts of this workflow (docs/solutions/, CLAUDE.md, scattered notes). Consolidate before building new.

### Phase 1: Research Execution (separate session, ~4 hours)

**Approach:** High-level per family, dynamic execution. Don't pre-specify exact search terms — adapt based on what's found.

**Per-family research (×4):**

| Family | Key concepts to search | Primary sources | Good answer looks like |
|--------|----------------------|----------------|----------------------|
| Linear (no reg) | "feature selection OLS small sample", "stability selection linear regression", meta-estimators for unregularized models | NLM Stability Selection notebook, Paper Search | Complete estimation strategy with literature citations, evaluation metrics identified |
| L1-regularized | "LASSO stability selection calibration", "fused LASSO meta-estimation", regularization path as FS | NLM Stability Selection, existing plan Q1-Q2 answers | Whether stability selection wrapping L1 is best, or L1's own path suffices, with evidence |
| L2-regularized | "feature selection Ridge regression p>>N", "external selection for shrinkage models" | Paper Search, NLM | What FS approach pairs with Ridge when it doesn't select, validated meta-approach |
| Tree-based | "decision tree high-dimensional small sample", "feature pre-filtering trees nested CV" | Paper Search, Context7 (sklearn), existing plan Q3 answer | Evidence for/against pre-filtering, appropriate meta-estimator, tree-specific eval metrics |

**Cross-cutting research:**
- Search: "multi-criteria evaluation ML clinical prediction", "Rashomon set characterization", "model comparison small sample", "TRIPOD checklist feature selection"
- Sources: Paper Search, WebSearch, NLM after upload

### Phase 2: Synthesis (within research session or follow-up)

- Aggregate NLM answers into per-family strategy documents
- Identify shared evaluation dimensions vs family-specific
- Define the cross-family comparison methodology
- Update the methodology framework plan with grounded answers

## Decisions Made

1. **Core claim = prediction, methodology = defense** — Not a methods paper
2. **Model family is the fundamental unit** — No universal pipeline
3. **Don't pre-commit to stability selection for all families** — Research which meta-estimator fits each
4. **Evaluation dimensions are model-family-specific** — Shared + per-family layers
5. **Tool stack hardening BEFORE research** — Separate session, consolidate existing docs first
6. **Search strategy is dynamic** — High-level concepts per family, adapt during execution
7. **MVP = 4 families** (Linear, L1, L2, Tree) — Non-parametric and imodels deferred
8. **Don't pre-decompose unknown sub-questions** — Let research reveal structure

## Open Questions

- How does the existing plan (docs/plans/2026-02-08-feat-arterial-methodology-framework-plan.md) relate to this? Does it need rewriting or just augmenting?
- Should the hardening session also cover Claude Desktop → Chrome pipeline for manual paper access?
- How to handle the Monday presentation deadline — is this brainstorm's scope completable before Monday?
- NLM notebook organization: new notebook for this research or extend existing?

## Next Steps

1. **Tool stack hardening session** — Fix paper pipeline, NLM auth, consolidate existing workflow docs
2. **Research execution session** — Run per-family + cross-cutting research with hardened tools
3. **Synthesis** — Build the grounded methodology framework
4. **Update plan** — Revise `2026-02-08-feat-arterial-methodology-framework-plan.md` with findings

→ Run `/workflows:plan` after research is complete to structure the implementation.
