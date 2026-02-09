#!/usr/bin/env python3
"""
Claude Desktop MCP Server - Control Claude Desktop from any agent.

Uses the main process debugger (port 9229) to proxy CDP commands to the renderer.
Requires: Enable "Main Process Debugger" in Claude Desktop settings.

Tools:
  - claude_desktop_send: Send a message and optionally wait for response
  - claude_desktop_read: Get current conversation messages
  - claude_desktop_info: Get conversation ID and metadata
"""

import json
import time
import subprocess
import sys
from typing import Any

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

import requests
import websocket


def get_inspect_url():
    """Get the inspect URL - localhost works for both native and WSL."""
    # WSL can reach Windows localhost:9229 directly, no need for host IP
    return "http://127.0.0.1:9229"


INSPECT_URL = get_inspect_url()


def get_claude_desktop_exe():
    """Find the latest Claude Desktop executable dynamically."""
    import os
    import platform

    if platform.system() == "Windows":
        base_path = os.path.expandvars(r"%LOCALAPPDATA%\AnthropicClaude")
        if os.path.exists(base_path):
            # Find all app-* directories and get the latest one
            app_dirs = [d for d in os.listdir(base_path) if d.startswith("app-")]
            if app_dirs:
                # Sort by version number (app-1.1.1890 -> 1.1.1890)
                app_dirs.sort(
                    key=lambda x: [int(n) for n in x.replace("app-", "").split(".")],
                    reverse=True,
                )
                latest = app_dirs[0]
                exe_path = os.path.join(base_path, latest, "claude.exe")
                if os.path.exists(exe_path):
                    return exe_path
        # Fallback to Squirrel launcher
        launcher = os.path.join(base_path, "claude.exe")
        if os.path.exists(launcher):
            return launcher
    else:
        # Linux/Mac paths
        for path in [
            "/usr/bin/claude",
            "/Applications/Claude.app/Contents/MacOS/Claude",
        ]:
            if os.path.exists(path):
                return path

    return None


def get_main_process_ws():
    """Connect to Claude Desktop main process via Node inspector."""
    try:
        response = requests.get(f"{INSPECT_URL}/json", timeout=5)
        targets = response.json()
        for target in targets:
            if target.get("type") == "node":
                ws_url = target.get("webSocketDebuggerUrl")
                if ws_url:
                    return websocket.create_connection(ws_url, timeout=10)
    except Exception as e:
        return None
    return None


def send_inspector_cmd(ws, method, params=None, cmd_id=1):
    """Send command to Node inspector."""
    cmd = {"id": cmd_id, "method": method}
    if params:
        cmd["params"] = params
    ws.send(json.dumps(cmd))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == cmd_id:
            return resp


def eval_in_main(ws, expression, cmd_id=1):
    """Evaluate JS in main process."""
    result = send_inspector_cmd(
        ws,
        "Runtime.evaluate",
        {"expression": expression, "returnByValue": True},
        cmd_id,
    )
    return result.get("result", {}).get("result", {}).get("value")


def ensure_debugger_attached(ws):
    """Ensure debugger is attached to the claude.ai renderer."""
    js = """
    (function() {
        try {
            const electron = process.mainModule ? process.mainModule.require("electron") : global.require("electron");
            const { webContents } = electron;
            const all = webContents.getAllWebContents();

            // Find the claude.ai webContents
            const claudeWc = all.find(wc => wc.getURL().includes("claude.ai"));
            if (!claudeWc) return { error: "No claude.ai webContents found. Make sure you're logged in." };

            if (!claudeWc.debugger.isAttached()) {
                claudeWc.debugger.attach("1.3");
            }
            return { attached: true, url: claudeWc.getURL() };
        } catch(e) {
            return { error: e.message };
        }
    })()
    """
    result = eval_in_main(ws, js)
    return result


