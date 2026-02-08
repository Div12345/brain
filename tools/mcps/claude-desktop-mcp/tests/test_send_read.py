
import pytest
import time
import json
from .conftest import requires_desktop

# Apply the marker to all tests in this module
pytestmark = [requires_desktop, pytest.mark.integration, pytest.mark.slow]

def get_messages(eval_renderer):
    """Helper to get all messages from conversation, adapted from server.py."""
    js = """
    (function() {
        const container = document.querySelector('.flex-1.flex.flex-col.px-4.max-w-3xl');
        if (!container) return '[]';
        const messages = [];
        Array.from(container.children).forEach((child, i) => {
            // Check if it's a message block, not a loader or other element
            const hasUserMsg = child.querySelector('[data-testid="user-message"]');
            const hasAssistantMsg = child.querySelector('.prose'); // A bit generic, but works for assistant responses
            
            if (hasUserMsg || hasAssistantMsg) {
                const text = (child.innerText || '').trim();
                if (text) {
                    messages.push({
                        index: i,
                        role: hasUserMsg ? 'user' : 'assistant',
                        text: text.substring(0, 2000)
                    });
                }
            }
        });
        return JSON.stringify(messages);
    })()
    """
    result = eval_renderer(js)
    try:
        return json.loads(result) if isinstance(result, str) else []
    except (json.JSONDecodeError, TypeError):
        return []

def test_send_and_read_cycle(eval_renderer):
    """
    Tests the full cycle of sending a message, waiting for the response,
    and reading the result.
    """
    prompt = "What is 2+2?"
    escaped_prompt = json.dumps(prompt)

    # 1. Get initial message count
    initial_messages = get_messages(eval_renderer)
    initial_message_count = len(initial_messages)

    # 2. Input the prompt into ProseMirror
    js_input = f"""
    (function() {{
        const pm = document.querySelector('.ProseMirror');
        if (!pm) return 'no-prosemirror';
        pm.focus();
        pm.innerHTML = '<p>' + {escaped_prompt} + '</p>';
        pm.dispatchEvent(new InputEvent('input', {{ bubbles: true, cancelable: true }}));
        return 'text-set';
    }})()
    """
    result = eval_renderer(js_input)
    assert result == 'text-set', "Failed to set text in ProseMirror editor"
    time.sleep(0.5)

    # 3. Click the send button
    js_send = """
    (function() {
        const btn = document.querySelector('button[aria-label="Send message"]');
        if (!btn) return 'no-send-button';
        if (btn.disabled) return 'button-disabled';
        btn.click();
        return 'sent';
    })()
    """
    result = eval_renderer(js_send)
    assert result == 'sent', "Failed to click send button"

    # 4. Wait for generation to start (stop button appears)
    generation_started = False
    for _ in range(10): # Max 5 seconds wait
        stop_button_exists = eval_renderer("document.querySelector('button[aria-label=\"Stop response\"]') !== null")
        if stop_button_exists:
            generation_started = True
            break
        time.sleep(0.5)
    assert generation_started, "Generation did not start (stop button never appeared)"

    # 5. Wait for generation to finish (stop button disappears)
    generation_finished = False
    for _ in range(60): # Max 30 seconds wait
        stop_button_exists = eval_renderer("document.querySelector('button[aria-label=\"Stop response\"]') !== null")
        if not stop_button_exists:
            generation_finished = True
            break
        time.sleep(0.5)
    assert generation_finished, "Generation did not finish in time (stop button did not disappear)"
    
    # Add a small buffer for UI to fully update after stop button disappears
    time.sleep(1)

    # 6. Get final messages and verify
    final_messages = get_messages(eval_renderer)
    assert len(final_messages) > initial_message_count, "Message count did not increase"

    # 7. Check the last message
    last_message = final_messages[-1]
    assert last_message['role'] == 'assistant', "Last message was not from the assistant"
    assert "4" in last_message['text'], f"Assistant response did not contain '4'. Got: {last_message['text']}"
