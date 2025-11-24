# Changelog

All notable changes to the BarrySharpProMover project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Phase 0: Critical Fixes - 2025-11-24

#### Added
- `.env.example` - Comprehensive environment configuration template with 100+ documented variables
- `scripts/validate_env.py` - Environment validation script with clear error messages
- `scripts/validation/validation_template.py` - Template for creating new validation scripts
- Comprehensive error handling to all validation scripts
- Proper exit codes for all Python scripts (0=success, 1=validation failure, 2=error, 130=cancelled)
- Structured logging with configurable levels across all validation scripts
- Type hints for improved code quality
- Detailed troubleshooting section in README.md
- Quick start guide with step-by-step setup instructions
- Build target validation in Makefile (`check-gbstudio`)

#### Changed
- **BREAKING:** Moved LangFlow components from `.langflow/components/` to `langflow_components/`
  - `gbstudio_build.py` → `langflow_components/tools/gbstudio_build.py`
  - All other components → `langflow_components/*.py`
  - Updated imports to use new structure
- **BREAKING:** Makefile now requires `GB_STUDIO_CLI_PATH` environment variable
  - Removed hardcoded path: `/Users/madisonmilesmedia/gb-studio/...`
  - Added automatic path detection (tries `command -v gb-studio-cli` first)
  - Loads configuration from `.env` file if present
- Completely rewrote `scripts/validation/check_bg_tiles.py` with:
  - Comprehensive error handling (file not found, permission denied, invalid image)
  - Structured logging with INFO/WARNING/ERROR levels
  - Proper exit codes for automation
  - Verbose mode (`-v` flag)
  - Better error messages with context
- Completely rewrote `scripts/validation/check_scene_limits.py` with:
  - JSON parsing error handling
  - Directory validation
  - Comprehensive error messages
  - Proper exit codes
  - Verbose mode support
- Updated `.gitignore` to include:
  - Environment files (`.env`, `.env.local`, `.env.*.local`)
  - Log directories (`logs/`, `*.log`)
  - Python artifacts (`__pycache__/`, `*.pyc`, `.pytest_cache/`)
  - Build artifacts (`build/*.gb`, `.cache/`)
  - Virtual environments (`venv/`, `langflow_env/`, etc.)
  - Project-specific patterns
- Completely rewrote `README.md` with:
  - Comprehensive quick start guide
  - Step-by-step environment setup
  - Detailed troubleshooting section
  - Asset validation documentation
  - Build command reference
  - LangFlow integration guide
- Enhanced Makefile with:
  - `.PHONY` targets for all commands
  - Environment variable support
  - GB Studio CLI path validation
  - Clearer success messages
  - `validate-all` target combining all validations

#### Fixed
- **CRITICAL:** Hardcoded GB Studio CLI paths prevented builds on any machine except original developer's
- **CRITICAL:** Component location mismatch causing import errors in LangFlow
- **HIGH:** Validation scripts had no error handling, causing silent failures
- **HIGH:** No environment configuration management, unclear setup requirements
- Missing executable permissions on validation scripts
- Inconsistent error messages across validation scripts
- No clear documentation for first-time setup
- Missing type hints in Python code
- Inconsistent logging patterns

#### Security
- Added `.env` to `.gitignore` to prevent accidental credential commits
- Externalized all configuration to environment variables
- Added security-focused variables in `.env.example` (API keys, tokens)
- Added file size and extension limits in environment configuration

#### Documentation
- Created `PROJECT_REVIEW_AND_IMPROVEMENT_PLAN.md` - Complete 5-phase roadmap (500+ lines)
- Created `CRITICAL_REVIEW_SUMMARY.md` - Executive summary and findings (300+ lines)
- Created `PHASE_0_CHECKLIST.md` - Step-by-step implementation guide (400+ lines)
- Created `CHANGELOG.md` - This file
- Created `CLAUDE.md` - AI assistant development notes
- Updated `README.md` with comprehensive setup and usage documentation

#### Validation
All Phase 0 changes validated empirically:
- ✅ Makefile syntax and environment variable loading
- ✅ Environment validation script with clear error messages
- ✅ All LangFlow component imports working correctly
- ✅ Validation scripts with proper error handling and exit codes
- ✅ `.env.example` created with comprehensive documentation
- ✅ `.gitignore` updated with security and development patterns
- ✅ File structure organized correctly
- ✅ README provides clear setup instructions

## [0.1.0] - 2023-11-15

### Added
- Initial GB Studio project structure
- LangFlow automation integration
- RAG (Retrieval-Augmented Generation) system with FAISS
- CI/CD pipeline component
- Enhanced file watcher with debouncing
- Basic validation scripts for backgrounds and scenes
- Automation control system
- Project state tracking and approval queue
- Build automation with Makefile
- Asset organization structure

### Components Implemented
- `ci_cd_pipeline.py` - Automated build, test, and deployment (370 LOC)
- `enhanced_file_watcher.py` - Real-time file monitoring (348 LOC)
- `file_watcher.py` - Basic file watcher (99 LOC)
- `gbstudio_build.py` - GB Studio CLI integration (66 LOC)
- `report_gen.py` - Status report generation (54 LOC)
- `notifier.py` - CLI notification system (19 LOC)
- `import_nodes.py` - Component installer (25 LOC)

---

## Version History

- **Unreleased** - Phase 0: Critical Fixes (2025-11-24)
- **0.1.0** - Initial Release (2023-11-15)

---

## Upgrade Guide

### From 0.1.0 to Unreleased (Phase 0)

**BREAKING CHANGES:**

1. **Environment Configuration Required**
   ```bash
   # Copy template
   cp .env.example .env

   # Edit and set GB_STUDIO_CLI_PATH
   nano .env

   # Validate
   python3 scripts/validate_env.py
   ```

2. **Component Imports Changed**
   ```python
   # OLD (will not work):
   from .langflow.components.gbstudio_build import GBStudioBuild

   # NEW:
   from langflow_components.tools.gbstudio_build import GBStudioBuild
   ```

3. **Build Command Changes**
   ```bash
   # Before running make build-rom, you must:
   make check-gbstudio

   # This validates GB Studio CLI is configured
   ```

**Migration Steps:**

1. Pull latest changes
2. Create `.env` from `.env.example`
3. Set `GB_STUDIO_CLI_PATH` in `.env`
4. Run `python3 scripts/validate_env.py`
5. Run `make check-gbstudio`
6. Update any custom scripts importing LangFlow components
7. Test build: `make build-rom`

---

## Notes

### Exit Code Standards

All Python scripts now follow consistent exit codes:
- `0` - Success
- `1` - Validation failure (expected errors, e.g., asset exceeds limits)
- `2` - Runtime error (unexpected errors, e.g., file not found)
- `130` - User cancellation (Ctrl+C)

### Logging Standards

All scripts use Python's `logging` module:
- `INFO` - Normal operations
- `WARNING` - Potential issues (e.g., non-standard dimensions)
- `ERROR` - Failures (e.g., validation failed, file not found)
- `DEBUG` - Detailed diagnostic information (use `-v` flag)

### Environment Variables

Required:
- `GB_STUDIO_CLI_PATH` - Path to GB Studio CLI executable

Optional:
- `OLLAMA_HOST` - Ollama server URL (default: http://localhost:11434)
- `LANGFLOW_PORT` - LangFlow port (default: 7860)
- `LANGFLOW_HOST` - LangFlow host (default: 127.0.0.1)
- `LOG_LEVEL` - Logging level (default: INFO)
- See `.env.example` for complete list

---

**For detailed development roadmap, see `PROJECT_REVIEW_AND_IMPROVEMENT_PLAN.md`**
