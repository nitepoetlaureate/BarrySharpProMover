# Security Policy

## Overview

BarrySharpProMover follows security best practices to protect against common vulnerabilities. This document outlines our security measures, how to report vulnerabilities, and development guidelines.

## 🔒 Security Measures

### 1. Input Validation & Sanitization

All user inputs are validated and sanitized to prevent injection attacks:

- **Path Traversal Protection**: All file paths validated with `scripts/security/path_validator.py`
- **Input Sanitization**: User strings sanitized with `scripts/security/input_sanitizer.py`
- **JSON Validation**: JSON inputs validated for size and nesting depth
- **Filename Validation**: Filenames checked for malicious characters

**Example:**
```python
from security.path_validator import safe_path
from security.input_sanitizer import sanitize_string

# Validate user-provided path
safe_file = safe_path(user_path, base_dir="/project/assets")

# Sanitize user input
clean_input = sanitize_string(user_input, max_length=1000)
```

### 2. Secrets Management

- **Environment Variables**: All secrets stored in `.env` file (never committed)
- **No Hardcoded Credentials**: Regular audits for hardcoded secrets
- **API Key Protection**: API keys loaded from environment only

**Setup:**
```bash
# Copy example file
cp .env.example .env

# Edit and add your secrets
vim .env

# Verify setup
python3 scripts/validate_env.py
```

### 3. Dependency Security

- **Pinned Versions**: All dependencies pinned in `requirements.txt`
- **Security Scanning**: Run `python3 scripts/security_audit.py`
- **Regular Updates**: Dependencies updated and tested regularly

**Run Security Audit:**
```bash
# Full security audit
python3 scripts/security_audit.py

# Check for vulnerable dependencies (requires safety)
pip install safety
safety check
```

### 4. File Operation Security

- **Size Limits**: Maximum file sizes enforced per asset type
- **Extension Validation**: Only allowed file types accepted
- **Permission Checks**: File permissions validated before operations

**File Size Limits:**
- Images: 10MB
- Audio: 50MB
- JSON: 5MB
- ROM: 8MB

### 5. Command Injection Prevention

- **No Shell Execution**: Use `subprocess` with `shell=False`
- **Command Allowlisting**: Only allowed commands executed
- **Argument Escaping**: Shell arguments properly escaped when necessary

### 6. JSON Security

- **Size Limits**: Maximum 5MB JSON files
- **Depth Limits**: Maximum nesting depth of 10 levels
- **Parse Before Use**: All JSON validated before parsing

## 🛡️ Security Configuration

Configure security settings in `.env`:

```bash
# Path traversal protection
REJECT_ABSOLUTE_PATHS=true

# Input sanitization
INPUT_SANITIZATION_ENABLED=true
MAX_JSON_DEPTH=10
MAX_INPUT_LENGTH=10000

# File validation
STRICT_FILENAME_VALIDATION=true
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Command injection protection
COMMAND_INJECTION_PROTECTION=true
```

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email security details to: [Your security email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## 🔐 Security Best Practices for Contributors

### Code Review Checklist

- [ ] No hardcoded secrets or credentials
- [ ] All file paths validated with `safe_path()`
- [ ] User inputs sanitized
- [ ] File sizes validated
- [ ] No shell command execution (or properly escaped)
- [ ] Dependencies pinned with versions
- [ ] Security tests added for new features

### Testing

All security utilities have comprehensive unit tests:

```bash
# Run security tests
pytest tests/unit/test_security_*.py -v

# Run with coverage
pytest tests/unit/test_security_*.py --cov=scripts/security
```

### Pre-Commit Security Checks

Before committing code:

1. Run security audit: `python3 scripts/security_audit.py`
2. Run tests: `make test`
3. Check for secrets: `grep -r "password\|api_key\|secret" --exclude-dir=.git`
4. Verify `.env` not in git: `git status | grep .env`

## 📋 Security Utilities Reference

### Path Validation (`scripts/security/path_validator.py`)

- `safe_path(user_path, base_dir)` - Validate path within base directory
- `validate_file_path(path, allowed_extensions, max_size_mb)` - Comprehensive file validation
- `is_safe_filename(filename)` - Check if filename is safe
- `get_allowed_directories()` - Get allowed asset directories

### Input Sanitization (`scripts/security/input_sanitizer.py`)

- `sanitize_string(input_str, max_length)` - Sanitize string input
- `sanitize_json_input(json_str, max_depth, max_size_mb)` - Validate JSON
- `validate_file_size(file_path, asset_type)` - Check file size
- `sanitize_filename(filename)` - Make filename safe
- `validate_command_input(command, allowed_commands)` - Validate command
- `escape_shell_arg(arg)` - Escape shell argument

## 🔍 Common Vulnerabilities Prevented

### Path Traversal
**Attack:** `../../../etc/passwd`
**Prevention:** `safe_path()` function validates all paths

### Command Injection
**Attack:** `build; rm -rf /`
**Prevention:** Command allowlisting and no shell execution

### JSON Bomb
**Attack:** Deeply nested JSON causing DoS
**Prevention:** Max nesting depth of 10 levels

### File Upload DoS
**Attack:** Uploading huge files to fill disk
**Prevention:** File size limits enforced

### Hidden Files
**Attack:** Uploading `.htaccess` or `.bashrc`
**Prevention:** Filenames starting with `.` rejected

### Null Byte Injection
**Attack:** `file.txt\x00.exe`
**Prevention:** Null bytes detected and rejected

## 📊 Security Metrics

Track security status:

```bash
# Run full security audit
python3 scripts/security_audit.py

# Check test coverage of security utilities
pytest tests/unit/test_security_*.py --cov=scripts/security --cov-report=term
```

## 🔄 Security Update Process

1. **Monitor**: Check for security advisories regularly
2. **Test**: Update dependencies in development environment
3. **Validate**: Run full test suite
4. **Deploy**: Update production after validation
5. **Document**: Update CHANGELOG.md

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Safety Documentation](https://pyup.io/safety/)

## ✅ Security Compliance

This project implements security controls for:

- ✅ Path Traversal (CWE-22)
- ✅ Command Injection (CWE-78)
- ✅ JSON Injection (CWE-91)
- ✅ Improper Input Validation (CWE-20)
- ✅ Uncontrolled Resource Consumption (CWE-400)
- ✅ Use of Hard-coded Credentials (CWE-798)

---

**Last Updated:** 2025-11-24
**Version:** 1.0.0
**Contact:** [Your security contact]
