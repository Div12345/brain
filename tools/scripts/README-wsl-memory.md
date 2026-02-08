# WSL Memory Management

## Problem
WSL memory balloons because:
1. MCP servers (node processes) don't terminate when terminals close
2. Linux doesn't release cached memory back to Windows automatically
3. Gemini/Claude subprocesses can orphan

## Solutions

### 1. Run cleanup script manually
```bash
~/brain/tools/scripts/wsl-cleanup.sh
```

### 2. Add to Windows .wslconfig (limits WSL memory)
Create/edit `%USERPROFILE%\.wslconfig`:
```ini
[wsl2]
memory=8GB
swap=4GB
processors=4
```
Then restart WSL: `wsl --shutdown`

### 3. Reclaim memory from Windows (no restart)
```powershell
# In PowerShell (admin)
wsl --shutdown
# Wait 8 seconds, then start WSL again
```

### 4. Auto-cleanup on terminal exit
Add to `~/.bash_logout`:
```bash
# Kill MCP servers started by this session
pkill -P $$ 2>/dev/null || true
```

### 5. Scheduled cleanup (cron)
```bash
# Add to crontab -e
0 * * * * /home/div/brain/tools/scripts/wsl-cleanup.sh >> /tmp/wsl-cleanup.log 2>&1
```
