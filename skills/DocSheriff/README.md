# DocSheriff

Your codebase documentation enforcer. Analyzes, standardizes, and maintains documentation files with strict guardrails against accidental rewrites and hallucinated certainty.

## What It Does

DocSheriff enforces a documentation contract across your codebase:

- **Validates** documentation against a strict schema
- **Standardizes** frontmatter, section order, and TODO formats
- **Tracks freshness** - treats doc rot as a first-class concern
- **Cross-links** docs to code with automatic verification
- **Syncs** documentation claims with actual code implementation
- **Monorepo-aware** - detects package drift, build script issues, and stale recommendations

## Installation

Copy the skill file to your Claude Code skills directory:

```bash
mkdir -p .claude/skills/docsheriff
cp SKILL.md .claude/skills/docsheriff/SKILL.md
```

## Usage

```
/docsheriff [command] [path]
```

### Commands

| Command | Description |
|---------|-------------|
| `check` | Validate docs against contract, report issues (no changes) |
| `fix` | Apply safe auto-fixes, add placeholders for meaning changes |
| `audit` | Full documentation audit with freshness analysis |
| `new` | Interactive creation of new documentation |
| `monorepo` | Validate monorepo structure, package docs, and build scripts |
| `sync` | Generate code TODOs based on documentation gaps |

### Examples

```bash
# Check all documentation in a directory
/docsheriff check apps/web/docs/

# Fix documentation issues automatically
/docsheriff fix src/services/

# Full audit of all docs
/docsheriff audit

# Create new documentation interactively
/docsheriff new auth-service

# Validate monorepo structure and package documentation
/docsheriff monorepo

# Validate and auto-fix monorepo issues
/docsheriff monorepo --fix

# Sync docs with code and generate TODOs
/docsheriff sync
```

## Inputs

- **Path** (optional): Directory or file to process. Defaults to current directory.
- **Command**: One of `check`, `fix`, `audit`, `new`, or `sync`.

## Outputs

### Check/Fix Mode
- List of files scanned and modified
- Safe fixes applied
- Unverified claims found
- TODOs added

### Audit Mode
- Freshness analysis
- Cross-link verification
- Glossary consistency report

### Monorepo Mode
- Package drift report (documented vs actual packages)
- Build script validation
- Structure diagram discrepancies
- Stale recommendations (completed work still marked as future)
- Cross-document consistency report

### Sync Mode
- Proposed code TODOs based on doc claims
- Questions for user clarification
- Prioritized task list

## The Doc Contract

Every documentation file should include:

### Required Frontmatter

```yaml
---
title: [Document Title]
owner: [team-name or @username]
last_reviewed: YYYY-MM-DD
status: draft | active | deprecated | historical | archived
applies_to: [service/package/module path]
audience: engineers | sales | ops | mixed
tags: [array, of, tags]
---
```

### Required Sections

1. TL;DR
2. TODO / Open Questions
3. Context
4. How It Works
5. How To Use / Runbook
6. Risks / Footguns
7. References

## Safe Auto-Fix vs. Meaning Changes

### Safe (Always Applied)
- Heading order normalization
- Date format standardization
- Broken internal link fixes
- Missing template sections (with placeholders)
- Terminology normalization

### Requires Evidence
- Technical explanation rewrites
- Command/config updates
- API description changes

## Limitations

- Does not process files in `node_modules/`, `dist/`, `build/`, or `vendor/` directories
- Skips files with `<!-- docsheriff: ignore -->` marker
- Cannot verify external links (only checks domain exists)
- Large document changes (>30%) trigger a warning for manual review

## License

MIT License - Free to use and modify.

---

*Built by Cory Shelton*
