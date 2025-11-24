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

# Validation targets
.PHONY: check-bg
check-bg:
	python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

.PHONY: check-scenes
check-scenes:
	python3 scripts/validation/check_scene_limits.py project/scenes/

.PHONY: check-json
check-json:
	find . -name "*.json" -exec jq . {} \;

.PHONY: validate-all
validate-all: check-bg check-scenes
	@echo "✅ All validations passed"

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