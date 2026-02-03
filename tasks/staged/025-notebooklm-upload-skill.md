---
name: notebooklm-upload-skill
priority: 3
estimated_tokens: 12000
mode: autonomous
timeout: 20m
skill: analyze
model_hint: sonnet
tags: [notebooklm, skill, tools]
depends_on: [notebooklm-library-pipeline, notebooklm-agent-tools]
bead_id: brain-djh
---

# NotebookLM Token-Efficient Upload Skill

## Goal
Build a tool/script that facilitates identifying and uploading documents to NotebookLM without manual work.

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **Depends on:** brain-qms (source patterns), brain-jtj (registry system)
- **Working dir:** ~/brain

## What This Task Must Produce

### 1. Upload Facilitator Script
Create tools/scripts/nlm-upload.py:
```
nlm-upload --notebook <n> --url <url>
nlm-upload --notebook <n> --file <path>
nlm-upload --notebook <n> --text <file.md>
nlm-upload --notebook <n> --zotero <collection>
```

### 2. Batch Upload Support
- Accept list of URLs from file
- Accept directory of PDFs
- Progress reporting
- Error handling with retry

### 3. Integration with Registry
- Auto-update notebooks.yaml after upload
- Increment source_count
- Update last_verified

## Success Criteria
- [ ] Script created and executable
- [ ] Single upload works (url, file, text)
- [ ] Batch upload works
- [ ] Registry auto-updates

## Overnight Agent Instructions
1. Read brain-qms output (source patterns from knowledge/tools/notebooklm-source-patterns.md)
2. Read brain-jtj output (registry at ~/.config/notebooklm/notebooks.yaml)
3. Build script with argparse
4. Test each upload mode
5. Add registry update logic
