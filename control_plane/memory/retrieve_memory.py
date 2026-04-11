"""Retrieve Memory — Scoped memory retrieval for sessions, tasks, and modules."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MemoryRetriever:
    """Retrieve compact memory by scope: session, task, or module."""

    def __init__(self, memory_dir: Path, runtime_dir: Path) -> None:
        self.memory_dir = memory_dir
        self.runtime_dir = runtime_dir

    def get_task_memory(self, task_id: str) -> dict[str, Any]:
        """Get all memory for a specific task."""
        decisions = self._load_json(self.memory_dir / "tasks" / f"{task_id}.decisions.json")
        summary = self._load_json(self.runtime_dir / "reports" / f"{task_id}.summary.json")
        return {"decisions": decisions, "summary": summary}

    def get_module_memory(self, module: str, limit: int = 5) -> list[dict[str, Any]]:
        """Get recent decisions for a module."""
        decisions = self._load_json(self.memory_dir / "modules" / f"{module}.decisions.json")
        if isinstance(decisions, list):
            return decisions[-limit:]
        return []

    def get_session_memory(self, session_id: str) -> dict[str, Any] | None:
        """Get session memory if available."""
        path = self.memory_dir / "sessions" / f"{session_id}.json"
        return self._load_json(path) if path.exists() else None

    def _load_json(self, path: Path) -> Any:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
