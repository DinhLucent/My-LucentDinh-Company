"""Acceptance Checker — Validates task output against acceptance criteria."""
from __future__ import annotations

from typing import Any


class AcceptanceChecker:
    """Check whether execution results satisfy acceptance criteria."""

    def check(self, task: dict[str, Any], execution_result: dict[str, Any]) -> dict[str, Any]:
        criteria = task.get("acceptance_criteria", [])
        satisfied = execution_result.get("satisfied_criteria", [])
        missing = [c for c in criteria if c not in satisfied]

        return {
            "name": "acceptance",
            "result": "passed" if not missing else "failed",
            "total_criteria": len(criteria),
            "satisfied": len(satisfied),
            "missing_criteria": missing,
        }
