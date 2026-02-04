---
name: task-name-here
priority: 2
estimated_tokens: 10000
mode: autonomous
timeout: 20m
skill: analyze
model_hint: sonnet
tags: []
depends_on: []
bead_id: brain-xxx
---

# Task Title

## Goal
[One sentence: What does "done" look like?]

## Environment Constraints
- **Execution env:** WSL2
- **Working dir:** ~/brain
- **MCP tools needed:** [list or "None"]
- **Depends on:** [bead IDs or "None"]

## What This Task Must Produce

### 1. [Deliverable Name]
[Description of what to create, with file path]

### 2. [Deliverable Name]
[Description of what to create, with file path]

## Known Blockers
[List foreseeable problems, or "None"]

## Success Criteria
- [ ] [Verifiable criterion with how to test]
- [ ] [Verifiable criterion with how to test]
- [ ] [Verifiable criterion with how to test]

## Fallback
[What to do if primary approach fails, or "Document issues for next iteration"]

## Overnight Agent Instructions
1. [First step]
2. [Second step]
3. [Third step]
4. [Verification step]

## Output
[List of files/artifacts this task produces]
- [path/to/output1]
- [path/to/output2]