def eval_in_renderer(ws, expression, cmd_id=1):
    """Evaluate JS in renderer via main process proxy.

    Targets the webContents that has claude.ai URL (not the wrapper window).
    """
    # Escape the expression for embedding in JS string
    escaped_expr = json.dumps(expression)

    js = f"""
    (async function() {{
        try {{
            const electron = process.mainModule ? process.mainModule.require("electron") : global.require("electron");
            const {{ webContents }} = electron;
            const all = webContents.getAllWebContents();

            // Find the claude.ai webContents (not the wrapper)
            const claudeWc = all.find(wc => wc.getURL().includes("claude.ai"));
            if (!claudeWc) return JSON.stringify({{ error: "No claude.ai webContents found" }});

            if (!claudeWc.debugger.isAttached()) {{
                claudeWc.debugger.attach("1.3");
            }}

            const result = await claudeWc.debugger.sendCommand("Runtime.evaluate", {{
                expression: {escaped_expr},
                returnByValue: true
            }});

            return JSON.stringify(result);
        }} catch(e) {{
            return JSON.stringify({{ error: e.message }});
        }}
    }})()
    """

    # Use awaitPromise since we're using async
    result = send_inspector_cmd(
        ws,
        "Runtime.evaluate",
        {"expression": js, "returnByValue": True, "awaitPromise": True},
        cmd_id,
    )

    value = result.get("result", {}).get("result", {}).get("value")
    if value:
        try:
            parsed = json.loads(value)
            return parsed.get("result", {}).get("value")
        except:
            return value
    return None


def exec_in_renderer(ws, script, cmd_id=1):
    """Execute JavaScript in renderer using executeJavaScript.

    More reliable for async scripts than debugger.sendCommand.
    The script should be a Promise that resolves to the result.
    """
    escaped_script = json.dumps(script)

    js = f"""
    (async function() {{
        const electron = process.mainModule ? process.mainModule.require("electron") : global.require("electron");
        const {{ webContents }} = electron;
        const all = webContents.getAllWebContents();
        
        const claudeWc = all.find(wc => wc.getURL().includes("claude.ai"));
        if (!claudeWc) return JSON.stringify({{ error: "No claude.ai webContents found" }});
        
        try {{
            const result = await claudeWc.executeJavaScript({escaped_script});
            return JSON.stringify(result);
        }} catch(e) {{
            return JSON.stringify({{ error: e.message }});
        }}
    }})()
    """

    result = send_inspector_cmd(
        ws,
        "Runtime.evaluate",
        {"expression": js, "returnByValue": True, "awaitPromise": True},
        cmd_id,
    )

    value = result.get("result", {}).get("result", {}).get("value")
    if value:
        try:
            return json.loads(value)
        except:
            return value
    return None


def change_model(ws, model_name):
    """Change the Claude model.

    Args:
        model_name: One of 'Opus 4.6', 'Opus 4.5', 'Sonnet 4.5', 'Sonnet 4', 'Haiku 4.5', 'Opus 3', 'Haiku 3.5'
    """
    escaped_model = json.dumps(model_name)

    script = f"""
        new Promise(async (resolve) => {{
            const delay = ms => new Promise(r => setTimeout(r, ms));
            
            // Step 1: Click model selector
            const modelBtn = document.querySelector('[data-testid="model-selector-dropdown"]');
            if (!modelBtn) {{ resolve({{error: 'no model selector'}}); return; }}
            modelBtn.click();
            await delay(600);
            
            // Check if target model is already visible (might be in quick list)
            let targetEl = null;
            document.querySelectorAll('div, span').forEach(el => {{
                if (el.innerText?.trim() === {escaped_model} && el.children.length === 0) {{
                    targetEl = el;
                }}
            }});
            
            // If not found, click "More models" first
            if (!targetEl) {{
                let moreModels = null;
                document.querySelectorAll('div, span').forEach(el => {{
                    if (el.innerText?.trim() === 'More models' && el.children.length === 0) {{
                        moreModels = el;
                    }}
                }});
                
                if (moreModels) {{
                    moreModels.click();
                    await delay(600);
                    
                    // Now find the target model
                    document.querySelectorAll('div, span').forEach(el => {{
                        if (el.innerText?.trim() === {escaped_model} && el.children.length === 0) {{
                            targetEl = el;
                        }}
                    }});
                }}
            }}
            
            if (!targetEl) {{ 
                // Press Escape to close menu
                document.body.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
                resolve({{error: 'Model not found: ' + {escaped_model}}}); 
                return; 
            }}
            
            // Click the parent container (the clickable menu item row)
            let clickTarget = targetEl.parentElement?.parentElement || targetEl.parentElement || targetEl;
            clickTarget.click();
            await delay(500);
            
            // Get final model
            const finalModel = document.querySelector('[data-testid="model-selector-dropdown"]')?.innerText;
            resolve({{success: true, model: finalModel}});
        }})
    """

    return exec_in_renderer(ws, script)


