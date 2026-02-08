---
title: "Arterial Analysis Methodology Framework"
type: feat
date: 2026-02-08
status: draft
tags: [ce/plan, project/arterial, theme/methodology, theme/feature-selection]
brainstorm: "Projects/arterial analysis/sessions/2026-02-07-monday-update-brainstorm.md"
task_ref: "Task 2 (Methodology Framework)"
---

# Arterial Analysis: Methodology Framework

## Overview

Define the complete ML pipeline structure for arterial waveform analysis — which feature selection methods pair with which model families, how they interact within nested CV, and what makes the framework defensible for publication. This is Task 2 from the Monday research update brainstorm.

**Key insight from brainstorm:** The gap is *problem formulation* (defining the pipeline structure per model family), not more broad literature searching. The existing notes are more complete than they feel.

## Problem Statement / Motivation

The arterial analysis project predicts central hemodynamic parameters (cSBP, cPP, cfPWV) from peripheral waveform features (N=179 train, p=545). The current pipeline uses stepwise OLS + PyCaret comparison across 180 experiments, but lacks a unified framework that:

1. Maps which feature selection approach is appropriate for each model family
2. Justifies choices with literature for publication
3. Defines how stability selection, the B↔C entanglement, and nested CV interact
4. Resolves the "perfectionism on methodology" blocker identified in the Feb 6 session

## What Already Exists (Inventory)

### Decisions Already Made (Feb 6 Session)
- Sequential pipeline: stability-based feature selection THEN model tuning, inside nested CV
- Primary evaluation: RMSE + feature selection frequency + model parsimony
- For LR: stability selection with LASSO base. For trees: native selection + importance stability reporting
- Skip AutoML — manual pipeline gives interpretability needed
- Post-hoc corrections: defer until results exist

### Literature Coverage (Synthesis Note, Feb 1)
| Gap | Status | Solution |
|-----|--------|----------|
| Gap 1: Topology (waveform continuity) | Covered | Fused LASSO (Tibshirani 2005) |
| Gap 2: Post-selection inference | Covered | Lee 2016 POSI |
| Gap 3: Non-linearity check | Covered | HSIC-Lasso (Yamada 2014) |
| Gap 4: Interactions | Deferred | Too complex for N=179 |
| Gap 5: Collinear flipping (CRITICAL) | Covered | Cluster Stability Selection (Faletto & Bien 2022) |
| Gap 6: Causality | Deferred | Needs multi-environment data |

### Current Pipeline (L5-Modeling)
- Stage 1: Stepwise OLS (in-fold selection, no leakage)
- Stage 2: PyCaret (10 models x 5 filters, pre-CV filtering — potential leakage)
- 3x3 experiment design per target
- Hamilton DAG architecture

### Existing Knowledge Notes
- `Feature Selection Methods Comparison` — full taxonomy with low-N recommendations
- `ML Pipeline Taxonomy` — A (Specification) / B (Computation) / C (Assessment) / D (Post-hoc) structure
- `Feature Selection Methodology Decision` — concrete recommendations (Fused LASSO, Cluster Stability, EBIC, Selective Inference)
- `Synthesis - Current Understanding` — 6 gaps, papers extracted, critical reframing (cPP R²=0.858 beats clinical baseline by ~10%)

## Proposed Solution: Per-Family Pipeline Mapping

The core deliverable is a structured document that maps, for each model family, the complete pipeline from feature prep through evaluation.

### The A→B→C Framework (from brainstorm)

```
A (Feature Prep) → B (Feature Selection) → C (Model Fitting)
```

**Critical insight:** B and C are entangled, not strictly sequential. The relationship differs per model family.

### Model Families and Their Pipeline Structure (Grounded)

