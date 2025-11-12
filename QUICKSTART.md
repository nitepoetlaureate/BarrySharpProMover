# Barry Sharp Pro Mover - Quick Start Guide

Get up and running with the Barry Sharp Pro Mover development environment in minutes.

## Prerequisites Check

```bash
# Run the environment verification script
./scripts/verify_dev_environment.sh
```

## Step 1: Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

## Step 2: Verify Installation

```bash
# Check Python packages
python -c "import langflow; print('Langflow installed successfully!')"

# Check project structure
ls -la langflow_agents/
ls -la memory/
```

## Step 3: Choose Your Development Path

### Option A: Langflow Development

Start the Langflow server for visual workflow development:

```bash
./start_langflow_local.sh
```

Then open your browser to:
- **Frontend**: http://localhost:3000
- **API**: http://127.0.0.1:7860

### Option B: GB Studio Game Development

**Note**: GB Studio CLI needs to be installed first (see Setup Guide).

```bash
# Build the ROM
make build-rom

# Build web version
make build-web
```

### Option C: Asset Development

Work on game assets with validation:

```bash
# Validate background tiles
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

# Check scene limits
python3 scripts/validation/check_scene_limits.py project/scenes/
```

### Option D: Custom Component Development

Create Langflow components in `langflow_components/`:

```python
# Example component structure
from langflow.base.io.component import Component

class MyComponent(Component):
    display_name = "My Component"
    description = "Does something cool"

    def build(self):
        # Your implementation here
        pass
```

## Common Commands

```bash
# Create a project snapshot
./scripts/snapshot.sh "Added new feature"

# Bootstrap project structure (if needed)
./bootstrap_pm_backbone.sh

# Build directories
make build-dirs

# Sync GB Studio resources
./scripts/sync_gbsres.sh
```

## Project Structure

```
BarrySharpProMover/
├── assets/              # Game assets (sprites, backgrounds, music)
├── build/               # Compiled ROMs and builds
├── docs/                # Documentation
├── langflow_agents/     # Agent configurations
├── langflow_components/ # Custom Langflow components
├── langflow_projects/   # Langflow workflows
├── memory/              # Project state and logs
├── scripts/             # Development scripts
├── vectorstore/         # Knowledge base
└── venv/                # Python virtual environment
```

## Need Help?

- **Full Setup Guide**: `docs/DEV_ENVIRONMENT_SETUP_COMPLETE.md`
- **Langflow Guide**: `docs/LANGFLOW_LOCAL_SETUP_GUIDE.md`
- **Automation Guide**: `docs/AUTOMATION_GUIDE.md`
- **Main README**: `README.md`

## Troubleshooting

### "Command not found" errors

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### GB Studio build fails

GB Studio CLI needs to be installed. See the full setup guide for details.

### Langflow import errors

Reinstall the project package:
```bash
pip install -e .
```

## What's Next?

1. Read the full setup documentation
2. Install GB Studio CLI (if building ROMs)
3. Explore the Langflow UI
4. Start developing your game!

Happy coding! 🎮