def get_available_models(ws):
    """Get list of available models."""
    script = """
        new Promise(async (resolve) => {
            const delay = ms => new Promise(r => setTimeout(r, ms));
            
            // Click model selector
            const modelBtn = document.querySelector('[data-testid="model-selector-dropdown"]');
            if (!modelBtn) { resolve({error: 'no model selector'}); return; }
            
            const currentModel = modelBtn.innerText?.trim();
            modelBtn.click();
            await delay(600);
            
            // Click More models
            let moreModels = null;
            document.querySelectorAll('div, span').forEach(el => {
                if (el.innerText?.trim() === 'More models' && el.children.length === 0) {
                    moreModels = el;
                }
            });
            
            if (moreModels) {
                moreModels.click();
                await delay(600);
            }
            
            // Collect all model names
            const modelNames = ['Opus 4.6', 'Opus 4.5', 'Sonnet 4.5', 'Sonnet 4', 'Haiku 4.5', 'Opus 3', 'Haiku 3.5'];
            const available = [];
            
            document.querySelectorAll('div, span').forEach(el => {
                const text = el.innerText?.trim();
                if (modelNames.includes(text) && el.children.length === 0) {
                    if (!available.includes(text)) {
                        available.push(text);
                    }
                }
            });
            
            // Close menu
            document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
            
            resolve({current: currentModel, available: available});
        })
    """

    return exec_in_renderer(ws, script)


def get_conversations(ws):
    """Get list of conversations from sidebar."""
    js = """
    (function() {
        const items = document.querySelectorAll('a[href*="/chat/"]');
        const convos = [];
        items.forEach((el, i) => {
            if (i < 50) {
                const href = el.href || '';
                const id = href.split('/chat/').pop()?.split('?')[0] || '';
                const title = (el.innerText || '').trim().substring(0, 100);
                if (id && title) convos.push({id, title, href});
            }
        });
        return JSON.stringify(convos);
    })()
    """
    result = eval_in_renderer(ws, js)
    try:
        return json.loads(result) if result else []
    except:
        return []


def navigate_to_chat(ws, chat_id):
    """Navigate to a specific conversation."""
    url = f"https://claude.ai/chat/{chat_id}"
    js = f"window.location.href = '{url}'"
    eval_in_renderer(ws, js)
    time.sleep(2)
    return {"success": True, "navigated_to": url}


def create_new_chat(ws):
    """Create a new conversation."""
    js = "window.location.href = 'https://claude.ai/new'"
    eval_in_renderer(ws, js)
    time.sleep(1)
    return {"success": True, "url": "https://claude.ai/new"}


def search_conversations(ws, query):
    """Search conversations by title."""
    convos = get_conversations(ws)
    query_lower = query.lower()
    matches = [c for c in convos if query_lower in c.get("title", "").lower()]
    return matches


def get_messages(ws):
    """Get all messages from conversation."""
    js = """
    (function() {
        const container = document.querySelector('.flex-1.flex.flex-col.px-4.max-w-3xl');
        if (!container) return '[]';
        const messages = [];
        Array.from(container.children).forEach((child, i) => {
            const text = (child.innerText || '').trim();
            if (text.length < 20) return;
            const hasUserMsg = child.querySelector('[data-testid="user-message"]');
            messages.push({
                index: i,
                role: hasUserMsg ? 'user' : 'assistant',
                text: text.substring(0, 4000)
            });
        });
        return JSON.stringify(messages);
    })()
    """
    result = eval_in_renderer(ws, js)
    try:
        return json.loads(result) if result else []
    except:
        return []


