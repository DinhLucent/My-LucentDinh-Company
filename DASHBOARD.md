# DASHBOARD

CEO quick view for SHIELD.

This file is for fast project status only.

Detailed process lives in `OPERATING_RULES.md`.

## Executive Snapshot

| Key | Value |
|---|---|
| Project | Agents-of-SHIELD |
| Operating model | Product + CTO first, workers execute assigned tasks |
| Current phase | Collaboration workflow + sandbox validation |
| System health | Stable for serial runtime, audit, prompt sandbox, and system-test |
| Last updated | 2026-04-14 |

## What Matters Now

- The control plane is running end-to-end with execute -> verify -> retry.
- The leadership-first workflow is restored and documented.
- Sandbox validation is passing, so the main risk is workflow drift, not runtime failure.

## CEO Check

Use the live dashboard for the real snapshot:

```bash
python run_orchestrator.py dashboard
```

Look at these fields first:

- `active_tasks`
- `blocked_tasks`
- `recent_done`
- `recent_handoffs`
- `recent_system_tests`

## How To Read The Live View

- `active_tasks`: work currently in progress
- `blocked_tasks`: tasks needing intervention or reassignment
- `recent_done`: latest completed or terminal tasks
- `recent_handoffs`: work that changed owner or needs another role
- `recent_system_tests`: latest proof that SHIELD still works as a system

Note:

- Audit fixtures may appear in recent history.
- For real project progress, prioritize business task ids and leadership artifacts over audit task ids.

## Current Focus

- Keep Product/CTO as the intake gate for raw requests.
- Keep worker sessions scoped to assigned tasks only.
- Keep reports, handoffs, and dashboard outputs aligned with runtime artifacts.
- Keep sandbox validation green after every meaningful control-plane change.

## At Risk

- Process drift if sessions skip Product/CTO and jump straight into worker execution.
- Stale status if docs are updated without re-running validation.
- Mixed signal in recent history when audit tasks and real project tasks are viewed together.

## Next Leadership Action

- Review live dashboard before opening more worker sessions.
- Approve only small, scoped tasks that preserve role boundaries.
- Re-run `audit`, `prompt-sandbox`, and `system-test` after orchestration or workflow changes.
