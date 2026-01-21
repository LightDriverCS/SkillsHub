---
name: docsheriff
description: DocSheriff cleans up, standardizes, and maintains documentation across your codebase. Use when creating new documentation for complex tasks, cleaning up outdated docs, restructuring poorly written documentation, or ensuring docs match actual code structure. Enforces a strict doc contract with machine-readable frontmatter, structured TODOs, and verified code references. Includes monorepo-aware validation that detects package drift, build script mismatches, and stale architecture recommendations. Asks for user feedback when uncertain and proposes code TODOs based on documentation gaps.
metadata:
  argument-hint: "[path | audit | check | fix | sync | monorepo]"
  author: Cory Shelton
  version: "2.0"
---

# DocSheriff

Your codebase documentation enforcer. Analyzes, standardizes, and maintains documentation files with strict guardrails against accidental rewrites and hallucinated certainty.

**Always asks for user feedback when:**
- Uncertain about meaning changes
- Detecting potential code-documentation mismatches
- Finding claims that can't be verified in code
- Proposing new TODOs for the codebase

## Core Principles

1. **Enforce a doc contract** - Never invent style; validate against schema
2. **Minimal diffs** - Smallest change that achieves compliance
3. **Cite evidence** - Never update facts without verification
4. **Preserve meaning** - Format changes are safe; meaning changes require proof
5. **Track freshness** - Docs rot; treat it as first-class concern

---

## The Doc Contract

Every documentation file MUST have this structure. The skill validates against this schema.

### Required Frontmatter (Machine-Readable)

```yaml
---
title: [Document Title]
owner: [team-name or @username]           # Who maintains this
last_reviewed: YYYY-MM-DD                  # When last verified accurate
status: draft | active | deprecated | historical | archived
applies_to: [service/package/module path]  # What code this covers
audience: engineers | sales | ops | mixed
tags: [array, of, tags]
related:                                    # Optional but recommended
  - code: src/services/auth.ts             # Primary code paths
  - ticket: JIRA-123                        # Related tickets
  - adr: docs/adr/001-auth-design.md       # Architecture decisions
---
```

### Required Sections (Human-Readable)

Documents MUST include these sections in this order:

1. **TL;DR** - One paragraph max, what this doc covers
2. **TODO / Open Questions** - Structured task list (see format below)
3. **Context** - Why this exists, background
4. **How It Works** - Technical explanation
5. **How To Use / Runbook** - Practical steps
6. **Risks / Footguns** - What can go wrong
7. **References** - Links to related docs, code, external resources

### Optional Sections

- Table of Contents (for docs > 200 lines)
- API Reference
- Configuration
- Troubleshooting
- Changelog
- Related Code Map

---

## Structured TODO Format

TODOs MUST be machine-parseable. Free-form prose is not acceptable.

### Schema

```markdown
## TODO / Open Questions

<!--
  Machine-readable task table
  Sort: priority (P0 first), then created (oldest first)
  Move completed items to "Completed" section or remove after 30 days
-->

| id | created | last_touched | owner | priority | status | due | note | link |
|----|---------|--------------|-------|----------|--------|-----|------|------|
| TODO-001 | 2024-01-15 | 2024-01-20 | @alice | P1 | open | 2024-02-01 | Fix session timeout bug | [#123](link) |
| TODO-002 | 2024-01-18 | 2024-01-18 | @bob | P2 | blocked | - | Add OAuth support, waiting on security review | [#456](link) |

### Completed (last 30 days)

| id | created | completed | owner | note | link |
|----|---------|-----------|-------|------|------|
| TODO-000 | 2024-01-01 | 2024-01-10 | @alice | Initial setup | [#100](link) |
```

### Priority Levels

- **P0**: Critical, blocking production or users
- **P1**: High, significant impact, this sprint
- **P2**: Medium, planned work, this quarter
- **P3**: Low, backlog, nice-to-have

### TODO Automation Rules

The skill will:
- Flag stale items: `last_touched` > 30 days ago → add warning
- Normalize dates to ISO 8601
- Detect missing owner or priority → add placeholder with warning
- Move done items to Completed section
- Remove completed items older than 30 days (or archive)
- Ensure TODO section is ALWAYS at top (after TL;DR)

---

## Change Policy

### Safe Auto-Fix (Always Allowed)

These changes preserve meaning and are applied automatically:

