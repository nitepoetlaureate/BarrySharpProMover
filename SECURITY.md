# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of these methods:

### Email

Send details to: **security@[PROJECT_DOMAIN]** (replace with actual contact)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Private Security Advisory

Use GitHub's private vulnerability reporting:
1. Go to the Security tab
2. Click "Report a vulnerability"
3. Fill out the form with details

## Response Timeline

- **Initial response:** Within 48 hours
- **Status update:** Within 7 days
- **Fix timeline:** Depends on severity

### Severity Levels

| Severity | Response Time | Fix Timeline |
|----------|--------------|--------------|
| Critical | 24 hours | 7 days |
| High | 48 hours | 14 days |
| Medium | 7 days | 30 days |
| Low | 14 days | 60 days |

## Security Best Practices

### For Contributors

When contributing code:

1. **Never commit secrets**
   - No API keys, passwords, or tokens
   - Use environment variables
   - Check `.gitignore` is comprehensive

2. **Validate all inputs**
   - Sanitize user input
   - Validate file paths (prevent traversal)
   - Check file types and sizes

3. **Avoid unsafe operations**
   - No `eval()` or `exec()` on user input
   - No shell=True in subprocess calls
   - Use parameterized queries (if applicable)

4. **Dependencies**
   - Keep dependencies updated
   - Review security advisories
   - Use `pip-audit` and `npm audit`

### For Users

When using this project:

1. **Keep updated**
   - Update to latest version regularly
   - Subscribe to security notifications

2. **Secure your environment**
   - Use virtual environments
   - Don't run as root/administrator
   - Review permissions

3. **Custom components**
   - Review custom LangFlow components
   - Understand what code executes
   - Isolate untrusted workflows

## Known Security Considerations

### Code Execution

This project includes LangFlow integration which can execute Python code:

- **Risk:** Custom components can run arbitrary Python
- **Mitigation:** Only use trusted components
- **Future:** Sandboxing in development (see REMEDIATION_PLAN.md)

### File Operations

Build automation involves file system operations:

- **Risk:** Path traversal if input not validated
- **Mitigation:** All paths use `pathlib.Path.resolve()`
- **Status:** Validated in Phase 2 (current)

### Subprocess Calls

GB Studio CLI is invoked via subprocess:

- **Risk:** Command injection if paths not sanitized
- **Mitigation:** `shell=False` and input validation
- **Status:** Implemented and tested

## Security Enhancements Roadmap

Planned security improvements (see REMEDIATION_PLAN.md Phase 4):

- [ ] **SEC-007:** Replace all `exec()`/`eval()` with AST parsing
- [ ] **SEC-008:** Implement rate limiting on endpoints
- [ ] **SEC-009:** Add CSRF protection
- [ ] **SEC-010:** Enhance cookie security (httponly, secure, samesite)
- [ ] **SEC-011:** Add security headers middleware
- [ ] **SEC-012:** Professional penetration testing

## Disclosure Policy

After a security issue is fixed:

1. **Patch release** published
2. **Security advisory** published (24 hours later)
3. **CVE requested** (if applicable)
4. **Credit given** to reporter (unless anonymous)

## Security Contacts

- **Project Maintainer:** [MAINTAINER_EMAIL]
- **Security Team:** security@[PROJECT_DOMAIN]
- **GitHub:** Use private vulnerability reporting

## Acknowledgments

We thank the following security researchers:

- None yet - be the first!

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

---

**Last Updated:** 2025-11-21
**Next Review:** 2026-02-21
