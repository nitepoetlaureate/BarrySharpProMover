# Support

Thank you for using Barry Sharp Pro Mover! This document provides resources for getting help and support.

## Documentation

Before seeking support, please check our comprehensive documentation:

- **[README.md](README.md)** - Project overview and quick start
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions for all platforms
- **[Architecture Documentation](docs/ARCHITECTURE.md)** - System design and architecture diagrams
- **[API Documentation](docs/API.md)** - Complete API reference for all components
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Security Policy](SECURITY.md)** - Security guidelines and vulnerability reporting

## Getting Help

### 1. Search Existing Issues

Before creating a new issue, please search [existing issues](https://github.com/nitepoetlaureate/BarrySharpProMover/issues) to see if your question has already been answered.

### 2. GitHub Discussions

For general questions, ideas, and community discussions:

- **[GitHub Discussions](https://github.com/nitepoetlaureate/BarrySharpProMover/discussions)**
  - Q&A - Ask questions and get help from the community
  - Ideas - Share ideas for new features
  - Show and Tell - Share what you've built
  - General - General discussion about the project

### 3. Report Bugs

Found a bug? Please create a detailed bug report:

1. Go to [Issues](https://github.com/nitepoetlaureate/BarrySharpProMover/issues/new/choose)
2. Select "Bug Report" template
3. Fill in all required information
4. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages/logs

### 4. Request Features

Have an idea for a new feature?

1. Go to [Issues](https://github.com/nitepoetlaureate/BarrySharpProMover/issues/new/choose)
2. Select "Feature Request" template
3. Describe:
   - The problem it solves
   - Proposed solution
   - Alternative solutions considered
   - Use cases

## Community Resources

### GB Studio Community

- **[GB Studio Official Site](https://www.gbstudio.dev/)**
- **[GB Studio Discord](https://discord.gg/bxerKnc)** - Active community for GB Studio help
- **[GB Studio Documentation](https://www.gbstudio.dev/docs/)**

### LangFlow Community

- **[LangFlow Official Site](https://www.langflow.org/)**
- **[LangFlow Discord](https://discord.gg/langflow)** - Get help with LangFlow workflows
- **[LangFlow Documentation](https://docs.langflow.org/)**

### Game Boy Development

- **[Pan Docs](https://gbdev.io/pandocs/)** - Comprehensive Game Boy technical reference
- **[GB Dev Community](https://gbdev.io/)** - Resources and community
- **[r/Gameboy](https://www.reddit.com/r/Gameboy/)** - Reddit community

## Troubleshooting

### Common Issues

#### GB Studio CLI Not Found

**Problem:** `make: gb-studio-cli-not-found: No such file or directory`

**Solution:**
1. Verify GB Studio is installed
2. Set environment variable:
   ```bash
   export GB_STUDIO_CLI="/path/to/gb-studio-cli.js"
   ```
3. See [Installation Guide](docs/INSTALLATION.md#gb-studio-installation) for details

#### Python Import Errors

**Problem:** `ModuleNotFoundError: No module named 'langflow'`

**Solution:**
1. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Reinstall dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

#### Test Failures

**Problem:** Tests failing unexpectedly

**Solution:**
1. Clean test cache:
   ```bash
   rm -rf .pytest_cache __pycache__
   ```
2. Run with verbose output:
   ```bash
   pytest -v --tb=short
   ```
3. Check [Troubleshooting Guide](docs/INSTALLATION.md#troubleshooting)

#### Build Failures

**Problem:** ROM build fails

**Solution:**
1. Verify project file exists:
   ```bash
   ls -la BARRY-SHARP-PRO-MOVER-1.gbsproj
   ```
2. Run validation first:
   ```bash
   make check-bg check-scenes check-json
   ```
3. Check build logs:
   ```bash
   make build-rom 2>&1 | tee build.log
   ```

## Response Times

We aim to respond to issues and questions in a timely manner:

- **Bug Reports (Critical):** Within 24-48 hours
- **Bug Reports (Non-Critical):** Within 1 week
- **Feature Requests:** Within 1-2 weeks
- **Questions:** Within 3-5 days

*Note: This is an open-source project maintained by volunteers. Response times may vary.*

## Contributing

Want to contribute? We welcome contributions!

1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Check out [Good First Issues](https://github.com/nitepoetlaureate/BarrySharpProMover/labels/good%20first%20issue)
3. Join discussions and help others

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Please report unacceptable behavior to the project maintainers.

## Security Issues

**Do NOT create public issues for security vulnerabilities.**

Please see our [Security Policy](SECURITY.md) for how to responsibly disclose security issues.

## Professional Support

For professional support, consulting, or custom development:

- Open a discussion in the "Professional Services" category
- Include your requirements and timeline
- We'll connect you with experienced contributors

---

## Quick Links

- **[Report a Bug](https://github.com/nitepoetlaureate/BarrySharpProMover/issues/new?template=bug_report.md)**
- **[Request a Feature](https://github.com/nitepoetlaureate/BarrySharpProMover/issues/new?template=feature_request.md)**
- **[Ask a Question](https://github.com/nitepoetlaureate/BarrySharpProMover/discussions/new?category=q-a)**
- **[View Documentation](docs/)**
- **[Contributing Guide](CONTRIBUTING.md)**

---

**Last Updated:** 2025-11-21

Thank you for being part of the Barry Sharp Pro Mover community! 🎮
