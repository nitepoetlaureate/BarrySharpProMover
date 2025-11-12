# Development Environment Setup - Complete Guide

This document describes the completed development environment setup for the Barry Sharp Pro Mover project.

## Setup Date

- **Date**: November 12, 2025
- **System**: Linux 4.4.0
- **Branch**: claude/incomplete-query-011CV3weZuv6hxDCGu5RLXXd

## System Prerequisites ✓

All core system tools have been verified and are installed:

| Tool | Version | Status |
|------|---------|--------|
| Python | 3.11.14 | ✓ Installed |
| Node.js | v22.21.1 | ✓ Installed |
| npm | 10.9.4 | ✓ Installed |
| Make | GNU Make 4.3 | ✓ Installed |
| Git | 2.43.0 | ✓ Installed |

## Python Environment Setup ✓

### Virtual Environment

- **Location**: `/home/user/BarrySharpProMover/venv`
- **Python Version**: 3.11.14
- **Status**: ✓ Created and functional

### Activation

```bash
source venv/bin/activate
```

## Python Packages Installed ✓

The following packages have been installed in the virtual environment:

### Core Dependencies

- **Langflow >= 1.4** - Installed via project dependencies
- **barrysharp-components 0.1.0** - Installed in editable mode

### Installation Commands Used

```bash
# Activate virtual environment
source venv/bin/activate

# Install project package (includes Langflow)
pip install -e .
```

## Project Structure Setup ✓

The project management backbone has been initialized with the following structure:

### Directories Created

- `langflow_agents/` - Agent registry and definitions
- `langflow_projects/` - Langflow workflow definitions
- `feedback/` - User feedback and testing results
- `approved/` - Approved changes and assets
- `memory/` - Project state tracking
- `vectorstore/` - Knowledge base storage
- `staging/` - Temporary staging area

### Key Files Created

- `langflow_agents/registry.json` - Agent configuration
- `memory/approval_queue.json` - Approval workflow queue
- `memory/pm_ledger.jsonl` - Project management event log
- `scripts/verify_dev_environment.sh` - Environment verification script

### Bootstrap Script

The PM backbone was initialized using:

```bash
./bootstrap_pm_backbone.sh
```

## Build System Verification ✓

### Build Directory

- **Location**: `/home/user/BarrySharpProMover/build`
- **Status**: ✓ Exists with previous build artifacts
- **ROM File**: build/game.gb (65536 bytes)

### Make Targets Tested

```bash
make build-dirs  # ✓ Working
```

## GB Studio CLI Status ⚠️

### Current Status

GB Studio CLI is **NOT** currently installed or configured on this Linux system.

### Issue

The Makefile contains a hardcoded macOS-specific path:

```makefile
/Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js
```

### Required Actions

To use GB Studio CLI on this Linux environment, you need to:

1. **Install GB Studio**
   - Download from: https://www.gbstudio.dev/
   - Install AppImage or build from source

2. **Update Makefile**
   - Locate the GB Studio CLI installation
   - Update paths in `Makefile` to point to correct location
   - Typical Linux locations:
     - `/usr/local/bin/gb-studio-cli`
     - `/opt/gb-studio/cli/`
     - User local installation

3. **Alternative**: Use GB Studio Desktop Application
   - Open the `.gbsproj` file in GB Studio
   - Use the GUI to build ROMs

### Workaround

Until GB Studio CLI is installed, you can:
- Use other make targets that don't require GB Studio CLI
- Develop Langflow components and automation
- Work on assets and project structure

## Verification Script ✓

A comprehensive environment verification script has been created:

**Location**: `scripts/verify_dev_environment.sh`

### Usage

```bash
./scripts/verify_dev_environment.sh
```

### What It Checks

- ✓ System prerequisites (Python, Node.js, npm, Make, Git)
- ⚠️ GB Studio CLI availability
- ✓ Python virtual environment
- ✓ Python packages (Langflow)
- ✓ Project directory structure
- ✓ Project management backbone files
- ✓ Build artifacts

