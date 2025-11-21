# Barry Sharp Pro Mover - API Documentation

**Version:** 0.1.0
**Last Updated:** 2025-11-21

---

## Table of Contents

1. [Overview](#overview)
2. [LangFlow Components](#langflow-components)
3. [Validation Scripts](#validation-scripts)
4. [Shared Utilities](#shared-utilities)
5. [Project Memory APIs](#project-memory-apis)
6. [Build System](#build-system)
7. [Testing Utilities](#testing-utilities)

---

## Overview

This document provides complete API documentation for all custom components, scripts, and utilities in the Barry Sharp Pro Mover project.

### Component Base Class

All LangFlow components inherit from:

```python
from langflow.components.base.custom import CustomComponent
```

**Required Methods:**
- `build(**kwargs) -> str`: Main execution method, returns result as string

**Optional Attributes:**
- `display_name: str`: Human-readable component name
- `description: str`: Short description for LangFlow UI

---

## LangFlow Components

### GBStudioBuild

**File:** `.langflow/components/gbstudio_build.py`

Compiles a GB Studio project into a Game Boy ROM.

#### Class Definition

```python
class GBStudioBuild(CustomComponent):
    """Build GB Studio project to ROM."""

    display_name = "GB Studio Build"
    description = "Compile GB Studio project to Game Boy ROM"
```

#### Method: build()

```python
def build(
    project_dir: str = ".",
    target: str = "rom",
    launch_emulator: bool = False,
    gb_studio_cli_path: str | None = None,
    code: str | None = None,
    **_: object
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_dir` | `str` | `"."` | Path to GB Studio project directory |
| `target` | `str` | `"rom"` | Build target: `"rom"`, `"web"`, or `"all"` |
| `launch_emulator` | `bool` | `False` | Launch ROM in emulator after build |
| `gb_studio_cli_path` | `str \| None` | `None` | Custom path to GB Studio CLI |
| `code` | `str \| None` | `None` | LangFlow compatibility (ignored) |
| `**_` | `object` | - | Future-proof kwargs |

**Returns:** `str` - Path to built ROM file

**Raises:**
- `RuntimeError`: If GB Studio CLI not found
- `RuntimeError`: If build fails
- `RuntimeError`: If ROM not produced

**Example Usage:**

```python
from .langflow.components.gbstudio_build import GBStudioBuild

builder = GBStudioBuild()

# Basic ROM build
rom_path = builder.build(
    project_dir="/path/to/project",
    target="rom"
)
print(f"ROM created: {rom_path}")

# Build and launch in emulator
rom_path = builder.build(
    project_dir="/path/to/project",
    target="rom",
    launch_emulator=True
)

# Build web target
web_path = builder.build(
    project_dir="/path/to/project",
    target="web"
)
```

**Output Directory Structure:**
```
dist/
└── YYYYMMDD_HHMMSS/
    ├── rom.gb          # ROM build
    └── web/            # Web build
        ├── index.html
        └── ...
```

---

### FileWatcher

**File:** `.langflow/components/file_watcher.py`

Monitors project directories for file changes.

#### Class Definition

```python
class FileWatcher(CustomComponent):
    """Monitor project files for changes."""

    display_name = "File Watcher"
    description = "Watch directories and detect file changes"
```

#### Method: build()

```python
def build(
    watch_dirs: list[str] | None = None,
    poll_interval: int = 1,
    code: str | None = None,
    **_: object
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `watch_dirs` | `list[str] \| None` | Auto-detected | Directories to monitor |
| `poll_interval` | `int` | `1` | Polling interval in seconds |
| `code` | `str \| None` | `None` | LangFlow compatibility (ignored) |

**Returns:** `str` - Status message with detected changes

**Default Watch Directories:**
- `assets/sprites/`
- `assets/backgrounds/`
- `assets/dialogue/`
- `scripts/`

**Example Usage:**

```python
from .langflow.components.file_watcher import FileWatcher

watcher = FileWatcher()

# Watch default directories
result = watcher.build(poll_interval=2)

# Watch custom directories
result = watcher.build(
    watch_dirs=["assets/sprites/", "assets/music/"],
    poll_interval=1
)
```

**Signal Handling:**
- `SIGINT` (Ctrl+C): Graceful shutdown
- `SIGTERM`: Graceful shutdown

---

### EnhancedFileWatcher

**File:** `.langflow/components/enhanced_file_watcher.py`

Advanced file monitoring with automatic CI/CD triggering.

#### Class Definition

```python
class EnhancedFileWatcher(CustomComponent):
    """Advanced file watcher with auto-triggering."""

    display_name = "Enhanced File Watcher"
    description = "Monitor files and trigger automated CI/CD workflows"
```

#### Method: build()

```python
def build(
    watch_directories: List[str] = None,
    ignore_patterns: List[str] = None,
    auto_trigger_pipeline: bool = True,
    debounce_seconds: int = 5,
    watch_duration: int = 0,
    code: str | None = None,
    **_: object
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `watch_directories` | `List[str]` | See below | Directories/files to watch |
| `ignore_patterns` | `List[str]` | See below | File patterns to ignore |
| `auto_trigger_pipeline` | `bool` | `True` | Auto-trigger CI/CD on changes |
| `debounce_seconds` | `int` | `5` | Wait time after last change |
| `watch_duration` | `int` | `0` | Duration to watch (0 = infinite) |
| `code` | `str \| None` | `None` | LangFlow compatibility |

**Default Watch Directories:**
```python
[
    "assets/sprites/",
    "assets/backgrounds/",
    "assets/music/",
    "assets/sounds/",
    "scripts/",
    "docs/",
    "BARRY-SHARP-PRO-MOVER-1.gbsproj"
]
```

**Default Ignore Patterns:**
```python
[
    "*.tmp", "*.bak", "*~", ".DS_Store",
    "*.swp", "*.swo",
    "build/*", "memory/*", ".git/*"
]
```

**Returns:** `str` - Formatted status message

**Example Usage:**

```python
from .langflow.components.enhanced_file_watcher import EnhancedFileWatcher

watcher = EnhancedFileWatcher()

# Start watching with auto-trigger
result = watcher.build(
    auto_trigger_pipeline=True,
    debounce_seconds=5
)

# Watch for 60 seconds
result = watcher.build(
    watch_duration=60,
    auto_trigger_pipeline=False
)

# Stop watching
watcher.stop_watching()
```

**Change Detection:**
- Uses MD5 hashing for file change detection
- Debouncing prevents multiple triggers
- Creates approval queue entries for all changes

---

### CICDPipeline

**File:** `.langflow/components/ci_cd_pipeline.py`

Automated build, test, and deployment pipeline.

#### Class Definition

```python
class CICDPipeline(CustomComponent):
    """Automated CI/CD pipeline."""

    display_name = "CI/CD Pipeline"
    description = "Automated build, test, and deployment pipeline"
```

#### Method: build()

```python
def build(
    trigger_event: str = "manual",
    run_validation: bool = True,
    auto_test: bool = True,
    deploy_target: str = "local",
    notify_on_completion: bool = True,
    code: str | None = None,
    **_: object
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger_event` | `str` | `"manual"` | Event that triggered pipeline |
| `run_validation` | `bool` | `True` | Run pre-build validations |
| `auto_test` | `bool` | `True` | Run automated tests |
| `deploy_target` | `str` | `"local"` | Deployment target: `local`, `staging`, `production` |
| `notify_on_completion` | `bool` | `True` | Send notifications when complete |
| `code` | `str \| None` | `None` | LangFlow compatibility |

**Returns:** `str` - Formatted pipeline results with status

**Pipeline Stages:**

1. **Validation** (if `run_validation=True`)
   - `make check-bg`
   - `make check-scenes`
   - `make check-json`

2. **Build**
   - `make build-and-test`
   - Verify ROM created
   - Record ROM size

3. **Test** (if `auto_test=True`)
   - Run validation scripts
   - Check asset limits

4. **Deploy**
   - Local: Keep in `build/`
   - Staging: Copy to `staging/` with timestamp
   - Production: (future) Upload to itch.io

5. **Notify** (if `notify_on_completion=True`)
   - Execute `scripts/notify_cli.sh`

**Example Usage:**

```python
from .langflow.components.ci_cd_pipeline import CICDPipeline

pipeline = CICDPipeline()

# Full pipeline with all stages
result = pipeline.build(
    trigger_event="manual",
    run_validation=True,
    auto_test=True,
    deploy_target="local",
    notify_on_completion=True
)

# Quick build without validation
result = pipeline.build(
    run_validation=False,
    auto_test=False,
    deploy_target="local"
)

# Staging deployment
result = pipeline.build(
    trigger_event="git_tag",
    deploy_target="staging",
    notify_on_completion=True
)
```

**Output Format:**

```markdown
# CI/CD Pipeline Results

**Pipeline ID:** pipeline_1732186245
**Status:** success
**Duration:** 0:00:45.234567

## Stage Results

- **Validation:** ✅
- **Build:** ✅
- **Test:** ✅
- **Deploy:** ✅
- **Notify:** ✅
```

**Event Logging:**
- `pipeline_start`: When pipeline begins
- `pipeline_complete`: When pipeline succeeds
- `pipeline_error`: When pipeline fails

---

### ReportGenerator

**File:** `.langflow/components/report_gen.py`

Generate status reports from project ledger and approval queue.

#### Class Definition

```python
class ReportGenerator(CustomComponent):
    """Generate project status reports."""

    display_name = "Report Generator"
    description = "Create reports from ledger and approval queue"
```

#### Method: build()

```python
def build(
    report_type: str = "full",
    include_charts: bool = False,
    output_format: str = "markdown",
    code: str | None = None,
    **_: object
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `report_type` | `str` | `"full"` | Type: `full`, `summary`, `errors` |
| `include_charts` | `bool` | `False` | Include ASCII charts |
| `output_format` | `str` | `"markdown"` | Format: `markdown`, `html`, `json` |
| `code` | `str \| None` | `None` | LangFlow compatibility |

**Returns:** `str` - Formatted report

**Example Usage:**

```python
from .langflow.components.report_gen import ReportGenerator

reporter = ReportGenerator()

# Full report with charts
report = reporter.build(
    report_type="full",
    include_charts=True,
    output_format="markdown"
)

# Summary report
report = reporter.build(
    report_type="summary"
)

# Error-only report
report = reporter.build(
    report_type="errors"
)
```

---

### ApprovalQueue

**File:** `.langflow/components/approval_queue.py`

Manage workflow approvals for automated tasks.

#### Class Definition

```python
class ApprovalQueue(CustomComponent):
    """Manage approval queue for automated tasks."""

    display_name = "Approval Queue"
    description = "Queue management for human-in-the-loop workflows"
```

#### Method: build()

```python
def build(
    action: str = "list",
    task_id: str | None = None,
    decision: str | None = None,
    code: str | None = None,
    **_: object
) -> str
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | `str` | `"list"` | Action: `list`, `approve`, `reject`, `view` |
| `task_id` | `str \| None` | `None` | Task ID for approve/reject/view |
| `decision` | `str \| None` | `None` | `approve` or `reject` |
| `code` | `str \| None` | `None` | LangFlow compatibility |

**Returns:** `str` - Action result

**Example Usage:**

```python
from .langflow.components.approval_queue import ApprovalQueue

queue = ApprovalQueue()

# List all pending tasks
result = queue.build(action="list")

# View specific task
result = queue.build(
    action="view",
    task_id="file_change_1732186245"
)

# Approve task
result = queue.build(
    action="approve",
    task_id="file_change_1732186245",
    decision="approve"
)

# Reject task
result = queue.build(
    action="reject",
    task_id="file_change_1732186245",
    decision="reject"
)
```

---

## Validation Scripts

### check_scene_limits.py

**Path:** `scripts/validation/check_scene_limits.py`

Validate GB Studio scene complexity limits.

#### Function: check_scene()

```python
def check_scene(scene_file: str) -> bool
```

**Parameters:**
- `scene_file: str` - Path to scene JSON file

**Returns:** `bool` - `True` if valid, `False` if violations found

**Limits Checked:**

| Constraint | Limit | Reason |
|------------|-------|--------|
| Actors per scene | 20 | Game Boy RAM limit |
| Triggers per scene | 30 | Performance |
| Sprite tiles used | 25-64 | VRAM constraint |

**Example Usage:**

```bash
# Check single scene
python scripts/validation/check_scene_limits.py project/scenes/scene001.json

# Check all scenes
python scripts/validation/check_scene_limits.py project/scenes/
```

**Output:**
```
✓ scene001.json: OK
⚠️ scene002.json: Too many actors (25 > 20)
⚠️ scene003.json: Too many sprite tiles (70 > 64)
```

---

### check_bg_tiles.py

**Path:** `scripts/validation/check_bg_tiles.py`

Validate background tile usage.

#### Function: check_background()

```python
def check_background(bg_file: str) -> bool
```

**Parameters:**
- `bg_file: str` - Path to background PNG file

**Returns:** `bool` - `True` if valid, `False` if too many unique tiles

**Limits:**
- **Maximum unique tiles:** 192 (Game Boy background tile limit)

**Example Usage:**

```bash
# Check single background
python scripts/validation/check_bg_tiles.py assets/backgrounds/town.png

# Check all backgrounds
python scripts/validation/check_bg_tiles.py assets/backgrounds/
```

---

### check_json_schema.py

**Path:** `scripts/validation/check_json_schema.py`

Validate GB Studio JSON schema compliance.

#### Function: validate_json()

```python
def validate_json(json_file: str) -> bool
```

**Parameters:**
- `json_file: str` - Path to JSON file

**Returns:** `bool` - `True` if valid JSON, `False` if malformed

**Example Usage:**

```bash
# Check project file
python scripts/validation/check_json_schema.py BARRY-SHARP-PRO-MOVER-1.gbsproj

# Check all JSON files
python scripts/validation/check_json_schema.py project/
```

---

## Shared Utilities

### Logging Utilities

**Path:** `.langflow/utils/logging.py`

Centralized event logging for all components.

#### Function: log_to_ledger()

```python
def log_to_ledger(
    event_type: str,
    agent: str,
    task_id: str,
    details: Dict[str, Any],
    ledger_path: Path | None = None
) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `event_type` | `str` | Event name (e.g., `build_started`) |
| `agent` | `str` | Component/agent name |
| `task_id` | `str` | Unique task identifier |
| `details` | `Dict[str, Any]` | Event-specific details |
| `ledger_path` | `Path \| None` | Custom ledger path (optional) |

**Returns:** `None`

**Example Usage:**

```python
from .langflow.utils.logging import log_to_ledger

log_to_ledger(
    event_type="build_started",
    agent="ci_cd_pipeline",
    task_id="build-001",
    details={
        "target": "rom",
        "platform": "linux"
    }
)
```

**Ledger Entry Created:**
```json
{
  "timestamp": "2025-11-21T10:30:45.123456",
  "event": "build_started",
  "agent": "ci_cd_pipeline",
  "task_id": "build-001",
  "details": {
    "target": "rom",
    "platform": "linux"
  }
}
```

---

#### Function: load_ledger()

```python
def load_ledger(ledger_path: Path | None = None) -> list
```

**Parameters:**
- `ledger_path: Path | None` - Custom ledger path (optional)

**Returns:** `list` - List of all ledger entries

**Example Usage:**

```python
from .langflow.utils.logging import load_ledger

entries = load_ledger()
for entry in entries:
    print(f"{entry['timestamp']}: {entry['event']}")
```

---

#### Function: get_recent_events()

```python
def get_recent_events(
    event_type: str | None = None,
    agent: str | None = None,
    limit: int = 25,
    ledger_path: Path | None = None
) -> list
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `event_type` | `str \| None` | `None` | Filter by event type |
| `agent` | `str \| None` | `None` | Filter by agent |
| `limit` | `int` | `25` | Max events to return |
| `ledger_path` | `Path \| None` | `None` | Custom ledger path |

**Returns:** `list` - Filtered events, most recent first

**Example Usage:**

```python
from .langflow.utils.logging import get_recent_events

# Get last 10 build events
builds = get_recent_events(event_type="build_complete", limit=10)

# Get last 25 CI/CD pipeline events
pipeline_events = get_recent_events(agent="ci_cd_pipeline")

# Get all recent events
all_events = get_recent_events(limit=100)
```

---

#### Function: clear_ledger()

```python
def clear_ledger(ledger_path: Path | None = None) -> None
```

**Parameters:**
- `ledger_path: Path | None` - Custom ledger path (optional)

**Returns:** `None`

**⚠️ WARNING:** This permanently deletes all ledger history. Use only for testing.

**Example Usage:**

```python
from .langflow.utils.logging import clear_ledger

# Clear ledger (testing only!)
clear_ledger()
```

---

## Project Memory APIs

### Ledger File Format

**Path:** `memory/pm_ledger.jsonl`
**Format:** JSON Lines (one JSON object per line)

**Schema:**
```json
{
  "timestamp": "ISO 8601 datetime string",
  "event": "Event type string",
  "agent": "Component/agent name",
  "task_id": "Unique task identifier",
  "details": {
    "key": "value",
    "...": "..."
  }
}
```

### Approval Queue Format

**Path:** `memory/approval_queue.json`
**Format:** JSON

**Schema:**
```json
{
  "queue": [
    {
      "task_id": "Unique task ID",
      "agent": "Component name",
      "task_type": "Task type",
      "description": "Human-readable description",
      "details": {
        "key": "value"
      },
      "status": "detected|approved|rejected",
      "submitted_at": "ISO 8601 datetime",
      "comments": "Optional comments"
    }
  ]
}
```

---

## Build System

### Makefile Targets

#### build-rom

```bash
make build-rom
```

Build ROM from GB Studio project.

**Environment Variables:**
- `GB_STUDIO_CLI`: Path to GB Studio CLI (auto-detected if not set)

---

#### build-and-test

```bash
make build-and-test
```

Run all validations, then build ROM.

**Includes:**
- `make check-bg`
- `make check-scenes`
- `make check-json`
- `make build-rom`

---

#### check-bg

```bash
make check-bg
```

Validate all background tiles.

---

#### check-scenes

```bash
make check-scenes
```

Validate all scene limits.

---

#### check-json

```bash
make check-json
```

Validate JSON syntax.

---

#### run-emulator

```bash
make run-emulator
```

Launch built ROM in emulator.

**Emulators Supported:**
- BGB (Windows)
- SameBoy (macOS/Linux)
- Emulicious (Java-based)

---

## Testing Utilities

### Shared Fixtures (conftest.py)

**Path:** `tests/conftest.py`

#### Fixture: temp_project_dir

```python
@pytest.fixture
def temp_project_dir():
    """Create temporary project directory for testing."""
    ...
```

**Usage:**
```python
def test_something(temp_project_dir):
    project_file = temp_project_dir / "test.gbsproj"
    project_file.write_text("{}")
```

---

#### Fixture: mock_subprocess

```python
@pytest.fixture
def mock_subprocess():
    """Mock subprocess.run for testing CLI interactions."""
    ...
```

**Usage:**
```python
from unittest.mock import patch

def test_build(mock_subprocess):
    mock_subprocess.return_value.returncode = 0
    with patch('subprocess.run', mock_subprocess):
        # Test code that calls subprocess.run
        ...
```

---

#### Fixture: sample_gbsproj_path

```python
@pytest.fixture
def sample_gbsproj_path(temp_project_dir):
    """Create a sample GB Studio project file."""
    ...
```

**Usage:**
```python
def test_project(sample_gbsproj_path):
    assert sample_gbsproj_path.exists()
    data = json.loads(sample_gbsproj_path.read_text())
    assert data["name"] == "test-project"
```

---

## Error Handling

### Common Exceptions

| Exception | When Raised | How to Handle |
|-----------|-------------|---------------|
| `RuntimeError` | Build failures, missing CLI | Check logs, verify GB Studio installed |
| `FileNotFoundError` | Missing project files | Verify paths, check file exists |
| `json.JSONDecodeError` | Malformed JSON | Validate JSON syntax |
| `subprocess.CalledProcessError` | CLI command failed | Check command output, stderr |

### Error Response Format

Components return error information in their output string:

```markdown
**Error:** Description of error

**Details:**
- Error type: RuntimeError
- Message: GB Studio CLI not found
```

---

## Rate Limits and Performance

### File Watcher

- **Poll Interval:** Default 1 second
- **Debounce:** Default 5 seconds
- **File Hash Cache:** In-memory, cleared on restart

### CI/CD Pipeline

- **Concurrent Pipelines:** 1 (sequential execution)
- **Timeout:** None (manual intervention required)
- **Stage Retries:** None (fail fast)

### Event Logging

- **Write Performance:** ~1ms per event
- **File Locking:** None (append-only)
- **Max File Size:** Unlimited (rotation recommended at 10MB)

---

## Versioning

This API follows [Semantic Versioning](https://semver.org/):

- **Major:** Breaking changes to component interfaces
- **Minor:** New features, backward-compatible
- **Patch:** Bug fixes, documentation updates

**Current Version:** 0.1.0 (Phase 3 - Advanced Features)

---

## Changelog

### v0.1.0 (2025-11-21) - Phase 3

- ✅ Shared logging utilities (`log_to_ledger`, `load_ledger`, `get_recent_events`)
- ✅ Refactored `ci_cd_pipeline.py` to use shared logging
- ✅ Refactored `enhanced_file_watcher.py` to use shared logging
- ✅ Comprehensive API documentation

### v0.0.2 (2025-11-21) - Phase 2

- Added comprehensive testing (80%+ coverage)
- Refactored `file_watcher.py` and `report_gen.py`
- Added CI/CD workflows
- Created CONTRIBUTING.md and SECURITY.md

### v0.0.1 (2025-11-20) - Phase 1

- Initial component creation
- Basic build and validation functionality
- Makefile build system

---

## Support

For issues, questions, or contributions:

- **Issues:** [GitHub Issues](https://github.com/nitepoetlaureate/BarrySharpProMover/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nitepoetlaureate/BarrySharpProMover/discussions)
- **Documentation:** [docs/](../docs/)
- **Contributing:** [CONTRIBUTING.md](../CONTRIBUTING.md)

---

*Last Updated: 2025-11-21*
*API Version: 0.1.0*
