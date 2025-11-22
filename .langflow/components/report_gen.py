"""Generate status reports from project ledger and approval queue."""

import json
from datetime import datetime
from pathlib import Path

# Determine project root (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

LEDGER_PATH = PROJECT_ROOT / "memory" / "pm_ledger.jsonl"
QUEUE_PATH = PROJECT_ROOT / "memory" / "approval_queue.json"
OUTPUT_PATH = PROJECT_ROOT / "docs" / f"status_report_{datetime.now().strftime('%Y%m%d')}.md"

def load_ledger() -> list:
    """Load project ledger entries from JSONL file.

    Returns:
        List of ledger entry dictionaries
    """
    if not LEDGER_PATH.exists():
        return []
    with open(LEDGER_PATH) as f:
        return [json.loads(line.strip()) for line in f if line.strip()]


def load_queue() -> list:
    """Load approval queue from JSON file.

    Returns:
        List of queue item dictionaries
    """
    if not QUEUE_PATH.exists():
        return []
    with open(QUEUE_PATH) as f:
        return json.load(f).get("queue", [])

def generate_report() -> Path:
    """Generate a markdown status report from ledger and queue.

    Creates a dated report file in docs/ directory with:
    - Tasks awaiting approval
    - Recent activity from project ledger

    Returns:
        Path to the generated report file
    """
    ledger = load_ledger()
    queue = load_queue()
    report = []

    # Header
    report.append(f"# Status Report - {datetime.now().strftime('%Y-%m-%d')}\n")

    # Summarize approval queue
    report.append("## Tasks Awaiting Approval\n")
    if queue:
        for item in queue:
            task_type = item.get('task_type', 'task')
            desc = item.get('description', '')
            submitted = item.get('submitted_at', '-')
            status = item.get('status', '-')
            report.append(f"- **[{task_type}]** `{desc}` (Submitted: {submitted}) — *{status}*")
    else:
        report.append("- No pending approvals.\n")

    # Summarize activity from ledger (last 25 entries)
    report.append("\n## Recent Activity (Ledger)\n")
    if ledger:
        for entry in ledger[-25:]:
            ts = entry.get("timestamp", "-")
            evt = entry.get("event", "-")
            agt = entry.get("agent", "-")
            tid = entry.get("task_id", "-")
            det = entry.get("details", "")
            report.append(f"- `{ts}` [{evt}] ({agt}) task `{tid}` — {det}")
    else:
        report.append("- Ledger is empty.\n")

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write report
    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(report))

    print(f"[ReportGen] Report generated: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    generate_report()

