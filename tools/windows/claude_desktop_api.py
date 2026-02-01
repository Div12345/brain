#!/usr/bin/env python3
"""
Claude Desktop Controller - Bidirectional communication with Claude Desktop on Windows.
Run from Windows Python (Anaconda): python claude_desktop_api.py <command> [args]

Commands:
    status              Check if Claude Desktop is running
    send <message>      Send a message to Claude Desktop
    read                Read the current conversation
    last                Get the last assistant response
    latest              Get only the latest exchange (last user msg + response)
    wait [timeout]      Wait for Claude to finish responding
    watch [interval]    Watch for new responses (continuous)
"""

import sys
import time
import re
import hashlib
import pyautogui
import pyperclip

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Disable pyautogui failsafe for automation
pyautogui.FAILSAFE = False

# Cache for detecting changes
_last_content_hash = None


def find_claude_window():
    """Find and return the Claude Desktop window."""
    windows = pyautogui.getWindowsWithTitle('Claude')
    for w in windows:
        if w.title == 'Claude':
            return w
    return None


def focus_claude():
    """Focus the Claude Desktop window."""
    w = find_claude_window()
    if w:
        w.activate()
        time.sleep(0.3)
        return True
    return False


def send_message(message):
    """Send a message to Claude Desktop."""
    if not focus_claude():
        return {"success": False, "error": "Claude window not found"}

    time.sleep(0.2)
    pyautogui.typewrite(message, interval=0.01)
    time.sleep(0.1)
    pyautogui.press('enter')
    return {"success": True, "message": "Message sent"}


def read_conversation():
    """Read the full conversation from Claude Desktop."""
    if not focus_claude():
        return {"success": False, "error": "Claude window not found"}

    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    pyautogui.press('escape')

    content = pyperclip.paste()
    return {"success": True, "content": content}


def parse_messages(content):
    """Parse conversation into structured messages."""
    # Remove footer
    content = re.sub(r'Claude is AI and can make mistakes.*$', '', content, flags=re.DOTALL).strip()

    # Split by timestamps (pattern: "X:XX AM/PM" on its own line)
    # Each timestamp starts a new message
    parts = re.split(r'\n(\d{1,2}:\d{2}\s*[AP]M)\n', content)

    messages = []
    i = 0
    while i < len(parts):
        if i == 0 and parts[0].strip():
            # Content before first timestamp
            messages.append({"time": None, "content": parts[0].strip()})
            i += 1
        elif i + 1 < len(parts):
            # timestamp followed by content
            timestamp = parts[i].strip()
            msg_content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if msg_content:
                messages.append({"time": timestamp, "content": msg_content})
            i += 2
        else:
            i += 1

    return messages


def get_last_response():
    """Extract the last assistant response from the conversation."""
    result = read_conversation()
    if not result["success"]:
        return result

    messages = parse_messages(result["content"])

    if not messages:
        return {"success": True, "last_response": ""}

    # Get last message (should be assistant's response)
    last = messages[-1]["content"]

    # Try to separate the thinking line from the actual response
    lines = last.split('\n')
    if len(lines) > 1 and any(word in lines[0].lower() for word in ['acknowledged', 'recognized', 'understood', 'analyzing']):
        # First line is likely Claude's "thinking" indicator
        return {"success": True, "last_response": '\n'.join(lines[1:]).strip()}

    return {"success": True, "last_response": last}


def get_latest_exchange():
    """Get the last user message and Claude's response."""
    result = read_conversation()
    if not result["success"]:
        return result

    messages = parse_messages(result["content"])

    if len(messages) < 2:
        return {"success": True, "user_message": "", "response": messages[-1]["content"] if messages else ""}

    # Last two messages: user's question and Claude's response
    # But we need to identify which is which
    # Typically, messages with thinking indicators are Claude's

    last = messages[-1]["content"]
    second_last = messages[-2]["content"]

    return {
        "success": True,
        "user_message": second_last,
        "response": last
    }


def content_changed(content):
    """Check if content has changed since last read."""
    global _last_content_hash
    current_hash = hashlib.md5(content.encode()).hexdigest()
    if current_hash != _last_content_hash:
        _last_content_hash = current_hash
        return True
    return False


def wait_for_response(timeout=120, poll_interval=2):
    """Wait for Claude to finish responding."""
    start = time.time()
    last_content = ""
    stable_count = 0

    while time.time() - start < timeout:
        result = read_conversation()
        if not result["success"]:
            time.sleep(poll_interval)
            continue

        current = result["content"]

        if current == last_content:
            stable_count += 1
            if stable_count >= 2:
                return get_last_response()
        else:
            stable_count = 0
            last_content = current

        time.sleep(poll_interval)

    return {"success": False, "error": "Timeout waiting for response"}


def watch_for_responses(interval=3):
    """Continuously watch for new responses."""
    global _last_content_hash
    print("Watching for new responses... (Ctrl+C to stop)")

    # Initialize with current content
    result = read_conversation()
    if result["success"]:
        _last_content_hash = hashlib.md5(result["content"].encode()).hexdigest()

    try:
        while True:
            time.sleep(interval)
            result = read_conversation()
            if result["success"] and content_changed(result["content"]):
                response = get_last_response()
                if response["success"]:
                    print(f"\n--- New response at {time.strftime('%H:%M:%S')} ---")
                    print(response["last_response"][:500])
                    if len(response["last_response"]) > 500:
                        print("... (truncated)")
                    print("---")
    except KeyboardInterrupt:
        print("\nStopped watching.")


def status():
    """Check Claude Desktop status."""
    w = find_claude_window()
    if w:
        return {"success": True, "running": True, "window": str(w)}
    return {"success": True, "running": False}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "status":
        result = status()
    elif command == "send":
        if len(sys.argv) < 3:
            print("Usage: claude_desktop_api.py send <message>")
            sys.exit(1)
        message = " ".join(sys.argv[2:])
        result = send_message(message)
    elif command == "read":
        result = read_conversation()
    elif command == "last":
        result = get_last_response()
    elif command == "latest":
        result = get_latest_exchange()
    elif command == "wait":
        timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 120
        result = wait_for_response(timeout)
    elif command == "watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        watch_for_responses(interval)
        return
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    # Output
    if result.get("success"):
        if "content" in result:
            print(result["content"])
        elif "last_response" in result:
            print(result["last_response"])
        elif "response" in result:
            print(f"USER: {result.get('user_message', '')[:100]}...")
            print(f"CLAUDE: {result['response']}")
        elif "running" in result:
            print(f"Running: {result['running']}")
        else:
            print(result.get("message", "OK"))
    else:
        print(f"ERROR: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
