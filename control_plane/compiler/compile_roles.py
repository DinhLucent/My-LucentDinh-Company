"""Compile Roles — Parse manifest.yaml → role_index.json.

Reads the existing manifest.yaml (list-of-dicts format) and produces
a compiled role_index.json that the runtime can consume directly.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


# Default capabilities when manifest doesn't specify runtime block
_DEFAULT_TASK_TYPES: dict[str, list[str]] = {
    "cto": ["architecture", "review", "planning"],
    "backend": ["bugfix", "feature", "refactor"],
    "frontend": ["bugfix", "feature", "refactor"],
    "fullstack": ["bugfix", "feature", "refactor"],
    "qa": ["test", "verification", "bugfix_review"],
    "security": ["security", "audit", "review"],
    "devops": ["infra", "deployment", "hotfix"],
    "docs": ["documentation"],
    "reviewer": ["review"],
    "producer": ["planning", "sprint"],
}


def _normalise_role_key(agent_id: str) -> str:
    """Strip '-agent' suffix for cleaner index keys."""
    return re.sub(r"-agent$", "", agent_id)


def compile_roles(repo_root: Path) -> Path:
    """Read manifest.yaml and produce knowledge/compiled/role_index.json."""
    manifest_path = repo_root / "manifest.yaml"
    output_dir = repo_root / "knowledge" / "compiled"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.yaml not found: {manifest_path}")

    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

    # manifest.yaml uses a list of agent dicts, not a dict-of-dicts
    agents_list: list[dict[str, Any]] = data.get("agents", [])
    active_ids: list[str] = data.get("active_agents", [])

    compiled: dict[str, Any] = {}

    for agent in agents_list:
        agent_id = agent.get("id", "")
        role_key = _normalise_role_key(agent_id)

        # Check for inline runtime block (v2 manifest extension)
        runtime = agent.get("runtime", {})

        compiled[role_key] = {
            "agent_id": agent_id,
            "name": agent.get("name", ""),
            "persona_path": agent.get("persona", ""),
            "skills": agent.get("skills", []),
            "active": agent_id in active_ids,
            "allowed_task_types": runtime.get(
                "allowed_task_types",
                _DEFAULT_TASK_TYPES.get(role_key, ["bugfix", "feature"]),
            ),
            "required_context_types": runtime.get(
                "required_context", ["task_packet", "code", "tests"],
            ),
            "verification_defaults": runtime.get(
                "verification", ["lint", "tests"],
            ),
            "handoff_targets": runtime.get("handoff_targets", []),
            "max_parallel_tasks": runtime.get("max_parallel_tasks", 1),
            "memory_scope": runtime.get("memory_scope", "module"),
        }

    out_path = output_dir / "role_index.json"
    out_path.write_text(json.dumps(compiled, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    result = compile_roles(Path(".").resolve())
    print(f"Compiled role index → {result}")