| Change Type | Example |
|-------------|---------|
| Heading order | Move sections to match template |
| Date normalization | `Jan 15, 2024` → `2024-01-15` |
| Formatting | Fix indentation, list markers |
| Broken internal links | Update paths that moved |
| Duplicate headings | Rename for uniqueness |
| Missing template sections | Add with `<!-- TODO: Fill in -->` placeholder |
| Consistent terminology | Apply glossary (see below) |
| Frontmatter completion | Add missing required fields with TODO values |

### Meaning-Touching Changes (Require Evidence)

These changes affect technical content. Only apply with verification:

| Change Type | Requirement |
|-------------|-------------|
| Rewriting technical explanations | Must cite code reference |
| Updating commands/configs | Must verify command exists |
| Deprecating claims | Must confirm in code that feature is removed |
| Changing API descriptions | Must match actual implementation |

**Evidence Citation Format:**

```markdown
<!-- Verified: src/services/auth.ts:45-60, commit abc1234 -->
The authentication flow now uses JWT tokens instead of sessions.
```

### Never Auto-Change

- Delete content without explicit user approval
- Rewrite prose style (only structure)
- Change meaning without evidence
- Remove historical context

---

## Doc Freshness Rules

Docs rot. The skill treats freshness as a first-class concern.

### Automatic Freshness Actions

| Condition | Action |
|-----------|--------|
| `last_reviewed` missing | Add as today, mark `needs_review: true` |
| `last_reviewed` > 90 days | Add TODO: "Review for accuracy" |
| References non-existent file | Mark as stale, add TODO with details |
| References deleted API/function | Add deprecation warning |
| `status: deprecated` without banner | Add deprecation banner at top |

### Deprecation Banner Format

```markdown
> **DEPRECATED** as of 2024-01-15
>
> This document is no longer maintained. See [New Documentation](./new-doc.md) for current information.
>
> Reason: [Brief explanation of why deprecated]
```

### Historical Document Banner

```markdown
> **HISTORICAL REFERENCE**
>
> This document describes the system as of 2023-06-01. It may not reflect current behavior.
> Kept for context and decision history.
```

---

## Glossary & Canonical Terms

The skill respects a glossary to avoid synonym chaos.

### Glossary Location

Create or maintain: `docs/glossary.yml` or `docs/glossary.md`

### Glossary Format

```yaml
# docs/glossary.yml
terms:
  - canonical: "Processing Job"
    aliases: ["job", "processing task", "worker job"]
    definition: "A unit of work queued for the desktop processing engine"
    source: "packages/integration/src/types/job.ts"

  - canonical: "Instance"
    aliases: ["tenant", "organization", "workspace"]
    definition: "A multi-tenant workspace containing users and data"
    source: "apps/web/src/types/instance.ts"
```

### Terminology Normalization Rules

- Replace aliases with canonical term on first use
- Keep alias in parentheses once: "Processing Job (also called 'job')"
- Link to glossary on first use: "[Processing Job](../glossary.md#processing-job)"
- Don't replace in code blocks or direct quotes

---

## Code Cross-Linking

The skill makes docs valuable by connecting them to code.

### Automatic Behaviors

- Infer ownership from CODEOWNERS or package.json
- Attach `applies_to` based on nearest package root
- Add "Related Code" section with paths to primary modules
- Verify runbook links point to actual scripts/entrypoints
- Create documentation map entries

### Related Code Section Format

```markdown
## Related Code

| Component | Path | Purpose |
|-----------|------|---------|
| Main Service | `src/services/auth.ts` | Authentication logic |
| Types | `packages/types/src/auth.ts` | Type definitions |
| Tests | `src/__tests__/auth.test.ts` | Unit tests |
| Config | `config/auth.json` | Runtime configuration |

**Documentation Map:**
- This doc explains: Authentication flow
- Implemented in: `src/services/auth.ts`
- Configured by: `config/auth.json`
- Tested by: `src/__tests__/auth.test.ts`
```

---

## Guardrails Against Hallucinated Certainty

The skill NEVER confidently rewrites unverified claims.

### Verification Rules

1. **Technical claims must be verified in code**
   - If can't find in codebase → mark as `<!-- Unverified: ... -->`
   - Add TODO: "Verify this claim against implementation"

2. **Commands must be tested**
   - If command doesn't exist → mark as `<!-- Unverified: command not found -->`
   - Don't assume commands work

3. **Links must be checked**
   - If internal link broken → suggest fix or mark stale
   - External links → verify domain exists

4. **Numbers and metrics must have sources**
   - "Handles 10k requests/sec" needs citation
   - No performance claims without evidence

---

## Output Format

