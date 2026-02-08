# Methodology Research Synthesis: Stability Selection & Pipeline Formulation

**Date:** 2026-02-08
**Context:** Preparation for Monday update. Gap was problem formulation for ML pipeline in HDLSS regime.

## Executive Summary
The "A->B->C" pipeline (Prep -> Selection -> Modeling) is valid, but "Selection" (B) is nuanced. 
- **Selection** is for identifying important features.
- **Modeling** is for prediction.
- **Nested CV** wraps BOTH to estimate performance unbiasedly.
- **Stability Selection** is a meta-method that stabilizes B (Selection) to ensure only robust features enter C (Modeling).

## Key Frameworks

### 1. Stability Selection (The "Meta-Method")
*Ref: Meinshausen & Bühlmann (2010)*
- **What:** Runs a base selector (LASSO, Filter) on many subsamples (bootstraps). Keeps features selected in > threshold (e.g., 60%) of runs.
- **Why:** Controls false discovery rate (FDR) in finite samples. Essential for HDLSS where single-pass selection is noisy.
- **Application:**
    - **Filter methods:** Run MI/F-score on bootstraps, aggregate rankings.
    - **Embedded (LASSO):** Randomized LASSO on bootstraps.
    - **Wrappers:** Boruta is essentially stability selection for RF.

### 2. Nested Cross-Validation (The "Truth Teller")
*Ref: Varma & Simon (2006), Cawley & Talbot (2010)*
- **What:** Outer loop for performance estimation, Inner loop for hyperparameter tuning AND feature selection.
- **Why:** Prevents "selection bias" (overfitting to the test set).
- **Distinction:** Nested CV answers "How well does it generalize?". Stability Selection answers "Which features are real?".

## Pipeline Taxonomy (Model Family Pairings)

| Model Family | Selection Strategy | Rationale |
|--------------|--------------------|-----------|
| **Linear (OLS, Huber)** | **Filter + Stability** | Cannot handle p > n. Need strict pre-filtering. Stability ensures filters aren't just noise-mining. |
| **Penalized (LASSO, EN)** | **Randomized LASSO + Stability** | Embedded selection is unstable in HDLSS. Stability selection fixes this. (Meinshausen 2010). |
| **Tree-based (RF, XGB)** | **Boruta / Implicit + Stability** | Implicit importance is biased. Boruta uses shadow features + stability. |
| **Distance (KNN, SVM)** | **Filter + Stability** | Curse of dimensionality. Must reduce space first. |

## Proposed Diagram (A->B->C)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARTERIAL STIFFNESS ML PIPELINE                           │
│                    (High-Dimensional, Low Sample Size)                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────────────┐    ┌─────────────────────┐
│   A. PREP       │───▶│   B. FEATURE SELECTION  │───▶│   C. MODELING       │
│                 │    │                         │    │                     │
│ • Signal QC     │    │ ┌─────────────────────┐ │    │ ┌─────────────────┐ │
│ • Detrending    │    │ │ FILTER METHODS      │ │    │ │ LINEAR MODELS   │ │
│ • Normalization │    │ │ (MI, F-score, mRMR) │ │    │ │ OLS, Huber, KNN │ │
│ • Segmentation  │    │ │         ↓           │ │    │ │ (require filter)│ │
│                 │    │ │ Stability Selection │ │    │ └─────────────────┘ │
│                 │    │ └─────────────────────┘ │    │                     │
│                 │    │                         │    │ ┌─────────────────┐ │
│                 │    │ ┌─────────────────────┐ │    │ │ PENALIZED       │ │
│                 │    │ │ EMBEDDED METHODS    │ │    │ │ LASSO, EN       │ │
│                 │    │ │ (LASSO, EN)         │ │    │ │ (embedded)      │ │
│                 │    │ │         ↓           │ │    │ └─────────────────┘ │
│                 │    │ │ Randomized LASSO +  │ │    │                     │
│                 │    │ │ Stability Selection │ │    │ ┌─────────────────┐ │
│                 │    │ └─────────────────────┘ │    │                     │
│                 │    │                         │    │ ┌─────────────────┐ │
│                 │    │ ┌─────────────────────┐ │    │ │ TREE-BASED      │ │
│                 │    │ │ IMPLICIT METHODS    │ │    │ │ RF, XGBoost     │ │
│                 │    │ │ (Gini, Permutation) │ │    │ │ (implicit)      │ │
│                 │    │ │         ↓           │ │    │ └─────────────────┘ │
│                 │    │ │ Boruta / Bootstrap  │ │    │                     │
│                 │    │ │ Stability           │ │    │                     │
│                 │    │ └─────────────────────┘ │    │                     │
└─────────────────┘    └─────────────────────────┘    └─────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │   NESTED CROSS-VALIDATION   │
                    │   (Unbiased Performance)    │
                    │                             │
                    │  Outer: Performance Est.    │
                    │    └── Inner: HP Tuning     │
                    │          └── Stability Sel. │
                    └─────────────────────────────┘
```

## References
1. **Meinshausen & Bühlmann (2010)**: Stability Selection.
2. **Varma & Simon (2006)**: Bias in error estimation (Nested CV).
3. **Cawley & Talbot (2010)**: Over-fitting in model selection.
4. **Dall'Olio et al. (2020)**: Vascular aging prediction pipeline.
