# Model Family Literature Search — Review Document
# For: Arterial stiffness methodology framework (N=179, p=545, correlated waveform features)
# Status: COMPLETE — all 10 models + 2 cross-cutting sections filled. Ready for review.
# Created: 2026-02-09

## How to review
- Each model section has Tier 1 (seminal/must-have), Tier 2 (practical guidance), Tier 3 (niche/theoretical)
- Mark papers you want acquired with ✅, skip with ❌
- I'll batch-download → Zotero → NLM for all approved papers

---

## 1. Ridge Regression
**Your regime**: p/n ≈ 3 (overparameterized). Ridge stays well-defined when p>n unlike OLS.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Hoerl & Kennard 1970 — "Ridge regression: Biased estimation for nonorthogonal problems" | 19,799 | Technometrics | Original Ridge paper. Proves bias-variance tradeoff under multicollinearity. |
| Witten & Tibshirani 2009 — "Covariance-regularized regression for high dimensional problems" | 324 | JRSSB | Ridge/LASSO/ElasticNet as covariance regularization. When each is optimal at p>n. |
| Tsigler & Bartlett 2023 — "Benign overfitting in ridge regression" | 353 | JMLR | When Ridge interpolates yet generalizes. Characterizes double descent in p>n. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Patil et al. 2021 — "Uniform consistency of CV estimators for high-dimensional ridge" | 74 | AISTATS | Proves CV selects optimal λ at p/n>1. Your nested CV works. |
| Liu & Dobriban 2019 — "Ridge regression: Structure, cross-validation, and sketching" | 79 | arXiv/ICLR | Random matrix theory for exact risk at given p/n ratio. |
| van de Wiel et al. 2021 — "Fast CV for multi-penalty high-dimensional ridge" | 30 | JCGS | Multi-penalty for grouped features like waveform families. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Wu & Xu 2020 — "Optimal weighted regularization in overparameterized linear regression" | 225 | NeurIPS | Optimal λ avoids double descent. |
| Atanasov et al. 2024 — "Risk and CV in ridge regression with correlated samples" | 12 | arXiv | CV under correlation — your exact scenario. |

**Key constraint for Ridge**: Well-suited to p>n. CV consistently tunes λ at p/n≈3. Risk is underpowered CV, not Ridge failure.

---

## 2. LASSO
**Your regime**: p/n ≈ 3, highly correlated features. LASSO's L1 penalty does variable selection but has known failure modes under correlation.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Tibshirani 1996 — "Regression shrinkage and selection via the lasso" | 68,376 | JRSSB | THE original LASSO paper. L1 penalty for simultaneous estimation and selection. |
| Zhao & Yu 2006 — "On model selection consistency of Lasso" | 3,800 | JMLR | Defines the **irrepresentable condition** — the exact condition under which LASSO is consistent. Your correlated waveform features likely VIOLATE this. Critical constraint paper. |
| Meinshausen & Yu 2009 — "Lasso-type recovery of sparse representations for high-dimensional data" | 1,115 | Annals of Statistics | What LASSO can/cannot recover when irrepresentable condition fails. From the stability selection author. |
| Zhang & Huang 2008 — "The sparsity and bias of the Lasso selection in high-dimensional linear regression" | 1,057 | Annals of Statistics | Characterizes LASSO bias and sparsity. Shows sparse Riesz condition as alternative to irrepresentable. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| McNeish 2015 — "Using lasso for predictor selection and to assuage overfitting" | 505 | Multivariate Behavioral Research | Practical guide. Documents that LASSO picks one of correlated vars arbitrarily — directly relevant to your waveform groups. |
| Buch et al. 2023 — "Systematic review of statistical methods for group variable selection" | 26 | Statistics in Medicine | Reviews Group LASSO and alternatives for when features have natural groups (like your waveform families). |
| Liu et al. 2023 — "LASSO and elastic net tend to over-select features" | 26 | Mathematics | Documents over-selection problem in HD settings. Directly relevant risk for your p=545. |

