---
title: "feat: Pareto-Based Model Selection Framework for Low-N Arterial Analysis"
type: feat
date: 2026-02-06
status: ready-for-review
project: arterial-analysis
tags: [ml-methodology, model-selection, pareto, feature-selection]
---

# Pareto-Based Model Selection Framework for Low-N Arterial Analysis

## Overview

A multi-objective model selection framework that goes beyond prediction error to jointly consider:
- **Accuracy** (RMSE, R², etc.)
- **Feature stability** (consistency of selected features across CV folds)
- **Model parsimony** (number of selected features, model complexity)
- **Hyperparameter sensitivity** (robustness to tuning choices)

This replaces the current "grid search everything and pick best RMSE" approach with a principled Pareto-based methodology.

## Problem Statement / Motivation

### Current Pain Points

1. **Model family choice is unjustified** - Started with OLS (p-values), then PyCaret 10 families, but no principled reason for these specific families
2. **Single-metric selection is insufficient** - Best RMSE doesn't mean best model when you care about interpretability and stability
3. **Feature correlations are ignored** - Waveform features have internal structure; selection methods may be sensitive to this
4. **Hyperparameter sensitivity unknown** - A model that's good at one HP setting but terrible at another is risky

### What Success Looks Like

- A Pareto frontier showing trade-offs between accuracy/stability/parsimony
- Justified model family selection based on n≪p constraints
- Confidence intervals on feature selection, not just point estimates
- Documented rationale for each pipeline choice

## Proposed Solution: Multi-Objective Model Comparison

### The Pareto Framework

Instead of: `argmax(model | accuracy)`

Use: `Pareto_front(models | accuracy, stability, parsimony, robustness)`

**Objectives:**

| Objective | Metric | Direction | Rationale |
|-----------|--------|-----------|-----------|
| Prediction accuracy | RMSE (inner CV) | minimize | Core goal |
| Feature stability | Nogueira stability index | maximize | Consistent features = trustworthy |
| Parsimony | # selected features | minimize | Low-N needs sparse models |
| HP robustness | σ(RMSE) across HP grid | minimize | Want stable performance |

### How to Compute the Pareto Front

1. **For each model family × feature selector combination:**
   - Run nested CV (outer for generalization, inner for selection + tuning)
   - Record: best RMSE, feature frequency across folds, # features, RMSE variance across HP settings

2. **Normalize objectives** (COPA approach):
   - Use rank-based normalization to make incomparable objectives comparable
   - Each objective → percentile rank within the model population

3. **Compute Pareto front:**
   - A model is Pareto-optimal if no other model dominates it on ALL objectives
   - User preferences → weighted aggregation or knee-point selection

### Implementation: Pipeline Structure

```
Outer CV (k=5, generalization estimate)
└── For each fold:
    └── Inner CV (k=5, selection + tuning)
        └── For each model family:
            └── For each HP config:
                └── Stability selection (features)
                └── Fit model
                └── Record: RMSE, features, stability
    └── Aggregate: Pareto front for this fold
└── Final: Pareto front across all folds
```

## Technical Approach

### Model Families to Include (Justified)

| Family | Include? | Rationale |
|--------|----------|-----------|
| **Linear (Ridge, LASSO, ElasticNet)** | ✅ Yes | Baseline, interpretable, handles p>n with regularization |
| **Stability Selection + LASSO** | ✅ Yes | Your primary approach, well-justified for low-N |
| **Gradient Boosting (XGBoost, LightGBM)** | ⚠️ Maybe | Powerful but may overfit with N=179; include with heavy regularization |
| **Random Forest** | ⚠️ Maybe | Handles correlations well, but interpretability suffers |
| **Interpretable (FIGS, EBM)** | ✅ Yes | Explicitly designed for interpretability + accuracy trade-off |
| **SVM** | ❌ Skip | Poor interpretability, no intrinsic feature selection |
| **Neural Networks** | ❌ Skip | N=179 is too small, overfit risk too high |

**Decision rule:** Include families that are (a) known to work in n≪p, OR (b) have built-in regularization/sparsity, OR (c) are interpretable by design.

### Feature Selection Methods

| Method | Include? | Pairs with |
|--------|----------|------------|
| **Stability Selection (LASSO base)** | ✅ Yes | Linear models |
| **Native tree selection** | ✅ Yes | Tree models (report importance stability) |
| **Permutation importance** | ⚠️ Maybe | Any model, but computationally expensive |
| **Stepwise (p-values)** | ❌ No | Invalidated by multiple testing, no stability |

### Handling Correlated Features

Your waveform features (p=545) have structure. Options:
1. **Randomized LASSO** in stability selection (Meinshausen variant) - specifically designed for correlated features
2. **Grouped stability selection** - if you know feature groups a priori
3. **PCA pre-processing** - but loses interpretability

**Recommendation:** Use randomized LASSO variant, document which correlated features tend to substitute.

## Acceptance Criteria

### Functional Requirements

