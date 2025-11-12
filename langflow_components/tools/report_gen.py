"""Report Generator Component for Langflow

Generates formatted reports from workflow data.
Supports multiple formats (Markdown, HTML, JSON) and templates.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from langflow.custom import Component
from langflow.io import MessageTextInput, Output, StrInput, DropdownInput, BoolInput, DataInput, MultilineInput
from langflow.schema import Data


class ReportGenerator(Component):
    display_name = "Report Generator"
    description = "Generate formatted reports from workflow data in multiple formats"
    documentation = "Create reports for builds, validations, and workflow results"
    icon = "📊"
    name = "ReportGenerator"

    inputs = [
        StrInput(
            name="report_title",
            display_name="Report Title",
            info="Title for the generated report",
            value="Barry Sharp Pro Mover - Build Report",
            required=True,
        ),
        DataInput(
            name="report_data",
            display_name="Report Data",
            info="Input data to include in report",
            required=False,
        ),
        MultilineInput(
            name="custom_content",
            display_name="Custom Content",
            info="Additional content to include in report",
            value="",
            required=False,
        ),
        DropdownInput(
            name="report_format",
            display_name="Report Format",
            info="Output format for the report",
            options=["markdown", "html", "json", "text"],
            value="markdown",
            required=True,
        ),
        StrInput(
            name="output_path",
            display_name="Output Path",
            info="File path to save the report (leave empty for return only)",
            value="",
            required=False,
        ),
        BoolInput(
            name="include_timestamp",
            display_name="Include Timestamp",
            info="Add generation timestamp to report",
            value=True,
        ),
        BoolInput(
            name="include_summary",
            display_name="Include Summary",
            info="Generate summary section from data",
            value=True,
        ),
        BoolInput(
            name="include_metadata",
            display_name="Include Metadata",
            info="Add system and process metadata",
            value=True,
        ),
    ]

    outputs = [
        Output(display_name="Report", name="report", method="generate_report"),
        Output(display_name="Report Data", name="data", method="generate_report"),
    ]

    def _generate_markdown(self, title: str, data: Dict, custom_content: str) -> str:
        """Generate Markdown formatted report"""
        lines = []

        # Title
        lines.append(f"# {title}")
        lines.append("")

        # Timestamp
        if self.include_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"**Generated:** {timestamp}")
            lines.append("")

        # Summary section
        if self.include_summary and data:
            lines.append("## Summary")
            lines.append("")

            # Extract key metrics
            if isinstance(data, dict):
                summary_items = []

                # Build results
                if "success" in data:
                    status = "✅ Success" if data["success"] else "❌ Failed"
                    summary_items.append(f"- **Status:** {status}")

                if "build_type" in data:
                    summary_items.append(f"- **Build Type:** {data['build_type']}")

                if "output_files" in data:
                    count = len(data.get("output_files", []))
                    summary_items.append(f"- **Output Files:** {count}")

                # File changes
                if "changes" in data:
                    changes = data.get("changes", [])
                    if isinstance(changes, list):
                        summary_items.append(f"- **Files Changed:** {len(changes)}")

                # Errors
                if "error" in data:
                    summary_items.append(f"- **Error:** {data['error']}")

                if summary_items:
                    lines.extend(summary_items)
                    lines.append("")

        # Custom content
        if custom_content:
            lines.append("## Details")
            lines.append("")
            lines.append(custom_content)
            lines.append("")

        # Data section
        if data:
            lines.append("## Data")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(data, indent=2))
            lines.append("```")
            lines.append("")

        # Metadata
        if self.include_metadata:
            lines.append("## Metadata")
            lines.append("")
            lines.append(f"- **Generated At:** {datetime.now().isoformat()}")
            lines.append(f"- **Report Format:** {self.report_format}")
            lines.append("")

        return "\n".join(lines)

    def _generate_html(self, title: str, data: Dict, custom_content: str) -> str:
        """Generate HTML formatted report"""
        html_parts = []

        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html>")
        html_parts.append("<head>")
        html_parts.append(f"    <title>{title}</title>")
        html_parts.append("    <style>")
        html_parts.append("        body { font-family: Arial, sans-serif; margin: 40px; }")
        html_parts.append("        h1 { color: #333; }")
        html_parts.append("        h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }")
        html_parts.append("        .timestamp { color: #999; font-style: italic; }")
        html_parts.append("        .success { color: green; }")
        html_parts.append("        .failed { color: red; }")
        html_parts.append("        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }")
        html_parts.append("        ul { line-height: 1.8; }")
        html_parts.append("    </style>")
        html_parts.append("</head>")
        html_parts.append("<body>")

        # Title
        html_parts.append(f"    <h1>{title}</h1>")

        # Timestamp
        if self.include_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html_parts.append(f'    <p class="timestamp">Generated: {timestamp}</p>')

        # Summary
        if self.include_summary and data:
            html_parts.append("    <h2>Summary</h2>")
            html_parts.append("    <ul>")

            if isinstance(data, dict):
                if "success" in data:
                    status_class = "success" if data["success"] else "failed"
                    status_text = "Success" if data["success"] else "Failed"
                    html_parts.append(f'        <li class="{status_class}"><strong>Status:</strong> {status_text}</li>')

                if "build_type" in data:
                    html_parts.append(f'        <li><strong>Build Type:</strong> {data["build_type"]}</li>')

                if "changes" in data and isinstance(data["changes"], list):
                    html_parts.append(f'        <li><strong>Files Changed:</strong> {len(data["changes"])}</li>')

            html_parts.append("    </ul>")

        # Custom content
        if custom_content:
            html_parts.append("    <h2>Details</h2>")
            html_parts.append(f"    <p>{custom_content.replace(chr(10), '<br>')}</p>")

        # Data
        if data:
            html_parts.append("    <h2>Data</h2>")
            html_parts.append("    <pre>")
            html_parts.append(json.dumps(data, indent=2))
            html_parts.append("    </pre>")

        # Metadata
        if self.include_metadata:
            html_parts.append("    <h2>Metadata</h2>")
            html_parts.append("    <ul>")
            html_parts.append(f"        <li><strong>Generated At:</strong> {datetime.now().isoformat()}</li>")
            html_parts.append(f"        <li><strong>Report Format:</strong> {self.report_format}</li>")
            html_parts.append("    </ul>")

        html_parts.append("</body>")
        html_parts.append("</html>")

        return "\n".join(html_parts)

    def _generate_json(self, title: str, data: Dict, custom_content: str) -> str:
        """Generate JSON formatted report"""
        report = {
            "title": title,
            "timestamp": datetime.now().isoformat() if self.include_timestamp else None,
            "custom_content": custom_content if custom_content else None,
            "data": data,
        }

        if self.include_metadata:
            report["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "format": self.report_format,
            }

        return json.dumps(report, indent=2)

    def _generate_text(self, title: str, data: Dict, custom_content: str) -> str:
        """Generate plain text formatted report"""
        lines = []

        # Title
        lines.append(title)
        lines.append("=" * len(title))
        lines.append("")

        # Timestamp
        if self.include_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"Generated: {timestamp}")
            lines.append("")

        # Summary
        if self.include_summary and data and isinstance(data, dict):
            lines.append("SUMMARY")
            lines.append("-" * 40)

            if "success" in data:
                status = "SUCCESS" if data["success"] else "FAILED"
                lines.append(f"Status: {status}")

            if "build_type" in data:
                lines.append(f"Build Type: {data['build_type']}")

            if "changes" in data and isinstance(data["changes"], list):
                lines.append(f"Files Changed: {len(data['changes'])}")

            lines.append("")

        # Custom content
        if custom_content:
            lines.append("DETAILS")
            lines.append("-" * 40)
            lines.append(custom_content)
            lines.append("")

        # Data
        if data:
            lines.append("DATA")
            lines.append("-" * 40)
            lines.append(json.dumps(data, indent=2))
            lines.append("")

        # Metadata
        if self.include_metadata:
            lines.append("METADATA")
            lines.append("-" * 40)
            lines.append(f"Generated At: {datetime.now().isoformat()}")
            lines.append(f"Report Format: {self.report_format}")
            lines.append("")

        return "\n".join(lines)

    def generate_report(self) -> Data:
        """Generate formatted report"""
        try:
            # Extract data
            data_dict = {}
            if self.report_data:
                if isinstance(self.report_data, Data):
                    data_dict = self.report_data.data if hasattr(self.report_data, 'data') else {}
                elif isinstance(self.report_data, dict):
                    data_dict = self.report_data

            # Generate report based on format
            generators = {
                "markdown": self._generate_markdown,
                "html": self._generate_html,
                "json": self._generate_json,
                "text": self._generate_text,
            }

            generator = generators.get(self.report_format, self._generate_markdown)
            report_content = generator(self.report_title, data_dict, self.custom_content)

            # Save to file if path specified
            saved_to = None
            if self.output_path:
                output_path = Path(self.output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(report_content)

                saved_to = str(output_path)
                self.log(f"Report saved to {output_path}")

            result_data = {
                "title": self.report_title,
                "format": self.report_format,
                "generated_at": datetime.now().isoformat(),
                "content_length": len(report_content),
                "saved_to": saved_to,
            }

            return Data(
                data=result_data,
                text=report_content,
            )

        except Exception as e:
            error_msg = f"Report generation error: {str(e)}"
            self.log(error_msg)
            return Data(
                data={
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                }
            )
