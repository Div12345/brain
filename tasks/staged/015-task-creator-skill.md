---
name: task-creator-skill
priority: 2
estimated_tokens: 10000
mode: autonomous
timeout: 15m
skill: analyze
model_hint: sonnet
tags: [infrastructure, skill]
depends_on: []
bead_id: brain-pmj
---

# Skill: Standardized Task Creator

## Goal
Create a skill that generates properly-specified tasks in both bd AND scheduler format.

## Environment Constraints
- **Execution env:** WSL2 Claude Code
- **Working dir:** ~/brain
- **References:** knowledge/skills/task-specification.md (existing template)

## What This Task Must Produce

### 1. Task Creator Skill Document
Create knowledge/skills/task-creator.md that defines:

**Input template (what user provides):**
- Goal (1-2 sentences)
- Environment hints (where it runs, what tools needed)
- Known blockers (if any)
- Dependencies (other bead IDs)

**Output (what skill produces):**
- bd create command with full spec
- tasks/pending/NNN-name.md file content
- Both linked via bead_id field

### 2. Task Spec Template
Create tasks/templates/task-template.md

### 3. BD Integration Pattern
Document how bd and scheduler should sync:
- bd is source of truth
- Scheduler task files reference bead_id
- When bead closes, scheduler task moves to completed

## Success Criteria
- [ ] Task creator skill document complete
- [ ] Template file created
- [ ] Integration pattern documented
- [ ] Test: Use skill to create one new task

## Overnight Agent Instructions
1. Read existing task-specification.md
2. Read good examples: 020-notebooklm-library-pipeline.md
3. Extract the pattern into reusable skill
4. Create template file
5. Document bd↔scheduler sync pattern
