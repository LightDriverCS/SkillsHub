# SkillsHub

A community registry for Claude Code skills. Browse, rate, download, and contribute skills that extend Claude Code's capabilities.

## What is SkillsHub?

SkillsHub is a centralized repository where developers can share and discover skills for [Claude Code](https://claude.ai/claude-code). Skills are reusable instruction sets that teach Claude how to perform specialized tasks - from documentation enforcement to code generation patterns.

## Browse Skills

All skills are located in the [`/skills`](./skills) directory. Each skill has:

- `skill.json` - Metadata including name, version, description, and usage
- `README.md` - Detailed documentation
- Source files - The actual skill implementation

**Current Skills:**

| Skill | Description | Language | Author |
|-------|-------------|----------|--------|
| [DocSheriff](./skills/DocSheriff) | Documentation enforcer that standardizes and maintains docs across your codebase | Markdown | Cory Shelton |

See the full registry in [`/skills/index.json`](./skills/index.json).

## Install a Skill

1. Navigate to the skill folder (e.g., `/skills/DocSheriff`)
2. Copy the skill file(s) to your project's `.claude/skills/` directory
3. Invoke the skill using its documented commands

**Example:**

```bash
# Create the skills directory in your project
mkdir -p .claude/skills/docsheriff

# Copy the skill file
cp skills/DocSheriff/SKILL.md .claude/skills/docsheriff/SKILL.md
```

## Rating Skills

Skills are rated through two mechanisms:

1. **GitHub Stars** - Star this repository to show overall support, or use GitHub's "Watch" feature on specific skill discussions
2. **Discussions** - Visit the [Discussions](../../discussions) tab to:
   - Share your experience with a skill
   - Ask questions about usage
   - Suggest improvements
   - Rate skills with reaction emojis

## Submit a Skill

Want to contribute? Follow these steps:

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/SkillsHub.git
cd SkillsHub
```

### 2. Create Your Skill Folder

```bash
mkdir skills/YourSkillName
```

### 3. Add Required Files

**`skill.json`** (required):

```json
{
  "name": "YourSkillName",
  "version": "1.0.0",
  "author": "Your Name",
  "license": "MIT",
  "description": "One to two sentences describing what your skill does.",
  "tags": ["category1", "category2"],
  "entrypoint": "SKILL.md",
  "language": "markdown",
  "requirements": [],
  "usage": "/yourskill [command]",
  "tested_on": ["mac", "windows", "linux"],
  "created_at": "2025-01-21",
  "updated_at": "2025-01-21"
}
```

**`README.md`** (required):

Document your skill with:
- What it does
- How to install
- How to use (with examples)
- Inputs and outputs
- Limitations
- License info

**Skill source files** (required):

Include all files needed to run your skill.

### 4. Validate Your Skill

```bash
python scripts/validate_skill.py skills/YourSkillName
```

### 5. Submit a Pull Request

1. Commit your changes
2. Push to your fork
3. Open a Pull Request using the skill submission template

## Skill Quality Checklist

Before submitting, ensure your skill:

- [ ] Has a valid `skill.json` with all required fields
- [ ] Has a comprehensive `README.md`
- [ ] Includes clear usage examples
- [ ] Documents any limitations or known issues
- [ ] Has been tested on at least one platform
- [ ] Does not include sensitive data or credentials
- [ ] Uses an OSI-approved license
- [ ] Follows the coding standards in [CONTRIBUTING.md](./CONTRIBUTING.md)

## Repository Structure

```
SkillsHub/
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── skill_submission.yml
│   ├── workflows/
│   │   └── validate.yml
│   └── pull_request_template.md
├── skills/
│   ├── index.json
│   └── [SkillName]/
│       ├── skill.json
│       ├── README.md
│       └── [source files]
└── scripts/
    ├── validate_skill.py
    └── build_index.py
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:

- Coding standards
- Security best practices
- How to add a new skill
- Skill submission checklist

## License

This repository is licensed under the [MIT License](./LICENSE).

Individual skills may have their own licenses - check each skill's `skill.json` and `README.md` for details.

---

Built and maintained by the community. Star this repo to show your support!