| Family | Models | B↔C Relationship | Feature Selection Approach | Literature Justification |
|--------|--------|-------------------|---------------------------|-------------------------|
| **Linear (no reg)** | OLS, Bayesian Ridge, Huber | B separate from C | Cluster Stability Selection (Randomized LASSO base, π≥0.9, q≈21) → then fit | Meinshausen 2010, Faletto & Bien 2022 |
| **L1-regularized** | LASSO, Elastic Net | B fused with C | Embedded L1 does selection. Wrap with Stability Selection as meta-layer. Consider Fused LASSO for topology | Meinshausen 2010, Tibshirani 2005, Philipp 2017 |
| **L2-regularized** | Ridge, Kernel Ridge | Shrinks, doesn't eliminate → needs external B | Same as Linear: Cluster Stability Selection → then fit with Ridge | Meinshausen 2010 |
| **Non-parametric** | KNN, SVM (RBF) | B separate from C | Stability Selection or correlation filter → reduced feature set → fit. **MVP: future work** | (defer) |
| **Tree-based** | Decision Tree | Implicit selection, but unreliable at p>>N | External pre-filtering INSIDE nested CV (~30 features) → then fit tree. Report importance stability. Use 1-SE rule for depth | Vabalas 2019, NotebookLM Q3 |
| **Interpretable ML** | imodels (RuleFit, SLIM, EBMs) | Own constraints | **MVP: future work** — different pipeline branches needed | (defer) |

### Stability Selection as Meta-Layer (D)

Stability selection sits ON TOP of B as a meta-method — not a 4th category alongside filter/wrapper/embedded:

```
D (Stability Selection meta-layer)
└── B (Base selector — LASSO, correlation filter, etc.)
    └── Run on many subsamples
    └── Keep features selected > π threshold (0.6-0.9)
```

For collinear waveform data, use **Cluster Stability Selection** (Faletto & Bien 2022):
1. Cluster 545 features by correlation (hierarchical, t≈0.3)
2. Run stability selection on cluster representatives
3. Report cluster-level stability, not individual feature

### Nesting Structure

```
C1 (Outer CV — generalization estimate, 5-fold)
└── C2 (Inner CV — selection + tuning)
    └── D (Stability selection — subsample loop)
        └── B (Base selector per model family)
            └── A + C_fit (Feature prep + Model fit)
```

**Key rule:** Everything data-dependent must be inside the evaluation loop to be honest.

## Specific Gaps to Fill (Not "need more research" — "need to know X about Y")

### Gap A: Fused LASSO as base selector in stability selection
- **Question:** Can Fused LASSO serve as the base selector inside stability selection? Or does the adjacency penalty conflict with subsampling?
- **Why it matters:** If yes, this elegantly solves Gap 1 (topology) + Gap 5 (collinearity) together
- **Where to look:** Meinshausen & Buhlmann 2010 (do they discuss structured base selectors?), Fused LASSO implementations
- **Tool:** NotebookLM stability selection notebook, or targeted paper search

### Gap B: Practical stability selection calibration for N=179
- **Question:** What are sensible values for π threshold and λ regularization when N=179 and p=545?
- **Why it matters:** Default π=0.6 and arbitrary λ could be too conservative or too liberal
- **Where to look:** Nouraie & Muller 2025 (stabplot calibration), Bodinier 2025 (sharp auto-calibration)
- **Tool:** Zotero (both papers confirmed in library), NotebookLM

### Gap C: Tree models — does pre-filtering help or hurt in low-N?
- **Question:** For Decision Trees with N=179 and p=545, does external feature filtering before fitting improve or degrade performance?
- **Why it matters:** Trees do implicit selection, but 545 features for N=179 may cause spurious splits
- **Where to look:** Literature on tree-based models in high-dimensional low-N settings
- **Tool:** Paper search, Context7 for scikit-learn docs on tree behavior

### Gap D: imodels/InterpretML scope decision
- **Question:** Do RuleFit, EBMs, SLIM expand the model family set in a way that's worth including for Monday, or is that future work?
- **Why it matters:** These models have fundamentally different feature selection stories and would require separate pipeline branches
- **Where to look:** imodels documentation, InterpretML documentation
- **Tool:** Context7 for up-to-date docs

### Gap E: EBIC gamma parameter for waveform data
- **Question:** What gamma value (0.5-1.0) is appropriate for p=545 correlated waveform features?
- **Why it matters:** EBIC is the proposed stopping rule — gamma controls how aggressively it penalizes model complexity
- **Where to look:** Chen & Chen 2008 (original paper), any follow-up on correlated features
- **Tool:** Zotero, paper search

## Research Queries Design

For each gap, a structured query ready for execution:

