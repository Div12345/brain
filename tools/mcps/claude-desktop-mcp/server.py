#!/usr/bin/env python3
"""
Claude Desktop MCP Server - Control Claude Desktop from any agent.

Tools:
  - claude_desktop_send: Send a message and optionally wait for response
  - claude_desktop_read: Get current conversation messages
  - claude_desktop_info: Get conversation ID and metadata
"""

import json
import time
import hashlib
import sys
from typing import Any

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# DevTools connection (reuse existing logic)
import requests
import websocket

DEVTOOLS_URL = "http://127.0.0.1:9222"

def get_claude_ws():
    """Connect to Claude Desktop via DevTools."""
    try:
        response = requests.get(f"{DEVTOOLS_URL}/json", timeout=5)
        targets = response.json()
        for target in targets:
            if "claude.ai" in target.get("url", "") and target.get("type") == "page":
                ws_url = target.get("webSocketDebuggerUrl")
                if ws_url:
                    return websocket.create_connection(ws_url, timeout=10)
    except Exception as e:
        return None
    return None

def send_cdp(ws, method, params=None, cmd_id=1):
    """Send CDP command."""
    cmd = {"id": cmd_id, "method": method}
    if params:
        cmd["params"] = params
    ws.send(json.dumps(cmd))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == cmd_id:
            return resp

def eval_js(ws, expression, cmd_id=1):
    """Evaluate JS in page."""
    result = send_cdp(ws, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True
    }, cmd_id)
    return result.get("result", {}).get("result", {}).get("value")

def get_conversations(ws):
    """Get list of conversations from sidebar."""
    js = """
    (function() {
        const items = document.querySelectorAll('a[href*="/chat/"]');
        const convos = [];
        items.forEach((el, i) => {
            if (i < 30) {
                const href = el.href || '';
                const id = href.split('/chat/').pop()?.split('?')[0] || '';
                const title = (el.innerText || '').trim().substring(0, 100);
                if (id && title) convos.push({id, title, href});
            }
        });
        return JSON.stringify(convos);
    })()
    """
    result = eval_js(ws, js)
    return json.loads(result) if result else []

def get_messages(ws):
    """Get all messages from conversation."""
    js = """
    (function() {
        const container = document.querySelector('.flex-1.flex.flex-col.px-4.max-w-3xl');
        if (!container) return '[]';
        const messages = [];
        Array.from(container.children).forEach((child, i) => {
            const text = (child.innerText || '').trim();
            if (text.length < 20) return;
            const hasUserMsg = child.querySelector('[data-testid="user-message"]');
            messages.push({
                index: i,
                role: hasUserMsg ? 'user' : 'assistant',
                text: text.substring(0, 4000)
            });
        });
        return JSON.stringify(messages);
    })()
    """
    result = eval_js(ws, js)
    return json.loads(result) if result else []

def send_message(ws, message):
    """Send a message via ProseMirror contenteditable."""
    # Escape message for JS string
    escaped = json.dumps(message)

    # Target ProseMirror editor (not textarea - that's just for accessibility)
    js_input = f"""
    (function() {{
        const pm = document.querySelector('.ProseMirror');
        if (!pm) return 'no-prosemirror';

        // Focus the editor
        pm.focus();

        // Set content via innerHTML (works with contenteditable)
        pm.innerHTML = '<p>' + {escaped} + '</p>';

        // Dispatch input event so React/tiptap picks up the change
        pm.dispatchEvent(new InputEvent('input', {{
            bubbles: true,
            cancelable: true,
            inputType: 'insertText',
            data: {escaped}
        }}));

        return 'text-set';
    }})()
    """
    result = eval_js(ws, js_input, 5)
    if result != 'text-set':
        return {"success": False, "error": f"Input failed: {result}"}

    time.sleep(0.3)

    js_send = """
    (function() {
        const btn = document.querySelector('button[aria-label="Send message"]');
        if (!btn) return 'no-send-button';
        if (btn.disabled) return 'button-disabled';
        btn.click();
        return 'sent';
    })()
    """
    result = eval_js(ws, js_send, 6)
    return {"success": result == 'sent', "error": None if result == 'sent' else result}

def wait_for_response(ws, timeout=120, poll_interval=2):
    """Wait for Claude to finish responding."""
    start = time.time()
    last_hash = None
    stable_count = 0

    while time.time() - start < timeout:
        messages = get_messages(ws)
        current_hash = hashlib.md5(json.dumps(messages).encode()).hexdigest()

        if current_hash == last_hash:
            stable_count += 1
            # Response stable for 2 polls = done
            if stable_count >= 2 and messages and messages[-1].get('role') == 'assistant':
                return messages[-1].get('text', '')
        else:
            stable_count = 0
            last_hash = current_hash

        time.sleep(poll_interval)

    return None  # Timeout

# MCP Server Setup
server = Server("claude-desktop")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="claude_desktop_send",
            description="Send a message to Claude Desktop. Optionally wait for response.",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Message to send"},
                    "wait_for_response": {"type": "boolean", "description": "Wait for Claude's response", "default": True},
                    "timeout": {"type": "integer", "description": "Max seconds to wait", "default": 120}
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="claude_desktop_read",
            description="Read messages from current Claude Desktop conversation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "last_n": {"type": "integer", "description": "Only return last N messages", "default": 10}
                }
            }
        ),
        Tool(
            name="claude_desktop_info",
            description="Get current Claude Desktop conversation info (ID, URL, title).",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="claude_desktop_list",
            description="List all conversations from Claude Desktop sidebar.",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    ws = get_claude_ws()
    if not ws:
        return [TextContent(
            type="text",
            text=json.dumps({"error": "Cannot connect to Claude Desktop. Launch with --remote-debugging-port=9222 --remote-allow-origins=*"})
        )]

    try:
        if name == "claude_desktop_send":
            message = arguments.get("message", "")
            wait = arguments.get("wait_for_response", True)
            timeout = arguments.get("timeout", 120)

            result = send_message(ws, message)
            if not result["success"]:
                return [TextContent(type="text", text=json.dumps(result))]

            if wait:
                response = wait_for_response(ws, timeout)
                return [TextContent(type="text", text=json.dumps({
                    "success": True,
                    "sent": message,
                    "response": response
                }))]
            else:
                return [TextContent(type="text", text=json.dumps({
                    "success": True,
                    "sent": message,
                    "response": None,
                    "note": "Message sent, not waiting for response"
                }))]

        elif name == "claude_desktop_read":
            last_n = arguments.get("last_n", 10)
            messages = get_messages(ws)
            return [TextContent(type="text", text=json.dumps({
                "messages": messages[-last_n:] if last_n else messages,
                "total": len(messages)
            }))]

        elif name == "claude_desktop_info":
            url = eval_js(ws, "window.location.href", 1)
            title = eval_js(ws, "document.title", 2)
            conv_id = None
            if url and '/chat/' in url:
                conv_id = url.split('/chat/')[-1].split('?')[0]
            return [TextContent(type="text", text=json.dumps({
                "url": url,
                "conversation_id": conv_id,
                "title": title
            }))]

        elif name == "claude_desktop_list":
            convos = get_conversations(ws)
            return [TextContent(type="text", text=json.dumps({
                "conversations": convos,
                "total": len(convos)
            }))]

        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    finally:
        ws.close()

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