### Tier 3: Workarounds for your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Jia & Rohe 2015 — "Preconditioning the Lasso for sign consistency" | 69 | Electronic J. Statistics | Fix for when irrepresentable condition fails: precondition the design matrix. Potential workaround for your correlated features. |

**Key constraint for LASSO**: Irrepresentable condition almost certainly violated with your correlated waveforms. LASSO will arbitrarily pick one feature from a correlated group, giving unstable selections. Use stability selection (already in your pipeline) or switch to Elastic Net/Group LASSO.

---

## 3. Elastic Net
**Your regime**: p/n ≈ 3, highly correlated features. Elastic Net was explicitly designed for this — grouping effect handles correlation.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Zou & Hastie 2005 — "Regularization and variable selection via the elastic net" | 25,845 | JRSSB | THE original. Explicitly states: "particularly useful when p >> n" and "encourages grouping effect where strongly correlated predictors tend to be in or out together." Your ideal method. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Waldmann et al. 2013 — "Evaluation of lasso and elastic net in GWAS" | 281 | Frontiers in Genetics | LASSO vs ElasticNet on genomic data (high-dim, correlated). ElasticNet handles degeneracies from correlation. Similar data structure to yours. |
| Algamal & Lee 2015 — "Regularized logistic regression with adjusted adaptive elastic net for HD cancer classification" | 158 | Computers in Biology and Medicine | Adaptive elastic net reduces bias in selection. HD biomedical application. |
| Xiao & Xu 2015 — "Multi-step adaptive elastic-net: reducing false positives in HD variable selection" | 60 | J. Statistical Computation and Simulation | Multi-step approach to control false positives — relevant since Liu 2023 shows over-selection. |
| Ajana et al. 2019 — "Benefits of dimension reduction in penalized regression for HD grouped data: low sample size" | 31 | Bioinformatics | Combines dimension reduction + penalized regression for grouped HD data with **low sample size**. Your exact scenario. |

**Key constraint for Elastic Net**: Best linear method for your scenario. The α parameter (L1/L2 mixing) needs careful CV tuning. At α→0 approaches Ridge (no selection), at α→1 approaches LASSO (unstable selection). Literature suggests α ∈ [0.1, 0.5] for highly correlated data.

---

## 4. Random Forest
**Your regime**: p/n ≈ 3, correlated features. RF handles p>n natively via random subspace (mtry). Key risk: variable importance bias with correlated features.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Breiman 2001 — "Random Forests" | 109,000 | Machine Learning | THE original RF paper. OOB error estimation, variable importance, random subspace method. |
| Biau & Scornet 2016 — "A random forest guided tour" | 3,395 | TEST | Definitive modern review of RF theory. Mathematical foundations, parameter selection, variable importance. Addresses p>>n settings. |
| Scornet, Biau & Vert 2015 — "Consistency of random forests" | ~500 | Annals of Statistics | Proves consistency of Breiman's algorithm in additive models. Shows how RF adapts to sparsity — critical for p>>n. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Strobl et al. 2007 — "Bias in random forest variable importance measures" | 1,176 | BMC Bioinformatics | **CRITICAL**: Standard RF importance is BIASED toward correlated predictors. Two mechanisms identified. Solution: conditional importance (R `party` package). |
| Strobl et al. 2008 — "Conditional variable importance for random forests" | ~800 | BMC Bioinformatics | Develops conditional permutation scheme for unbiased importance with correlated predictors. Essential for your waveform features. |
| Genuer et al. 2010 — "Variable selection using random forests" | ~600 | Pattern Recognition Letters | Two-stage variable selection: ranking via permutation importance + stepwise forward selection. Basis for R `VSURF` package. |
| Huang & Boutros 2016 — "The parameter sensitivity of random forests" | ~300 | BMC Bioinformatics | Systematic hyperparameter sensitivity study (ntree, mtry, nodesize). Practical tuning guidance for genomic/biomedical applications. |
| Díaz-Uriarte & Alvarez de Andrés 2006 — "Gene selection and classification of microarray data using random forest" | ~1,500 | BMC Bioinformatics | RF in p>>n genomics. RF performs well when most predictors are noise. Introduces gene selection procedure preserving accuracy. |
| Mentch & Hooker 2016 — "Quantifying uncertainty in random forests via confidence intervals and hypothesis tests" | 321 | JMLR | Formal statistical inference for RF via subsampling U-statistic structure. Important for small-sample uncertainty quantification. |
| Wallace et al. 2023 — "Use and misuse of random forest variable importance metrics in medicine" | 70 | BMC Medical Research Methodology | OOB importance UNRELIABLE with correlated features. Recommends knockoff VIMPs as unbiased alternative. |
| Wright & Ziegler 2017 — "ranger: A fast implementation of random forests for high dimensional data" | ~2,000 | J. Statistical Software | Fastest RF implementation for large p. Use `ranger` for your p=545 analysis. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Cantor et al. 2024 — "Knowledge-slanted random forest for HD data and small sample size" | 9 | BioData Mining | Method specifically for HD + small N (mentions n≤30). Integrates prior knowledge + modified Boruta. |
| Luan et al. 2020 — "Predictive performances of random forest models with limited sample size" | 163 | Fisheries Research | Empirical guidance on when RF maintains predictive power despite small N. |
| An et al. 2021 — "Radiomics ML study with small sample size: single random training-test split may lead to unreliable results" | 73 | PLOS ONE | Single train-test splits UNRELIABLE with small N. Results vary dramatically across splits. |
| Rotari & Kulahci 2024 — "Variable selection wrapper for correlated input variables in random forest" | 14 | Quality & Reliability Eng. Int. | Extends Boruta for CORRELATED data using conditional importance. Your exact scenario. |