def send_message(ws, message):
    """Send a message via ProseMirror contenteditable."""
    escaped = json.dumps(message)

    # Use textContent to avoid HTML injection — escaped is already JSON-safe
    js_input = f"""
    (function() {{
        const pm = document.querySelector('.ProseMirror');
        if (!pm) return 'no-prosemirror';
        pm.focus();
        // Create a text node inside a paragraph to avoid HTML interpretation
        const p = document.createElement('p');
        p.textContent = {escaped};
        pm.innerHTML = '';
        pm.appendChild(p);
        pm.dispatchEvent(new InputEvent('input', {{
            bubbles: true,
            cancelable: true,
            inputType: 'insertText',
            data: {escaped}
        }}));
        return 'text-set';
    }})()
    """
    result = eval_in_renderer(ws, js_input, 5)
    if result != "text-set":
        return {"success": False, "error": f"Input failed: {result}"}

    time.sleep(0.3)

    js_send = """
    (function() {
        const btn = document.querySelector('button[aria-label="Send message"]');
        if (!btn) return 'no-send-button';
        if (btn.disabled) return 'button-disabled';
        btn.click();
        return 'sent';
    })()
    """
    result = eval_in_renderer(ws, js_send, 6)
    return {"success": result == "sent", "error": None if result == "sent" else result}


def is_generating(ws):
    """Check if Desktop is currently generating a response.

    Uses the stop button as the definitive signal:
    - Present → generating
    - Absent → idle/done
    """
    js = """
    (function() {
        const stopBtn = document.querySelector('button[aria-label="Stop response"]');
        return stopBtn !== null;
    })()
    """
    result = eval_in_renderer(ws, js, 99)
    return result is True or result == "true" or result == True


def get_status(ws):
    """Get current Desktop status — lightweight, no side effects."""
    js = """
    (function() {
        const stopBtn = document.querySelector('button[aria-label="Stop response"]');
        const sendBtn = document.querySelector('button[aria-label="Send message"]');
        const modelEl = document.querySelector('[data-testid="model-selector-dropdown"]');

        // Count messages
        const userMsgs = document.querySelectorAll('[data-testid="user-message"]');
        const allMsgBlocks = document.querySelectorAll('[data-testid="user-message"], [data-testid="chat-message-text"]');

        return JSON.stringify({
            is_generating: stopBtn !== null,
            send_button: sendBtn ? (sendBtn.disabled ? 'disabled' : 'enabled') : 'absent',
            model: modelEl ? modelEl.innerText.trim() : null,
            message_count: allMsgBlocks.length,
            url: window.location.href
        });
    })()
    """
    result = eval_in_renderer(ws, js, 98)
    try:
        return json.loads(result) if result else {}
    except:
        return {"error": str(result)}


def stop_generation(ws):
    """Click the stop button to halt generation."""
    js = """
    (function() {
        try {
            const stopBtn = document.querySelector('button[aria-label="Stop response"]');
            if (!stopBtn) return 'not-generating';
            stopBtn.click();
            return 'stopped';
        } catch(e) {
            return 'error: ' + e.message;
        }
    })()
    """
    result = eval_in_renderer(ws, js, 97)
    return {"success": result == "stopped", "result": result}


