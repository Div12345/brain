"""Desktop notification module - sends task responses back to Claude Desktop."""

import json
import sys
import logging
from pathlib import Path
from typing import TYPE_CHECKING

# Import from parent server.py
sys.path.insert(0, str(Path(__file__).parent.parent))
from server import get_main_process_ws as get_claude_ws, send_message

if TYPE_CHECKING:
    from .schema import Response

logger = logging.getLogger(__name__)


def notify_desktop(response: "Response") -> bool:
    """
    Notify Claude Desktop that a response is ready via DevTools.

    Args:
        response: Response object containing task_id, status, result, and error

    Returns:
        True if notification sent successfully, False if Desktop not connected
        or any error occurred

    Examples:
        >>> from bridge.schema import Response, ResponseError
        >>> resp = Response(
        ...     task_id="task-123",
        ...     status="success",
        ...     result={"output": "done"}
        ... )
        >>> success = notify_desktop(resp)
    """
    ws = None
    try:
        ws = get_claude_ws()
        if not ws:
            logger.warning("Claude Desktop not connected via DevTools")
            return False

        # Build formatted notification
        error_info = "None"
        if response.error:
            error_info = f"{response.error.code}: {response.error.message}"
            if response.error.details:
                error_info += f" ({response.error.details})"

        result_info = "N/A"
        if response.result:
            try:
                result_info = json.dumps(response.result)
            except (TypeError, ValueError) as e:
                logger.warning(f"Failed to serialize result: {e}")
                result_info = str(response.result)

        notification = f"""[BRIDGE RESPONSE]
Task ID: {response.task_id}
Status: {response.status}
Result: {result_info}
Error: {error_info}
Completed: {response.completed_at.isoformat() if response.completed_at else 'N/A'}"""

        # Send via DOM
        result = send_message(ws, notification)
        if result and result.get("success"):
            logger.info(f"Notification sent for task {response.task_id}")
            return True
        else:
            error_msg = result.get("error", "Unknown error") if result else "send_message returned None"
            logger.error(f"Failed to send notification: {error_msg}")
            return False

    except Exception as e:
        logger.exception(f"Exception while notifying Desktop: {e}")
        return False

    finally:
        if ws:
            try:
                ws.close()
            except Exception as e:
                logger.debug(f"Error closing WebSocket: {e}")
