# kukufiti-api

Broiler farm management API for Kenyan smallholder farmers.

This project is being built as a modular FastAPI backend. The long-term goal is to help a farmer track broiler batches, farm finances, health observations, alerts, and authentication-protected workflows. The current repo is still early-stage, so this README is intentionally honest about what works today and what is planned next.

## Current Status

What exists and works today:

- FastAPI application shell in `app/main.py`
- `/health` endpoint that checks all four module database pools
- Docker Compose setup for PostgreSQL, migration runner, and the API
- PostgreSQL schema-per-module foundation through `scripts/init_db.sql`
- Separate database roles for `batches`, `finance`, `health`, `auth`, and `core`
- **Batches module: fully implemented** — router, service, repository, schemas, models
  - `POST /api/v1/batches/` — create batch
  - `GET /api/v1/batches/` — list with filtering and real pagination count
  - `GET /api/v1/batches/{id}` — get batch by ID
  - `PATCH /api/v1/batches/{id}/status` — transition status
  - `POST /api/v1/batches/{id}/close` — convenience close endpoint
  - `GET /api/v1/batches/{id}/summary` — computed summary (FCR, mortality rate)
- **Finance module: fully implemented** — isolated schema, M-Pesa STK push
  - `POST /api/v1/finance/transactions/income` — record manual income
  - `POST /api/v1/finance/transactions/expense` — record manual expense
  - `GET /api/v1/finance/batches/{batch_id}/transactions` — list transactions
  - `GET /api/v1/finance/batches/{batch_id}/pl` — profit & loss summary
  - `POST /api/v1/finance/mpesa/stk-push` — initiate Daraja payment
  - `POST /api/v1/finance/mpesa/callback` — Daraja webhook handler (unauthenticated)
- Migration runner with tracking: `scripts/run_migration.py` (idempotent, transactional)

Planned, not yet implemented:

- Health logs and alert rules
- OTP/JWT authentication
- Automated test suite
- Production deployment

## Tech Stack

- Python 3.12
- FastAPI
- asyncpg
- PostgreSQL 16
- Pydantic Settings
- Docker and Docker Compose
- pytest, planned for test coverage

## Project Shape

```text
kukufiti-api/
|-- app/
|   |-- main.py
|   |-- core/
|   |-- modules/
|   |   |-- auth/
|   |   |-- batches/
|   |   |-- finance/
|   |   `-- health/
|   `-- shared/
|-- migrations/
|   `-- batches/
|-- scripts/
|   |-- init_db.sql
|   `-- run_migration.py
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

## Prerequisites

Install these before running the project:

- Python 3.12
- Docker
- Docker Compose

Optional but useful:

- `curl`
- VS Code or another editor

## Environment Setup

From the `kukufiti-api/` directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

The local `.env.example` is configured for PostgreSQL running in Docker on host port `5432`.

If your shell has a non-boolean `DEBUG` variable exported, Pydantic may reject it. Fix that with:

```bash
unset DEBUG
```

or run commands with:

```bash
DEBUG=false <command>
```

## Run Locally

### Option 1: Run PostgreSQL in Docker and API from your venv

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the API:

```bash
python3.12 -m uvicorn app.main:app --reload
```

Open:

- API health check: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

### Option 2: Run everything with Docker Compose

```bash
docker compose up --build
```

Open:

- API health check: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

The API container listens on port `8000` inside Docker and is exposed as `8000` on your machine.

## Database Architecture

The database uses one PostgreSQL database with separate schemas per module:

- `batches`
- `finance`
- `health`
- `auth`
- `core`

Each module also has its own database role:

- `batches_app`
- `finance_app`
- `health_app`
- `auth_app`
- `core_app`

This keeps module boundaries visible at the database layer. For example, batches code should connect using `BATCHES_DB_URL`, while finance code should connect using `FINANCE_DB_URL`.

The schemas and roles are created by:

```text
scripts/init_db.sql
```

Docker runs that file automatically the first time the PostgreSQL volume is created.

## Migrations

Migrations are tracked in `public.schema_migrations`. Re-running a migration
that has already been applied is safe — it prints a skip message and exits 0.

Run migrations from the `kukufiti-api/` directory.

### Run all pending migrations (recommended)

```bash
python3.12 -m scripts.run_migration --all
```

This is also what `docker compose up` runs automatically via the `migrate` service.

### Run a single specific migration

```bash
python3.12 -m scripts.run_migration <module> <migration_id>
```

Examples:

```bash
python3.12 -m scripts.run_migration batches 001
python3.12 -m scripts.run_migration finance 001
```

Current migrations:

```text
migrations/batches/001_create_batches_tables.sql
migrations/finance/001_create_finance_tables.sql
```

## Available Endpoints

### `GET /health`

Checks that the API is alive and can connect to **all** module databases.

Example:

```bash
curl http://localhost:8000/health
```

Expected healthy response:

```json
{
  "status": "healthy",
  "databases": {
    "batches": "connected",
    "finance": "connected",
    "health": "connected",
    "auth": "connected"
  },
  "version": "0.1.0"
}
```

### Finance Commands (curl)

First, set your variables. Since the auth module is pending, use the dev token generator:

```bash
BATCH_ID="your-batch-uuid"
TOKEN="your-dev-jwt-token"
```

**1. List all transactions for a batch:**
```bash
curl -s -X GET "http://localhost:8000/api/v1/finance/batches/$BATCH_ID/transactions" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**2. Record an expense:**
```bash
curl -s -X POST http://localhost:8000/api/v1/finance/transactions/expense \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "'$BATCH_ID'",
    "category": "feed",
    "amount_kes": 15000.00,
    "transaction_date": "2026-06-09",
    "notes": "Starter feed purchase"
  }' | python3 -m json.tool
```

