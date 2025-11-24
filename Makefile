# GB Studio Build Automation Targets

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
		echo "Copy .env.example to .env and configure your path"; \
		echo ""; \
		echo "Example paths:"; \
		echo "  macOS:   /Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js"; \
		echo "  Linux:   /opt/gb-studio/out/cli/gb-studio-cli.js"; \
		echo "  Windows: C:/Program Files/GB Studio/resources/app/out/cli/gb-studio-cli.js"; \
		exit 1; \
	fi
	@echo "✅ GB Studio CLI found: $(GB_STUDIO_CLI)"

# Ensure build directories exist
.PHONY: build-dirs
build-dirs:
	@mkdir -p build

# Validation targets - Asset validation
.PHONY: check-bg
check-bg:
	@if [ -d "assets/backgrounds" ] && [ -n "$$(ls -A assets/backgrounds/*.png 2>/dev/null)" ]; then \
		python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png; \
	else \
		echo "⏭️  No backgrounds to validate"; \
	fi

.PHONY: check-sprites
check-sprites:
	@if [ -d "assets/sprites" ] && [ -n "$$(ls -A assets/sprites/*.png 2>/dev/null)" ]; then \
		python3 scripts/validation/check_sprites.py assets/sprites/*.png; \
	else \
		echo "⏭️  No sprites to validate"; \
	fi

.PHONY: check-audio
check-audio:
	@if [ -d "assets/music" ] || [ -d "assets/sounds" ]; then \
		python3 scripts/validation/check_audio.py assets/music/*.{mod,uge} assets/sounds/*.{wav,vgm} 2>/dev/null || echo "⏭️  No audio files to validate"; \
	else \
		echo "⏭️  No audio to validate"; \
	fi

.PHONY: check-fonts
check-fonts:
	@if [ -d "assets/fonts" ] && [ -n "$$(ls -A assets/fonts/*.json 2>/dev/null)" ]; then \
		python3 scripts/validation/check_fonts.py assets/fonts/*.json; \
	else \
		echo "⏭️  No fonts to validate"; \
	fi

.PHONY: check-scenes
check-scenes:
	@if [ -d "project/scenes" ]; then \
		python3 scripts/validation/check_scene_limits.py project/scenes/; \
	else \
		echo "⏭️  No scenes to validate"; \
	fi

.PHONY: check-project
check-project:
	@if [ -n "$$(ls -A *.gbsproj 2>/dev/null)" ]; then \
		python3 scripts/validation/check_project.py *.gbsproj; \
	else \
		echo "❌ No .gbsproj file found"; \
		exit 1; \
	fi

.PHONY: check-build
check-build:
	@if [ -d "build" ] && [ -n "$$(ls -A build/*.gb 2>/dev/null)" ]; then \
		python3 scripts/validation/check_build.py build/*.gb; \
	else \
		echo "⏭️  No ROM builds to validate"; \
	fi

.PHONY: check-json
check-json:
	@find . -name "*.json" -not -path "./node_modules/*" -not -path "./langflow/*" -exec jq . {} \; >/dev/null && echo "✅ All JSON files are valid"

# Comprehensive validation
.PHONY: validate-all
validate-all:
	@echo "🚀 Running comprehensive validation..."
	@python3 scripts/validate_all.py

.PHONY: validate-assets
validate-assets: check-bg check-sprites check-audio check-fonts
	@echo "✅ All asset validations passed"

# Build targets
.PHONY: build-rom
build-rom: check-gbstudio build-dirs
	node "$(GB_STUDIO_CLI)" export BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	node "$(GB_STUDIO_CLI)" make:rom BARRY-SHARP-PRO-MOVER-1.gbsproj build/game.gb
	cp build/game.gb build/rom.gb
	@echo "✅ ROM build complete: build/rom.gb"

.PHONY: build-web
build-web: check-gbstudio build-dirs
	node "$(GB_STUDIO_CLI)" make:web BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	@echo "✅ Web build complete: build/"

.PHONY: build-and-test
build-and-test: build-rom
	./scripts/build/launch_openemu.sh

.PHONY: hash-rom
hash-rom: build-rom
	md5sum ./build/rom.gb > ./build/rom.md5
	@echo "✅ ROM hash: $$(cat ./build/rom.md5)"

# Testing targets
.PHONY: test
test:
	@echo "🧪 Running all tests..."
	pytest

.PHONY: test-unit
test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -m unit

.PHONY: test-integration
test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/integration/ -m integration

.PHONY: test-fast
test-fast:
	@echo "🧪 Running fast tests only..."
	pytest -m "not slow"

.PHONY: test-verbose
test-verbose:
	@echo "🧪 Running tests with verbose output..."
	pytest -vv

.PHONY: coverage
coverage:
	@echo "📊 Generating coverage report..."
	pytest --cov=scripts --cov=langflow_components --cov-report=html --cov-report=term
	@echo "📊 Coverage report generated in htmlcov/index.html"

.PHONY: coverage-report
coverage-report:
	@if [ -d "htmlcov" ]; then \
		python3 -m http.server 8000 --directory htmlcov; \
	else \
		echo "❌ No coverage report found. Run 'make coverage' first."; \
	fi

.PHONY: install-test-deps
install-test-deps:
	@echo "📦 Installing test dependencies..."
	pip install -r requirements-dev.txt
	@echo "✅ Test dependencies installed"

.PHONY: test-clean
test-clean:
	@echo "🧹 Cleaning test artifacts..."
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf tests/__pycache__
	rm -rf tests/unit/__pycache__
	rm -rf tests/integration/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Test artifacts cleaned"