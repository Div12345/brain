---
module: Arterial Analysis
date: 2026-02-12
problem_type: workflow_issue
component: development_workflow
symptoms:
  - "Trust in arterial analysis codebase completely lost after agent modifications"
  - "Target extraction code partly lost — comparative calibration script gone"
  - "Same dataset exists under 3 names across 4 repos with no clear provenance"
  - "Calibration happens inside processData.m, not as separate pipeline step"
root_cause: incomplete_setup
resolution_type: workflow_improvement
severity: high
tags: [arterial-analysis, data-provenance, codebase-archaeology, matlab, pipeline-rebuild, calibration]
---

# Troubleshooting: Arterial Analysis Pipeline — Data Provenance and Trust Rebuild

## Problem

The arterial waveform analysis pipeline spread across 4 repos with agent-modified code, lost scripts, and no clear data provenance. Trust was completely gone — the user couldn't verify what code produced which outputs, and a key comparative calibration script was lost.

## Environment
- Module: Arterial Analysis (research pipeline)
- Repos: AAA_detection (Windows), AAA_detection_personal (WSL), AAA_detection_refactor-YAGnr (WSL), main_compare (WSL, no git)
- Languages: MATLAB (ensemble averaging, calibration) + Python (feature extraction, modeling)
- Date: 2026-02-12

## Symptoms
- 4 repos with overlapping but inconsistent data and code
- Same raw dataset under 3 names: "Taiwan data" (Windows), "Control_Data" (personal repo) — md5 verified identical
- Agent-written `ABCF_waveform_qual_check.m` replaced user's simple visualizer with a complex calibration pipeline
- `foot_calibrated_waveform_extractions.csv` and `min_calibrated_waveform_extractions.csv` exist but code that generated them is partly lost
- Confusing naming: `cmin_brachialmap` maps to `foot_calibrated`, `cmin_cuffmbp` maps to `min_calibrated`
- Ensemble averaging script in debug state: `for i=1:5` and `n=1` hardcoded

## What Didn't Work

**Attempted Solution 1:** Refactoring existing repos (AAA_detection_refactor-YAGnr)
- **Why it failed:** Added more confusion without establishing trust in the base data and code

**Attempted Solution 2:** Agent audit of existing code (audit/v2-2026-02-08 branch)
- **Why it failed:** Agents modified code without full understanding, replacing user scripts with complex alternatives

## Solution

**Fresh repo approach** — created `arterial_analysis` with only verified raw data and original user scripts.

**Repo created:** https://github.com/Div12345/arterial_analysis (private)
**Location:** `C:\Users\din18\OneDrive - University of Pittsburgh\Work\Github\arterial_analysis`

**Accepted raw data sources (verified):**
```
data/
  raw/
    Control_Data/              # 729 subject folders (raw .0, .MAT, .CAL, .zip) — 580MB
    ensemble_ankbrach_dot0/    # 370 .mat files — ensemble-averaged ankle+brachial
    ensemble_ankbrach_cf_dot0/ # 279 .mat files — ensemble-averaged carotid+femoral
    con_data.xlsx              # clinical outcomes (from Windows)
    new_outcomes.xlsx          # updated outcomes
  gin/
    gin_dot0.xlsx              # manual beat selection indices
    gin_dot0_const.xlsx        # "const" = constant amplitude ankle selection
    gin_dot0_mix.xlsx          # "mix" = mixed amplitude selection
matlab/
  ensembleAverage_CONTROLS_AnkBrach.m   # Step 0: raw .0 → ensemble dot0
  ABCF_checks_PWV.m                     # cfPWV + cSBP calculation
  recalibrate_waveforms.m               # min-mean recalibration
  functions/
    foots.m                   # intersecting tangent foot detection
    processData.m             # beat segmentation + calibration + selection (567 lines)
    saveWaveformsAndMeta.m    # save .mat + update master xlsx
    saveWaveformsAndMetaCF.m  # CF variant
    plotData.m                # visualization
    PulseAnalyse.m            # pulse analysis utilities
```

