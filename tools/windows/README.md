# Windows Automation Tools

Bidirectional control of Windows applications from WSL.

## Claude Desktop Controller

Full API for controlling Claude Desktop from WSL - send messages AND read responses.

### Quick Start

```bash
# Add to PATH (optional)
export PATH="$PATH:/home/div/brain/tools/windows"

# Check status
claude status

# Send a message
claude send "Hello, how are you?"

# Read the last response
claude last

# Read full conversation
claude read
```

### Commands

| Command | Description |
|---------|-------------|
| `claude status` | Check if Claude Desktop is running |
| `claude send <msg>` | Send a message |
| `claude read` | Read full conversation |
| `claude last` | Get last assistant response |
| `claude wait [timeout]` | Wait for response to complete |

### Example: Automated Q&A

```bash
claude send "What is the capital of France?"
sleep 5
claude last
# Output: Paris is the capital of France...
```

### How It Works

1. Uses **pyautogui** (Windows Anaconda Python) for GUI automation
2. Finds Claude window, activates it, types via `typewrite()`
3. Reads responses via `Ctrl+A`, `Ctrl+C`, clipboard paste
4. Parses conversation to extract last response

### Requirements

- WSL with access to Windows filesystem (`/mnt/c/`)
- Windows Anaconda Python at `C:\ProgramData\Anaconda3\python.exe`
- Python packages: `pyautogui`, `pyperclip` (auto-installed)
- Claude Desktop running (not minimized to tray)

### Files

| File | Purpose |
|------|---------|
| `claude` | Main CLI wrapper (bash) |
| `claude_desktop_api.py` | Python API (runs on Windows) |
| `claude_desktop_control.ps1` | PowerShell version (legacy) |
| `claude_send.sh` | Simple send-only script (legacy) |

### Limitations

- Requires Claude Desktop window visible (not minimized)
- Can't detect "thinking" vs "done" states precisely
- Clipboard is overwritten during read operations

### Future Ideas

- [ ] MCP server wrapping this API
- [ ] Orchestration between Claude Code + Claude Desktop
- [ ] Gemini CLI integration for multi-model workflows
