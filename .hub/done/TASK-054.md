# TASK-054: Setup LIS Core project (FastAPI + PostgreSQL + Alembic)
- Agent: backend-agent | Claimed: 2026-04-01T12:32:54.6609314+07:00 | Status: ✅ DONE

## Acceptance Criteria
- [x] FastAPI app starts and serves `GET /health`
- [x] Alembic init with first empty migration
- [x] PostgreSQL connection verified
- [x] Project structure: `routers/`, `models/`, `services/`, `schemas/`

## Work Log
- [2026-04-01T12:32:54.6609314+07:00] Read onboarding, task hub protocol, operating rules, dashboard, backlog, and CTO handoff for Sprint 6.
- [2026-04-01T12:32:54.6609314+07:00] Confirmed TASK-054 is the next claimable backend task with dependency TASK-053 completed.
- [2026-04-01T12:42:20.8611838+07:00] Scaffolded `packages/lis-core` with FastAPI app factory, `/health` router, settings, SQLAlchemy/PostgreSQL session wiring, Alembic config, initial empty revision, and package metadata.
- [2026-04-01T12:42:20.8611838+07:00] Installed missing backend dependencies (`sqlalchemy`, `alembic`, `psycopg`) and verified package smoke checks: `pytest` 4 passed, `alembic history`, and app import.
- [2026-04-01T13:20:42+07:00] Verified PostgreSQL 16 service was reachable on `127.0.0.1:5432`; initial attempts failed only because the `postgres` password was not yet provided.
- [2026-04-01T13:28:00+07:00] Verified admin login with the provided `postgres` password, confirmed `lis_core` database exists, and confirmed no dedicated `lis_core_app` role has been created yet.
- [2026-04-01T13:33:34.7059837+07:00] Verified live connectivity through the LIS Core code path: SQLAlchemy health check returned `ok`, `alembic upgrade head` succeeded against PostgreSQL, and `/health` returned `200` with `database.status = ok`.

## Completion Report
- Completed: 2026-04-01T13:33:34.7059837+07:00
- Files:
  - `packages/lis-core/pyproject.toml`
  - `packages/lis-core/requirements.txt`
  - `packages/lis-core/alembic.ini`
  - `packages/lis-core/alembic/env.py`
  - `packages/lis-core/alembic/script.py.mako`
  - `packages/lis-core/alembic/versions/20260401_01_initial_scaffold.py`
  - `packages/lis-core/src/lis_core/app.py`
  - `packages/lis-core/src/lis_core/settings.py`
  - `packages/lis-core/src/lis_core/db/base.py`
  - `packages/lis-core/src/lis_core/db/session.py`
  - `packages/lis-core/src/lis_core/models/base.py`
  - `packages/lis-core/src/lis_core/routers/health.py`
  - `packages/lis-core/src/lis_core/services/health.py`
  - `packages/lis-core/src/lis_core/schemas/health.py`
  - `packages/lis-core/tests/conftest.py`
  - `packages/lis-core/tests/test_database.py`
  - `packages/lis-core/tests/test_health.py`
- Summary: LIS Core now has a working FastAPI service scaffold, PostgreSQL-ready SQLAlchemy session wiring, Alembic migration setup, and a health endpoint that reports real database connectivity. The package is verified both with unit tests and against a live PostgreSQL 16 instance.
- Decisions: Kept the initial migration intentionally empty so TASK-055 can introduce domain tables cleanly. Used `LIS_CORE_DATABASE_URL` with `psycopg` v3 and exposed database health through the service-level `/health` endpoint.
- Issues: The environment currently uses the `postgres` superuser for verification; a dedicated least-privilege application role still needs to be created later if the team wants stricter runtime credentials.
- Verification:
  - `python -m pytest tests -q` → `4 passed`
  - `alembic -c alembic.ini history`
  - SQLAlchemy health check with `LIS_CORE_DATABASE_URL=postgresql+psycopg://...@127.0.0.1:5432/lis_core` → `ok`
  - `alembic -c alembic.ini upgrade head` against PostgreSQL 16 → success
  - `GET /health` via ASGI transport → `200` with `database.status = ok`
- Notes for next Agent: TASK-055 can build the first domain tables directly on top of this scaffold. If desired, create a dedicated `lis_core_app` role before moving toward production-like deployments.