- [ ] Nested CV pipeline runs end-to-end for all included model families
- [ ] Pareto front computed with ≥4 objectives (accuracy, stability, parsimony, HP robustness)
- [ ] Visualization of Pareto front (2D projections + hypervolume)
- [ ] Feature stability report: which features appear in >60%, >80%, >90% of folds
- [ ] HP sensitivity analysis: RMSE variance across grid for each model

### Non-Functional Requirements

- [ ] Pipeline runs in <24h on available compute
- [ ] Results reproducible with fixed random seeds
- [ ] All pipeline choices documented with literature citations

### Quality Gates

- [ ] At least 3 model families on Pareto front (not dominated)
- [ ] Feature stability >0.6 for final model
- [ ] RMSE within acceptable range for clinical relevance

## Dependencies & Prerequisites

| Dependency | Status | Notes |
|------------|--------|-------|
| Arterial codebase reviewed | ❌ Pending | Needed to understand current pipeline |
| stability-selection Python package | ✅ Available | scikit-learn compatible |
| COPA implementation | ⚠️ Check | May need to implement ranking normalization |
| Zotero papers extracted | ⚠️ Partial | Need to add Schneider 2023, COPA |

## References & Research

### Internal References

- Session note: [[Projects/arterial analysis/sessions/2026-02-06-evaluation-methodology]]
- Knowledge: [[02 - Knowledge/Computer/ML/Stability Selection]]
- Knowledge: [[02 - Knowledge/Computer/ML/ML Pipeline Taxonomy]]
- Prior decisions: [[context/plans/research-pipeline-arterial-idea]]

### Your Zotero Papers (Already Have)

**Core Methodology - Model Selection & CV:**
| Paper | Key | Relevance |
|-------|-----|-----------|
| Wainer & Cawley 2018 | DCV2TKLG | Nested CV is "overzealous" for most cases - justifies simpler approach when HP count is low |
| Varma & Simon 2006 | MNBVZZX5 | Bias in CV model selection - foundational |
| On over-fitting in model selection | M96JBRZG | Directly addresses your concern |
| Parvandeh 2020 - Consensus Features Nested CV | 4FMG4UFV | **Key paper** - combines nested CV with feature consensus |
| Roberts et al. 2017 | 9487RT7W | CV strategies for structured data |
| Little et al. 2017 | HAEW5ZJA | Understanding CV strategies |
| Larracy 2021 | C3LZBDTQ | ML validation for small sample - directly applicable |

**Feature Selection & Stability:**
| Paper | Key | Relevance |
|-------|-----|-----------|
| Meinshausen & Buhlmann 2009 | 8NMA2USC | Stability Selection - your primary method |
| Nouraie 2025 | A89QYYZF | Meta-stability of stability selection |
| Nogueira et al. | G97EKEDV | Stability index definition |
| He & Yu 2010 | C6NWCTST | Stable feature selection for biomarker discovery |
| Hofner et al. 2015 | 48C3T4L6 | Boosting + stability selection (n≪p) |

**High-Dimensional Small Sample:**
| Paper | Key | Relevance |
|-------|-----|-----------|
| Sima & Dougherty 2006 | W58XEI68 | "What should be expected from feature selection in small-sample" - **must read** |
| Dobbin & Simon 2011 | PEJURMBK | Optimal train/test splitting for HD classifiers |
| Piironen et al. 2020 | ZCLD6VPQ | Projective inference in HD - Bayesian approach |
| Zuber & Strimmer 2011 | HK6W5WV7 | CAR scores for HD selection |
| Fisher & Mehta 2014 | ZXLLZXE4 | Fast Bayesian feature selection |

**AutoML:**
| Paper | Key | Relevance |
|-------|-----|-----------|
| Auto-sklearn 2.0 | G4WRX95J | How AutoML handles these decisions |
| ExploreKit (Katz 2016) | P4NIW4Q5 | Automatic feature generation |

### Papers to Add (Optional - for Pareto Framework)

| Paper | Why Important | Priority |
|-------|---------------|----------|
| **COPA (Javaloy 2025)** | Ranking-based normalization for Pareto model selection | High if you want formal Pareto |
| **Schneider 2023** | Multi-objective optimization of performance + interpretability | High |
| **Karl 2022** | Survey of multi-objective HPO | Medium (survey) |

### Reading Priority Order

