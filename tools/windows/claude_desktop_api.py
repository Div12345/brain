#!/usr/bin/env python3
"""
Claude Desktop Controller - Bidirectional communication with Claude Desktop on Windows.
Run from Windows Python (Anaconda): python claude_desktop_api.py <command> [args]

Commands:
    status          - Check if Claude Desktop is running
    send <message>  - Send a message to Claude Desktop
    read            - Read the current conversation
    last            - Get the last assistant response
    wait            - Wait for Claude to finish responding
"""

import sys
import time
import re
import pyautogui
import pyperclip

# Disable pyautogui failsafe for automation
pyautogui.FAILSAFE = False


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

    # Type the message
    pyautogui.typewrite(message, interval=0.01)
    time.sleep(0.1)

    # Send with Enter
    pyautogui.press('enter')

    return {"success": True, "message": "Message sent"}


def read_conversation():
    """Read the full conversation from Claude Desktop."""
    if not focus_claude():
        return {"success": False, "error": "Claude window not found"}

    time.sleep(0.2)

    # Select all and copy
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    pyautogui.press('escape')

    content = pyperclip.paste()
    return {"success": True, "content": content}


def get_last_response():
    """Extract the last assistant response from the conversation."""
    result = read_conversation()
    if not result["success"]:
        return result

    content = result["content"]

    # Split by time stamps (pattern: "X:XX AM/PM")
    # Messages are typically separated by timestamps
    parts = re.split(r'\n\d{1,2}:\d{2}\s*[AP]M\n', content)

    if len(parts) < 2:
        return {"success": True, "last_response": content[-1000:]}

    # Get the last non-empty part
    last = parts[-1].strip()

    # Remove the footer
    last = re.sub(r'Claude is AI and can make mistakes.*$', '', last, flags=re.DOTALL).strip()

    return {"success": True, "last_response": last}


def is_claude_responding():
    """Check if Claude is currently generating a response."""
    result = read_conversation()
    if not result["success"]:
        return None

    content = result["content"]

    # Look for indicators that Claude is still responding
    # (Stop button visible, or content is changing)
    if "Stop" in content[-200:]:  # Stop button might be visible
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
            if stable_count >= 2:  # Content stable for 2 polls
                return get_last_response()
        else:
            stable_count = 0
            last_content = current

        time.sleep(poll_interval)

    return {"success": False, "error": "Timeout waiting for response"}


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
    elif command == "wait":
        timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 120
        result = wait_for_response(timeout)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    # Output as simple format
    if result.get("success"):
        if "content" in result:
            print(result["content"])
        elif "last_response" in result:
            print(result["last_response"])
        elif "running" in result:
            print(f"Running: {result['running']}")
        else:
            print(result.get("message", "OK"))
    else:
        print(f"ERROR: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
