"""Packet Builder — Assembles the task_packet.json for an agent.

The task packet is the ONLY structured object sent to the LLM,
plus relevant code/test snippets. No raw handbook loading.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PacketBuilder:
    """Build a minimal, focused task packet from classified + retrieved data."""

    def __init__(self, runtime_dir: Path) -> None:
        self.runtime_dir = runtime_dir
        self.packet_dir = runtime_dir / "state" / "task_packets"
        self.packet_dir.mkdir(parents=True, exist_ok=True)

    def build(
        self,
        task: dict[str, Any],
        session_id: str,
        classification: dict[str, Any],
        routing: dict[str, Any],
        context_bundle: dict[str, Any],
    ) -> Path:
        """Build and persist a task packet, return the file path."""
        task_id = task["id"]

        packet = {
            "task_id": task_id,
            "session_id": session_id,
            "role": routing["primary_role"],
            "secondary_roles": routing.get("secondary_roles", []),
            "mode": routing.get("mode", "solo"),
            "task_type": classification["task_type"],
            "domain": classification["domain"],
            "risk_level": classification["risk_level"],
            "goal": task.get("title", ""),
            "summary": task.get("description", ""),
            "rules": self._build_rules(task),
            "context_budget": {
                "max_input_tokens": 12000,
                "max_code_tokens": 8000,
                "max_memory_tokens": 1500,
            },
            "context_fragments": context_bundle.get("fragments", []),
            "files": context_bundle.get("files", []),
            "tests": context_bundle.get("tests", []),
            "handoff_refs": context_bundle.get("handoffs", []),
            "memory_refs": [],
            "verification_plan": self._build_verification_plan(
                routing["primary_role"], classification["risk_level"]
            ),
            "expected_outputs": self._expected_outputs(classification["task_type"]),
            "acceptance_criteria": task.get("acceptance_criteria", []),
        }

        out_path = self.packet_dir / f"{task_id}.json"
        out_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False), encoding="utf-8")
        return out_path

    # ── Private helpers ──────────────────────────────────────

    def _build_rules(self, task: dict[str, Any]) -> list[str]:
        rules = [
            "Prefer minimal patch",
            "Do not change unrelated modules",
            "Update handoff after execution",
        ]
        rules.extend(task.get("constraints", []))
        return rules

    def _build_verification_plan(self, role: str, risk: str) -> list[str]:
        plan = ["lint changed files"]
        if role in ("backend", "fullstack", "frontend"):
            plan.append("typecheck related module")
        plan.append("run related tests")
        if risk == "high":
            plan.append("security check")
        return plan

    def _expected_outputs(self, task_type: str) -> list[str]:
        base = ["patch", "change_summary", "handoff_update"]
        if task_type == "documentation":
            base = ["doc_update", "change_summary"]
        elif task_type == "test":
            base = ["test_files", "coverage_report"]
        return base
