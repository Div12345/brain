# Arterial Analysis — Quick Reference (Brain Pointer)

> **Single source of truth:** Read the full rules at the arterial repo CLAUDE.md
> **Path from WSL:** `/mnt/c/Users/din18/OneDrive - University of Pittsburgh/Work/Github/arterial_analysis/CLAUDE.md`
> **Path from Windows:** `C:\Users\din18\OneDrive - University of Pittsburgh\Work\Github\arterial_analysis\CLAUDE.md`

## Summary

- **Tooling:** DVC + Hamilton + W&B + Pandera + single JSON config + Git PRs
- **Languages:** MATLAB (signal processing) → Python/Hamilton (modeling)
- **Data:** 179 subjects, 545 features, DVC-versioned
- **Config:** `config/experiment.json` — single file read by all tools
- **Experiments:** edit config → `dvc repro` → W&B auto-logs → compare on dashboard

## When working on arterial analysis from brain

1. Read the arterial CLAUDE.md for current rules
2. Delegate code changes to agents working in the arterial repo
3. Compound learnings back to `brain/docs/solutions/`
4. Methodology decisions stay in Obsidian `[[Projects/arterial analysis/Command Center]]`

## Workflow diagrams

See Obsidian: `[[Projects/arterial analysis/Workflow]]`

## Key docs in brain

| Doc | What it captures |
|-----|-----------------|
| `docs/solutions/.../data-provenance-rebuild.md` | Data provenance crisis, md5 verification, what's lost |
| `docs/solutions/best-practices/research-pipeline-tooling-stack.md` | Tooling evaluation and selection |
| `knowledge/research/research-pipeline-integration-architecture.md` | 1234-line DVC+Hamilton+W&B integration patterns |
| `knowledge/research/biomedical-signal-processing-codebase-organization.md` | 620-line best practices guide |
