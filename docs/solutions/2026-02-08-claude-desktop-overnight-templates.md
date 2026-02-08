---
created: 2026-02-08
tags:
  - template
  - delegation
  - claude-desktop
  - overnight
---

# Claude Desktop Overnight Delegation Template

## Task 1: Codebase Audit (Arterial Analysis)

**Copy-paste this into Claude Desktop:**

```
CONTEXT: I'm delegating a codebase audit for my arterial analysis ML pipeline. The code has been modified by AI agents and I need to regain confidence before presenting results.

CODEBASE: /home/div/AAA_detection_personal (accessible via filesystem MCP or desktop-commander)

FIRST: Read Dashboard/State.md from Obsidian for current context, then read Projects/arterial analysis/sessions/2026-02-07-monday-update-brainstorm.md — specifically Task 1 (Codebase Audit).

YOUR TASK:
1. Read the entire pipeline end-to-end in /home/div/AAA_detection_personal
2. Explain what each level/module does and justify it
3. Document what tests exist (pytest), what they cover, what's missing
4. Check all random states are properly set for reproducibility
5. Check experiment configs are correct and consistent
6. Flag anything suspicious or non-deterministic
7. If possible, run experiments for all 3 targets (cSBP, cPP, cfPWV) and confirm deterministic results

PRODUCE: A structured report I can use as a guide when reviewing code files myself. Save to:
- Projects/arterial analysis/sessions/2026-02-08-codebase-audit-report.md (via Obsidian MCP)

COMPOUND PROTOCOL (when done):
- Update Dashboard/State.md with what you did
- Append learnings to Projects/brain system/compound-log.md
- If you discover reusable patterns, note them for docs/solutions/
```

---

## Task 4: CV Deaths Exploration (Quick/Independent)

**Copy-paste this into Claude Desktop:**

```
CONTEXT: Quick exploratory analysis of ~7 CV death subjects out of ~192 in my arterial analysis dataset.

CODEBASE: /home/div/AAA_detection_personal

FIRST: Read Dashboard/State.md from Obsidian, then read Projects/arterial analysis/sessions/2026-02-07-monday-update-brainstorm.md — Task 4.

YOUR TASK:
1. Find and load the arterial analysis dataset
2. Check Daily/2026-01-28.md in Obsidian — mentions outcome variables from Dr. Hahn
3. Subset the CV death subjects (~7)
4. Look at correlations/patterns with existing clinical and waveform variables
5. Create visualizations: waveforms of CV death cases vs non-CV-death subjects
6. Flag any obvious visual or statistical differences

This is exploratory — show me what's interesting, don't over-engineer.

PRODUCE: Save findings to Projects/arterial analysis/sessions/2026-02-08-cv-deaths-exploration.md

COMPOUND PROTOCOL (when done):
- Update Dashboard/State.md
- If interesting patterns found, note in compound-log.md
```

---

## How to Use

1. Open Claude Desktop
2. Create new conversation
3. Copy-paste the appropriate task prompt above
4. Let it run (session limit only, no weekly cap)
5. Check results in morning via Obsidian

## Checking Status from OpenCode/Gemini

```bash
cd /home/div/brain/tools/mcps/claude-desktop-mcp
source .venv/bin/activate
python -c "
from server import *
ws = get_main_process_ws()
ensure_debugger_attached(ws)
status = get_status(ws)
print('Status:', status)
messages = get_messages(ws)
if messages:
    print('Last message:', messages[-1].get('text', '')[:500])
ws.close()
"
```
