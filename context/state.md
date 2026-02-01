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
- [ ] Check if mortality outcome = followup + death variables

## Tool Context
- Primary: Claude Desktop/Code
- Active: Pycaret, Zotero, Obsidian
- MCP: paper-search, obsidian, zotero, memory available
- **NEW**: Windows Claude Desktop automation via `tools/windows/claude_send.sh`

## Recent Completions
- [x] Taiwan/Hao Min lit review - 20 papers catalogued (see [[Taiwan Group Papers Summary]])
- [x] Windows automation - can send messages to Claude Desktop from WSL

## Next Actions
1. Verify mortality/death outcome variable definitions
2. Implement cluster stability selection in pipeline
3. Test Fused LASSO on waveform features
4. Explore orchestration: Gemini CLI + Claude Desktop coordination

---
*Updated: 2026-02-01 05:30*