### 1. File Changes

Actual changes to documentation files, following minimal diff principle.

### 2. Cleanup Report

```markdown
## Documentation Cleanup Report

**Date:** 2024-01-21
**Scope:** apps/web/docs/
**Mode:** fix

### Summary

| Metric | Count |
|--------|-------|
| Files scanned | 15 |
| Files modified | 8 |
| Files skipped | 3 |
| Safe fixes applied | 45 |
| Meaning changes (with evidence) | 3 |
| Unverified claims found | 7 |
| Stale references found | 4 |
| TODOs added | 12 |
| TODOs completed/removed | 2 |

### Changes by Type

| Type | Count | Files |
|------|-------|-------|
| Frontmatter completion | 8 | auth.md, api.md, ... |
| Date normalization | 12 | various |
| Section reordering | 5 | setup.md, deploy.md, ... |
| Broken link fixes | 3 | readme.md |
| Terminology normalization | 7 | various |

### Unverified Claims Found

| File | Line | Claim | Action |
|------|------|-------|--------|
| api.md | 45 | "Supports 1000 connections" | Marked unverified, TODO added |
| auth.md | 78 | "Uses bcrypt with cost 12" | Verified in config.ts:23 |

### Stale References

| File | Reference | Issue | Suggestion |
|------|-----------|-------|------------|
| setup.md | `src/old/config.ts` | File not found | Maybe `src/config/index.ts`? |
| api.md | `getUserById()` | Function renamed | Now `findUserById()` |

### Docs Marked for Review

| File | Reason |
|------|--------|
| legacy-api.md | References deleted code, needs deprecation decision |
| old-setup.md | Not reviewed in 180 days |

### TODOs Added

| File | TODO ID | Priority | Note |
|------|---------|----------|------|
| auth.md | TODO-AUTH-001 | P2 | Verify bcrypt cost claim |
| api.md | TODO-API-001 | P1 | Update stale file reference |

### Warnings

- `generated/` directory skipped (appears auto-generated)
- `vendor/` directory skipped (third-party)
- 2 files had merge conflicts, skipped
```

---

## Modes of Operation

### Check Mode (CI)

```
/docsheriff check [path]
```

- Validates against doc contract
- Reports violations without modifying
- Exit codes: 0 = pass, 1 = violations found
- Use in CI to block PRs with doc issues

### Fix Mode (Development)

```
/docsheriff fix [path]
```

- Applies safe auto-fixes
- Adds placeholders for meaning changes
- Generates report

### Audit Mode

```
/docsheriff audit
```

- Full scan of all documentation
- Freshness analysis
- Cross-link verification
- Glossary consistency check
- No modifications, report only

### New Mode

```
/docsheriff new [name]
```

- Interactive creation of new documentation
- Guided through template
- Automatic code scanning for references

### Monorepo Mode

```
/docsheriff monorepo [--fix]
```

