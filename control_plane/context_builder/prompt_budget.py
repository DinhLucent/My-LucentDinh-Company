"""Prompt Budget — Token budget enforcement for context loading.

Ensures the total context sent to the LLM stays within limits.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BudgetConfig:
    max_input_tokens: int = 12000
    max_code_tokens: int = 8000
    max_memory_tokens: int = 1500
    chars_per_token: float = 3.5  # rough estimate


class PromptBudget:
    """Enforce token budget on context fragments."""

    def __init__(self, config: BudgetConfig | None = None) -> None:
        self.config = config or BudgetConfig()

    def trim_fragments(self, fragments: list[dict[str, Any]], budget_key: str = "max_input_tokens") -> list[dict[str, Any]]:
        """Trim fragment list to fit within token budget."""
        max_chars = int(getattr(self.config, budget_key) * self.config.chars_per_token)
        total_chars = 0
        trimmed: list[dict[str, Any]] = []

        for frag in fragments:
            content = frag.get("content", frag.get("summary", ""))
            frag_chars = len(str(content))
            if total_chars + frag_chars > max_chars:
                break
            trimmed.append(frag)
            total_chars += frag_chars

        return trimmed

    def estimate_tokens(self, text: str) -> int:
        """Rough token count estimate."""
        return int(len(text) / self.config.chars_per_token)
