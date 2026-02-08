import json
import time
import sys
import os

sys.path.append(os.getcwd())
from server import *


def list_sidebar_chats():
    ws = get_main_process_ws()
    if not ws:
        return
    ensure_debugger_attached(ws)

    js_renderer = """
    (function() {
        // Look for sidebar items. 
        // They usually have titles.
        // We'll search for 'Cardiovascular' or 'death'
        
        const deepSearch = (root) => {
            const queue = [root];
            const found = [];
            while (queue.length > 0) {
                const el = queue.shift();
                if (!el) continue;
                
                const text = el.innerText || '';
                if (text.includes('Cardiovascular') || text.includes('death')) {
                    found.push({
                        text: text.substring(0, 50),
                        tagName: el.tagName,
                        className: el.className,
                        rect: el.getBoundingClientRect()
                    });
                }
                
                for (let i = 0; i < el.children.length; i++) {
                    queue.push(el.children[i]);
                }
                if (found.length > 10) break;
            }
            return found;
        };
        
        return deepSearch(document.body);
    })()
    """

    js_main = f"""
    (function() {{
        const electron = process.mainModule.require('electron');
        const win = electron.BrowserWindow.fromId(1);
        return win.webContents.executeJavaScript(`{js_renderer}`);
    }})()
    """

    command = {
        "id": 5001,
        "method": "Runtime.evaluate",
        "params": {"expression": js_main, "awaitPromise": True, "returnByValue": True},
    }

    ws.send(json.dumps(command))
    time.sleep(2)

    while True:
        try:
            res = json.loads(ws.recv())
            if res.get("id") == 5001:
                print(json.dumps(res, indent=2))
                break
        except:
            break
    ws.close()


if __name__ == "__main__":
    list_sidebar_chats()
