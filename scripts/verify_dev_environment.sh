#!/bin/bash
# Development Environment Verification Script
# This script checks that all required tools and dependencies are properly installed

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  Barry Sharp Pro Mover"
echo "  Development Environment Verification"
echo "=========================================="
echo ""

# Track overall status
ALL_CHECKS_PASSED=true

# Function to check command existence
check_command() {
    local cmd=$1
    local name=$2
    local version_flag=$3

    if command -v "$cmd" &> /dev/null; then
        local version=$($cmd $version_flag 2>&1 | head -1)
        echo -e "${GREEN}✓${NC} $name: $version"
        return 0
    else
        echo -e "${RED}✗${NC} $name: NOT FOUND"
        ALL_CHECKS_PASSED=false
        return 1
    fi
}

# Function to check directory existence
check_directory() {
    local dir=$1
    local name=$2

    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $name: $dir"
        return 0
    else
        echo -e "${RED}✗${NC} $name: NOT FOUND at $dir"
        ALL_CHECKS_PASSED=false
        return 1
    fi
}

# Function to check file existence
check_file() {
    local file=$1
    local name=$2

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $name: $file"
        return 0
    else
        echo -e "${RED}✗${NC} $name: NOT FOUND at $file"
        ALL_CHECKS_PASSED=false
        return 1
    fi
}

# Function to check Python package
check_python_package() {
    local package=$1
    local name=$2

    if python3 -c "import $package" &> /dev/null; then
        local version=$(python3 -c "import $package; print(getattr($package, '__version__', 'installed'))" 2>&1)
        echo -e "${GREEN}✓${NC} $name: $version"
        return 0
    else
        echo -e "${RED}✗${NC} $name: NOT INSTALLED"
        ALL_CHECKS_PASSED=false
        return 1
    fi
}

echo "=== Core System Tools ==="
check_command "python3" "Python" "--version"
check_command "node" "Node.js" "--version"
check_command "npm" "npm" "--version"
check_command "make" "Make" "--version"
check_command "git" "Git" "--version"
echo ""

echo "=== GB Studio CLI ==="
if command -v gb-studio &> /dev/null; then
    check_command "gb-studio" "GB Studio CLI" "--version"
else
    echo -e "${YELLOW}⚠${NC}  GB Studio CLI: Not in PATH"
    echo "    Note: GB Studio CLI path needs to be configured in Makefile"
    echo "    Current Makefile uses: /Users/madisonmilesmedia/gb-studio/out/cli/gb-studio-cli.js"
fi
echo ""

echo "=== Python Virtual Environment ==="
check_directory "venv" "Virtual Environment"

if [ -d "venv" ]; then
    # Check if venv is activated
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo -e "${GREEN}✓${NC} Virtual environment is activated: $VIRTUAL_ENV"
    else
        echo -e "${YELLOW}⚠${NC}  Virtual environment exists but not activated"
        echo "    Run: source venv/bin/activate"
    fi
fi
echo ""

echo "=== Python Packages ==="
# Activate venv if not already activated
if [[ "$VIRTUAL_ENV" == "" ]] && [ -d "venv" ]; then
    source venv/bin/activate
fi

check_python_package "langflow" "Langflow" || echo "    Install with: pip install langflow>=1.4"
echo ""

echo "=== Project Structure ==="
check_directory "assets" "Assets Directory"
check_directory "build" "Build Directory"
check_directory "docs" "Documentation Directory"
check_directory "scripts" "Scripts Directory"
check_directory "langflow_components" "Langflow Components"
check_directory "langflow_agents" "Langflow Agents"
check_directory "memory" "Memory Directory"
check_directory "vectorstore" "Vector Store"
check_file "BARRY-SHARP-PRO-MOVER-1.gbsproj" "GB Studio Project"
check_file "Makefile" "Makefile"
check_file "pyproject.toml" "Python Project Config"
echo ""

echo "=== Project Management Backbone ==="
check_file "langflow_agents/registry.json" "Agent Registry"
check_file "memory/approval_queue.json" "Approval Queue"
check_file "memory/pm_ledger.jsonl" "PM Ledger"
echo ""

echo "=== Build Artifacts ==="
if [ -f "build/game.gb" ]; then
    echo -e "${GREEN}✓${NC} ROM File: build/game.gb ($(stat -f%z build/game.gb 2>/dev/null || stat -c%s build/game.gb 2>/dev/null) bytes)"
else
    echo -e "${YELLOW}⚠${NC}  ROM File: Not built yet"
    echo "    Run: make build-rom"
fi
echo ""

echo "=========================================="
if [ "$ALL_CHECKS_PASSED" = true ]; then
    echo -e "${GREEN}✓ All required checks passed!${NC}"
    echo ""
    echo "Development environment is ready!"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure GB Studio CLI is installed and path is configured"
    echo "  2. Activate virtual environment: source venv/bin/activate"
    echo "  3. Start Langflow: ./start_langflow_local.sh"
    echo "  4. Build ROM: make build-rom"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Please address the issues above before continuing."
    exit 1
fi
