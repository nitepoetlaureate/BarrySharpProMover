# GB Studio Build Automation Targets

# GB Studio CLI path detection (cross-platform)
# Set GB_STUDIO_CLI environment variable to override
GB_STUDIO_CLI ?= $(shell \
	if command -v gbstudio-cli >/dev/null 2>&1; then \
		echo "gbstudio-cli"; \
	elif [ -f "/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js" ]; then \
		echo "/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js"; \
	elif [ -f "$$HOME/gb-studio/out/cli/gb-studio-cli.js" ]; then \
		echo "$$HOME/gb-studio/out/cli/gb-studio-cli.js"; \
	else \
		echo "gb-studio-cli-not-found"; \
	fi)

# Ensure build directories exist
build-dirs:
	@mkdir -p build

# Validation targets
check-bg:
	@python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

check-scenes:
	@python3 scripts/validation/check_scene_limits.py project/scenes/

check-json:
	@find . -name "*.json" -exec jq . {} \;

# Build targets
build-rom:
	@if [ "$(GB_STUDIO_CLI)" = "gb-studio-cli-not-found" ]; then \
		echo "ERROR: GB Studio CLI not found."; \
		echo "Please set GB_STUDIO_CLI environment variable or install GB Studio."; \
		echo "Example: export GB_STUDIO_CLI=/path/to/gb-studio-cli.js"; \
		exit 1; \
	fi
	node "$(GB_STUDIO_CLI)" export BARRY-SHARP-PRO-MOVER-1.gbsproj build/
	node "$(GB_STUDIO_CLI)" make:rom BARRY-SHARP-PRO-MOVER-1.gbsproj build/game.gb
	cp build/game.gb build/rom.gb

build-web:
	@if [ "$(GB_STUDIO_CLI)" = "gb-studio-cli-not-found" ]; then \
		echo "ERROR: GB Studio CLI not found."; \
		echo "Please set GB_STUDIO_CLI environment variable."; \
		exit 1; \
	fi
	node "$(GB_STUDIO_CLI)" make:web BARRY-SHARP-PRO-MOVER-1.gbsproj build/

build-and-test: build-rom
	./scripts/build/launch_openemu.sh

hash-rom: build-rom
	@md5sum ./build/rom.gb > ./build/rom.md5

.PHONY: build-dirs check-bg check-scenes check-json build-rom build-web build-and-test hash-rom