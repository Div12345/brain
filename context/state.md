# Current State - 2026-02-01

## Active Project
- **arterial_analysis**: Feature selection, stability selection, nested CV methodology
- Status: Methodology framework created (see [[Feature Selection Methodology Decision]])
- Tech: pycaret, Taiwan dataset (death outcomes, IMT, LVM-2D), cfpwv features

## Methodology Status: RESOLVED
Key decisions now documented:
- Fused LASSO for collinear waveform data
- Cluster Stability Selection (Faletto & Bien 2022)
- Post-Selection Inference for valid p-values
- EBIC stopping rules for high-P settings

## Stuck Tasks
- [ ] Credit card payment (!!!marked, recurring)
- [ ] Taiwan/Hao Min lit review - catalog all publications from group
- [ ] Check if mortality outcome = followup + death variables

## Tool Context
- Primary: Claude Desktop/Code
- Active: Pycaret, Zotero, Obsidian
- MCP: paper-search, obsidian, zotero available

## Next Actions
1. Complete Taiwan papers lit review via Zotero
2. Verify mortality/death outcome variable definitions
3. Implement cluster stability selection in pipeline
4. Test Fused LASSO on waveform features

---
*Updated: 2026-02-01 04:15*
