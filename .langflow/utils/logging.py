"""Shared logging utilities for LangFlow components.

Provides centralized logging functionality for project ledger and event tracking.
"""

import datetime
import json
from pathlib import Path
from typing import Any, Dict


# Determine project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
LEDGER_PATH = PROJECT_ROOT / "memory" / "pm_ledger.jsonl"


def log_to_ledger(
    event_type: str,
    agent: str,
    task_id: str,
    details: Dict[str, Any],
    ledger_path: Path | None = None
) -> None:
    """Log an event to the project ledger.

    Writes a JSONL entry to the project ledger file with timestamp and event details.
    Creates the ledger directory if it doesn't exist.

    Args:
        event_type: Type of event (e.g., 'build_started', 'validation_complete')
        agent: Name of the agent/component logging the event
        task_id: Unique identifier for the task
        details: Dictionary containing event-specific details
        ledger_path: Optional custom ledger path (defaults to PROJECT_ROOT/memory/pm_ledger.jsonl)

    Example:
        >>> log_to_ledger(
        ...     event_type="build_started",
        ...     agent="ci_cd_pipeline",
        ...     task_id="build-001",
        ...     details={"target": "rom", "platform": "linux"}
        ... )
    """
    if ledger_path is None:
        ledger_path = LEDGER_PATH

    # Ensure directory exists
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    # Create log entry
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event_type,
        "agent": agent,
        "task_id": task_id,
        "details": details
    }

    # Append to JSONL file
    with open(ledger_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def load_ledger(ledger_path: Path | None = None) -> list:
    """Load all entries from the project ledger.

    Args:
        ledger_path: Optional custom ledger path

    Returns:
        List of ledger entry dictionaries, ordered by timestamp
    """
    if ledger_path is None:
        ledger_path = LEDGER_PATH

    if not ledger_path.exists():
        return []

    entries = []
    with open(ledger_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    # Skip malformed lines
                    continue

    return entries


def get_recent_events(
    event_type: str | None = None,
    agent: str | None = None,
    limit: int = 25,
    ledger_path: Path | None = None
) -> list:
    """Get recent events from the ledger, optionally filtered.

    Args:
        event_type: Filter by event type (optional)
        agent: Filter by agent name (optional)
        limit: Maximum number of events to return (default: 25)
        ledger_path: Optional custom ledger path

    Returns:
        List of matching ledger entries, most recent first

    Example:
        >>> # Get last 10 build events
        >>> builds = get_recent_events(event_type="build_complete", limit=10)
        >>>
        >>> # Get last 25 events from ci_cd_pipeline
        >>> pipeline_events = get_recent_events(agent="ci_cd_pipeline")
    """
    entries = load_ledger(ledger_path)

    # Filter by event type if specified
    if event_type:
        entries = [e for e in entries if e.get("event") == event_type]

    # Filter by agent if specified
    if agent:
        entries = [e for e in entries if e.get("agent") == agent]

    # Return most recent first, up to limit
    return entries[-limit:][::-1]


def clear_ledger(ledger_path: Path | None = None) -> None:
    """Clear all entries from the ledger.

    **WARNING:** This permanently deletes all ledger history.
    Use with caution, typically only for testing.

    Args:
        ledger_path: Optional custom ledger path
    """
    if ledger_path is None:
        ledger_path = LEDGER_PATH

    if ledger_path.exists():
        ledger_path.unlink()
