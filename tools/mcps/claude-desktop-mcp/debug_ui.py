import json
import time
import sys
import os

# Add server directory to path to import server
sys.path.append(os.getcwd())
from server import *


def debug_ui():
    ws = get_main_process_ws()
    if not ws:
        print("Could not connect to main process debugger")
        return

    ensure_debugger_attached(ws)

    # JS to run in Renderer
    js_renderer = """
    (function() {
        // Helper to get element info
        function getInfo(el) {
            return {
                tagName: el.tagName,
                text: (el.innerText || '').substring(0, 50).replace(/\\n/g, ' '),
                ariaLabel: el.getAttribute('aria-label'),
                testid: el.getAttribute('data-testid'),
                className: el.className,
                rect: el.getBoundingClientRect()
            };
        }

        // Find buttons related to Model or Claude
        const buttons = Array.from(document.querySelectorAll('button'));
        const candidates = buttons.filter(b => {
            const t = (b.innerText || '').toLowerCase();
            const a = (b.getAttribute('aria-label') || '').toLowerCase();
            const d = (b.getAttribute('data-testid') || '').toLowerCase();
            return t.includes('model') || t.includes('claude') || t.includes('sonnet') || t.includes('opus') ||
                   a.includes('model') || a.includes('claude') ||
                   d.includes('model') || d.includes('selector');
        });

        return candidates.map(getInfo);
    })()
    """

    # JS to run in Main process (to inject renderer JS)
    # properly escaped for JSON string
    js_main = f"""
    (function() {{
        try {{
            const electron = process.mainModule.require('electron');
            const {{ BrowserWindow }} = electron;
            const win = BrowserWindow.fromId(1);
            if (!win) return {{ error: 'Window 1 not found' }};
            
            return win.webContents.executeJavaScript(`{js_renderer}`);
        }} catch (e) {{
            return {{ error: e.toString() }};
        }}
    }})()
    """

    print("Sending Runtime.evaluate...")

    command = {
        "id": 3001,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_main,
            "awaitPromise": True,  # Important for executeJavaScript
            "returnByValue": True,
        },
    }

    ws.send(json.dumps(command))

    # Wait for response
    start = time.time()
    while time.time() - start < 10:
        try:
            raw = ws.recv()
            msg = json.loads(raw)
            if msg.get("id") == 3001:
                print(json.dumps(msg, indent=2))
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    ws.close()


if __name__ == "__main__":
    debug_ui()
