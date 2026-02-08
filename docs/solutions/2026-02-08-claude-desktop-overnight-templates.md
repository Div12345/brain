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

**STATUS: Plan exists, execution not yet done.**

A CC Web session (session_0196fsjA8FFUVmr8Bre5kJMT) already created:
- `/home/div/AAA_detection_personal/docs/plans/2026-02-08-codebase-audit-plan.md` - full audit methodology
- `/home/div/AAA_detection_personal/docs/context/audit-context-from-obsidian.md` - project context

**Copy-paste this into Claude Desktop to CONTINUE the audit:**

```
CONTEXT: Continuing a codebase audit that was planned but not yet executed.

CODEBASE: /home/div/AAA_detection_personal (use desktop-commander MCP for file access)

FIRST: Read these files in order:
1. /home/div/AAA_detection_personal/docs/plans/2026-02-08-codebase-audit-plan.md — THE FULL PLAN (follow this exactly)
2. /home/div/AAA_detection_personal/docs/context/audit-context-from-obsidian.md — project context
3. /home/div/AAA_detection_personal/CLAUDE.md — conventions

YOUR TASK: Execute the audit plan. It tells you exactly what to do:
- Audit each module in src/
- Run tests
- Check determinism for all 3 targets (cSBP, cPP, cfPWV)
- Trace feature selection leakage
- Document random states

PRODUCE: Write the report to /home/div/AAA_detection_personal/docs/plans/2026-02-08-codebase-audit-report.md as specified in the plan.

Also save a copy to Obsidian: Projects/arterial analysis/sessions/2026-02-08-codebase-audit-report.md

COMPOUND PROTOCOL (when done):
- Update Dashboard/State.md with what you did
- Append learnings to Projects/brain system/compound-log.md
- Commit to git: git add -A && git commit -m "[audit]: codebase audit report"
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
