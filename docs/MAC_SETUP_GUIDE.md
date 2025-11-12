# Barry Sharp Pro Mover - macOS Setup Guide

Complete setup instructions for developing on macOS.

## Prerequisites

Ensure you have these installed on your Mac:

```bash
# Check versions
python3 --version  # Should be 3.9+
node --version     # Should be 14+
npm --version
git --version
```

## Step 1: Navigate to Your Cloned Repository

```bash
cd ~/BarrySharpProMover
git checkout claude/incomplete-query-011CV3weZuv6hxDCGu5RLXXd
```

## Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

## Step 3: Install Python Packages

```bash
# Install the project package (this will also install Langflow)
pip install -e .
```

This will install:
- Langflow >= 1.4
- All Langflow dependencies
- The barrysharp-components package in editable mode

**Note**: This installation may take 5-10 minutes as Langflow has many dependencies.

## Step 4: Verify Installation

```bash
# Check that packages are installed
pip list | grep langflow
pip list | grep barrysharp

# Test import
python -c "import langflow_base; print('Langflow installed successfully!')"
```

## Step 5: Install GB Studio

### Option A: Download from Website

1. Go to https://www.gbstudio.dev/
2. Download the macOS version
3. Install to Applications folder

### Option B: Via Homebrew (if available)

```bash
brew install gbstudio
```

### Locate GB Studio CLI

After installation, find the CLI:

```bash
# Check common locations
ls /Applications/GB\ Studio.app/Contents/Resources/app/out/cli/
ls ~/Applications/GB\ Studio.app/Contents/Resources/app/out/cli/

# Or use find
find /Applications -name "gb-studio-cli.js" 2>/dev/null
```

## Step 6: Update Makefile

Edit the `Makefile` and update the GB Studio CLI path on lines 19-20, 24:

**Current (macOS-specific path - needs updating):**
```makefile
node "/Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js" ...
```

**Update to your path:**
```makefile
node "/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js" ...
```

Or if you installed elsewhere, use that path.

## Step 7: Initialize Project Structure

```bash
# Run the bootstrap script
./bootstrap_pm_backbone.sh

# This creates:
# - langflow_agents/
# - langflow_projects/
# - memory/
# - vectorstore/
# - feedback/
# - approved/
```

## Step 8: Test Build System

```bash
# Test basic make commands
make build-dirs

# Try building the ROM (requires GB Studio CLI)
make build-rom

# Build web version
make build-web
```

## Step 9: Start Langflow (Local Development)

### Using the Provided Script

```bash
./start_langflow_local.sh
```

This will:
1. Clone the Langflow repository to `langflow_repo/`
2. Create a separate virtual environment in `langflow_env/`
3. Install backend and frontend dependencies
4. Build the frontend
5. Start both services

**Access:**
- Frontend UI: http://localhost:3000
- Backend API: http://127.0.0.1:7860

### Stopping Langflow

```bash
# Find the processes
lsof -i :3000  # Frontend
lsof -i :7860  # Backend

# Kill them
kill <PID_from_port_3000>
kill <PID_from_port_7860>
```

## macOS-Specific Notes

### Permissions

If you get permission errors:

```bash
chmod +x bootstrap_pm_backbone.sh
chmod +x start_langflow_local.sh
chmod +x scripts/*.sh
```

### Python Version

macOS may have both `python` and `python3`. Always use `python3`:

```bash
# Create alias (add to ~/.zshrc or ~/.bash_profile)
alias python=python3
```

### Node.js Version

If you need to update Node.js:

```bash
# Using Homebrew
brew install node

# Or use nvm (Node Version Manager)
```

## Quick Start Commands

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Verify setup
./scripts/verify_dev_environment.sh

# 3. Start Langflow
./start_langflow_local.sh

# 4. Build ROM (in another terminal)
source venv/bin/activate
make build-rom
```

## Directory Structure (After Setup)

```
~/BarrySharpProMover/
├── venv/                    # Your Python virtual environment
├── langflow_repo/           # Cloned Langflow source (for local dev)
├── langflow_env/            # Separate venv for Langflow dev server
├── langflow_agents/         # Agent configurations
├── langflow_projects/       # Your Langflow workflows
├── langflow_components/     # Custom components
├── assets/                  # Game assets
├── build/                   # Built ROMs
├── docs/                    # Documentation
├── memory/                  # Project state
├── scripts/                 # Dev scripts
└── vectorstore/             # Knowledge bases
```

## Git Ignore

These directories should already be in `.gitignore`:
- `venv/`
- `langflow_repo/`
- `langflow_env/`
- `__pycache__/`
- `*.pyc`

## Troubleshooting

### "Command not found: langflow"

```bash
# Make sure venv is activated
source venv/bin/activate

# Check installation
pip show langflow-base
```

### GB Studio Build Fails

```bash
# Verify GB Studio CLI exists
ls -la "/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js"

# Update Makefile with correct path
```

### Port Already in Use

```bash
# Kill processes on ports
lsof -ti:3000 | xargs kill
lsof -ti:7860 | xargs kill
```

### Python Version Issues

```bash
# Use specific Python version
python3.11 -m venv venv
# or
python3.9 -m venv venv
```

### Permission Denied on Scripts

```bash
# Make executable
chmod +x *.sh
chmod +x scripts/*.sh
```

## Development Workflow

### Typical Session

```bash
# Terminal 1: Langflow
cd ~/BarrySharpProMover
./start_langflow_local.sh
# Keep this running, access UI at http://localhost:3000

# Terminal 2: Development
cd ~/BarrySharpProMover
source venv/bin/activate
# Edit files, run builds
make build-rom
./scripts/validation/check_bg_tiles.py assets/backgrounds/*.png
```

### Creating Components

1. Create Python file in `langflow_components/`
2. Restart Langflow server
3. Your component appears in the UI
4. Build workflows in the UI
5. Export workflows to `langflow_projects/`

## Next Steps

1. ✅ Complete this setup
2. Open Langflow UI (http://localhost:3000)
3. Explore the existing components
4. Create your first custom component
5. Build a workflow
6. Test with GB Studio

## Resources

- **GB Studio Docs**: https://www.gbstudio.dev/docs
- **Langflow Docs**: https://docs.langflow.org/
- **Project README**: `../README.md`
- **Automation Guide**: `AUTOMATION_GUIDE.md`

## Support

If you encounter issues:

1. Check this guide
2. Run `./scripts/verify_dev_environment.sh`
3. Check the logs in `memory/automation.log`
4. Review error messages carefully
5. Ensure all prerequisites are installed

---

**You're all set!** 🎮 Start developing your GB Studio game with Langflow automation!
