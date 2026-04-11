"""On Verification Fail Hook — Injects minimal failure context for retries.

Instead of reloading the entire context, only appends the specific
failure details needed for the next attempt.
"""
from __future__ import annotations

from typing import Any


class OnVerificationFailHook:
    """Compute minimal additional context needed after a verification failure."""

    MAX_RETRIES = 3

    def run(
        self,
        verification_report: dict[str, Any],
        attempt: int = 1,
    ) -> dict[str, Any]:
        failed_checks = [
            c for c in verification_report.get("checks", [])
            if c.get("result") == "failed"
        ]

        additional_context = []
        for check in failed_checks:
            if check["name"] == "pytest":
                additional_context.append("stack_trace")
                additional_context.append("failing_test_source")
            elif check["name"] == "lint":
                additional_context.append("lint_error_details")
            elif check["name"] == "typecheck":
                additional_context.append("type_error_details")
            elif check["name"] == "security":
                additional_context.append("security_finding_details")

        should_retry = attempt < self.MAX_RETRIES
        should_escalate = not should_retry

        return {
            "hook": "on_verification_fail",
            "failed_checks": [c["name"] for c in failed_checks],
            "additional_context_needed": additional_context,
            "attempt": attempt,
            "should_retry": should_retry,
            "should_escalate": should_escalate,
            "escalation_target": "reviewer" if should_escalate else None,
        }
