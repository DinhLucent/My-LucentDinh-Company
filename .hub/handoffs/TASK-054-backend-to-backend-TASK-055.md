# Handoff: backend-agent -> backend-agent
## Task: TASK-055 - Master Data: TestCatalog + ReferenceRangeRule schema & seeder

## Completed (TASK-054)
- `packages/lis-core` is now a working FastAPI package with `GET /health`.
- PostgreSQL connectivity is verified live against the local PostgreSQL 16 instance on `127.0.0.1:5432`.
- Alembic is initialized with revision `20260401_01` and `upgrade head` succeeds.

## What TASK-055 must do
1. Add the first LIS Core domain tables through Alembic:
   - `TestCatalog`
   - `ReferenceRangeRule`
2. Implement the SQLAlchemy models under `src/lis_core/models/`.
3. Add a seed path for initial catalog/range data.
4. Expose read-only metadata endpoints for test catalog and reference ranges.
5. Add unit tests for seeding and meta endpoints.

## Context / Warnings
- `lis_core` database exists locally.
- Verification used the `postgres` superuser DSN from `LIS_CORE_DATABASE_URL`; no dedicated `lis_core_app` role exists yet.
- Keep using the shared contract package from TASK-053 for integration payloads; do not recreate parallel Pydantic contract models inside LIS Core.
