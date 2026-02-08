
import pytest
from .conftest import requires_desktop

# Apply the marker to all tests in this module
pytestmark = requires_desktop

def test_idle_status_buttons(eval_renderer):
    """
    When idle, the 'Send message' button should be present
    and the 'Stop response' button should not be.
    """
    # Check for send button
    send_button_exists = eval_renderer("document.querySelector('button[aria-label=\"Send message\"]') !== null")
    assert send_button_exists is True, "Send message button should exist when idle"

    # Check for stop button
    stop_button_exists = eval_renderer("document.querySelector('button[aria-label=\"Stop response\"]') !== null")
    assert stop_button_exists is False, "Stop response button should not exist when idle"
