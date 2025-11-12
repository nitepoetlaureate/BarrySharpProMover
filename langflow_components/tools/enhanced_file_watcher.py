"""Enhanced File Watcher Component for Langflow

Monitors file system for changes and triggers workflow actions.
Supports filtering by file patterns, debouncing, and event types.
"""

import os
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from langflow.custom import Component
from langflow.io import MessageTextInput, Output, StrInput, MultilineInput, BoolInput, IntInput
from langflow.schema import Data


class EnhancedFileWatcher(Component):
    display_name = "Enhanced File Watcher"
    description = "Monitor directories for file changes with filtering and debouncing"
    documentation = "Monitor file system changes and trigger workflow actions"
    icon = "👁️"
    name = "EnhancedFileWatcher"

    inputs = [
        StrInput(
            name="watch_path",
            display_name="Watch Path",
            info="Directory or file path to monitor",
            value="assets/",
            required=True,
        ),
        MultilineInput(
            name="include_patterns",
            display_name="Include Patterns",
            info="Glob patterns to include (one per line, e.g., *.png)",
            value="*.png\n*.gbsproj\n*.json",
            required=False,
        ),
        MultilineInput(
            name="exclude_patterns",
            display_name="Exclude Patterns",
            info="Glob patterns to exclude (one per line)",
            value="__pycache__\n*.pyc\n.git",
            required=False,
        ),
        BoolInput(
            name="watch_created",
            display_name="Watch Created",
            info="Monitor file creation events",
            value=True,
        ),
        BoolInput(
            name="watch_modified",
            display_name="Watch Modified",
            info="Monitor file modification events",
            value=True,
        ),
        BoolInput(
            name="watch_deleted",
            display_name="Watch Deleted",
            info="Monitor file deletion events",
            value=False,
        ),
        IntInput(
            name="debounce_seconds",
            display_name="Debounce (seconds)",
            info="Wait time before triggering after last change",
            value=2,
            required=True,
        ),
        BoolInput(
            name="recursive",
            display_name="Recursive",
            info="Watch subdirectories recursively",
            value=True,
        ),
        BoolInput(
            name="compute_hash",
            display_name="Compute File Hash",
            info="Calculate MD5 hash of changed files",
            value=False,
        ),
    ]

    outputs = [
        Output(display_name="Changes", name="changes", method="scan_for_changes"),
        Output(display_name="Change Data", name="data", method="scan_for_changes"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_states: Dict[str, Dict] = {}
        self._last_scan_time = 0

    def _matches_pattern(self, filepath: Path, patterns: List[str]) -> bool:
        """Check if filepath matches any of the given patterns"""
        if not patterns:
            return False

        for pattern in patterns:
            pattern = pattern.strip()
            if not pattern:
                continue

            # Simple pattern matching (extend for more complex patterns)
            if pattern.startswith("*"):
                if str(filepath).endswith(pattern[1:]):
                    return True
            elif pattern.endswith("*"):
                if str(filepath).startswith(pattern[:-1]):
                    return True
            elif pattern in str(filepath):
                return True

        return False

    def _should_include_file(self, filepath: Path) -> bool:
        """Determine if file should be monitored based on patterns"""
        # Parse patterns
        include_list = [p.strip() for p in self.include_patterns.split("\n") if p.strip()]
        exclude_list = [p.strip() for p in self.exclude_patterns.split("\n") if p.strip()]

        # Check exclusions first
        if self._matches_pattern(filepath, exclude_list):
            return False

        # If no include patterns, include everything (except excluded)
        if not include_list:
            return True

        # Check inclusions
        return self._matches_pattern(filepath, include_list)

    def _get_file_hash(self, filepath: Path) -> Optional[str]:
        """Calculate MD5 hash of file contents"""
        if not self.compute_hash or not filepath.exists():
            return None

        try:
            hasher = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            self.log(f"Error computing hash for {filepath}: {e}")
            return None

    def _scan_directory(self) -> List[Dict]:
        """Scan directory for changes since last scan"""
        changes = []
        watch_path = Path(self.watch_path)

        if not watch_path.exists():
            self.log(f"Watch path does not exist: {watch_path}")
            return []

        # Determine files to check
        if watch_path.is_file():
            files_to_check = [watch_path]
        else:
            if self.recursive:
                files_to_check = list(watch_path.rglob("*"))
            else:
                files_to_check = list(watch_path.glob("*"))

        # Filter to only files (not directories)
        files_to_check = [f for f in files_to_check if f.is_file()]

        current_files = set()

        for filepath in files_to_check:
            if not self._should_include_file(filepath):
                continue

            current_files.add(str(filepath))

            try:
                stat = filepath.stat()
                mtime = stat.st_mtime
                size = stat.st_size
                file_hash = self._get_file_hash(filepath)

                file_key = str(filepath)

                # Check if file is new
                if file_key not in self._file_states:
                    if self.watch_created:
                        change_event = {
                            "event": "created",
                            "path": str(filepath),
                            "filename": filepath.name,
                            "size": size,
                            "modified_time": datetime.fromtimestamp(mtime).isoformat(),
                            "hash": file_hash,
                        }
                        changes.append(change_event)
                        self.log(f"File created: {filepath}")

                    self._file_states[file_key] = {
                        "mtime": mtime,
                        "size": size,
                        "hash": file_hash,
                    }
                # Check if file was modified
                elif self.watch_modified:
                    prev_state = self._file_states[file_key]

                    # Check if actually changed
                    if mtime > prev_state["mtime"] or size != prev_state["size"]:
                        # Verify change with hash if enabled
                        if self.compute_hash and file_hash == prev_state.get("hash"):
                            # Hash unchanged, skip
                            continue

                        change_event = {
                            "event": "modified",
                            "path": str(filepath),
                            "filename": filepath.name,
                            "size": size,
                            "size_delta": size - prev_state["size"],
                            "modified_time": datetime.fromtimestamp(mtime).isoformat(),
                            "hash": file_hash,
                            "previous_hash": prev_state.get("hash"),
                        }
                        changes.append(change_event)
                        self.log(f"File modified: {filepath}")

                        self._file_states[file_key] = {
                            "mtime": mtime,
                            "size": size,
                            "hash": file_hash,
                        }

            except Exception as e:
                self.log(f"Error processing {filepath}: {e}")

        # Check for deleted files
        if self.watch_deleted:
            deleted_files = set(self._file_states.keys()) - current_files
            for deleted_path in deleted_files:
                change_event = {
                    "event": "deleted",
                    "path": deleted_path,
                    "filename": Path(deleted_path).name,
                }
                changes.append(change_event)
                self.log(f"File deleted: {deleted_path}")
                del self._file_states[deleted_path]

        return changes

    def scan_for_changes(self) -> Data:
        """Scan for file system changes"""
        try:
            current_time = time.time()

            # Implement debouncing
            if current_time - self._last_scan_time < self.debounce_seconds:
                return Data(
                    data={
                        "changes": [],
                        "debounced": True,
                        "message": "Scan debounced"
                    }
                )

            self._last_scan_time = current_time

            # Scan for changes
            changes = self._scan_directory()

            result_data = {
                "changes": changes,
                "count": len(changes),
                "watch_path": str(self.watch_path),
                "timestamp": datetime.now().isoformat(),
                "debounced": False,
            }

            if changes:
                summary = f"Detected {len(changes)} change(s) in {self.watch_path}"
                self.log(summary)
            else:
                summary = f"No changes detected in {self.watch_path}"

            return Data(
                data=result_data,
                text=summary,
            )

        except Exception as e:
            error_msg = f"File watcher error: {str(e)}"
            self.log(error_msg)
            return Data(
                data={
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                }
            )
