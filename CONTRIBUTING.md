# Contributing to SkillsHub

Thank you for your interest in contributing to SkillsHub! This document provides guidelines for contributing skills and improvements to the repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Adding a New Skill](#adding-a-new-skill)
- [Skill Submission Checklist](#skill-submission-checklist)
- [Coding Standards](#coding-standards)
- [Security Guidelines](#security-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to the [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the repository maintainers.

## How to Contribute

### Reporting Bugs

- Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include steps to reproduce the issue
- Specify which skill is affected
- Include your environment details

### Suggesting Features

- Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Describe the problem you're trying to solve
- Explain your proposed solution

### Submitting Skills

- Use the [skill submission template](.github/ISSUE_TEMPLATE/skill_submission.yml)
- Follow the guidelines below

## Adding a New Skill

### Step 1: Create Your Skill Folder

Create a new folder under `/skills/` with your skill name (PascalCase):

```bash
mkdir skills/YourSkillName
```

### Step 2: Create Required Files

Every skill MUST include:

#### `skill.json`

```json
{
  "name": "YourSkillName",
  "version": "1.0.0",
  "author": "Your Name or GitHub Handle",
  "license": "MIT",
  "description": "A concise 1-2 sentence description of what your skill does.",
  "tags": ["relevant", "tags", "here"],
  "entrypoint": "SKILL.md",
  "language": "markdown|python|javascript|typescript|other",
  "requirements": ["list", "of", "dependencies"],
  "usage": "/yourskill [arguments]",
  "tested_on": ["mac", "windows", "linux"],
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

**Field Descriptions:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill name, must match folder name |
| `version` | Yes | Semantic version (e.g., "1.0.0") |
| `author` | Yes | Your name or GitHub handle |
| `license` | Yes | OSI-approved license identifier |
| `description` | Yes | 1-2 sentence description |
| `tags` | Yes | Array of relevant tags for discovery |
| `entrypoint` | Yes | Relative path to main skill file |
| `language` | Yes | Primary language of the skill |
| `requirements` | Yes | Dependencies (empty array if none) |
| `usage` | Yes | Brief usage syntax |
| `tested_on` | Yes | Platforms tested on |
| `created_at` | Yes | ISO date of creation |
| `updated_at` | Yes | ISO date of last update |

#### `README.md`

Your skill's README must include:

1. **Title and Description** - What the skill does
2. **Installation** - How to install/set up the skill
3. **Usage** - How to invoke and use the skill
4. **Examples** - Real-world usage examples
5. **Inputs/Outputs** - What the skill expects and produces
6. **Limitations** - Known limitations or edge cases
7. **License** - License information

### Step 3: Validate Your Skill

Run the validation script:

```bash
python scripts/validate_skill.py skills/YourSkillName
```

Fix any errors before submitting.

### Step 4: Submit a Pull Request

1. Fork the repository
2. Create a feature branch: `git checkout -b add-skill-yourskillname`
3. Commit your changes: `git commit -m "Add YourSkillName skill"`
4. Push to your fork: `git push origin add-skill-yourskillname`
5. Open a Pull Request

## Skill Submission Checklist

Before submitting your skill, verify:

### Required Files
- [ ] `skill.json` exists and is valid JSON
- [ ] `README.md` exists with all required sections
- [ ] Entrypoint file exists at the specified path

### Metadata Quality
- [ ] `name` matches the folder name
- [ ] `version` follows semantic versioning
- [ ] `description` is clear and concise
- [ ] `tags` are relevant and helpful for discovery
- [ ] `tested_on` accurately reflects your testing

### Documentation Quality
- [ ] README explains what the skill does
- [ ] Installation instructions are complete
- [ ] Usage examples are provided
- [ ] Limitations are documented
- [ ] License is specified

### Security
- [ ] No hardcoded credentials or secrets
- [ ] No sensitive personal information
- [ ] No malicious or harmful code
- [ ] Dependencies are from trusted sources

### Testing
- [ ] Skill has been tested locally
- [ ] Skill works as documented
- [ ] Edge cases have been considered

## Coding Standards

### File Naming
- Skill folders: PascalCase (e.g., `DocSheriff`, `CodeReviewer`)
- Skill files: lowercase with dashes for multi-word (e.g., `SKILL.md`, `helper-utils.py`)

### Documentation
- Use clear, concise language
- Include code examples where appropriate
- Keep lines under 100 characters when possible
- Use proper Markdown formatting

### Skill Design
- Single responsibility: one skill, one purpose
- Clear inputs and outputs
- Graceful error handling
- User-friendly messages

## Security Guidelines

### Do NOT Include
- API keys, tokens, or secrets
- Personal information (emails, addresses, etc.)
- Credentials of any kind
- Internal URLs or proprietary endpoints

### Do Include
- Placeholder examples for configuration
- Documentation on required environment setup
- Clear warnings about security considerations

### Dependency Management
- List all dependencies in `requirements` field
- Use specific versions when possible
- Prefer well-maintained, popular libraries
- Avoid dependencies with known vulnerabilities

## Pull Request Process

1. **Title**: Use format `Add [SkillName] skill` or `Fix: [description]`
2. **Description**: Fill out the PR template completely
3. **Checks**: Ensure CI validation passes
4. **Review**: Wait for maintainer review
5. **Updates**: Address any requested changes
6. **Merge**: Maintainer will merge when approved

### Review Criteria

PRs are reviewed for:
- Completeness of required files
- Quality of documentation
- Adherence to coding standards
- Security considerations
- Usefulness to the community

---

Questions? Open a [Discussion](../../discussions) or reach out to the maintainers.

Thank you for contributing to SkillsHub!