### Query 1 (Gap A): Fused LASSO + Stability Selection compatibility
```
Sources: NotebookLM stability selection notebook, Meinshausen 2010, Tibshirani 2005
Query: "Can a structured penalty (fused LASSO) serve as the base selector in stability selection?
Does subsampling preserve the adjacency structure? Any implementations?"
```

### Query 2 (Gap B): Calibration parameters
```
Sources: Nouraie 2025 (stabplot), Bodinier 2025 (sharp), Meinshausen 2010
Query: "For N=179, p=545 with high inter-feature correlation (ρ>0.9 for adjacent features):
What π threshold and λ range give controlled PFER? Does sharp auto-calibrate?"
```

### Query 3 (Gap C): Trees in high-P low-N
```
Sources: scikit-learn docs, general ML literature
Query: "Decision tree performance with p>>N: does pre-filtering to ~30 features improve
generalization, or does the tree's own pruning suffice? Evidence from small-sample studies."
```

### Query 4 (Gap D): imodels scope
```
Sources: imodels docs (Context7), InterpretML docs
Query: "For regression with N=179 and 545 features: which imodels/InterpretML models
handle feature selection natively? What's the minimum implementation overhead?"
```

### Query 5 (Gap E): EBIC gamma
```
Sources: Chen & Chen 2008, follow-up literature
Query: "EBIC gamma selection for correlated covariates: does high inter-feature correlation
change the recommended gamma range? Any guidance for functional/waveform data?"
```

## Minimum Viable Framework (Monday Presentation)

Not all 6 families need to be fully specified. The MVP for a defensible Monday presentation:

**Must have (4 families):**
- Linear (no regularization) — OLS baseline, most scrutinized
- L1-regularized — stability selection showcase, core methodology
- L2-regularized — Ridge is common in this domain
- Tree-based — different selection story, shows breadth

**Future work (2 families):**
- Non-parametric (KNN, SVM) — viable but not priority for interpretability story
- Interpretable ML (imodels) — attractive but scope creep risk; decide early, don't research if "out"

**Presentation angle:** "Rigorous framework for the four model families most appropriate for N=179, p=545 interpretable prediction, with clear extensions for future work."

## Scope Decisions (Decide BEFORE Research, Not After)

These decisions should be made upfront to prevent perfectionism and scope creep:

- [ ] **imodels in or out for Monday?** → Recommend OUT. Defer to future work. Skip Query 4.
- [ ] **Nested CV: non-negotiable or negotiable?** → Recommend NON-NEGOTIABLE for linear models (high leakage risk per Vabalas 2019). Negotiable for trees (lower risk). This is the defensible position.
- [ ] **Multi-target strategy:** Run 3 separate pipelines (one per target: cSBP, cPP, cfPWV). Joint selection is a future refinement.
- [ ] **Ensemble methods:** OUT for Monday. PyCaret ensembles (Stacking, Blending) excluded from framework — these are not interpretable.

## Acceptance Criteria

- [ ] Per-family pipeline map complete for MVP 4 families, with A→B→C→D structure and literature citations
- [ ] Stability selection integration specified: how D (meta-layer) wraps B for each family
- [ ] The 5 specific gaps (A-E) have answers or explicit "defer" decisions with rationale and Monday impact noted
- [ ] Nesting structure validated: diagram drawn, cross-checked against Vabalas 2019
- [ ] Can explain the framework verbally to supervisor with literature-backed justifications
- [ ] Code changes identified with rough hour estimates and feasibility confirmed
- [ ] Every pipeline choice has at least one literature citation
- [ ] Framework internally consistent (no contradictions between family specs)
- [ ] Multi-target approach defined (per-target or joint)

## Research Query Findings (Grounded via NotebookLM + Zotero)

### Q1 Answer: Fused LASSO + Stability Selection Compatibility

**Verdict: YES — compatible, with caveats on error bounds.**