def read_interim(ws):
    """Read the last assistant message even if generation is ongoing."""
    js = """
    (function() {
        const stopBtn = document.querySelector('button[aria-label="Stop response"]');
        const isGenerating = stopBtn !== null;

        // Get all chat message text blocks
        const msgBlocks = document.querySelectorAll('[data-testid="chat-message-text"]');
        if (msgBlocks.length === 0) {
            // Fallback to container-based detection
            const container = document.querySelector('main');
            if (!container) return JSON.stringify({text: null, is_complete: !isGenerating, char_count: 0});
        }

        // Last message block is the most recent assistant response
        const lastBlock = msgBlocks[msgBlocks.length - 1];
        const text = lastBlock ? lastBlock.innerText.trim() : '';

        return JSON.stringify({
            text: text.substring(0, 10000),
            is_complete: !isGenerating,
            char_count: text.length
        });
    })()
    """
    result = eval_in_renderer(ws, js, 96)
    try:
        return (
            json.loads(result)
            if result
            else {"text": None, "is_complete": True, "char_count": 0}
        )
    except:
        return {
            "text": str(result),
            "is_complete": True,
            "char_count": len(str(result)),
        }


def wait_for_response(ws, timeout=120, poll_interval=2):
    """Wait for Claude to finish responding using stop-button detection.

    Uses debounce: requires stop button absent for 2 consecutive polls
    to avoid false positives from UI flicker.
    """
    start = time.time()
    seen_generating = False
    absent_count = 0  # debounce: consecutive polls with no stop button

    while time.time() - start < timeout:
        generating = is_generating(ws)

        if generating:
            seen_generating = True
            absent_count = 0
        elif seen_generating:
            absent_count += 1
            if absent_count >= 2:
                # Stop button absent for 2 consecutive polls — response is complete
                time.sleep(0.5)  # brief settle time for DOM update
                messages = get_messages(ws)
                if messages and messages[-1].get("role") == "assistant":
                    return messages[-1].get("text", "")
                return None

        # If we haven't seen generating yet, check if there's already a new assistant message
        if not seen_generating and time.time() - start > 5:
            messages = get_messages(ws)
            if messages and messages[-1].get("role") == "assistant":
                # Response appeared without us catching the generating state
                # (very fast response or we missed it)
                return messages[-1].get("text", "")

        time.sleep(poll_interval)

    return None


def list_connectors(ws):
    """List all MCP connectors and their enabled state."""
    script = """
        new Promise(async (resolve) => {
            const delay = ms => new Promise(r => setTimeout(r, ms));
            
            // Step 1: Click Toggle menu (input area menu)
            const toggleMenu = document.querySelector('button[aria-label="Toggle menu"]');
            if (!toggleMenu) { resolve({error: 'Toggle menu not found'}); return; }
            toggleMenu.click();
            await delay(500);
            
            // Step 2: Find and click Connectors
            const menuItems = document.querySelectorAll('[role="menuitem"]');
            let connectorsItem = null;
            for (const item of menuItems) {
                if (item.innerText?.includes('Connectors')) {
                    connectorsItem = item;
                    break;
                }
            }
            
            if (!connectorsItem) { 
                document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
                resolve({error: 'Connectors menu item not found'}); 
                return; 
            }
            
            connectorsItem.click();
            await delay(500);
            
            // Step 3: Get connector list
            const subMenuItems = document.querySelectorAll('[role="menuitemcheckbox"], [role="menuitem"]');
            const connectors = [];
            
            for (const item of subMenuItems) {
                const text = item.innerText?.trim() || '';
                const role = item.getAttribute('role');
                
                // Skip menu navigation items
                if (text.includes('Manage connectors') || text.includes('Add files') || 
                    text.includes('Add to project') || text.includes('Use style') || 
                    text === 'Connectors' || text.length > 50) {
                    continue;
                }
                
                // Parse name - format is "X\\n\\nname" for MCPs or just "name" for built-in
                let name = text;
                if (text.includes('\\n')) {
                    const parts = text.split('\\n').filter(p => p.trim());
                    name = parts[parts.length - 1] || text;
                }
                
                // Check enabled state
                const isChecked = item.getAttribute('aria-checked') === 'true';
                
                if (name) {
                    connectors.push({
                        name: name,
                        enabled: isChecked,
                        type: role === 'menuitemcheckbox' ? 'builtin' : 'mcp'
                    });
                }
            }
            
            // Close menu
            document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
            await delay(100);
            document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
            
            resolve({connectors: connectors});
        })
    """
    return exec_in_renderer(ws, script)


