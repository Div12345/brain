import json
import time
import sys
import os

sys.path.append(os.getcwd())
from server import *


def dump_html():
    ws = get_main_process_ws()
    if not ws:
        return
    ensure_debugger_attached(ws)

    js_main = """
    (function() {
        const electron = process.mainModule.require('electron');
        const win = electron.BrowserWindow.fromId(1);
        return win.webContents.executeJavaScript('document.body.outerHTML');
    })()
    """

    command = {
        "id": 6001,
        "method": "Runtime.evaluate",
        "params": {"expression": js_main, "awaitPromise": True, "returnByValue": True},
    }

    ws.send(json.dumps(command))
    time.sleep(2)

    while True:
        try:
            res = json.loads(ws.recv())
            if res.get("id") == 6001:
                # Save to file
                html = res.get("result", {}).get("result", {}).get("value", "")
                with open("cd_dump.html", "w") as f:
                    f.write(html)
                print("Dumped to cd_dump.html")
                break
        except:
            break
    ws.close()


if __name__ == "__main__":
    dump_html()
