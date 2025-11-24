# Phase 0: Critical Fixes - Action Checklist
**Goal:** Fix blocking issues that prevent basic functionality
**Timeline:** 1-2 days
**Priority:** 🔴 CRITICAL - Must complete before any other work

---

## 📋 QUICK START CHECKLIST

Use this checklist to systematically address critical issues.

---

## ✅ TASK 0.1: Fix Hardcoded GB Studio Paths

**Current Issue:** `Makefile` contains `/Users/madisonmilesmedia/gb-studio/...`
**Impact:** Build fails on any other machine
**Estimated Time:** 30-45 minutes

### Steps:

#### Step 1: Create Environment Configuration Template
- [ ] Create `.env.example` file in project root:
```bash
# GB Studio Configuration
GB_STUDIO_CLI_PATH=/path/to/gb-studio/out/cli/gb-studio-cli.js
# Example paths:
# macOS: /Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js
# Linux: /opt/gb-studio/out/cli/gb-studio-cli.js
# Windows: C:/Program Files/GB Studio/resources/app/out/cli/gb-studio-cli.js

# LangFlow Configuration
LANGFLOW_PORT=7860
LANGFLOW_HOST=127.0.0.1

# RAG System Configuration
OLLAMA_HOST=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=mistral

# Build Configuration
BUILD_DIR=build
ROM_NAME=game.gb
```

#### Step 2: Update Makefile to Use Environment Variable
- [ ] Open `Makefile`
- [ ] Add environment variable handling at the top:
```makefile
# Load environment variables from .env if it exists
-include .env
export

# GB Studio CLI path - use environment variable or try to find in PATH
GB_STUDIO_CLI ?= $(shell command -v gb-studio-cli 2>/dev/null || echo "$$GB_STUDIO_CLI_PATH")

# Validate GB Studio CLI is available
.PHONY: check-gbstudio
check-gbstudio:
	@if [ -z "$(GB_STUDIO_CLI)" ] || [ ! -f "$(GB_STUDIO_CLI)" ]; then \
		echo "❌ ERROR: GB Studio CLI not found"; \
		echo "Please set GB_STUDIO_CLI_PATH in .env file"; \
		echo "Example: GB_STUDIO_CLI_PATH=/path/to/gb-studio/out/cli/gb-studio-cli.js"; \
		exit 1; \
	fi
	@echo "✅ GB Studio CLI found: $(GB_STUDIO_CLI)"
```

- [ ] Update `build-rom` target:
```makefile
build-rom: check-gbstudio build-dirs
	node "$(GB_STUDIO_CLI)" export BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	node "$(GB_STUDIO_CLI)" make:rom BARRY-SHARP-PRO-MOVER-1.gbsproj build/game.gb
	cp build/game.gb build/rom.gb
```

- [ ] Update `build-web` target:
```makefile
build-web: check-gbstudio build-dirs
	node "$(GB_STUDIO_CLI)" make:web BARRY-SHARP-PRO-MOVER-1.gbsproj build/
```

#### Step 3: Update README with Setup Instructions
- [ ] Add to README.md under "Requirements" section:
```markdown
## Setup

### 1. Configure Environment Variables

Copy the environment template:
```bash
cp .env.example .env
```

Edit `.env` and set your GB Studio CLI path:
```bash
# Find your GB Studio CLI path
# macOS:
find /Applications/GB\ Studio.app -name gb-studio-cli.js

# Linux:
which gb-studio-cli || find /opt /usr/local -name gb-studio-cli.js

# Then add to .env:
GB_STUDIO_CLI_PATH=/path/to/your/gb-studio-cli.js
```

### 2. Verify Setup

```bash
make check-gbstudio
```

If successful, you should see:
```
✅ GB Studio CLI found: /path/to/gb-studio-cli.js
```
```

