"""Test Runner — Runs project tests and reports structured results."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class TestRunner:
    """Run tests and produce a structured verification result."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def run(self, test_paths: list[str] | None = None) -> dict[str, Any]:
        """Run tests. Returns { name, result, details }."""
        cmd = self._detect_test_command(test_paths)
        if not cmd:
            return {"name": "pytest", "result": "skipped", "details": "No test command detected"}

        try:
            proc = subprocess.run(
                cmd, cwd=str(self.repo_root), capture_output=True, text=True, timeout=120
            )
            return {
                "name": cmd[0],
                "result": "passed" if proc.returncode == 0 else "failed",
                "details": proc.stdout[-1000:] if proc.stdout else proc.stderr[-1000:],
                "returncode": proc.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"name": cmd[0], "result": "timeout", "details": "Test execution timed out (120s)"}
        except FileNotFoundError:
            return {"name": cmd[0], "result": "skipped", "details": f"Command not found: {cmd[0]}"}

    def _detect_test_command(self, test_paths: list[str] | None) -> list[str] | None:
        if (self.repo_root / "pytest.ini").exists() or (self.repo_root / "pyproject.toml").exists():
            cmd = ["python", "-m", "pytest", "-v", "--tb=short"]
            if test_paths:
                cmd.extend(test_paths)
            return cmd
        if (self.repo_root / "package.json").exists():
            return ["npm", "test", "--", "--passWithNoTests"]
        return None
