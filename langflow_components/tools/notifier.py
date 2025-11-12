"""Notifier Component for Langflow

Sends notifications through various channels (console, file, webhook).
Supports severity levels, formatting, and notification throttling.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from langflow.custom import Component
from langflow.io import MessageTextInput, Output, StrInput, DropdownInput, BoolInput, IntInput, MultilineInput
from langflow.schema import Data


class Notifier(Component):
    display_name = "Notifier"
    description = "Send notifications through multiple channels with formatting and throttling"
    documentation = "Multi-channel notification system for workflow events"
    icon = "📢"
    name = "Notifier"

    inputs = [
        StrInput(
            name="title",
            display_name="Notification Title",
            info="Title or subject of the notification",
            value="Barry Sharp Pro Mover",
            required=True,
        ),
        MultilineInput(
            name="message",
            display_name="Message",
            info="Notification message body",
            value="",
            required=True,
        ),
        DropdownInput(
            name="severity",
            display_name="Severity Level",
            info="Notification severity/priority",
            options=["info", "success", "warning", "error", "critical"],
            value="info",
            required=True,
        ),
        DropdownInput(
            name="channel",
            display_name="Notification Channel",
            info="Where to send the notification",
            options=["console", "file", "webhook", "all"],
            value="console",
            required=True,
        ),
        StrInput(
            name="log_file",
            display_name="Log File Path",
            info="File path for file-based notifications",
            value="memory/automation.log",
            required=False,
        ),
        StrInput(
            name="webhook_url",
            display_name="Webhook URL",
            info="HTTP endpoint for webhook notifications",
            value="",
            required=False,
        ),
        BoolInput(
            name="include_timestamp",
            display_name="Include Timestamp",
            info="Add timestamp to notifications",
            value=True,
        ),
        BoolInput(
            name="include_metadata",
            display_name="Include Metadata",
            info="Add system metadata to notifications",
            value=False,
        ),
        IntInput(
            name="throttle_seconds",
            display_name="Throttle (seconds)",
            info="Minimum seconds between notifications (0 = no throttle)",
            value=0,
            required=False,
        ),
    ]

    outputs = [
        Output(display_name="Notification Result", name="result", method="send_notification"),
        Output(display_name="Status", name="status", method="send_notification"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_notification_time: Dict[str, float] = {}

    def _get_severity_icon(self, severity: str) -> str:
        """Get emoji icon for severity level"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨",
        }
        return icons.get(severity, "📝")

    def _get_severity_color(self, severity: str) -> str:
        """Get ANSI color code for severity"""
        colors = {
            "info": "\033[94m",      # Blue
            "success": "\033[92m",    # Green
            "warning": "\033[93m",    # Yellow
            "error": "\033[91m",      # Red
            "critical": "\033[95m",   # Magenta
        }
        return colors.get(severity, "\033[0m")

    def _format_message(self, title: str, message: str, severity: str) -> str:
        """Format notification message with optional timestamp and metadata"""
        parts = []

        # Add timestamp if enabled
        if self.include_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            parts.append(f"[{timestamp}]")

        # Add severity icon and label
        icon = self._get_severity_icon(severity)
        parts.append(f"{icon} [{severity.upper()}]")

        # Add title
        parts.append(title)

        header = " ".join(parts)

        # Build full message
        formatted = f"{header}\n{message}"

        # Add metadata if enabled
        if self.include_metadata:
            metadata = {
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
                "pid": os.getpid(),
            }
            formatted += f"\n\nMetadata: {json.dumps(metadata, indent=2)}"

        return formatted

    def _should_throttle(self, key: str) -> bool:
        """Check if notification should be throttled"""
        if self.throttle_seconds <= 0:
            return False

        import time
        current_time = time.time()
        last_time = self._last_notification_time.get(key, 0)

        if current_time - last_time < self.throttle_seconds:
            return True

        self._last_notification_time[key] = current_time
        return False

    def _send_console(self, formatted_message: str) -> bool:
        """Send notification to console"""
        try:
            color = self._get_severity_color(self.severity)
            reset = "\033[0m"
            print(f"\n{color}{formatted_message}{reset}\n")
            return True
        except Exception as e:
            self.log(f"Console notification failed: {e}")
            return False

    def _send_file(self, formatted_message: str) -> bool:
        """Send notification to log file"""
        try:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            with open(log_path, "a", encoding="utf-8") as f:
                f.write(formatted_message + "\n" + "="*80 + "\n")

            self.log(f"Notification written to {log_path}")
            return True
        except Exception as e:
            self.log(f"File notification failed: {e}")
            return False

    def _send_webhook(self, formatted_message: str) -> bool:
        """Send notification via webhook"""
        if not self.webhook_url:
            self.log("Webhook URL not configured, skipping webhook notification")
            return False

        try:
            import requests

            payload = {
                "title": self.title,
                "message": self.message,
                "severity": self.severity,
                "timestamp": datetime.now().isoformat(),
                "formatted": formatted_message,
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            response.raise_for_status()
            self.log(f"Webhook notification sent: {response.status_code}")
            return True

        except ImportError:
            self.log("Requests library not available for webhook notifications")
            return False
        except Exception as e:
            self.log(f"Webhook notification failed: {e}")
            return False

    def send_notification(self) -> Data:
        """Send notification through configured channels"""
        try:
            # Check throttling
            throttle_key = f"{self.severity}:{self.title}"
            if self._should_throttle(throttle_key):
                return Data(
                    data={
                        "sent": False,
                        "throttled": True,
                        "message": "Notification throttled"
                    },
                    text="Notification throttled"
                )

            # Format message
            formatted_message = self._format_message(self.title, self.message, self.severity)

            # Send through configured channels
            results = {}

            if self.channel in ["console", "all"]:
                results["console"] = self._send_console(formatted_message)

            if self.channel in ["file", "all"]:
                results["file"] = self._send_file(formatted_message)

            if self.channel in ["webhook", "all"]:
                results["webhook"] = self._send_webhook(formatted_message)

            # Determine overall success
            success = any(results.values()) if results else False

            result_data = {
                "sent": success,
                "throttled": False,
                "severity": self.severity,
                "title": self.title,
                "channels": results,
                "timestamp": datetime.now().isoformat(),
            }

            status_text = f"Notification sent via {self.channel}: {self.title}"
            self.log(status_text)

            return Data(
                data=result_data,
                text=status_text,
            )

        except Exception as e:
            error_msg = f"Notification error: {str(e)}"
            self.log(error_msg)
            return Data(
                data={
                    "sent": False,
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                }
            )
