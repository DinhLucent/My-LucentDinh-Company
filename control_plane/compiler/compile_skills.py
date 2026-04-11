"""Compile Skills — Parse Skills/**/SKILL.md → skill_index.json.

Reads SKILL.md frontmatter (YAML between --- delimiters) plus the
file body to extract description, triggers, and tags.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


def compile_skills(repo_root: Path) -> Path:
    """Walk Skills/ directory and produce knowledge/compiled/skill_index.json."""
    skills_dir = repo_root / "Skills"
    output_dir = repo_root / "knowledge" / "compiled"
    output_dir.mkdir(parents=True, exist_ok=True)

    compiled: dict[str, Any] = {}

    if skills_dir.exists():
        for skill_md in skills_dir.rglob("SKILL.md"):
            skill_key = skill_md.parent.relative_to(skills_dir).as_posix()
            entry = _parse_skill(skill_md)
            compiled[skill_key] = entry

    # Also scan .skills_pool if present
    pool_dir = repo_root / ".skills_pool"
    if pool_dir.exists():
        for skill_md in pool_dir.rglob("SKILL.md"):
            skill_key = f".skills_pool/{skill_md.parent.relative_to(pool_dir).as_posix()}"
            entry = _parse_skill(skill_md)
            compiled[skill_key] = entry

    out_path = output_dir / "skill_index.json"
    out_path.write_text(json.dumps(compiled, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def _parse_skill(path: Path) -> dict[str, Any]:
    """Extract frontmatter + first paragraph from a SKILL.md file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter: dict[str, Any] = {}
    body = text

    # Try to parse YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
        body = fm_match.group(2)

    # Extract first meaningful paragraph as summary
    lines = [l.strip() for l in body.splitlines() if l.strip() and not l.startswith("#")]
    summary = " ".join(lines[:3])[:300]

    return {
        "path": str(path),
        "description": frontmatter.get("description", summary),
        "triggers": frontmatter.get("triggers", []),
        "tags": frontmatter.get("tags", []),
        "summary": summary,
    }


if __name__ == "__main__":
    result = compile_skills(Path(".").resolve())
    print(f"Compiled skill index → {result}")