**Key constraint for RF**: Handles p>n natively. Main risk is variable importance bias from correlated features — use conditional importance (Strobl 2008) or SHAP, not default permutation importance. Use `ranger` for speed at p=545.

---

## 5. Gradient Boosting (GBM/XGBoost)
**Your regime**: p/n ≈ 3, small N. Boosting achieves p>>n consistency but overfitting risk is HIGH — base learners can achieve perfect training accuracy when p>n.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Friedman 2001 — "Greedy function approximation: A gradient boosting machine" | 26,919 | Annals of Statistics | THE original GBM paper. Gradient descent in function space framework. |
| Chen & Guestrin 2016 — "XGBoost: A scalable tree boosting system" | 47,294 | KDD | State-of-the-art implementation. Sparsity-aware algorithms, L1/L2 regularization. The practical standard. |
| Friedman 2002 — "Stochastic gradient boosting" | 5,541 | Comp. Stats & Data Analysis | Subsample-based regularization. Outperforms standard GB in high dimensions. |
| Ke et al. 2017 — "LightGBM: A highly efficient gradient boosting decision tree" | 12,860 | NeurIPS | GOSS + Exclusive Feature Bundling for efficiency with HD data. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Bühlmann & Hothorn 2007 — "Boosting algorithms: Regularization, prediction and model fitting" | ~1,500 | Statistical Science | Comprehensive review of regularization in boosting: early stopping, shrinkage, subsampling. Essential conceptual overview. |
| Bühlmann 2006 — "Boosting for high-dimensional linear models" | ~700 | Annals of Statistics | **CRITICAL**: Proves L2Boosting consistency when p grows exponentially with n. No assumptions on predictor correlation needed. |
| Mayr et al. 2014 — "The evolution of boosting algorithms" | ~400 | Methods of Info. in Medicine | How boosting evolved from ML to statistical modeling. Overview of variants and when to use each. |
| Lundberg & Lee 2017 — "A unified approach to interpreting model predictions (SHAP)" | ~30,000 | NeurIPS | TreeSHAP for feature attribution. Only method with consistency + accuracy. Use instead of built-in XGBoost importance for correlated features. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Blagus & Lusa 2015 — "Boosting for high-dimensional two-class prediction" | ~150 | BMC Bioinformatics | **DIRECTLY RELEVANT**: When p>n, even weak base classifiers achieve perfect training accuracy → overfitting. Recommends stochastic GB with shrinkage. |
| Blagus & Lusa 2017 — "Gradient boosting for high-dimensional prediction of rare events" | ~100 | Comp. Stats & Data Analysis | Tuning ineffective when sample size small. Small N prevents efficient bias removal from training data. |
| Prokhorenkova et al. 2018 — "CatBoost: unbiased boosting with categorical features" | ~5,000 | NeurIPS | Ordered boosting fights prediction shift and target leakage. Modern regularization technique. |

