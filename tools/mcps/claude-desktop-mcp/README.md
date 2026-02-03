# Claude Desktop MCP

Control Claude Desktop from any agent via MCP tools.

## Requirements

Launch Claude Desktop with DevTools enabled:
```
claude.exe --remote-debugging-port=9222 --remote-allow-origins=*
```

**Windows (from WSL):**
```powershell
powershell.exe -Command "Get-Process claude -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Process 'C:\Users\din18\AppData\Local\AnthropicClaude\claude.exe' -ArgumentList '--remote-debugging-port=9222','--remote-allow-origins=*'"
```

## Tools

| Tool | Description |
|------|-------------|
| `claude_desktop_send` | Send message, optionally wait for response |
| `claude_desktop_read` | Read conversation messages |
| `claude_desktop_info` | Get conversation ID/URL/title |
| `claude_desktop_list` | List all conversations from sidebar |
| `claude_desktop_navigate` | Navigate to conversation by ID |
| `claude_desktop_new` | Create new conversation |
| `claude_desktop_search` | Search conversations by title |

## Setup

Add to your Claude Code MCP config:

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

**List conversations:**
```
claude_desktop_list()
→ {conversations: [{id: "abc123", title: "My Chat", href: "..."}], total: 15}
```

**Search by title:**
```
claude_desktop_search(query="scheduler")
→ {query: "scheduler", matches: [...], total: 2}
```

**Navigate to chat:**
```
claude_desktop_navigate(chat_id="abc123-def456")
→ {success: true, navigated_to: "https://claude.ai/chat/abc123-def456"}
```

**Send and wait:**
```
claude_desktop_send(message="What is 2+2?", wait_for_response=true)
→ {success: true, sent: "What is 2+2?", response: "2+2 equals 4"}
```

**Read messages:**
```
claude_desktop_read(last_n=5)
→ {messages: [...], total: 20}
```

**New conversation:**
```
claude_desktop_new()
→ {success: true, url: "https://claude.ai/new"}
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ Claude Code │────▶│ MCP Server   │────▶│ Claude Desktop│
│ (WSL)       │     │ (Python)     │     │ (Windows)     │
└─────────────┘     └──────────────┘     └───────────────┘
                           │
                    DevTools Protocol
                    (ws://127.0.0.1:9222)
```

## Limitations

- Requires Claude Desktop running with debug port
- WSL→Windows networking may need configuration
- Some selectors may break with Claude Desktop updates
