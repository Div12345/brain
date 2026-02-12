# Research Pipeline Integration Architecture: DVC + Hamilton + W&B + Git

**Date:** 2026-02-12
**Context:** Mixed MATLAB (Windows) + Python (WSL) arterial waveform analysis pipeline
**Scope:** N=179 subjects, p=545 features, 4 model families, 180+ planned experiments
**Researcher:** Single PhD researcher

---

## Table of Contents

1. [Hamilton Testing/Validation Capabilities](#1-hamilton-testingvalidation-capabilities)
2. [DVC + Hamilton Integration (Macro + Micro DAGs)](#2-dvc--hamilton-integration)
3. [W&B + Hamilton Integration](#3-wb--hamilton-integration)
4. [DVC + W&B Integration](#4-dvc--wb-integration)
5. [Testing Pyramid for Research Pipelines](#5-testing-pyramid-for-research-pipelines)
6. [Data Validation Between MATLAB and Python](#6-data-validation-between-matlab-and-python)
7. [Configuration Management Across the Stack](#7-configuration-management-across-the-stack)

---

## 1. Hamilton Testing/Validation Capabilities

### 1.1 Built-in `@check_output` Decorator

Hamilton provides a native `@check_output` decorator that validates function outputs at runtime without external dependencies. This is your first line of defense for data quality.

**Source:** [Hamilton Data Quality writeup](https://github.com/apache/hamilton/blob/main/writeups/data_quality.md), [Context7 Hamilton docs](/apache/hamilton)

```python
from hamilton.function_modifiers import check_output
import pandas as pd
import numpy as np

@check_output(
    range=(40.0, 200.0),       # Physiological pressure range in mmHg
    data_type=np.float64,
    allow_nans=False,
    importance="fail"           # "warn" (default) or "fail" (halt execution)
)
def calibrated_sbp(raw_waveform: pd.Series, dbp: float, mbp: float) -> pd.Series:
    """Calibrated systolic blood pressure -- must be 40-200 mmHg."""
    calibrated = ((dbp - mbp) / (raw_waveform.min() - raw_waveform.mean())) * \
                 (raw_waveform - raw_waveform.mean()) + mbp
    return calibrated
```

**What `@check_output` supports natively:**
- `range=(min, max)` -- value bounds (perfect for physiological ranges)
- `data_type=` -- dtype enforcement
- `allow_nans=True/False` -- NaN control
- `values_in=[...]` -- categorical value enforcement
- `importance="fail"` -- halt vs warn

**What it enforces:** If `importance="fail"`, the pipeline stops. If `importance="warn"`, it logs a warning but continues. Default is warn.

**What breaks if you skip it:** Silent corruption. A calibration bug that produces 500 mmHg values propagates to feature extraction, then to modeling, then to results -- and you only notice when a reviewer questions your impossible predictions.

### 1.2 Pandera Integration for Complex Schemas

For validation beyond simple range checks (multi-column constraints, statistical properties, cross-column dependencies), Hamilton integrates with Pandera.

**Source:** [Hamilton + Pandera integration blog](https://blog.dagworks.io/p/data-quality-with-hamilton-and-pandera), [Pandera docs](https://pandera.readthedocs.io/)

**Install:** `pip install sf-hamilton[pandera]`

```python
import pandera as pa
import pandas as pd
from hamilton.function_modifiers import check_output

# Define a schema for the feature matrix
feature_matrix_schema = pa.DataFrameSchema({
    "subject_id": pa.Column(str, nullable=False, unique=True),
    "csbp": pa.Column(float, pa.Check.in_range(60, 250), nullable=False),
    "cpp": pa.Column(float, pa.Check.in_range(10, 120), nullable=False),
    "cfpwv": pa.Column(float, pa.Check.in_range(2.0, 30.0), nullable=True),
    # Waveform morphology features
    "augmentation_index": pa.Column(float, pa.Check.in_range(-50, 80)),
    "pulse_width_50": pa.Column(float, pa.Check.gt(0)),
}, strict=False, coerce=True)

@check_output(schema=feature_matrix_schema)
def feature_matrix(
    subject_ids: pd.Series,
    csbp_values: pd.Series,
    cpp_values: pd.Series,
    cfpwv_values: pd.Series,
    morphology_features: pd.DataFrame,
) -> pd.DataFrame:
    """Assemble final feature matrix. Pandera validates on every execution."""
    df = pd.DataFrame({
        "subject_id": subject_ids,
        "csbp": csbp_values,
        "cpp": cpp_values,
        "cfpwv": cfpwv_values,
    })
    return pd.concat([df, morphology_features], axis=1)
```

**Cross-column validation example (SBP > DBP always):**

```python
feature_schema = pa.DataFrameSchema({
    "sbp": pa.Column(float, pa.Check.in_range(60, 250)),
    "dbp": pa.Column(float, pa.Check.in_range(30, 160)),
}, checks=[
    pa.Check(lambda df: (df["sbp"] > df["dbp"]).all(),
             error="SBP must exceed DBP for every subject")
])
```

**What it enforces:** Schema violations raise `SchemaError` at runtime. The Hamilton pipeline halts before downstream nodes consume bad data.

**What breaks if you skip it:** You discover that 3 subjects have DBP > SBP (data entry error in outcomes spreadsheet) only after running 180 experiments. You have to re-run everything.

### 1.3 Testing Hamilton Functions Directly

Hamilton's functional design makes unit testing trivial -- each function is independently callable.

**Source:** [Hamilton testing best practices](https://hamilton.dagworks.io/en/latest/), existing doc at `/home/div/brain/knowledge/research/ml-codebase-trust-tooling-2026.md`

```python
# tests/test_calibration.py
import numpy as np
import pandas as pd
from python.src.pipeline import calibrate_waveform, extract_augmentation_index

def test_calibrate_known_signal():
    """Known input -> known output. The most basic trust check."""
    # Synthetic waveform: sine wave with known min/mean
    t = np.linspace(0, 1, 100)
    raw = np.sin(2 * np.pi * t)  # min=-1, mean=0
    raw_series = pd.Series(raw)

    result = calibrate_waveform(raw_waveform=raw_series, dbp=80.0, mbp=93.0)

    # min should map to DBP, mean should map to MBP
    assert abs(result.min() - 80.0) < 0.01, f"Min should be ~80, got {result.min()}"
    assert abs(result.mean() - 93.0) < 0.01, f"Mean should be ~93, got {result.mean()}"

def test_augmentation_index_known_waveform():
    """AI > 0 for a waveform with a secondary peak above primary."""
    # Create waveform where reflected wave exceeds incident wave
    waveform = pd.Series([0, 80, 60, 90, 40, 0])  # secondary peak (90) > primary (80)
    ai = extract_augmentation_index(calibrated_waveform=waveform)
    assert ai > 0, f"AI should be positive for this waveform, got {ai}"

def test_feature_count_matches_expectation():
    """Guard against accidental feature addition/removal."""
    # Use Hamilton driver to execute feature extraction
    from hamilton import driver
    import python.src.features as features_module

    dr = driver.Builder().with_modules(features_module).build()
    result = dr.execute(
        ["feature_names"],
        inputs={"calibrated_waveforms": test_waveforms}
    )
    assert len(result["feature_names"]) == 545, \
        f"Expected 545 features, got {len(result['feature_names'])}"
```

### 1.4 Hamilton Configuration Injection for Experiments

Hamilton's `@config.when` decorator and `driver.Builder().with_config()` provide configuration-driven DAG construction. This is how you switch between experiment configurations without changing code.

**Source:** [Hamilton config.when docs](https://hamilton.dagworks.io/en/latest/reference/decorators/config_when/), [Hamilton Builder docs](https://hamilton.dagworks.io/en/latest/concepts/builder/)

```python
# python/src/calibration.py
from hamilton.function_modifiers import config

@config.when(calibration_method="min_mean")
def calibrate_waveform__min_mean(
    raw_waveform: pd.Series, dbp: float, mbp: float
) -> pd.Series:
    """Min-mean calibration: min(signal) -> DBP, mean(signal) -> MBP."""
    return ((dbp - mbp) / (raw_waveform.min() - raw_waveform.mean())) * \
           (raw_waveform - raw_waveform.mean()) + mbp

@config.when(calibration_method="foot")
def calibrate_waveform__foot(
    raw_waveform: pd.Series, dbp: float, mbp: float, foot_index: int
) -> pd.Series:
    """Foot calibration: foot(signal) -> DBP, mean(signal) -> MBP."""
    foot_val = raw_waveform.iloc[foot_index]
    return ((dbp - mbp) / (foot_val - raw_waveform.mean())) * \
           (raw_waveform - raw_waveform.mean()) + mbp
```

```python
# python/src/run_modeling.py -- the script DVC calls
import json
from hamilton import driver
import python.src.calibration as calib_module
import python.src.features as feat_module
import python.src.modeling as model_module

def main(config_path: str):
    with open(config_path) as f:
        config = json.load(f)

    # Config determines WHICH functions are in the DAG
    dr = (
        driver.Builder()
        .with_modules(calib_module, feat_module, model_module)
        .with_config({
            "calibration_method": config["calibration"]["method"],  # "min_mean" or "foot"
            "model_family": config["modeling"]["family"],            # "linear", "l1", "l2", "tree"
        })
        .build()
    )

    # Inputs are runtime data; config determines DAG structure
    results = dr.execute(
        final_vars=["metrics", "predictions", "feature_importances"],
        inputs={
            "feature_matrix_path": config["paths"]["feature_matrix"],
            "outcomes_path": config["paths"]["outcomes"],
            "random_seed": config["modeling"]["random_seed"],
            "cv_folds": config["modeling"]["cv_folds"],
            "target": config["modeling"]["target"],  # "csbp", "cpp", or "cfpwv"
        }
    )
    return results

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
```

**Key distinction:** `with_config()` determines DAG *structure* (which functions exist). `inputs={}` provides runtime *data*. Config is set once at build time; inputs change per execution.

**What it enforces:** If you pass `calibration_method="typo"`, Hamilton raises an error at build time because no `@config.when(calibration_method="typo")` function exists. You cannot accidentally run with an undefined configuration.

**What breaks if you skip it:** You use if/else branches inside functions instead. These are invisible to Hamilton's DAG, untestable in isolation, and create silent dead code paths.

---

## 2. DVC + Hamilton Integration

### 2.1 The Two-DAG Architecture

**Macro DAG (DVC):** Cross-language pipeline stages. Each stage is an OS-level command.
```
MATLAB ensemble_average --> MATLAB calibrate --> Python model
```

**Micro DAG (Hamilton):** Function-level Python transformations within a single DVC stage.
```
load_features --> select_features --> scale --> train --> evaluate --> metrics
```

**How they compose:** DVC calls a Python script. That script internally creates a Hamilton driver and executes the micro DAG. DVC sees only inputs/outputs at the stage boundary; Hamilton manages everything inside.

```
dvc.yaml stage "train_model"
    cmd: python python/src/run_modeling.py config/experiment.json
    |
    v
run_modeling.py
    |-- reads config/experiment.json
    |-- builds Hamilton driver with config
    |-- dr.execute(["metrics", "model"], inputs={...})
    |       |
    |       v
    |   Hamilton micro-DAG:
    |       load_features -> validate_schema -> select_features
    |       -> scale -> split -> train -> evaluate -> metrics
    |
    |-- writes results/metrics.json
    |-- writes results/models/best_model.pkl
```

### 2.2 DVC Stage Wrapping Hamilton Driver

**Source:** [DVC pipeline docs](https://dvc.org/doc/user-guide/pipelines/defining-pipelines), [Hamilton wrapping driver docs](https://hamilton.dagworks.io/en/latest/how-tos/wrapping-driver/)

```yaml
# dvc.yaml
stages:
  # --- MATLAB stages (macro DAG) ---
  ensemble_average:
    cmd: matlab -batch "run_pipeline('ensemble', 'config/experiment.json')"
    deps:
      - data/raw/Control_Data/
      - data/curated/beat_indices/
      - matlab/+sigproc/ensemble_average.m
      - config/experiment.json
    params:
      - config/experiment.json:
          - ensemble_averaging
    outs:
      - data/interim/01_ensemble_averaged/

  calibrate:
    cmd: matlab -batch "run_pipeline('calibrate', 'config/experiment.json')"
    deps:
      - data/interim/01_ensemble_averaged/
      - matlab/+calib/apply_calibration.m
      - config/experiment.json
    params:
      - config/experiment.json:
          - calibration
    outs:
      - data/interim/02_calibrated/
      - data/processed/feature_matrix.csv

  # --- Python stage (Hamilton micro DAG inside) ---
  train_model:
    cmd: python python/src/run_modeling.py config/experiment.json
    deps:
      - data/processed/feature_matrix.csv
      - data/external/outcomes.xlsx
      - python/src/run_modeling.py
      - python/src/calibration.py
      - python/src/features.py
      - python/src/modeling.py
      - config/experiment.json
    params:
      - config/experiment.json:
          - modeling
    outs:
      - results/models/best_model.pkl
    metrics:
      - results/metrics.json:
          cache: false
    plots:
      - results/plots/bland_altman.csv:
          x: mean
          y: diff
```

**Critical detail for `deps`:** List all Python source files that Hamilton imports as modules. If you change a Hamilton function in `features.py`, DVC must know to re-run the stage. This is the coupling point between the two DAGs.

**What it enforces:** DVC's hash-based dependency tracking ensures that:
- If MATLAB code changes, MATLAB stages re-run
- If Python code changes, Python stages re-run
- If config changes, only affected stages re-run (via `params:` section)
- If nothing changes, `dvc repro` is a no-op

**What breaks if you skip it:** You manually run scripts in the wrong order, or forget to re-run calibration after changing a filter parameter. Results are silently stale.

### 2.3 Best Practice: Thin Wrapper Script Pattern

The Python script that DVC calls should be a **thin wrapper** -- it reads config, builds the Hamilton driver, executes, and writes outputs. No business logic in the wrapper.

```python
# python/src/run_modeling.py -- THIN WRAPPER
"""DVC-callable entry point. All logic lives in Hamilton modules."""
import json
import sys
from hamilton import driver
import python.src.features as feat_mod
import python.src.modeling as model_mod
import python.src.validation as val_mod

def main(config_path: str):
    with open(config_path) as f:
        full_config = json.load(f)

    model_config = full_config["modeling"]

    dr = (
        driver.Builder()
        .with_modules(feat_mod, model_mod, val_mod)
        .with_config({
            "model_family": model_config["family"],
            "feature_selection": model_config.get("feature_selection", "none"),
        })
        .build()
    )

    results = dr.execute(
        final_vars=["metrics_dict", "trained_model", "predictions"],
        inputs={
            "feature_matrix_path": full_config["paths"]["feature_matrix"],
            "outcomes_path": full_config["paths"]["outcomes"],
            "target_variable": model_config["target"],
            "cv_folds": model_config["cv_folds"],
            "random_seed": model_config["random_seed"],
            "alpha": model_config.get("alpha", 1.0),
        }
    )

    # Write outputs for DVC to track
    with open("results/metrics.json", "w") as f:
        json.dump(results["metrics_dict"], f, indent=2)

    import joblib
    joblib.dump(results["trained_model"], "results/models/best_model.pkl")

if __name__ == "__main__":
    main(sys.argv[1])
```

**Rule:** If you are writing `if/else` or `for` loops in this file, you are doing it wrong. Move that logic into a Hamilton module where it becomes a testable, trackable DAG node.

---

## 3. W&B + Hamilton Integration

### 3.1 Architecture: W&B Wraps Hamilton (Not the Reverse)

W&B should initialize *outside* the Hamilton DAG, in the wrapper script. Hamilton nodes should not call `wandb.log()` directly -- that couples your pipeline logic to a specific tracking tool.

**Source:** [Hamilton lifecycle adapters](https://hamilton.dagworks.io/en/latest/reference/lifecycle-hooks/), [Hamilton MLFlowTracker](https://hamilton.dagworks.io/en/latest/reference/lifecycle-hooks/MLFlowTracker/) (pattern transferable to W&B), [W&B docs](https://docs.wandb.ai/models/track/config)

**Pattern:** Use Hamilton's lifecycle adapter system to create a W&B adapter that automatically logs node outputs without modifying pipeline code.

### 3.2 Custom W&B Lifecycle Adapter

Hamilton has a built-in `MLFlowTracker` adapter. There is no built-in W&B adapter, but the lifecycle API makes it straightforward to create one.

```python
# python/src/adapters/wandb_tracker.py
"""Hamilton lifecycle adapter for Weights & Biases experiment tracking."""
import wandb
import numpy as np
import pandas as pd
from typing import Any, Dict, Optional

from hamilton.lifecycle.api import (
    NodeExecutionHook,
    GraphExecutionHook,
)


class WandbTracker(NodeExecutionHook, GraphExecutionHook):
    """Logs Hamilton DAG execution to W&B.

    Usage:
        tracker = WandbTracker(project="arterial-analysis", config=my_config)
        dr = driver.Builder()
            .with_modules(...)
            .with_adapters(tracker)
            .build()
    """

    def __init__(
        self,
        project: str,
        config: dict,
        tags: list[str] = None,
        log_nodes: list[str] = None,  # None = log final_vars only
        notes: str = None,
    ):
        self.project = project
        self.config = config
        self.tags = tags or []
        self.log_nodes = log_nodes  # explicit allowlist of nodes to log
        self.notes = notes
        self.run = None

    # --- Graph-level hooks ---
    def run_before_graph_execution(self, **kwargs):
        """Start W&B run before Hamilton executes."""
        self.run = wandb.init(
            project=self.project,
            config=self.config,
            tags=self.tags,
            notes=self.notes,
            reinit=True,
        )

    def run_after_graph_execution(self, **kwargs):
        """Finish W&B run after Hamilton completes."""
        if self.run:
            self.run.finish()
            self.run = None

    # --- Node-level hooks ---
    def run_before_node_execution(self, *, node_name: str, **kwargs):
        pass  # No pre-execution logging needed

    def run_after_node_execution(
        self,
        *,
        node_name: str,
        node_tags: Dict[str, Any],
        result: Any,
        error: Optional[Exception],
        success: bool,
        **future_kwargs,
    ):
        """Log node results to W&B based on type."""
        if not success or self.run is None:
            return

        # Only log nodes in allowlist (or all final_vars if None)
        if self.log_nodes and node_name not in self.log_nodes:
            return

        # Auto-log based on result type
        if isinstance(result, dict):
            # Metrics dicts get logged directly
            self.run.log({f"{node_name}/{k}": v for k, v in result.items()
                         if isinstance(v, (int, float, np.floating))})
        elif isinstance(result, (int, float, np.floating)):
            self.run.log({node_name: result})
        elif isinstance(result, pd.DataFrame) and len(result) < 1000:
            # Small DataFrames become W&B Tables
            self.run.log({node_name: wandb.Table(dataframe=result)})
```

### 3.3 Using the Adapter in the Wrapper Script

```python
# python/src/run_modeling.py -- with W&B integration
import json
import sys
import wandb
from hamilton import driver
from python.src.adapters.wandb_tracker import WandbTracker
import python.src.features as feat_mod
import python.src.modeling as model_mod

def main(config_path: str):
    with open(config_path) as f:
        full_config = json.load(f)

    model_config = full_config["modeling"]

    # W&B adapter -- config is logged automatically
    tracker = WandbTracker(
        project="arterial-analysis",
        config={
            **model_config,
            "config_path": config_path,
            "calibration_method": full_config["calibration"]["method"],
        },
        tags=[model_config["family"], full_config["calibration"]["method"]],
        log_nodes=["metrics_dict", "cv_results", "feature_importances"],
        notes=f"Target: {model_config['target']}, Family: {model_config['family']}",
    )

    dr = (
        driver.Builder()
        .with_modules(feat_mod, model_mod)
        .with_config({"model_family": model_config["family"]})
        .with_adapters(tracker)  # <-- single line adds W&B tracking
        .build()
    )

    results = dr.execute(
        final_vars=["metrics_dict", "trained_model", "predictions"],
        inputs={...}
    )

    # Write metrics for DVC (file-based tracking)
    with open("results/metrics.json", "w") as f:
        json.dump(results["metrics_dict"], f, indent=2)

if __name__ == "__main__":
    main(sys.argv[1])
```

### 3.4 Tracking Which Hamilton Config Produced Which W&B Run

The `WandbTracker` logs the full config dict to W&B at run start. To link back:

```python
# In WandbTracker.run_before_graph_execution:
self.run = wandb.init(
    config={
        # Hamilton DAG config (determines structure)
        "hamilton_config": {"model_family": "l1", "calibration_method": "min_mean"},
        # Runtime inputs
        "target": "csbp",
        "cv_folds": 10,
        "alpha": 0.5,
        # Provenance
        "git_hash": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
        "dvc_repro_hash": os.environ.get("DVC_STAGE_HASH", "unknown"),
    }
)
```

In the W&B UI, you can then filter/group runs by `config.hamilton_config.model_family` or `config.target`.

**What it enforces:** Every W&B run has a complete record of both the DAG structure (which functions ran) and the runtime parameters (what values were used). You can reconstruct any experiment.

**What breaks if you skip it:** You have 180 W&B runs with metrics but no way to know which Hamilton configuration produced them. "Which run used foot calibration with L1 regularization?" becomes an archaeological expedition.

---

## 4. DVC + W&B Integration

### 4.1 Complementary Roles (They Do Not Conflict)

**Source:** [Neptune.ai DVC alternatives](https://neptune.ai/blog/dvc-alternatives-for-experiment-tracking), [DVC experiment tracking docs](https://doc.dvc.org/use-cases/experiment-tracking)

| Concern | DVC handles it | W&B handles it |
|---------|---------------|----------------|
| Data versioning (580MB raw data) | YES -- `dvc add`, content-addressable storage | No |
| Pipeline DAG definition | YES -- `dvc.yaml` | No |
| Pipeline reproducibility | YES -- `dvc repro`, hash-based deps | No |
| Config parameter tracking | YES -- `params:` in dvc.yaml | YES -- `wandb.config` |
| Metrics comparison | Basic -- `dvc metrics diff` | RICH -- dashboards, charts, tables |
| Experiment comparison across 180 runs | Awkward -- `dvc exp show` is tabular | EXCELLENT -- W&B UI filters, grouping, parallel coordinates |
| Model artifacts | YES -- `dvc push` to remote | YES -- `wandb.Artifact` |
| Cross-language stages (MATLAB) | YES -- any shell command | No |

**The split:** DVC owns **reproducibility** (can you re-run it?). W&B owns **analysis** (which run was best and why?).

### 4.2 Linking DVC Pipeline Runs to W&B Experiments

The link is the **git commit hash + config file contents**. Both systems can access these.

```python
# In run_modeling.py, log DVC provenance to W&B
import subprocess
import os

def get_dvc_info():
    """Capture DVC state for W&B logging."""
    git_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode().strip()

    git_dirty = subprocess.check_output(
        ["git", "status", "--porcelain"]
    ).decode().strip()

    return {
        "git_commit": git_hash,
        "git_dirty": len(git_dirty) > 0,
        "dvc_stage": os.environ.get("DVC_STAGE", "unknown"),
    }

# In wandb.init:
wandb.init(
    config={
        **model_config,
        **get_dvc_info(),
    }
)
```

### 4.3 `dvc exp` and W&B: Peaceful Coexistence

`dvc exp` creates lightweight git branches for parameter sweeps. W&B creates runs. They do not conflict because they operate on different layers:

- `dvc exp run -S modeling.alpha=0.1` -- changes a param, runs the pipeline, creates a DVC experiment
- Inside that pipeline run, `wandb.init()` creates a W&B run
- Both record the same metrics, but in different systems

**Recommended workflow:**

```bash
# Option A: DVC-driven experiment sweep (small scale, <10 experiments)
dvc exp run -S config/experiment.json:modeling.alpha=0.1
dvc exp run -S config/experiment.json:modeling.alpha=0.5
dvc exp run -S config/experiment.json:modeling.alpha=1.0
dvc exp show  # Quick comparison

# Option B: Script-driven sweep with W&B (large scale, 180 experiments)
# Write a sweep script that iterates configs, each calling the Hamilton driver
# W&B handles comparison via its dashboard
python python/src/sweep.py --config config/sweep_definition.json
```

For 180 experiments, **Option B is better**. DVC experiments are designed for iterative exploration (try a few things, compare, pick one). W&B is designed for systematic sweeps with rich comparison.

**Recommended split for your project:**
- Use `dvc repro` for the full pipeline (MATLAB + Python)
- Use `dvc exp` only when manually exploring parameter changes (< 10 at a time)
- Use W&B for the 180-experiment systematic comparison
- Let both log metrics; use W&B for analysis, DVC for reproducibility

**What breaks if you skip the link:** You find a great run in W&B (RMSE = 8.2 mmHg) but cannot reproduce it because you do not know which git commit and data version produced it.

---

## 5. Testing Pyramid for Research Pipelines

### 5.1 Adapted Testing Pyramid for Single Researcher

The classic 70/20/10 ratio (unit/integration/E2E) does not apply directly to research code. For a single PhD researcher, the constraint is **time**, not coverage.

**Source:** [Martin Fowler - Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html), existing doc at `/home/div/brain/knowledge/research/ml-codebase-trust-tooling-2026.md`

**Recommended pyramid:**

```
                /\
               /  \
              / R  \          Reproducibility tests (dvc repro)
             /  E   \         ~2 tests, run weekly or before paper submission
            / P R O  \
           /----------\
          / INTEGRATION \     Hamilton @check_output + Pandera schemas
         /  (automatic)  \    ~15-20 schemas, run on every pipeline execution
        /------------------\
       /    UNIT TESTS      \  Individual function correctness
      /  (pytest, manual)    \ ~30-50 tests, run on every commit
     /________________________\
```

### 5.2 Unit Tests: Individual Function Correctness

**What to test:** Calibration formulas, feature extraction, data loading, config parsing.

**How many:** One test per "non-trivial" function. Skip trivial wrappers.

**Run when:** Every `git commit` (via pre-commit or CI).

```python
# tests/unit/test_calibration.py
def test_min_mean_calibration_identity():
    """If raw signal has min=DBP and mean=MBP, output equals input."""
    raw = pd.Series([80.0, 93.0, 106.0])  # min=80 (DBP), mean=93 (MBP)
    result = calibrate_waveform__min_mean(raw_waveform=raw, dbp=80.0, mbp=93.0)
    pd.testing.assert_series_equal(result, raw)

def test_min_mean_calibration_scaling():
    """Known scaling: raw [-1, 0, 1] with DBP=80, MBP=90 -> [80, 90, 100]."""
    raw = pd.Series([-1.0, 0.0, 1.0])
    result = calibrate_waveform__min_mean(raw_waveform=raw, dbp=80.0, mbp=90.0)
    expected = pd.Series([80.0, 90.0, 100.0])
    pd.testing.assert_series_equal(result, expected)
```

### 5.3 Integration Tests: Stage Output Shape/Range (Hamilton's Validation Layer)

**What to test:** Data flowing between stages has expected schema, range, completeness.

**How many:** One Pandera schema per key DataFrame in the pipeline (~5-8 schemas).

**Run when:** Every pipeline execution (automatic via `@check_output`).

```python
# python/src/validation.py -- loaded as a Hamilton module
import pandera as pa
from hamilton.function_modifiers import check_output

# Schema for the MATLAB -> Python handoff
handoff_schema = pa.DataFrameSchema({
    "subject_id": pa.Column(str, nullable=False),
    "n_beats": pa.Column(int, pa.Check.in_range(3, 100)),
    "sampling_rate": pa.Column(int, pa.Check.isin([100, 128, 200, 256, 500, 1000])),
}, checks=[
    pa.Check(lambda df: len(df) >= 100,
             error="Expected at least 100 subjects after QC filtering"),
])

@check_output(schema=handoff_schema)
def loaded_feature_matrix(feature_matrix_path: str) -> pd.DataFrame:
    """Load feature matrix from MATLAB output. Pandera validates automatically."""
    return pd.read_csv(feature_matrix_path)
```

### 5.4 Pipeline Tests: End-to-End Reproducibility

**What to test:** `dvc repro` on the same commit produces the same `metrics.json`.

**How many:** 1-2 tests.

**Run when:** Before paper submission, after major refactors.

```bash
#!/bin/bash
# tests/pipeline/test_reproducibility.sh

# Run 1
dvc repro
cp results/metrics.json /tmp/metrics_run1.json

# Run 2 (clean and re-run)
dvc repro --force
cp results/metrics.json /tmp/metrics_run2.json

# Compare
python -c "
import json
m1 = json.load(open('/tmp/metrics_run1.json'))
m2 = json.load(open('/tmp/metrics_run2.json'))
for key in m1:
    assert abs(m1[key] - m2[key]) < 1e-10, f'{key}: {m1[key]} != {m2[key]}'
print('PASS: Pipeline is deterministic')
"
```

### 5.5 Minimal Viable Testing Setup (Week 1)

For a single researcher with limited time:

| Priority | Test | Effort | Value |
|----------|------|--------|-------|
| 1 (do now) | `@check_output(range=(...))` on calibrated pressures | 5 min per function | Catches physics violations |
| 2 (do now) | Pandera schema on feature_matrix handoff | 30 min | Catches MATLAB/Python mismatch |
| 3 (week 1) | 5 unit tests for calibration formula | 1 hour | Catches math bugs |
| 4 (week 2) | Determinism test | 30 min | Catches random seed issues |
| 5 (later) | Deepchecks train/test validation | 2 hours | Catches data leakage |

**What breaks if you skip it:** You submit a paper with a calibration bug that makes all SBP values 10 mmHg too high. A reviewer asks for your code. You rerun it and get different numbers because random seeds were not set. You cannot reproduce your own results.

---

## 6. Data Validation Between MATLAB and Python

### 6.1 The Handoff Problem

MATLAB writes `.mat` files (or `.csv`). Python reads them. Between write and read, several things can go wrong:
- MATLAB struct field names do not match Python expected keys
- MATLAB saves v7.3 (HDF5) but Python uses `scipy.io.loadmat` (v7 only)
- MATLAB writes NaN where Python expects a number
- MATLAB saves 370 files but Python expects 380 (some subjects dropped silently)

### 6.2 Where Validation Lives: Hamilton, Not DVC

DVC tracks **whether files changed** (hash-based). It cannot validate **what is inside** files. Validation belongs in the Hamilton micro-DAG, as the first node after loading.

**Source:** [scipy.io.loadmat docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html), [Pandera docs](https://pandera.readthedocs.io/)

```python
# python/src/data_loading.py -- Hamilton module
import scipy.io as sio
import pandas as pd
import numpy as np
import os
from pathlib import Path
from hamilton.function_modifiers import check_output
import pandera as pa


def _validate_mat_file(mat_dict: dict, subject_id: str) -> None:
    """Validate a single .mat file has expected structure.

    Raises ValueError with detailed message if validation fails.
    """
    required_keys = {"betterankle", "brachial", "metadata"}
    actual_keys = {k for k in mat_dict.keys() if not k.startswith("__")}
    missing = required_keys - actual_keys
    if missing:
        raise ValueError(
            f"Subject {subject_id}: .mat file missing keys {missing}. "
            f"Available: {actual_keys}"
        )

    for signal_name in ["betterankle", "brachial"]:
        signal = mat_dict[signal_name]
        if signal.ndim != 2 or signal.shape[1] != 3:
            raise ValueError(
                f"Subject {subject_id}: {signal_name} shape is {signal.shape}, "
                f"expected (N, 3) for 3 selected beats"
            )
        if signal.shape[0] < 50:
            raise ValueError(
                f"Subject {subject_id}: {signal_name} has only {signal.shape[0]} "
                f"samples. Minimum expected: 50"
            )

        # Pressure range check (calibrated values should be 30-220 mmHg)
        if np.nanmin(signal) < 30 or np.nanmax(signal) > 220:
            raise ValueError(
                f"Subject {subject_id}: {signal_name} values "
                f"[{np.nanmin(signal):.1f}, {np.nanmax(signal):.1f}] "
                f"outside physiological range [30, 220] mmHg"
            )


def load_ensemble_mat_files(ensemble_dir: str) -> pd.DataFrame:
    """Load all ensemble-averaged .mat files with validation.

    This is a Hamilton node -- it runs validation on every execution.
    """
    records = []
    mat_files = sorted(Path(ensemble_dir).glob("*.mat"))

    if len(mat_files) < 100:
        raise ValueError(
            f"Expected >= 100 .mat files in {ensemble_dir}, found {len(mat_files)}"
        )

    for mat_path in mat_files:
        subject_id = mat_path.stem
        mat = sio.loadmat(str(mat_path))
        _validate_mat_file(mat, subject_id)  # Fails fast on bad data

        ankle = mat["betterankle"]
        brachial = mat["brachial"]

        records.append({
            "subject_id": subject_id,
            "ankle_waveform": ankle.mean(axis=1),  # Average 3 beats
            "brachial_waveform": brachial.mean(axis=1),
            "n_samples": ankle.shape[0],
        })

    return pd.DataFrame(records)
```

### 6.3 Pandera Schema at the Handoff Boundary

After loading .mat files into a DataFrame, apply a Pandera schema:

```python
# Schema for the MATLAB -> Python boundary
matlab_handoff_schema = pa.DataFrameSchema({
    "subject_id": pa.Column(str, nullable=False, unique=True),
    "ankle_waveform": pa.Column(object),  # numpy arrays stored as objects
    "brachial_waveform": pa.Column(object),
    "n_samples": pa.Column(int, pa.Check.in_range(50, 2000)),
}, checks=[
    pa.Check(lambda df: len(df) >= 100,
             error="Fewer than 100 subjects after loading"),
    pa.Check(lambda df: df["n_samples"].std() < 500,
             error="Extreme variation in waveform lengths suggests mixed sampling rates"),
])

@check_output(schema=matlab_handoff_schema)
def loaded_ensemble_data(ensemble_dir: str) -> pd.DataFrame:
    return load_ensemble_mat_files(ensemble_dir)
```

### 6.4 Pandera vs Great Expectations for This Project

**Use Pandera.** The decision is clear for a single-researcher project.

| Criterion | Pandera | Great Expectations |
|-----------|---------|-------------------|
| Dependencies | 12 packages | 107 packages |
| Hamilton integration | First-class (`@check_output`) | Manual wrapping |
| Learning curve | Hours | Days |
| Schema definition | Python code (familiar) | JSON/YAML DSL or Python |
| Sufficient for N=179? | Yes | Massive overkill |

**Source:** Existing doc at `/home/div/brain/knowledge/research/ml-codebase-trust-tooling-2026.md`

### 6.5 Completeness Checks

Beyond schema validation, check that the expected set of subjects survived the handoff:

```python
def validate_subject_completeness(
    loaded_data: pd.DataFrame,
    expected_subjects_path: str,
) -> pd.DataFrame:
    """Verify no subjects were silently dropped during MATLAB processing."""
    expected = pd.read_csv(expected_subjects_path)["subject_id"].tolist()
    actual = loaded_data["subject_id"].tolist()

    missing = set(expected) - set(actual)
    extra = set(actual) - set(expected)

    if missing:
        raise ValueError(
            f"{len(missing)} subjects missing after MATLAB processing: "
            f"{sorted(list(missing))[:10]}..."
        )
    if extra:
        raise ValueError(
            f"{len(extra)} unexpected subjects in MATLAB output: "
            f"{sorted(list(extra))[:10]}..."
        )

    return loaded_data  # Pass through if valid
```

**What it enforces:** The Python pipeline cannot start unless it receives the exact subjects it expects. A MATLAB bug that silently drops subjects (e.g., `for i=1:5` instead of `for i=1:N`) is caught immediately.

**What breaks if you skip it:** You train on 370 subjects, but 50 were silently dropped because a MATLAB loop had a hardcoded limit. Your N=179 becomes N=129 with no warning. Your paper reports the wrong sample size.

---

## 7. Configuration Management Across the Stack

### 7.1 The Four Config Consumers

Your pipeline has four systems that need configuration:

1. **MATLAB** -- reads JSON via `jsondecode(fileread(...))`
2. **Python/Hamilton** -- reads JSON via `json.load()`, builds driver with `with_config()`
3. **DVC** -- tracks JSON params via `params:` in `dvc.yaml`
4. **W&B** -- logs config via `wandb.init(config=...)`

### 7.2 Single Source of Truth: One JSON File

**Source:** [DVC params docs](https://dvc.org/doc/command-reference/params), [W&B config docs](https://docs.wandb.ai/models/track/config), existing doc at `/home/div/brain/knowledge/research/biomedical-signal-processing-codebase-organization.md`

```json
// config/experiment.json -- THE ONE CONFIG FILE
{
  "experiment_name": "minmean_l1_csbp_alpha05",
  "version": "1.0",

  "ensemble_averaging": {
    "min_beats": 10,
    "alignment_method": "r_peak",
    "outlier_rejection_sd": 2.5
  },

  "calibration": {
    "method": "min_mean",
    "pressure_source": "brachial_map"
  },

  "feature_extraction": {
    "normalize": true,
    "features_to_extract": ["morphology", "timing", "spectral"]
  },

  "modeling": {
    "family": "l1",
    "target": "csbp",
    "cv_folds": 10,
    "random_seed": 42,
    "alpha": 0.5,
    "feature_selection": "lasso_path"
  },

  "paths": {
    "raw_data": "data/raw/Control_Data",
    "ensemble_dir": "data/interim/01_ensemble_averaged",
    "calibrated_dir": "data/interim/02_calibrated",
    "feature_matrix": "data/processed/feature_matrix.csv",
    "outcomes": "data/external/outcomes.xlsx"
  }
}
```

### 7.3 How Each Consumer Reads It

**MATLAB:**
```matlab
config = jsondecode(fileread('config/experiment.json'));
min_beats = config.ensemble_averaging.min_beats;  % 10
method = config.calibration.method;                % "min_mean"
```

**Python/Hamilton:**
```python
import json
with open("config/experiment.json") as f:
    config = json.load(f)

# Hamilton DAG structure config
dr = driver.Builder().with_config({
    "calibration_method": config["calibration"]["method"],
    "model_family": config["modeling"]["family"],
}).build()

# Hamilton runtime inputs
dr.execute(["metrics"], inputs={
    "random_seed": config["modeling"]["random_seed"],
    "alpha": config["modeling"]["alpha"],
})
```

**DVC (tracks parameter changes):**
```yaml
# dvc.yaml
stages:
  train_model:
    cmd: python python/src/run_modeling.py config/experiment.json
    params:
      - config/experiment.json:
          - modeling.family
          - modeling.target
          - modeling.cv_folds
          - modeling.alpha
          - calibration.method
```

DVC reads the JSON file directly (JSON is a supported params format alongside YAML and TOML). When you change `modeling.alpha` from 0.5 to 1.0, `dvc repro` knows to re-run `train_model` but not `ensemble_average`.

**W&B:**
```python
import json
with open("config/experiment.json") as f:
    config = json.load(f)

wandb.init(
    project="arterial-analysis",
    config=config,  # Logs the ENTIRE config dict
    name=config["experiment_name"],
)
```

### 7.4 Keeping Them in Sync

The sync problem is solved by architecture: all four consumers read the **same file**. There is no sync because there is no duplication.

| Consumer | Reads from | Writes to | Sync needed? |
|----------|-----------|-----------|-------------|
| MATLAB | `config/experiment.json` | Nothing | No |
| Hamilton | `config/experiment.json` | Nothing | No |
| DVC | `config/experiment.json` (via params) | `dvc.lock` (hashes) | No |
| W&B | `config/experiment.json` (via Python) | W&B cloud (run config) | No |

**The one rule:** Never hardcode parameters in MATLAB functions, Python functions, dvc.yaml, or wandb.init. Always read from `config/experiment.json`.

### 7.5 Experiment Variation Pattern

For 180 experiments, you need multiple configs. Two approaches:

**Approach A: Named config files (simple, explicit)**
```
config/
  experiments/
    minmean_linear_csbp.json
    minmean_l1_csbp_alpha01.json
    minmean_l1_csbp_alpha05.json
    foot_l2_cpp.json
    ...
```

Each file is a complete config. Run with:
```bash
dvc repro --set-param config=config/experiments/minmean_l1_csbp_alpha05.json
# or
python python/src/run_modeling.py config/experiments/minmean_l1_csbp_alpha05.json
```

**Approach B: Base config + override pattern (DRY)**
```python
# python/src/sweep.py
import json
import itertools

base = json.load(open("config/experiment.json"))

sweep_grid = {
    "calibration.method": ["min_mean", "foot"],
    "modeling.family": ["linear", "l1", "l2", "tree"],
    "modeling.target": ["csbp", "cpp", "cfpwv"],
    "modeling.alpha": [0.01, 0.1, 0.5, 1.0, 5.0, 10.0],
}

for combo in itertools.product(*sweep_grid.values()):
    exp_config = json.loads(json.dumps(base))  # deep copy
    for key, value in zip(sweep_grid.keys(), combo):
        parts = key.split(".")
        d = exp_config
        for p in parts[:-1]:
            d = d[p]
        d[parts[-1]] = value

    exp_config["experiment_name"] = "_".join(str(v) for v in combo)

    # Write temp config and run
    config_path = f"/tmp/exp_{exp_config['experiment_name']}.json"
    with open(config_path, "w") as f:
        json.dump(exp_config, f)

    # Each run logs to W&B via the Hamilton adapter
    os.system(f"python python/src/run_modeling.py {config_path}")
```

**What it enforces:** Every experiment has a complete, self-describing config. W&B stores the full config. You can reproduce any experiment by feeding its config back to the pipeline.

**What breaks if you skip it:** You have 180 W&B runs but half of them used a hardcoded `alpha=1.0` in the Python code that overrode the config value. Your comparison is invalid but you do not know it.

---

## Summary: Integration Map

```
config/experiment.json -----> MATLAB (reads JSON natively)
        |                          |
        |                     writes .mat files
        |                          |
        |                          v
        |                  data/interim/*.mat
        |                          |
        +-----> DVC (params tracking) <-- tracks hashes of all inputs/outputs
        |                          |
        |                  dvc repro triggers:
        |                          |
        +-----> Python wrapper script (thin)
        |           |
        |           +---> Hamilton driver.Builder()
        |           |         .with_config(from JSON)
        |           |         .with_adapters(WandbTracker)
        |           |         .with_modules(feat, model, val)
        |           |         .build()
        |           |
        |           +---> Hamilton micro-DAG executes:
        |           |         load -> validate (Pandera) -> features
        |           |         -> select -> train -> evaluate -> metrics
        |           |
        |           +---> Writes results/metrics.json (for DVC)
        |
        +-----> W&B (receives full config + all metrics via adapter)
                    |
                    v
              W&B dashboard: compare 180 experiments
```

## Rule Enforcement Summary

| Rule | Enforced By | Mechanism | Failure Mode if Skipped |
|------|------------|-----------|------------------------|
| Pressures in 40-200 mmHg | Hamilton `@check_output` | Runtime range check | Silent impossible values |
| Feature matrix has expected schema | Pandera via Hamilton | Schema validation | Shape mismatch crashes or wrong results |
| All expected subjects present | Custom Hamilton node | Set comparison | Wrong N in paper |
| Pipeline stages run in order | DVC `dvc.yaml` | Dependency DAG | Stale intermediate files |
| Changed params trigger re-run | DVC `params:` | Hash tracking | Results do not match config |
| Every experiment is traceable | W&B + config logging | Full config in every run | Cannot reproduce best run |
| Config is consistent across languages | Single JSON file | One source of truth | MATLAB and Python use different params |
| Code changes trigger re-run | DVC `deps:` | File hash tracking | Code changed but results are old |

---

## Sources

### Official Documentation (Verified Current)
- [Hamilton Data Quality writeup](https://github.com/apache/hamilton/blob/main/writeups/data_quality.md) -- `@check_output` and Pandera integration
- [Hamilton Builder docs](https://hamilton.dagworks.io/en/latest/concepts/builder/) -- `with_config`, `with_modules`, `with_adapters`
- [Hamilton config.when decorator](https://hamilton.dagworks.io/en/latest/reference/decorators/config_when/) -- conditional DAG construction
- [Hamilton Wrapping Driver](https://hamilton.dagworks.io/en/latest/how-tos/wrapping-driver/) -- wrapper pattern for external orchestration
- [Hamilton Lifecycle Hooks](https://hamilton.dagworks.io/en/latest/reference/lifecycle-hooks/) -- custom adapter API
- [Hamilton MLFlowTracker](https://hamilton.dagworks.io/en/latest/reference/lifecycle-hooks/MLFlowTracker/) -- reference adapter implementation
- [DVC Pipeline docs](https://dvc.org/doc/user-guide/pipelines/defining-pipelines) -- stage definition, deps, outs, params
- [DVC params](https://dvc.org/doc/command-reference/params) -- JSON/YAML/TOML parameter tracking
- [DVC Experiment Pipelines](https://dvc.org/doc/start/experiments/experiment-pipelines)
- [W&B Config docs](https://docs.wandb.ai/models/track/config) -- configuration logging
- [W&B Artifacts](https://docs.wandb.ai/tutorials/artifacts/) -- dataset and model versioning
- [Pandera docs](https://pandera.readthedocs.io/) -- DataFrame validation
- [scipy.io.loadmat](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html) -- .mat file loading

### Blog Posts and Guides
- [Hamilton + Pandera integration blog](https://blog.dagworks.io/p/data-quality-with-hamilton-and-pandera)
- [Tracking Pipelines with MLFlow and Hamilton](https://blog.dagworks.io/p/tracking-pipelines-with-mlflow-and) -- MLFlow adapter (W&B adapter modeled after this)
- [Customizing Hamilton's Execution with Lifecycle API](https://blog.dagworks.io/p/customizing-hamiltons-execution-with)
- [Martin Fowler - Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

### Internal Knowledge Base
- `/home/div/brain/knowledge/research/ml-codebase-trust-tooling-2026.md` -- ML trust tooling landscape
- `/home/div/brain/knowledge/research/biomedical-signal-processing-codebase-organization.md` -- codebase organization
- `/home/div/brain/docs/solutions/best-practices/research-pipeline-tooling-stack-ArterialAnalysis-20260212.md` -- tooling stack decisions
- `/home/div/brain/docs/solutions/workflow-issues/2026-02-12-arterial-analysis-data-provenance-rebuild.md` -- data provenance context
