#!/usr/bin/env python3
"""
Environment Configuration Validator
Validates that all required environment variables are set and valid.

Usage:
    python3 scripts/validate_env.py
    python3 scripts/validate_env.py -v  # verbose mode

Exit Codes:
    0 - Environment is valid
    1 - Required variables missing or invalid
    2 - Error occurred
"""

import os
import sys
from pathlib import Path
import argparse


def check_file_exists(path: str, description: str) -> tuple[bool, str]:
    """Check if a file path exists."""
    if not path:
        return False, f"{description}: Not set"

    file_path = Path(path).expanduser()
    if not file_path.exists():
        return False, f"{description}: Path does not exist: {path}"

    return True, path


def validate_env():
    """Validate environment configuration."""
    print("🔍 Validating environment configuration...\n")

    errors = []
    warnings = []
    info = []

    # ======================================
    # Required variables
    # ======================================

    # GB Studio CLI path
    gb_cli_path = os.getenv('GB_STUDIO_CLI_PATH')
    is_valid, message = check_file_exists(gb_cli_path, 'GB_STUDIO_CLI_PATH')
    if is_valid:
        print(f"✅ GB_STUDIO_CLI_PATH: {message}")
        info.append(message)
    else:
        print(f"❌ {message}")
        errors.append(message)
        print("   💡 Set in .env file. Example:")
        print("      GB_STUDIO_CLI_PATH=/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js")

    # ======================================
    # Optional but recommended variables
    # ======================================

    # Ollama host for RAG
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    print(f"ℹ️  OLLAMA_HOST: {ollama_host}")
    if ollama_host == 'http://localhost:11434':
        warnings.append("OLLAMA_HOST using default value")

    # LangFlow settings
    langflow_port = os.getenv('LANGFLOW_PORT', '7860')
    langflow_host = os.getenv('LANGFLOW_HOST', '127.0.0.1')
    print(f"ℹ️  LANGFLOW: {langflow_host}:{langflow_port}")

    # Embedding model
    embedding_model = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
    print(f"ℹ️  EMBEDDING_MODEL: {embedding_model}")

    # LLM model
    llm_model = os.getenv('LLM_MODEL', 'mistral')
    print(f"ℹ️  LLM_MODEL: {llm_model}")

    # Build settings
    build_dir = os.getenv('BUILD_DIR', 'build')
    print(f"ℹ️  BUILD_DIR: {build_dir}")

    # ======================================
    # Optional variables (not critical)
    # ======================================

    # API keys (only check if set)
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if google_api_key:
        print(f"✅ GOOGLE_API_KEY: Set (length: {len(google_api_key)})")
    else:
        warnings.append("GOOGLE_API_KEY not set (optional)")

    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        print(f"✅ GITHUB_TOKEN: Set (length: {len(github_token)})")
    else:
        warnings.append("GITHUB_TOKEN not set (optional)")

    # Notifications
    notify_email = os.getenv('NOTIFY_EMAIL')
    if notify_email:
        print(f"✅ NOTIFY_EMAIL: {notify_email}")
    else:
        warnings.append("NOTIFY_EMAIL not set (notifications disabled)")

    # Debug mode
    debug_mode = os.getenv('DEBUG_MODE', 'false')
    if debug_mode.lower() in ['true', '1', 'yes']:
        print(f"⚠️  DEBUG_MODE: Enabled")
        warnings.append("DEBUG_MODE is enabled")

    # ======================================
    # Print summary
    # ======================================

    print("\n" + "=" * 60)

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"   • {warning}")

    if errors:
        print("\n❌ Errors:")
        for error in errors:
            print(f"   • {error}")
        print("\n💡 Quick fix:")
        print("   1. Copy .env.example to .env:")
        print("      cp .env.example .env")
        print("   2. Edit .env and set required variables")
        print("   3. Run this validator again:")
        print("      python3 scripts/validate_env.py")
        return 1

    print("\n✅ Environment configuration is valid!")
    print("\nYou can now:")
    print("  • Check GB Studio: make check-gbstudio")
    print("  • Build ROM: make build-rom")
    print("  • Start automation: ./scripts/automation_control.sh start")

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate environment configuration"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    args = parser.parse_args()

    # Try to load .env if python-dotenv is available
    try:
        from dotenv import load_dotenv
        env_file = Path.cwd() / '.env'
        if env_file.exists():
            load_dotenv()
            if args.verbose:
                print(f"📄 Loaded environment from: {env_file}\n")
        else:
            print("⚠️  No .env file found. Copy .env.example to .env first.\n")
            print("   cp .env.example .env\n")
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with:")
        print("   pip install python-dotenv\n")
        print("Checking environment variables anyway...\n")

    return validate_env()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nValidation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(2)
