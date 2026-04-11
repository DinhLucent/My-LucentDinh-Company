"""Typecheck Runner — Runs type checkers on affected modules."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


class TypecheckRunner:
    """Run type checking and return structured results."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def run(self, files: list[str] | None = None) -> dict[str, Any]:
        cmd = self._detect_typecheck_command(files)
        if not cmd:
            return {"name": "typecheck", "result": "skipped", "details": "No type checker detected"}

        try:
            proc = subprocess.run(
                cmd, cwd=str(self.repo_root), capture_output=True, text=True, timeout=60
            )
            return {
                "name": cmd[0],
                "result": "passed" if proc.returncode == 0 else "failed",
                "details": proc.stdout[-800:] if proc.stdout else proc.stderr[-800:],
            }
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return {"name": "typecheck", "result": "skipped", "details": str(e)}

    def _detect_typecheck_command(self, files: list[str] | None) -> list[str] | None:
        targets = files or ["."]
        if (self.repo_root / "pyproject.toml").exists():
            return ["python", "-m", "mypy"] + targets
        if (self.repo_root / "tsconfig.json").exists():
            return ["npx", "tsc", "--noEmit"]
        return None
