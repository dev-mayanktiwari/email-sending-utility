"""
Send history tracking using a local JSON file.
"""
import json
import os
from datetime import datetime

from config import HISTORY_FILE, DATA_DIR


def _ensure_file():
    """Create the history file if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)


def _read_all() -> list:
    """Read all history entries."""
    _ensure_file()
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _write_all(data: list):
    """Write all history entries."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_send(
    recipient_email: str,
    subject: str,
    success: bool,
    error: str | None = None,
    mode: str = "template",
    template_name: str | None = None,
) -> None:
    """
    Log a send attempt to history.

    Args:
        recipient_email: The recipient's email address
        subject: Email subject line
        success: Whether the send succeeded
        error: Error message if failed
        mode: "quick" or "template"
        template_name: Name of template used (if template mode)
    """
    history = _read_all()
    entry = {
        "recipient": recipient_email,
        "subject": subject,
        "success": success,
        "error": error,
        "mode": mode,
        "template": template_name,
        "timestamp": datetime.now().isoformat(),
    }
    history.insert(0, entry)  # Newest first

    # Keep max 500 entries
    if len(history) > 500:
        history = history[:500]

    _write_all(history)


def get_history(limit: int = 50) -> list:
    """Get recent send history, newest first."""
    history = _read_all()
    return history[:limit]


def get_history_stats() -> dict:
    """Get aggregate stats from history."""
    history = _read_all()
    total = len(history)
    successful = sum(1 for h in history if h.get("success"))
    failed = total - successful

    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "success_rate": round((successful / total * 100), 1) if total > 0 else 0,
    }


def clear_history() -> None:
    """Clear all history."""
    _write_all([])