1. **Sima & Dougherty 2006** (W58XEI68) - Sets realistic expectations for small-sample feature selection
2. **Parvandeh 2020** (4FMG4UFV) - Consensus Features Nested CV - combines your concerns
3. **Wainer & Cawley 2018** (DCV2TKLG) - When nested CV is overkill
4. **Larracy 2021** (C3LZBDTQ) - Practical small-sample validation
5. **Nouraie 2025** (A89QYYZF) - Meta-stability (you've already referenced this)
6. **Hofner 2015** (48C3T4L6) - Boosting + stability selection implementation

## Implementation Phases

### Phase 1: Foundation
- [ ] Review arterial codebase (what's the current pipeline?)
- [ ] Add missing papers to Zotero (COPA, Schneider, Karl)
- [x] Create NotebookLM notebook with all model selection papers (notebook: e7b3cc25-b803-40a2-86f9-10f323075c84)
- [ ] Document current model families in PyCaret

### Phase 2: Core Framework
- [ ] Implement Pareto front computation (4 objectives)
- [ ] Implement COPA-style ranking normalization
- [ ] Implement stability selection with randomized LASSO
- [ ] Create nested CV wrapper that records all objectives

### Phase 3: Execution
- [ ] Run pipeline on arterial data
- [ ] Generate Pareto front visualization
- [ ] Identify knee-point / recommended models
- [ ] Document feature stability results

### Phase 4: Validation
- [ ] Compare with current (single-metric) approach
- [ ] Sensitivity analysis on Pareto objectives
- [ ] Write up methodology for paper

## Open Questions

- [ ] Should HP robustness be inner-CV or cross-validated separately?
- [ ] How to handle class imbalance in stability selection (if outcome is binary)?
- [ ] What's the computational budget? Full grid vs. Bayesian HPO?
- [ ] Should interpretability (e.g., # interactions) be a separate objective?

## Next Actions

1. **Immediate:** Review arterial codebase against this framework
2. **Today:** Add COPA, Schneider, Karl papers to Zotero
3. **This week:** Implement Pareto front computation on toy data
4. **Delegate:** Create NotebookLM notebook from model selection papers

---

## Grounded Findings (NotebookLM Synthesis 2026-02-06)

### Pareto Multi-Objective Framework

**How to frame model selection as Pareto optimization:**

1. **Metrics to optimize:**
   - **Accuracy**: RMSE, MSE, or Log-Likelihood
   - **Stability**: Nogueira's $\hat{\Phi}$ (variance-based, corrected for chance)
   - **Parsimony**: # selected features (often implicit via regularization)
   - **HP Robustness**: Stability paths across λ grid

2. **Selecting from Pareto front:**
   - **λ_stable**: Smallest regularization where stability >0.75 ("excellent")
   - **Max sum**: Maximize accuracy + stability
   - **1-SE fallback**: If stability never hits 0.75, use λ within 1 SE of max stability
   - **Trade-off insight**: Often can sacrifice <1% accuracy for massive stability gain (0.34 → 0.98)

3. **Convergence**: Need ~200 subsamples for stability estimator to converge

### Model Families for Small Samples (n~150-200, p~500)

**Recommended:**
| Family | Evidence |
|--------|----------|
| **Random Forest** | High performance in simulations with n=200, p=500; robust to irrelevant features |
| **Elastic Net** | Preferred over LASSO when features correlated (grouping effect) |
| **Penalized Regression** | Well-suited for p>n; use stability selection |

**Not Recommended:**
- Neural networks (n too small)
- Standard LASSO alone (arbitrary among correlated features)

### Nested vs Flat CV Decision

| Goal | Use | Rationale |
|------|-----|-----------|
| **Accurate performance estimation** | Nested CV | Flat CV is optimistic for n<600 |
| **Algorithm selection only** | Flat CV may suffice | Same algorithm often selected |
| **Computational efficiency** | Consensus Nested CV | Feature selection in inner folds without classifier training |

### Feature Selection Stability Expectations

**Be conservative:**
- Correct selection rates often <50% even at n=600
- Standard nested CV selects many false positives at n=200
- Stability scores rarely hit "excellent" (0.75) in real biomedical data

**Improving stability:**
- Randomized LASSO (Meinshausen variant) for correlated features
- Consensus features across inner folds (cnCV)
- Stable Stability Selection: optimize λ for stability not just accuracy

### Modified One-Standard-Error Rule

**Classic rule limitation:** Overestimates variation between models (ignores correlation), leads to underfitting.

**Modified rule:**
$$\sigma_{adj_m} \approx \sigma_{best} \sqrt{1 - \rho_{best, m}}$$

When model scores are highly correlated ($\rho \approx 1$), interval shrinks → favor best model.
When independent ($\rho \approx 0$), behaves like classic rule.

**Application:** Select least-complex model whose adjusted interval includes best model's score.

---

## Appendix: The Nouraie Connection

You mentioned Nouraie 2025 does "feature stability, hyperparam choices". Looking at it:
- Nouraie addresses *meta-stability*: whether stability selection itself is stable
- This is related but different from Pareto optimization
- Nouraie's insight: even the π threshold choice affects what features you get
- **Implication for your Pareto framework:** Include "meta-stability" as a sensitivity check - run stability selection at π=0.6, 0.7, 0.8, 0.9 and see if the same features survive

## Appendix: PyCaret Model Families

PyCaret's default 10 regression models:
1. Linear Regression
2. Lasso Regression
3. Ridge Regression
4. Elastic Net
5. Lasso Least Angle Regression
6. Orthogonal Matching Pursuit
7. Bayesian Ridge
8. Huber Regressor
9. Passive Aggressive Regressor
10. Least Angle Regression

**Assessment:** Mostly linear variants. For a Pareto comparison, you'd want to add:
- XGBoost (tree-based, with regularization)
- Random Forest (tree-based, handles correlations)
- EBM / FIGS (interpretable ML)

This gives you a broader model family landscape to find genuine trade-offs.