**Key constraint for GBM**: Overfitting risk HIGH at p/n≈3. Base learners can achieve perfect training accuracy. Mitigate with: (1) aggressive early stopping, (2) stochastic subsampling (subsample=0.5-0.8), (3) strong L1/L2 regularization, (4) shallow trees (max_depth=2-4). Use SHAP for importance, not built-in metrics.

---

## 6. Support Vector Machine (SVM)
**Your regime**: p/n ≈ 3. SVM classically excels at p>>n via dual formulation (n=179 dual variables, not p=545). Linear kernel strongly recommended.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Cortes & Vapnik 1995 — "Support-vector networks" | 29,782 | Machine Learning | THE canonical SVM paper. Maximum-margin hyperplanes with soft margins. |
| Vapnik 1998 — "The Nature of Statistical Learning Theory" | 91,650 | Springer (book) | VC dimension, generalization bounds. Why SVMs work in high-dimensional spaces. |
| Scholkopf & Smola 2002 — "Learning with Kernels" | 5,263 | MIT Press (book) | Comprehensive kernel methods text. Dual formulation advantage when p>>n. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Guyon et al. 2002 — "Gene selection for cancer classification using support vector machines" | 7,789 | Machine Learning | **SVM-RFE** — gold standard for SVM feature selection in p>>n microarray data. Directly relevant to your pipeline. |
| Chang & Lin 2011 — "LIBSVM: A library for support vector machines" | 22,062 | ACM TIST | Most widely used SVM implementation. Practical optimization and parameter selection guidance. |
| Ben-Hur & Weston 2010 — "A user's guide to support vector machines" | ~500 | Methods in Molecular Biology | Practical tutorial for biological applications. Parameter selection, kernel choice, normalization for small samples. |
| Hsu, Chang & Lin 2003 — "A practical guide to support vector classification" | ~10,000 | National Taiwan University | THE practical implementation guide. C parameter selection, kernel choice, CV strategies. |
| Noble 2006 — "What is a support vector machine?" | ~3,000 | Nature Biotechnology | Clear tutorial for biologists. SVM concepts and biological applications. |
| Hofmann, Scholkopf & Smola 2008 — "Kernel methods in machine learning" | 2,163 | Annals of Statistics | Comprehensive kernel methods review with theoretical justification for HD performance. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Statnikov et al. 2005 — "A comprehensive evaluation of multicategory classification methods for microarray gene expression cancer diagnosis" | ~800 | Bioinformatics | Evaluates 11 datasets. SVM superiority for microarray data (similar p>>n structure). |
| Braga-Neto & Dougherty 2004 — "Is cross-validation valid for small-sample microarray classification?" | 475 | Bioinformatics | **CRITICAL**: CV has excessive variance with small samples. Essential for interpreting your N=179 results. |
| Furey et al. 2000 — "Support vector machine classification and validation of cancer tissue samples using microarray expression data" | ~1,500 | Bioinformatics | Early SVM demonstration on microarray data. HD classification with very small samples. |

**Key constraint for SVM**: Well-suited to p>>n via dual formulation (n dual variables). Use LINEAR kernel for p>>n (fewer hyperparameters, less overfitting). RBF kernel overfits with small N. C parameter needs careful nested CV tuning. SVM-RFE (Guyon 2002) for feature selection.

---

