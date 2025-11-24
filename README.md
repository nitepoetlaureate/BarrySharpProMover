# Barry Sharp Pro Mover - GB Studio Game Project

A Game Boy game developed using GB Studio with integrated LangFlow automation and build tools.

## 🚀 Quick Start

### 1. Prerequisites

Before you begin, ensure you have the following installed:
- **GB Studio** 4.1.0+ (with CLI tools) - [Download](https://www.gbstudio.dev/)
- **Node.js** 16+ (for GB Studio CLI)
- **Python** 3.11+ (for validation scripts and automation)
- **Git** (for version control)
- **Ollama** (optional, for RAG/AI features) - [Install](https://ollama.ai/)

### 2. Environment Setup

**Step 1: Copy environment template**
```bash
cp .env.example .env
```

**Step 2: Configure GB Studio CLI path**

Find your GB Studio CLI path:
```bash
# macOS
find /Applications/GB\ Studio.app -name gb-studio-cli.js

# Linux
which gb-studio-cli || find /opt /usr/local -name gb-studio-cli.js

# Windows
where gb-studio-cli.js
```

Edit `.env` and set your path:
```bash
GB_STUDIO_CLI_PATH=/path/to/your/gb-studio-cli.js
```

**Step 3: Install Python dependencies**
```bash
# Install python-dotenv for environment management
pip install python-dotenv

# Install Pillow for image validation
pip install Pillow

# Optional: Install LangFlow for automation
pip install langflow
```

**Step 4: Validate your environment**
```bash
python3 scripts/validate_env.py
```

You should see:
```
✅ Environment configuration is valid!
```

**Step 5: Verify GB Studio configuration**
```bash
make check-gbstudio
```

You should see:
```
✅ GB Studio CLI found: /path/to/gb-studio-cli.js
```

### 3. Building the Game

```bash
# Build ROM file
make build-rom

# Build web version
make build-web

# Validate all assets before building
make validate-all
```

### 4. Development Workflow

```bash
# Validate background images
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

# Validate scene limits (if you have scenes)
python3 scripts/validation/check_scene_limits.py project/scenes/

# Run all validations
make validate-all
```

## 📁 Project Structure

### Core Game Files
- `BARRY-SHARP-PRO-MOVER-1.gbsproj` - Main GB Studio project file
- `assets/` - All game assets (sprites, backgrounds, music, sounds, etc.)
- `build/` - Compiled game outputs (ROM and web builds)

### Development Tools
- `Makefile` - Build automation using GB Studio CLI
- `scripts/` - Development and validation scripts
  - `build/` - Build-related scripts
  - `validation/` - Asset validation tools
  - `validate_env.py` - Environment configuration validator
- `langflow_components/` - Custom LangFlow components for automation
- `.langflow/` - LangFlow workflow definitions and configuration

### Documentation
- `docs/` - Project documentation organized by category
  - `design/` - Game design documents
  - `shared/` - General project documentation
  - `AUTOMATION_GUIDE.md` - Comprehensive automation guide
- `PROJECT_REVIEW_AND_IMPROVEMENT_PLAN.md` - Development roadmap
- `CRITICAL_REVIEW_SUMMARY.md` - Project status and issues
- `PHASE_0_CHECKLIST.md` - Critical fixes checklist

### Project Management
- `memory/` - Project state and approval tracking
- `feedback/` - User feedback and testing results
- `staging/` - Temporary staging area for outputs
- `vectorstore/` - Knowledge base storage (RAG system)

## 🎮 Building the Game

### Build Commands

```bash
# Build ROM file
make build-rom
# Output: build/rom.gb

# Build web version
make build-web
# Output: build/index.html

# Build and generate ROM hash
make hash-rom
# Output: build/rom.md5

# Clean build artifacts
make clean
```

### Build Targets

- `build-rom` - Compile Game Boy ROM file
- `build-web` - Build web-playable version
- `build-and-test` - Build ROM and launch in emulator
- `hash-rom` - Build ROM and generate MD5 hash
- `check-gbstudio` - Verify GB Studio CLI is configured
- `build-dirs` - Create build directory structure

## ✅ Asset Validation

### Validation Scripts

```bash
# Check background tile counts (must be ≤192 tiles)
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

# Check scene limits (actors, triggers, sprites)
python3 scripts/validation/check_scene_limits.py project/scenes/

# Validate all assets
make validate-all
```

### Validation Limits

- **Background Tiles:** Maximum 192 unique tiles per background
- **Background Dimensions:** 160x144 pixels (GB screen size)
- **Scene Actors:** Maximum 20 actors per scene
- **Scene Triggers:** Maximum 30 triggers per scene
- **Sprite Tiles:** Maximum 96 sprite tiles per scene

## 🔧 Development Scripts

### Validation
- `scripts/validation/check_bg_tiles.py` - Validate background images
- `scripts/validation/check_scene_limits.py` - Validate scene limits
- `scripts/validation/validation_template.py` - Template for new validators
- `scripts/validate_env.py` - Validate environment configuration

### Build & Automation
- `scripts/automation_control.sh` - Start/stop automation system
- `scripts/build_rag.py` - Build RAG knowledge bases
- `scripts/test_rag.py` - Test RAG system interactively
- `scripts/sync_gbsres.sh` - Sync GB Studio resources
- `scripts/snapshot.sh` - Create project snapshot

## 🤖 LangFlow Integration (Optional)

### Setup LangFlow

```bash
# Install LangFlow
pip install langflow

# Start LangFlow server
./start_langflow.sh

# Access LangFlow UI
# Open browser to: http://127.0.0.1:7860
```

### Automation Features

- **CI/CD Pipeline** - Automated build, test, and deployment
- **File Watcher** - Real-time monitoring of project files
- **Status Reporting** - Comprehensive project health reports
- **RAG System** - AI-powered documentation search

See `docs/AUTOMATION_GUIDE.md` for detailed instructions.

## 📦 Asset Organization

All game assets are consolidated in the `assets/` directory:

```
assets/
├── backgrounds/     # Background images (160x144 PNG)
├── sprites/         # Character and object sprites
├── music/           # Background music files
├── sounds/          # Sound effects
├── fonts/           # Custom fonts
├── palettes/        # Color palettes
├── tilesets/        # Tile graphics
├── ui/              # User interface elements
├── avatars/         # Character avatars
└── emotes/          # Emote sprites
```

## 📋 Requirements

### Required
- **GB Studio** 4.1.0+ with CLI tools
- **Node.js** 16+ (for GB Studio CLI)
- **Python** 3.11+ (for validation scripts)
- **Pillow** (Python image library)
- **python-dotenv** (Environment management)

### Optional
- **LangFlow** 1.4+ (for automation workflows)
- **Ollama** (for RAG/AI features)
  - `nomic-embed-text` model (embeddings)
  - `mistral` model (LLM responses)

### Installation

```bash
# Install Python dependencies
pip install Pillow python-dotenv

# Optional: Install LangFlow
pip install langflow

# Optional: Install Ollama and pull models
# See: https://ollama.ai/
ollama pull nomic-embed-text
ollama pull mistral
```

## 🐛 Troubleshooting

### Common Issues

**"GB Studio CLI not found"**
```bash
# Verify your .env file has the correct path
cat .env | grep GB_STUDIO_CLI_PATH

# Find the correct path
find /Applications -name gb-studio-cli.js 2>/dev/null
```

**"Permission denied" on scripts**
```bash
# Make scripts executable
chmod +x scripts/validation/*.py
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

**"Module not found" errors**
```bash
# Install missing Python packages
pip install Pillow python-dotenv langflow
```

**Validation fails with "too many tiles"**
- Reduce colors in your background image
- Use more repeated tiles
- Optimize with tools like [GB Studio Tileset Optimizer](https://github.com/pau-tomas/gb-studio-tileset-optimizer)

## 📚 Documentation

### Project Documentation
- `PROJECT_REVIEW_AND_IMPROVEMENT_PLAN.md` - Complete 5-phase development roadmap
- `CRITICAL_REVIEW_SUMMARY.md` - Project status and critical issues
- `PHASE_0_CHECKLIST.md` - Critical fixes implementation guide
- `docs/AUTOMATION_GUIDE.md` - Comprehensive automation system guide
- `docs/design/01-game-design-document.md` - Game design specification

### External Resources
- [GB Studio Documentation](https://www.gbstudio.dev/docs/)
- [LangFlow Documentation](https://docs.langflow.org/)
- [Ollama Documentation](https://github.com/ollama/ollama)

## 🤝 Contributing

This project follows a validation-first approach:
1. All code must pass validation (`make validate-all`)
2. Maintain test coverage (see `PROJECT_REVIEW_AND_IMPROVEMENT_PLAN.md`)
3. Follow the Phase 0-5 development plan
4. Update documentation with changes

See `CONTRIBUTING.md` (coming soon) for detailed guidelines.

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- Built with [GB Studio](https://www.gbstudio.dev/)
- Automated with [LangFlow](https://www.langflow.org/)
- AI features powered by [Ollama](https://ollama.ai/)

---

**Quick Links:**
- 🚀 [Quick Start](#-quick-start)
- 📖 [Documentation](#-documentation)
- 🔧 [Development Scripts](#-development-scripts)
- 🤖 [LangFlow Integration](#-langflow-integration-optional)
- 🐛 [Troubleshooting](#-troubleshooting)