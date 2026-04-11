"""Knowledge Retriever — Retrieves compiled fragments by domain/task.

Selects the minimum context needed from compiled indexes and fragments
instead of loading raw markdown.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class KnowledgeRetriever:
    """Retrieve context fragments, files, tests, and handoffs for a task."""

    def __init__(self, repo_root: Path, knowledge_dir: Path, hub_dir: Path) -> None:
        self.repo_root = repo_root
        self.knowledge_dir = knowledge_dir
        self.hub_dir = hub_dir
        self.fragments_dir = knowledge_dir / "compiled" / "context_fragments"

    def retrieve(
        self,
        task: dict[str, Any],
        classification: dict[str, Any],
        routing: dict[str, Any],
    ) -> dict[str, Any]:
        domain = classification["domain"]
        inputs = task.get("inputs", {})
        files: list[str] = inputs.get("related_paths", [])
        tests: list[str] = inputs.get("related_tests", [])
        handoff_refs: list[str] = inputs.get("related_handoffs", [])

        # Auto-discover handoffs if none specified
        if not handoff_refs:
            handoff_refs = self._find_recent_handoffs(domain, limit=2)

        fragments = self._select_fragments(domain)
        dashboard_snapshot = self._read_dashboard_snapshot()

        return {
            "domain": domain,
            "files": files,
            "tests": tests,
            "handoffs": handoff_refs,
            "fragments": fragments,
            "dashboard_snapshot": dashboard_snapshot,
            "role": routing["primary_role"],
        }

    # ── Private helpers ──────────────────────────────────────

    def _select_fragments(self, domain: str) -> list[dict[str, str]]:
        """Select fragments matching the task domain."""
        results: list[dict[str, str]] = []
        if not self.fragments_dir.exists():
            return results

        for path in self.fragments_dir.glob("*.json"):
            # Include if domain appears in filename or if it's a core doc
            if domain in path.name or path.name in (
                "operating_rules.summary.json",
                "soul.summary.json",
            ):
                results.append({
                    "id": path.stem,
                    "type": "module_summary",
                    "path": str(path.relative_to(self.repo_root)),
                })
        return results

    def _find_recent_handoffs(self, domain: str, limit: int = 2) -> list[str]:
        """Find recent handoff files in .hub/handoffs/ related to domain."""
        handoffs_dir = self.hub_dir / "handoffs"
        if not handoffs_dir.exists():
            return []
        all_handoffs = sorted(handoffs_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        return [str(h.relative_to(self.repo_root)) for h in all_handoffs[:limit]]

    def _read_dashboard_snapshot(self) -> dict[str, Any] | None:
        """Read cached dashboard snapshot if available."""
        snapshot_path = (
            self.repo_root / "runtime" / "cache" / "summaries" / "current_dashboard.json"
        )
        if snapshot_path.exists():
            return json.loads(snapshot_path.read_text(encoding="utf-8"))
        return None
