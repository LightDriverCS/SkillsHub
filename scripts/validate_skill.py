#!/usr/bin/env python3
"""
Validate skill.json files in the SkillsHub repository.

Usage:
    python validate_skill.py [skill_path]
    python validate_skill.py skills/DocSheriff
    python validate_skill.py  # validates all skills
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

REQUIRED_FIELDS = [
    "name",
    "version",
    "author",
    "license",
    "description",
    "tags",
    "entrypoint",
    "language",
    "requirements",
    "usage",
    "tested_on",
    "created_at",
    "updated_at",
]

VALID_LANGUAGES = ["markdown", "python", "javascript", "typescript", "other"]
VALID_PLATFORMS = ["mac", "windows", "linux"]


def validate_date(date_str: str) -> bool:
    """Validate ISO date format YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_version(version: str) -> bool:
    """Validate semantic version format."""
    parts = version.split(".")
    if len(parts) != 3:
        return False
    return all(part.isdigit() for part in parts)


def validate_skill(skill_path: Path) -> list[str]:
    """Validate a single skill directory. Returns list of errors."""
    errors = []
    skill_json_path = skill_path / "skill.json"
    readme_path = skill_path / "README.md"

    # Check skill.json exists
    if not skill_json_path.exists():
        errors.append(f"Missing skill.json in {skill_path}")
        return errors

    # Check README.md exists
    if not readme_path.exists():
        errors.append(f"Missing README.md in {skill_path}")

    # Parse skill.json
    try:
        with open(skill_json_path, "r", encoding="utf-8") as f:
            skill_data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in {skill_json_path}: {e}")
        return errors

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in skill_data:
            errors.append(f"Missing required field '{field}' in {skill_json_path}")

    # Validate name matches folder
    if "name" in skill_data:
        if skill_data["name"] != skill_path.name:
            errors.append(
                f"Skill name '{skill_data['name']}' doesn't match folder name '{skill_path.name}'"
            )

    # Validate version format
    if "version" in skill_data:
        if not validate_version(skill_data["version"]):
            errors.append(
                f"Invalid version format '{skill_data['version']}' - use semantic versioning (e.g., 1.0.0)"
            )

    # Validate language
    if "language" in skill_data:
        if skill_data["language"].lower() not in VALID_LANGUAGES:
            errors.append(
                f"Invalid language '{skill_data['language']}' - must be one of {VALID_LANGUAGES}"
            )

    # Validate tags is array
    if "tags" in skill_data:
        if not isinstance(skill_data["tags"], list):
            errors.append("'tags' must be an array")
        elif len(skill_data["tags"]) == 0:
            errors.append("'tags' array cannot be empty")

    # Validate requirements is array
    if "requirements" in skill_data:
        if not isinstance(skill_data["requirements"], list):
            errors.append("'requirements' must be an array")

    # Validate tested_on
    if "tested_on" in skill_data:
        if not isinstance(skill_data["tested_on"], list):
            errors.append("'tested_on' must be an array")
        else:
            for platform in skill_data["tested_on"]:
                if platform.lower() not in VALID_PLATFORMS:
                    errors.append(
                        f"Invalid platform '{platform}' - must be one of {VALID_PLATFORMS}"
                    )

    # Validate dates
    if "created_at" in skill_data:
        if not validate_date(skill_data["created_at"]):
            errors.append(
                f"Invalid date format for 'created_at': {skill_data['created_at']} - use YYYY-MM-DD"
            )

    if "updated_at" in skill_data:
        if not validate_date(skill_data["updated_at"]):
            errors.append(
                f"Invalid date format for 'updated_at': {skill_data['updated_at']} - use YYYY-MM-DD"
            )

    # Validate entrypoint exists
    if "entrypoint" in skill_data:
        entrypoint_path = skill_path / skill_data["entrypoint"]
        if not entrypoint_path.exists():
            errors.append(
                f"Entrypoint file '{skill_data['entrypoint']}' not found in {skill_path}"
            )

    return errors


def find_skills_dir() -> Path:
    """Find the skills directory."""
    # Check if we're in the repo root
    if Path("skills").exists():
        return Path("skills")
    # Check if we're in scripts directory
    if Path("../skills").exists():
        return Path("../skills")
    # Check parent directories
    current = Path.cwd()
    while current != current.parent:
        skills_dir = current / "skills"
        if skills_dir.exists():
            return skills_dir
        current = current.parent
    raise FileNotFoundError("Could not find skills directory")


def main():
    """Main entry point."""
    all_errors = []

    if len(sys.argv) > 1:
        # Validate specific skill
        skill_path = Path(sys.argv[1])
        if not skill_path.exists():
            print(f"Error: Path '{skill_path}' does not exist")
            sys.exit(1)
        if not skill_path.is_dir():
            print(f"Error: Path '{skill_path}' is not a directory")
            sys.exit(1)

        print(f"Validating skill: {skill_path.name}")
        errors = validate_skill(skill_path)
        all_errors.extend(errors)
    else:
        # Validate all skills
        try:
            skills_dir = find_skills_dir()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

        print(f"Validating all skills in {skills_dir}")
        skill_count = 0

        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                # Skip index.json
                if item.name == "index.json":
                    continue
                skill_count += 1
                print(f"  Validating: {item.name}")
                errors = validate_skill(item)
                all_errors.extend(errors)

        print(f"\nValidated {skill_count} skill(s)")

    # Report results
    if all_errors:
        print(f"\nValidation failed with {len(all_errors)} error(s):\n")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\nValidation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
