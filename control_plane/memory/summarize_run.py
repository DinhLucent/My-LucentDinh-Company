"""Summarize Run — Generates compact run summaries after task execution."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RunSummarizer:
    """Produce a compact summary after each agent run."""

    def __init__(self, runtime_dir: Path) -> None:
        self.summary_dir = runtime_dir / "reports"
        self.summary_dir.mkdir(parents=True, exist_ok=True)

    def summarize(
        self,
        task: dict[str, Any],
        session_id: str,
        agent_output: dict[str, Any],
        verification_results: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        summary = {
            "session_id": session_id,
            "task_id": task["id"],
            "title": task.get("title", ""),
            "assigned_role": task.get("assigned_role"),
            "agent_status": agent_output.get("status"),
            "verification": verification_results or [],
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "next_step": self._decide_next(agent_output, verification_results),
        }

        out_path = self.summary_dir / f"{task['id']}.summary.json"
        out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        return summary

    def _decide_next(
        self, output: dict[str, Any], verifications: list[dict[str, Any]] | None
    ) -> str:
        if output.get("status") == "pending_execution":
            return "execute_agent"
        if verifications:
            failed = [v for v in verifications if v.get("result") == "failed"]
            if failed:
                return "retry_with_failure_context"
        return "complete_and_handoff"
