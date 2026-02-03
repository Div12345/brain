# Quick Start Guide: AI Agent Scheduling

**Choose your path based on your needs:**

---

## Path 1: Simple Time-Based Scheduling (Easiest)

### For macOS Users (Non-Technical)
**Tool:** runCLAUDErun
**Time:** 5 minutes

```bash
1. Download from https://runclauderun.com/
2. Open app
3. Create task with GUI
4. Done!
```

**Best for:** Non-developers, simple schedules, GUI preference

---

### For Any Platform (Plugin)
**Tool:** claude-code-scheduler
**Time:** 10 minutes

```bash
# In Claude Code
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler

# Natural language: "Schedule code review every weekday at 9am"
# Claude handles the rest
```

**Best for:** Quick setup, natural language config, cross-platform

---

### For Linux/macOS (Command Line)
**Tool:** cron
**Time:** 5 minutes

```bash
# Edit crontab
crontab -e

# Add line (daily at 9 AM)
0 9 * * * /usr/local/bin/claude -p "Review yesterday's commits" >> /tmp/claude.log 2>&1

# Save and exit
```

**Best for:** Simple, traditional, always-on servers

---

## Path 2: Webhook Notifications + Scheduling

**Tool:** claude-tasks
**Time:** 15 minutes

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/kylemclaren/claude-tasks/main/install.sh | bash

# Run TUI
claude-tasks

# Press 'a' to add task
# Configure Discord/Slack webhook
# Set cron schedule with second precision
```

**Best for:** Teams wanting notifications, usage tracking, rich scheduling

---

## Path 3: GitHub-Integrated Automation

**Tool:** GitHub Actions
**Time:** 10 minutes

```bash
# In Claude Code
/install-github-app

# Or manually:
# 1. Install app: https://github.com/apps/claude
# 2. Add ANTHROPIC_API_KEY to repo secrets
# 3. Create .github/workflows/claude.yml
```

**Example workflow:**
```yaml
name: Daily Code Review
on:
  schedule:
    - cron: "0 9 * * 1-5"  # Weekdays at 9 AM
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review commits from last 24 hours"
```

**Best for:** GitHub users, CI/CD integration, team workflows

---

## Path 4: Multi-Agent Coordination

**Tool:** agent-task-queue
**Time:** 15 minutes

```bash
# Install
uvx agent-task-queue@latest

# Add to Claude Code MCP config (~/.claude/mcp.json)
{
  "mcpServers": {
    "agent-task-queue": {
      "command": "uvx",
      "args": ["agent-task-queue@latest"]
    }
  }
}

# Restart Claude Code
# Now multiple agents won't conflict on expensive operations
```

**Best for:** Multiple AI agents, preventing resource thrashing, build coordination

---

## Path 5: Overnight Autonomous Mode

**Tool:** Ralph (gmickel-claude-marketplace)
**Time:** 30 minutes

```bash
# Install plugin
/plugin marketplace add gmickel/gmickel-claude-marketplace

# Initialize Ralph
/flow-next:ralph-init

# Run overnight
scripts/ralph/ralph.sh

# Monitor (optional)
bun add -g @gmickel/flow-next-tui
```

**Best for:** Complex features, overnight development, autonomous execution

---

## Path 6: Event-Driven (Git Hooks)

**Tool:** Claude Code Hooks
**Time:** 20 minutes

```bash
# Create .claude/hooks/pre-commit.sh
#!/bin/bash
set -euo pipefail

# Run linter
eslint $(git diff --cached --name-only --diff-filter=ACM | grep '\.js$')

# Check for secrets
if git diff --cached | grep -i "api[_-]key\|password\|secret"; then
    echo "⚠️  Potential secret detected!"
    exit 1
fi

# Make executable
chmod +x .claude/hooks/pre-commit.sh

# Configure in .claude/config.json
{
  "hooks": {
    "PreToolUse:Bash": {
      "command": ".claude/hooks/pre-commit.sh"
    }
  }
}
```

**Best for:** Git workflow automation, validation, reactive triggers

---

## Decision Tree

```
START
  |
  ├─ Need simple scheduling?
  |    ├─ macOS + GUI → runCLAUDErun
  |    ├─ Any platform + easy → claude-code-scheduler
  |    └─ Command line → cron (Linux/macOS) or Task Scheduler (Windows)
  |
  ├─ Need team notifications?
  |    └─ claude-tasks (Discord/Slack webhooks)
  |
  ├─ Already using GitHub?
  |    └─ GitHub Actions
  |
  ├─ Multiple agents fighting for resources?
  |    └─ agent-task-queue
  |
  ├─ Need overnight autonomous work?
  |    └─ Ralph
  |
  └─ Need event-driven (git hooks, webhooks)?
       └─ Claude Code Hooks or webhook services
```

---

## Testing Your Setup

### Step 1: Manual Test
```bash
# Run command manually first
claude -p "Your task here"

# Verify it works before scheduling
```

### Step 2: Short Schedule Test
```bash
# Test with frequent schedule first
*/5 * * * * /path/to/command  # Every 5 minutes

# Once working, change to desired schedule
```

### Step 3: Check Logs
```bash
# Verify execution
tail -f /tmp/claude.log  # or your log location

# Look for errors
grep -i error /tmp/claude.log
```

### Step 4: Verify Output
```bash
# Check that task actually completed
# Look for expected files, commits, notifications, etc.
```

---

## Common First-Time Issues

### Issue 1: "Command not found"
**Solution:** Use absolute path to claude
```bash
# Find full path
which claude
# Use in schedule: /usr/local/bin/claude
```

### Issue 2: Environment variables not set
**Solution:** Source full environment
```bash
# In cron
*/10 * * * * /bin/bash -l -c '/path/to/script.sh'

# In script
export PATH=/usr/local/bin:$PATH
export ANTHROPIC_API_KEY="your-key"
```

### Issue 3: No output/logs
**Solution:** Add explicit logging
```bash
# Redirect output
command >> /tmp/claude.log 2>&1

# Or use logger
command 2>&1 | logger -t claude
```

### Issue 4: Task doesn't run when expected
**Solution:** Check scheduler is running
```bash
# Linux - check cron
sudo systemctl status cron

# macOS - check launchd
launchctl list | grep local

# Verify schedule syntax
# Use https://crontab.guru/ for cron expressions
```

---

## Next Steps

1. **Start simple** - Pick one path above and implement
2. **Test thoroughly** - Manual test → frequent schedule → desired schedule
3. **Add monitoring** - Logs, notifications, alerts
4. **Expand gradually** - Add more schedules as needed
5. **Read comprehensive guide** - For advanced patterns and troubleshooting

---

## Resource Links

- **Comprehensive Guide:** `comprehensive-guide.md` (in this directory)
- **Comparison Matrix:** `comparison-matrix.md` (in this directory)
- **Official Docs:** https://code.claude.com/docs/
- **GitHub Actions:** https://code.claude.com/docs/en/github-actions
- **Cron Syntax:** https://crontab.guru/

---

**Quick Support:**
- Environment issues → Check PATH and API keys
- Scheduling issues → Verify cron syntax and scheduler status
- Execution issues → Check logs first
- Coordination issues → Consider agent-task-queue

**Remember:** Start with the simplest solution that meets your needs. You can always upgrade to more sophisticated patterns later.