## Langflow Components Status

### Directory Structure

- **Location**: `/home/user/BarrySharpProMover/langflow_components/`
- **Status**: Directory exists but custom components not yet implemented

### Expected Components

According to the documentation, the following components should be created:

- `ci_cd_pipeline.py` - CI/CD automation
- `enhanced_file_watcher.py` - File monitoring
- `gbstudio_build.py` - GB Studio integration
- `notifier.py` - Notification system
- `report_gen.py` - Report generation

### Development Note

These components are referenced in the automation documentation but are not yet implemented in the repository. They will need to be developed as part of the project enhancement.

## Starting Langflow

### Local Development Server

To start Langflow for development:

```bash
./start_langflow_local.sh
```

This script will:
1. Clone Langflow repository (if needed) to `langflow_repo/`
2. Create virtual environment in `langflow_env/`
3. Install backend and frontend dependencies
4. Build frontend
5. Start backend (port 7860) and frontend (port 3000)

### Access Points

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://127.0.0.1:7860

## Next Steps for Development

### 1. GB Studio CLI Setup

- Install GB Studio CLI for Linux
- Update Makefile with correct paths
- Test ROM building: `make build-rom`

### 2. Langflow Development

- Start Langflow: `./start_langflow_local.sh`
- Create custom components in `langflow_components/`
- Design workflows in Langflow UI
- Export workflows to `langflow_projects/`

### 3. Project Package Development

- Implement custom Langflow components
- Add project-specific tools
- Test component integration

### 4. Automation Setup

- Configure file watchers
- Set up CI/CD pipeline
- Test automation workflows

### 5. Asset Development

- Create sprites, backgrounds, music
- Use validation scripts:
  ```bash
  python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png
  python3 scripts/validation/check_scene_limits.py project/scenes/
  ```

## Environment Variables

No special environment variables are currently required. The project uses local paths and configurations.

## Troubleshooting

### Virtual Environment Not Activating

```bash
cd /home/user/BarrySharpProMover
source venv/bin/activate
```

### Langflow Import Errors

```bash
source venv/bin/activate
python -c "import langflow; print(langflow.__version__)"
```

### Make Targets Failing

Check that you're in the project root:

```bash
pwd  # Should show: /home/user/BarrySharpProMover
```

### GB Studio Build Failures

Ensure GB Studio CLI is installed and Makefile paths are updated (see GB Studio CLI Status section above).

## Summary

### ✅ Completed

- System prerequisites verification
- Python virtual environment setup
- Langflow installation
- Project package installation (barrysharp-components)
- Project structure initialization
- PM backbone bootstrap
- Build system verification
- Environment verification script creation

### ⚠️ Requires Attention

- GB Studio CLI installation/configuration
- Makefile path updates for Linux environment
- Custom Langflow components implementation

### 📋 Ready for Development

The development environment is **ready for**:
- Langflow workflow development
- Python component development
- Asset creation and validation
- Project management automation
- Documentation and testing

The environment is **not ready for**:
- GB Studio ROM building (requires GB Studio CLI)
- Complete CI/CD pipeline (requires GB Studio CLI)

## Quick Reference Commands

```bash
# Activate environment
source venv/bin/activate

# Verify setup
./scripts/verify_dev_environment.sh

# Start Langflow
./start_langflow_local.sh

# Build directories
make build-dirs

# Validate assets
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

# Create snapshot
./scripts/snapshot.sh "description"

# Bootstrap PM backbone (if needed again)
./bootstrap_pm_backbone.sh
```

## Additional Documentation

- `docs/LANGFLOW_LOCAL_SETUP_GUIDE.md` - Langflow setup details
- `docs/AUTOMATION_GUIDE.md` - Automation system guide
- `README.md` - Project overview
- `scripts/README.md` - Scripts documentation

## Support and Resources

- GB Studio: https://www.gbstudio.dev/
- Langflow: https://docs.langflow.org/
- Project Repository: github.com/nitepoetlaureate/BarrySharpProMover
