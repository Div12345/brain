# Comprehensive Guide: Scheduling & Automation for AI Agents

**Research Date:** 2026-02-02
**Focus:** Claude Code scheduling, cron-based AI, event-driven triggers, overnight/batch processing, and task queues

---

## Executive Summary

This guide covers scheduling and automation patterns for AI agents, particularly Claude Code. Five main categories emerged:

1. **Claude Code Schedulers** - Tools specifically designed for scheduling Claude tasks
2. **Cron-Based Scheduling** - Traditional time-based scheduling adapted for AI
3. **Event-Driven Triggers** - Webhooks, git hooks, and reactive automation
4. **Task Queues** - Coordinating multiple AI agents with queuing systems
5. **Overnight/Autonomous Mode** - Long-running autonomous agent patterns

---

## 1. Claude Code Schedulers

### 1.1 claude-code-scheduler (jshchnz)

**GitHub:** [jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler)

#### Installation
```bash
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler
```

#### Requirements
- Claude Code v1.0.33+
- macOS, Linux, or Windows
- `claude` CLI in system PATH

#### Configuration

Tasks stored as JSON:
- **Project-level:** `.claude/schedules.json`
- **Global:** `~/.claude/schedules.json`

Key settings:

| Setting | Default | Purpose |
|---------|---------|---------|
| `enabled` | false | Activates scheduled task |
| `branchPrefix` | "claude-task/" | Git branch naming |
| `remoteName` | "origin" | Target git remote |
| `skipPermissions` | - | Autonomous execution mode |
| `timeout` | 300 | Max execution time (seconds) |

#### How It Works

Uses native OS schedulers:
- **macOS:** launchd
- **Linux:** crontab
- **Windows:** Task Scheduler

Executes via: `claude -p "your command"`

Optional autonomous mode: `--dangerously-skip-permissions`

#### Example Cron Patterns
```bash
0 9 * * 1-5    # Weekdays at 9:00 AM
0 10 * * 1     # Mondays at 10:00 AM
0 0 * * *      # Daily at midnight
```

#### Pros
- No Claude Code window required after scheduling
- Automatic logging to `~/.claude/logs/<task-id>.log`
- One-time tasks self-delete after completion
- Git worktree isolation prevents main branch interference

#### Cons
- Requires absolute paths for reliability
- Failed worktree pushes need manual cleanup at `~/.worktrees/`
- Must configure cron syntax (though natural language preferred)

---

### 1.2 claude-mcp-scheduler (tonybentley)

