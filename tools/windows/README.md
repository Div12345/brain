# Windows Automation Tools

Tools for controlling Windows applications from WSL.

## Claude Desktop Controller

Send messages to Claude Desktop on Windows from WSL.

### Usage

```bash
# Check if Claude Desktop is running
./claude_send.sh --status

# Focus Claude Desktop window
./claude_send.sh --focus

# Send a message
./claude_send.sh "Your message here"
```

### How It Works

1. Uses PowerShell Win32 API calls to find Claude Desktop window
2. Brings window to foreground with `SetForegroundWindow`
3. Uses `SendKeys` to type and send the message

### Requirements

- WSL with access to Windows PowerShell
- Claude Desktop running on Windows

### Limitations

- Requires Claude Desktop window to be accessible (not minimized to tray only)
- SendKeys can be disrupted if focus is lost
- No way to read Claude's response programmatically (yet)

### Future Improvements

- [ ] Read Claude responses via screen capture + OCR
- [ ] Queue messages for rate-limited sending
- [ ] Create MCP server for full integration
