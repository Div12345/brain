
import pytest
import json
import websocket
import requests

# --- Copied from server.py ---

def get_main_process_ws():
    """Connect to Claude Desktop main process via Node inspector."""
    try:
        response = requests.get("http://127.0.0.1:9229/json", timeout=1)
        targets = response.json()
        for target in targets:
            if target.get("type") == "node":
                ws_url = target.get("webSocketDebuggerUrl")
                if ws_url:
                    return websocket.create_connection(ws_url, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None
    except Exception:
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

def _eval_in_renderer_raw(ws, expression, cmd_id=1):
    """
    Helper to evaluate JS in renderer and return the raw JSON string result.
    This is needed because the final value can be a stringified JSON object.
    """
    escaped_expr = json.dumps(expression)
    js = f"""
    (async function() {{
        try {{
            const electron = process.mainModule ? process.mainModule.require("electron") : global.require("electron");
            const {{ webContents }} = electron;
            const all = webContents.getAllWebContents();
            const claudeWc = all.find(wc => wc.getURL().includes("claude.ai"));
            if (!claudeWc) return JSON.stringify({{ "error": "No claude.ai webContents found" }});
            if (!claudeWc.debugger.isAttached()) {{
                claudeWc.debugger.attach("1.3");
            }}
            const result = await claudeWc.debugger.sendCommand("Runtime.evaluate", {{
                expression: {escaped_expr},
                returnByValue: true
            }});
            return JSON.stringify(result);
        }} catch(e) {{
            return JSON.stringify({{ "error": e.message }});
        }}
    }})()
    """
    result = send_inspector_cmd(ws, "Runtime.evaluate", {
        "expression": js,
        "returnByValue": True,
        "awaitPromise": True
    }, cmd_id)
    return result.get("result", {}).get("result", {}).get("value")

# --- Pytest Fixtures ---

# Marker for tests that require a live desktop connection
requires_desktop = pytest.mark.skipif(
    get_main_process_ws() is None,
    reason="Claude Desktop with debugger on port 9229 is not available"
)

@pytest.fixture(scope="module")
def ws_connection():
    """Fixture to provide a websocket connection to the Claude Desktop main process."""
    ws = get_main_process_ws()
    if ws is None:
        pytest.skip("Could not connect to Claude Desktop. Is it running with the debugger enabled?")
    
    # Ensure the debugger is attached to the renderer
    init_js = """
    (function() {
        try {
            const electron = process.mainModule ? process.mainModule.require("electron") : global.require("electron");
            const { webContents } = electron;
            const all = webContents.getAllWebContents();
            const claudeWc = all.find(wc => wc.getURL().includes("claude.ai"));
            if (claudeWc && !claudeWc.debugger.isAttached()) {
                claudeWc.debugger.attach("1.3");
            }
            return claudeWc ? claudeWc.getURL() : null;
        } catch(e) {
            return e.message;
        }
    })()
    """
    send_inspector_cmd(ws, "Runtime.evaluate", {"expression": init_js, "returnByValue": True, "awaitPromise": True}, 999)

    yield ws
    ws.close()

@pytest.fixture(scope="function")
def eval_renderer(ws_connection):
    """Fixture to provide a function that evaluates JS in the renderer process."""
    def _evaluator(expression: str, cmd_id: int = 1):
        raw_result_str = _eval_in_renderer_raw(ws_connection, expression, cmd_id)
        
        if not raw_result_str:
            return {"error": "No result from renderer."}

        try:
            # First level of parsing (the result of the main process eval)
            parsed_outer = json.loads(raw_result_str)
        except json.JSONDecodeError:
            return {"error": "Outer result is not valid JSON.", "raw": raw_result_str}

        # Check for errors from the CDP command itself
        if "error" in parsed_outer:
            return parsed_outer

        # The actual result of the renderer's Runtime.evaluate is often in a nested 'value' field.
        renderer_result = parsed_outer.get("result", {})
        if "value" in renderer_result:
            return renderer_result["value"]
        
        # Handle cases where the result is an exception in the renderer
        if "exceptionDetails" in renderer_result:
            return {"error": "JavaScript exception", "details": renderer_result["exceptionDetails"]}

        return renderer_result

    return _evaluator
