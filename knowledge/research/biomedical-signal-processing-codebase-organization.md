# Best Practices: Organizing a Biomedical Signal Processing Research Codebase

**Date:** 2026-02-12
**Context:** Mixed MATLAB + Python pipeline for arterial waveform analysis (PhD-level, single researcher)
**Pipeline:** Raw recordings -> Ensemble Averaging -> Calibration -> Feature Extraction -> ML Modeling

---

## 1. Directory Structure and Function Decomposition

### Recommended Project Layout

```
arterial_analysis/
├── README.md                    # Project overview, setup instructions, pipeline diagram
├── config/
│   ├── default_config.json      # Master config (shared by MATLAB and Python)
│   ├── subjects.json            # Per-subject metadata and inclusion criteria
│   └── experiments/             # Named experiment configs (override defaults)
│       ├── exp_2026_full.json
│       └── exp_2026_subset.json
│
├── data/
│   ├── raw/                     # NEVER modify. Original device recordings (.mat)
│   │   ├── subject_001/
│   │   │   ├── recording_2025-03-15.mat
│   │   │   └── recording_metadata.json
│   │   └── subject_002/
│   ├── curated/                 # Manual curation indices, QC annotations
│   │   ├── beat_indices/        # .gin files or .mat with selected beat indices
│   │   └── exclusion_log.csv    # Why beats/subjects were excluded
│   ├── interim/                 # Machine-generated intermediate outputs
│   │   ├── 01_ensemble_averaged/
│   │   ├── 02_calibrated/
│   │   ├── 03_features/
│   │   └── processing_log.csv   # What was run, when, with which config
│   ├── processed/               # Final analysis-ready datasets
│   │   ├── feature_matrix.csv   # For ML consumption (Python)
│   │   └── feature_matrix.mat   # Same data, MATLAB format
│   └── external/                # Third-party data (outcomes .xlsx, reference values)
│
├── matlab/
│   ├── startup.m                # Auto-runs on MATLAB launch: sets paths
│   ├── run_pipeline.m           # Main entry point script (calls functions in order)
│   ├── +sigproc/                # Signal processing package (namespace)
│   │   ├── load_recording.m
│   │   ├── preprocess.m
│   │   ├── detect_beats.m
│   │   ├── ensemble_average.m
│   │   └── extract_features.m
│   ├── +calib/                  # Calibration package
│   │   ├── apply_calibration.m
│   │   └── calibration_models.m
│   ├── +util/                   # Shared utilities
│   │   ├── read_config.m        # JSON config reader
│   │   ├── save_interim.m       # Standardized saving with metadata
│   │   └── validate_input.m
│   └── +viz/                    # Visualization functions
│       ├── plot_waveform.m
│       ├── plot_ensemble.m
│       └── plot_qa.m
│
├── python/
│   ├── pyproject.toml           # Python project config (or requirements.txt)
│   ├── src/
│   │   ├── load_features.py     # Load feature matrix from interim/
│   │   ├── modeling/
│   │   │   ├── train.py
│   │   │   ├── evaluate.py
│   │   │   └── feature_selection.py
│   │   └── utils/
│   │       ├── config.py        # Reads same JSON config as MATLAB
│   │       └── io.py
│   └── notebooks/
│       ├── 01_eda.ipynb         # Exploratory data analysis
│       ├── 02_model_comparison.ipynb
│       └── exploratory/        # Scratch notebooks (gitignored or not)
│
├── scripts/                     # Numbered top-level orchestration scripts
│   ├── 01_preprocess.sh         # Calls matlab -batch "run_pipeline('preprocess')"
│   ├── 02_extract_features.sh   # Calls matlab -batch "run_pipeline('features')"
│   ├── 03_train_model.sh        # Calls python src/modeling/train.py
│   └── run_all.sh               # Full pipeline end-to-end
│
├── results/
│   ├── figures/
│   │   ├── exploratory/         # Working plots
│   │   └── publication/         # Final, print-ready figures
│   ├── tables/
│   └── models/                  # Saved model artifacts
│
├── tests/                       # Lightweight validation
│   ├── matlab/
│   │   └── test_ensemble_average.m
│   └── python/
│       └── test_load_features.py
│
├── docs/
│   ├── pipeline_diagram.png     # Visual overview of data flow
│   ├── data_dictionary.md       # What every column/variable means
│   └── decisions.md             # Why you chose method X over Y
│
├── dvc.yaml                     # Pipeline definition (add later)
├── dvc.lock                     # Auto-generated lock file
├── .gitignore
└── .dvc/
    └── config                   # DVC remote storage config
```

