# Contributing to Barry Sharp Pro Mover

Thank you for your interest in contributing to Barry Sharp Pro Mover! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Node.js 16+** (for LangFlow frontend)
- **GB Studio** with CLI (for game builds)
- **Git** with Git LFS configured

### Setup Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nitepoetlaureate/BarrySharpProMover.git
   cd BarrySharpProMover
   ```

2. **Install Git LFS:**
   ```bash
   git lfs install
   git lfs pull
   ```

3. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Configure GB Studio CLI:**
   ```bash
   export GB_STUDIO_CLI=/path/to/gb-studio-cli.js
   # Or add to ~/.bashrc or ~/.zshrc
   ```

5. **Verify installation:**
   ```bash
   make build-rom  # Should build successfully
   pytest          # Should run all tests
   ruff check .    # Should pass linting
   ```

## Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following our style guide
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and linting:**
   ```bash
   pytest --cov=.langflow
   ruff check .
   mypy .
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

## Code Style

### Python

We follow **PEP 8** with these specific guidelines:

- **Line length:** 120 characters (configured in `pyproject.toml`)
- **Imports:** Organized using `isort` (automatic via ruff)
- **Type hints:** Required for all public functions
- **Docstrings:** Google or numpy style for all public APIs

**Example:**
```python
from pathlib import Path


def process_sprite(sprite_path: Path, output_dir: Path) -> Path:
    """Process a sprite file for Game Boy.

    Args:
        sprite_path: Path to the input sprite file
        output_dir: Directory for processed output

    Returns:
        Path to the processed sprite file

    Raises:
        ValueError: If sprite dimensions are invalid
    """
    # Implementation here
    pass
```

### Makefile

- Use tabs for indentation (Make requirement)
- Add `@` prefix to suppress command echo where appropriate
- Document complex targets with comments

### Markdown

- Use ATX-style headers (`#` not underlines)
- One sentence per line (makes diffs clearer)
- Include table of contents for docs > 200 lines

## Testing Requirements

### Test Coverage

- **Minimum:** 80% coverage for all new code
- **Target:** 90%+ for critical components (build, validation)
- **Run:** `pytest --cov=.langflow --cov-report=html`

### Test Organization

```
tests/
├── unit/              # Unit tests for individual functions
├── integration/       # Integration tests for workflows
├── fixtures/          # Shared test data
└── conftest.py        # Shared fixtures and configuration
```

### Writing Tests

**Unit Test Example:**
```python
import pytest
from pathlib import Path


def test_sprite_validation_success(temp_project_dir):
    """Test that valid sprites pass validation."""
    sprite = temp_project_dir / "sprite.png"
    sprite.write_bytes(b"valid PNG data")

    result = validate_sprite(sprite)

    assert result.is_valid
    assert result.errors == []
```

**Integration Test Example:**
```python
def test_full_build_workflow(temp_project_dir):
    """Test complete build from assets to ROM."""
    # Setup test project
    setup_test_assets(temp_project_dir)

    # Run build
    result = run_build(temp_project_dir)

    # Verify
    assert (temp_project_dir / "build" / "rom.gb").exists()
    assert result.exit_code == 0
```

### Test Best Practices

- ✅ Test one thing per test
- ✅ Use descriptive test names
- ✅ Use fixtures for shared setup
- ✅ Mock external dependencies (subprocess, file I/O)
- ❌ Don't test implementation details
- ❌ Don't use sleep() (use mocking instead)

## Commit Message Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, no logic change)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Build process, dependencies, tooling

### Examples

```bash
feat(build): add support for web builds

Add make targets for generating web builds alongside ROM builds.
Includes HTML5 wrapper and WASM binary.

Closes #42
```

```bash
fix(validation): handle missing sprite files gracefully

Previously validation crashed if sprite file was missing.
Now returns clear error message.

Related: #38
```

```bash
docs(architecture): add system component diagram

Add mermaid diagram showing interaction between GB Studio,
LangFlow, and build automation components.
```

## Pull Request Process

### Before Submitting

- [ ] All tests pass (`pytest`)
- [ ] Linting passes (`ruff check .`)
- [ ] Type checking passes (`mypy .`)
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow conventions

### PR Template

When creating a PR, include:

```markdown
## Summary
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- List of specific changes made
- Can be bullet points

## Test Plan
How did you test this? Steps to verify.

## Screenshots
If UI changes, include before/after screenshots

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Follows code style guidelines
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Testing** on multiple platforms (if applicable)
4. **Approval** required before merge
5. **Squash and merge** to keep history clean

### After Merge

- Delete your feature branch
- Pull latest main: `git pull origin main`
- Create new branch for next feature

## Project-Specific Guidelines

### GB Studio Assets

- **Sprites:** 16x16 or 32x32 pixels, 4 colors max
- **Backgrounds:** 160x144 pixels (or multiples), 4 colors max
- **Music:** MOD format, tracked music
- **Naming:** Use snake_case for all asset files

### LangFlow Components

- Place custom components in `.langflow/components/`
- Include `display_name` and `description` class attributes
- Handle LangFlow import errors gracefully (see existing components)
- Document component inputs and outputs

### Build Automation

- Test all Makefile changes on Linux and macOS
- Ensure GB_STUDIO_CLI variable is respected
- Add validation before expensive operations

## Getting Help

- **Documentation:** Check `/docs` directory
- **Issues:** Search existing issues on GitHub
- **Discussions:** Use GitHub Discussions for questions
- **Discord:** Join our community server (link in README)

## Recognition

Contributors are recognized in:
- AUTHORS.md file
- Release notes
- Project README

Thank you for contributing to Barry Sharp Pro Mover! 🚚✨
