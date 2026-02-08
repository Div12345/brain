
import pytest
from .conftest import requires_desktop

# Apply the marker to all tests in this module
pytestmark = requires_desktop

def test_model_selector_exists(eval_renderer):
    """Verify the model selector dropdown is present."""
    js = "document.querySelector('[data-testid=\"model-selector-dropdown\"]') !== null"
    result = eval_renderer(js)
    assert result is True, "Model selector dropdown not found"

def test_prosemirror_editor_exists(eval_renderer):
    """Verify the ProseMirror editor is present."""
    js = "document.querySelector('.ProseMirror') !== null"
    result = eval_renderer(js)
    assert result is True, "ProseMirror editor not found"

def test_send_button_exists(eval_renderer):
    """Verify the send message button is present."""
    js = "document.querySelector('button[aria-label=\"Send message\"]') !== null"
    result = eval_renderer(js)
    assert result is True, "Send message button not found"

def test_file_upload_input_exists(eval_renderer):
    """Verify the file upload input is present."""
    js = "document.querySelector('#chat-input-file-upload-bottom') !== null"
    result = eval_renderer(js)
    assert result is True, "File upload input not found"

def test_sidebar_conversation_links_exist(eval_renderer):
    """Verify sidebar conversation links are present."""
    js = "document.querySelector('a[href*=\"/chat/\"]') !== null"
    result = eval_renderer(js)
    assert result is True, "No sidebar conversation links found. The conversation list might be empty."

def test_user_message_exists_in_history(eval_renderer):
    """
    Verify that user messages can be found. 
    Note: This test requires a conversation with at least one user message to be open.
    """
    js = "document.querySelector('[data-testid=\"user-message\"]') !== null"
    result = eval_renderer(js)
    assert result is True, "No user message found. This test needs a conversation with history."