### Key Principles Behind This Structure

**Source: [Plotivy Research Data Organization Guide](https://plotivy.app/blog/research-data-organization-guide)**

1. **Never modify raw data.** The `data/raw/` directory is sacred. Treat it as read-only. All transformations produce new files in `data/interim/` or `data/processed/`.

2. **Numbered prefixes show execution order.** Both in `scripts/` (01_, 02_, 03_) and in `data/interim/` (01_ensemble_averaged/, 02_calibrated/). Anyone looking at the project can understand the pipeline flow without reading code.

3. **Separate code by language, not by function.** Put MATLAB code in `matlab/`, Python in `python/`. The glue between them is the `data/interim/` directory and the shared `config/` files. Do not try to make MATLAB call Python or vice versa within a single step -- let each step write files that the next step reads.

4. **Future-you is a stranger.** Write a `data_dictionary.md` and a `decisions.md`. In six months you will not remember why you chose a 4th-order Butterworth filter at 16 Hz cutoff.

---

## 2. MATLAB-Specific Best Practices

### Functions Over Scripts (Always)

**Source: [MathWorks - Scripts vs Functions](https://www.mathworks.com/help/matlab/matlab_prog/scripts-and-functions.html), [MathWorks - Function Types](https://www.mathworks.com/help/matlab/matlab_prog/types-of-functions.html)**

- **Use functions for everything except the top-level entry point.** Functions have their own workspace (variable scope isolation), preventing subtle bugs from leftover variables. Scripts share the base workspace, which causes silent overwrites.
- **One primary function per file.** The file name must match the function name. Helper functions can go in the same file as local functions, or in the package.
- **The only script in your project should be `run_pipeline.m`** (or similar), which calls functions in sequence. Even this can be a function that takes a config path argument.

### Use MATLAB Packages (Namespaces) Instead of Flat Folders

```matlab
% BAD: flat folder with addpath
addpath('signal_processing');
addpath('calibration');
addpath('utilities');
result = preprocess(data);  % Which preprocess? Name collisions possible.

% GOOD: package folders (start with +)
result = sigproc.preprocess(data);
cal = calib.apply_calibration(result);
```

**Why packages:**
- No `addpath` spaghetti
- No name collisions (you can have `sigproc.validate` and `calib.validate`)
- Clear provenance -- you always know where a function lives
- Works with MATLAB's built-in help system

### Path Management with startup.m

Create a `startup.m` file in the project root (or matlab/ folder):

```matlab
% startup.m -- Auto-configures MATLAB for this project
% Run MATLAB from the project root, or set MATLAB's startup folder

project_root = fileparts(mfilename('fullpath'));

% Add only what's needed (packages auto-resolve, but util may need explicit add)
addpath(fullfile(project_root, 'matlab'));

% Set data paths as project-level constants
setenv('ARTERIAL_DATA_ROOT', fullfile(project_root, 'data'));
setenv('ARTERIAL_CONFIG', fullfile(project_root, 'config', 'default_config.json'));

fprintf('Arterial analysis project loaded. Data root: %s\n', getenv('ARTERIAL_DATA_ROOT'));
```

**Source: [SSI - Concise Guide to Reproducible MATLAB Projects](https://www.software.ac.uk/blog/concise-guide-reproducible-matlab-projects)**

### Config Management: Use JSON (Not Hardcoded Parameters)

**Source: [MathWorks Community - Config File Strategies](https://www.mathworks.com/matlabcentral/answers/2176935-using-a-config-file-to-specify-model-set-up-json-or-env), [MathWorks Community - Strategies for Configuration Data](https://www.mathworks.com/matlabcentral/answers/59686-strategies-to-store-load-configuration-data)**

MATLAB natively reads JSON since R2016b. JSON is the best config format for a mixed MATLAB/Python project because both languages read it natively.

```json
{
  "preprocessing": {
    "filter_order": 4,
    "filter_type": "butterworth",
    "lowpass_cutoff_hz": 16,
    "highpass_cutoff_hz": 0.5
  },
  "ensemble_averaging": {
    "min_beats": 10,
    "alignment_method": "r_peak",
    "outlier_rejection_threshold_sd": 2.5
  },
  "feature_extraction": {
    "features_to_extract": ["systolic_peak", "dicrotic_notch", "area_under_curve", "pulse_width"],
    "normalize": true
  },
  "subjects": {
    "exclude": ["subject_003", "subject_017"],
    "exclude_reason": "poor signal quality"
  }
}
```

```matlab
% MATLAB: read config
config = jsondecode(fileread('config/default_config.json'));
fc = config.preprocessing.lowpass_cutoff_hz;  % 16
```

```python
# Python: read same config
import json
with open('config/default_config.json') as f:
    config = json.load(f)
fc = config['preprocessing']['lowpass_cutoff_hz']  # 16
```

**Why JSON over YAML:** MATLAB reads JSON natively (`jsondecode`). YAML requires third-party toolboxes or Python bridges. For a single researcher, native support wins.

**Why not .m config files:** Mixing code and configuration is an anti-pattern. You cannot version config changes cleanly, and you cannot share config between MATLAB and Python.

---

## 3. Mixed MATLAB/Python Workflow Patterns

### The Handoff Pattern (Recommended for PhD-Level Work)

The simplest and most robust approach: MATLAB and Python never call each other directly. They communicate through files.

```
MATLAB writes → data/interim/*.mat or *.csv → Python reads
Python writes → results/models/*.pkl, results/*.csv → (MATLAB can read .csv if needed)
```

**Why this is best for a single researcher:**
- No MATLAB Engine for Python setup/debugging
- No `py.` calls breaking when MATLAB or Python updates
- Each language does what it does best
- Any step can be re-run independently
- Easy to add DVC later (each step is already a clean command)

### Language Boundary Recommendations

| Pipeline Step | Recommended Language | Why |
|---|---|---|
| Raw signal loading | MATLAB | Native .mat support, familiar toolboxes |
| Preprocessing (filtering, baseline correction) | MATLAB | Signal Processing Toolbox is excellent |
| Beat detection & segmentation | MATLAB | Established algorithms, visual QC easier |
| Ensemble averaging | MATLAB | Matrix operations, natural fit |
| Manual curation / QC | MATLAB | GUI tools, interactive plotting |
| Calibration | MATLAB | Domain-specific, likely already written |
| Feature extraction | **Either** (but pick one and stick with it) | If MATLAB: keep signal processing chain clean. If Python: scipy works fine |
| Feature matrix assembly | Python | pandas DataFrames are better for tabular data |
| ML modeling | Python | scikit-learn, XGBoost, SHAP -- no contest |
| Results visualization | Python | matplotlib/seaborn for publication figures |

### File Format for the Handoff

The critical question: what format to use at the MATLAB-to-Python boundary?

| Format | Pros | Cons | Verdict |
|---|---|---|---|
| .mat (v7.3 / HDF5) | MATLAB native, preserves structure | Python needs `h5py` or `scipy.io`, version issues | Good for complex data |
| .mat (v7) | Simple, `scipy.io.loadmat` works | Size limit ~2GB, nested structs get messy | **Best default choice** |
| .csv | Universal, human-readable | No metadata, slow for large matrices | Best for final feature matrix |
| .parquet | Fast, typed, compressed | MATLAB cannot write natively | Good if Python-only downstream |
| HDF5 | Both languages support well | More setup | Good for very large datasets |

**Recommendation:** Use `.mat` (v7) for interim data between MATLAB steps. Export a `.csv` (or `.parquet`) feature matrix at the MATLAB/Python boundary. This is the simplest approach that works.

```matlab
% MATLAB: save feature matrix as CSV at the boundary
feature_table = array2table(feature_matrix, 'VariableNames', feature_names);
writetable(feature_table, 'data/processed/feature_matrix.csv');

% Also save as .mat for MATLAB re-use
save('data/processed/feature_matrix.mat', 'feature_matrix', 'feature_names', 'subject_ids', '-v7');
```

---

## 4. Intermediate Output Management

### The Core Decision: Save Everything or Save Selectively?

For a PhD arterial waveform pipeline, you have a specific tension: ensemble averaging selects/averages beats from many recorded beats. Do you save all detected beats, or only the selected/averaged ones?

**Answer: Save both, but in different tiers.**

#### Tier 1: Always Save (Small, Critical)
- Ensemble-averaged waveforms per subject (the "result" of signal processing)
- Feature matrices (the input to ML)
- Beat selection indices (which beats were included/excluded and why)
- Configuration used for each run

#### Tier 2: Save With Cleanup Policy (Large, Regenerable)
- All detected individual beats (before selection/averaging)
- Filtered/preprocessed continuous recordings
- Intermediate calibration outputs

#### Tier 3: Never Save (Always Regenerate)
- Temporary variables, debug outputs
- Plots that can be regenerated from saved data

### Practical Implementation

```matlab
function save_interim(data, stage_name, config, subject_id)
    % Standardized saving with metadata for reproducibility
    output_dir = fullfile(getenv('ARTERIAL_DATA_ROOT'), 'interim', stage_name);
    if ~exist(output_dir, 'dir'), mkdir(output_dir); end

    metadata = struct();
    metadata.created = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    metadata.matlab_version = version;
    metadata.config_hash = DataHash(config);  % or just save the config
    metadata.subject_id = subject_id;
    metadata.source_file = '';  % fill in caller

    output_file = fullfile(output_dir, sprintf('%s_%s.mat', subject_id, stage_name));
    save(output_file, 'data', 'metadata', 'config', '-v7');

    % Log this run
    log_file = fullfile(getenv('ARTERIAL_DATA_ROOT'), 'interim', 'processing_log.csv');
    log_entry = sprintf('%s,%s,%s,%s\n', metadata.created, subject_id, stage_name, output_file);
    fid = fopen(log_file, 'a'); fprintf(fid, log_entry); fclose(fid);
end
```

### Naming Convention for Interim Files

Follow the pattern: `{subject_id}_{stage}_{version}.mat`

```
data/interim/01_ensemble_averaged/
├── subject_001_ensemble_v01.mat
├── subject_002_ensemble_v01.mat
├── subject_001_ensemble_v02.mat    # Re-processed with updated config
└── ...
```

For the beat selection indices (curation data):

```
data/curated/beat_indices/
├── subject_001_beat_selection.mat   # Contains: included_idx, excluded_idx, exclusion_reasons
├── subject_002_beat_selection.mat
└── ...
```

### When to Version Processed Outputs

**Manual curation data (beat_indices, exclusion_log) = track in Git.** These are small files that represent human judgment. They are irreplaceable.

**Machine-generated interim data = track with DVC (when ready).** These can be regenerated from raw data + code + config, but regeneration is expensive (time). DVC lets you cache them.

**Raw data = track with DVC from day one.** Even before you set up pipelines, just do `dvc add data/raw/` and push to a remote. This is insurance.

---

## 5. Reproducibility Tooling: DVC for Mixed MATLAB/Python

### Why DVC (Not Snakemake) for This Project

**Source: [Hacker News Snakemake Discussion](https://news.ycombinator.com/item?id=36735616), [DVC Pipeline Docs](https://doc.dvc.org/user-guide/pipelines)**

| Criterion | DVC | Snakemake |
|---|---|---|
| Primary strength | Data versioning + pipeline | Pipeline orchestration |
| MATLAB integration | Call via `matlab -batch` in cmd | Call via `shell:` directive |
| Learning curve | Moderate (Git-like) | Moderate (Python-like) |
| Data versioning | Built-in (core feature) | Not built-in (need separate tool) |
| Single-researcher fit | Good -- Git workflow you know | Good -- Python you know |
| ML experiment tracking | Built-in (`dvc exp`) | Not built-in |

**Recommendation: DVC** -- because you specifically mentioned wanting DVC, and because data versioning is your bigger need. Snakemake is better for complex DAG orchestration (bioinformatics with hundreds of samples), but for a single-researcher signal processing pipeline, DVC's combined data versioning + pipeline is the better fit.

### DVC Setup for Mixed MATLAB/Python Pipeline

#### Step 1: Initialize (Do This Now, Even Before Pipelines)

```bash
cd arterial_analysis/
git init        # if not already
dvc init
dvc add data/raw/
git add data/raw/.gitignore data/raw.dvc .dvc/ .dvcignore
git commit -m "Initialize DVC, track raw data"

# Set up remote storage (local NAS, Google Drive, S3, etc.)
dvc remote add -d myremote /path/to/shared/storage
# or: dvc remote add -d gdrive gdrive://folder_id
dvc push
```

#### Step 2: Add Pipeline Stages (When Ready)

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: matlab -batch "run_pipeline('preprocess', 'config/default_config.json')"
    deps:
      - data/raw/
      - matlab/+sigproc/preprocess.m
      - matlab/+sigproc/detect_beats.m
      - config/default_config.json
    outs:
      - data/interim/01_ensemble_averaged/

  extract_features:
    cmd: matlab -batch "run_pipeline('features', 'config/default_config.json')"
    deps:
      - data/interim/01_ensemble_averaged/
      - matlab/+sigproc/extract_features.m
      - matlab/+calib/apply_calibration.m
      - config/default_config.json
    outs:
      - data/interim/02_calibrated/
      - data/processed/feature_matrix.csv

  train_model:
    cmd: python python/src/modeling/train.py --config config/default_config.json
    deps:
      - data/processed/feature_matrix.csv
      - data/external/outcomes.xlsx
      - python/src/modeling/train.py
      - config/default_config.json
    params:
      - config/default_config.json:
          - modeling.algorithm
          - modeling.cv_folds
          - modeling.random_seed
    outs:
      - results/models/best_model.pkl
    metrics:
      - results/metrics.json:
          cache: false
    plots:
      - results/figures/roc_curve.csv:
          x: fpr
          y: tpr
```

#### How `matlab -batch` Works in DVC

**Source: [MathWorks - Call MATLAB from Command Line](https://www.mathworks.com/matlabcentral/answers/102082-how-do-i-call-matlab-from-the-dos-prompt)**

```bash
# The modern way (R2019a+): -batch flag
# Runs without GUI, exits automatically, returns nonzero on error
matlab -batch "run_pipeline('preprocess', 'config/default_config.json')"

# Your run_pipeline.m function should:
# 1. Accept stage name and config path as arguments
# 2. Read the config
# 3. Execute the stage
# 4. Exit cleanly (no need for explicit exit with -batch)
```

```matlab
function run_pipeline(stage, config_path)
    % run_pipeline - Execute a named pipeline stage
    %   run_pipeline('preprocess', 'config/default_config.json')

    config = jsondecode(fileread(config_path));

    switch stage
        case 'preprocess'
            sigproc.run_preprocessing(config);
        case 'features'
            sigproc.run_feature_extraction(config);
        case 'all'
            sigproc.run_preprocessing(config);
            sigproc.run_feature_extraction(config);
        otherwise
            error('Unknown pipeline stage: %s', stage);
    end
end
```

#### Step 3: Reproduce and Track Experiments

```bash
# Run full pipeline
dvc repro

# Run only from a specific stage onward
dvc repro train_model

# Track an experiment (change a parameter, run, compare)
# Edit config/default_config.json (e.g., change filter cutoff)
dvc repro
dvc exp show   # Compare metrics across runs
```

---

## 6. Plotivy Principles Applied to This Pipeline

**Source: [Plotivy Research Data Organization Guide](https://plotivy.app/blog/research-data-organization-guide)**

The Plotivy guide is aimed at general research data organization. Here is how each principle maps to this specific arterial waveform pipeline:

### Principle 1: "Never Modify Raw Data"
**Application:** `data/raw/` is write-once. Device recordings go in, nothing comes out changed. Even if you discover a recording has an error, do not edit it -- add it to `data/curated/exclusion_log.csv` with a reason.

### Principle 2: "Date-First Naming"
**Application:** Useful for recordings (`recording_2025-03-15.mat`), but for processed outputs, `subject_id + stage` naming is more useful than dates. Use dates for log files and experiment configs.

### Principle 3: "No Spaces, Lowercase, Hyphens"
**Application:** Critical for MATLAB compatibility and command-line tools. Use `subject_001` not `Subject 001`. Use underscores for MATLAB compatibility (MATLAB variable names cannot contain hyphens).

**Adaptation for MATLAB:** Use underscores instead of hyphens. `subject_001_ensemble_averaged.mat` not `subject-001-ensemble-averaged.mat`, because MATLAB variable names derived from filenames will break with hyphens.

### Principle 4: "Numbered Scripts Show Order"
**Application:** Already applied in the directory structure above. `scripts/01_preprocess.sh`, `scripts/02_extract_features.sh`. Also applied to `data/interim/01_ensemble_averaged/`, `02_calibrated/`, `03_features/`.

### Principle 5: "Future-You Is a Stranger"
**Application:** Write `docs/data_dictionary.md` that defines every feature you extract. Write `docs/decisions.md` that records why you chose ensemble averaging over single-beat analysis, why you chose a specific calibration model, etc. Use the decision rationale template from your existing `knowledge/analysis/ml-pipeline-coverage.md`.

### Principle 6: "3-2-1 Backup Rule"
**Application:**
- Copy 1: Local workstation
- Copy 2: DVC remote (university NAS or cloud storage)
- Copy 3: GitHub (code + DVC metadata)

---

## 7. PhD-Level Pragmatic Advice

### What to Do Now (Week 1)

1. **Create the directory structure above.** It takes 15 minutes. Do not overthink it.
2. **Move raw data into `data/raw/`.** Organize by subject.
3. **Convert your main MATLAB scripts to functions.** Start with the biggest/most-reused ones.
4. **Create `config/default_config.json`** with your current hardcoded parameters.
5. **Write a one-page `README.md`** with a pipeline diagram (even ASCII art counts).
6. **`git init` and `dvc init` and `dvc add data/raw/`.** Do this before writing any more code.

### What to Do Next (Month 1)

7. **Organize MATLAB functions into packages** (`+sigproc/`, `+calib/`, `+util/`).
8. **Create `run_pipeline.m`** that orchestrates stages via config.
9. **Write `data_dictionary.md`** for your feature matrix columns.
10. **Save beat selection indices** as explicit data files, not embedded in processing code.

### What to Do Later (When Pipeline Is Stable)

11. **Define `dvc.yaml` stages** for automated pipeline reproduction.
12. **Set up DVC remote storage** for data backup.
13. **Add `docs/decisions.md`** entries for each method choice.
14. **Add lightweight tests** for critical functions (ensemble averaging edge cases, feature extraction on known signals).

### What NOT to Do

- **Do not build a GUI.** You are the only user. Command-line entry points are sufficient.
- **Do not use MATLAB Projects (.prj).** They add toolbox dependency and IDE coupling without proportional benefit for a single researcher.
- **Do not try to call Python from MATLAB** (or vice versa) within a pipeline step. File-based handoff is simpler and more robust.
- **Do not use Snakemake AND DVC.** Pick one pipeline orchestrator. DVC handles both data versioning and pipeline definition.
- **Do not version interim data in Git.** That is what DVC is for. Git should only track code, config, small curation files, and DVC metadata.
- **Do not create elaborate class hierarchies.** This is research code, not a software product. Functions in packages are sufficient.
- **Do not use MATLAB's `addpath` everywhere.** Use packages instead.

---

## 8. Quick Reference: File Types and Where They Go

| File Type | Example | Tracked By | Directory |
|---|---|---|---|
| Raw device recordings | `.mat` from device | DVC | `data/raw/` |
| Outcomes / clinical data | `.xlsx` | DVC | `data/external/` |
| Manual curation indices | `.gin`, `.mat` of beat indices | **Git** (small, irreplaceable) | `data/curated/` |
| Ensemble-averaged waveforms | `.mat` per subject | DVC | `data/interim/01_...` |
| Feature matrices | `.csv`, `.mat` | DVC | `data/processed/` |
| MATLAB functions | `.m` | Git | `matlab/+pkg/` |
| Python source | `.py` | Git | `python/src/` |
| Jupyter notebooks | `.ipynb` | Git (with nbstripout) | `python/notebooks/` |
| Config files | `.json` | Git | `config/` |
| Trained models | `.pkl`, `.mat` | DVC | `results/models/` |
| Figures (publication) | `.pdf`, `.png` | Git | `results/figures/publication/` |
| Figures (exploratory) | `.png` | `.gitignore` | `results/figures/exploratory/` |

---

## Sources

### Official Documentation
- [MathWorks - Scripts vs Functions](https://www.mathworks.com/help/matlab/matlab_prog/scripts-and-functions.html)
- [MathWorks - Types of Functions](https://www.mathworks.com/help/matlab/matlab_prog/types-of-functions.html)
- [MathWorks - Create Projects](https://www.mathworks.com/help/matlab/matlab_prog/create-projects.html)
- [MathWorks - Biomedical Signal Processing](https://www.mathworks.com/discovery/biomedical-signal-processing.html)
- [MathWorks - Config File Strategies](https://www.mathworks.com/matlabcentral/answers/2176935-using-a-config-file-to-specify-model-set-up-json-or-env)
- [MathWorks - MATLAB from Command Line](https://www.mathworks.com/matlabcentral/answers/102082-how-do-i-call-matlab-from-the-dos-prompt)
- [DVC - Defining Pipelines](https://doc.dvc.org/user-guide/pipelines/defining-pipelines)
- [DVC - Project Structure](https://dvc.org/doc/user-guide/project-structure)
- [DVC - Get Started Data Pipelines](https://doc.dvc.org/start/data-pipelines/data-pipelines)

### Research Best Practices
- [SSI - Concise Guide to Reproducible MATLAB Projects](https://www.software.ac.uk/blog/concise-guide-reproducible-matlab-projects)
- [Plotivy - Research Data Organization Guide](https://plotivy.app/blog/research-data-organization-guide)
- [Ten Simple Rules for Large-Scale Data Processing (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8830682/)
- [Data & Design Lab - Modular Approach to Reproducible Research](https://www.dndlab.org/2024/10/15/a-modular-approach-to-reproducible-research/)

### Domain-Specific Tools
- [BioSPPy - Python Toolbox for Physiological Signal Processing](https://www.sciencedirect.com/science/article/pii/S2352711024000839)
- [BioSig - Free/Open Source Library for Biomedical Signal Processing](https://pmc.ncbi.nlm.nih.gov/articles/PMC3061298/)
- [PPGFeat - MATLAB Toolbox for PPG Fiducial Points](https://pmc.ncbi.nlm.nih.gov/articles/PMC10292016/)
- [PulseLab - MATLAB Toolbox for BP from ECG/PPG](https://github.com/pulselabteam/pulselab)
- [Bio-SP Signal Processing Tool (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10980118/)
- [BRAVEHEART - Open Source ECG/VCG Analysis](https://www.sciencedirect.com/science/article/pii/S0169260723004649)

### Community Discussions
- [Snakemake Discussion (Hacker News)](https://news.ycombinator.com/item?id=36735616)
- [MathWorks - How to Organize MATLAB Files](https://www.mathworks.com/matlabcentral/answers/350269-how-should-i-organize-my-matlab-files)
- [MathWorks - How to Organize a Project](https://www.mathworks.com/matlabcentral/answers/587018-how-to-organize-a-project)
- [UBC MATLAB Guide - Writing Functions](https://ubcmatlabguide.github.io/html/writingFunctions.html)
