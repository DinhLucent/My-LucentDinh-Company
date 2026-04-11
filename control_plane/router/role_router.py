"""Role Router — Maps classified tasks to the correct agent(s).

Reads role_index.json to validate agent capabilities and decides
solo / paired / directed-swarm execution mode.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RoleRouter:
    """Route a classified task to primary + secondary agents."""

    def __init__(self, knowledge_dir: Path) -> None:
        self.role_index_path = knowledge_dir / "compiled" / "role_index.json"
        self.role_index = self._load_role_index()

    def _load_role_index(self) -> dict[str, Any]:
        if not self.role_index_path.exists():
            return {}
        return json.loads(self.role_index_path.read_text(encoding="utf-8"))

    def route(self, task: dict[str, Any], classification: dict[str, Any]) -> dict[str, Any]:
        assigned_role = task.get("assigned_role")
        task_type = classification["task_type"]
        risk_level = classification["risk_level"]

        # Honour explicit assignment if the role supports the task type
        if assigned_role and self._role_supports(assigned_role, task_type):
            primary_role = assigned_role
        else:
            primary_role = self._infer_role(task_type, classification.get("domain", "general"))

        secondary_roles = self._decide_secondary(risk_level, primary_role)
        mode = self._decide_mode(risk_level, secondary_roles)

        return {
            "primary_role": primary_role,
            "secondary_roles": secondary_roles,
            "mode": mode,
        }

    # ── Helpers ──────────────────────────────────────────────

    def _role_supports(self, role: str, task_type: str) -> bool:
        config = self.role_index.get(role, {})
        allowed = config.get("allowed_task_types", [])
        if not allowed:
            # No compiled index → assume OK
            return True
        return task_type in allowed

    def _infer_role(self, task_type: str, domain: str) -> str:
        if task_type == "security":
            return "security"
        if task_type == "documentation":
            return "docs"
        if task_type == "test":
            return "qa"
        if domain == "frontend":
            return "frontend"
        return "backend"

    def _decide_secondary(self, risk_level: str, primary: str) -> list[str]:
        if risk_level != "high":
            return []
        secondary: list[str] = []
        if primary != "reviewer" and "reviewer" in self.role_index:
            secondary.append("reviewer")
        if primary != "qa" and "qa" in self.role_index:
            secondary.append("qa")
        if primary != "security" and "security" in self.role_index:
            secondary.append("security")
        return secondary

    def _decide_mode(self, risk_level: str, secondary: list[str]) -> str:
        if not secondary:
            return "solo"
        if len(secondary) == 1:
            return "paired"
        return "directed_swarm"
