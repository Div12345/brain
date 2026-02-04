# ML Pipeline Literature Coverage Assessment

Assessment of Zotero library coverage for arterial_analysis ML pipeline.

**Date:** 2026-02-03
**Bead:** brain-2wz

## Coverage Summary

| Pipeline Stage | Coverage | Papers | Action Needed |
|----------------|----------|--------|---------------|
| Feature Selection | STRONG | 9+ | None |
| Cross-Validation | MODERATE | 3 | Consider adding 1-2 |
| High-Dimensional Methods | STRONG | 8 | None |
| Arterial/Pulse Wave ML | STRONG | 9 | None |
| Calibration (Measurement) | STRONG | 10 | None |
| Preprocessing | GAP | 0 | Add 2-3 papers |
| Interpretability/XAI | GAP | 0 | Add 2-3 papers |
| Ensemble Methods | GAP | 0 | Add 1-2 papers |
| Model Calibration (Probability) | GAP | 0 | Add 1-2 papers |

## Detailed Assessment by Stage

### 1. Data Preprocessing
**Status: GAP**

No dedicated papers on:
- Normalization strategies for physiological signals
- Imputation methods for missing waveform data
- Outlier detection/handling in time series

**Recommended searches:**
- "physiological signal preprocessing"
- "time series imputation medical"
- "outlier detection waveform"

### 2. Feature Selection
**Status: STRONG**

Key papers in library:
- Nogueira et al. - Stability of feature selection algorithms (G97EKEDV)
- Piironen et al. - Projective inference in high-dimensional problems (ZCLD6VPQ)
- He & Yu - Stable feature selection for biomarker discovery (C6NWCTST)
- Pudjihartono et al. - Feature selection for disease risk prediction (IQM7PFGL)
- Demircioglu - Bias of incorrect feature selection in CV (EADGHILM)
- Bodinier et al. - Automated calibration for stability selection (MQUQ9LT2)

**Gaps within topic:**
- Filter vs wrapper vs embedded comparison missing
- Need clinical domain-specific feature selection paper

### 3. Feature Extraction
**Status: MODERATE (domain-specific)**

Covered through arterial/pulse wave papers:
- Almeida et al. - ML for Arterial Pressure Waveform Analysis (BWQZ4M7W)
- Aghilinejad et al. - Wave intensity via Fourier + ML (2JZB2R6J)

**Gaps:**
- General feature extraction methods (PCA, autoencoders)
- Domain-agnostic dimensionality reduction

### 4. Model Selection
**Status: MODERATE**

Key papers:
- Yates et al. - Cross validation for model selection (LAPQG7XF)
- Varma & Simon - Bias in error estimation with CV (MNBVZZX5)
- Arlot & Celisse - Survey of CV procedures (KIKGV7EN)

**Gaps:**
- Algorithm comparison studies
- Ensemble method papers (Random Forest, XGBoost, stacking)

### 5. Validation
**Status: MODERATE**

CV covered well. Missing:
- Calibration of predicted probabilities
- Clinical validation frameworks
- External validation strategies

### 6. Interpretability
**Status: GAP**

No papers on:
- SHAP values
- LIME
- Feature importance methods
- Clinical interpretability requirements

**Recommended searches:**
- "SHAP machine learning medicine"
- "interpretable machine learning clinical"
- "feature importance cardiovascular"

## Domain-Specific Coverage

### Arterial Stiffness / Pulse Wave Analysis
**Status: STRONG**

Excellent coverage with ML focus:
- Almeida et al. - ML techniques for APW analysis
- Aghilinejad et al. - Wave intensity with ML
- Kim et al. - Deep learning for PAD detection
- Wang et al. - ML for AAA detection
- Natarajan et al. - PPG features for BP measurement
- Multiple calibration papers for arterial measurement

### High-Dimensional / Small Sample
**Status: STRONG**

- Multiple stability selection papers
- Bayesian approaches for genomics (transferable)
- Projective inference methods

## Gap Prioritization

### High Priority (Need before starting)
1. **Interpretability** - Required for clinical acceptance
2. **Preprocessing** - Foundation for reproducibility

### Medium Priority (Add during analysis)
3. **Ensemble Methods** - Likely to use, need justification
4. **Model Calibration** - Important for clinical predictions

### Low Priority (Nice to have)
5. **General feature extraction** - Domain-specific methods may suffice

## Recommended Paper Searches

```
# High priority
"SHAP cardiovascular machine learning"
"interpretable ML clinical prediction"
"physiological signal preprocessing normalization"
"missing data imputation time series medical"

# Medium priority
"random forest vs XGBoost medical"
"calibration machine learning clinical"
"probability calibration prediction"

# Domain-specific additions
"pulse wave velocity machine learning"
"arterial stiffness prediction model"
```

## Decision Rationale Template

For each pipeline choice, document:

```markdown
## [Stage]: [Choice Made]

**Options considered:** A, B, C
**Chosen:** B
**Rationale:** [1-2 sentences]
**Evidence:** [Paper citation]
**Equivalencies:** A could also work because [reason], chose B for [specific advantage]
```

## Next Steps

1. Run recommended searches in Zotero/Google Scholar
2. Add 5-8 papers to fill critical gaps
3. Create `arterial-pipeline-decisions.md` with rationale for each choice
4. Query NotebookLM notebooks for additional context
