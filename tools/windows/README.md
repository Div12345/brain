# Windows Automation Tools

Bidirectional control of Claude Desktop from WSL.

## Claude Desktop Controller

### Quick Start

```bash
# Basic usage (pyautogui-based)
claude status          # Is Claude Desktop running?
claude send "message"  # Send message
claude last            # Get last response

# DevTools mode (more precise - requires special launch)
claude info            # Get conversation ID, URL
claude messages        # Structured messages with roles
```

### Enabling DevTools Mode

For precise transcript access with conversation IDs, launch Claude Desktop with debug flags:

```powershell
# PowerShell
& "$env:LOCALAPPDATA\AnthropicClaude\claude.exe" --remote-debugging-port=9222 --remote-allow-origins=*
```

Or create a shortcut with these arguments.

### Commands

| Command | Method | Description |
|---------|--------|-------------|
| `status` | pyautogui | Check if running |
| `send <msg>` | pyautogui | Send a message |
| `read` | pyautogui | Full conversation (clipboard) |
| `last` | auto | Last assistant response |
| `watch [sec]` | pyautogui | Poll for changes |
| `info` | DevTools | Conversation ID, URL, title |
| `messages` | DevTools | Structured messages with roles |

### Example: Get Conversation ID

```bash
$ claude info
{
  "url": "https://claude.ai/chat/854e04d2-6918-45b9-bb7b-1722f9f69cd2",
  "conversation_id": "854e04d2-6918-45b9-bb7b-1722f9f69cd2",
  "title": "OpenClaw for personal data management - Claude",
  "is_new": false
}
```

### Files

| File | Purpose |
|------|---------|
| `claude` | Main CLI (bash wrapper) |
| `claude_desktop_api.py` | pyautogui-based automation |
| `claude_devtools_api.py` | Chrome DevTools Protocol API |

### Requirements

- WSL with access to Windows filesystem
- Windows Anaconda Python: `C:\ProgramData\Anaconda3\python.exe`
- Python packages: `pyautogui`, `pyperclip`, `websocket-client`, `requests`
- Claude Desktop running (not minimized to tray)
- For DevTools: Launch with `--remote-debugging-port=9222 --remote-allow-origins=*`

### How It Works

**pyautogui mode**: GUI automation - finds window, types, reads via clipboard

**DevTools mode**: Chrome DevTools Protocol via WebSocket:
- Connects to `ws://127.0.0.1:9222/devtools/page/<id>`
- Executes JavaScript in page context
- Reads DOM directly for message structure
- Gets conversation ID from URL
