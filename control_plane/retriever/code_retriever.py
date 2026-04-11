"""Code Retriever — Retrieves relevant code paths for a task."""
from __future__ import annotations

from pathlib import Path
from typing import Any


class CodeRetriever:
    """Find code files relevant to a task by path or domain scanning."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def retrieve(self, task: dict[str, Any], domain: str) -> list[str]:
        """Return list of relevant code paths."""
        explicit = task.get("inputs", {}).get("related_paths", [])
        if explicit:
            return [p for p in explicit if (self.repo_root / p).exists()]

        # Fallback: scan for domain-named directories
        return self._scan_by_domain(domain)

    def _scan_by_domain(self, domain: str, limit: int = 10) -> list[str]:
        results: list[str] = []
        src_dir = self.repo_root / "src"
        if not src_dir.exists():
            return results
        for path in src_dir.rglob(f"*{domain}*"):
            if path.is_file() and path.suffix in (".py", ".ts", ".js", ".go"):
                results.append(str(path.relative_to(self.repo_root)))
                if len(results) >= limit:
                    break
        return results