## 7. K-Nearest Neighbors (KNN)
**Your regime**: p/n ≈ 3. KNN suffers SEVERELY from curse of dimensionality at p=545 — distance concentration makes neighbors meaningless.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Cover & Hart 1967 — "Nearest neighbor pattern classification" | 12,000 | IEEE Trans. Info. Theory | THE original KNN paper. Error bounds: R* ≤ R ≤ R*(2 - MR*/(M-1)). IEEE Golden Jubilee Award. |
| Beyer et al. 1999 — "When is 'nearest neighbor' meaningful?" | 2,000 | ICDT | **CRITICAL**: As dimensionality increases, nearest and farthest distances converge. Effect starts at 10-15 dimensions — your p=545 is catastrophically affected. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Aggarwal, Hinneburg & Keim 2001 — "On the surprising behavior of distance metrics in high dimensional space" | 1,800 | ICDT | Manhattan (L1) consistently preferable to Euclidean (L2) in HD. Introduces fractional distance metrics. |
| Radovanovic, Nanopoulos & Ivanovic 2010 — "Hubs in space: Popular nearest neighbors in high-dimensional data" | 500 | JMLR | Hubness phenomenon: certain points become "universal" neighbors in HD, degrading KNN quality. |
| Weinberger & Saul 2009 — "Distance metric learning for large margin nearest neighbor classification" | 3,500 | JMLR | LMNN learns metric ensuring k-NNs belong to same class with large margin. Potential rescue for KNN in HD. |
| Goldberger et al. 2004 — "Neighbourhood components analysis" | 2,500 | NeurIPS | Learns Mahalanobis metric by maximizing stochastic LOO KNN score. Supervised metric learning for HD. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Keller, Gray & Givens 1985 — "A fuzzy k-nearest neighbor algorithm" | 3,000 | IEEE Trans. SMC | Fuzzy memberships give confidence measures. Valuable for small samples where uncertainty quantification matters. |

**Key constraint for KNN**: Distance concentration at p=545 makes naive KNN nearly useless. MUST apply dimension reduction (PCA, UMAP) or metric learning (LMNN, NCA) before KNN. Even then, KNN is a weak baseline for your regime. Include as a comparison anchor, not a primary method.

---

## 8. Decision Trees / CART
**Your regime**: p/n ≈ 3. Single trees have HIGH variance and will severely overfit with p=545, N=179. Include as ensemble building block, not standalone.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Breiman et al. 1984 — "Classification and Regression Trees" | 40,000 | Wadsworth (book) | THE foundational CART text. Tree-structured rules, pruning, splitting criteria. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Loh 2011 — "Classification and regression trees" | 1,283 | WIREs Data Mining | Comprehensive modern review covering 69 references. Updates CART theory for contemporary applications. |
| Dietterich 2000 — "Ensemble methods in machine learning" | 7,600 | MCS | Why single trees have high variance / low bias. Bagging works best for unstable high-variance learners. With N=179, p=545, single CART will severely overfit. |

**Key constraint for CART**: Single trees are unstable with p>>n — a different random seed can produce a completely different tree. Useful only as baseline or ensemble component (RF, GBM). Not a primary standalone method for your regime.

---

## 9. Partial Least Squares (PLS)
**Your regime**: p/n ≈ 3, highly correlated features. PLS was DESIGNED for this — maximizes covariance between X and Y while handling multicollinearity.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Wold, Sjostrom & Eriksson 2001 — "PLS-regression: a basic tool of chemometrics" | 8,851 | Chemometrics & Intelligent Lab Systems | THE foundational PLS reference. PLS designed specifically for many correlated predictors. |
| de Jong 1993 — "SIMPLS: An alternative approach to partial least squares regression" | 1,816 | Chemometrics & Intelligent Lab Systems | Efficient PLS algorithm calculating factors directly. Widely implemented in software. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Boulesteix & Strimmer 2007 — "Partial least squares: A versatile tool for the analysis of high-dimensional genomic data" | 815 | Briefings in Bioinformatics | **DIRECTLY** addresses your use case. Review of 80 references on PLS for p>>n genomics. Essential reading. |
| Chun & Keles 2010 — "Sparse partial least squares regression for simultaneous dimension reduction and variable selection" | 859 | JRSSB | Standard PLS lacks asymptotic consistency in large p, small n. Sparse PLS does both dimension reduction AND variable selection. Critical for interpretability at p=545. |
| Frank & Friedman 1993 — "A statistical view of some chemometrics regression tools" | 2,700 | Technometrics | Classic PLS vs PCR comparison. PLS generally no worse and often better for prediction. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Rannar et al. 1994 — "A PLS kernel algorithm for data sets with many variables and fewer objects" | 301 | J. Chemometrics | **YOUR EXACT SCENARIO**: specifically for "many variables, fewer objects." Kernel approach for computational efficiency when p>>n. |
| Chung & Keles 2010 — "Sparse partial least squares classification for high dimensional data" | 204 | Stat. Applications in Genetics & Mol. Bio. | Extension of sparse PLS to classification. Directly applicable to HD classification tasks. |