- Stability selection is a general meta-algorithm compatible with ANY high-dimensional variable selector (Meinshausen & Buhlmann 2010)
- Philipp et al. (2017) explicitly extended stability selection to **structured selection algorithms** including Group LASSO and Structured Input-Output LASSO — Fused LASSO fits this category
- **Subsampling preserves adjacency:** Stability selection subsamples *observations* (rows), not features (columns). The Fused LASSO penalty applies to adjacent *feature coefficients*, so feature ordering remains intact across all subsamples
- **Caveat:** Complex structure reduces reliability of the theoretical PFER error bound. The exchangeability assumption among noise variables may be violated when overlapping groups favor certain noise variables. The bound is less tight than with standard LASSO, but still provides control
- **For high correlation (ρ>0.9):** Use **Randomized LASSO** (weakness parameter α ∈ [0.2, 0.8]) as the base selector instead of standard LASSO, to prevent correlated features from splitting votes

**Action:** Can use Fused LASSO inside stability selection. Consider Randomized Fused LASSO for best results. Accept that PFER bound is approximate, not exact.

### Q2 Answer: Calibration Parameters for N=179, p=545

**Concrete recommendations:**

| Parameter | Standard (Meinshausen) | stabplot (Nouraie 2025) |
|-----------|----------------------|------------------------|
| **π threshold** | 0.6–0.9 (default 0.9 for strict control) | Calibrated via optimal λ |
| **λ range** | Set grid so q ≈ √(0.8p) ≈ **21 variables** selected on average | Choose smallest λ where stability Φ ≥ **0.75** |
| **Base selector** | Randomized LASSO (α ∈ [0.2, 0.8]) for correlated features | Same |
| **Subsamples** | n/2 per subsample | ~200 subsamples for convergence |

- For p=545: q_Λ ≈ √(0.8 × 545) ≈ **21 variables** selected on average to get E(V) ≤ 1 false positive
- **stabplot** finds λ_stable as smallest λ where overall stability ≥ 0.75. If never reached, uses λ_stable-1sd (max stability minus one std dev)
- **sharp package** not in NotebookLM sources — need separate web search if auto-calibration desired
- Standard LASSO violates irrepresentable condition when ρ > 0.5 → must use Randomized LASSO

### Q3 Answer: Trees in High-P Low-N

**Verdict: Pre-filtering helps, but MUST be inside CV loop.**

- Do NOT rely solely on CART's internal pruning for p=545, N=179. High dimensionality causes spurious splits (fitting noise)
- Do NOT pre-filter on full 179 samples then validate — this is selection bias (Vabalas 2019)
- **DO** use nested CV with pre-filtering inside the training folds
- **Stability Selection** recommended as the filtering method for trees too — identifies robustly associated features before fitting
- Consider **one-standard-error rule** when selecting tree depth (pick simplest model within 1 SE of best)
- Random Forests outperform single CART for robustness, but are less interpretable

**Action for tree family:** External pre-filtering (via stability selection or correlation filter) inside nested CV → then fit Decision Tree on reduced feature set (~30 features).

### Q4 Answer: Feature Selection ↔ Hyperparameter Tuning Interaction

**Verdict: Joint optimization recommended, but sequential is acceptable for N=179.**

- Literature recommends treating feature count as another hyperparameter and jointly optimizing in a grid with model parameters (Krstajic et al.)
- However, for N=179, joint optimization increases the search space substantially → risk of overfitting the selection process itself
- **Recommended protocol for N=179:**
  1. Repeated Stratified Nested CV (e.g., 50 repeats × 10-fold outer × 10-fold inner)
  2. Inner loop: joint grid search over hyperparameters + feature sets
  3. Outer loop: unbiased error estimate
  4. Report average error AND variance/interval across repeats
- **Regularization preferred over hard selection:** LASSO/Elastic Net provide continuous regularization, more stable than discrete "top-K" selection for small N
- **Stability Selection provides finite sample false positive control** — crucial when N is small

**Revision to Feb 6 decision:** The "sequential (select → tune)" decision may need upgrading to joint optimization within inner CV loop for maximum rigor. However, sequential is still defensible if well-justified (simpler, more interpretable, lower overfitting risk with N=179).

### Q5 Answer: EBIC Gamma

**Verdict: NotebookLM sources don't cover EBIC directly. Alternative approaches recommended.**

