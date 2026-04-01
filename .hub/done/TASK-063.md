# TASK-063: QA: Negative Path Tests (Retry, Idempotency, Resolver, Restart)
- Agent: qa-lead-agent | Claimed: 2026-04-02T00:11:21.3220903+07:00 | Completed: 2026-04-02T00:17:15.6801942+07:00 | Status: DONE

## Acceptance Criteria
- Mirth retry: Gateway down->up, order syncs, ACK received
- Duplicate: same idempotency_key produces 1 inbox record
- Resolver: range_unresolved, unit_mismatch, unknown_test all handled correctly
- Restart: LIS restart preserves all order states and inbox data

## Work Log
- 2026-04-02T00:11:21.3220903+07:00 Started TASK-063 after TASK-062 completion and handoff review.
- 2026-04-02T00:11:21.3220903+07:00 Reused the TASK-062 local QA harness pattern, but switched to a file-backed SQLite database so restart persistence could be verified across process restarts.
- 2026-04-02T00:13:00+07:00 Added `output/playwright/task_063_harness.py` with QA-only endpoints for order listing, order queueing (`queued_for_gateway`), and result inspection.
- 2026-04-02T00:16:00+07:00 Executed `output/playwright/task_063_negative_check.py` to validate duplicate idempotency, all three resolver fallback branches, restart persistence, and a composite retry path.
- 2026-04-02T00:16:30+07:00 Ran gateway regression surrogate for transient retry: `pytest packages/lab-connector/tests/test_pipeline_e2e.py -k transient_dispatch_retry_succeeds -q -o cache_dir=.pytest-cache-local`; result `1 passed, 4 deselected`.
- 2026-04-02T00:17:15.6801942+07:00 Saved final summary and persisted-report artifact, then prepared sprint QA closure handoff.

## Completion Report
- Completed: 2026-04-02T00:17:15.6801942+07:00
- Files:
  - `output/playwright/task_063_harness.py`
  - `output/playwright/task_063_negative_check.py`
  - `output/playwright/task-063/task_063_summary.json`
  - `output/playwright/task-063/retry_pytest_output.txt`
  - `output/playwright/task-063/restart_persisted_report.pdf`
  - `output/playwright/task-063/task_063.sqlite3`
  - `output/pdf/task_063_restart_persisted_report.pdf`
- Summary:
  - Duplicate idempotency passed: the second inbound result with the same `idempotency_key` returned `idempotent=true` and no additional inbox record was created.
  - Resolver fallbacks passed on the live LIS Core surface: `range_unresolved` and `unit_mismatch` both stayed in `pending_manual_review`, while `unknown_test` entered `exception_queue`.
  - Restart persistence passed on the file-backed harness: `created`, `synced_to_gateway`, `result_received`, and `approved` order states all survived a full process restart, and the approved result PDF remained downloadable afterward.
  - Retry coverage passed with composite evidence rather than a single live end-to-end router flow: the order was explicitly moved to `queued_for_gateway`, the gateway transient retry regression test passed, and the ACK callback still transitioned the order to `synced_to_gateway`.
- Decisions:
  - Used a QA-only file-backed SQLite harness because the checked-out workspace still has no configured PostgreSQL DSN and restart persistence cannot be proven with the in-memory TASK-062 harness.
  - Added a QA-only queue transition endpoint because the current LIS Core app still has no public outbound order-sync router even though `OrderService.trigger_gateway_push()` exists.
  - Treated retry as composite evidence, not as a pure live E2E pass, because the checked-out Sprint 6 implementation does not expose a complete runtime route from order creation to outbound Mirth dispatch.
- Issues:
  - The Sprint 6 spec file referenced in backlog remains missing from the checked-out worktree, so QA continued to validate the live implementation and existing tests as the source of truth.
  - Retry/recover cannot be observed through one public LIS Core route today; validation had to combine queued order state, the gateway retry regression test, and ACK callback verification.
- Notes for next Agent:
  - Primary artifact summary: `output/playwright/task-063/task_063_summary.json`
  - Retry surrogate evidence: `output/playwright/task-063/retry_pytest_output.txt`
  - Persistence DB artifact: `output/playwright/task-063/task_063.sqlite3`
  - Root repo branch: `codex/task-063-negative-path-qa` (local only at completion time)
  - MyTeam branch: `codex/task-063-negative-path-qa` (local only at completion time)
  - Push/PR: not created during this QA execution
