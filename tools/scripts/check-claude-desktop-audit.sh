#!/bin/bash
# Quick check on Claude Desktop audit progress

cd /home/div/brain/tools/mcps/claude-desktop-mcp

echo "=== Claude Desktop Status ==="
python3 -c "
import sys
sys.path.insert(0, '.')
from server import get_main_process_ws, get_status, get_messages
import json

ws = get_main_process_ws()
if not ws:
    print('ERROR: Cannot connect to Claude Desktop')
    sys.exit(1)

status = get_status(ws)
print(json.dumps(status, indent=2))

if not status.get('is_generating'):
    print('\n=== Last Response (truncated) ===')
    msgs = get_messages(ws)
    if msgs:
        last = msgs[-1].get('text', '')
        print(last[:2000])
        if len(last) > 2000:
            print(f'\n... ({len(last)} total chars)')

ws.close()
"

echo ""
echo "=== Check for output file ==="
ls -la /home/div/AAA_detection_personal/docs/plans/2026-02-08-codebase-audit-report-v2.md 2>/dev/null || echo "Report not yet created"
