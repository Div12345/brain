---
created: 2026-01-31
tags:
  - tools
  - configs
  - documentation
updated: 2026-01-31T09:45
---

# Configuration Templates

> Prototype configs for scheduling, hooks, integrations.

## Contents

| File | Platform | Purpose |
|------|----------|---------|
| `overnight-brain.ps1` | Windows | PowerShell overnight runner |
| `nightly-brain.xml` | Windows | Task Scheduler import file |
| `overnight-brain.sh` | Linux/macOS/WSL | Bash overnight runner |
| `brain-overnight.service` | Linux | Systemd service unit |
| `brain-overnight.timer` | Linux | Systemd timer (2am daily) |

## Installation

### Windows (Task Scheduler)
```powershell
schtasks /create /tn "BrainNightlyRun" /xml "C:\brain\tools\configs\nightly-brain.xml"
```

### Linux (Systemd)
```bash
sudo cp brain-overnight.service /etc/systemd/system/brain-overnight@.service
sudo cp brain-overnight.timer /etc/systemd/system/brain-overnight@.timer
sudo systemctl enable brain-overnight@$USER.timer
sudo systemctl start brain-overnight@$USER.timer
```

### Linux (Cron)
```bash
# Edit with: crontab -e
0 2 * * * /home/user/brain/tools/configs/overnight-brain.sh >> /home/user/brain/logs/cron.log 2>&1
```

## Related

- [[agents/overnight]] - Agent definition
- [[tools/orchestration/DESIGN]] - System architecture
- [[.claude/settings.json]] - CC hooks config
