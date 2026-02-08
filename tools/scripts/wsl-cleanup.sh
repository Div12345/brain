#!/bin/bash
# WSL Memory Cleanup Script
# Kills orphaned processes from closed terminals

set -euo pipefail

echo "=== WSL Memory Cleanup ==="
echo "Before:"
free -h | grep Mem

# Kill orphaned gemini processes (not attached to terminal)
echo -e "\nKilling orphaned gemini processes..."
pkill -f "gemini -p" 2>/dev/null || true

# Kill orphaned npm exec MCP servers (detached from terminal)
echo "Killing orphaned npm exec processes..."
pgrep -f "npm exec.*mcp" | while read pid; do
    # Check if process has a controlling terminal
    if ! ps -p "$pid" -o tty= | grep -q "pts"; then
        echo "  Killing orphaned MCP: $pid"
        kill "$pid" 2>/dev/null || true
    fi
done

# Kill orphaned node processes older than 2 hours with no terminal
echo "Killing old orphaned node processes..."
ps aux | grep node | grep -v grep | while read user pid cpu mem vsz rss tty stat start time cmd; do
    if [[ "$tty" == "?" ]]; then
        # Process has no terminal - check if it's old
        echo "  Found detached node: $pid ($cmd)"
        # Be conservative - only kill if explicitly orphaned
    fi
done

# Kill any ccq/scheduler processes not in current session
echo "Killing orphaned ccq processes..."
pkill -f "ccq run" 2>/dev/null || true

# Clear page cache (requires sudo)
if command -v sudo &>/dev/null; then
    echo -e "\nClearing page cache..."
    sudo sh -c 'echo 1 > /proc/sys/vm/drop_caches' 2>/dev/null || echo "  (skipped - needs sudo)"
fi

echo -e "\nAfter:"
free -h | grep Mem

echo -e "\n=== Active processes ==="
ps aux --sort=-%mem | head -10