#### Step 4: Add .env to .gitignore
- [ ] Verify `.env` is in `.gitignore`:
```bash
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

#### Step 5: Test on Different Environment
- [ ] Create `.env` file from template
- [ ] Set GB_STUDIO_CLI_PATH to your actual path
- [ ] Run: `make check-gbstudio`
- [ ] Run: `make build-rom` (if GB Studio is installed)
- [ ] Verify build completes without hardcoded path errors

### Acceptance Criteria:
- ✅ `.env.example` exists with clear documentation
- ✅ Makefile uses `$(GB_STUDIO_CLI)` variable
- ✅ `make check-gbstudio` validates setup
- ✅ Clear error message if GB Studio not configured
- ✅ README documents setup process
- ✅ `.env` in `.gitignore`

---

## ✅ TASK 0.2: Resolve Component Location Mismatch

**Current Issue:** Components in `.langflow/components/` but `pyproject.toml` expects `langflow_components/`
**Impact:** LangFlow components fail to import
**Estimated Time:** 20-30 minutes

### Steps:

#### Step 1: Decide on Approach
**Recommended:** Move components to `langflow_components/` (cleaner structure)

#### Step 2: Move Components
- [ ] Create proper structure:
```bash
mkdir -p langflow_components/tools
```

- [ ] Move components:
```bash
mv .langflow/components/gbstudio_build.py langflow_components/tools/
mv .langflow/components/ci_cd_pipeline.py langflow_components/
mv .langflow/components/enhanced_file_watcher.py langflow_components/
mv .langflow/components/file_watcher.py langflow_components/
mv .langflow/components/report_gen.py langflow_components/
mv .langflow/components/notifier.py langflow_components/
mv .langflow/components/import_nodes.py langflow_components/
```

- [ ] Create `__init__.py` files:
```bash
touch langflow_components/__init__.py
touch langflow_components/tools/__init__.py
```

#### Step 3: Update Imports in LangFlow Flows
This is critical - the JSON flow files may reference the old paths.

- [ ] Check flow files for component references:
```bash
grep -r "\.langflow\.components" .langflow/flows/
```

- [ ] Update any references from `.langflow.components` to `langflow_components`

#### Step 4: Verify pyproject.toml Configuration
- [ ] Open `pyproject.toml`
- [ ] Verify entry point:
```toml
[project.entry-points."langflow_components"]
gbstudio-build = "langflow_components.tools.gbstudio_build:GBStudioBuild"
```

#### Step 5: Test Component Imports
- [ ] Test Python import:
```bash
python3 -c "from langflow_components.tools.gbstudio_build import GBStudioBuild; print('✅ Import successful')"
```

- [ ] Test other components:
```bash
python3 -c "from langflow_components.ci_cd_pipeline import CICDPipeline; print('✅ CI/CD import successful')"
python3 -c "from langflow_components.enhanced_file_watcher import EnhancedFileWatcher; print('✅ File watcher import successful')"
```

#### Step 6: Clean Up Old Location
- [ ] Remove old components directory (after confirming imports work):
```bash
rm -rf .langflow/components/*.py
```
- [ ] Keep `.langflow/components/registry.json` if it exists

### Acceptance Criteria:
- ✅ All components in `langflow_components/`
- ✅ Proper `__init__.py` files created
- ✅ All Python imports working
- ✅ No orphaned files in `.langflow/components/`
- ✅ LangFlow flows load without errors

---

## ✅ TASK 0.3: Add Error Handling to Validation Scripts

**Current Issue:** Validation scripts lack try/except blocks and error recovery
**Impact:** Silent failures, unclear error messages
**Estimated Time:** 45-60 minutes

### Steps:

#### Step 1: Update check_bg_tiles.py

- [ ] Open `scripts/validation/check_bg_tiles.py`
- [ ] Add imports at top:
```python
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)
```

- [ ] Wrap main logic in error handling:
```python
def validate_background(path: str) -> bool:
    """Validate a single background image."""
    try:
        if not os.path.isfile(path):
            logger.error(f"File not found: {path}")
            return False

        img = Image.open(path)
        width, height = img.size

        if width != 160 or height != 144:
            logger.warning(f"{os.path.basename(path)}: Size is {width}x{height}, expected 160x144")

        tiles = get_tiles(img)
        tile_count = len(tiles)

        if tile_count > MAX_TILES:
            logger.error(f"{os.path.basename(path)}: {tile_count} tiles (limit is {MAX_TILES})")
            return False
        else:
            logger.info(f"{os.path.basename(path)}: {tile_count} tiles OK")
            return True

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return False
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        return False
    except Exception as e:
        logger.error(f"Error processing {path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Check GB Studio background tile counts")
    parser.add_argument("files", nargs='+', help="Path(s) to PNG files")
    args = parser.parse_args()

    all_valid = True
    for path in args.files:
        if not validate_background(path):
            all_valid = False

    # Exit with appropriate code
    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Validation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(2)
```

#### Step 2: Update check_scene_limits.py

- [ ] Apply same pattern to `scripts/validation/check_scene_limits.py`
- [ ] Add logging, error handling, proper exit codes
- [ ] Test with valid and invalid inputs

#### Step 3: Create Validation Script Template

- [ ] Create `scripts/validation/validation_template.py` for future validators:
```python
#!/usr/bin/env python3
"""
Template for validation scripts.
Copy this file and modify for specific validation needs.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def validate_item(path: Path) -> Tuple[bool, str]:
    """
    Validate a single item.

    Args:
        path: Path to item to validate

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        # Validation logic here
        return True, f"{path.name}: OK"

    except FileNotFoundError:
        return False, f"File not found: {path}"
    except PermissionError:
        return False, f"Permission denied: {path}"
    except Exception as e:
        return False, f"Error processing {path}: {e}"


def main():
    parser = argparse.ArgumentParser(description="Validate items")
    parser.add_argument("files", nargs='+', help="Path(s) to files")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    all_valid = True
    for file_path in args.files:
        path = Path(file_path)
        is_valid, message = validate_item(path)

        if is_valid:
            logger.info(f"✅ {message}")
        else:
            logger.error(f"❌ {message}")
            all_valid = False

    # Exit codes: 0 = success, 1 = validation failure, 2 = error
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\\nValidation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(2)
```

#### Step 4: Test Updated Scripts

- [ ] Test `check_bg_tiles.py` with valid backgrounds:
```bash
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png
echo "Exit code: $?"
```

- [ ] Test with non-existent file:
```bash
python3 scripts/validation/check_bg_tiles.py /nonexistent/file.png
echo "Exit code: $?"  # Should be 1 or 2
```

- [ ] Test with invalid file type:
```bash
python3 scripts/validation/check_bg_tiles.py README.md
echo "Exit code: $?"  # Should be 1 or 2
```

### Acceptance Criteria:
- ✅ All file operations wrapped in try/except
- ✅ Clear error messages for common failures
- ✅ Proper exit codes (0=success, 1=validation fail, 2=error, 130=cancel)
- ✅ Logging throughout with appropriate levels
- ✅ Template created for future validators

---

## ✅ TASK 0.4: Create Comprehensive .env.example

**Current Issue:** No environment configuration documentation
**Impact:** Unclear setup requirements
**Estimated Time:** 20-30 minutes

### Steps:

#### Step 1: Create Comprehensive .env.example

- [ ] Create `.env.example` in project root:
```bash
# BarrySharpProMover Environment Configuration
# Copy this file to .env and configure for your environment
# DO NOT commit .env to version control!

# ======================================
# GB Studio Configuration (REQUIRED)
# ======================================

# Path to GB Studio CLI
# Find with: find /Applications/GB\ Studio.app -name gb-studio-cli.js (macOS)
GB_STUDIO_CLI_PATH=/path/to/gb-studio/out/cli/gb-studio-cli.js

# ======================================
# LangFlow Configuration
# ======================================

# LangFlow server settings
LANGFLOW_PORT=7860
LANGFLOW_HOST=127.0.0.1

# ======================================
# RAG System Configuration
# ======================================

# Ollama server URL (must be running for RAG features)
OLLAMA_HOST=http://localhost:11434

# Embedding model for vector storage
EMBEDDING_MODEL=nomic-embed-text

# LLM model for RAG responses
LLM_MODEL=mistral

# ======================================
# Build Configuration
# ======================================

# Build output directory
BUILD_DIR=build

# ROM output filename
ROM_NAME=game.gb

# Enable debug mode for verbose build output
DEBUG_MODE=false

# ======================================
# Automation Configuration
# ======================================

# Auto-run tests after build
AUTO_TEST=true

# File watcher debounce time (seconds)
FILE_WATCHER_DEBOUNCE=5

# ======================================
# Notification Configuration (Optional)
# ======================================

# Email notifications
NOTIFY_EMAIL=

# Slack webhook for build notifications
NOTIFY_SLACK_WEBHOOK=

# Discord webhook for build notifications
NOTIFY_DISCORD_WEBHOOK=

# ======================================
# API Keys (SENSITIVE - DO NOT COMMIT)
# ======================================

# Google API key for integrations
GOOGLE_API_KEY=

# GitHub token for automation
GITHUB_TOKEN=

# ======================================
# Development Options
# ======================================

# Python log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Enable development mode features
DEV_MODE=false

# Project root (auto-detected if not set)
PROJECT_ROOT=
```

#### Step 2: Update .gitignore

- [ ] Ensure `.gitignore` includes:
```bash
# Environment configuration
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# Build artifacts
build/
*.gb
*.pocket

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
venv/
.pytest_cache/
```

#### Step 3: Create Setup Validation Script

- [ ] Create `scripts/validate_env.py`:
```python
#!/usr/bin/env python3
"""Validate environment configuration."""

import os
import sys
from pathlib import Path

def validate_env():
    """Validate required environment variables."""
    print("🔍 Validating environment configuration...")
    print()

    errors = []
    warnings = []

    # Check required variables
    required = {
        'GB_STUDIO_CLI_PATH': 'GB Studio CLI path'
    }

    for var, description in required.items():
        value = os.getenv(var)
        if not value:
            errors.append(f"❌ {var} not set ({description})")
        elif not Path(value).exists():
            errors.append(f"❌ {var} path does not exist: {value}")
        else:
            print(f"✅ {var}: {value}")

    # Check optional variables
    optional = {
        'OLLAMA_HOST': 'Ollama server URL',
        'LANGFLOW_PORT': 'LangFlow port',
    }

    for var, description in optional.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            warnings.append(f"⚠️  {var} not set ({description})")

    print()

    # Print warnings
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    # Print errors and exit if any
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  {error}")
        print()
        print("💡 Copy .env.example to .env and configure required variables")
        sys.exit(1)

    print("✅ Environment configuration is valid!")
    return 0

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        print("Checking environment variables anyway...")

    sys.exit(validate_env())
```

- [ ] Make executable:
```bash
chmod +x scripts/validate_env.py
```

#### Step 4: Update README with Setup Instructions

- [ ] Add to README.md:
```markdown
## Environment Setup

### 1. Copy environment template

```bash
cp .env.example .env
```

### 2. Configure required variables

Edit `.env` and set at minimum:

- `GB_STUDIO_CLI_PATH`: Path to your GB Studio CLI installation

### 3. Validate configuration

```bash
python3 scripts/validate_env.py
```

### 4. Install Python dependencies

```bash
pip install python-dotenv
```

For full functionality:
```bash
pip install -r requirements.txt
```
```

#### Step 5: Update All Scripts to Load .env

- [ ] Add to top of `build_rag.py`, `test_rag.py`, and other scripts:
```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Use environment variables
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
```

### Acceptance Criteria:
- ✅ Comprehensive `.env.example` with all variables documented
- ✅ `.env` in `.gitignore`
- ✅ Validation script to check configuration
- ✅ README updated with setup instructions
- ✅ No hardcoded configuration in scripts

---

## 📊 PHASE 0 COMPLETION CHECKLIST

### All Tasks Complete When:

- [ ] **Task 0.1:** Makefile uses environment variables for GB Studio path
- [ ] **Task 0.2:** All LangFlow components import correctly
- [ ] **Task 0.3:** Validation scripts have comprehensive error handling
- [ ] **Task 0.4:** Environment configuration documented and validated

### Validation:

- [ ] Build works on at least 2 different machines/users
- [ ] Clear error message if environment not configured
- [ ] All validation scripts handle errors gracefully
- [ ] README documents setup process clearly
- [ ] No hardcoded paths or credentials in repository

### Exit Criteria:

Run these commands successfully:

```bash
# Validate environment
python3 scripts/validate_env.py

# Check GB Studio configuration
make check-gbstudio

# Test validation scripts
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

# Test component imports
python3 -c "from langflow_components.tools.gbstudio_build import GBStudioBuild"

# Attempt build (if GB Studio installed)
make build-rom
```

All should complete without errors or with clear, actionable error messages.

---

## 🎯 SUCCESS METRICS

### Phase 0 is complete when:
✅ Build portability: Works on 3+ different machines
✅ Error handling: All validation scripts have try/except blocks
✅ Configuration: All configuration externalized to .env
✅ Documentation: Setup process documented in README
✅ Validation: Environment validation script passes

---

## 📝 NOTES

### Common Issues:

**GB Studio CLI Path:**
- macOS: Usually in `/Applications/GB Studio.app/Contents/Resources/app/out/cli/`
- Linux: Check `/usr/local/bin/` or `/opt/`
- Windows: Check `C:\Program Files\GB Studio\resources\app\out\cli\`

**Component Import Errors:**
- Ensure `__init__.py` files exist in all package directories
- Check Python path includes project root
- Verify file names match import statements

**Validation Script Errors:**
- Install Pillow: `pip install Pillow`
- Check file permissions on asset directories
- Ensure running from project root

---

## 🚀 NEXT PHASE

Once Phase 0 is complete, proceed to:
**Phase 1: Validation Infrastructure** - See `PROJECT_REVIEW_AND_IMPROVEMENT_PLAN.md`

---

**Document Version:** 1.0
**Last Updated:** 2025-11-24
