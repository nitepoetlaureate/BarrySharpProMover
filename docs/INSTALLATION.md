# Barry Sharp Pro Mover - Installation Guide

**Version:** 0.1.0
**Last Updated:** 2025-11-21

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [GB Studio Installation](#gb-studio-installation)
4. [Python Environment Setup](#python-environment-setup)
5. [LangFlow Installation](#langflow-installation)
6. [Project Setup](#project-setup)
7. [Verification](#verification)
8. [Platform-Specific Notes](#platform-specific-notes)
9. [Troubleshooting](#troubleshooting)
10. [Optional Tools](#optional-tools)

---

## Quick Start

**For experienced developers:**

```bash
# 1. Clone repository
git clone https://github.com/nitepoetlaureate/BarrySharpProMover.git
cd BarrySharpProMover

# 2. Install Python dependencies
pip install -e ".[dev]"

# 3. Install GB Studio (download from gbstudio.dev)
# Then verify:
make --version
python --version
gbstudio-cli --version  # or check Makefile auto-detection

# 4. Run tests
pytest

# 5. Build ROM
make build-and-test
```

**First-time setup? Continue reading for detailed instructions.**

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | macOS 10.15, Ubuntu 20.04, Windows 10 | Latest stable |
| **RAM** | 4 GB | 8 GB+ |
| **Disk Space** | 2 GB | 5 GB+ |
| **CPU** | Dual-core | Quad-core+ |

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.9+ | Component development |
| **Node.js** | 18+ | GB Studio CLI |
| **Git** | 2.30+ | Version control |
| **Git LFS** | Latest | Large file storage |
| **Make** | Any | Build automation |

### Check Installed Versions

```bash
python --version      # Should be 3.9+
node --version        # Should be v18+
git --version         # Should be 2.30+
git lfs version       # Should be installed
make --version        # Should be present
```

---

## GB Studio Installation

GB Studio is required to compile Game Boy ROMs.

### Option 1: Official Release (Recommended)

**Download from:** https://www.gbstudio.dev/

#### macOS

```bash
# 1. Download GB Studio.dmg from gbstudio.dev
# 2. Drag to Applications folder
# 3. Verify installation
ls -la "/Applications/GB Studio.app/Contents/Resources/app.asar.unpacked/out/cli/gb-studio-cli.js"
```

**CLI Path (macOS):**
```
/Applications/GB Studio.app/Contents/Resources/app.asar.unpacked/out/cli/gb-studio-cli.js
```

#### Linux

```bash
# 1. Download GB-Studio-linux-x64.AppImage from gbstudio.dev
# 2. Make executable
chmod +x GB-Studio-linux-x64.AppImage

# 3. Extract or run
./GB-Studio-linux-x64.AppImage --appimage-extract
```

**CLI Path (Linux):**
```
squashfs-root/resources/app.asar.unpacked/out/cli/gb-studio-cli.js
```

#### Windows

```bash
# 1. Download GB-Studio-win-x64.exe from gbstudio.dev
# 2. Run installer
# 3. Verify installation
ls "C:\Program Files\GB Studio\resources\app.asar.unpacked\out\cli\gb-studio-cli.js"
```

**CLI Path (Windows):**
```
C:\Program Files\GB Studio\resources\app.asar.unpacked\out\cli\gb-studio-cli.js
```

---

### Option 2: Build from Source

**For advanced users or custom setups:**

```bash
# 1. Clone GB Studio repository
git clone https://github.com/chrismaltby/gb-studio.git
cd gb-studio

# 2. Install dependencies
npm install

# 3. Build
npm run build

# 4. CLI will be at:
ls out/cli/gb-studio-cli.js
```

**Set environment variable:**
```bash
export GB_STUDIO_CLI="$HOME/gb-studio/out/cli/gb-studio-cli.js"
```

---

### Verify GB Studio CLI

**Test the CLI:**

```bash
# macOS (official install)
node "/Applications/GB Studio.app/Contents/Resources/app.asar.unpacked/out/cli/gb-studio-cli.js" --version

# Or if gb-studio-cli is in PATH
gbstudio-cli --version
```

**Expected output:**
```
4.0.0 (or later)
```

---

## Python Environment Setup

### Create Virtual Environment

**Using venv (recommended):**

```bash
# 1. Navigate to project
cd BarrySharpProMover

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate
source venv/bin/activate        # macOS/Linux
# or
.\venv\Scripts\activate         # Windows
```

**Using conda:**

```bash
# 1. Create environment
conda create -n barrysharp python=3.11

# 2. Activate
conda activate barrysharp
```

---

### Install Python Dependencies

**Install in development mode:**

```bash
# Install all dependencies including dev tools
pip install -e ".[dev]"
```

**This installs:**
- **Runtime:** `langflow>=1.4`
- **Testing:** `pytest`, `pytest-cov`, `pytest-mock`, `pytest-asyncio`
- **Linting:** `ruff`, `mypy`
- **Type stubs:** (as needed)

**Verify installation:**

```bash
pip list | grep -E "(langflow|pytest|ruff|mypy)"
```

**Expected output:**
```
langflow                 1.4.0
pytest                   7.4.0
pytest-cov               4.1.0
pytest-mock              3.12.0
ruff                     0.1.0
mypy                     1.7.0
```

---

## LangFlow Installation

LangFlow provides the AI workflow automation platform.

### Option 1: Use Existing LangFlow (Recommended)

If you have LangFlow already installed:

```bash
# Verify LangFlow is running
curl http://localhost:7860/health

# Expected: {"status": "ok"}
```

**Register custom components:**

```bash
# LangFlow auto-discovers components in .langflow/components/
# Restart LangFlow to reload:
pkill -f langflow
langflow run
```

---

### Option 2: Local LangFlow Setup

**Install LangFlow:**

```bash
pip install langflow>=1.4
```

**Start LangFlow server:**

```bash
langflow run --host 0.0.0.0 --port 7860
```

**Access UI:**
```
http://localhost:7860
```

**Import components:**
1. Open LangFlow UI
2. Create new flow
3. Components from `.langflow/components/` will appear in sidebar
4. Drag and drop to use

---

### Option 3: Docker Setup

**Using Docker Compose:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  langflow:
    image: langflowai/langflow:latest
    ports:
      - "7860:7860"
    volumes:
      - ./langflow:/app/.langflow
    environment:
      - LANGFLOW_AUTO_LOGIN=true
```

**Start:**
```bash
docker-compose up -d
```

---

## Project Setup

### Clone Repository

```bash
# 1. Clone with LFS
git lfs install
git clone https://github.com/nitepoetlaureate/BarrySharpProMover.git
cd BarrySharpProMover

# 2. Verify LFS checkout
git lfs pull
ls -lh assets/sprites/  # Should show actual PNGs, not pointers
```

---

### Configure Environment

**Create `.env` file (optional):**

```bash
# .env
GB_STUDIO_CLI=/path/to/your/gb-studio-cli.js
LANGFLOW_HOST=localhost
LANGFLOW_PORT=7860
```

**Or set environment variables:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export GB_STUDIO_CLI="/Applications/GB Studio.app/Contents/Resources/app.asar.unpacked/out/cli/gb-studio-cli.js"
```

---

### Initialize Project Memory

```bash
# Create memory directory (gitignored)
mkdir -p memory

# Initialize empty ledger
touch memory/pm_ledger.jsonl

# Initialize approval queue
echo '{"queue": []}' > memory/approval_queue.json
```

---

## Verification

### Verify Installation

**Run comprehensive verification:**

```bash
# 1. Check Python dependencies
python -c "import langflow; print('LangFlow OK')"

# 2. Check GB Studio CLI
make --dry-run build-rom

# 3. Run linting
ruff check .
ruff format --check .

# 4. Run type checking
mypy .

# 5. Run tests
pytest --cov=.langflow --cov-report=term-missing

# 6. Run validation scripts
python scripts/validation/check_scene_limits.py project/scenes/ || true
python scripts/validation/check_bg_tiles.py assets/backgrounds/ || true
```

**Expected results:**
- ✅ All imports successful
- ✅ GB Studio CLI detected
- ✅ Linting passes (0 errors)
- ✅ Type checking passes
- ✅ All tests pass (80%+ coverage)
- ✅ Validation scripts run without errors

---

### Test Build

**Build ROM to verify end-to-end:**

```bash
# Full build with all checks
make build-and-test
```

**Expected output:**
```
✓ Background tiles validated
✓ Scene limits validated
✓ JSON schema validated
✓ Building ROM...
✓ ROM created: build/rom.gb (512 KB)
```

**Verify ROM:**
```bash
ls -lh build/rom.gb
file build/rom.gb
```

**Expected:**
```
build/rom.gb: Game Boy ROM image
```

---

## Platform-Specific Notes

### macOS

**Homebrew packages:**
```bash
brew install git git-lfs node python@3.11 make
```

**Python location:**
```bash
which python3  # /usr/local/bin/python3 or /opt/homebrew/bin/python3
```

**Known issues:**
- **Gatekeeper:** Right-click GB Studio.app → Open to bypass security
- **Rosetta:** On M1/M2, ensure Node.js is arm64 version

---

### Linux (Ubuntu/Debian)

**System packages:**
```bash
sudo apt update
sudo apt install -y \
    git git-lfs \
    python3 python3-pip python3-venv \
    nodejs npm \
    build-essential \
    make
```

**AppImage setup:**
```bash
# Extract AppImage
./GB-Studio-linux-x64.AppImage --appimage-extract

# Create symlink
sudo ln -s "$(pwd)/squashfs-root/resources/app.asar.unpacked/out/cli/gb-studio-cli.js" \
    /usr/local/bin/gbstudio-cli
```

**Known issues:**
- **FUSE:** May need `sudo apt install libfuse2` for AppImages
- **Permissions:** Ensure AppImage is executable: `chmod +x GB-Studio-*.AppImage`

---

### Windows (WSL2 Recommended)

**Using WSL2:**

```bash
# 1. Enable WSL2
wsl --install

# 2. Install Ubuntu
wsl --install -d Ubuntu

# 3. Follow Linux instructions above in WSL shell
```

**Using native Windows:**

```powershell
# Install via Chocolatey
choco install git git-lfs nodejs python make

# Install GB Studio (manual download)
# Follow installer prompts
```

**Known issues:**
- **Line endings:** Configure git: `git config --global core.autocrlf input`
- **Paths:** Use forward slashes in Makefile: `GB_STUDIO_CLI=C:/Program Files/GB Studio/...`
- **Make:** Install via `choco install make` or use WSL2

---

## Troubleshooting

### GB Studio CLI Not Found

**Error:**
```
make: gb-studio-cli-not-found: No such file or directory
```

**Solutions:**

1. **Set environment variable:**
   ```bash
   export GB_STUDIO_CLI="/path/to/gb-studio-cli.js"
   ```

2. **Verify path:**
   ```bash
   ls -la "$GB_STUDIO_CLI"
   ```

3. **Update Makefile:**
   ```makefile
   GB_STUDIO_CLI ?= /custom/path/to/gb-studio-cli.js
   ```

---

### Python Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'langflow'
```

**Solutions:**

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Check Python version:**
   ```bash
   python --version  # Must be 3.9+
   ```

---

### Git LFS Issues

**Error:**
```
Encountered 24 file(s) that should have been pointers, but weren't
```

**Solutions:**

1. **Install Git LFS:**
   ```bash
   git lfs install
   ```

2. **Re-pull LFS files:**
   ```bash
   git lfs pull
   ```

3. **Verify LFS tracking:**
   ```bash
   git lfs ls-files
   ```

---

### Test Failures

**Error:**
```
FAILED tests/unit/test_gbstudio_build.py::test_successful_rom_build
```

**Solutions:**

1. **Check test output:**
   ```bash
   pytest -v --tb=short
   ```

2. **Run specific test:**
   ```bash
   pytest tests/unit/test_gbstudio_build.py::test_successful_rom_build -v
   ```

3. **Clean and rerun:**
   ```bash
   rm -rf .pytest_cache __pycache__
   pytest
   ```

---

### Build Failures

**Error:**
```
Error: ROM file not found after build
```

**Solutions:**

1. **Check GB Studio CLI output:**
   ```bash
   make build-rom 2>&1 | tee build.log
   ```

2. **Verify project file:**
   ```bash
   ls -la BARRY-SHARP-PRO-MOVER-1.gbsproj
   ```

3. **Check disk space:**
   ```bash
   df -h .
   ```

4. **Run validation first:**
   ```bash
   make check-bg check-scenes check-json
   ```

---

### LangFlow Connection Issues

**Error:**
```
ConnectionError: Cannot connect to LangFlow at localhost:7860
```

**Solutions:**

1. **Verify LangFlow is running:**
   ```bash
   curl http://localhost:7860/health
   ```

2. **Check port:**
   ```bash
   lsof -i :7860
   # or
   netstat -an | grep 7860
   ```

3. **Restart LangFlow:**
   ```bash
   pkill -f langflow
   langflow run --host 0.0.0.0 --port 7860
   ```

---

## Optional Tools

### Game Boy Emulators

**For testing ROMs:**

| Emulator | Platform | Download |
|----------|----------|----------|
| **BGB** | Windows | https://bgb.bircd.org/ |
| **SameBoy** | macOS/Linux | https://sameboy.github.io/ |
| **Emulicious** | Cross-platform (Java) | https://emulicious.net/ |
| **mGBA** | Cross-platform | https://mgba.io/ |

**Install SameBoy (macOS):**
```bash
brew install sameboy
```

**Install mGBA (Linux):**
```bash
sudo apt install mgba-qt
```

---

### Development Tools

**VS Code Extensions:**
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
code --install-extension tamasfe.even-better-toml
```

**Git GUI:**
- **GitKraken:** https://www.gitkraken.com/
- **Sourcetree:** https://www.sourcetreeapp.com/
- **GitHub Desktop:** https://desktop.github.com/

---

## Next Steps

After installation:

1. **Read documentation:**
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [API.md](API.md) - Component documentation
   - [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guide

2. **Explore project:**
   ```bash
   # View project structure
   tree -L 2 .

   # Check recent events
   python -c "from .langflow.utils.logging import load_ledger; print(load_ledger()[-5:])"
   ```

3. **Build your first ROM:**
   ```bash
   make build-and-test
   make run-emulator
   ```

4. **Set up LangFlow workflow:**
   - Open http://localhost:7860
   - Import `.langflow/components/`
   - Create automation flow

5. **Run CI/CD locally:**
   ```bash
   # Simulate CI/CD pipeline
   python .langflow/components/ci_cd_pipeline.py
   ```

---

## Getting Help

**Resources:**

- **Documentation:** [`/docs`](.)
- **Issues:** [GitHub Issues](https://github.com/nitepoetlaureate/BarrySharpProMover/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nitepoetlaureate/BarrySharpProMover/discussions)
- **GB Studio Docs:** https://www.gbstudio.dev/docs/
- **LangFlow Docs:** https://docs.langflow.org/

**Community:**

- **GB Studio Discord:** https://discord.gg/bxerKnc
- **LangFlow Discord:** https://discord.gg/langflow

---

## Installation Checklist

Before proceeding with development:

- [ ] Python 3.9+ installed and verified
- [ ] Node.js 18+ installed
- [ ] Git and Git LFS configured
- [ ] GB Studio installed (CLI accessible)
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed (`pip install -e ".[dev]"`)
- [ ] LangFlow running (if using AI components)
- [ ] Repository cloned with LFS files
- [ ] Tests passing (`pytest`)
- [ ] ROM build successful (`make build-and-test`)
- [ ] Documentation reviewed

---

**Installation complete!** 🎉

You're ready to develop Barry Sharp Pro Mover. Check out [CONTRIBUTING.md](../CONTRIBUTING.md) to start contributing.

---

*Last Updated: 2025-11-21*
*For issues, please file at: https://github.com/nitepoetlaureate/BarrySharpProMover/issues*
