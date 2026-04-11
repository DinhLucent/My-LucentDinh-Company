"""Store Decisions — Persists decision logs per task and module."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class DecisionStore:
    """Store and retrieve decision logs scoped by task or module."""

    def __init__(self, memory_dir: Path) -> None:
        self.tasks_dir = memory_dir / "tasks"
        self.modules_dir = memory_dir / "modules"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.modules_dir.mkdir(parents=True, exist_ok=True)

    def store_task_decision(self, task_id: str, decision: dict[str, Any]) -> Path:
        """Append a decision to a task's decision log."""
        log_path = self.tasks_dir / f"{task_id}.decisions.json"
        log = self._load_log(log_path)
        decision["timestamp"] = datetime.now(timezone.utc).isoformat()
        log.append(decision)
        log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
        return log_path

    def store_module_decision(self, module: str, decision: dict[str, Any]) -> Path:
        """Append a decision to a module's decision log."""
        log_path = self.modules_dir / f"{module}.decisions.json"
        log = self._load_log(log_path)
        decision["timestamp"] = datetime.now(timezone.utc).isoformat()
        log.append(decision)
        log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
        return log_path

    def get_task_decisions(self, task_id: str) -> list[dict[str, Any]]:
        log_path = self.tasks_dir / f"{task_id}.decisions.json"
        return self._load_log(log_path)

    def get_module_decisions(self, module: str, limit: int = 10) -> list[dict[str, Any]]:
        log_path = self.modules_dir / f"{module}.decisions.json"
        log = self._load_log(log_path)
        return log[-limit:]

    def _load_log(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))