def toggle_connector(ws, connector_name, enable=None):
    """Toggle an MCP connector on/off."""
    escaped_name = json.dumps(connector_name.lower())
    enable_js = "null" if enable is None else ("true" if enable else "false")

    script = f"""
        new Promise(async (resolve) => {{
            const delay = ms => new Promise(r => setTimeout(r, ms));
            
            // Step 1: Click Toggle menu
            const toggleMenu = document.querySelector('button[aria-label="Toggle menu"]');
            if (!toggleMenu) {{ resolve({{error: 'Toggle menu not found'}}); return; }}
            toggleMenu.click();
            await delay(500);
            
            // Step 2: Click Connectors
            const menuItems = document.querySelectorAll('[role="menuitem"]');
            let connectorsItem = null;
            for (const item of menuItems) {{
                if (item.innerText?.includes('Connectors')) {{
                    connectorsItem = item;
                    break;
                }}
            }}
            if (!connectorsItem) {{ 
                document.body.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
                resolve({{error: 'Connectors not found'}}); 
                return; 
            }}
            connectorsItem.click();
            await delay(500);
            
            // Step 3: Find and click target connector
            const subItems = document.querySelectorAll('[role="menuitem"], [role="menuitemcheckbox"]');
            for (const item of subItems) {{
                let text = item.innerText?.toLowerCase() || '';
                // Parse name - format is "X\\n\\nname" for MCPs
                if (text.includes('\\n')) {{
                    const parts = text.split('\\n').filter(p => p.trim());
                    text = parts[parts.length - 1] || text;
                }}
                
                if (text.includes({escaped_name})) {{
                    const currentState = item.getAttribute('aria-checked') === 'true';
                    const targetState = {enable_js};
                    
                    if (targetState === null || currentState !== targetState) {{
                        item.click();
                        await delay(300);
                    }}
                    
                    // Close menus
                    document.body.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
                    await delay(100);
                    document.body.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
                    
                    resolve({{
                        connector: {escaped_name},
                        previousState: currentState,
                        newState: targetState === null ? !currentState : targetState,
                        action: (targetState === null || currentState !== targetState) ? 'toggled' : 'no-change'
                    }});
                    return;
                }}
            }}
            
            // Close and error
            document.body.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
            await delay(100);
            document.body.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
            resolve({{error: 'Connector not found', name: {escaped_name}}});
        }})
    """
    return exec_in_renderer(ws, script)


def reload_mcp_config(ws):
    """Reload MCP configuration via Developer menu."""
    js = """
    (function() {
        try {
            const electron = process.mainModule ? process.mainModule.require("electron") : global.require("electron");
            const { Menu } = electron;
            const menu = Menu.getApplicationMenu();
            if (!menu) return JSON.stringify({error: "No application menu"});

            const devMenu = menu.items.find(item => item.label === 'Developer');
            if (!devMenu || !devMenu.submenu) return JSON.stringify({error: "No Developer menu"});

            const reloadItem = devMenu.submenu.items.find(item =>
                item.label && item.label.includes('Reload MCP')
            );

            if (!reloadItem) return JSON.stringify({error: "No Reload MCP Configuration menu item"});

            reloadItem.click();

            return JSON.stringify({
                success: true,
                message: "MCP Configuration reloaded"
            });
        } catch(e) {
            return JSON.stringify({error: e.message});
        }
    })()
    """
    result = eval_in_main(ws, js)
    try:
        return json.loads(result) if result else {"error": "no result"}
    except:
        return {"error": "parse error", "raw": result}