**3. View Profit & Loss (P&L):**
```bash
curl -s -X GET "http://localhost:8000/api/v1/finance/batches/$BATCH_ID/pl" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**4. Initiate M-Pesa STK Push:**
```bash
curl -s -X POST http://localhost:8000/api/v1/finance/mpesa/stk-push \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "'$BATCH_ID'",
    "phone_number": "254700000000",
    "amount_kes": 1,
    "category": "bird_sales",
    "description": "batch payment"
  }' | python3 -m json.tool
```

## Command Reference

Run these commands from the `kukufiti-api/` directory unless noted otherwise.

### Environment

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file:

```bash
cp .env.example .env
```

Clear a bad shell-level `DEBUG` value:

```bash
unset DEBUG
```

Run one command with a safe debug value:

```bash
DEBUG=false python3.12 -m scripts.run_migration batches 001
```

### Run the App

Start only PostgreSQL:

```bash
docker compose up -d postgres
```

Run the API locally from the virtual environment:

```bash
python3.12 -m uvicorn app.main:app --reload
```

Run the API locally with an explicit host and port:

```bash
python3.12 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Run PostgreSQL and the API with Docker Compose:

```bash
docker compose up --build
```

Run Docker Compose in the background:

```bash
docker compose up -d --build
```

Stop Docker services:

```bash
docker compose down
```

Stop Docker services and delete the local database volume:

```bash
docker compose down -v
```

### Health and Docs

Check the API when running locally with Uvicorn:

```bash
curl http://localhost:8000/health
```

Check the API when running through Docker Compose:

```bash
curl http://localhost:8000/health
```

Fail fast if the Docker Compose health check is unhealthy:

```bash
curl -fsS http://localhost:8000/health
```

Open these URLs in your browser:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

### Migrations

Run all pending migrations:

```bash
python3.12 -m scripts.run_migration --all
```

Run a single migration:

```bash
python3.12 -m scripts.run_migration <module> <migration_id>
```

Examples:

```bash
python3.12 -m scripts.run_migration batches 001
python3.12 -m scripts.run_migration finance 001
python3.12 -m scripts.run_migration health 001
python3.12 -m scripts.run_migration auth 001
```

### Database

Open `psql` as the local admin user:

```bash
docker exec -it kukufiti_postgres psql -U fred -d kukufiti_dev
```

Open `psql` as the batches module role:

```bash
docker exec -it kukufiti_postgres psql -U batches_app -d kukufiti_dev
```

Useful commands inside `psql`:

```sql
\dn
\dt *.*
\dt batches.*
\d batches.batches
SELECT * FROM batches.batches;
```

Check that app schemas exist:

```sql
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name IN ('batches', 'finance', 'health', 'auth', 'core');
```

Test schema isolation from a module role:

```sql
SELECT * FROM batches.batches;
SELECT * FROM finance.some_table;
```

The finance query should fail once finance tables exist, because `batches_app` should not own finance data.

### Tests

Run all tests:

```bash
.venv/bin/pytest
```

Run tests quietly:

```bash
.venv/bin/pytest -q
```

Future test commands once markers and coverage are configured:

```bash
pytest -m unit
pytest -m integration
pytest -m slice
pytest --cov=app --cov-report=term-missing
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

### VS Code Tasks

The repo includes VS Code tasks for common commands:

- `API: docker compose up`
- `API: docker compose down`
- `DB: docker compose up postgres`
- `API: health check`
- `Tests: pytest`
- `DB: alembic current`

Run them from the VS Code command palette with `Tasks: Run Task`.

## Troubleshooting

### `ModuleNotFoundError: No module named 'app.scripts'`

Use the top-level `scripts` module:

```bash
python3.12 -m scripts.run_migration batches 001
```

### `debug Input should be a valid boolean`

Your shell may have `DEBUG=release` or another non-boolean value exported. Run:

```bash
unset DEBUG
```

Then retry the command.

### `schema "batches" does not exist`

Make sure PostgreSQL was initialized with `scripts/init_db.sql`. The simplest fix during local development is usually to recreate the Docker volume:

```bash
docker compose down -v
docker compose up -d postgres
```

Then rerun the migration.

## Roadmap

The full build plan lives in:

```text
../docs/kukufiti api 20 Week Phased.md
```

Current next steps:

- Add tests for the batches and finance vertical slices (unit + integration)
- Implement health logs and alert rules
- Add OTP/JWT auth module
- Configure test coverage and production deployment