**Key constraint for PLS**: Excellent for p>>n with correlated features (its design purpose). Use Sparse PLS (Chun & Keles 2010) for simultaneous dimension reduction + variable selection. Number of latent components is the key hyperparameter — tune via CV. PLS generally outperforms PCR because it uses Y information in dimension reduction.

---

## 10. Principal Component Regression (PCR)
**Your regime**: p/n ≈ 3. PCR does UNSUPERVISED dimension reduction — PCs explaining most X variance may be irrelevant to Y. Weaker than PLS for prediction.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Jolliffe 1982 — "A note on the use of principal components in regression" | 913 | Applied Statistics (JRSS-C) | Classic WARNING: low-variance PCs may be most predictive. PCR's fundamental flaw — components explaining most X variance may be irrelevant to Y. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Artemiou & Li 2009 — "On principal components and regression: A statistical explanation of a natural phenomenon" | 150 | Statistica Sinica | Probabilistically explains why leading PCs often correlate with response. Shows when PCR works despite unsupervised nature. |
| Cook 2007 — "Fisher lecture: Dimension reduction in regression" | 600 | Statistical Science | Comprehensive review of dimension reduction approaches including PCR limitations. |
| Frank & Friedman 1993 — "A statistical view of some chemometrics regression tools" | 2,700 | Technometrics | PLS vs PCR comparison. PLS generally superior for prediction due to supervised reduction. |

**Key constraint for PCR**: Unsupervised reduction means NO guarantee selected PCs associate with outcome. Low-variance PCs may be most predictive but get dropped. PLS is strictly superior for prediction when p>>n. Include PCR as a comparison method, but PLS is preferred.

---

## Cross-cutting: Nested CV Design
**Your regime**: N=179 with 10 models × hyperparameters. Nested CV essential to avoid selection bias in performance estimation.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Varma & Simon 2006 — "Bias in error estimation when using cross-validation for model selection" | 1,598 | BMC Bioinformatics | THE key paper. Non-nested CV gives substantially biased error estimates. Nested CV essential. |
| Cawley & Talbot 2010 — "On over-fitting in model selection and subsequent selection bias in performance evaluation" | 2,000 | JMLR | Low variance is as important as unbiasedness. Non-negligible variance introduces overfitting in model selection. |
| Vabalas et al. 2019 — "ML algorithm validation with a limited sample size" | 350 | PLOS ONE | **CRITICAL for N=179**: k-fold CV produces strongly biased estimates with small N. Nested CV gives unbiased estimates regardless of sample size. (Already in registry.) |
| Kohavi 1995 — "A study of cross-validation and bootstrap for accuracy estimation and model selection" | 13,000 | IJCAI | Landmark study (500k+ runs): 10-fold stratified CV is optimal even when computation allows more folds. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Bates, Hastie & Tibshirani 2024 — "Cross-validation: What does it estimate and how well does it do it?" | 50 | JASA | Modern theory: CV estimates average prediction error of models fit on OTHER training sets, not the model at hand. Addresses confidence interval issues. |
| Arlot & Celisse 2010 — "A survey of cross-validation procedures for model selection" | 2,500 | Statistics Surveys | Comprehensive theoretical survey relating CV to model selection theory. Guidelines for choosing CV procedures. |
| Molinaro, Simon & Pfeiffer 2005 — "Prediction error estimation: a comparison of resampling methods" | 1,000 | Bioinformatics | Compares CV, bootstrap, .632+ methods for prediction error estimation. |
| Krstajic et al. 2014 — "Cross-validation pitfalls when selecting and assessing regression and classification models" | 800 | J. Cheminformatics | Practical guide: detailed algorithms for repeated grid-search CV and repeated nested CV. |
| Kim 2009 — "Estimating classification error rate: Repeated cross-validation, repeated hold-out and bootstrap" | 900 | Comp. Stats & Data Analysis | Repeated 10-fold CV outperforms .632+ bootstrap for highly adaptive classifiers on small samples (N=20-120). |
| Efron & Tibshirani 1997 — "Improvements on cross-validation: The .632+ bootstrap method" | 3,500 | JASA | .632+ bootstrap as smoothed version of CV with lower variance. Alternative to repeated CV. |

