#!/bin/bash
# Send a message to Claude Desktop on Windows
# Usage: ./claude_send.sh "Your message here"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PS_SCRIPT="$(wslpath -w "$SCRIPT_DIR/claude_desktop_control.ps1")"

if [ -z "$1" ]; then
    echo "Usage: $0 \"message to send\""
    echo "       $0 --status    # Check if Claude Desktop is running"
    echo "       $0 --focus     # Focus Claude Desktop window"
    exit 1
fi

case "$1" in
    --status)
        /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File "$PS_SCRIPT" -Action status
        ;;
    --focus)
        /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File "$PS_SCRIPT" -Action focus
        ;;
    *)
        /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File "$PS_SCRIPT" -Action send -Message "$1"
        ;;
esac