def relaunch_desktop(timeout=30):
    """Kill and relaunch Claude Desktop, wait for debugger to be available."""
    import platform
    import os

    exe_path = get_claude_desktop_exe()
    if not exe_path:
        return {"success": False, "error": "Could not find Claude Desktop executable"}

    # Kill Claude Desktop processes (not Claude Code)
    if platform.system() == "Windows":
        # Kill only AnthropicClaude processes, not .local/bin/claude.exe (Claude Code)
        kill_cmd = '''powershell -Command "Get-Process -Name claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*AnthropicClaude*' } | Stop-Process -Force"'''
        subprocess.run(kill_cmd, shell=True, capture_output=True)
    else:
        # Linux/Mac - kill by path pattern
        subprocess.run("pkill -f 'AnthropicClaude'", shell=True, capture_output=True)

    time.sleep(2)

    # Launch Claude Desktop
    if platform.system() == "Windows":
        subprocess.Popen(
            [exe_path],
            creationflags=subprocess.DETACHED_PROCESS
            | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    else:
        subprocess.Popen([exe_path], start_new_session=True)

    # Poll for debugger availability
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{INSPECT_URL}/json", timeout=2)
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Claude Desktop relaunched and debugger is available",
                }
        except:
            pass
        time.sleep(1)

    return {
        "success": False,
        "error": "Claude Desktop relaunched but debugger not available. Please enable 'Main Process Debugger' in Claude Desktop: Menu > Help > Enable Main Process Debugger",
    }


