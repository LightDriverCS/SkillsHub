#!/usr/bin/env python3
"""
Build the skills index.json from all skill.json files.

Usage:
    python build_index.py
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def find_skills_dir() -> Path:
    """Find the skills directory."""
    if Path("skills").exists():
        return Path("skills")
    if Path("../skills").exists():
        return Path("../skills")
    current = Path.cwd()
    while current != current.parent:
        skills_dir = current / "skills"
        if skills_dir.exists():
            return skills_dir
        current = current.parent
    raise FileNotFoundError("Could not find skills directory")


def build_index():
    """Build the index.json file from all skill.json files."""
    try:
        skills_dir = find_skills_dir()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

    skills = []

    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue

        skill_json_path = item / "skill.json"
        if not skill_json_path.exists():
            print(f"  Warning: No skill.json in {item.name}, skipping")
            continue

        try:
            with open(skill_json_path, "r", encoding="utf-8") as f:
                skill_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  Error: Invalid JSON in {skill_json_path}: {e}")
            continue

        # Extract fields for index
        index_entry = {
            "name": skill_data.get("name", item.name),
            "version": skill_data.get("version", "0.0.0"),
            "author": skill_data.get("author", "Unknown"),
            "license": skill_data.get("license", "Unknown"),
            "description": skill_data.get("description", ""),
            "tags": skill_data.get("tags", []),
            "entrypoint": skill_data.get("entrypoint", ""),
            "language": skill_data.get("language", ""),
            "path": item.name,
        }
        skills.append(index_entry)
        print(f"  Added: {item.name}")

    # Build index
    index = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "skills": skills,
        "total_count": len(skills),
    }

    # Write index
    index_path = skills_dir / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"\nGenerated {index_path} with {len(skills)} skill(s)")
    return True


if __name__ == "__main__":
    print("Building skills index...")
    success = build_index()
    exit(0 if success else 1)
