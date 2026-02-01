#!/usr/bin/env python3
"""
Claude Desktop DevTools API - Precise transcript access via Chrome DevTools Protocol.

Requires: Claude Desktop launched with --remote-debugging-port=9222 --remote-allow-origins=*

Commands:
    info                Get current conversation info (URL, ID, title)
    messages            Get all messages from current conversation
    last                Get last assistant message
    send <message>      Send a message
    watch [interval]    Watch for new messages
"""

import sys
import json
import time
import hashlib
import requests
import websocket

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

DEVTOOLS_URL = "http://127.0.0.1:9222"

def get_claude_page():
    """Find the Claude page from DevTools targets."""
    try:
        response = requests.get(f"{DEVTOOLS_URL}/json", timeout=5)
        targets = response.json()
        for target in targets:
            url = target.get("url", "")
            # Match any page on claude.ai domain
            if "claude.ai" in url and target.get("type") == "page":
                return target
    except Exception as e:
        print(f"Error connecting to DevTools: {e}", file=sys.stderr)
        print("Make sure Claude Desktop is running with --remote-debugging-port=9222 --remote-allow-origins=*", file=sys.stderr)
    return None


def connect_devtools():
    """Connect to Claude page via WebSocket."""
    page = get_claude_page()
    if not page:
        return None
    ws_url = page.get("webSocketDebuggerUrl")
    if not ws_url:
        return None
    try:
        return websocket.create_connection(ws_url, timeout=10)
    except Exception as e:
        print(f"WebSocket connection error: {e}", file=sys.stderr)
        return None


def send_command(ws, method, params=None, cmd_id=1):
    """Send a CDP command and get response."""
    cmd = {"id": cmd_id, "method": method}
    if params:
        cmd["params"] = params
    ws.send(json.dumps(cmd))

    while True:
        response = json.loads(ws.recv())
        if response.get("id") == cmd_id:
            return response
        # Skip events, wait for our response


def evaluate_js(ws, expression, cmd_id=1):
    """Evaluate JavaScript in page context."""
    result = send_command(ws, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True
    }, cmd_id)
    return result.get("result", {}).get("result", {}).get("value")


def get_info(ws):
    """Get current conversation info."""
    url = evaluate_js(ws, "window.location.href", 1)
    title = evaluate_js(ws, "document.title", 2)

    conv_id = None
    if url and '/chat/' in url:
        conv_id = url.split('/chat/')[-1].split('?')[0]

    return {
        "url": url,
        "conversation_id": conv_id,
        "title": title,
        "is_new": conv_id is None
    }


def get_messages(ws):
    """Extract messages from the conversation DOM."""
    js_code = """
    (function() {
        // Find the conversation container
        const container = document.querySelector('.flex-1.flex.flex-col.px-4.max-w-3xl');
        if (!container) return '[]';

        const messages = [];

        // Each direct child is a message turn - filter out empty elements
        Array.from(container.children).forEach((child, i) => {
            const text = (child.innerText || '').trim();
            // Skip empty or tiny elements
            if (text.length < 20) return;

            const hasUserMsg = child.querySelector('[data-testid="user-message"]');
            messages.push({
                index: i,
                role: hasUserMsg ? 'user' : 'assistant',
                text: text.substring(0, 2000)
            });
        });

        return JSON.stringify(messages);
    })()
    """
    result = evaluate_js(ws, js_code, 3)
    if result:
        try:
            return json.loads(result)
        except:
            return []
    return []


def get_last_message(ws):
    """Get the last assistant message."""
    js_code = """
    (function() {
        const container = document.querySelector('.flex-1.flex.flex-col.px-4.max-w-3xl');
        if (!container) return null;

        // Find the last child with actual content that isn't a user message
        const children = Array.from(container.children);
        for (let i = children.length - 1; i >= 0; i--) {
            const child = children[i];
            const text = (child.innerText || '').trim();
            // Skip empty elements
            if (text.length < 20) continue;

            const hasUserMsg = child.querySelector('[data-testid="user-message"]');
            if (!hasUserMsg) {
                return text.substring(0, 3000);
            }
        }
        return null;
    })()
    """
    return evaluate_js(ws, js_code, 4)


def send_message_via_dom(ws, message):
    """Send a message via DevTools using execCommand (works with React)."""
    # Use execCommand insertText which properly triggers React's input handling
    js_code = f"""
    (function() {{
        const ta = document.querySelector('textarea');
        if (!ta) return 'no-textarea';

        ta.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, {json.dumps(message)});

        return 'text-set';
    }})()
    """
    result = evaluate_js(ws, js_code, 5)

    if result != 'text-set':
        return f"Input failed: {result}"

    time.sleep(0.2)

    # Click send button
    js_send = """
    (function() {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
            if (ariaLabel.includes('send')) {
                btn.click();
                return 'sent';
            }
        }
        return 'no send button';
    })()
    """
    result = evaluate_js(ws, js_send, 6)
    return "Message sent" if result == 'sent' else result


def watch_messages(ws, interval=3):
    """Watch for new messages."""
    print("Watching for new messages... (Ctrl+C to stop)")
    last_hash = None

    try:
        while True:
            messages = get_messages(ws)
            current_hash = hashlib.md5(json.dumps(messages).encode()).hexdigest()

            if current_hash != last_hash and last_hash is not None:
                print(f"\n--- New content at {time.strftime('%H:%M:%S')} ---")
                if messages:
                    last_msg = messages[-1] if messages else {}
                    print(f"Last: {last_msg.get('text', '')[:200]}")
                print("---")

            last_hash = current_hash
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped watching.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    ws = connect_devtools()
    if not ws:
        print("Failed to connect to Claude Desktop DevTools", file=sys.stderr)
        print("Launch Claude with: claude.exe --remote-debugging-port=9222 --remote-allow-origins=*", file=sys.stderr)
        sys.exit(1)

    try:
        if command == "info":
            info = get_info(ws)
            print(json.dumps(info, indent=2))

        elif command == "messages":
            messages = get_messages(ws)
            for msg in messages[-10:]:  # Last 10 messages
                role = msg.get('role', '?')
                text = msg.get('text', '')[:100].replace('\n', ' ')
                print(f"[{role}] {text}")

        elif command == "last":
            last = get_last_message(ws)
            print(last if last else "No messages found")

        elif command == "send":
            if len(sys.argv) < 3:
                print("Usage: claude_devtools_api.py send <message>")
                sys.exit(1)
            message = " ".join(sys.argv[2:])
            result = send_message_via_dom(ws, message)
            print(result)

        elif command == "watch":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            watch_messages(ws, interval)

        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)

    finally:
        ws.close()


if __name__ == "__main__":
    main()
