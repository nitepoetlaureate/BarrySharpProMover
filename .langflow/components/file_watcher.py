"""File watcher component for monitoring project files and tracking changes."""

import json
import signal
import sys
import threading
import time
from pathlib import Path

# LangFlow 1.4.x locates CustomComponent here ↓
try:
    from langflow.components.base.custom import CustomComponent
    LANGFLOW_AVAILABLE = True
except ImportError:
    # Fallback for standalone usage
    class CustomComponent:
        def __init__(self):
            pass
    LANGFLOW_AVAILABLE = False

# Configuration
WATCH_INTERVAL = 2  # seconds between scans

# Determine project root (3 levels up from this file: .langflow/components/file_watcher.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# List of directories to watch (relative to project root)
WATCH_DIRS = [
    PROJECT_ROOT / "assets" / "sprites",
    PROJECT_ROOT / "assets" / "dialogue",
    PROJECT_ROOT / "assets" / "music",
    PROJECT_ROOT / "scripts",
    PROJECT_ROOT / "docs"
]

APPROVAL_QUEUE_PATH = PROJECT_ROOT / "memory" / "approval_queue.json"

# Global flag for graceful shutdown
_running = True


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global _running
    print(f"\n[FileWatcher] Received signal {signum}, shutting down gracefully...")
    _running = False
    sys.exit(0)

def scan_files(dir_path: Path) -> set:
    """Recursively list all files in a directory.

    Args:
        dir_path: Path object pointing to directory to scan

    Returns:
        Set of Path objects for all files in directory tree
    """
    file_set = set()
    if not dir_path.exists():
        return file_set

    for file_path in dir_path.rglob("*"):
        if file_path.is_file():
            file_set.add(file_path)
    return file_set

def load_approval_queue() -> dict:
    """Load the approval queue from disk.

    Returns:
        Dictionary containing the approval queue
    """
    if not APPROVAL_QUEUE_PATH.exists():
        return {"queue": []}
    with open(APPROVAL_QUEUE_PATH, "r") as f:
        return json.load(f)

def update_approval_queue(new_file: Path) -> None:
    """Add a new file to the approval queue.

    Args:
        new_file: Path to the file that was added/modified
    """
    queue = load_approval_queue()
    file_str = str(new_file)

    # Prevent duplicate entries
    already_tracked = any(item.get("output_path") == file_str for item in queue["queue"])
    if not already_tracked:
        entry = {
            "task_id": f"auto-{int(time.time())}",
            "agent": "FileWatcher",
            "task_type": "file_event",
            "description": f"Detected file update: {new_file.name}",
            "input_path": file_str,
            "output_path": file_str,
            "status": "awaiting_approval",
            "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "comments": ""
        }
        queue["queue"].append(entry)

        # Ensure parent directory exists
        APPROVAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(APPROVAL_QUEUE_PATH, "w") as f:
            json.dump(queue, f, indent=2)

def watch() -> None:
    """Main file watching loop.

    Monitors configured directories for new files and adds them to approval queue.
    Runs until interrupted by signal.
    """
    global _running

    print("[FileWatcher] Starting up...")
    print(f"[FileWatcher] Monitoring {len(WATCH_DIRS)} directories")
    print(f"[FileWatcher] Scan interval: {WATCH_INTERVAL}s")

    file_state = {}
    for watch_dir in WATCH_DIRS:
        file_state[watch_dir] = scan_files(watch_dir)
        print(f"[FileWatcher] Tracking {watch_dir}: {len(file_state[watch_dir])} files")

    while _running:
        for watch_dir in WATCH_DIRS:
            if not watch_dir.exists():
                continue

            new_state = scan_files(watch_dir)
            added = new_state - file_state[watch_dir]

            for file_path in added:
                print(f"[FileWatcher] New file detected: {file_path}")
                update_approval_queue(file_path)

            file_state[watch_dir] = new_state

        time.sleep(WATCH_INTERVAL)

    print("[FileWatcher] Shutdown complete")

class FileWatcher(CustomComponent):
    """LangFlow component for monitoring project files.

    Watches configured directories for new or modified files and adds them
    to an approval queue for review before build integration.
    """

    display_name = "File Watcher"
    description = "Monitor project directories for file changes and track in approval queue"

    def __init__(self):
        super().__init__()

    def run(self) -> str:
        """Start the file watcher in a background thread.

        Returns:
            Status message indicating watcher has started
        """
        thread = threading.Thread(target=watch, daemon=True)
        thread.start()
        return f"File watcher started monitoring {len(WATCH_DIRS)} directories"


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("[FileWatcher] Press Ctrl+C to stop")

    t = threading.Thread(target=watch, daemon=True)
    t.start()

    # Block main thread until signal received
    try:
        while _running:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