- Neither the Stability Selection nor Pareto notebooks contain EBIC/Chen & Chen 2008
- The literature in these notebooks recommends **stability-based stopping** (stabplot's Φ ≥ 0.75 criterion) rather than information criteria
- **Alternative stopping rules from sources:**
  - stabplot: λ_stable where overall stability ≥ 0.75
  - One-standard-error rule for CV-based selection
  - Consensus Nested CV (cnCV) — features consistently chosen across inner folds
- **EBIC still valid** but may be redundant if using stability selection with stabplot calibration
- **Fallback:** Use gamma=0.5 (moderate) to gamma=1.0 (conservative) per Chen & Chen 2008 defaults. Higher gamma = fewer features selected.

### Zotero Library Gaps

Papers referenced in Obsidian notes but NOT found in Zotero:
- Tibshirani 2005 (Fused LASSO)
- Faletto & Bien 2022 (Cluster Stability Selection)
- Chen & Chen 2008 (EBIC)
- Bodinier 2025 (sharp)
- Vabalas 2019 (Nested CV bias)

**Action needed:** Add these to Zotero for proper citation management. Only Meinshausen 2010, Nogueira 2018, Nouraie 2025, and Philipp 2017 confirmed in library.

---

## MCP Access Status

| Tool | Status | Notebook IDs |
|------|--------|-------------|
| NotebookLM | Working | Stability Selection: `d2c53446`, Pareto: `e7b3cc25`, Taiwan Lit: `2b000f61`, CV: `58ea2b83` |
| Zotero | Working | Stability selection papers confirmed in library |
| Claude Desktop | Not connected | Not needed for this task |
| Context7 | Working | Available for scikit-learn, imodels docs |

**MCP fallback mapping (if tools stay broken):**
| Query | Primary Tool | Fallback |
|-------|-------------|----------|
| Q1 (Fused LASSO compat) | NotebookLM | `Feature Selection Methodology Decision.md` + web search |
| Q2 (Calibration params) | Zotero + NotebookLM | `Synthesis` papers section + Nouraie/Bodinier defaults |
| Q3 (Trees in high-P) | Context7 + paper search | `Feature Selection Methods Comparison.md` tree section + web |
| Q5 (EBIC gamma) | Zotero + paper search | Chen & Chen 2008 defaults (gamma=0.5-1.0) |

**Circuit breaker:** If MCP fix takes >15 min, switch to fallback immediately.

## Execution Plan (Time-Budgeted)

**Total budget: ~6 hours** across Saturday/Sunday

### Phase 0: Scope Decisions (15 min)
- [ ] Review and confirm MVP scope decisions above with user
- [ ] If imodels = OUT, skip Query 4 entirely
- [ ] Confirm nested CV position (non-negotiable for linear, negotiable for trees)

### Phase 1: Fix Tool Access (15 min, hard cap)
- [ ] Run `nlm.exe login` on Windows, copy auth tokens to WSL `~/.nlm/`
- [ ] Verify Zotero MCP is responsive (confirmed working)
- [ ] List NotebookLM notebooks, find stability selection notebook ID
- [ ] If NotebookLM still broken after 15 min → use fallback mapping above

### Phase 2: Run Research Queries (2 hours, time-boxed)

**Priority order** (if time-constrained, run in this sequence):

| Priority | Query | Time Box | Why Critical |
|----------|-------|----------|--------------|
| 1 (CRITICAL) | Q1: Fused LASSO + Stability Selection | 30 min | Keystone question — determines if topology + collinearity solved together |
| 2 | Q3: Trees in high-P low-N | 20 min | Affects tree-family pipeline spec |
| 3 | Q5: EBIC gamma for waveform data | 15 min | Affects stopping rule, has sensible defaults |
| 4 | Q2: Calibration parameters | 15 min | Has defaults (π=0.6, sharp auto-calibration) |
| 5 (SKIP if imodels OUT) | Q4: imodels scope | 10 min | Only if scope decision = IN |

- [ ] Q1: Fused LASSO + Stability Selection — NotebookLM + paper search (30 min)
- [ ] Q3: Trees in high-P — Context7 + paper search (20 min)
- [ ] Q5: EBIC gamma — Zotero + paper search (15 min)
- [ ] Q2: Calibration parameters — Zotero + NotebookLM (15 min)
- [ ] Q4: imodels scope — Context7 (10 min, SKIP if out of scope)

**If Q1 returns "incompatible":** Fallback = (1) Cluster Stability for collinearity (Gap 5), (2) address topology via feature engineering in step A (pre-clustering adjacent waveform features), not step B.

### Phase 3: Synthesize into Framework Document (2 hours)
- [ ] Consolidate query answers into per-family pipeline map
- [ ] For each MVP family: specify A→B→C→D with literature citation
- [ ] Define hyperparameter tuning position in nesting structure (C_tune)
- [ ] Specify multi-target approach (per-target pipelines)
- [ ] Update `Feature Selection Methodology Decision.md` with refined framework
- [ ] Create Knowledge note: "Evaluation Framework for Low-N Feature Selection"
- [ ] Identify code changes needed with rough hour estimates

### Phase 3.5: Validation (30 min)
- [ ] Cross-check: every MVP family has A→B→C→D specified
- [ ] Cross-check: every pipeline choice has a literature citation
- [ ] Cross-check: stability selection integration is consistent across families
- [ ] Cross-check: nested CV position is clear and defensible
- [ ] Estimate total implementation time for code changes
- [ ] If implementation > 8 hours, flag and reconsider scope

### Phase 4: Review and Presentation Prep (1 hour)
- [ ] User reviews framework document
- [ ] Confirm all scope decisions are final
- [ ] Draft 1-page presentation outline (key slides for Monday)
- [ ] Practice verbal explanation of framework (acceptance criterion)
- [ ] Optional: send framework summary to supervisor for async Sunday review

## Dependencies & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Perfectionism trap (query expansion) | HIGH (60%) | Misses Monday deadline | Time boxes per query, circuit breakers, scope decisions upfront |
| MCP tools remain down | MEDIUM (40%) | Lower confidence in answers | Fallback mapping per query, 15 min cap on fix attempts |
| Fused LASSO incompatible with stability selection | MEDIUM (30%) | Need alternative for topology | Cluster-based approach works independently; topology via feature engineering |
| Code changes larger than expected | MEDIUM (25%) | Framework not implementable by Monday | Phase 3.5 estimates hours; if >8h, reduce scope |
| Query answers inconclusive | MEDIUM (30%) | Weaker evidence base | Only Q1 is a potential Monday blocker; others have sensible defaults |
| imodels scope creep | MEDIUM (30%) | Hours lost on exploration | Hard boundary: decide in/out in Phase 0, not Phase 4 |

**Key SpecFlow insight:** Only Q1 (Fused LASSO compatibility) is a potential Monday blocker. All other queries have acceptable fallback defaults. With time budgets and upfront scope decisions, Monday deadline risk drops from HIGH to MEDIUM.

## References & Research

### Internal References
- `Projects/arterial analysis/sessions/2026-02-07-monday-update-brainstorm.md` — Task 2 spec
- `Projects/arterial analysis/sessions/2026-02-06-evaluation-methodology.md` — Prior decisions
- `02 - Knowledge/Computer/ML/Feature Selection Methods Comparison.md` — Method taxonomy
- `02 - Knowledge/Computer/ML/ML Pipeline Taxonomy.md` — A/B/C/D structure
- `Projects/arterial analysis/Literature Review - Feature Selection in Low-N High-P/Synthesis - Current Understanding.md` — 6 gaps, papers
- `Projects/arterial analysis/Feature Selection Methodology Decision.md` — Concrete recommendations
- `Projects/arterial analysis/Command Center/L5-Modeling.md` — Current pipeline

### Key Papers (in Zotero)
- Meinshausen & Buhlmann 2010 — Stability Selection (JRSSB)
- Faletto & Bien 2022 — Cluster Stability Selection (Biometrika)
- Tibshirani 2005 — Fused LASSO (JRSSB)
- Nouraie & Muller 2025 — Stability calibration (stabplot)
- Bodinier 2025 — Auto-calibration (sharp)
- Lee et al. 2016 — Post-Selection Inference (Annals of Statistics)
- Chen & Chen 2008 — EBIC (Biometrika)
- Vabalas 2019 — Nested CV bias
- Yamada 2014 — HSIC-Lasso
- Nogueira 2018 — Stability estimator

### Tools
- NotebookLM: stability selection notebook (ID needed)
- Zotero: arterial analysis collection
- Context7: scikit-learn, imodels, InterpretML docs
