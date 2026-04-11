"""Pre-Task Hook — Runs before task execution.

Ensures compiled indexes are fresh and dashboard snapshot is hydrated.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PreTaskHook:
    """Pre-task lifecycle hook."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.compiled_dir = repo_root / "knowledge" / "compiled"
        self.cache_dir = repo_root / "runtime" / "cache" / "summaries"

    def run(self) -> dict[str, Any]:
        """Check caches and recompile if stale."""
        actions: list[str] = []

        # Check if compiled indexes exist
        if not (self.compiled_dir / "role_index.json").exists():
            actions.append("role_index_missing")
        if not (self.compiled_dir / "skill_index.json").exists():
            actions.append("skill_index_missing")
        if not (self.compiled_dir / "project_index.json").exists():
            actions.append("project_index_missing")

        # Hydrate dashboard snapshot
        self._hydrate_dashboard()
        actions.append("dashboard_snapshot_hydrated")

        return {
            "hook": "pre_task",
            "actions": actions,
            "needs_recompile": any("missing" in a for a in actions),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _hydrate_dashboard(self) -> None:
        """Parse DASHBOARD.md → JSON snapshot."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        dashboard_path = self.repo_root / "DASHBOARD.md"
        if not dashboard_path.exists():
            return

        text = dashboard_path.read_text(encoding="utf-8", errors="replace")
        snapshot = {
            "active_tasks": [],
            "blocked_tasks": [],
            "recent_handoffs": [],
            "focus_modules": [],
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "raw_summary": text[:500],
        }

        out_path = self.cache_dir / "current_dashboard.json"
        out_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
