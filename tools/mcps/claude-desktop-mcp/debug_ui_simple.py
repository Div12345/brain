import json
import time
import sys
import os

sys.path.append(os.getcwd())
from server import *


def debug_ui_simple():
    ws = get_main_process_ws()
    if not ws:
        print("No WS")
        return
    ensure_debugger_attached(ws)

    # Very simple JS
    js_simple = "window.location.href + ' | ' + document.title"

    js_main = f"""
    (function() {{
        try {{
            const electron = process.mainModule.require('electron');
            const {{ BrowserWindow }} = electron;
            const win = BrowserWindow.fromId(1);
            return win.webContents.executeJavaScript("{js_simple}");
        }} catch (e) {{
            return {{ error: e.toString() }};
        }}
    }})()
    """

    command = {
        "id": 4001,
        "method": "Runtime.evaluate",
        "params": {"expression": js_main, "awaitPromise": True, "returnByValue": True},
    }

    ws.send(json.dumps(command))
    start = time.time()
    while time.time() - start < 5:
        try:
            raw = ws.recv()
            msg = json.loads(raw)
            if msg.get("id") == 4001:
                print(json.dumps(msg, indent=2))
                break
        except:
            break
    ws.close()


if __name__ == "__main__":
    debug_ui_simple()
