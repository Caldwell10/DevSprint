# DevSprint

DevSprint is a personal study & coding tracker. It gives a clear picture of how you spend focused time across coding projects, LeetCode prep, and learning/system design work—without streaks or competition.

## What it does
- Log focused sessions with type, category, topic, difficulty, notes, and optional tags/project name.
- Query sessions with filters and pagination.
- View basic analytics (time totals, breakdowns, daily trends).

## Tech stack (planned)
- FastAPI + Pydantic
- Async SQLAlchemy + asyncpg (Postgres via Supabase)
- Alembic for migrations (to be added)

## Status
- Scaffold in progress: package layout, virtual environment, notes structure.

## Running locally (planned)
- Create/activate venv `devsprint.env`, install deps, set `DATABASE_URL` (Supabase Postgres).
- Run `uvicorn main:app --reload` once app code is in place.

## Notes
- Personal tool first; designed to be API-first so a lightweight dashboard can be added later.
