"""Security Checker — Runs basic security checks on changed files."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


# Patterns that indicate potential security issues
_SECRET_PATTERNS = [
    (r"(?i)(password|secret|api.?key|token)\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret/credential"),
    (r"(?i)BEGIN\s+(RSA|EC|DSA)\s+PRIVATE\s+KEY", "Hardcoded private key"),
    (r"(?i)(aws_access_key|aws_secret)", "AWS credential in code"),
]

_PII_PATTERNS = [
    (r"(?i)print\s*\(.*?(email|ssn|phone|address|password)", "Possible PII in print/log"),
    (r"(?i)log(ger)?\.(info|debug|warn)\(.*?(email|password|token)", "Possible PII in log"),
]


class SecurityChecker:
    """Run basic security checks on source files."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def check(self, files: list[str]) -> dict[str, Any]:
        findings: list[dict[str, Any]] = []

        for file_path in files:
            full_path = self.repo_root / file_path
            if not full_path.exists() or not full_path.is_file():
                continue

            try:
                content = full_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            for pattern, desc in _SECRET_PATTERNS + _PII_PATTERNS:
                for match in re.finditer(pattern, content):
                    line_no = content[:match.start()].count("\n") + 1
                    findings.append({
                        "file": file_path,
                        "line": line_no,
                        "issue": desc,
                        "snippet": content[max(0, match.start() - 20):match.end() + 20][:100],
                    })

        return {
            "name": "security",
            "result": "passed" if not findings else "failed",
            "findings": findings,
            "details": f"{len(findings)} issue(s) found" if findings else "No issues",
        }