**Key constraint for Nested CV**: With N=179, use 10-fold stratified CV (Kohavi 1995). Repeat outer loop 10-50x for stable estimates (Kim 2009). Feature selection MUST be inside inner CV loop. Budget: 10 outer × 10 inner × repeats = 1000+ model fits per method.

---

## Cross-cutting: Feature Selection + Stability
**Your regime**: 10 models × p=545 features. Selection stability across models/folds is essential for interpretability. Partially covered by existing NLM notebooks.

### Tier 1: Foundational
| Paper | Cites | Journal | What it establishes |
|-------|-------|---------|---------------------|
| Guyon & Elisseeff 2003 — "An introduction to variable and feature selection" | 16,000 | JMLR | THE canonical survey. Filter/wrapper/embedded taxonomy. Stability and evaluation. |
| Meinshausen & Buhlmann 2010 — "Stability selection" | 3,000 | JRSSB | Subsampling + selection with finite-sample error control. (Already in registry + NLM.) |
| Nogueira, Sechidis & Brown 2018 — "On the stability of feature selection algorithms" | 500 | JMLR | Consolidates stability metrics. Enables confidence intervals and hypothesis tests on stability. |

### Tier 2: Practical guidance
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Saeys, Inza & Larranaga 2007 — "A review of feature selection techniques in bioinformatics" | 4,336 | Bioinformatics | Comprehensive bioinformatics-focused review. Taxonomy of methods for HD biological data. |
| Ambroise & McLachlan 2002 — "Selection bias in gene extraction on the basis of microarray gene-expression data" | 2,000 | PNAS | **LANDMARK**: Selection bias when test error calculated on samples used for gene selection. Feature selection MUST be inside CV. |
| Simon et al. 2003 — "Pitfalls in the use of DNA microarray data for diagnostic and prognostic classification" | 3,500 | JNCI | Clinical perspective on selection bias. Emphasizes external validation and proper methodology. |
| Boulesteix & Slawski 2009 — "Stability and aggregation of ranked gene lists" | 188 | Briefings in Bioinformatics | Methods for assessing stability of ranked feature lists. Aggregation across multiple selection runs. |
| Kalousis, Prados & Hilario 2007 — "Stability of feature selection algorithms: a study on high-dimensional spaces" | 800 | Knowledge & Info. Systems | First systematic study of FS stability. Generalized Kalousis estimator measuring sensitivity to training set variations. |

### Tier 3: Specific to your scenario
| Paper | Cites | Journal | What it tells you |
|-------|-------|---------|-------------------|
| Reunanen 2003 — "Overfitting in making comparisons between variable selection methods" | 400 | JMLR | CV performance estimates overfit when used with intensive search. Independent test sets needed to compare selection methods. |

**Key constraint for Feature Selection**: Feature selection MUST happen inside CV (Ambroise 2002). Measure stability across folds/repeats (Nogueira 2018). Stability selection (Meinshausen 2010) provides error-controlled selection. Report stability metrics alongside accuracy for each of 10 models.
