"""On Handoff Hook — Normalizes handoff format when agents transfer work."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class OnHandoffHook:
    """Normalize and store handoff documents."""

    def __init__(self, hub_dir: Path) -> None:
        self.handoffs_dir = hub_dir / "handoffs"
        self.handoffs_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        task_id: str,
        from_role: str,
        to_role: str,
        completed: list[str],
        needs_continuation: list[str],
        context: str = "",
    ) -> Path:
        handoff = {
            "task_id": task_id,
            "from": from_role,
            "to": to_role,
            "completed": completed,
            "needs_continuation": needs_continuation,
            "context": context,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        filename = f"{task_id}-{from_role}-to-{to_role}.json"
        out_path = self.handoffs_dir / filename
        out_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False), encoding="utf-8")
        return out_path