**Key data verification:**
```bash
# Taiwan data = Control_Data (same dataset, different name)
md5sum "Taiwan data/#1-C010203a/A010203B.MAT"   # 5069d3cbf075453108d323b8b2fda5c4
md5sum "Control_Data/#1-C010203a/A010203B.MAT"   # 5069d3cbf075453108d323b8b2fda5c4

# Personal repo .mat = Windows original
md5sum "personal/data/raw/.../dot0/1.mat"        # 4951ece3005ad65deb6d9a50b0b64e05
md5sum "windows/.../dot0/1.mat"                  # 4951ece3005ad65deb6d9a50b0b64e05
```

## Why This Works

1. **Single source of truth** — one repo with verified data, not 4 overlapping repos
2. **No processed outputs** — everything will be regenerated step by step with trusted code
3. **Original user scripts preserved** — agent-modified versions excluded
4. **Windows location** — MATLAB has native access, WSL accesses via `/mnt/c/` (slight perf overhead but fine for ~11MB repo)

## Key Findings

### dot0 .mat file contents (ensemble-averaged waveforms)
**AnkBrach:** `betterankle` (Nx3), `brachial` (Nx3), `metadata` (SubjectID, RMSE, accepted, etc.)
**CF:** `carotid` (Nx3), `femoral` (Nx3), `metadata`
- 3 columns = 3 best beats selected by median RMSE
- Values are **already calibrated** (~57-101 mmHg range) — calibration happens inside `processData.m:calibrateBeat()` line 562

### Calibration formula (min-mean, inside processData.m)
```matlab
calibratedBeat = ((dbp - mbp)/(min(signal) - mean(signal, 'omitnan'))*(signal - mean(signal, 'omitnan'))) + mbp;
```
This maps: min(signal) → DBP, mean(signal) → MBP. The "foot" alternative would map foots(signal) → DBP instead.

### Code structure of processData.m (567-line monolith)
- Beat segmentation using gin indices + R-wave locations
- Calibration per beat (min-mean) — `calibrateBeat()`
- Two beat selection algorithms: `median_algo_v2` (current), `median_algo_v1` (old)
- Also has `findSimilarBeats` (min-max similarity method)
- Wave feature extraction: `getWaveFeatures`, `getWaveFeatureLocs`
- Inter-beat RMSE calculation

### What's lost
- User's comparative calibration script (min vs foot, cuffMBP vs brachialMAP)
- This script generated the target CSVs the Python pipeline depends on
- Naming confusion: `cmin_brachialmap` → `foot_calibrated_waveform_extractions.csv`

### WSL ↔ Windows filesystem
- Cross-filesystem access (`/mnt/c/` from WSL or `\\wsl$\` from Windows) uses 9P protocol — slower
- Native access is fast on both sides
- For small repos (~11MB), the overhead is negligible
- Git can run from either side (WSL git or Windows git.exe) on the same repo

## Prevention

- **One repo per project** — don't let repos proliferate with overlapping data
- **Never let agents replace user scripts** — agents should create NEW files, not overwrite originals
- **Verify data identity early** — md5sum checks prevent duplicate data under different names
- **Separate calibration from beat selection** — these are independent pipeline steps that should be in separate functions/scripts
- **Track gin files** — manual beat selection indices are irreplaceable and must be version-controlled
- **Name things by what they ARE, not by method** — `cmin_brachialmap` is opaque; `foot_calibrated` is slightly better but still confusing

## Next Steps (for Thursday session)

1. Restructure repo: pipeline-based layout (not language-based)
2. Define and implement Step 1: clean calibration as separate step (both min and foot methods)
3. Rewrite the comparative calibration script that was lost
4. Possibly set up DVC once pipeline stages are defined and trusted

## Related Issues

No related issues documented yet.
