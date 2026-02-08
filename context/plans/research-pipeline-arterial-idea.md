---
status: idea
created: 2026-02-05
priority: high
tags: [research, arterial-analysis, pipeline, cardiac-output, feature-selection]
source: obsidian-dailies-jan28-feb05
---

# Research Pipeline: Arterial Analysis & Cardiac Output

## Context
This is the core research work. Appears in nearly every daily note from the past week. Multiple sub-threads:

## Sub-projects

### A. Feature Selection Methodology
- Stability selection keeps coming up as a framework
- Need empirical guidance on small dataset feature selection
- Nested CV validation — is current approach acceptable?
- FWER corrections, significance testing, confidence intervals
- Wainer and Cawley 2018 — most relevant paper for evaluation question
- Connected papers search turned up AutoML papers
- Want to read papers that worked on similar datasets (Nature, ML confs)
- Talk to Aaditya Ramdas (CMU) about stats correction methods for ML

### B. Taiwan Dataset Papers
- Build Zotero subcollection with all Taiwan group publications
- Check what Hao Min has published before
- Death/outcome variables — 35 deaths, 7 cardiovascular out of 192
- Follow-up date issues (14 people with negative follow-up duration)
- CVD variables: IMT, LVM-2D, death, follow date
- PP amplification stratified errors, augmentation index

### C. Cardiac Output Project
- Needs acceptable evaluation pipeline setup
- Blocked on: what evaluation is acceptable?

### D. Code Pipeline
- Pycaret DAG refactoring (almost done as of Jan 28)
- Wandb integration lost — needs restoration
- Feature importance extraction from all models
- Tests need running
- Validation steps: non-CV option for pycaret, feature permutation testing

## What Could Be Delegated to Overnight Agent
- Literature search tasks (paper-search MCP + Zotero)
- Code review of pycaret pipeline
- Connected papers exploration
- Dataset variable compilation and documentation
