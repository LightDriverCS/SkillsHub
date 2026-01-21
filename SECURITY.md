# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in SkillsHub or any skill in this repository, please report it responsibly.

### How to Report

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Email the maintainers directly or use GitHub's private vulnerability reporting feature
3. Include as much detail as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- Acknowledgment within 48 hours
- Regular updates on progress
- Credit in the fix announcement (unless you prefer anonymity)

## Security Best Practices for Skill Authors

When creating skills for SkillsHub:

### Do NOT Include

- API keys, tokens, or secrets
- Hardcoded credentials
- Personal or sensitive information
- Internal/proprietary URLs

### Do Include

- Clear documentation on required environment variables
- Warnings about security considerations
- Input validation where appropriate

### Dependency Security

- Use well-maintained dependencies
- Specify version ranges to avoid known vulnerabilities
- Regularly update dependencies

## Scope

This security policy applies to:

- The SkillsHub repository infrastructure
- All skills hosted in this repository
- Associated scripts and tooling

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | Yes                |
| older   | Best effort        |
