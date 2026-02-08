# ML Codebase Trust Tooling: Research Landscape (2025-2026)

**Date:** 2026-02-08
**Context:** Python + Hamilton DAG + PyCaret + scikit-learn + statsmodels research repo
**Starting point:** Zero automated quality gates (no CI, no pre-commit, no linting, no type checking)

---

## Executive Summary

The ML trust tooling landscape has matured significantly. For a single-person research project, the highest-leverage starting point is a layered approach:

1. **Immediate wins (day 1):** Ruff + nbstripout + detect-secrets via pre-commit
2. **Week 1:** Pandera schemas on Hamilton DAG nodes + Deepchecks train/test validation suite
3. **Week 2:** DVC for data versioning + MLflow autolog for experiment tracking
4. **Ongoing:** Property-based testing with Hypothesis for data transforms, Deepchecks in CI

The key insight: most "reproducibility" tools only TRACK, they do not ENFORCE. Only DVC pipelines, Pandera schemas, and Deepchecks suites actually BLOCK bad code from proceeding. Everything else is logging that you may or may not look at.

---

## 1. ML-Specific Static Analysis / Linting

### LeakageDetector (2.0)

- **What:** Static analysis that detects data leakage (overlap, preprocessing, multi-test) in ML code by analyzing function call patterns from scikit-learn, Keras, etc.
- **Automated or manual:** Automated -- IDE plugin (PyCharm, VS Code) that flags leakage in real-time with LLM-driven fix suggestions.
- **Works with PyCaret + Hamilton + scikit-learn:** Partial. Detects scikit-learn patterns directly. PyCaret wraps scikit-learn so some leakage patterns will be caught. Hamilton DAG structure may confuse the analysis since it expects linear notebook-style code.
- **Maturity:** Emerging (academic tool, v2.0 published 2025). Not production-hardened.
- **Setup effort:** Minutes (VS Code extension install). But expect false negatives with Hamilton's functional DAG style.
- **Source:** [LeakageDetector on arXiv](https://arxiv.org/abs/2503.14723) | [GitHub](https://github.com/malusamayo/leakage-analysis)

### Ruff (with ML-relevant rule sets)

- **What:** Ultra-fast Python linter/formatter (written in Rust) that replaces flake8, isort, pyupgrade, and more. Not ML-specific, but catches real bugs in numpy/pandas code that ML-specific tools miss.
- **Automated or manual:** Fully automated via pre-commit or CI.
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, fully. Handles numpy/pandas imports correctly (unlike flake8 which chokes on them).
- **Maturity:** Production-ready. Used by pandas, numpy, FastAPI, and major projects.
- **Setup effort:** Minutes. `pip install ruff` + config in `pyproject.toml`.
- **Key rule sets for ML:**
  - `E` / `W` (pycodestyle) -- basic errors
  - `F` (pyflakes) -- unused imports, undefined names
  - `B` (flake8-bugbear) -- common Python bugs
  - `NPY` (numpy-specific rules) -- deprecated numpy usage
  - `PD` (pandas-vet) -- pandas anti-patterns
  - `UP` (pyupgrade) -- modernize Python syntax
  - `S` (bandit/security) -- hardcoded passwords, unsafe yaml
- **Source:** [Ruff docs](https://docs.astral.sh/ruff/) | [GitHub](https://github.com/astral-sh/ruff)

### Semgrep (custom ML rules)

- **What:** AST-based pattern matcher that can find arbitrary code patterns. You can write custom rules to catch ML anti-patterns (e.g., `fit()` called on full dataset before `train_test_split()`).
- **Automated or manual:** Automated (CI or pre-commit), but you must WRITE the rules yourself for ML-specific patterns.
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, language-agnostic pattern matching.
- **Maturity:** Production-ready (the engine). But ML-specific rule sets are DIY / community-contributed.
- **Setup effort:** Hours (to write useful ML rules). The tool itself installs in minutes.
- **Source:** [Semgrep](https://semgrep.dev/)

### Type Checking: Pyright or mypy

- **What:** Static type checkers that catch type errors before runtime. With pandas-stubs and numpy type stubs, they can catch shape mismatches and wrong dtypes.
- **Automated or manual:** Automated (CI or pre-commit).
- **Works with PyCaret + Hamilton + scikit-learn:** Partial. pandas-stubs and numpy stubs are improving rapidly (2025 saw major investment from Scientific Python community). scikit-learn has partial type coverage. PyCaret has minimal stubs.
- **Maturity:** Production-ready (the checkers). Stubs for ML libraries are moderate quality.
- **Setup effort:** Hours to days (configuring strictness level, dealing with untyped ML library calls).
- **Recommendation:** Pyright is faster and has better VS Code integration. Start with `basic` mode, not `strict`.
- **Source:** [Pyright](https://github.com/microsoft/pyright) | [pandas-stubs](https://pypi.org/project/pandas-stubs/)

### VERDICT for Category 1

**Start with Ruff** (5 minutes, immediate value). Add **Pyright in basic mode** when you have an afternoon. **LeakageDetector** is worth installing as a VS Code extension but do not rely on it as your only leakage defense -- it works best on notebook-style code, not Hamilton DAGs. Skip Semgrep unless you have specific patterns you want to enforce.

---

## 2. Data Validation Frameworks

### Pandera -- RECOMMENDED for research

- **What:** Lightweight dataframe validation with type-safe schemas. Define expected column types, value ranges, nullability, and custom statistical checks as decorators or schema objects.
- **What it catches:** Wrong dtypes, out-of-range values, unexpected nulls, schema violations, statistical property violations (mean/std within bounds), custom hypothesis tests.
- **Automated or manual:** Automated -- schemas validate at runtime when data flows through.
- **Works with PyCaret + Hamilton + scikit-learn:** EXCELLENT. Hamilton has first-class Pandera integration via `@check_output(schema=...)` decorator. Install with `pip install sf-hamilton[pandera]`. Validates data at every DAG node automatically.
- **Maturity:** Production-ready. v0.29.0 (Jan 2026). Used by major data teams.
- **Setup effort:** Minutes to hours. Define a schema per dataframe, decorate Hamilton functions. Incremental adoption.
- **Dependencies:** 12 packages (lightweight).
- **Source:** [Pandera docs](https://pandera.readthedocs.io/) | [Hamilton + Pandera integration](https://blog.dagworks.io/p/data-quality-with-hamilton-and-pandera)

### Deepchecks -- RECOMMENDED for ML validation

- **What:** ML-specific validation suite that runs 40+ checks on your data and models, organized into data integrity, train/test validation, and model evaluation suites.
- **What it catches (train/test validation suite -- 12 checks):**
  - Train-Test Samples Mix (duplicate rows across splits)
  - Index / Date leakage between train and test
  - Feature drift, label drift, multivariate drift
  - New categories or labels in test not seen in train
  - Feature-label correlation changes (potential leakage signal)
  - String mismatch between datasets
  - Dataset size comparison
- **Automated or manual:** Automated -- run suite, get pass/fail report. Can integrate into CI.
- **Works with PyCaret + Hamilton + scikit-learn:** YES. PyCaret has built-in `deep_check()` function that wraps Deepchecks. Accepts any scikit-learn-compatible estimator. Works with Hamilton by running suites on DAG outputs.
- **Maturity:** Production-ready. Published in JMLR. 6k+ GitHub stars.
- **Setup effort:** Minutes for basic suite. `pip install deepchecks`, then 5-10 lines of code to run a full validation suite.
- **Source:** [Deepchecks docs](https://docs.deepchecks.com/) | [GitHub](https://github.com/deepchecks/deepchecks)

### Great Expectations

- **What:** Enterprise-grade data validation with checkpoints, data docs, and alerting.
- **What it catches:** Same schema/statistical checks as Pandera, plus multi-engine support (Spark, SQL, pandas).
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, but overkill.
- **Maturity:** Production-ready (enterprise focus).
- **Setup effort:** Hours to days. 107 package dependencies. CLI-driven workflow. Steep learning curve.
- **Verdict:** SKIP for single-person research. Use Pandera instead. Great Expectations is designed for teams with shared data pipelines and governance requirements.
- **Source:** [Great Expectations docs](https://docs.greatexpectations.io/)

### Evidently AI

- **What:** Data drift detection and model monitoring with visual reports. Compares reference (training) data distribution against current (new) data.
- **What it catches:** Feature drift (PSI, KL-divergence, Wasserstein, Jensen-Shannon), model performance degradation, prediction drift.
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, framework-agnostic. Takes pandas DataFrames.
- **Maturity:** Production-ready. Strong open-source community.
- **Setup effort:** Minutes for basic report. `pip install evidently`, 10 lines for a drift report.
- **Verdict:** USEFUL but not first priority. Best for when you have multiple data collection waves and need to check if new data differs from training data. Less useful during initial model development.
- **Source:** [Evidently AI](https://github.com/evidentlyai/evidently) | [Docs](https://docs.evidentlyai.com/)

### WhyLogs

- **What:** Lightweight statistical profiling that creates mergeable, privacy-preserving data profiles. Logs distribution summaries without storing raw data.
- **What it catches:** Distribution shifts, missing values, type changes, cardinality changes.
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, pandas-native.
- **Maturity:** Production-ready (backed by WhyLabs).
- **Setup effort:** Minutes. `pip install whylogs`, one line to profile a DataFrame.
- **Verdict:** NICE TO HAVE for longitudinal tracking across experiment runs. Not a replacement for schema validation (Pandera) or ML-specific checks (Deepchecks). Best value when you want to compare data profiles across time without storing raw data.
- **Source:** [WhyLogs GitHub](https://github.com/whylabs/whylogs) | [Docs](https://docs.whylabs.ai/)

### VERDICT for Category 2

**Pandera + Deepchecks** is the winning combination for research. Pandera validates data shape/schema at every Hamilton node. Deepchecks validates ML-specific properties (leakage, drift, train/test integrity) after splitting. Together they cover the full pipeline. Add Evidently later if you get multiple data waves.

---

## 3. Reproducibility Enforcement

### The critical distinction: ENFORCE vs TRACK

| Tool | Enforces | Tracks | What it means |
|------|----------|--------|---------------|
| DVC | YES (pipelines) | YES (data versions) | `dvc repro` refuses to skip changed stages. `dvc.lock` captures exact hashes. |
| MLflow | NO | YES | Logs params/metrics/artifacts. Does not prevent non-deterministic runs. |
| Sacred | PARTIAL | YES | Auto-seeds PRNGs. Does not lock data versions or enforce pipeline order. |
| Guild AI | NO | YES | Tracks runs externally. No code modification required, but no enforcement either. |

### DVC -- RECOMMENDED for data versioning + pipeline enforcement

- **What:** Git for data. Versions datasets and models via content-addressable storage. Defines reproducible pipelines in `dvc.yaml` with automatic dependency tracking.
- **What it ENFORCES:**
  - Pipeline stages must declare their dependencies and outputs explicitly
  - `dvc repro` only runs stages whose dependencies have changed (hash-based)
  - `dvc.lock` captures exact MD5 hashes of every input, output, and parameter
  - Anyone checking out a git commit + running `dvc pull` + `dvc repro` gets identical results
- **What it does NOT enforce:** Random seeds, library versions, OS-level differences.
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, framework-agnostic. Wraps any Python script.
- **Maturity:** Production-ready. Widely adopted. Active development.
- **Setup effort:** Hours. `pip install dvc`, `dvc init`, define `dvc.yaml` stages. Learning curve for remote storage setup.
- **Source:** [DVC docs](https://doc.dvc.org/) | [GitHub](https://github.com/iterative/dvc)

### MLflow -- RECOMMENDED for experiment tracking

- **What:** Experiment tracking platform that logs parameters, metrics, models, and artifacts with a UI for comparison.
- **What it ENFORCES:** Nothing. It only records.
- **What it TRACKS:**
  - `mlflow.autolog()` -- one line captures all scikit-learn params, metrics, and fitted models automatically
  - Git commit hash, source file, environment info
  - Custom tags and nested runs
- **Works with PyCaret + Hamilton + scikit-learn:** YES. scikit-learn autolog is mature. PyCaret has MLflow integration built in (`log_experiment=True` in `setup()`).
- **Maturity:** Production-ready. Apache project. Industry standard.
- **Setup effort:** Minutes for local tracking. `pip install mlflow`, add `mlflow.autolog()` before training code. UI via `mlflow ui`.
- **Source:** [MLflow docs](https://mlflow.org/docs/latest/) | [scikit-learn guide](https://mlflow.org/docs/latest/ml/traditional-ml/sklearn/guide/)

### Sacred -- GOOD for seed management

- **What:** Experiment configuration, logging, and random seed management framework from IDSIA.
- **What it ENFORCES:**
  - Deterministic PRNG seeding: all `_seed` and `_rnd` instances derive from a single root seed
  - Source code is captured automatically for every run
  - Configuration is immutable once an experiment starts
- **What it does NOT enforce:** Data versions, pipeline ordering, library versions.
- **Works with PyCaret + Hamilton + scikit-learn:** Partial. Works well with raw scikit-learn. PyCaret's internal randomness may not be captured by Sacred's seed management. Hamilton DAG execution is separate from Sacred's experiment lifecycle.
- **Maturity:** Stable but maintenance-mode. Last major update was limited. Community has largely moved to MLflow/W&B.
- **Setup effort:** Hours. Requires restructuring code into Sacred experiments with `@ex.automain` decorator.
- **Verdict:** The seed management is genuinely useful, but the ecosystem has moved on. Consider extracting the seed management PATTERN (set all seeds in one place) without adopting the full framework.
- **Source:** [Sacred docs](https://sacred.readthedocs.io/) | [GitHub](https://github.com/IDSIA/sacred)

### Guild AI

- **What:** Zero-code-change experiment tracking. Runs scripts externally and captures everything.
- **What it ENFORCES:** Nothing. Pure tracking.
- **Works with PyCaret + Hamilton + scikit-learn:** Yes, framework-agnostic.
- **Maturity:** Stable but niche. Small community.
- **Setup effort:** Minutes.
- **Verdict:** SKIP. MLflow provides the same tracking with better ecosystem support and PyCaret integration.
- **Source:** [Guild AI](https://guild.ai/)

### Practical seed enforcement pattern (no framework needed)

```python
# reproducibility.py -- import at top of every script/notebook
import random
import numpy as np
import os

def set_all_seeds(seed: int = 42):
    """Set all random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    # If using PyCaret, pass random_state=seed to setup()
    # If using scikit-learn directly, pass random_state=seed to estimators
```

This pattern, enforced by code review or a custom pre-commit check, is more practical than adopting Sacred for seed management alone.

### VERDICT for Category 3

**DVC for data/pipeline enforcement** (the only tool that actually blocks bad runs) + **MLflow autolog for tracking** (one line of code, PyCaret integration built in). Skip Sacred and Guild AI. Implement the seed pattern manually.

---

## 4. Pre-commit / CI for ML Repos

### Recommended `.pre-commit-config.yaml` for ML research

```yaml
repos:
  # Fast Python linting + formatting (replaces flake8, isort, black)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.1
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Strip notebook outputs (prevent bloated git history)
  - repo: https://github.com/kynan/nbstripout
    rev: 0.8.1
    hooks:
      - id: nbstripout

  # Prevent secrets/credentials from being committed
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets

  # Prevent large files from being committed
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-yaml
      - id: check-toml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict

  # Type checking (optional, add when ready)
  # - repo: https://github.com/RobertCraiwordie/pyright-python
  #   rev: v1.1.390
  #   hooks:
  #     - id: pyright
```

### ML-specific CI checks (GitHub Actions)

There are NO mature, off-the-shelf pre-commit hooks that automatically catch data leakage or missing random seeds. This is a gap in the ecosystem. Your options:

1. **Custom Semgrep rules** -- Write rules that flag `fit()` before `train_test_split()`, or `StandardScaler().fit_transform()` on full dataset.
2. **Deepchecks in CI** -- Run the train/test validation suite as a CI step. This is the most practical approach:

```yaml
# .github/workflows/ml-checks.yml
name: ML Quality Gates
on: [push, pull_request]
jobs:
  ml-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - name: Run Deepchecks validation
        run: python scripts/run_validation_suite.py
      - name: Run Pandera schema tests
        run: pytest tests/test_schemas.py
      - name: Run Ruff
        run: ruff check .
```

3. **nbQA** -- Run linters on Jupyter notebooks. Note: Ruff 0.6+ natively supports notebooks, so nbQA is only needed for tools that don't (mypy, pylint).

### What each hook catches

| Hook | Catches | ML-specific? |
|------|---------|-------------|
| ruff | Unused imports, undefined names, pandas anti-patterns, numpy deprecations, security issues | Partially (PD/NPY rules) |
| nbstripout | Bloated notebook outputs in git, accidental data exposure in outputs | Yes (notebooks) |
| detect-secrets | API keys, passwords, tokens in committed code | No (general security) |
| check-added-large-files | Accidentally committed datasets or model files | Yes (ML repos) |
| Deepchecks (CI) | Data leakage, drift, train/test contamination | YES |
| Pandera (CI) | Schema violations, wrong dtypes, out-of-range values | Partially |

### VERDICT for Category 4

Install pre-commit with Ruff + nbstripout + detect-secrets + large file check on day 1 (15 minutes). Add Deepchecks and Pandera as CI steps in week 2. There is no magic "catch all ML bugs" pre-commit hook -- the closest thing is Deepchecks in CI.

---

## 5. Test Patterns for ML Pipelines

### Pattern 1: Schema tests with Pandera (data contract testing)

```python
import pandera as pa
from pandera import Column, Check, DataFrameSchema

raw_data_schema = DataFrameSchema({
    "patient_id": Column(int, Check.gt(0), nullable=False),
    "sbp": Column(float, Check.in_range(50, 300), nullable=True),
    "dbp": Column(float, Check.in_range(20, 200), nullable=True),
    "age": Column(int, Check.in_range(0, 120), nullable=False),
    "pulse_wave_velocity": Column(float, Check.gt(0), nullable=True),
})

def test_raw_data_conforms():
    df = load_raw_data()
    raw_data_schema.validate(df)
```

### Pattern 2: Property-based testing with Hypothesis

- **What:** Generate random inputs that satisfy constraints and verify properties hold for ALL inputs, not just hand-picked examples.
- **Works with scikit-learn:** Yes. Test that transforms are invertible, that predictions are within bounds, that feature importance sums are consistent.
- **Maturity:** Production-ready. Well-established Python library.
- **Setup effort:** Hours (learning the API + writing strategies for ML data).

```python
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.pandas import columns, data_frames, column
import numpy as np

# Test: StandardScaler output always has mean ~0, std ~1
@given(data_frames(columns=[
    column('feature_1', dtype=float, elements=st.floats(min_value=-1000, max_value=1000, allow_nan=False)),
    column('feature_2', dtype=float, elements=st.floats(min_value=-1000, max_value=1000, allow_nan=False)),
], index=st.just(pd.RangeIndex(100)))
)
@settings(max_examples=50)
def test_scaler_properties(df):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    assert np.abs(scaled.mean(axis=0)).max() < 1e-10
    assert np.abs(scaled.std(axis=0) - 1).max() < 1e-10
```

### Pattern 3: Deepchecks validation suites as tests

```python
import pytest
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import train_test_validation, data_integrity

def test_data_integrity():
    """Verify data has no integrity issues before training."""
    ds = Dataset(df, label='target', features=feature_cols)
    result = data_integrity().run(ds)
    assert result.passed(), f"Data integrity failed: {result.get_not_passed_checks()}"

def test_train_test_no_leakage():
    """Verify no leakage between train and test."""
    train_ds = Dataset(train_df, label='target')
    test_ds = Dataset(test_df, label='target')
    result = train_test_validation().run(train_ds, test_ds)
    assert result.passed(), f"Train/test validation failed: {result.get_not_passed_checks()}"
```

### Pattern 4: Determinism tests

```python
def test_model_determinism():
    """Verify same seed produces identical results."""
    from reproducibility import set_all_seeds

    set_all_seeds(42)
    model_1 = train_model(data)
    preds_1 = model_1.predict(test_data)

    set_all_seeds(42)
    model_2 = train_model(data)
    preds_2 = model_2.predict(test_data)

    np.testing.assert_array_equal(preds_1, preds_2)
```

### Pattern 5: Distribution shift tests (for multiple data waves)

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def test_no_significant_drift():
    """Verify new data hasn't drifted from training distribution."""
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=train_df, current_data=new_df)
    result = report.as_dict()
    drift_share = result['metrics'][0]['result']['share_of_drifted_columns']
    assert drift_share < 0.3, f"{drift_share:.0%} of columns drifted"
```

### Pattern 6: Hamilton DAG-specific testing

Hamilton's functional design makes unit testing natural:

```python
# Each Hamilton function is independently testable
from my_pipeline import compute_bmi, normalize_sbp

def test_compute_bmi():
    result = compute_bmi(weight_kg=pd.Series([70, 80]), height_m=pd.Series([1.75, 1.80]))
    assert (result > 0).all()
    assert (result < 100).all()  # sanity bound

def test_normalize_sbp():
    sbp = pd.Series([120, 140, 160])
    result = normalize_sbp(sbp=sbp)
    assert abs(result.mean()) < 1e-10  # zero-centered after normalization
```

### Pattern 7: Model performance regression tests

```python
def test_model_performance_above_baseline():
    """Guard against model degradation."""
    model = train_model(train_df)
    metrics = evaluate_model(model, test_df)

    assert metrics['r2'] > 0.5, f"R2 too low: {metrics['r2']}"
    assert metrics['mae'] < 15.0, f"MAE too high: {metrics['mae']}"
    # These thresholds should be updated as your model improves
```

### VERDICT for Category 5

**Start with Pandera schema tests** (they integrate directly into Hamilton) and **Deepchecks validation suites as pytest tests**. Add **Hypothesis property-based tests** for your data transforms. Add **determinism tests** early -- they are cheap and catch real bugs. Distribution shift and performance regression tests become valuable once you have a baseline model.

---

## Implementation Roadmap

### Day 1 (30 minutes)

1. Install pre-commit: `pip install pre-commit`
2. Create `.pre-commit-config.yaml` with Ruff + nbstripout + detect-secrets + large file check
3. Run `pre-commit install`
4. Add `ruff.toml` with NPY + PD + B rule sets

### Week 1 (2-4 hours)

1. Install Pandera: `pip install sf-hamilton[pandera]`
2. Define schemas for your raw data and key intermediate DataFrames
3. Add `@check_output(schema=...)` decorators to Hamilton functions
4. Install Deepchecks: `pip install deepchecks`
5. Write a basic `test_train_test_validation.py` using Deepchecks suite
6. Create `reproducibility.py` with `set_all_seeds()` function

### Week 2 (2-4 hours)

1. Set up DVC: `pip install dvc`, `dvc init`
2. Track your data files: `dvc add data/raw/`
3. Define pipeline in `dvc.yaml`
4. Set up MLflow: `pip install mlflow`, add `mlflow.autolog()` to training scripts
5. Set up basic GitHub Actions CI with Ruff + Pandera tests + Deepchecks

### Month 1 (ongoing)

1. Add Hypothesis property-based tests for data transforms
2. Add determinism tests
3. Add model performance regression tests
4. Consider Evidently if you receive new data waves

---

## Tool Comparison Matrix

| Tool | Category | Automated? | Hamilton? | PyCaret? | sklearn? | Maturity | Setup | Enforces? |
|------|----------|-----------|-----------|----------|----------|----------|-------|-----------|
| **Ruff** | Linting | Yes | Yes | Yes | Yes | Production | Minutes | Yes (blocks) |
| **Pyright** | Types | Yes | Partial | Partial | Partial | Production | Hours | Yes (blocks) |
| **LeakageDetector** | Static analysis | Yes | Poor | Partial | Yes | Emerging | Minutes | No (warns) |
| **Pandera** | Data validation | Yes | EXCELLENT | Yes | Yes | Production | Hours | Yes (blocks) |
| **Deepchecks** | ML validation | Yes | Yes | BUILT-IN | Yes | Production | Minutes | Yes (blocks) |
| **Great Expectations** | Data validation | Yes | Yes | Yes | Yes | Production | Days | Yes (blocks) |
| **Evidently** | Drift detection | Yes | Yes | Yes | Yes | Production | Minutes | No (reports) |
| **WhyLogs** | Data profiling | Yes | Yes | Yes | Yes | Production | Minutes | No (profiles) |
| **DVC** | Reproducibility | Yes | Yes | Yes | Yes | Production | Hours | YES (pipeline) |
| **MLflow** | Tracking | Yes | Yes | BUILT-IN | Yes | Production | Minutes | No (tracks) |
| **Sacred** | Tracking + seeds | Partial | Poor | Poor | Yes | Stable (stale) | Hours | Partial (seeds) |
| **Guild AI** | Tracking | Yes | Yes | Yes | Yes | Stable (niche) | Minutes | No (tracks) |
| **Hypothesis** | Testing | Yes | Yes | Yes | Yes | Production | Hours | Yes (blocks) |
| **nbstripout** | Notebooks | Yes | N/A | N/A | N/A | Production | Minutes | Yes (blocks) |
| **detect-secrets** | Security | Yes | N/A | N/A | N/A | Production | Minutes | Yes (blocks) |

---

## What to SKIP and Why

| Tool | Why skip |
|------|----------|
| Great Expectations | 107 dependencies, enterprise complexity, overkill for solo research. Pandera does the same with 12 deps. |
| Sacred | Ecosystem has moved on. Seed management pattern is trivially implementable without the framework. |
| Guild AI | MLflow has better ecosystem support and PyCaret integration. |
| W&B / Neptune / Comet | Cloud-hosted experiment tracking. Overkill and adds external dependency for solo research. MLflow local is sufficient. |
| nbQA | Ruff 0.6+ natively supports notebooks. nbQA only needed for tools without native notebook support. |

---

## Sources

### ML-Specific Static Analysis
- [LeakageDetector paper (arXiv)](https://arxiv.org/abs/2503.14723)
- [LeakageDetector 2.0 (arXiv)](https://arxiv.org/html/2509.15971)
- [LeakageDetector GitHub](https://github.com/malusamayo/leakage-analysis)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [Ruff rules reference](https://docs.astral.sh/ruff/rules/)
- [Data leakage static detection (ACM)](https://dl.acm.org/doi/10.1145/3551349.3556918)

### Data Validation
- [Pandera documentation](https://pandera.readthedocs.io/)
- [Pandera PyPI](https://pypi.org/project/pandera/)
- [Deepchecks GitHub](https://github.com/deepchecks/deepchecks)
- [Deepchecks train/test validation](https://docs.deepchecks.com/stable/tabular/auto_tutorials/quickstarts/plot_quick_train_test_validation.html)
- [Data validation landscape 2025](https://aeturrell.com/blog/posts/the-data-validation-landscape-in-2025/)
- [Hamilton + Pandera integration](https://blog.dagworks.io/p/data-quality-with-hamilton-and-pandera)
- [Hamilton data quality docs](https://multithreaded.stitchfix.com/blog/2022/07/26/hamilton-data-quality/)
- [Evidently AI GitHub](https://github.com/evidentlyai/evidently)
- [WhyLogs GitHub](https://github.com/whylabs/whylogs)
- [Pandera vs Great Expectations comparison](https://medium.com/@bhagyarana80/8-great-expectations-vs-pandera-which-fits-your-python-stack-a115c9241dcb)
- [Deepchecks vs Great Expectations](https://www.fuzzylabs.ai/blog-post/validation-deepchecks-vs-great-expectations)

### Reproducibility
- [DVC documentation](https://doc.dvc.org/)
- [DVC pipelines](https://doc.dvc.org/user-guide/pipelines)
- [MLflow autolog](https://mlflow.org/docs/latest/tracking/autolog/)
- [MLflow scikit-learn guide](https://mlflow.org/docs/latest/ml/traditional-ml/sklearn/guide/)
- [Sacred randomness docs](https://sacred.readthedocs.io/en/latest/randomness.html)
- [Guild AI](https://guild.ai/)
- [Sacred GitHub](https://github.com/IDSIA/sacred)
- [MLflow + DVC combined](https://towardsdatascience.com/use-mlflow-and-dvc-for-open-source-reproducible-machine-learning-2ab8c0678a94/)
- [Best ML experiment tracking tools 2025](https://neptune.ai/blog/best-ml-experiment-tracking-tools)

### Pre-commit / CI
- [Pre-commit framework](https://pre-commit.com/)
- [Top pre-commit hooks for ML (Medium)](https://medium.com/@andrii.suruhov/top-pre-commit-hooks-for-data-ml-analytics-projects-dd65ad4bb0a7)
- [Pre-commit for data scientists](https://kaushikmoudgalya.medium.com/pre-commit-for-data-scientists-5f8fcaefc9b2)
- [nbstripout GitHub](https://github.com/kynan/nbstripout)
- [nbQA GitHub](https://github.com/nbQA-dev/nbQA)
- [Scientific Python pre-commit guide](https://nsls-ii.github.io/scientific-python-cookiecutter/pre-commit.html)

### Testing Patterns
- [Effective testing for ML (Ploomber)](https://ploomber.io/blog/ml-testing-i/)
- [Testing ML systems (Made With ML)](https://madewithml.com/courses/mlops/testing/)
- [Art of testing ML pipelines (Fuzzy Labs)](https://www.fuzzylabs.ai/blog-post/the-art-of-testing-machine-learning-pipelines)
- [Hypothesis property-based testing](https://semaphore.io/blog/property-based-testing-python-hypothesis-pytest)
- [Testing ML code like scikit-learn](https://medium.com/analytics-vidhya/testing-ml-code-how-scikit-learn-does-it-97e45180e834)
- [Tools for ML model testing (Neptune)](https://neptune.ai/blog/tools-ml-model-testing)
- [Deepchecks as testing tool](https://www.deepchecks.com/best-tools-for-testing-machine-learning-algorithms/)

### Type Checking
- [NumPy typing fellowship retrospective](https://blog.scientific-python.org/numpy/fellowship-program-2025-retrospective/)
- [pandas-stubs PyPI](https://pypi.org/project/pandas-stubs/)
- [Pyright GitHub](https://github.com/microsoft/pyright)
- [mypy vs Pyright comparison](https://discuss.python.org/t/mypy-vs-pyright-in-practice/75984)
