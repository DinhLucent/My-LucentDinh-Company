"""Post-Task Hook — Runs after task execution.

Summarizes run, compacts memory, and updates dashboard state.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class PostTaskHook:
    """Post-task lifecycle hook."""

    def run(
        self,
        task: dict[str, Any],
        session_id: str,
        agent_output: dict[str, Any],
        verification_results: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return {
            "hook": "post_task",
            "task_id": task.get("id"),
            "session_id": session_id,
            "status": agent_output.get("status"),
            "verification_passed": all(
                v.get("result") == "passed" for v in (verification_results or [])
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
