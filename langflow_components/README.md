# Barry Sharp Pro Mover - Custom Langflow Components

This directory contains custom Langflow components for automating GB Studio game development workflows.

## Components

### 1. GB Studio Build (`gbstudio_build.py`)

**Purpose:** Build Game Boy ROMs and web exports using GB Studio CLI.

**Features:**
- Build ROM, web, and pocket versions
- Configurable GB Studio CLI path
- Clean build option
- Verbose output logging
- Automatic output directory creation
- Build artifact tracking

**Inputs:**
- Project path (.gbsproj file)
- Build type (rom/web/pocket)
- Output directory
- GB Studio CLI path (optional)
- Clean build flag
- Verbose output flag

**Outputs:**
- Build result (success/failure)
- Build output logs
- Build data (files, paths, errors)

### 2. Enhanced File Watcher (`enhanced_file_watcher.py`)

**Purpose:** Monitor file system for changes and trigger workflow actions.

**Features:**
- Pattern-based file filtering (include/exclude)
- Event type selection (created/modified/deleted)
- Debouncing to prevent rapid re-triggers
- Recursive directory watching
- File hash computation for change verification
- Change event tracking with metadata

**Inputs:**
- Watch path (directory or file)
- Include patterns (glob patterns)
- Exclude patterns (glob patterns)
- Event types to watch
- Debounce delay
- Recursive flag
- Hash computation flag

**Outputs:**
- List of detected changes
- Change details (event type, path, size, hash)

### 3. Notifier (`notifier.py`)

**Purpose:** Send notifications through multiple channels.

**Features:**
- Multiple notification channels (console/file/webhook)
- Severity levels (info/success/warning/error/critical)
- Colored console output with icons
- File logging with timestamps
- Webhook integration
- Notification throttling
- Metadata inclusion

**Inputs:**
- Notification title
- Message body
- Severity level
- Notification channel
- Log file path (for file channel)
- Webhook URL (for webhook channel)
- Timestamp inclusion flag
- Metadata inclusion flag
- Throttle delay

**Outputs:**
- Notification result
- Delivery status per channel

### 4. Report Generator (`report_gen.py`)

**Purpose:** Generate formatted reports from workflow data.

**Features:**
- Multiple output formats (Markdown/HTML/JSON/Text)
- Automatic summary generation
- Custom content sections
- Timestamp and metadata inclusion
- File output option
- Template-based formatting

**Inputs:**
- Report title
- Report data (from other components)
- Custom content
- Report format
- Output file path (optional)
- Timestamp flag
- Summary flag
- Metadata flag

**Outputs:**
- Formatted report content
- Report metadata (format, length, path)

### 5. CI/CD Pipeline (`ci_cd_pipeline.py`)

**Purpose:** Orchestrate continuous integration and deployment workflows.

**Features:**
- Multi-stage pipeline execution
- Stage-based validation, build, test, deploy, notify, report
- Error handling and stop-on-error option
- Pipeline artifacts generation
- Execution history tracking
- Configurable timeouts
- Stage duration tracking

**Inputs:**
- Pipeline name
- Trigger mode
- Pipeline stages (list)
- Project root
- Stop on error flag
- Timeout
- Artifacts generation flag
- Artifacts directory

**Outputs:**
- Pipeline execution result
- Stage-by-stage results
- Overall success status
- Execution metadata

## Usage

### Installation

These components are automatically available when you install the `barrysharp-components` package:

```bash
pip install -e .
```

### In Langflow

1. Start Langflow:
   ```bash
   langflow run
   ```

2. Open the Langflow UI (http://localhost:7860)

3. Look for the custom components in the components panel:
   - **GB Studio Build** - Under Tools
   - **Enhanced File Watcher** - Under Tools
   - **Notifier** - Under Tools
   - **Report Generator** - Under Tools
   - **CI/CD Pipeline** - Under Tools

4. Drag and drop components into your workflow

5. Connect components to create automation pipelines

### Example Workflow

Here's a typical automation workflow:

```
1. Enhanced File Watcher
   ↓ (detects .gbsproj change)
2. GB Studio Build
   ↓ (builds ROM)
3. Notifier (build started)
   ↓
4. CI/CD Pipeline (validation)
   ↓
5. Report Generator (build report)
   ↓
6. Notifier (build completed)
```

## Component Development

### Adding New Components

1. Create a new file in `langflow_components/tools/`
2. Inherit from `langflow.custom.Component`
3. Define inputs using Langflow input types
4. Define outputs using `Output`
5. Implement component methods
6. Update `__init__.py` to export the component

### Component Template

```python
from langflow.custom import Component
from langflow.io import StrInput, Output
from langflow.schema import Data

class MyComponent(Component):
    display_name = "My Component"
    description = "Description of component"
    icon = "🎮"
    name = "MyComponent"

    inputs = [
        StrInput(
            name="input_param",
            display_name="Input Parameter",
            info="Parameter description",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Result", name="result", method="process"),
    ]

    def process(self) -> Data:
        # Component logic here
        return Data(
            data={"success": True},
            text="Operation completed"
        )
```

## Testing Components

Test components individually before integrating into workflows:

```python
from langflow_components.tools.gbstudio_build import GBStudioBuild

# Create component instance
builder = GBStudioBuild()
builder.project_path = "BARRY-SHARP-PRO-MOVER-1.gbsproj"
builder.build_type = "rom"
builder.output_dir = "build/"

# Execute
result = builder.build_project()
print(result.data)
```

## Troubleshooting

### Component Not Appearing in Langflow

1. Ensure package is installed: `pip list | grep barrysharp`
2. Restart Langflow server
3. Check component imports in `__init__.py`
4. Verify component class inherits from `Component`

### Import Errors

1. Activate virtual environment: `source venv/bin/activate`
2. Reinstall package: `pip install -e .`
3. Check Python path: `python -c "import langflow_components; print(langflow_components.__file__)"`

### GB Studio Build Failures

1. Verify GB Studio CLI is installed
2. Check GB Studio CLI path configuration
3. Ensure .gbsproj file exists
4. Check build output logs for errors

## Resources

- **Langflow Documentation**: https://docs.langflow.org/
- **GB Studio Documentation**: https://www.gbstudio.dev/docs
- **Project README**: `../README.md`
- **Setup Guide**: `../docs/DEV_ENVIRONMENT_SETUP_COMPLETE.md`

## Contributing

When adding new components:

1. Follow existing component structure
2. Include comprehensive docstrings
3. Add input validation
4. Implement error handling
5. Log important operations
6. Update this README
7. Test thoroughly before committing

---

**Barry Sharp Pro Mover** - Automating Game Boy game development with Langflow
