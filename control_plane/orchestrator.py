"""Orchestrator — Main entry point for the v2 control plane.

Flow: classify → route → retrieve → build_packet → (execute) → verify → memory
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from control_plane.classifier.task_classifier import TaskClassifier
from control_plane.router.role_router import RoleRouter
from control_plane.router.parallel_policy import ParallelPolicy
from control_plane.retriever.knowledge_retriever import KnowledgeRetriever
from control_plane.context_builder.packet_builder import PacketBuilder
from control_plane.context_builder.prompt_budget import PromptBudget
from control_plane.verifier.acceptance_checker import AcceptanceChecker
from control_plane.verifier.security_checker import SecurityChecker
from control_plane.memory.summarize_run import RunSummarizer
from control_plane.memory.store_decisions import DecisionStore
from control_plane.hooks.pre_task import PreTaskHook
from control_plane.hooks.post_task import PostTaskHook
from control_plane.hooks.on_verification_fail import OnVerificationFailHook


@dataclass
class OrchestratorConfig:
    """Configuration paths for the orchestrator."""
    repo_root: Path
    runtime_dir: Path
    knowledge_dir: Path
    hub_dir: Path
    max_verification_retries: int = 3


class Orchestrator:
    """
    Central orchestrator that coordinates the full task lifecycle:

    1. Pre-task hook (check caches)
    2. Classify task
    3. Route to agent(s)
    4. Retrieve relevant context
    5. Build task packet
    6. [Agent execution — external]
    7. Verify output
    8. Store memory + summarize
    9. Post-task hook
    """

    def __init__(self, config: OrchestratorConfig) -> None:
        self.config = config
        self.classifier = TaskClassifier(config.knowledge_dir)
        self.router = RoleRouter(config.knowledge_dir)
        self.parallel_policy = ParallelPolicy()
        self.retriever = KnowledgeRetriever(
            config.repo_root, config.knowledge_dir, config.hub_dir,
        )
        self.packet_builder = PacketBuilder(config.runtime_dir)
        self.prompt_budget = PromptBudget()
        self.acceptance_checker = AcceptanceChecker()
        self.security_checker = SecurityChecker(config.repo_root)
        self.run_summarizer = RunSummarizer(config.runtime_dir)
        self.decision_store = DecisionStore(config.knowledge_dir / "memory")
        self.pre_task_hook = PreTaskHook(config.repo_root)
        self.post_task_hook = PostTaskHook()
        self.on_fail_hook = OnVerificationFailHook()

    def run_task(self, task: dict[str, Any], session_id: str) -> dict[str, Any]:
        """Full task lifecycle: classify → route → retrieve → packet → verify → memory."""

        # ── Step 0: Pre-task hook ────────────────────────────
        pre_result = self.pre_task_hook.run()

        # ── Step 1: Classify ────────────────────────────────
        classification = self.classifier.classify(task)

        # ── Step 2: Route ───────────────────────────────────
        routing = self.router.route(task, classification)
        parallelism = self.parallel_policy.evaluate(classification, routing)

        # ── Step 3: Retrieve ────────────────────────────────
        context_bundle = self.retriever.retrieve(task, classification, routing)

        # ── Step 4: Build packet ────────────────────────────
        task_packet_path = self.packet_builder.build(
            task=task,
            session_id=session_id,
            classification=classification,
            routing=routing,
            context_bundle=context_bundle,
        )

        # ── Step 5: Placeholder for agent execution ─────────
        # Actual LLM/agent execution happens externally.
        # The orchestrator produces the packet; Opus/Claude/etc. consumes it.
        agent_output = {
            "status": "pending_execution",
            "task_packet_path": str(task_packet_path),
            "assigned_role": routing["primary_role"],
            "mode": routing["mode"],
        }

        # ── Step 6: Store decision ──────────────────────────
        self.decision_store.store_task_decision(task["id"], {
            "action": "task_packet_generated",
            "classification": classification,
            "routing": routing,
            "parallelism": parallelism,
        })

        # ── Step 7: Summarize ───────────────────────────────
        summary = self.run_summarizer.summarize(
            task=task,
            session_id=session_id,
            agent_output=agent_output,
        )

        # ── Step 8: Post-task hook ──────────────────────────
        post_result = self.post_task_hook.run(
            task=task,
            session_id=session_id,
            agent_output=agent_output,
        )

        return {
            "pre_task": pre_result,
            "classification": classification,
            "routing": routing,
            "parallelism": parallelism,
            "task_packet_path": str(task_packet_path),
            "summary": summary,
            "post_task": post_result,
        }

    def run_verification(
        self, task: dict[str, Any], execution_result: dict[str, Any]
    ) -> dict[str, Any]:
        """Run verification checks on agent output."""
        checks: list[dict[str, Any]] = []

        # Acceptance criteria
        checks.append(self.acceptance_checker.check(task, execution_result))

        # Security check on changed files
        changed_files = execution_result.get("changed_files", [])
        if changed_files:
            checks.append(self.security_checker.check(changed_files))

        all_passed = all(c.get("result") == "passed" for c in checks)
        status = "passed" if all_passed else "failed"

        report = {
            "task_id": task["id"],
            "status": status,
            "checks": checks,
        }

        # Save report
        report_dir = self.config.runtime_dir / "state" / "verification_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{task['id']}.verification.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        return report