**For monorepos:** Comprehensive structure validation including:
- Package drift detection (docs vs actual packages/)
- Build script validation (build:packages includes all packages)
- Structure diagram validation (tree diagrams match filesystem)
- Stale recommendation detection (future work that's already done)
- Cross-document consistency (all docs reference same package list)

Use `--fix` to auto-apply safe corrections.

See "Monorepo Structure Validation" section for full details.

### Sync Mode (Docs → Code TODOs)

```
/docsheriff sync [path]
```

**The killer feature:** DocSheriff reads your cleaned-up documentation and proposes a TODO list to bring the code into alignment with what the docs say it should do.

**How it works:**
1. Parses all documentation in scope
2. Extracts stated behaviors, features, and contracts
3. Scans codebase for implementation
4. Identifies gaps where docs describe something code doesn't implement
5. Asks for user feedback on each proposed TODO
6. Generates prioritized TODO list

**Example output:**

```markdown
## DocSheriff Sync Report

Based on documentation analysis, the following code work is needed:

### Proposed Code TODOs

| Priority | Source Doc | Claim | Code Status | Proposed TODO |
|----------|------------|-------|-------------|---------------|
| P1 | auth.md | "Supports OAuth2 PKCE flow" | Not found | Implement OAuth2 PKCE |
| P2 | api.md | "Rate limited to 100 req/min" | Hardcoded to 50 | Update rate limit config |
| P2 | setup.md | "Automatic retry on failure" | No retry logic | Add retry mechanism |
| P3 | readme.md | "Supports PostgreSQL and MySQL" | Only PostgreSQL | Add MySQL adapter |

### Questions for User

Before finalizing, please clarify:

1. **OAuth2 PKCE** - Is this planned for v2.0 or should the doc be corrected?
2. **Rate limiting** - Should code be updated to 100, or doc corrected to 50?
3. **MySQL support** - Is this still planned? Last commit mentioning it was 6 months ago.
```

**User feedback integration:**

DocSheriff will present findings and ask:
- "Should I create these as GitHub issues?"
- "Should I update the docs to match current code instead?"
- "Which items should be deferred vs immediate?"

---

## Document Type Handling

The skill handles different doc types appropriately:

| Type | Location Pattern | Template | Notes |
|------|------------------|----------|-------|
| README | `**/README.md` | readme-template | Entry points |
| Package docs | `packages/*/docs/*.md` | standard | Package-specific |
| App docs | `apps/*/docs/*.md` | standard | App-specific |
| ADRs | `**/adr/*.md`, `**/decisions/*.md` | adr-template | Don't restructure, only metadata |
| Runbooks | `**/runbooks/*.md`, `**/playbooks/*.md` | runbook-template | Ops-focused |
| CLAUDE.md | `**/CLAUDE.md` | claude-template | Claude Code instructions |

### Exclusions (Never Process)

- `node_modules/`
- `dist/`, `build/`, `.next/`, `target/`
- `**/generated/`
- `**/vendor/`
- `CHANGELOG.md` (has its own format)
- Files with `<!-- docsheriff: ignore -->` marker

---

## Minimal Diff Constraint

Docs are collaboration surfaces. Big rewrites create review pain.

### Rules

- Prefer smallest change that achieves compliance
- Don't reflow paragraphs unless necessary for compliance
- Don't reorder sections if it breaks narrative flow (unless template enforcement requested)
- Preserve whitespace style of the document
- Don't change code block content unless fixing syntax identifier
- Keep inline formatting (bold, italic, code) as-is

### Diff Size Warning

If changes exceed 30% of document, warn user:

```
⚠️ Large change detected (45% of document)
This may indicate the document needs full restructuring rather than cleanup.
Options:
1. Apply changes anyway
2. Create new document from template, migrate content manually
3. Review changes in detail first
```

---

## Interactive Workflow

When invoked without arguments:

```
What would you like to do?
1. check - Validate docs, report issues (no changes)
2. fix - Apply safe auto-fixes
3. audit - Full documentation audit
4. new - Create new documentation
5. monorepo - Validate monorepo structure & package docs
6. sync - Generate code TODOs from documentation

Scope?
1. All documentation
2. Specific directory
3. Single file

Options?
1. Include glossary normalization?
2. Enforce strict template order?
3. Generate evidence citations for all changes?
4. Include package drift detection? (monorepo mode)
```

---

## Supporting Files

- `template.md` - Full document templates
- `schema.yml` - Frontmatter and TODO schema for validation
- `glossary-template.yml` - Starter glossary

---

## CI Integration

See `ci-integration.md` for GitHub Actions / CI setup.

**Basic workflow:**

```yaml
# .github/workflows/doc-lint.yml
- name: Check documentation
  run: claude /docsheriff check
  # Fails if violations found
```

---

## Installation

**To use:** Create `.claude/skills/docsheriff/SKILL.md` in any project and paste this content.

---

## Monorepo Structure Validation

For monorepos, DocSheriff performs deep structure validation to catch documentation drift.

### Monorepo Mode

```
/docsheriff monorepo
```

Performs comprehensive monorepo-specific validation:

1. **Package Drift Detection** - Compares documented packages against actual `packages/` directory
2. **Build Script Validation** - Ensures `build:packages` includes all packages
3. **Structure Diagram Validation** - Verifies tree diagrams match filesystem
4. **Stale Recommendation Detection** - Finds "future work" that's already completed
5. **Cross-Doc Consistency** - Ensures all docs reference the same canonical package list

### Package Drift Detection

Compares what packages are documented vs what actually exists:

```markdown
## Package Drift Report

### Documented but Missing
| Package | Documented In | Status |
|---------|--------------|--------|
| @kestrel/legacy-utils | ARCHITECTURE.md | Not found in packages/ |

### Exist but Undocumented
| Package | Location | Suggestion |
|---------|----------|------------|
| @kestrel/new-feature | packages/new-feature | Add to package overview |

### Name Mismatches
| Documented Name | Actual Name | Files Affected |
|-----------------|-------------|----------------|
| @kestrel/util | @kestrel/utils | 3 docs |
```

### Build Script Validation

Checks that root `package.json` build scripts include all packages:

```markdown
## Build Script Analysis

### Root package.json: build:packages
Current: "turbo run build --filter=./packages/*"

### Missing from build:
| Package | Has build script? | Suggestion |
|---------|-------------------|------------|
| @kestrel/new-pkg | Yes | Add to turbo pipeline |

### In build but no script:
| Package | Issue |
|---------|-------|
| @kestrel/types | No "build" script in package.json |
```

### Structure Diagram Validation

Verifies ASCII tree diagrams match actual filesystem:

```markdown
## Structure Diagram Issues

### File: ARCHITECTURE.md (lines 45-78)

Documented structure:
├── packages/
│   ├── core/
│   ├── utils/
│   └── shared/

Actual structure:
├── packages/
│   ├── core/
│   ├── utils/
│   ├── shared/
│   └── new-feature/    ← UNDOCUMENTED

### Suggestions:
1. Add `new-feature/` to diagram
2. Or mark diagram with `<!-- partial: core packages only -->`
```

### Stale Recommendation Detection

Finds "future work" or "TODO" items in docs that have already been completed:

```markdown
## Stale Recommendations Found

### File: ROADMAP.md

| Line | Recommendation | Status | Evidence |
|------|---------------|--------|----------|
| 23 | "Add TypeScript support" | COMPLETED | tsconfig.json exists |
| 45 | "Create shared utils package" | COMPLETED | packages/utils/ exists |
| 67 | "Add CI/CD pipeline" | COMPLETED | .github/workflows/ exists |

### Suggested Actions:
1. Move completed items to "Completed" section
2. Or remove if no longer relevant
3. Update status from "planned" to "done"
```

### Cross-Document Consistency

Ensures all docs reference the same canonical package list:

```markdown
## Cross-Document Consistency Report

### Canonical Source: packages/README.md
Packages listed: core, utils, shared, types, cli

### Inconsistencies Found:

| Document | Lists | Missing | Extra |
|----------|-------|---------|-------|
| ARCHITECTURE.md | core, utils, shared | types, cli | - |
| CONTRIBUTING.md | core, utils, types | shared, cli | legacy |
| docs/setup.md | all 5 | - | - | ✓ |

### Recommendation:
Create single source of truth in packages/README.md
Reference via include: `<!-- include: packages/README.md#package-list -->`
```

### Monorepo Configuration

Create `.docsheriff.yml` in monorepo root:

```yaml
# .docsheriff.yml
monorepo:
  # Package discovery
  package_paths:
    - packages/*
    - apps/*

  # Canonical package list source
  canonical_source: packages/README.md

  # Build script to validate
  build_script: build:packages

  # Docs that should list all packages
  package_docs:
    - ARCHITECTURE.md
    - docs/packages.md

  # Structure diagrams to validate
  structure_diagrams:
    - file: ARCHITECTURE.md
      lines: 45-78
      scope: packages  # Only validate packages/ portion

  # Stale detection
  stale_markers:
    - "TODO:"
    - "FUTURE:"
    - "PLANNED:"
    - "Coming soon"

  # Ignore patterns
  ignore:
    - packages/deprecated-*
    - packages/internal-*
```

### Monorepo Output Example

```markdown
## DocSheriff Monorepo Validation Report

**Repository:** kestrel-monorepo
**Date:** 2024-01-21
**Packages Found:** 12

### Summary

| Check | Status | Issues |
|-------|--------|--------|
| Package Drift | ⚠️ | 2 undocumented packages |
| Build Scripts | ✓ | All packages included |
| Structure Diagrams | ⚠️ | 1 outdated diagram |
| Stale Recommendations | ⚠️ | 3 completed items still listed |
| Cross-Doc Consistency | ✗ | 4 docs have different package lists |

### Critical Issues (Fix Required)

1. **packages/new-feature** not documented anywhere
2. **ARCHITECTURE.md** diagram missing 2 packages
3. **CONTRIBUTING.md** references deleted package `legacy`

### Warnings (Review Recommended)

1. ROADMAP.md has 3 completed items still marked as planned
2. docs/setup.md references old package name `@kestrel/util`

### Auto-Fix Available

Run `/docsheriff monorepo --fix` to:
- Add missing packages to canonical list
- Update structure diagrams
- Fix package name typos
- Move completed roadmap items

Would you like me to apply these fixes?
```

---

*Built by Cory Shelton • [Carbon Black Roofing](https://carbonblackroofing.com) • Free to use and modify*
