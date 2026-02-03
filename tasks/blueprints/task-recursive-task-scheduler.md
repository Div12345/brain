---
name: recursive-task-scheduler
priority: high
project: brain
estimated_tokens: 60000
mode: autonomous
timeout: 30m
schedule: daily
tags: [tasks, meta, daily]
---

## Task
Analyze work patterns and create new scheduled tasks for the scheduler.

## Context
- Current tasks: tasks/pending/, tasks/completed/
- Research queue: knowledge/research/queue.md
- Experiment ideas: knowledge/experiments/ideas.md

## Acceptance Criteria
- [ ] Reviewed completed work
- [ ] Identified gaps or follow-ups
- [ ] Created 1-3 new task files
- [ ] Tasks are well-structured for autonomous execution

## Workflow
1. Review completed tasks (last 7 days)
2. Check for:
   - Follow-up work needed
   - Research topics discovered
   - Experiments to try
3. For each new task:
   - Create task file in tasks/pending/
   - Set appropriate priority, timeout, tokens
   - Write clear acceptance criteria
4. Update knowledge/research/queue.md if research tasks
5. Log new tasks to logs/task-creation/

## Note
All generated tasks go to pending/ for review. User approves before execution.

## Error Handling
- If no patterns found: Log "no new tasks needed" and exit successfully
- Avoid creating duplicate tasks (check existing pending/)