**GitHub:** [tonybentley/claude-mcp-scheduler](https://github.com/tonybentley/claude-mcp-scheduler)

#### Purpose
Demonstrates scheduling Claude AI with cron while integrating MCP servers for tool access. Bridges "interactive AI assistants and production automation."

#### Installation
```bash
git clone https://github.com/tonybentley/claude-mcp-scheduler.git
cd claude-mcp-scheduler
npm install
```

#### Configuration

1. Create `.env` file with Anthropic API key
2. Copy `config/config.example.json` to `config/config.json`
3. Configure schedules with:
   - Name
   - Cron expression
   - Enabled status
   - Prompt text
   - Output path (supports `{name}`, `{timestamp}`, `{date}`)

#### MCP Integration

Model Context Protocol enables Claude to interact with:
- Local filesystem
- Databases
- APIs
- Custom tools

Example: filesystem MCP server for file access

#### Example Schedule
```json
{
  "name": "file-check",
  "cron": "*/10 * * * *",
  "enabled": true,
  "prompt": "List contents of directory",
  "outputPath": "outputs/{name}-{timestamp}.txt"
}
```

#### Pros
- Runs unattended on servers
- Batch processing support
- CI/CD integration
- Reduces API costs through scheduling
- Full MCP tool control

#### Cons
- Requires server setup
- More complex than interactive Claude
- Not ideal for visual/exploratory tasks

---

### 1.3 claude-tasks (kylemclaren)

**GitHub:** [kylemclaren/claude-tasks](https://github.com/kylemclaren/claude-tasks)
**Tagline:** "Cron 🤝 Claude Code"

#### Quick Install
```bash
curl -fsSL https://raw.githubusercontent.com/kylemclaren/claude-tasks/main/install.sh | bash
```

Installs to `~/.local/bin/`

#### Requirements
- Go 1.24+
- Claude CLI authenticated
- SQLite

#### Cron Format

6-field expressions: `second minute hour day month weekday`

Examples:
```bash
0 * * * * *      # Every minute
0 0 9 * * *      # Daily at 9:00 AM
0 30 8 * * 1-5   # Weekdays at 8:30 AM
0 0 */2 * * *    # Every 2 hours
```

#### Webhook Integrations

**Discord:**
- Rich embeds with colored sidebar (green/red/yellow)
- Markdown formatting preserved
- Task status and duration

**Slack:**
- Block Kit formatting
- Converts markdown to mrkdwn
- Timestamps included

Both include completion status, execution duration, formatted output, and error details.

#### Usage Tracking

Real-time API consumption with visual progress bars:
- Press `s` to set usage threshold (default 80%)
- Tasks auto-pause when exceeding limit
- Protects API quota

#### TUI Controls
- `a` - Add new task
- `r` - Run task immediately
- Toggle enabled/disabled status
- Configure cron expressions, prompts, webhooks

#### Pros
- Second-level granularity in cron
- Built-in webhook notifications
- Usage monitoring/throttling
- Interactive TUI
- SQLite persistence

#### Cons
- Requires Go build environment
- More complex setup than plugin-based solutions

---

### 1.4 runCLAUDErun (macOS)

**Website:** [runclauderun.com](https://runclauderun.com/)

#### Platform
macOS-specific native app

#### Key Features
- **Native GUI:** "Clean interface that fits naturally into your workflow"
- **Hardware support:** Apple Silicon (M1/M2/M3) and Intel Macs
- **macOS:** 10.13+
- **Local execution:** "Everything runs on your Mac. Your data stays with you"

#### How It Differs from Cron
- Graphical alternative to command-line
- No cron syntax knowledge required
- User quote: "Way easier than dealing with cron jobs. I can actually understand what's running when."

#### Setup
1. Download DMG for your Mac architecture
2. Create tasks in app interface
3. No command-line or config files needed

#### Scheduling Options
- Once
- Daily
- Weekly
- Custom intervals

#### Pricing
**Completely free** - no signup required (optional email for updates)

#### Requirements
- Active Claude subscription
- Claude Code installed locally

#### Use Cases
- Code reviews
- Content generation
- Data analysis
- Report generation

#### Pros
- Zero learning curve (GUI)
- Native macOS experience
- Free
- No terminal required

#### Cons
- macOS only
- Less flexible than command-line solutions
- Limited to predefined scheduling patterns

---

## 2. Task Queues for AI Agents

### 2.1 agent-task-queue (Block)

**GitHub:** [block/agent-task-queue](https://github.com/block/agent-task-queue)
**Purpose:** "Prevents multiple agents from running expensive operations concurrently and thrashing your machine"

#### The Problem
Multiple AI agents triggering builds simultaneously causes:
- Resource contention (CPU, memory, disk I/O)
- Both builds fighting for resources
- 5+ minute builds stretching to 30+ minutes

#### The Solution

**FIFO queuing** to serialize expensive operations:
- Agent B automatically waits for Agent A to finish
- Eliminates resource contention
- Practical impact: 30+ minute concurrent load → ~3:45 total (with caching)

#### SQLite Integration

Queue state at `/tmp/agent-task-queue/queue.db`

Tracks:
- Task ID and queue name
- Status (waiting vs running)
- Process IDs (liveness verification)
- Timestamps (entry and transition)

**Zombie protection:** Detects dead parent processes, terminates orphans, clears stale locks

#### MCP Protocol

Runs as FastMCP server. Agents invoke `run_task` tool:

Parameters:
- `command` - Command to execute
- `working_directory` - Where to run
- `queue_name` - Which queue (enables parallel queues)
- `timeout` - Max execution time

**Key feature:** "Timeout only applies to execution time—tasks can wait indefinitely in the queue without timing out"

#### Installation
```bash
uvx agent-task-queue@latest
```

#### MCP Configuration
```json
{
  "mcpServers": {
    "agent-task-queue": {
      "command": "uvx",
      "args": ["agent-task-queue@latest"]
    }
  }
}
```

Compatible with: Claude Code, Cursor, Windsurf, Amp, other MCP clients

#### Example Use Cases

**Separate queues (parallel execution):**
```python
run_task("./gradlew build", queue_name="android", ...)
run_task("npm run build", queue_name="web", ...)
```

**Same queue (serialized):**
- Docker builds
- Test suites (prevent shared state corruption)
- Gradle, Bazel, Cargo builds
- pytest runs

#### Pros
- Prevents resource thrashing
- Automatic zombie cleanup
- Queue-based parallelism (separate queues can run concurrently)
- MCP standard integration
- Works with multiple AI coding assistants

#### Cons
- Requires MCP-compatible client
- Local only (single machine)
- SQLite may not scale to high-throughput scenarios

---

### 2.2 huey (Python Task Queue)

**GitHub:** [coleifer/huey](https://github.com/coleifer/huey)
**Tagline:** "a little task queue for python"

#### Storage Backends

| Backend | Use Case | Notes |
|---------|----------|-------|
| **Redis** | Recommended | "Fantastic fit for lightweight task queueing" |
| **SQLite** | Built-in | Local persistence |
| **In-memory** | Testing | No persistence |

Redis advantages: "Self-contained, versatile, multi-purpose solution for caching, event publishing, analytics, rate-limiting, and more"

#### Python Integration

**Task definition with retries:**
```python
@huey.task(retries=2, retry_delay=60)
def flaky_task(url):
    return this_might_fail(url)
```

**Periodic scheduling:**
```python
@huey.periodic_task(crontab(minute='0', hour='3'))
def nightly_backup():
    sync_all_data()
```

#### Key Features for AI Agents

- **Execution models:** Multi-process, multi-thread, greenlet-based
- **Scheduling:** Delayed execution, cron-like recurrence, immediate queueing
- **Resilience:** Automatic retry with configurable delays
- **Result handling:** Task results stored and retrievable
- **Advanced patterns:** Pipelines, chains, prioritization, locking

#### Documentation
Official docs: **huey.readthedocs.io**

#### Pros
- Flexible storage options
- Rich feature set
- Well-documented
- Python ecosystem integration
- Cron-like scheduling built-in

#### Cons
- Python-specific
- Requires external storage setup (Redis/SQLite)
- More complex than file-based queues

---

## 3. Event-Driven Triggers

### 3.1 Webhooks for AI Agents

**Architecture:** Event-Driven Architecture (EDA) decouples services through event communication

#### How Webhooks Work

**Definition:** "HTTP request that one system sends to another when an event happens"

For AI agents:
- **Incoming webhook:** "Eyes and ears" - tells agent something happened
- **Outgoing webhook:** How agent tells the world what it did

#### Example: DevOps Automation

```
Git push to main
  ↓
Webhook triggers
  ↓
AI agent reviews code
  ↓
Posts findings to Slack (webhook)
```

#### Security: HMAC Verification

Standard method: "Sender signs request with secret key, you verify with same key"

Implementation:
```python
if signature_matches(request, secret_key):
    process_request()
else:
    reject()  # "No exceptions"
```

#### Production Requirements

1. **Security:** Signature validation (HMAC)
2. **Reliability:** Retries, dead-letter queues, idempotency
3. **State management:** Session IDs for multi-step tasks
4. **Observability:** Full logging for debugging autonomous systems

#### Use Cases

**Customer Support:**
- Zendesk ticket → webhook → AI drafts reply

**E-commerce:**
- `payment.succeeded` (Stripe) → update inventory → call shipping API

**DevOps:**
- Git push → code review → post to Slack

#### Benefits
- Systems push events as they happen
- AI responds instantly
- No polling required
- Scalable architecture

#### Cons
- Requires webhook infrastructure
- Security implementation critical
- Debugging can be complex

**Source:** [Hooklistener - Event-Driven AI & Webhooks](https://www.hooklistener.com/guides/event-driven-ai-webhooks)

---

### 3.2 Git Hooks with Claude Code

**Feature Request:** [GitHub Issue #4834](https://github.com/anthropics/claude-code/issues/4834)

#### What Are Claude Code Hooks?

"Shell commands that you define to run automatically at certain points in the Claude Code workflow"

#### Hook Types for Git Workflows

**PreToolUse Hooks:**
- Run before operations (like pre-commit)
- Can validate, modify, or block operations
- Examples:
  - Run linter (ESLint, Prettier, Black)
  - Scan for secrets (API keys, passwords)
  - Block commit if issues found

**PostToolUse Hooks:**
- Run after operations complete (like post-commit)
- Ideal for automation, notifications
- Examples:
  - Auto-push to remote
  - Trigger CI/CD
  - Send notifications

#### Integration Example: GitButler

With hooks setup:
1. Claude tells GitButler when code is generated/edited
2. GitButler isolates changes into branch per session
3. Multiple Claude sessions → separate branches automatically
4. When done, GitButler commits with sophisticated message

Quote: "If you have three sessions of Claude Code running at the same time, each will be communicating with GitButler at each step and GitButler will be assigning each change to the correct branch automatically"

#### Pre-Commit Hook Example

Send staged diff to Claude for commit message suggestion:
```bash
# Hook sends diff to Claude
claude -p "Generate commit message for: $(git diff --staged)"

# Can pause for confirmation or auto-commit
```

#### Headless Mode for Automation

Non-interactive contexts (CI, pre-commit, build scripts):
```bash
claude -p "your prompt" --output-format stream-json
```

**Sources:**
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [GitButler Claude Code Hooks](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)
- [Developer's Guide to Claude Code Hooks](https://www.eesel.ai/blog/claude-code-hooks)

---

## 4. Overnight/Autonomous Mode

### 4.1 Ralph (gmickel-claude-marketplace)

**GitHub:** [gmickel/gmickel-claude-marketplace](https://github.com/gmickel/gmickel-claude-marketplace)
**Tagline:** "Ralph autonomous mode (overnight coding with fresh context)"

#### What is Ralph?

"Ship features while you sleep. Fresh context per iteration, multi-model review gates, auto-blocks stuck tasks."

Designed to "run overnight, walk away"

#### Key Differentiators

| Factor | Standard Agents | Ralph |
|--------|-----------------|-------|
| **Context** | Accumulates (drift) | Fresh each iteration |
| **Quality gates** | Self-review only | Cross-model review |
| **Failure handling** | Infinite retry loops | Auto-block after N failures |
| **Verification** | Tests only | Tests + receipts + reviews |

#### Fresh Context Mechanism

Unlike typical agents where context accumulates causing drift, Ralph starts each iteration with a clean slate. Prevents degradation in long-running processes.

#### Failure Handling

"Auto-block stuck tasks — fails after N attempts, moves on"

Prevents infinite loops where agents repeatedly attempt same failing task. Marks as blocked and proceeds to other work.

#### Setup
```bash
/flow-next:ralph-init              # Initialize
scripts/ralph/ralph.sh             # Execute
```

#### Monitoring

Terminal UI: `bun add -g @gmickel/flow-next-tui`

Real-time observation of autonomous operations

#### Pros
- True overnight autonomous operation
- Fresh context prevents drift
- Multi-model review gates (quality)
- Auto-blocks stuck tasks (no infinite loops)
- Receipt-based verification

#### Cons
- Requires setup/scaffolding
- More complex than simple scheduling
- Needs monitoring infrastructure

---

### 4.2 Automated Claude Workers Architecture

**Source:** [Building Automated Claude Code Workers](https://www.blle.co/blog/automated-claude-code-workers)

#### Core Components

1. **Task Queue (MCP Server)** - Manages pending/active/completed tasks
2. **Cron Scheduler** - Triggers worker execution at intervals
3. **Claude Worker Script** - Fetches and executes tasks
4. **Feedback Loop** - Updates status and stores results

#### Shell Script Best Practices

Use "strict mode": `set -euo pipefail`

- `-e` - Exit on command failure
- `-u` - Treat undefined variables as errors
- `-o pipefail` - Detect pipeline failures

Quote: "This prevents silent failures that could leave your automation in an inconsistent state"

#### Structured Prompt Architecture

Don't embed logic in shell scripts. Route through dedicated prompts:
- `/process-next-task` - Main workflow orchestrator
- Task-specific prompts (code review, data analysis, file processing)

#### Cron Configuration

```bash
*/10 * * * * /bin/zsh -l -c '/path/to/claude-worker.sh'
```

`-l` flag preserves full environment (Node.js, PATH settings)

#### MCP Server Requirements

Essential functions:
- `get_next_task()` - Retrieve pending work
- `update_task_status(id, status)` - Track progress
- `complete_task(id, results)` - Store outcomes
- `fail_task(id, error)` - Log failures

#### Ideal Use Cases

- Continuous code review
- Data processing pipelines
- Content generation
- System monitoring
- Research tasks

#### Pros
- Full automation
- Structured, maintainable
- Error handling built-in
- Scales to multiple workers

#### Cons
- Requires MCP server development
- More setup than simple cron
- Needs monitoring/alerting

---

## 5. Official GitHub Actions Integration

**Source:** [Claude Code GitHub Actions Docs](https://code.claude.com/docs/en/github-actions)

### Overview

"Claude Code GitHub Actions brings AI-powered automation to your GitHub workflow. With a simple `@claude` mention in any PR or issue, Claude can analyze code, create PRs, implement features, and fix bugs."

### Quick Setup

```bash
# In Claude Code terminal
/install-github-app
```

Guides you through:
- GitHub App installation
- Secret configuration

**Requirements:**
- Repository admin access
- Direct Claude API users (not AWS Bedrock/Google Vertex via this method)

### Manual Setup

1. Install Claude GitHub app: [github.com/apps/claude](https://github.com/apps/claude)
2. Add `ANTHROPIC_API_KEY` to repository secrets
3. Copy workflow file from [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) to `.github/workflows/`

### Permissions Required

- **Contents:** Read & write (modify files)
- **Issues:** Read & write (respond to issues)
- **Pull requests:** Read & write (create PRs, push changes)

### Basic Workflow

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Scheduled Automation

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"  # 9 AM daily
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate summary of yesterday's commits and open issues"
          claude_args: "--model claude-opus-4-5-20251101"
```

### Skills Integration

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/review"
          claude_args: "--max-turns 5"
```

### Configuration Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `prompt` | Instructions or skill (e.g., `/review`) | No* |
| `claude_args` | CLI arguments for Claude Code | No |
| `anthropic_api_key` | Claude API key | Yes** |
| `github_token` | GitHub token for API access | No |
| `trigger_phrase` | Custom trigger (default: "@claude") | No |
| `use_bedrock` | Use AWS Bedrock | No |
| `use_vertex` | Use Google Vertex AI | No |

*Optional for issue/PR comments (responds to trigger phrase)
**Required for direct API, not for Bedrock/Vertex

### Common CLI Arguments

```yaml
claude_args: |
  --max-turns 10
  --model claude-sonnet-4-5-20250929
  --append-system-prompt "Follow coding standards"
```

Options:
- `--max-turns` - Max conversation turns (default: 10)
- `--model` - Model selection
- `--mcp-config` - Path to MCP configuration
- `--allowed-tools` - Comma-separated tool whitelist
- `--debug` - Enable debug output

### AWS Bedrock Integration

**Prerequisites:**
- Amazon Bedrock enabled with Claude models
- GitHub OIDC Identity Provider in AWS
- IAM role with Bedrock permissions

**Workflow example:**
```yaml
- name: Configure AWS Credentials (OIDC)
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
    aws-region: us-west-2

- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    use_bedrock: "true"
    claude_args: '--model us.anthropic.claude-sonnet-4-5-20250929-v1:0'
```

### Google Vertex AI Integration

**Prerequisites:**
- Vertex AI API enabled
- Workload Identity Federation configured
- Service account with Vertex AI permissions

**Workflow example:**
```yaml
- name: Authenticate to Google Cloud
  id: auth
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
    service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

- uses: anthropics/claude-code-action@v1
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    use_vertex: "true"
    claude_args: '--model claude-sonnet-4@20250514'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
    CLOUD_ML_REGION: us-east5
```

### Best Practices

**CLAUDE.md Configuration:**
Create `CLAUDE.md` in repository root with:
- Code style guidelines
- Review criteria
- Project-specific rules
- Preferred patterns

**Security:**
- Always use GitHub Secrets
- Never commit API keys
- Limit action permissions
- Review Claude's suggestions before merging

**Cost Optimization:**
- Use specific `@claude` commands to reduce API calls
- Configure `--max-turns` to prevent excessive iterations
- Set workflow-level timeouts
- Use GitHub concurrency controls

### CI Costs

**GitHub Actions:**
- Consumes GitHub Actions minutes
- See [GitHub billing docs](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)

**API Costs:**
- Token usage varies by task complexity and codebase size
- See [Claude pricing](https://claude.com/platform/api)

### Pros
- Official Anthropic support
- Integrates with GitHub workflow
- Scheduled automation via cron
- Multiple cloud provider support
- Skills integration

### Cons
- GitHub-specific (not portable)
- Requires GitHub Actions minutes
- API costs per execution
- Setup complexity for Bedrock/Vertex

---

## 6. OS-Specific Scheduling Patterns

### 6.1 Linux: systemd Timers vs Cron

**Sources:**
- [SystemD Timers vs. Cron Jobs](https://akashrajpurohit.com/blog/systemd-timers-vs-cron-jobs/)
- [Start Using systemd Timers](https://www.neteye-blog.com/2022/12/start-using-systemd-timers-instead-of-cron-anacron/)

#### systemd Timers Advantages

**Reliability:**
"systemd timers ensure that tasks will be executed when the system is running at a later time, even if the expected execution time was missed due to the system being off"

Cron doesn't catch up on missed executions.

**No Overlapping Runs:**
"Systemd timers guarantee that only one instance of a task is in execution at any given moment. If a task takes longer than expected, systemd ensures the subsequent scheduled instance waits patiently."

**Integrated Logging:**
- Central logging via journald
- Automatically captures stdout and stderr
- No need for script-based logging
- View logs: `journalctl -u service-name`

**Event-Based Triggering:**
systemd can trigger based on:
- Time (like cron)
- System status changes
- Boot completion
- Other systemd unit states

**Better Syntax:**
More human-readable than cron's "cryptic syntax"

**Resource Management:**
- Each job runs in specific environment
- Attached to cgroups for resource control
- Critical for managing AI agent resource usage

**Dependency Management:**
Jobs can depend on other systemd units (useful for complex AI workflows)

#### Cron Advantages

**Simplicity:**
- Simple to set up
- Well-known syntax
- Straightforward for fixed-time tasks
- `@daily`, `@weekly` shortcuts

**Wide Support:**
- Available on most Unix-like systems
- Scripts are portable

#### When to Use Each

**Use systemd timers:**
- System sometimes off (laptops)
- Need resource control
- Complex dependencies
- Want integrated logging
- Event-based triggers

**Use cron:**
- Always-on systems (production servers)
- Quick, simple scheduling
- Maximum portability

#### For AI Agent Scheduling on Linux

systemd timers recommended because:
1. Resource management (cgroups)
2. Dependency management (complex workflows)
3. Integrated debugging (journald)
4. Missed execution handling

---

### 6.2 macOS: launchd

**Sources:**
- [launchd Tutorial](https://www.launchd.info/)
- [MacOS launchd Examples](https://alvinalexander.com/mac-os-x/launchd-examples-launchd-plist-file-examples-mac/)

#### Overview

"As of MacOSX 10.4, cron became deprecated in favor of launchd"

**Biggest advantage:** "Does not assume that your computer is always on. If your Mac is asleep when a scheduled job was supposed to run, it will automatically run when your Mac is awake."

#### File Structure

`.plist` files are XML files with keys and values.

**Location:** `~/Library/LaunchAgents/` for user agents (auto-load at login)

#### Key Components

**Label:**
Unique name for the job within launchd. Written in reverse domain notation:
```xml
<key>Label</key>
<string>local.myscript</string>
```

**Program:**
Path to executable:
```xml
<key>ProgramArguments</key>
<array>
  <string>/usr/local/bin/claude</string>
  <string>-p</string>
  <string>Your prompt here</string>
</array>
```

**Scheduling:**

Option 1 - Interval:
```xml
<key>StartInterval</key>
<integer>3600</integer>  <!-- Every hour -->
```

Option 2 - Calendar:
```xml
<key>StartCalendarInterval</key>
<dict>
  <key>Hour</key>
  <integer>9</integer>
  <key>Minute</key>
  <integer>0</integer>
  <key>Weekday</key>
  <integer>1</integer>  <!-- Monday -->
</dict>
```

#### Example: Daily at 9 AM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>local.claude.daily</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/claude</string>
    <string>-p</string>
    <string>Review yesterday's code changes</string>
  </array>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/tmp/claude-daily.log</string>

  <key>StandardErrorPath</key>
  <string>/tmp/claude-daily-error.log</string>
</dict>
</plist>
```

#### Management Commands

**Load (start):**
```bash
launchctl load ~/Library/LaunchAgents/local.claude.daily.plist
```

**Unload (stop):**
```bash
launchctl unload ~/Library/LaunchAgents/local.claude.daily.plist
```

**List loaded jobs:**
```bash
launchctl list | grep local
```

#### Pros
- Handles sleep/wake cycles
- Native macOS integration
- Persistent across reboots
- Better than cron for laptops

#### Cons
- XML configuration (verbose)
- macOS-specific
- Debugging can be tricky

---

### 6.3 Windows: Task Scheduler with PowerShell

**Sources:**
- [Automating PowerShell Scripts With Task Scheduler](https://www.oreateai.com/blog/automating-powershell-scripts-with-task-scheduler-a-stepbystep-guide/c86b5a5f8a819db1d2b334fa97ccc5fe)
- [How To Automate PowerShell Scripts](https://www.itprotoday.com/powershell/how-to-automate-powershell-scripts-with-windows-task-scheduler)

#### Overview

Windows Task Scheduler is built-in tool for scheduling based on specific triggers or conditions.

#### Setup via GUI

1. Open Task Scheduler (search in Start menu)
2. Click "Create Basic Task"
3. Define trigger (time, event, etc.)
4. Action: Select `powershell.exe` from `system32\WindowsPowerShell\v1.0`
5. Add script path and arguments

#### Setup via PowerShell

```powershell
# Define trigger
$trigger = New-ScheduledTaskTrigger -Daily -At 9am

# Define action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
  -Argument "-File C:\scripts\claude-worker.ps1"

# Register task
Register-ScheduledTask -TaskName "ClaudeWorker" `
  -Trigger $trigger `
  -Action $action `
  -Description "Run Claude worker daily"
```

#### AI Agent Integration

"PowerShell's robust capabilities combined with Task Scheduler's scheduling prowess offer a scalable solution for managing everything from AI model rendering to content distribution."

2025 trend: "25% increase in demand for automated content pipelines year-over-year"

#### Example: Claude Worker Script

```powershell
# C:\scripts\claude-worker.ps1

# Error handling
$ErrorActionPreference = "Stop"

# Log file
$logFile = "C:\logs\claude-$(Get-Date -Format 'yyyyMMdd').log"

try {
    # Call Claude CLI
    & "C:\Program Files\Claude\claude.exe" -p "Process pending tasks" `
        | Out-File -FilePath $logFile -Append

    Write-Output "Success at $(Get-Date)" | Out-File -FilePath $logFile -Append
}
catch {
    Write-Error "Failed: $_" | Out-File -FilePath $logFile -Append
}
```

#### Advanced Triggers

Task Scheduler supports:
- **Time-based:** Daily, weekly, monthly, specific times
- **Event-based:** System events, log entries
- **Condition-based:** Idle time, network connection
- **Startup/logon:** System startup, user logon

#### Benefits

- Improves consistency
- Saves time
- Reduces human error
- Useful for backups, updates, monitoring, cleanups

#### Pros
- Built into Windows
- GUI and PowerShell options
- Event-driven triggers
- No additional software needed

#### Cons
- Windows-specific
- PowerShell knowledge helpful
- Less elegant than Unix solutions

---

## 7. Coordination Patterns for Multi-Agent Systems

**Source:** [AI Agent Coordination: 8 Proven Patterns](https://tacnode.io/post/ai-agent-coordination)

### Primary Patterns

#### 7.1 Sequential/Pipeline Pattern

"Agents arranged like an assembly line, each passing output to the next"

Characteristics:
- Linear
- Deterministic
- Easy to debug

Example: Code generation → Review → Test → Deploy

#### 7.2 Concurrent Pattern

"Multiple agents work simultaneously on independent tasks"

Impact: "Cutting processing time by 60-80% for tasks with no dependencies between steps"

Example: Parallel data processing, multiple code reviews

#### 7.3 Coordinator/Hub Pattern

"One agent acts as decision maker, receiving requests and dispatching to specialized agents"

Coordinator:
- Maintains context
- Synthesizes results
- Routes to specialists

### Key Infrastructure Considerations

**Problem with message queues alone:**
"Over-reliance on message queues alone is problematic - queues don't provide freshness or shared context, leading to inconsistent agent views"

**Solution:**
"Shared context layer with low-latency reads and real-time ingestion of structured and unstructured data"

### Integration Technologies

AI agents require:
- **REST/GraphQL APIs** - System interaction
- **Message queues** - Kafka, RabbitMQ for events
- **Vector databases** - Pinecone, Weaviate for semantic search
- **Enterprise data platforms** - Context access
- **Workflow orchestration** - Temporal, Airflow

### 2026 Trend

"Clear trend is move away from single, general-purpose agents toward multiple specialized agents that work together, with each agent handling defined responsibility while orchestration layer coordinates how work moves between them"

---

## 8. Decision Matrix: Choosing the Right Approach

### For Simple Time-Based Scheduling

| Platform | Recommended Tool | Complexity | Best For |
|----------|------------------|------------|----------|
| **macOS** | runCLAUDErun | Low | Non-technical users |
| **macOS** | launchd | Medium | Technical users, system integration |
| **Linux** | systemd timers | Medium | Production servers, resource control |
| **Linux** | cron | Low | Simple, always-on servers |
| **Windows** | Task Scheduler | Medium | Windows environments |
| **Cross-platform** | claude-code-scheduler | Low | Plugin-based, easy setup |

### For Advanced Features

| Need | Recommended Tool | Why |
|------|------------------|-----|
| **Webhook notifications** | claude-tasks | Discord/Slack integration |
| **Usage tracking** | claude-tasks | API quota monitoring |
| **MCP integration** | claude-mcp-scheduler | Tool access, custom MCP servers |
| **GitHub integration** | GitHub Actions | Official, scheduled workflows |
| **Task coordination** | agent-task-queue | Prevents resource conflicts |
| **Overnight autonomous** | Ralph | Fresh context, multi-model review |

### For Event-Driven Automation

| Trigger Type | Solution | Use Case |
|-------------|----------|----------|
| **Git operations** | Claude Code hooks | Pre/post-commit automation |
| **External events** | Webhooks | System integration, reactive |
| **System events** | systemd (Linux) | Boot, status changes |
| **File changes** | File watchers + cron | Continuous processing |

### For Production Multi-Agent Systems

| Pattern | Implementation | When to Use |
|---------|----------------|-------------|
| **Sequential** | Pipeline pattern | Linear workflows |
| **Concurrent** | Multiple queues | Independent parallel tasks |
| **Coordinated** | agent-task-queue | Resource-intensive operations |
| **Autonomous** | Ralph + cron | Overnight batch processing |

---

## 9. Implementation Roadmap

### Phase 1: Basic Scheduling (Week 1)

**Goal:** Get single scheduled task running

1. Choose platform-specific scheduler:
   - macOS → runCLAUDErun or claude-code-scheduler
   - Linux → cron or systemd timer
   - Windows → Task Scheduler

2. Create simple task:
   ```bash
   # Example: Daily code review at 9 AM
   claude -p "Review yesterday's commits"
   ```

3. Test manually first
4. Schedule and verify logs

### Phase 2: Task Queue (Week 2)

**Goal:** Coordinate multiple agents

1. Install agent-task-queue:
   ```bash
   uvx agent-task-queue@latest
   ```

2. Configure MCP in Claude Code
3. Test with two concurrent operations
4. Monitor queue behavior

### Phase 3: Event-Driven (Week 3)

**Goal:** Reactive automation

1. Choose trigger type:
   - Git hooks for commit automation
   - Webhooks for external events

2. Implement Claude Code hooks:
   ```bash
   # PreToolUse hook example
   echo "Validating changes..." | claude -p "Check for issues"
   ```

3. Test trigger conditions
4. Add error handling

### Phase 4: Overnight Autonomous (Week 4)

**Goal:** True autonomous operation

1. Set up Ralph or automated workers:
   ```bash
   /flow-next:ralph-init
   ```

2. Configure cron for worker execution:
   ```bash
   0 2 * * * /path/to/claude-worker.sh
   ```

3. Implement monitoring:
   - Logs analysis
   - Success/failure alerts
   - Usage tracking

4. Test overnight run
5. Iterate based on results

### Phase 5: Production Hardening (Ongoing)

**Goal:** Reliable, maintainable system

1. **Monitoring:**
   - Set up log aggregation
   - Create dashboards
   - Configure alerts

2. **Error Handling:**
   - Retry logic
   - Dead-letter queues
   - Failure notifications

3. **Security:**
   - Secrets management
   - API key rotation
   - Access controls

4. **Cost Management:**
   - Usage tracking
   - Budget alerts
   - Optimization

---

## 10. Best Practices Summary

### Security

1. **Never commit API keys** - Use environment variables or secrets managers
2. **Implement HMAC verification** for webhooks
3. **Use OIDC/Workload Identity** instead of static credentials
4. **Rotate secrets regularly**
5. **Principle of least privilege** for permissions

### Reliability

1. **Implement retries** with exponential backoff
2. **Use dead-letter queues** for failed tasks
3. **Monitor execution** with logging and alerts
4. **Handle system downtime** (use systemd timers on Linux, launchd on macOS)
5. **Prevent resource thrashing** with task queues

### Cost Optimization

1. **Set usage limits** and alerts
2. **Use appropriate models** (Haiku for simple tasks)
3. **Configure max turns** to prevent runaway costs
4. **Monitor API consumption** in real-time
5. **Schedule during off-peak** if applicable

### Maintainability

1. **Use structured prompts** instead of embedded logic
2. **Implement strict error handling** (`set -euo pipefail`)
3. **Log comprehensively** for debugging
4. **Version control** all configurations
5. **Document schedules and behaviors**

### Debugging

1. **Start simple** - Test manually before scheduling
2. **Check logs first** - Most issues show in logs
3. **Verify environment** - PATH, credentials, permissions
4. **Test in isolation** - One component at a time
5. **Use debug modes** - `--debug` flags when available

---

## 11. Common Pitfalls and Solutions

### Pitfall 1: Environment Variables Not Set

**Problem:** Cron runs with minimal environment

**Solution:**
```bash
# Source full environment
*/10 * * * * /bin/zsh -l -c '/path/to/script.sh'
```

Or explicitly set in script:
```bash
export PATH=/usr/local/bin:$PATH
export ANTHROPIC_API_KEY="..."
```

### Pitfall 2: Concurrent Execution Conflicts

**Problem:** Multiple agents fight for resources

**Solution:** Use agent-task-queue or implement locking:
```bash
# Flock-based locking
flock -n /tmp/claude.lock -c 'claude -p "..."' || exit 1
```

### Pitfall 3: Silent Failures

**Problem:** Task fails but no notification

**Solution:** Implement error handling:
```bash
set -euo pipefail  # Exit on error

# Send notification on failure
trap 'notify_failure' ERR

notify_failure() {
    echo "Task failed" | mail -s "Alert" admin@example.com
}
```

### Pitfall 4: API Rate Limits

**Problem:** Scheduled tasks exceed quota

**Solution:**
- Use usage tracking (claude-tasks)
- Implement backoff
- Spread schedules across time
- Monitor consumption

### Pitfall 5: Context Loss in Long Runs

**Problem:** Agent loses context over time

**Solution:** Use Ralph's fresh context pattern or implement context reset:
```bash
# Start new session for each iteration
for task in $(get_tasks); do
    claude -p "Process: $task"  # Fresh context each time
done
```

### Pitfall 6: Missed Executions

**Problem:** System was off during scheduled time

**Solution:**
- Linux: Use systemd timers (catch-up built-in)
- macOS: Use launchd (catch-up built-in)
- Avoid cron for systems that sleep

### Pitfall 7: No Visibility

**Problem:** Can't tell if automation is working

**Solution:** Implement comprehensive logging:
```bash
# Structured logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a /var/log/claude.log
}

log "Starting task: $TASK_NAME"
# ... execution ...
log "Completed task: $TASK_NAME"
```

---

## 12. Future Directions

### Emerging Trends

1. **Specialized agent coordination** - Moving from monolithic to multi-agent systems
2. **Event-driven architectures** - Less polling, more reactive
3. **Shared context layers** - Better coordination through real-time data
4. **AI-driven scheduling** - Agents optimize their own schedules
5. **Hybrid approaches** - Combining time-based and event-driven

### Technologies to Watch

- **Temporal** - Workflow orchestration for complex agent coordination
- **Kafka** - Event streaming for high-scale agent systems
- **Vector databases** - Semantic search for agent knowledge
- **MCP protocol expansion** - More tools and integrations
- **Claude Code SDK** - Programmatic integration possibilities

---

## Sources

### Claude Code Schedulers
- [jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler)
- [tonybentley/claude-mcp-scheduler](https://github.com/tonybentley/claude-mcp-scheduler)
- [kylemclaren/claude-tasks](https://github.com/kylemclaren/claude-tasks)
- [runCLAUDErun](https://runclauderun.com/)
- [Complete Guide to Claude Code Scheduled Execution](https://smartscope.blog/en/generative-ai/claude/claude-code-scheduled-automation-guide/)

### Task Queues
- [block/agent-task-queue](https://github.com/block/agent-task-queue)
- [coleifer/huey](https://github.com/coleifer/huey)

### Event-Driven & Webhooks
- [Hooklistener - Event-Driven AI & Webhooks](https://www.hooklistener.com/guides/event-driven-ai-webhooks)
- [Webhooks with AI Agents](https://medium.com/@seyhunak/we-are-unlocked-full-automation-power-incoming-and-outgoing-webhooks-with-crafted-ai-agents-ed8d09241d4a)
- [Event-Driven Agents in Action](https://www.docker.com/blog/beyond-the-chatbot-event-driven-agents-in-action/)

### Git Hooks
- [Feature Request: Git Hooks for Claude Code](https://github.com/anthropics/claude-code/issues/4834)
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [GitButler Claude Code Hooks](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)
- [Developer's Guide to Claude Code Hooks](https://www.eesel.ai/blog/claude-code-hooks)

### Overnight/Autonomous
- [gmickel/gmickel-claude-marketplace](https://github.com/gmickel/gmickel-claude-marketplace) (Ralph)
- [Building Automated Claude Code Workers](https://www.blle.co/blog/automated-claude-code-workers)

### GitHub Actions
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)

### OS-Specific Scheduling
- [SystemD Timers vs. Cron Jobs](https://akashrajpurohit.com/blog/systemd-timers-vs-cron-jobs/)
- [launchd Tutorial](https://www.launchd.info/)
- [MacOS launchd Examples](https://alvinalexander.com/mac-os-x/launchd-examples-launchd-plist-file-examples-mac/)
- [Automating PowerShell Scripts With Task Scheduler](https://www.oreateai.com/blog/automating-powershell-scripts-with-task-scheduler-a-stepbystep-guide/c86b5a5f8a819db1d2b334fa97ccc5fe)

### Coordination Patterns
- [AI Agent Coordination: 8 Proven Patterns](https://tacnode.io/post/ai-agent-coordination)
- [AI Agent Orchestration Patterns - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Scheduled AI Agents - MindStudio](https://university.mindstudio.ai/docs/deployment-of-ai-agents/scheduled-ai-agents)

---

## Appendix: Quick Reference Commands

### Installation Commands

```bash
# claude-code-scheduler
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler

# claude-tasks
curl -fsSL https://raw.githubusercontent.com/kylemclaren/claude-tasks/main/install.sh | bash

# agent-task-queue
uvx agent-task-queue@latest

# Ralph
/flow-next:ralph-init

# GitHub Actions
/install-github-app
```

### Cron Examples

```bash
# Every minute
* * * * * command

# Every hour
0 * * * * command

# Daily at 9 AM
0 9 * * * command

# Weekdays at 9 AM
0 9 * * 1-5 command

# Every 10 minutes
*/10 * * * * command

# Monthly on the 1st at midnight
0 0 1 * * command
```

### systemd Timer Example

```bash
# Create service file: /etc/systemd/system/claude-worker.service
[Unit]
Description=Claude Worker

[Service]
Type=oneshot
ExecStart=/usr/local/bin/claude -p "Process tasks"

# Create timer file: /etc/systemd/system/claude-worker.timer
[Unit]
Description=Claude Worker Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# Enable and start
sudo systemctl enable claude-worker.timer
sudo systemctl start claude-worker.timer
```

### launchd Example

```xml
<!-- ~/Library/LaunchAgents/local.claude.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>local.claude.worker</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/claude</string>
    <string>-p</string>
    <string>Process tasks</string>
  </array>

  <key>StartInterval</key>
  <integer>3600</integer>

  <key>StandardOutPath</key>
  <string>/tmp/claude.log</string>
</dict>
</plist>
```

```bash
# Load
launchctl load ~/Library/LaunchAgents/local.claude.plist
```

### PowerShell Task Scheduler

```powershell
# Create scheduled task
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
  -Argument "-File C:\scripts\claude-worker.ps1"
Register-ScheduledTask -TaskName "ClaudeWorker" `
  -Trigger $trigger -Action $action
```

---

**Document Version:** 1.0
**Last Updated:** 2026-02-02
**Maintained By:** Researcher Agent
