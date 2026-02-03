# Claude Desktop MCP

Control Claude Desktop from any agent via MCP tools.

## Requirements

Launch Claude Desktop with DevTools enabled:
```
claude.exe --remote-debugging-port=9222 --remote-allow-origins=*
```

## Tools

| Tool | Description |
|------|-------------|
| `claude_desktop_send` | Send message, optionally wait for response |
| `claude_desktop_read` | Read conversation messages |
| `claude_desktop_info` | Get conversation ID/URL/title |

## Setup

Add to your Claude Code MCP config (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "claude-desktop": {
      "command": "python",
      "args": ["/home/div/brain/tools/mcps/claude-desktop-mcp/server.py"]
    }
  }
}
```

## Usage Examples

**Send and wait for response:**
```
claude_desktop_send(message="What is 2+2?", wait_for_response=true)
```

**Fire and forget:**
```
claude_desktop_send(message="Start analyzing...", wait_for_response=false)
```

**Read recent messages:**
```
claude_desktop_read(last_n=5)
```

**Get conversation info:**
```
claude_desktop_info()
```