# MCP Server Setup
server = Server("claude-desktop")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="claude_desktop_send",
            description="Send a message to Claude Desktop. Optionally wait for response.",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Message to send"},
                    "wait_for_response": {
                        "type": "boolean",
                        "description": "Wait for Claude's response",
                        "default": True,
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Max seconds to wait",
                        "default": 120,
                    },
                },
                "required": ["message"],
            },
        ),
        Tool(
            name="claude_desktop_read",
            description="Read messages from current Claude Desktop conversation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "last_n": {
                        "type": "integer",
                        "description": "Only return last N messages",
                        "default": 10,
                    }
                },
            },
        ),
        Tool(
            name="claude_desktop_info",
            description="Get current Claude Desktop conversation info (ID, URL, title).",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_list",
            description="List all conversations from Claude Desktop sidebar.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_navigate",
            description="Navigate to a specific conversation by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "Conversation ID to navigate to",
                    }
                },
                "required": ["chat_id"],
            },
        ),
        Tool(
            name="claude_desktop_new",
            description="Create a new conversation in Claude Desktop.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_search",
            description="Search conversations by title.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to match against conversation titles",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="claude_desktop_relaunch",
            description="Restart Claude Desktop. After relaunch, user may need to re-enable 'Main Process Debugger' in Help menu if debugger doesn't auto-connect.",
            inputSchema={
                "type": "object",
                "properties": {
                    "timeout": {
                        "type": "integer",
                        "description": "Max seconds to wait for debugger",
                        "default": 30,
                    }
                },
            },
        ),
        Tool(
            name="claude_desktop_status",
            description="Get Desktop status: is it generating? what model? message count? Lightweight, no side effects.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_stop",
            description="Stop the current response generation. Only works while Desktop is actively generating.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_read_interim",
            description="Read the current (possibly incomplete) assistant response. Works during and after generation.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_list_connectors",
            description="List all MCP connectors configured in Claude Desktop and their enabled/disabled state.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_toggle_connector",
            description="Enable or disable an MCP connector in Claude Desktop.",
            inputSchema={
                "type": "object",
                "properties": {
                    "connector_name": {
                        "type": "string",
                        "description": "Name of the connector to toggle (e.g., 'obsidian', 'github', 'memory')",
                    },
                    "enable": {
                        "type": "boolean",
                        "description": "True to enable, False to disable. Omit to toggle.",
                    },
                },
                "required": ["connector_name"],
            },
        ),
        Tool(
            name="claude_desktop_reload_mcp",
            description="Reload MCP configuration in Claude Desktop. Use after modifying claude_desktop_config.json to pick up new servers.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="claude_desktop_change_model",
            description="Change the Claude model. Available models: 'Opus 4.6', 'Opus 4.5', 'Sonnet 4.5', 'Sonnet 4', 'Haiku 4.5', 'Opus 3', 'Haiku 3.5'",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "Model name to switch to (e.g., 'Opus 4.6', 'Sonnet 4.5')",
                    },
                },
                "required": ["model_name"],
            },
        ),
        Tool(
            name="claude_desktop_list_models",
            description="List available Claude models and the currently selected model.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    # Handle relaunch separately - doesn't need existing connection
    if name == "claude_desktop_relaunch":
        timeout = arguments.get("timeout", 30)
        result = relaunch_desktop(timeout)
        return [TextContent(type="text", text=json.dumps(result))]

    ws = get_main_process_ws()
    if not ws:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "error": "Cannot connect to Claude Desktop. Enable 'Main Process Debugger' in Claude Desktop settings."
                    }
                ),
            )
        ]

    try:
        # Ensure debugger is attached
        attach_result = ensure_debugger_attached(ws)
        if isinstance(attach_result, dict) and attach_result.get("error"):
            return [TextContent(type="text", text=json.dumps(attach_result))]

        if name == "claude_desktop_send":
            message = arguments.get("message", "")
            wait = arguments.get("wait_for_response", True)
            timeout = arguments.get("timeout", 120)

            result = send_message(ws, message)
            if not result["success"]:
                return [TextContent(type="text", text=json.dumps(result))]

            if wait:
                response = wait_for_response(ws, timeout)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {"success": True, "sent": message, "response": response}
                        ),
                    )
                ]
            else:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {
                                "success": True,
                                "sent": message,
                                "response": None,
                                "note": "Message sent, not waiting for response",
                            }
                        ),
                    )
                ]

        elif name == "claude_desktop_read":
            last_n = arguments.get("last_n", 10)
            messages = get_messages(ws)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "messages": messages[-last_n:] if last_n else messages,
                            "total": len(messages),
                        }
                    ),
                )
            ]

        elif name == "claude_desktop_info":
            url = eval_in_renderer(ws, "window.location.href", 1)
            title = eval_in_renderer(ws, "document.title", 2)
            conv_id = None
            if url and "/chat/" in str(url):
                conv_id = str(url).split("/chat/")[-1].split("?")[0]
            status = get_status(ws)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "url": url,
                            "conversation_id": conv_id,
                            "title": title,
                            "model": status.get("model"),
                            "message_count": status.get("message_count", 0),
                            "is_generating": status.get("is_generating", False),
                        }
                    ),
                )
            ]

        elif name == "claude_desktop_list":
            convos = get_conversations(ws)
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"conversations": convos, "total": len(convos)}),
                )
            ]

        elif name == "claude_desktop_navigate":
            chat_id = arguments.get("chat_id", "")
            result = navigate_to_chat(ws, chat_id)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_new":
            result = create_new_chat(ws)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_search":
            query = arguments.get("query", "")
            matches = search_conversations(ws, query)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {"query": query, "matches": matches, "total": len(matches)}
                    ),
                )
            ]

        elif name == "claude_desktop_status":
            status = get_status(ws)
            return [TextContent(type="text", text=json.dumps(status))]

        elif name == "claude_desktop_stop":
            result = stop_generation(ws)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_read_interim":
            result = read_interim(ws)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_list_connectors":
            result = list_connectors(ws)
            # result is {connectors: [...]} or {error: "..."}
            if isinstance(result, dict) and "connectors" in result:
                connectors_list = result.get("connectors", [])
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {
                                "connectors": connectors_list,
                                "total": len(connectors_list),
                            }
                        ),
                    )
                ]
            else:
                # Error case - return as-is
                return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_toggle_connector":
            connector_name = arguments.get("connector_name", "")
            enable = arguments.get("enable")  # None means toggle
            result = toggle_connector(ws, connector_name, enable)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_reload_mcp":
            result = reload_mcp_config(ws)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_change_model":
            model_name = arguments.get("model_name", "")
            result = change_model(ws, model_name)
            return [TextContent(type="text", text=json.dumps(result))]

        elif name == "claude_desktop_list_models":
            result = get_available_models(ws)
            return [TextContent(type="text", text=json.dumps(result))]

        else:
            return [
                TextContent(
                    type="text", text=json.dumps({"error": f"Unknown tool: {name}"})
                )
            ]

    finally:
        ws.close()


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
