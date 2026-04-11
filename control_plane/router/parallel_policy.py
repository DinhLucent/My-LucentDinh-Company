"""Parallel Policy — Decides when multi-agent execution is allowed.

Default: solo. Only escalates to paired or directed swarm
when risk/task-size thresholds are met.
"""
from __future__ import annotations

from typing import Any


class ParallelPolicy:
    """Gate for multi-agent execution — never the default."""

    # Maximum agents per mode
    MODE_LIMITS = {
        "solo": 1,
        "paired": 2,
        "directed_swarm": 5,
    }

    def evaluate(self, classification: dict[str, Any], routing: dict[str, Any]) -> dict[str, Any]:
        mode = routing.get("mode", "solo")
        max_agents = self.MODE_LIMITS.get(mode, 1)

        return {
            "mode": mode,
            "max_agents": max_agents,
            "parallel_allowed": mode != "solo",
            "reason": self._reason(mode, classification),
        }

    def _reason(self, mode: str, classification: dict[str, Any]) -> str:
        if mode == "solo":
            return "Low/medium risk, single-role task"
        if mode == "paired":
            return f"Risk={classification['risk_level']}, adding reviewer/qa"
        return f"High risk ({classification['risk_level']}), directed swarm with full review chain"
