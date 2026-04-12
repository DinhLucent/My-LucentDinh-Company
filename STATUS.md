# STATUS

Last updated: 2026-04-12

## Current State

The V2 orchestrator is operational for normal serial use.

What is working:

- `compile -> plan -> run` is the active workflow.
- The runtime loop is real: execute -> verify -> retry/complete.
- Task state is persisted through the execution state machine.
- Runtime metrics are written per run.
- Audit fixtures are now runnable and verified serially:
  - `tests/fixtures/audit/happy_path.yaml`
  - `tests/fixtures/audit/retry_scenario.yaml`
  - `tests/fixtures/audit/hard_fail.yaml`
- `.skills_pool` is optional and only included when requested:
  - `python run_orchestrator.py compile --include-pool`

## Recommended Usage

For normal work:

```bash
python run_orchestrator.py compile
python run_orchestrator.py plan path/to/task.yaml
python run_orchestrator.py run path/to/task.yaml
```

For system re-validation after control-plane changes, use the serial audit flow in [SYSTEM_AUDIT.md](SYSTEM_AUDIT.md).

## Audit Status

The current audit baseline is:

- happy path completes in one attempt
- retry scenario passes on retry
- hard-fail scenario exhausts retries and writes a handoff

This means the control plane is currently healthy for serial runs and review.

## Known Limitations

- The executor is command-driven. Tasks still need `metadata.execution` to do useful work.
- Concurrent runs can hit a dashboard snapshot race in `control_plane/hooks/pre_task.py`.
- `manifest.yaml` still mixes runtime concerns and skill catalog concerns.

## Backlog

- `P2`: Split `manifest.yaml` into `runtime_manifest` and `skill_catalog` after a separate design review.
- `P2`: Harden dashboard snapshot writes for concurrent runs with atomic write or file locking.
- `P3`: Clean up encoding in `_agent/workflows/report-writing.md`.

## Source of Truth

- [README.md](README.md)
- [CHEATSHEET.md](CHEATSHEET.md)
- [SYSTEM_AUDIT.md](SYSTEM_AUDIT.md)
- [templates/task.yaml](templates/task.yaml)
