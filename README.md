# DevSprint

DevSprint is a personal study & coding tracker. It gives a clear picture of how you spend focused time across coding projects, LeetCode prep, and learning/system design work—without streaks or competition.

## What it does (v1)
- `POST /api/v1/sessions` — create a session (`session_type`, `duration_minutes`, `topic`, `notes?`; `created_at` auto).
- `GET /api/v1/sessions` — list all sessions (JSON array).

## Tech stack (current)
- FastAPI + Pydantic
- Async SQLAlchemy + asyncpg (Supabase Postgres)

## Setup
1) Create/activate a virtualenv (example uses `devsprint.env`):
   ```bash
   python3 -m venv devsprint.env
   source devsprint.env/bin/activate
   ```
2) Install dependencies:
   ```bash
   pip install -e .[dev,test]
   ```
3) Configure environment:
   - Copy `.env.example` → `.env`
   - Set `DATABASE_URL` to your Supabase Postgres URI (include `sslmode=require`).

## Database table
The app auto-creates the `sessions` table on startup. If you want to create it manually, run:
```sql
create extension if not exists "uuid-ossp";
create table if not exists sessions (
  id uuid primary key default uuid_generate_v4(),
  session_type varchar(50) not null,
  duration_minutes int not null check (duration_minutes > 0),
  topic varchar(255) not null,
  notes text,
  created_at timestamptz not null default now()
);
```

## Run
```bash
uvicorn main:app --reload
```
The API will start at `http://localhost:8000` and create the table if it doesn’t exist.

## Notes
- Personal tool first; designed to be API-first so a lightweight dashboard can be added later.
