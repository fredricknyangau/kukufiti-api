# kukufiti-api — 20-Week Phased Learning Roadmap

---

## Verifier Answers (Before the Roadmap)

**Q1:** Parallel tracks with sync points only. Track C topics (SQL Wks 9–10, FastAPI Wk 17, Auth Wk 20) are the theoretical reinforcement layer. kukufiti-api phases run independently and arrive at each sync point with working code that the Track C theory explains retrospectively. This is the correct order for a project-based learner — build first, name the concept second.

**Q2:** Confirmed. Modular monolith for kukufiti-api means: each module (`batches`, `finance`, `health`, `auth`) owns a PostgreSQL schema (`batches.*`, `finance.*`, `health.*`, `auth.*`). No module's SQL queries cross into another module's schema. Cross-module data needs are resolved through Python function calls between module service layers — never through SQL joins across schemas.

**Q3:** Confirmed with one addition. "Done" means: deployed to Render with a public URL, clean `/docs`, README with setup instructions, 80%+ test coverage on business logic — and at least one live demo flow that exercises all three modules end-to-end.

---

## Phase 0 — Weeks 1–2: Planning, Environment, Project Foundation

### Chain-of-Thought

**What Fredrick already knows:** Python fundamentals, OOP, Linux navigation, file system structure, Git basics, virtualenv.

**What this phase teaches:** Project scaffolding discipline, asyncpg pool setup, schema-per-module PostgreSQL design, Docker Compose for local dev, environment variable management with `.env`.

**Track C sync:** Week 8 (Git & GitHub mastery) — this phase produces the commit history structure that Week 8 will formalise.

**Vibe Coding workflow:** Use Claude to generate the Docker Compose and folder scaffold. Read every line before running. For asyncpg pool parameters (`min_size`, `max_size`, `command_timeout`), ask Claude to explain each one in one sentence before you copy it. Do not run any SQL until you can explain what it does.

**Go/No-Go:** `docker compose up` starts Postgres and the API without errors. `GET /health` returns `{"status": "healthy", "database": "connected"}`.

**Junior mistake:** Putting secrets in `main.py` or committing `.env` to Git. Prevention: create `.gitignore` with `.env` on Day 1, before writing a single line of application code.

---

### Phase Goal

Build the project skeleton that every subsequent phase plugs into. Nothing user-facing gets built here. What gets built is the foundation: folder structure, Docker Compose, asyncpg pool, environment config, health check, and the four PostgreSQL schemas with RBAC.

By end of Phase 0, `kukufiti-api` exists as a real project — not a tutorial clone, not a scaffold generator output. You made every decision consciously.

---

### Week 1 — Scaffold and Database Foundation

**Day 1–2: Folder structure and virtual environment**

```
~/dev/zealsync/backend/kukufiti-api/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   ├── shared/
│   │   ├── base_schema.py
│   │   └── types.py
│   └── modules/
│       ├── batches/
│       │   ├── __init__.py
│       │   ├── contracts.py
│       │   ├── router.py
│       │   ├── service.py
│       │   ├── repository.py
│       │   ├── schemas.py
│       │   ├── models.py
│       │   └── exceptions.py
│       ├── finance/
│       │   └── (same structure)
│       ├── health/
│       │   └── (same structure)
│       └── auth/
│           └── (same structure)
├── migrations/
│   ├── batches/
│   ├── finance/
│   ├── health/
│   └── auth/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── slices/
├── scripts/
│   └── init_db.sql
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .env               ← gitignored
├── .gitignore
└── README.md
```

```bash
# Terminal — run in ~/dev/zealsync/backend/
mkdir kukufiti-api && cd kukufiti-api
pyenv local 3.12.2
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn asyncpg pydantic-settings python-dotenv
pip freeze > requirements.txt
git init
git add .gitignore requirements.txt
git commit -m "chore: initialise project with virtualenv and requirements"
```

**Day 3–4: Docker Compose and PostgreSQL**

```yaml
# docker-compose.yml
version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    container_name: kukufiti_postgres
    environment:
      POSTGRES_DB: kukufiti_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres_local
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init_db.sql:/docker-entrypoint-initdb.d/01_init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d kukufiti_dev"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kukufiti_api
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

**Day 5: Schema isolation SQL**

```sql
-- scripts/init_db.sql
-- Run once on first container start

-- Create module schemas
CREATE SCHEMA IF NOT EXISTS batches;
CREATE SCHEMA IF NOT EXISTS finance;
CREATE SCHEMA IF NOT EXISTS health;
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS core;

-- Create module roles
CREATE ROLE batches_app WITH LOGIN PASSWORD 'batches_dev';
CREATE ROLE finance_app WITH LOGIN PASSWORD 'finance_dev';
CREATE ROLE health_app WITH LOGIN PASSWORD 'health_dev';
CREATE ROLE auth_app WITH LOGIN PASSWORD 'auth_dev';
CREATE ROLE core_app WITH LOGIN PASSWORD 'core_dev';

-- Grant schema ownership
GRANT USAGE ON SCHEMA batches TO batches_app;
GRANT ALL ON SCHEMA batches TO batches_app;
GRANT USAGE ON SCHEMA finance TO finance_app;
GRANT ALL ON SCHEMA finance TO finance_app;
GRANT USAGE ON SCHEMA health TO health_app;
GRANT ALL ON SCHEMA health TO health_app;
GRANT USAGE ON SCHEMA auth TO auth_app;
GRANT ALL ON SCHEMA auth TO auth_app;
GRANT USAGE ON SCHEMA core TO core_app;
GRANT ALL ON SCHEMA core TO core_app;

-- All module roles can write to core.outbox
GRANT USAGE ON SCHEMA core TO batches_app, finance_app, health_app, auth_app;

-- Default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA batches
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO batches_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA finance
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO finance_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA health
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO health_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO auth_app;
```

---

### Week 2 — Core Infrastructure

**Day 1–2: Config and database pool**

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    database_url: str
    batches_db_url: str
    finance_db_url: str
    health_db_url: str
    auth_db_url: str

    # Application
    app_name: str = "kukufiti-api"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "info"

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
```

```python
# app/core/database.py
import asyncpg
from contextlib import asynccontextmanager
from fastapi import Request

async def create_pool(dsn: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=2,          # minimum connections kept alive at idle
        max_size=10,         # maximum connections in pool
        statement_cache_size=0,  # required when using PgBouncer later
        command_timeout=30,  # kill any query running longer than 30 seconds
    )

@asynccontextmanager
async def get_connection(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        yield conn

# FastAPI dependency
async def get_db_connection(request: Request) -> asyncpg.Connection:
    async with request.app.state.batches_pool.acquire() as conn:
        yield conn
```

**Day 3: Lifespan and health check**

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import create_pool
from app.core.logging import configure_logging
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    logger.info("kukufiti-api starting up")

    # Create one pool per module — each uses its own DB role
    app.state.batches_pool = await create_pool(settings.batches_db_url)
    app.state.finance_pool = await create_pool(settings.finance_db_url)
    app.state.health_pool = await create_pool(settings.health_db_url)
    app.state.auth_pool = await create_pool(settings.auth_db_url)

    logger.info("All connection pools ready")
    yield

    # Graceful shutdown
    await app.state.batches_pool.close()
    await app.state.finance_pool.close()
    await app.state.health_pool.close()
    await app.state.auth_pool.close()
    logger.info("All connection pools closed")

app = FastAPI(
    title="kukufiti-api",
    description="Broiler farm management API for Kenyan smallholder farmers",
    version=settings.app_version,
    lifespan=lifespan,
)

@app.get("/health", tags=["health"])
async def health_check():
    try:
        async with app.state.batches_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {"status": "healthy", "database": "connected", "version": settings.app_version}
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)},
        )
```

**Day 4: .env setup and structured logging**

```bash
# .env.example — commit this
DATABASE_URL=postgresql://postgres:postgres_local@localhost:5432/kukufiti_dev
BATCHES_DB_URL=postgresql://batches_app:batches_dev@localhost:5432/kukufiti_dev
FINANCE_DB_URL=postgresql://finance_app:finance_dev@localhost:5432/kukufiti_dev
HEALTH_DB_URL=postgresql://health_app:health_dev@localhost:5432/kukufiti_dev
AUTH_DB_URL=postgresql://auth_app:auth_dev@localhost:5432/kukufiti_dev
SECRET_KEY=change_this_to_a_real_secret_in_production
DEBUG=true
LOG_LEVEL=info
```

**Day 5: Git history cleanup and Phase 0 commit**

```bash
git add .
git commit -m "feat(core): asyncpg pool, health check, structured logging"
git commit -m "feat(infra): docker-compose with postgres, schema-per-module RBAC"
git commit -m "chore: env config with pydantic-settings, .env.example"
```

---

### Phase 0 Deliverable

`GET /health` returns `200 {"status": "healthy", "database": "connected"}`. Docker Compose starts cleanly. Four PostgreSQL schemas exist with isolated roles. `.env` is in `.gitignore`. `.env.example` is committed.

### Go/No-Go Checkpoint

```bash
docker compose up -d
curl http://localhost:8000/health
# Must return: {"status":"healthy","database":"connected"}

# Verify RBAC — this must FAIL with permission denied
docker exec -it kukufiti_postgres psql -U batches_app -d kukufiti_dev \
  -c "SELECT * FROM finance.transactions LIMIT 1;"
# Expected: ERROR: permission denied for schema finance
```

Both must pass. The RBAC failure is a success condition.

---

## Phase 1 — Weeks 3–6: Module 1 — Batches

### Chain-of-Thought

**What Fredrick already knows:** Folder structure is scaffolded. asyncpg pool works. He has written Python classes and functions. He understands OOP.

**What this phase teaches:** Raw SQL via asyncpg, Pydantic v2 schemas, FastAPI router and dependency injection, UUID primary keys, soft deletes, FCR calculation as domain logic, repository pattern, status machine transitions.

**Track C sync:** Week 8 Git mastery — this phase produces 20+ commits that Week 8's branching strategies will organise retrospectively. Week 9–10 SQL — the raw SQL written here is the practice that makes SQL week click.

**Vibe Coding workflow:** Use Claude to generate the `CREATE TABLE` SQL. Before running it, draw the table on paper — column names, types, constraints. Then compare your drawing to Claude's output. Every discrepancy is a learning moment. Use GitHub Copilot for repetitive asyncpg `fetchrow` / `fetch` / `execute` patterns — but type the first one manually before accepting autocomplete for the rest.

**Go/No-Go:** All six batch endpoints return correct status codes and data. FCR calculation returns the correct decimal. `POST /batches` with missing required fields returns 422. Status transition `active → closed` works. `closed → active` returns 400.

**Junior mistake:** Putting business logic (FCR calculation, status validation) inside the router function instead of the service layer. Prevention: the router function body must be readable in under 10 lines. If it is longer, move logic to the service.

---

### Phase Goal

Build the complete Batches module: database schema, all six endpoints, FCR calculation, mortality rate, batch status machine. By the end, you can create a broiler batch, log its lifecycle, close it, and retrieve its performance summary — all through the API.

---

### Week 3 — Batches Schema and Repository

**Day 1–2: Database migration**

```sql
-- migrations/batches/001_create_batches_tables.sql

CREATE TABLE IF NOT EXISTS batches.batches (
    id               UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_name       TEXT         NOT NULL,
    breed            TEXT         NOT NULL,
    quantity         INTEGER      NOT NULL CHECK (quantity > 0),
    start_date       DATE         NOT NULL,
    end_date         DATE,
    status           TEXT         NOT NULL DEFAULT 'active'
                                  CHECK (status IN ('active', 'closed', 'archived')),

    -- Performance metrics (updated via health logs)
    total_feed_kg    NUMERIC(10,2) NOT NULL DEFAULT 0,
    mortality_count  INTEGER       NOT NULL DEFAULT 0,

    -- Soft delete
    deleted_at       TIMESTAMPTZ,

    created_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_batches_status
    ON batches.batches(status)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_batches_start_date
    ON batches.batches(start_date DESC)
    WHERE deleted_at IS NULL;
```

```python
# app/scripts/run_migration.py
# Run manually: python -m app.scripts.run_migration batches 001
import asyncio
import asyncpg
import sys
from pathlib import Path
from app.core.config import settings

DB_URLS = {
    "batches": settings.batches_db_url,
    "finance": settings.finance_db_url,
    "health": settings.health_db_url,
    "auth": settings.auth_db_url,
}

async def run_migration(module: str, migration_id: str):
    path = Path(f"migrations/{module}/{migration_id}_*.sql")
    files = list(Path("migrations").glob(f"{module}/{migration_id}*.sql"))

    if not files:
        print(f"No migration file found for {module}/{migration_id}")
        sys.exit(1)

    sql = files[0].read_text()
    conn = await asyncpg.connect(DB_URLS[module])
    try:
        await conn.execute(sql)
        print(f"Migration {files[0].name} applied successfully")
    finally:
        await conn.close()

if __name__ == "__main__":
    module, migration_id = sys.argv[1], sys.argv[2]
    asyncio.run(run_migration(module, migration_id))
```

**Day 3–5: Repository layer**

```python
# app/modules/batches/repository.py
import asyncpg
from uuid import UUID
from decimal import Decimal
from typing import Optional
from .models import Batch, BatchSummary

class BatchRepository:
    def __init__(self, connection: asyncpg.Connection):
        self._conn = connection

    async def create(
        self,
        batch_name: str,
        breed: str,
        quantity: int,
        start_date: str,
    ) -> Batch:
        row = await self._conn.fetchrow(
            """
            INSERT INTO batches.batches
                (batch_name, breed, quantity, start_date)
            VALUES ($1, $2, $3, $4)
            RETURNING id, batch_name, breed, quantity, start_date,
                      end_date, status, total_feed_kg, mortality_count,
                      created_at, updated_at
            """,
            batch_name, breed, quantity, start_date,
        )
        return Batch.from_row(row)

    async def find_by_id(self, batch_id: UUID) -> Optional[Batch]:
        row = await self._conn.fetchrow(
            """
            SELECT id, batch_name, breed, quantity, start_date,
                   end_date, status, total_feed_kg, mortality_count,
                   created_at, updated_at
            FROM batches.batches
            WHERE id = $1 AND deleted_at IS NULL
            """,
            batch_id,
        )
        return Batch.from_row(row) if row else None

    async def list_all(
        self,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Batch]:
        rows = await self._conn.fetch(
            """
            SELECT id, batch_name, breed, quantity, start_date,
                   end_date, status, total_feed_kg, mortality_count,
                   created_at, updated_at
            FROM batches.batches
            WHERE deleted_at IS NULL
              AND ($1::text IS NULL OR status = $1)
            ORDER BY start_date DESC
            LIMIT $2 OFFSET $3
            """,
            status, limit, offset,
        )
        return [Batch.from_row(row) for row in rows]

    async def update_status(
        self,
        batch_id: UUID,
        new_status: str,
        end_date: Optional[str] = None,
    ) -> Optional[Batch]:
        row = await self._conn.fetchrow(
            """
            UPDATE batches.batches
            SET status = $2,
                end_date = COALESCE($3, end_date),
                updated_at = NOW()
            WHERE id = $1 AND deleted_at IS NULL
            RETURNING id, batch_name, breed, quantity, start_date,
                      end_date, status, total_feed_kg, mortality_count,
                      created_at, updated_at
            """,
            batch_id, new_status, end_date,
        )
        return Batch.from_row(row) if row else None

    async def update_performance(
        self,
        batch_id: UUID,
        additional_feed_kg: Decimal,
        additional_mortality: int,
    ) -> None:
        await self._conn.execute(
            """
            UPDATE batches.batches
            SET total_feed_kg    = total_feed_kg + $2,
                mortality_count  = mortality_count + $3,
                updated_at       = NOW()
            WHERE id = $1 AND deleted_at IS NULL
            """,
            batch_id, additional_feed_kg, additional_mortality,
        )

    async def get_summary(self, batch_id: UUID) -> Optional[BatchSummary]:
        row = await self._conn.fetchrow(
            """
            SELECT
                b.id,
                b.batch_name,
                b.breed,
                b.quantity                                    AS initial_quantity,
                b.mortality_count,
                b.quantity - b.mortality_count                AS surviving_birds,
                b.total_feed_kg,
                b.start_date,
                b.end_date,
                b.status,
                CASE
                    WHEN b.quantity - b.mortality_count > 0
                    THEN ROUND(
                        b.total_feed_kg /
                        NULLIF((b.quantity - b.mortality_count)::numeric, 0),
                        3
                    )
                    ELSE NULL
                END                                           AS fcr,
                ROUND(
                    b.mortality_count * 100.0 /
                    NULLIF(b.quantity, 0),
                    2
                )                                             AS mortality_rate_pct,
                EXTRACT(DAY FROM NOW() - b.start_date::timestamptz) AS age_days
            FROM batches.batches b
            WHERE b.id = $1 AND b.deleted_at IS NULL
            """,
            batch_id,
        )
        return BatchSummary.from_row(row) if row else None
```

---

### Week 4 — Service Layer and Business Rules

```python
# app/modules/batches/models.py
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
import asyncpg

@dataclass
class Batch:
    id: UUID
    batch_name: str
    breed: str
    quantity: int
    start_date: date
    end_date: Optional[date]
    status: str
    total_feed_kg: Decimal
    mortality_count: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: asyncpg.Record) -> "Batch":
        return cls(
            id=row["id"],
            batch_name=row["batch_name"],
            breed=row["breed"],
            quantity=row["quantity"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            status=row["status"],
            total_feed_kg=row["total_feed_kg"],
            mortality_count=row["mortality_count"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

@dataclass
class BatchSummary:
    id: UUID
    batch_name: str
    breed: str
    initial_quantity: int
    mortality_count: int
    surviving_birds: int
    total_feed_kg: Decimal
    start_date: date
    end_date: Optional[date]
    status: str
    fcr: Optional[Decimal]              # Feed Conversion Ratio
    mortality_rate_pct: Optional[Decimal]
    age_days: int

    @classmethod
    def from_row(cls, row: asyncpg.Record) -> "BatchSummary":
        return cls(**{k: row[k] for k in row.keys()})
```

```python
# app/modules/batches/service.py
from uuid import UUID
from decimal import Decimal
from typing import Optional
from .repository import BatchRepository
from .models import Batch, BatchSummary
from .exceptions import (
    BatchNotFoundError,
    InvalidStatusTransitionError,
    BatchAlreadyClosedError,
)

# Valid status transitions — the state machine
VALID_TRANSITIONS = {
    "active": ["closed"],
    "closed": ["archived"],
    "archived": [],       # terminal state
}

class BatchService:
    def __init__(self, repository: BatchRepository):
        self._repo = repository

    async def create_batch(
        self,
        batch_name: str,
        breed: str,
        quantity: int,
        start_date: str,
    ) -> Batch:
        return await self._repo.create(
            batch_name=batch_name,
            breed=breed,
            quantity=quantity,
            start_date=start_date,
        )

    async def get_batch(self, batch_id: UUID) -> Batch:
        batch = await self._repo.find_by_id(batch_id)
        if batch is None:
            raise BatchNotFoundError(batch_id)
        return batch

    async def list_batches(
        self,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Batch]:
        return await self._repo.list_all(status=status, limit=limit, offset=offset)

    async def transition_status(
        self,
        batch_id: UUID,
        new_status: str,
        end_date: Optional[str] = None,
    ) -> Batch:
        batch = await self._repo.find_by_id(batch_id)
        if batch is None:
            raise BatchNotFoundError(batch_id)

        allowed = VALID_TRANSITIONS.get(batch.status, [])
        if new_status not in allowed:
            raise InvalidStatusTransitionError(
                current=batch.status,
                attempted=new_status,
                allowed=allowed,
            )

        # Closing a batch requires an end date
        if new_status == "closed" and not end_date:
            from datetime import date
            end_date = str(date.today())

        updated = await self._repo.update_status(batch_id, new_status, end_date)
        return updated

    async def close_batch(self, batch_id: UUID, end_date: Optional[str] = None) -> Batch:
        return await self.transition_status(batch_id, "closed", end_date)

    async def get_batch_summary(self, batch_id: UUID) -> BatchSummary:
        summary = await self._repo.get_summary(batch_id)
        if summary is None:
            raise BatchNotFoundError(batch_id)
        return summary
```

---

### Week 5 — Pydantic Schemas and Router

```python
# app/modules/batches/schemas.py
from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class CreateBatchRequest(AppBaseModel):
    batch_name: str
    breed: str
    quantity: int
    start_date: date

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    @field_validator("batch_name")
    @classmethod
    def batch_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Batch name cannot be empty")
        return v.strip()

class UpdateBatchStatusRequest(AppBaseModel):
    status: str
    end_date: Optional[date] = None

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        allowed = {"closed", "archived"}
        if v not in allowed:
            raise ValueError(f"Status must be one of: {allowed}")
        return v

class BatchResponse(AppBaseModel):
    id: UUID
    batch_name: str
    breed: str
    quantity: int
    start_date: date
    end_date: Optional[date]
    status: str
    total_feed_kg: Decimal
    mortality_count: int
    created_at: datetime
    updated_at: datetime

class BatchSummaryResponse(AppBaseModel):
    id: UUID
    batch_name: str
    breed: str
    initial_quantity: int
    mortality_count: int
    surviving_birds: int
    total_feed_kg: Decimal
    start_date: date
    end_date: Optional[date]
    status: str
    fcr: Optional[Decimal]
    mortality_rate_pct: Optional[Decimal]
    age_days: int

class BatchListResponse(AppBaseModel):
    batches: list[BatchResponse]
    total: int
    limit: int
    offset: int
```

```python
# app/modules/batches/router.py
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from .schemas import (
    CreateBatchRequest,
    UpdateBatchStatusRequest,
    BatchResponse,
    BatchSummaryResponse,
    BatchListResponse,
)
from .service import BatchService
from .dependencies import get_batch_service
from .exceptions import BatchNotFoundError, InvalidStatusTransitionError

router = APIRouter(prefix="/batches", tags=["batches"])

@router.post("/", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
async def create_batch(
    payload: CreateBatchRequest,
    service: BatchService = Depends(get_batch_service),
):
    batch = await service.create_batch(
        batch_name=payload.batch_name,
        breed=payload.breed,
        quantity=payload.quantity,
        start_date=str(payload.start_date),
    )
    return BatchResponse.model_validate(batch.__dict__)

@router.get("/", response_model=BatchListResponse)
async def list_batches(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: BatchService = Depends(get_batch_service),
):
    batches = await service.list_batches(status=status, limit=limit, offset=offset)
    return BatchListResponse(
        batches=[BatchResponse.model_validate(b.__dict__) for b in batches],
        total=len(batches),
        limit=limit,
        offset=offset,
    )

@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(
    batch_id: UUID,
    service: BatchService = Depends(get_batch_service),
):
    batch = await service.get_batch(batch_id)
    return BatchResponse.model_validate(batch.__dict__)

@router.patch("/{batch_id}/status", response_model=BatchResponse)
async def update_batch_status(
    batch_id: UUID,
    payload: UpdateBatchStatusRequest,
    service: BatchService = Depends(get_batch_service),
):
    batch = await service.transition_status(
        batch_id=batch_id,
        new_status=payload.status,
        end_date=str(payload.end_date) if payload.end_date else None,
    )
    return BatchResponse.model_validate(batch.__dict__)

@router.post("/{batch_id}/close", response_model=BatchResponse)
async def close_batch(
    batch_id: UUID,
    service: BatchService = Depends(get_batch_service),
):
    batch = await service.close_batch(batch_id)
    return BatchResponse.model_validate(batch.__dict__)

@router.get("/{batch_id}/summary", response_model=BatchSummaryResponse)
async def get_batch_summary(
    batch_id: UUID,
    service: BatchService = Depends(get_batch_service),
):
    summary = await service.get_batch_summary(batch_id)
    return BatchSummaryResponse.model_validate(summary.__dict__)
```

```python
# app/modules/batches/dependencies.py
from fastapi import Depends, Request
import asyncpg
from .repository import BatchRepository
from .service import BatchService

async def get_batches_connection(request: Request) -> asyncpg.Connection:
    async with request.app.state.batches_pool.acquire() as conn:
        yield conn

async def get_batch_service(
    conn: asyncpg.Connection = Depends(get_batches_connection),
) -> BatchService:
    repo = BatchRepository(conn)
    return BatchService(repository=repo)
```

---

### Week 6 — Exceptions, Router Registration, Manual Testing

```python
# app/modules/batches/exceptions.py
from uuid import UUID
from fastapi import HTTPException, status

class BatchNotFoundError(HTTPException):
    def __init__(self, batch_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch {batch_id} not found",
        )

class InvalidStatusTransitionError(HTTPException):
    def __init__(self, current: str, attempted: str, allowed: list[str]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_status_transition",
                "message": f"Cannot transition from '{current}' to '{attempted}'",
                "allowed_transitions": allowed,
            }
        )

class BatchAlreadyClosedError(HTTPException):
    def __init__(self, batch_id: UUID):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Batch {batch_id} is already closed",
        )
```

```python
# app/main.py — register batches router
from app.modules.batches.router import router as batches_router
app.include_router(batches_router, prefix="/api/v1")
```

Manual test sequence using curl or the Swagger UI at `/docs`:

```bash
# 1. Create a batch
curl -X POST http://localhost:8000/api/v1/batches/ \
  -H "Content-Type: application/json" \
  -d '{"batch_name":"Batch A","breed":"Ross 308","quantity":500,"start_date":"2026-05-01"}'

# 2. List batches
curl http://localhost:8000/api/v1/batches/

# 3. Get summary (FCR and mortality rate)
curl http://localhost:8000/api/v1/batches/{id}/summary

# 4. Close batch
curl -X POST http://localhost:8000/api/v1/batches/{id}/close

# 5. Attempt invalid transition (should return 400)
curl -X PATCH http://localhost:8000/api/v1/batches/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"active"}'
```

---

### Phase 1 Deliverable

Six working endpoints: `POST /batches/`, `GET /batches/`, `GET /batches/{id}`, `PATCH /batches/{id}/status`, `POST /batches/{id}/close`, `GET /batches/{id}/summary`. FCR and mortality rate calculate correctly in SQL. Invalid status transitions return 400.

### Go/No-Go Checkpoint

```bash
# All must pass:
curl -X POST .../batches/ -d '{"batch_name":"","breed":"Ross","quantity":500,"start_date":"2026-01-01"}'
# → 422 (empty batch_name)

curl -X POST .../batches/ -d '{"batch_name":"Test","breed":"Ross","quantity":-1,"start_date":"2026-01-01"}'
# → 422 (negative quantity)

# Create → close → try to close again
# → 400 (closed → active not allowed)

# Summary endpoint must return fcr and mortality_rate_pct as numbers, not null
# (requires updating total_feed_kg > 0 first)
```

### Phase 1 Commit Structure

```
feat(batches): create batches table migration
feat(batches): repository layer — create, find, list, update
feat(batches): service layer — FCR calculation, status machine
feat(batches): pydantic v2 schemas — request and response models
feat(batches): router — 6 endpoints registered at /api/v1/batches
feat(batches): exceptions — 404, 400, 409 with structured detail
fix(batches): summary query returns correct FCR when no mortality
```

---

## Phase 2 — Weeks 7–10: Module 2 — Finance + M-Pesa

### Chain-of-Thought

**What Fredrick already knows:** asyncpg patterns from Phase 1, repository/service/router structure, Pydantic v2 validators, FastAPI dependency injection.

**What this phase teaches:** Cross-module soft references (batch_id in finance without a cross-schema FK), financial arithmetic in raw SQL, M-Pesa Daraja STK push flow, webhook callback handling, async HTTP client (httpx), environment-based API key management.

**Track C sync:** Week 9–10 SQL — the financial aggregation queries (`SUM`, `GROUP BY`, `FILTER`) in this phase are exactly what SQL weeks cover. You write the SQL here, Track C explains why it works.

**Vibe Coding workflow:** For the M-Pesa Daraja integration, ask Claude to generate the STK push request structure first. Do not run it. Go to the Daraja documentation (developer.safaricom.co.ke) and verify every field matches. Differences between Claude's output and the docs are your learning points. For the P&L query, write it yourself first, then ask Claude to review it — not the other way around.

**Go/No-Go:** `POST /finance/transactions/expense` and `POST /finance/transactions/income` record correctly. `GET /finance/batches/{id}/pl` returns correct KES profit/loss. M-Pesa STK push endpoint returns a `CheckoutRequestID`. Callback handler updates transaction status.

**Junior mistake:** Storing M-Pesa credentials in the code or `.env` without documenting them in `.env.example` with placeholder values. A new developer cannot run the project. Prevention: every secret in `.env` must have a corresponding placeholder entry in `.env.example`, committed to Git.

---

### Phase Goal

Build the Finance module: income/expense tracking per batch in KES, profit/loss calculation, M-Pesa Daraja STK push initiation, and callback handling. By end of Phase 2, a farmer can record a sale, initiate M-Pesa payment collection, and see their batch P&L.

---

### Week 7 — Finance Schema and Repository

```sql
-- migrations/finance/001_create_finance_tables.sql

CREATE TABLE IF NOT EXISTS finance.transactions (
    id                UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id          UUID         NOT NULL,    -- soft reference to batches.batches
    transaction_type  TEXT         NOT NULL CHECK (transaction_type IN ('income', 'expense')),
    category          TEXT         NOT NULL,
    amount_kes        NUMERIC(12,2) NOT NULL CHECK (amount_kes > 0),
    mpesa_reference   TEXT,
    transaction_date  DATE         NOT NULL DEFAULT CURRENT_DATE,
    notes             TEXT,
    status            TEXT         NOT NULL DEFAULT 'confirmed'
                                   CHECK (status IN ('pending', 'confirmed', 'failed')),
    created_at        TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS finance.mpesa_requests (
    id                    UUID   PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id        UUID   REFERENCES finance.transactions(id),
    checkout_request_id   TEXT   NOT NULL UNIQUE,
    merchant_request_id   TEXT   NOT NULL,
    phone_number          TEXT   NOT NULL,
    amount_kes            NUMERIC(12,2) NOT NULL,
    status                TEXT   NOT NULL DEFAULT 'pending'
                                 CHECK (status IN ('pending', 'completed', 'failed', 'cancelled')),
    mpesa_receipt_number  TEXT,
    result_code           INTEGER,
    result_desc           TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at          TIMESTAMPTZ
);

CREATE INDEX idx_transactions_batch_id
    ON finance.transactions(batch_id);

CREATE INDEX idx_transactions_batch_type
    ON finance.transactions(batch_id, transaction_type);

CREATE INDEX idx_mpesa_checkout_id
    ON finance.mpesa_requests(checkout_request_id);
```

---

### Week 8 — M-Pesa Daraja Integration

```python
# app/modules/finance/mpesa_client.py
import httpx
import base64
import hashlib
from datetime import datetime
from decimal import Decimal
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class MpesaClient:
    """
    Safaricom Daraja API client.
    Handles OAuth token management and STK Push initiation.

    Free tier: Daraja sandbox is completely free — no payment required.
    Production requires a registered Safaricom business shortcode.
    """

    SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"
    PRODUCTION_BASE_URL = "https://api.safaricom.co.ke"

    def __init__(self):
        self._consumer_key = settings.mpesa_consumer_key
        self._consumer_secret = settings.mpesa_consumer_secret
        self._shortcode = settings.mpesa_shortcode
        self._passkey = settings.mpesa_passkey
        self._callback_url = settings.mpesa_callback_url
        self._base_url = (
            self.PRODUCTION_BASE_URL
            if settings.mpesa_environment == "production"
            else self.SANDBOX_BASE_URL
        )
        self._access_token: str | None = None

    def _generate_password(self) -> tuple[str, str]:
        """Generate Daraja API password and timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        raw = f"{self._shortcode}{self._passkey}{timestamp}"
        password = base64.b64encode(raw.encode()).decode()
        return password, timestamp

    async def _get_access_token(self) -> str:
        credentials = base64.b64encode(
            f"{self._consumer_key}:{self._consumer_secret}".encode()
        ).decode()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers={"Authorization": f"Basic {credentials}"},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def initiate_stk_push(
        self,
        phone_number: str,
        amount: Decimal,
        account_reference: str,
        transaction_desc: str,
    ) -> dict:
        """
        Initiate Lipa na M-Pesa Online (STK Push).
        Returns CheckoutRequestID used to track payment status.
        """
        token = await self._get_access_token()
        password, timestamp = self._generate_password()

        # Normalize phone: 0712345678 → 254712345678
        phone = phone_number.strip()
        if phone.startswith("0"):
            phone = f"254{phone[1:]}"
        elif phone.startswith("+"):
            phone = phone[1:]

        payload = {
            "BusinessShortCode": self._shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),                    # M-Pesa requires integer
            "PartyA": phone,
            "PartyB": self._shortcode,
            "PhoneNumber": phone,
            "CallBackURL": self._callback_url,
            "AccountReference": account_reference[:12],  # max 12 chars
            "TransactionDesc": transaction_desc[:13],    # max 13 chars
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=15.0,
            )
            response.raise_for_status()
            return response.json()
```

---

### Week 9 — P&L Queries and Service Layer

```python
# app/modules/finance/repository.py
import asyncpg
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from datetime import date

class FinanceRepository:
    def __init__(self, connection: asyncpg.Connection):
        self._conn = connection

    async def record_transaction(
        self,
        batch_id: UUID,
        transaction_type: str,
        category: str,
        amount_kes: Decimal,
        transaction_date: date,
        mpesa_reference: Optional[str] = None,
        notes: Optional[str] = None,
        status: str = "confirmed",
    ) -> dict:
        row = await self._conn.fetchrow(
            """
            INSERT INTO finance.transactions
                (batch_id, transaction_type, category, amount_kes,
                 mpesa_reference, transaction_date, notes, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id, batch_id, transaction_type, category, amount_kes,
                      mpesa_reference, transaction_date, notes, status, created_at
            """,
            batch_id, transaction_type, category, amount_kes,
            mpesa_reference, transaction_date, notes, status,
        )
        return dict(row)

    async def get_batch_pl(self, batch_id: UUID) -> dict:
        row = await self._conn.fetchrow(
            """
            SELECT
                batch_id,
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'income'
                    AND status = 'confirmed'
                ), 0)                                          AS total_income_kes,
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'expense'
                    AND status = 'confirmed'
                ), 0)                                          AS total_expense_kes,
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'income'
                    AND status = 'confirmed'
                ), 0) -
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'expense'
                    AND status = 'confirmed'
                ), 0)                                          AS profit_loss_kes,
                COUNT(*) FILTER (WHERE transaction_type = 'income')  AS income_count,
                COUNT(*) FILTER (WHERE transaction_type = 'expense') AS expense_count
            FROM finance.transactions
            WHERE batch_id = $1
            GROUP BY batch_id
            """,
            batch_id,
        )
        if not row:
            return {
                "batch_id": batch_id,
                "total_income_kes": Decimal("0"),
                "total_expense_kes": Decimal("0"),
                "profit_loss_kes": Decimal("0"),
                "income_count": 0,
                "expense_count": 0,
            }
        return dict(row)

    async def list_transactions(
        self,
        batch_id: UUID,
        transaction_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        rows = await self._conn.fetch(
            """
            SELECT id, batch_id, transaction_type, category, amount_kes,
                   mpesa_reference, transaction_date, notes, status, created_at
            FROM finance.transactions
            WHERE batch_id = $1
              AND ($2::text IS NULL OR transaction_type = $2)
            ORDER BY transaction_date DESC, created_at DESC
            LIMIT $3 OFFSET $4
            """,
            batch_id, transaction_type, limit, offset,
        )
        return [dict(row) for row in rows]

    async def create_mpesa_request(
        self,
        transaction_id: UUID,
        checkout_request_id: str,
        merchant_request_id: str,
        phone_number: str,
        amount_kes: Decimal,
    ) -> dict:
        row = await self._conn.fetchrow(
            """
            INSERT INTO finance.mpesa_requests
                (transaction_id, checkout_request_id, merchant_request_id,
                 phone_number, amount_kes)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, checkout_request_id, status, created_at
            """,
            transaction_id, checkout_request_id, merchant_request_id,
            phone_number, amount_kes,
        )
        return dict(row)

    async def handle_mpesa_callback(
        self,
        checkout_request_id: str,
        result_code: int,
        result_desc: str,
        mpesa_receipt_number: Optional[str] = None,
    ) -> None:
        new_status = "completed" if result_code == 0 else "failed"

        await self._conn.execute(
            """
            UPDATE finance.mpesa_requests
            SET status               = $2,
                result_code          = $3,
                result_desc          = $4,
                mpesa_receipt_number = $5,
                completed_at         = NOW()
            WHERE checkout_request_id = $1
            """,
            checkout_request_id, new_status, result_code,
            result_desc, mpesa_receipt_number,
        )

        # If payment succeeded, confirm the linked transaction
        if result_code == 0:
            await self._conn.execute(
                """
                UPDATE finance.transactions t
                SET status = 'confirmed',
                    mpesa_reference = $2
                FROM finance.mpesa_requests mr
                WHERE mr.checkout_request_id = $1
                  AND mr.transaction_id = t.id
                """,
                checkout_request_id, mpesa_receipt_number,
            )
```

---

### Week 10 — Router, Callback Handler, Registration

```python
# app/modules/finance/router.py
from uuid import UUID
from decimal import Decimal
from fastapi import APIRouter, Depends, status, Query, Request
from typing import Optional
from .schemas import (
    RecordTransactionRequest,
    InitiateMpesaRequest,
    TransactionResponse,
    BatchPLResponse,
)
from .service import FinanceService
from .dependencies import get_finance_service

router = APIRouter(prefix="/finance", tags=["finance"])

@router.post(
    "/transactions/income",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def record_income(
    payload: RecordTransactionRequest,
    service: FinanceService = Depends(get_finance_service),
):
    tx = await service.record_income(
        batch_id=payload.batch_id,
        category=payload.category,
        amount_kes=payload.amount_kes,
        transaction_date=payload.transaction_date,
        notes=payload.notes,
    )
    return TransactionResponse.model_validate(tx)

@router.post(
    "/transactions/expense",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def record_expense(
    payload: RecordTransactionRequest,
    service: FinanceService = Depends(get_finance_service),
):
    tx = await service.record_expense(
        batch_id=payload.batch_id,
        category=payload.category,
        amount_kes=payload.amount_kes,
        transaction_date=payload.transaction_date,
        notes=payload.notes,
    )
    return TransactionResponse.model_validate(tx)

@router.get("/batches/{batch_id}/pl", response_model=BatchPLResponse)
async def get_batch_pl(
    batch_id: UUID,
    service: FinanceService = Depends(get_finance_service),
):
    return await service.get_batch_pl(batch_id)

@router.get("/batches/{batch_id}/transactions")
async def list_transactions(
    batch_id: UUID,
    transaction_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: FinanceService = Depends(get_finance_service),
):
    return await service.list_transactions(batch_id, transaction_type, limit, offset)

@router.post("/mpesa/stk-push", status_code=status.HTTP_202_ACCEPTED)
async def initiate_mpesa_payment(
    payload: InitiateMpesaRequest,
    service: FinanceService = Depends(get_finance_service),
):
    return await service.initiate_mpesa_stk_push(
        batch_id=payload.batch_id,
        phone_number=payload.phone_number,
        amount_kes=payload.amount_kes,
        description=payload.description,
    )

@router.post("/mpesa/callback", status_code=status.HTTP_200_OK)
async def mpesa_callback(request: Request, service: FinanceService = Depends(get_finance_service)):
    """
    Safaricom calls this URL after STK push completes.
    Must return 200 quickly — Safaricom retries if response is slow.
    """
    body = await request.json()
    await service.process_mpesa_callback(body)
    return {"ResultCode": 0, "ResultDesc": "Accepted"}
```

### Phase 2 Deliverable

Seven endpoints operational. `GET /finance/batches/{id}/pl` returns correct KES totals. M-Pesa STK push returns `CheckoutRequestID`. Callback handler updates transaction status. P&L query uses `FILTER` aggregation — no ORM.

### Go/No-Go Checkpoint

```bash
# Record expense → record income → check P&L
# P&L must show correct arithmetic

# STK push must return 202 and a checkout_request_id
# (use sandbox — free tier, no real money)

# Callback with result_code=0 must mark transaction as confirmed
# Callback with result_code=1032 must mark transaction as failed
```

---

## Phase 3 — Weeks 11–14: Module 3 — Health + Alerts

### Chain-of-Thought

**What Fredrick already knows:** Full module structure (schema → repository → service → router), raw SQL aggregations, soft references, Pydantic validators.

**What this phase teaches:** Rules engine pattern (threshold-based alert generation), time-window queries (`WHERE log_date >= NOW() - INTERVAL '48 hours'`), alert lifecycle management (active → acknowledged), background processing concept (alert generation triggered by health log creation).

**Track C sync:** Week 13–14 Advanced Python — the rules engine is a practical application of generators, dataclasses, and type hints that Track C covers in theory.

**Vibe Coding workflow:** The disease trigger rules are business logic. Write the rule conditions yourself on paper first: "if mortality in last 48 hours > 3% of batch size, trigger alert." Then implement that condition in raw SQL. Use Claude only to review your SQL logic — not to write it.

**Go/No-Go:** Health log creates automatically evaluates all trigger rules. Active alerts are retrievable. Acknowledging an alert marks it resolved. The 48-hour mortality window calculates correctly against real timestamps.

**Junior mistake:** Hardcoding alert thresholds as magic numbers scattered across the rules engine. Prevention: define all thresholds as named constants in one file at the top of the health module.

---

### Phase Goal

Build the Health module: daily health logging, threshold-based disease trigger rules, alert generation, and alert acknowledgement. By end of Phase 3, a farmer can log daily health observations and receive automatic alerts when thresholds are breached.

---

### Week 11 — Health Schema

```sql
-- migrations/health/001_create_health_tables.sql

CREATE TABLE IF NOT EXISTS health.daily_logs (
    id                  UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id            UUID         NOT NULL,    -- soft reference
    log_date            DATE         NOT NULL,
    mortality_count     INTEGER      NOT NULL DEFAULT 0 CHECK (mortality_count >= 0),
    symptoms            TEXT[],                  -- PostgreSQL array of symptom strings
    feed_consumption_kg NUMERIC(8,2) NOT NULL DEFAULT 0,
    water_consumption_l NUMERIC(8,2) NOT NULL DEFAULT 0,
    notes               TEXT,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    -- One log per batch per day
    CONSTRAINT uq_health_log_batch_date UNIQUE (batch_id, log_date)
);

CREATE TABLE IF NOT EXISTS health.alerts (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id        UUID         NOT NULL,
    alert_type      TEXT         NOT NULL,
    severity        TEXT         NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    message         TEXT         NOT NULL,
    trigger_value   NUMERIC,
    threshold_value NUMERIC,
    status          TEXT         NOT NULL DEFAULT 'active'
                                 CHECK (status IN ('active', 'acknowledged', 'resolved')),
    acknowledged_at TIMESTAMPTZ,
    acknowledged_by TEXT,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_health_logs_batch_date
    ON health.daily_logs(batch_id, log_date DESC);

CREATE INDEX idx_alerts_batch_status
    ON health.alerts(batch_id, status)
    WHERE status = 'active';
```

---

### Week 12 — Rules Engine

```python
# app/modules/health/rules.py
"""
Disease trigger rules for broiler health monitoring.
All thresholds defined here as named constants — never hardcoded elsewhere.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

# ─── Thresholds ───────────────────────────────────────────────────────────────
MORTALITY_48HR_THRESHOLD_PCT = Decimal("3.0")   # >3% mortality in 48 hours
FEED_DROP_THRESHOLD_PCT = Decimal("20.0")        # >20% feed drop vs 7-day average
WATER_DROP_THRESHOLD_PCT = Decimal("25.0")       # >25% water drop vs 7-day average
HIGH_MORTALITY_SINGLE_DAY_PCT = Decimal("1.5")   # >1.5% mortality in single day

@dataclass
class AlertTrigger:
    alert_type: str
    severity: str
    message: str
    trigger_value: Optional[Decimal]
    threshold_value: Optional[Decimal]

async def evaluate_mortality_48hr(
    conn,
    batch_id,
    batch_quantity: int,
) -> Optional[AlertTrigger]:
    """
    Check if mortality in the last 48 hours exceeds 3% of batch size.
    """
    row = await conn.fetchrow(
        """
        SELECT COALESCE(SUM(mortality_count), 0) AS total_mortality
        FROM health.daily_logs
        WHERE batch_id = $1
          AND log_date >= CURRENT_DATE - INTERVAL '2 days'
        """,
        batch_id,
    )
    total = Decimal(str(row["total_mortality"]))
    threshold_count = (MORTALITY_48HR_THRESHOLD_PCT / 100) * batch_quantity
    pct = (total / batch_quantity * 100) if batch_quantity > 0 else Decimal("0")

    if total >= threshold_count:
        return AlertTrigger(
            alert_type="high_mortality_48hr",
            severity="critical",
            message=(
                f"Mortality in last 48 hours is {pct:.1f}% "
                f"({int(total)} birds) — exceeds {MORTALITY_48HR_THRESHOLD_PCT}% threshold. "
                f"Immediate veterinary attention recommended."
            ),
            trigger_value=pct,
            threshold_value=MORTALITY_48HR_THRESHOLD_PCT,
        )
    return None

async def evaluate_feed_drop(
    conn,
    batch_id,
) -> Optional[AlertTrigger]:
    """
    Check if today's feed consumption dropped >20% vs 7-day average.
    """
    row = await conn.fetchrow(
        """
        WITH recent AS (
            SELECT
                feed_consumption_kg,
                log_date,
                ROW_NUMBER() OVER (ORDER BY log_date DESC) AS rn
            FROM health.daily_logs
            WHERE batch_id = $1
              AND feed_consumption_kg > 0
        ),
        today_log AS (
            SELECT feed_consumption_kg FROM recent WHERE rn = 1
        ),
        week_avg AS (
            SELECT AVG(feed_consumption_kg) AS avg_feed
            FROM recent
            WHERE rn BETWEEN 2 AND 8    -- previous 7 days, excluding today
        )
        SELECT
            t.feed_consumption_kg AS today_feed,
            w.avg_feed            AS week_avg_feed,
            CASE
                WHEN w.avg_feed > 0
                THEN ROUND(
                    (w.avg_feed - t.feed_consumption_kg) * 100 / w.avg_feed,
                    2
                )
                ELSE 0
            END AS drop_pct
        FROM today_log t, week_avg w
        """,
        batch_id,
    )
    if not row or not row["week_avg_feed"] or row["week_avg_feed"] == 0:
        return None

    drop_pct = Decimal(str(row["drop_pct"]))
    if drop_pct >= FEED_DROP_THRESHOLD_PCT:
        return AlertTrigger(
            alert_type="feed_consumption_drop",
            severity="high",
            message=(
                f"Feed consumption dropped {drop_pct:.1f}% vs 7-day average "
                f"({row['today_feed']}kg vs avg {row['week_avg_feed']:.1f}kg). "
                f"Possible disease indicator — monitor closely."
            ),
            trigger_value=drop_pct,
            threshold_value=FEED_DROP_THRESHOLD_PCT,
        )
    return None

# Registry of all rules — add new rules here only
RULE_EVALUATORS = [
    evaluate_mortality_48hr,
    evaluate_feed_drop,
]
```

---

### Week 13 — Service Layer and Alert Lifecycle

```python
# app/modules/health/service.py
import asyncio
from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional
from .repository import HealthRepository
from .rules import RULE_EVALUATORS, evaluate_mortality_48hr, evaluate_feed_drop
from .exceptions import HealthLogNotFoundError, AlertNotFoundError, DuplicateLogError

class HealthService:
    def __init__(self, repository: HealthRepository):
        self._repo = repository

    async def log_daily_health(
        self,
        batch_id: UUID,
        log_date: date,
        mortality_count: int,
        feed_consumption_kg: Decimal,
        water_consumption_l: Decimal,
        symptoms: Optional[list[str]] = None,
        notes: Optional[str] = None,
        batch_quantity: int = 0,
    ) -> dict:
        # Check for duplicate log
        existing = await self._repo.find_log(batch_id, log_date)
        if existing:
            raise DuplicateLogError(batch_id, log_date)

        log = await self._repo.create_log(
            batch_id=batch_id,
            log_date=log_date,
            mortality_count=mortality_count,
            feed_consumption_kg=feed_consumption_kg,
            water_consumption_l=water_consumption_l,
            symptoms=symptoms or [],
            notes=notes,
        )

        # Evaluate alert triggers after log creation
        await self._evaluate_and_create_alerts(batch_id, batch_quantity)

        return log

    async def _evaluate_and_create_alerts(
        self,
        batch_id: UUID,
        batch_quantity: int,
    ) -> None:
        """
        Run all trigger rules. Create alerts for any that fire.
        Existing active alerts of the same type are not duplicated.
        """
        conn = self._repo._conn

        # Mortality rule requires batch_quantity
        mortality_trigger = await evaluate_mortality_48hr(conn, batch_id, batch_quantity)
        if mortality_trigger:
            existing = await self._repo.find_active_alert(
                batch_id, mortality_trigger.alert_type
            )
            if not existing:
                await self._repo.create_alert(
                    batch_id=batch_id,
                    alert_type=mortality_trigger.alert_type,
                    severity=mortality_trigger.severity,
                    message=mortality_trigger.message,
                    trigger_value=mortality_trigger.trigger_value,
                    threshold_value=mortality_trigger.threshold_value,
                )

        feed_trigger = await evaluate_feed_drop(conn, batch_id)
        if feed_trigger:
            existing = await self._repo.find_active_alert(
                batch_id, feed_trigger.alert_type
            )
            if not existing:
                await self._repo.create_alert(
                    batch_id=batch_id,
                    alert_type=feed_trigger.alert_type,
                    severity=feed_trigger.severity,
                    message=feed_trigger.message,
                    trigger_value=feed_trigger.trigger_value,
                    threshold_value=feed_trigger.threshold_value,
                )

    async def get_health_history(
        self,
        batch_id: UUID,
        limit: int = 30,
        offset: int = 0,
    ) -> list[dict]:
        return await self._repo.list_logs(batch_id, limit, offset)

    async def get_active_alerts(self, batch_id: UUID) -> list[dict]:
        return await self._repo.list_active_alerts(batch_id)

    async def acknowledge_alert(self, alert_id: UUID, acknowledged_by: str) -> dict:
        alert = await self._repo.find_alert(alert_id)
        if not alert:
            raise AlertNotFoundError(alert_id)
        if alert["status"] != "active":
            from .exceptions import AlertAlreadyAcknowledgedError
            raise AlertAlreadyAcknowledgedError(alert_id)
        return await self._repo.acknowledge_alert(alert_id, acknowledged_by)
```

---

### Week 14 — Router and Phase 3 Completion

Five endpoints: `POST /health/logs`, `GET /health/batches/{id}/logs`, `GET /health/batches/{id}/alerts`, `POST /health/alerts/{id}/acknowledge`, `GET /health/alerts/{id}`.

### Phase 3 Deliverable

Health logging creates alerts automatically when thresholds are breached. Alert lifecycle (active → acknowledged) works. Feed drop detection uses a 7-day rolling average in pure SQL.

### Go/No-Go Checkpoint

```bash
# Log 3 days of health data with high mortality
# GET /health/batches/{id}/alerts must return at least one critical alert

# Acknowledge the alert
# GET /health/alerts/{id} must show status: acknowledged

# Log health data below thresholds
# No new alerts should be created
```

---

## Phase 4 — Weeks 15–16: Auth Hardening + Route Protection

### Chain-of-Thought

**What Fredrick already knows:** All three modules working end-to-end. Dependency injection pattern deeply familiar.

**What this phase teaches:** OTP generation and validation flow, Redis for OTP storage with TTL, JWT access + refresh token pair, FastAPI dependency for protected routes, Africa's Talking SMS API.

**Track C sync:** Week 20 Auth — this phase implements what Track C covers in theory. You will arrive at Week 20 with working auth code, and the theory will explain why your implementation is secure.

**Vibe Coding workflow:** The OTP flow is security-critical. Generate it with Claude, then audit every security decision line by line: "Why `secrets.randbelow` and not `random.randint`? Why `hmac.compare_digest` and not `==`? Why a 6-minute TTL?" If you cannot answer these, do not deploy.

**Go/No-Go:** OTP request sends an SMS (Africa's Talking sandbox — free). OTP verification returns a JWT. Protected route returns 401 without token. Token refresh works. Brute-force lockout after 5 failed attempts.

**Junior mistake:** Logging the OTP value in structured logs for debugging convenience. Prevention: never log OTP values, token payloads, or phone numbers in plaintext. Use masked values: `phone=+254***678`.

---

### Phase Goal

Implement OTP-based authentication using Africa's Talking SMS, Redis OTP storage, JWT issuance, and protect all module endpoints behind JWT middleware.

### Week 15 — OTP Flow and JWT

```sql
-- migrations/auth/001_create_auth_tables.sql

CREATE TABLE IF NOT EXISTS auth.users (
    id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    phone        TEXT         NOT NULL UNIQUE,
    full_name    TEXT         NOT NULL,
    farm_name    TEXT,
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    last_login   TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS auth.otp_attempts (
    id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    phone        TEXT         NOT NULL,
    attempt_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    success      BOOLEAN      NOT NULL DEFAULT FALSE
);

-- Rate limiting: how many failed attempts in last 15 minutes
CREATE INDEX idx_otp_attempts_phone_time
    ON auth.otp_attempts(phone, attempt_at DESC);
```

```python
# app/modules/auth/otp_service.py
import secrets
import hmac
import hashlib
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

OTP_TTL_SECONDS = 360        # 6 minutes
OTP_LENGTH = 6
MAX_ATTEMPTS_PER_WINDOW = 5
ATTEMPT_WINDOW_SECONDS = 900  # 15 minutes

class OTPService:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client

    def _generate_otp(self) -> str:
        """Cryptographically secure 6-digit OTP."""
        return str(secrets.randbelow(10**OTP_LENGTH)).zfill(OTP_LENGTH)

    def _otp_key(self, phone: str) -> str:
        return f"otp:{phone}"

    def _attempt_key(self, phone: str) -> str:
        return f"otp_attempts:{phone}"

    async def generate_and_store(self, phone: str) -> str:
        # Check rate limit
        attempts = await self._redis.get(self._attempt_key(phone))
        if attempts and int(attempts) >= MAX_ATTEMPTS_PER_WINDOW:
            from .exceptions import OTPRateLimitError
            raise OTPRateLimitError(phone)

        otp = self._generate_otp()

        # Store hashed OTP — never store plaintext
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()
        await self._redis.setex(self._otp_key(phone), OTP_TTL_SECONDS, otp_hash)

        logger.info("OTP generated", extra={"phone": f"+254***{phone[-3:]}"})
        return otp  # returned to caller for SMS sending — never logged here

    async def verify(self, phone: str, otp: str) -> bool:
        stored_hash = await self._redis.get(self._otp_key(phone))
        if not stored_hash:
            return False

        # Increment attempt counter
        pipe = self._redis.pipeline()
        pipe.incr(self._attempt_key(phone))
        pipe.expire(self._attempt_key(phone), ATTEMPT_WINDOW_SECONDS)
        await pipe.execute()

        # Constant-time comparison — prevents timing attacks
        submitted_hash = hashlib.sha256(otp.encode()).hexdigest()
        valid = hmac.compare_digest(
            stored_hash.decode() if isinstance(stored_hash, bytes) else stored_hash,
            submitted_hash,
        )

        if valid:
            # Invalidate OTP immediately after successful use
            await self._redis.delete(self._otp_key(phone))
            # Reset attempt counter on success
            await self._redis.delete(self._attempt_key(phone))

        return valid
```

### Week 16 — JWT and Route Protection

```python
# app/modules/auth/jwt_service.py
from datetime import datetime, UTC, timedelta
from uuid import UUID
import jwt
from app.core.config import settings

ACCESS_TOKEN_EXPIRE = timedelta(minutes=settings.access_token_expire_minutes)
REFRESH_TOKEN_EXPIRE = timedelta(days=settings.refresh_token_expire_days)

def create_access_token(user_id: UUID, phone: str) -> str:
    payload = {
        "sub": str(user_id),
        "phone": phone,
        "type": "access",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + ACCESS_TOKEN_EXPIRE,
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def create_refresh_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + REFRESH_TOKEN_EXPIRE,
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def verify_token(token: str, token_type: str = "access") -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if payload.get("type") != token_type:
            raise ValueError("Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        from .exceptions import TokenExpiredError
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        from .exceptions import InvalidTokenError
        raise InvalidTokenError()
```

```python
# app/core/dependencies.py — shared across all modules
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.modules.auth.jwt_service import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/verify-otp")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = verify_token(token, "access")
        return {"user_id": payload["sub"], "phone": payload["phone"]}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

All three module routers then add `current_user: dict = Depends(get_current_user)` to each route handler.

### Phase 4 Deliverable

`POST /auth/request-otp` sends SMS. `POST /auth/verify-otp` returns JWT. All module endpoints return 401 without token. Brute force lockout after 5 attempts within 15 minutes.

### Go/No-Go Checkpoint

```bash
# Request OTP → verify OTP → get JWT → call protected endpoint
# Full flow must work end to end

# Call any batch endpoint without Authorization header → 401
# Call with expired token → 401
# Submit wrong OTP 5 times → rate limit error on 6th attempt
```

---

## Phase 5 — Weeks 17–18: Testing

### Chain-of-Thought

**What Fredrick already knows:** All four modules working. asyncpg patterns deeply familiar. Business logic is separated from routers.

**What this phase teaches:** pytest with asyncio, Testcontainers for real PostgreSQL in tests, FastAPI TestClient for slice tests, test fixtures with transaction rollback for isolation, 80%+ coverage on business logic.

**Track C sync:** Week 16 on the roadmap covers testing — this phase is its direct application.

**Vibe Coding workflow:** Use Claude to generate the `conftest.py` Testcontainers setup. Do not use it until you can explain what `scope="session"` means and why the rollback fixture uses `scope="function"`. Every test you write must be written by hand first, then shown to Claude for review.

**Go/No-Go:** `pytest --cov=app --cov-report=term-missing` shows ≥80% coverage on `service.py` files. All slice tests pass. `pytest -m integration` passes against a real PostgreSQL instance.

**Junior mistake:** Writing tests that test the ORM/query layer by asserting on raw SQL strings instead of on behaviour. Prevention: tests assert on what the endpoint returns, not on what SQL was executed.

---

### Phase Goal

Write the test suite that proves the system works: unit tests for service business logic, integration tests for repositories, slice tests for all endpoints.

### Week 17 — Test Infrastructure and Unit Tests

```python
# tests/conftest.py
import asyncio
import pytest
import asyncpg
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def postgres_container():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container

@pytest.fixture(scope="session")
async def db_pool(postgres_container):
    dsn = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2", "postgresql"
    )
    # Run migrations
    conn = await asyncpg.connect(dsn)
    for schema in ["batches", "finance", "health", "auth", "core"]:
        await conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    # Run all migration SQL files
    import glob
    for sql_file in sorted(glob.glob("migrations/**/*.sql", recursive=True)):
        await conn.execute(open(sql_file).read())
    await conn.close()

    pool = await asyncpg.create_pool(dsn=dsn, min_size=2, max_size=5,
                                      statement_cache_size=0)
    yield pool
    await pool.close()

@pytest.fixture
async def db_conn(db_pool):
    """Transaction-isolated connection — rolls back after each test."""
    async with db_pool.acquire() as conn:
        tx = conn.transaction()
        await tx.start()
        yield conn
        await tx.rollback()

@pytest.fixture
async def client(db_pool):
    app.state.batches_pool = db_pool
    app.state.finance_pool = db_pool
    app.state.health_pool = db_pool
    app.state.auth_pool = db_pool
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as c:
        yield c
```

```python
# tests/unit/test_batch_service.py
import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock
from app.modules.batches.service import BatchService, VALID_TRANSITIONS
from app.modules.batches.exceptions import (
    BatchNotFoundError,
    InvalidStatusTransitionError,
)

@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def service(mock_repo):
    return BatchService(repository=mock_repo)

class TestStatusTransitions:

    async def test_active_can_transition_to_closed(self, service, mock_repo):
        batch = AsyncMock()
        batch.status = "active"
        mock_repo.find_by_id.return_value = batch
        mock_repo.update_status.return_value = batch

        await service.transition_status(uuid4(), "closed")
        mock_repo.update_status.assert_called_once()

    async def test_closed_cannot_transition_to_active(self, service, mock_repo):
        batch = AsyncMock()
        batch.status = "closed"
        mock_repo.find_by_id.return_value = batch

        with pytest.raises(InvalidStatusTransitionError):
            await service.transition_status(uuid4(), "active")

    async def test_archived_has_no_valid_transitions(self):
        assert VALID_TRANSITIONS["archived"] == []

    async def test_raises_not_found_for_missing_batch(self, service, mock_repo):
        mock_repo.find_by_id.return_value = None

        with pytest.raises(BatchNotFoundError):
            await service.get_batch(uuid4())
```

### Week 18 — Integration and Slice Tests

```python
# tests/slices/test_batches_slices.py
import pytest
from uuid import uuid4

class TestCreateBatch:

    async def test_creates_batch_successfully(self, client):
        response = await client.post("/api/v1/batches/", json={
            "batch_name": "Batch A",
            "breed": "Ross 308",
            "quantity": 500,
            "start_date": "2026-05-01",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["batch_name"] == "Batch A"
        assert data["status"] == "active"
        assert data["quantity"] == 500

    async def test_returns_422_for_negative_quantity(self, client):
        response = await client.post("/api/v1/batches/", json={
            "batch_name": "Bad Batch",
            "breed": "Ross",
            "quantity": -1,
            "start_date": "2026-05-01",
        })
        assert response.status_code == 422

    async def test_returns_422_for_empty_name(self, client):
        response = await client.post("/api/v1/batches/", json={
            "batch_name": "   ",# kukufiti-api - Integrated 20-Week Roadmap

## Canonical Roadmap

This is the single execution roadmap for building `kukufiti-api` as a production-style backend for broiler farm intelligence in Kenya.

It synthesizes:

- `KukuFiti_Engineering_Guide.md`
- `KukuFiti Framework Godmode.md`
- `kukufiti_architectural_audit.md`
- `Modular Monolith Backend Architecture.md`
- The original `kukufiti api 20 Week Phased.md`

The other documents remain reference material. This file is the weekly build plan.

---

## Final Target

By the end of Week 20, `kukufiti-api` is a deployable FastAPI modular monolith with:

- A public Render deployment.
- Clean OpenAPI docs at `/docs`.
- A README that lets a reviewer run the project locally in under 10 minutes.
- PostgreSQL schema-per-module isolation.
- Row Level Security for tenant isolation.
- Soft deletes for AI-safe historical data.
- Idempotent M-Pesa payment callbacks.
- Batch lifecycle, operational logs, health alerts, finance, auth, and reporting.
- 80%+ test coverage on business logic.
- One live demo flow that exercises the system end to end.

This roadmap keeps the public domain language as `batches`. Concepts from the newer engineering guide that use `flocks` are translated into batch lifecycle events, batch operational logs, and batch intelligence.

---

## Architecture Baseline

### Core Stack

| Layer | Decision |
|---|---|
| API | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL 16 |
| Database access | Raw SQL through asyncpg |
| Validation | Pydantic v2 |
| Packaging | Docker and Docker Compose |
| Tests | Pytest |
| Deployment | Render primary target |
| AI-ready data | Event logs, strict enums/reference tables, batch context records |

### Modular Monolith Rules

The app is one deployable FastAPI service, but its modules are strict vertical slices.

```

app/
core/
shared/
modules/
batches/
finance/
health/
auth/
advisory/
migrations/
batches/
finance/
health/
auth/
advisory/
tests/
unit/
integration/
slices/
architecture/

````

Each module owns:

- Its router.
- Its service layer.
- Its repository layer.
- Its schemas and domain models.
- Its migrations.
- Its PostgreSQL schema.
- Its public contract.

No module reaches into another module's internal repository, model, migration, or private helper.

### Layer Rules

| Layer | Owns | Must not do |
|---|---|---|
| Router | HTTP input/output, dependencies, response codes | Business decisions, SQL |
| Service | Business rules, transactions, event emission | HTTP details, raw SQL |
| Repository | Raw SQL, persistence, row mapping | Business decisions, HTTP |
| Database | Constraints, RLS, indexes, integrity | Application branching |

### Cross-Module Communication

Allowed:

- Service contracts exposed by a module.
- Thin domain events.
- Outbox events for reliable async work.
- Shared value objects in `app/shared`.

Forbidden:

- Cross-module SQL joins.
- Importing another module's repository.
- Importing another module's internal model.
- Polling another module's table as a communication mechanism.

### Database Rules

Use one PostgreSQL database with schema isolation:

- `batches.*`
- `finance.*`
- `health.*`
- `auth.*`
- `advisory.*`
- `core.*` for system infrastructure such as outbox events and audit logs.

Every tenant-owned table must include:

- `id`
- `farm_id`
- `created_at`
- `updated_at`
- `deleted_at`

Every tenant-owned table must have Row Level Security enabled before the feature is considered complete.

Hard delete is not part of normal application behavior. Historical data is needed for audits, financial trust, and later AI training.

### Event Model

KukuFiti is not a CRUD app with alerts bolted on. It is an operational event system.

Examples of domain events:

- `BatchCreated`
- `BatchStatusChanged`
- `DailyLogRecorded`
- `MortalityLogged`
- `FeedRecorded`
- `WaterRecorded`
- `WeightMeasured`
- `ExpenseRecorded`
- `IncomeRecorded`
- `PaymentReceived`
- `AlertRaised`
- `AlertAcknowledged`

Events should be thin. They include identifiers and facts owned by the emitting module, not full object snapshots.

The Week 1-2 foundation introduces an in-process event bus for learning and local decoupling. Later phases add an outbox table so events are persisted in the same transaction as the business change.

---

## Canonical Module Map

| Module | Owns | Emits |
|---|---|---|
| `batches` | batch lifecycle, target matrix, daily logs, mortality/feed/water/weight records, pre-placement checks, seasonal context | `BatchCreated`, `DailyLogRecorded`, `MortalityLogged`, `FeedRecorded`, `WeightMeasured` |
| `finance` | income, expenses, feed inventory cost, sales, M-Pesa transactions, P&L, break-even, harvest economics | `ExpenseRecorded`, `IncomeRecorded`, `PaymentReceived`, `FeedDeliveryRecorded` |
| `health` | rules engine, alerts, vaccinations, water quality, litter, lighting, biosecurity, emergency protocols | `AlertRaised`, `AlertAcknowledged`, `VaccinationRecorded` |
| `auth` | users, farms, farm members, OTP, JWT, route protection, tenant context | `FarmCreated`, `MemberAdded` |
| `advisory` | AI-ready context, recommendation records, later pgvector/LangGraph integration | `RecommendationCreated` |
| `core` | config, logging, database pool, event bus, outbox, exception handling, middleware | System events only |

The first 20 weeks build the backend foundation and deterministic intelligence. Advanced ML and large-scale infrastructure are reserved for the Post-20 Backlog.

---

## Phase 0 - Weeks 1-2: Foundation, Boundaries, and Safety Rails

### Phase Goal

Create a FastAPI project that boots reliably, connects to PostgreSQL, enforces modular boundaries from Day 1, and gives every later feature a safe place to live.

This phase is not feature work. It is the foundation that prevents the project from becoming a layered big ball of mud.

### Week 1 - Project Skeleton, Docker, and Schema Isolation

Build:

- Project folder structure for `core`, `shared`, and modules.
- `docker-compose.yml` with PostgreSQL.
- `.env.example` and gitignored `.env`.
- `requirements.txt`.
- FastAPI `app/main.py`.
- `app/core/config.py`.
- `app/core/database.py`.
- `app/core/logging.py`.
- `scripts/run_migration.py`.
- Initial migrations for schemas and roles.

Database setup:

- Create schemas: `batches`, `finance`, `health`, `auth`, `advisory`, `core`.
- Create application role and module-specific roles.
- Grant each module role access only to its own schema.
- Deny default access to `public`.

Learning focus:

- Why a modular monolith is one deployable service with strict internal boundaries.
- Why schema-per-module is used instead of one large `public` schema.
- Why raw SQL forces understanding of indexes, constraints, and query behavior.

Acceptance:

- `docker compose up` starts PostgreSQL.
- API starts locally.
- `GET /health` returns database connectivity status.
- A role for one module cannot read another module's schema.

### Week 2 - RLS, Soft Deletes, Event Bus, and Outbox Skeleton

Build:

- Shared timestamp/soft-delete conventions.
- Tenant context helper based on `farm_id`.
- RLS policy pattern for tenant-owned tables.
- In-memory domain event bus.
- `core.outbox_events` table.
- Outbox writer API.
- Structured logging setup.
- Correlation ID middleware.
- Global exception handler.

Design rules:

- Every business mutation that should notify another module writes an outbox event in the same database transaction.
- Events are processed after commit.
- Logs include correlation ID, farm ID when available, route, status code, and elapsed time.

Acceptance:

- RLS test proves farm A cannot read farm B records.
- Soft-deleted rows disappear from normal queries but remain in the database.
- Event bus unit test proves multiple handlers can subscribe to one event.
- Outbox insert happens in the same transaction as a sample business insert.

### Phase 0 Go/No-Go

- API boots locally.
- Database health endpoint works.
- Schemas and roles exist.
- RBAC blocks cross-schema reads.
- RLS pattern is documented and tested.
- Soft delete pattern is documented and tested.
- Event bus and outbox skeleton exist.
- No module imports another module's internals.

---

## Phase 1 - Weeks 3-6: Batches, Operational Records, and Baseline Intelligence

### Phase Goal

Build the batch domain as the operational heart of KukuFiti.

A batch is not just a row with a start date. It is a 42-day biological and economic lifecycle made of daily records, target curves, mortality events, feed/water/weight measurements, seasonal context, and status transitions.

### Week 3 - Batch Lifecycle and Core Repository

Build:

- `batches.batches`
- `batches.batch_status_history`
- Batch repository with raw SQL.
- Batch service with lifecycle rules.
- Pydantic schemas for create, update, response, and summary.
- Router endpoints:
  - `POST /api/v1/batches`
  - `GET /api/v1/batches`
  - `GET /api/v1/batches/{batch_id}`
  - `PATCH /api/v1/batches/{batch_id}/status`
  - `POST /api/v1/batches/{batch_id}/close`

Core fields:

- `farm_id`
- `batch_name`
- `breed`
- `start_date`
- `initial_bird_count`
- `current_bird_count`
- `status`
- `house_name`
- `notes`
- timestamps and `deleted_at`

Status rules:

- `planned -> active`
- `active -> closed`
- `active -> cancelled`
- `planned -> cancelled`
- Closed and cancelled batches cannot become active again.

Events:

- Emit `BatchCreated`.
- Emit `BatchStatusChanged`.

Acceptance:

- Invalid status transitions return 400.
- Empty names and negative bird counts return 422.
- List endpoint uses cursor-style pagination, not offset pagination.
- Repository queries never cross into another module's schema.

### Week 4 - Target Matrix, Pre-Placement, and Seasonal Context

Build:

- `batches.batch_targets`
- `batches.pre_placement_checklist`
- `batches.farm_location_context`
- Seed migration for the 42-day target matrix.
- Batch target lookup service.
- Batch age calculation.
- Seasonal risk helper for Kenya seasons.

Target matrix includes:

- Day number.
- Target weight.
- Daily gain.
- Daily feed.
- Cumulative feed.
- Target water.
- Target temperature.
- Expected mortality percentage.

Pre-placement checklist covers:

- Cleanout.
- Disinfection.
- Litter readiness.
- Brooder readiness.
- Water line flushing.
- Feeder setup.
- Temperature pre-heating.
- Chick arrival readiness.

Seasonal context covers:

- Long rains.
- Cool dry season.
- Short rains.
- Hot dry season.
- Altitude/climate notes for future threshold adjustment.

Acceptance:

- A batch can retrieve its current day target.
- Missing target day returns a controlled error.
- Pre-placement checklist can be recorded before activation.
- Seasonal risk is calculated from farm context and date.

### Week 5 - Daily Operational Records

Build:

- `batches.daily_logs`
- `batches.mortality_events`
- `batches.feed_events`
- `batches.water_events`
- `batches.weight_samples`
- Repositories and services for operational records.
- Router endpoints:
  - `POST /api/v1/batches/{batch_id}/daily-logs`
  - `GET /api/v1/batches/{batch_id}/daily-logs`
  - `POST /api/v1/batches/{batch_id}/mortality`
  - `POST /api/v1/batches/{batch_id}/feed`
  - `POST /api/v1/batches/{batch_id}/water`
  - `POST /api/v1/batches/{batch_id}/weights`

Validation:

- Mortality count cannot exceed current live birds.
- Feed and water quantities cannot be negative.
- Weight samples must have positive weights.
- Daily log date must fall inside the batch lifecycle.
- Use enums or reference values for standardized causes and symptoms where possible.

Derived metrics:

- Current live bird count.
- Daily mortality rate.
- Cumulative mortality rate.
- Feed conversion ratio.
- Water-to-feed ratio.
- Average weight.
- Weight uniformity coefficient of variation.

Events:

- Emit `DailyLogRecorded`.
- Emit `MortalityLogged`.
- Emit `FeedRecorded`.
- Emit `WaterRecorded`.
- Emit `WeightMeasured`.

Acceptance:

- Current bird count is derived correctly after mortality.
- FCR does not divide by zero.
- Water-to-feed ratio is calculated when both inputs exist.
- Duplicate daily logs for the same batch/date are rejected or updated by explicit rule.

### Week 6 - Batch Summary, Intelligence Read Models, and API Polish

Build:

- `GET /api/v1/batches/{batch_id}/summary`
- `GET /api/v1/batches/{batch_id}/targets/today`
- `GET /api/v1/batches/{batch_id}/performance`
- Read model queries for dashboard-style summaries.
- OpenAPI descriptions for all batch endpoints.

Summary includes:

- Batch age.
- Initial and current bird count.
- Mortality totals and rates.
- Feed totals.
- Water totals.
- Average weight.
- FCR.
- Target vs actual weight.
- Target vs actual feed.
- Target vs actual water.
- Seasonal risk note.
- Status and close information.

Acceptance:

- Summary returns numbers instead of nulls where zero is correct.
- Closed batches keep historical metrics stable.
- Batch endpoints are protected by module boundaries and tested via slice tests.

### Phase 1 Go/No-Go

- Batch lifecycle works end to end.
- 42-day target matrix exists and is queryable.
- Daily operational records work.
- Derived metrics are correct.
- Batch summary is useful in Swagger.
- Batch module emits events but does not call finance, health, or advisory internals.

---

## Phase 2 - Weeks 7-10: Finance, M-Pesa, Feed Inventory, and Harvest Economics

### Phase Goal

Build financial trust. Farmers must be able to record costs, sales, feed inventory, M-Pesa transactions, and batch profitability without double-counting money or losing payment state.

### Week 7 - Finance Schema and Core Transactions

Build:

- `finance.expenses`
- `finance.income`
- `finance.sales`
- `finance.transaction_categories`
- Finance repository and service.
- Router endpoints:
  - `POST /api/v1/finance/batches/{batch_id}/expenses`
  - `POST /api/v1/finance/batches/{batch_id}/income`
  - `GET /api/v1/finance/batches/{batch_id}/transactions`
  - `GET /api/v1/finance/batches/{batch_id}/pl`

Rules:

- Expenses and income are tenant-owned.
- Currency is KES.
- Amounts must be positive.
- Batch IDs are soft references, not foreign keys across schemas.
- Finance verifies batch existence through a `batches` contract, not by querying `batches.*` directly.

Acceptance:

- P&L arithmetic is correct.
- Finance repository only queries `finance.*`.
- Finance service uses a public batch contract for batch validation.

### Week 8 - M-Pesa Daraja and Strict Idempotency

Build:

- `finance.mpesa_transactions`
- M-Pesa client wrapper.
- STK push endpoint.
- Callback endpoint.
- Idempotency-first callback service.

Router endpoints:

- `POST /api/v1/finance/mpesa/stk-push`
- `POST /api/v1/finance/mpesa/callback`
- `GET /api/v1/finance/mpesa/{checkout_request_id}`

Non-negotiable payment rules:

- Insert raw callback into `mpesa_transactions` before mutating any business entity.
- `checkout_request_id` is unique.
- Duplicate callbacks return success without double-applying effects.
- Callback processing is atomic.
- Raw payload is retained for audit.

Acceptance:

- STK push returns 202 with checkout request ID.
- Successful callback marks transaction confirmed.
- Failed or cancelled callback marks transaction failed.
- Duplicate successful callback does not duplicate income, subscription state, or any downstream effect.

### Week 9 - Feed Inventory and Cost Intelligence

Build:

- `finance.feed_inventory`
- Feed delivery records.
- Feed usage cost helpers.
- Supplier and feed brand fields.
- Mycotoxin/quality flag fields.
- Router endpoints:
  - `POST /api/v1/finance/batches/{batch_id}/feed-inventory`
  - `GET /api/v1/finance/batches/{batch_id}/feed-inventory`
  - `GET /api/v1/finance/batches/{batch_id}/feed-stock`

Fields:

- Feed brand.
- Feed phase.
- Supplier.
- Bag count or quantity kg.
- Cost per kg.
- Delivery date.
- Mill date when known.
- Batch or lot number when known.
- Quality concern flag.

Acceptance:

- Feed stock summary calculates remaining feed.
- Feed cost contributes to batch P&L.
- Quality flags are stored as structured fields, not loose prose only.

### Week 10 - Break-Even, Harvest Economics, and Finance Completion

Build:

- Break-even calculator.
- Batch profitability summary.
- Harvest economics endpoint.
- Feed withdrawal timer fields or endpoint plan.
- Router endpoints:
  - `GET /api/v1/finance/batches/{batch_id}/break-even`
  - `GET /api/v1/finance/batches/{batch_id}/harvest-economics`
  - `POST /api/v1/finance/batches/{batch_id}/feed-withdrawal/start`

Calculations:

- Total expenses.
- Total income.
- Net profit.
- Cost per live bird.
- Cost per kg live weight where weight data exists.
- Break-even price per kg.
- Marginal harvest recommendation from Day 28 onward.

Acceptance:

- Harvest economics handles missing weight data gracefully.
- Break-even calculation is documented in code and Swagger.
- Finance summary can be used in the final live demo.

### Phase 2 Go/No-Go

- Finance records income and expenses.
- P&L is correct.
- M-Pesa callback idempotency is tested.
- Feed inventory supports stock and cost visibility.
- Harvest economics endpoint works with real batch data.
- Finance never directly joins or queries `batches.*`.

---

## Phase 3 - Weeks 11-14: Health, Alerts, and Operational Intelligence

### Phase Goal

Turn biological and operational knowledge into deterministic backend intelligence.

This phase does not require advanced ML. It builds the rules, records, and alerts that later AI systems will learn from.

### Week 11 - Health Schema, Alert Lifecycle, and Rules Engine Skeleton

Build:

- `health.alerts`
- `health.alert_status_history`
- `health.rule_evaluations`
- Rules engine module.
- Alert service.
- Router endpoints:
  - `GET /api/v1/health/batches/{batch_id}/alerts`
  - `GET /api/v1/health/alerts/{alert_id}`
  - `POST /api/v1/health/alerts/{alert_id}/acknowledge`
  - `POST /api/v1/health/alerts/{alert_id}/resolve`

Alert statuses:

- `open`
- `acknowledged`
- `resolved`
- `dismissed`

Initial rules:

- Feed intake deviation.
- Water-to-feed ratio deviation.
- Mortality spike.
- Weight/FCR deviation.

Acceptance:

- Rules can run against batch summary data through public contracts.
- Alerts are not duplicated for the same active condition.
- Acknowledged and resolved alerts keep audit history.

### Week 12 - Biological Protocol Rules

Build deterministic rules from the operational intelligence framework:

- Cold stress/chilling protocol.
- Heat stress and enthalpy protocol.
- Pathogenic outbreak protocol.
- Hypoxia/ascites protocol.
- Mycotoxin suspicion protocol.

Rules use:

- Batch age.
- Target matrix.
- Feed intake.
- Water intake.
- Mortality rate.
- Weight trend.
- Temperature and humidity when available.
- Seasonal context.

Acceptance:

- High mortality creates a critical alert.
- Heat stress pattern creates an actionable alert.
- Low feed and low water with normal temperature suggests water-line or disease investigation.
- Rules return severity, confidence, probable cause, and recommended action.

### Week 13 - Operational Logs: Water, Litter, Lighting, Biosecurity, Vaccination

Build:

- `health.water_quality_logs`
- `health.litter_assessments`
- `health.lighting_programs`
- `health.biosecurity_log`
- `health.vaccination_events`

Router endpoints:

- `POST /api/v1/health/batches/{batch_id}/water-quality`
- `POST /api/v1/health/batches/{batch_id}/litter`
- `POST /api/v1/health/batches/{batch_id}/lighting`
- `POST /api/v1/health/batches/{batch_id}/biosecurity`
- `GET /api/v1/health/batches/{batch_id}/vaccinations/schedule`
- `POST /api/v1/health/batches/{batch_id}/vaccinations`

Vaccination schedule:

- Day 7: Newcastle + Infectious Bronchitis.
- Day 14: Gumboro dose 1.
- Day 21: Gumboro booster.
- Day 28: Newcastle booster.

Acceptance:

- Vaccination schedule is derived from batch start date.
- Water quality and litter logs can trigger alerts.
- Biosecurity log captures visitors, vehicles, zones, and disinfectant state.

### Week 14 - Emergency Protocols, Telemetry-Ready Design, and Health Completion

Build:

- `health.emergency_events`
- Emergency protocol library.
- Telemetry ingestion interface design.
- Moving average service design for future IoT.
- Router endpoints:
  - `POST /api/v1/health/batches/{batch_id}/emergencies`
  - `GET /api/v1/health/batches/{batch_id}/emergencies`
  - `GET /api/v1/health/protocols`

Emergency protocols:

- Power outage.
- Mass mortality event.
- Market price collapse.
- Feed supply disruption.

Telemetry-ready design:

- Document MQTT topic expectations.
- Prepare table design for future high-volume `telemetry_raw` partitions.
- Do not build full IoT infrastructure in the first 20 weeks unless all core backend work is complete.

Acceptance:

- Emergency events can be declared manually.
- Protocols are surfaced by severity and event type.
- Health phase can raise, acknowledge, and resolve alerts from real batch data.

### Phase 3 Go/No-Go

- Health rules produce alerts from batch records.
- Alert lifecycle works.
- Vaccination schedule works.
- Water, litter, lighting, and biosecurity logs exist.
- Emergency protocols are represented in the API.
- Telemetry is designed but not overbuilt.

---

## Phase 4 - Weeks 15-16: Auth, Farms, Tenant Isolation, and Auditability

### Phase Goal

Make the API multi-tenant and safe. Every request must know which farm it belongs to, and every protected endpoint must reject unauthorized access.

### Week 15 - Users, Farms, OTP, and JWT

Build:

- `auth.users`
- `auth.farms`
- `auth.farm_members`
- `auth.otp_challenges`
- OTP service.
- JWT service.
- Passwordless auth flow using phone number.

Router endpoints:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/request-otp`
- `POST /api/v1/auth/verify-otp`
- `POST /api/v1/auth/refresh-token`
- `GET /api/v1/auth/me`

Rules:

- OTPs expire.
- OTP attempts are rate limited.
- JWT contains user ID and active farm ID.
- Farm membership controls tenant access.

Acceptance:

- Request OTP -> verify OTP -> receive JWT works.
- Wrong OTP attempts are limited.
- Expired OTP fails.
- Token includes enough context for RLS.

### Week 16 - Route Protection, RLS Integration, and Audit Logs

Build:

- Shared auth dependency.
- Current user/farm dependency.
- RLS session context setter.
- `core.audit_logs`
- Protected route enforcement across all modules.
- Production startup checks for unsafe secrets.

Audit log captures:

- Actor user ID.
- Farm ID.
- Action.
- Target resource.
- Correlation ID.
- Timestamp.
- IP/user agent when available.

Acceptance:

- Calling protected endpoints without JWT returns 401.
- Calling another farm's resource returns 403 or not found by policy.
- Database RLS prevents leakage even if a query forgets app-level filtering.
- Audit log records sensitive actions such as payment callback processing, batch close, and alert resolution.

### Phase 4 Go/No-Go

- Auth flow works end to end.
- All module routes that expose tenant data are protected.
- RLS is active for tenant tables.
- Audit logs exist for critical actions.
- Production startup refuses unsafe default secrets.

---

## Phase 5 - Weeks 17-18: Testing Discipline and Architecture Enforcement

### Phase Goal

Prove the system works and prove it stays modular.

This phase turns architectural rules into tests so future edits cannot quietly destroy the design.

### Week 17 - Unit and Service Tests

Build tests for:

- Batch lifecycle transitions.
- Batch target lookup.
- Batch metric calculations.
- Finance P&L.
- Break-even and harvest economics.
- M-Pesa callback idempotency service.
- Health rules.
- Alert lifecycle.
- OTP and JWT services.
- Event bus behavior.
- Outbox writer behavior.

Standards:

- Service tests do not require HTTP.
- Repository tests use PostgreSQL, not SQLite.
- Business logic should be easy to test without booting the full app.

Acceptance:

- Core service tests pass.
- Duplicate M-Pesa callbacks are tested.
- Alert rules are tested with clear fixtures.
- Coverage trend is visible.

### Week 18 - Integration, Slice, and Architecture Tests

Build:

- API slice tests for major routes.
- Integration tests against PostgreSQL.
- RLS tests.
- RBAC tests.
- Soft delete tests.
- Migration ordering tests.
- Import boundary tests.
- Outbox transaction tests.

Architecture checks:

- Modules do not import other modules' repositories.
- Routers do not contain SQL.
- Repositories do not import FastAPI.
- Services do not import routers.
- Cross-module SQL joins are absent.
- Shared package stays pure.

Acceptance:

- `pytest` passes.
- `pytest --cov=app --cov-fail-under=80` passes or the remaining gap is documented with a concrete fix list.
- Architecture tests fail when an intentional boundary violation is introduced locally.

### Phase 5 Go/No-Go

- Unit, slice, integration, and architecture tests exist.
- Business logic has 80%+ coverage.
- RLS and idempotency are tested.
- Boundary enforcement is automated.
- Test suite can run from a clean checkout.

---

## Phase 6 - Weeks 19-20: Deployment, Observability, Documentation, and Demo

### Phase Goal

Package the backend as a credible production-style portfolio project.

The system must be runnable, reviewable, demonstrable, and honest about what is production-ready versus what belongs in the Post-20 Backlog.

### Week 19 - Production Docker and Render Deployment

Build:

- Production Dockerfile.
- Render deployment configuration.
- Managed PostgreSQL setup.
- Production environment variable checklist.
- Startup migration command or documented migration process.
- Health check endpoint for Render.
- Structured production logs.

Production requirements:

- `DEBUG=False`.
- Strong `SECRET_KEY`.
- No `.env` committed.
- Database URL provided by Render.
- CORS restricted to known clients.
- App refuses to boot with default production secrets.

Acceptance:

- App deploys to Render.
- `curl https://<render-url>/health` returns 200.
- Production logs include correlation IDs.
- Swagger loads in production.
- Database schemas exist in production.

### Week 20 - README, Swagger Polish, and Live Demo Flow

Build:

- Complete README.
- Architecture diagram or text diagram.
- Environment variable table.
- Local setup instructions.
- Test instructions.
- Deployment notes.
- API demo script.
- Swagger descriptions and response examples.

README must include:

- What KukuFiti does.
- Why it is a modular monolith.
- How to run locally.
- How to run tests.
- How to deploy.
- Module summary.
- Demo flow.
- Known limitations and Post-20 Backlog.

Live demo flow:

1. Register or authenticate.
2. Create a farm context.
3. Create a batch.
4. Activate the batch.
5. Record daily feed, water, mortality, and weight data.
6. Record feed inventory and expense.
7. Trigger or simulate M-Pesa payment callback.
8. View P&L.
9. Trigger a health alert from abnormal data.
10. Acknowledge the alert.
11. View batch summary.
12. Close the batch.

Acceptance:

- A reviewer can follow the README without private knowledge.
- Swagger shows real endpoints and examples.
- Demo flow exercises auth, batches, finance, and health.
- Final portfolio checklist is complete.

### Phase 6 Go/No-Go

- Public deployment works.
- README is complete.
- Swagger is clean.
- Demo flow works end to end.
- Coverage target is met.
- The project can be explained clearly in an interview.

---

## Public API Surface Target

The exact endpoint list can evolve during implementation, but the final API should expose at least these operational groups.

### System

- `GET /health`
- `GET /docs`

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/request-otp`
- `POST /api/v1/auth/verify-otp`
- `POST /api/v1/auth/refresh-token`
- `GET /api/v1/auth/me`

### Batches

- `POST /api/v1/batches`
- `GET /api/v1/batches`
- `GET /api/v1/batches/{batch_id}`
- `PATCH /api/v1/batches/{batch_id}/status`
- `POST /api/v1/batches/{batch_id}/close`
- `GET /api/v1/batches/{batch_id}/summary`
- `GET /api/v1/batches/{batch_id}/targets/today`
- `GET /api/v1/batches/{batch_id}/performance`
- `POST /api/v1/batches/{batch_id}/daily-logs`
- `GET /api/v1/batches/{batch_id}/daily-logs`
- `POST /api/v1/batches/{batch_id}/mortality`
- `POST /api/v1/batches/{batch_id}/feed`
- `POST /api/v1/batches/{batch_id}/water`
- `POST /api/v1/batches/{batch_id}/weights`

### Finance

- `POST /api/v1/finance/batches/{batch_id}/expenses`
- `POST /api/v1/finance/batches/{batch_id}/income`
- `GET /api/v1/finance/batches/{batch_id}/transactions`
- `GET /api/v1/finance/batches/{batch_id}/pl`
- `POST /api/v1/finance/mpesa/stk-push`
- `POST /api/v1/finance/mpesa/callback`
- `GET /api/v1/finance/mpesa/{checkout_request_id}`
- `POST /api/v1/finance/batches/{batch_id}/feed-inventory`
- `GET /api/v1/finance/batches/{batch_id}/feed-inventory`
- `GET /api/v1/finance/batches/{batch_id}/feed-stock`
- `GET /api/v1/finance/batches/{batch_id}/break-even`
- `GET /api/v1/finance/batches/{batch_id}/harvest-economics`
- `POST /api/v1/finance/batches/{batch_id}/feed-withdrawal/start`

### Health

- `GET /api/v1/health/batches/{batch_id}/alerts`
- `GET /api/v1/health/alerts/{alert_id}`
- `POST /api/v1/health/alerts/{alert_id}/acknowledge`
- `POST /api/v1/health/alerts/{alert_id}/resolve`
- `POST /api/v1/health/batches/{batch_id}/water-quality`
- `POST /api/v1/health/batches/{batch_id}/litter`
- `POST /api/v1/health/batches/{batch_id}/lighting`
- `POST /api/v1/health/batches/{batch_id}/biosecurity`
- `GET /api/v1/health/batches/{batch_id}/vaccinations/schedule`
- `POST /api/v1/health/batches/{batch_id}/vaccinations`
- `POST /api/v1/health/batches/{batch_id}/emergencies`
- `GET /api/v1/health/batches/{batch_id}/emergencies`
- `GET /api/v1/health/protocols`

---

## Data Model Expectations

This is not a final migration spec, but every implementation should account for these storage needs.

| Schema | Table/View | Purpose |
|---|---|---|
| `core` | `outbox_events` | Reliable event handoff after business transactions |
| `core` | `audit_logs` | Sensitive action audit trail |
| `auth` | `users` | Authenticated people |
| `auth` | `farms` | Tenant root |
| `auth` | `farm_members` | User-farm access |
| `auth` | `otp_challenges` | OTP verification |
| `batches` | `batches` | Batch lifecycle |
| `batches` | `batch_status_history` | State transition audit |
| `batches` | `batch_targets` | 42-day biological target matrix |
| `batches` | `pre_placement_checklist` | House preparation before activation |
| `batches` | `farm_location_context` | Climate, altitude, seasonal settings |
| `batches` | `daily_logs` | Daily operational summary |
| `batches` | `mortality_events` | Mortality facts |
| `batches` | `feed_events` | Feed consumption facts |
| `batches` | `water_events` | Water consumption facts |
| `batches` | `weight_samples` | Growth and uniformity facts |
| `finance` | `expenses` | Costs |
| `finance` | `income` | Revenue |
| `finance` | `sales` | Harvest/sale records |
| `finance` | `mpesa_transactions` | Idempotent M-Pesa callback log |
| `finance` | `feed_inventory` | Feed stock, supplier, quality and cost data |
| `health` | `alerts` | Active and historical farm alerts |
| `health` | `rule_evaluations` | Rule execution history |
| `health` | `water_quality_logs` | Water testing |
| `health` | `litter_assessments` | Litter moisture/caking |
| `health` | `lighting_programs` | Light schedule and observations |
| `health` | `biosecurity_log` | Visitor, vehicle, and zone records |
| `health` | `vaccination_events` | Scheduled/completed vaccinations |
| `health` | `emergency_events` | Emergency incidents and resolution |
| `advisory` | `batch_ai_context` | AI-ready recommendation/context records |

---

## Testing and Acceptance Matrix

| Area | Required tests |
|---|---|
| Schema isolation | Module role cannot read another module schema |
| RLS | Farm A cannot read Farm B data |
| Soft deletes | Deleted rows hidden from normal queries but retained |
| Batch lifecycle | Valid and invalid status transitions |
| Batch metrics | FCR, mortality, water ratio, current bird count |
| Target matrix | Correct target lookup by batch age |
| M-Pesa | Duplicate callback does not double-apply effects |
| Finance | P&L, break-even, harvest economics arithmetic |
| Health rules | Expected alerts from known abnormal input patterns |
| Auth | OTP success/failure, JWT protection, expired token rejection |
| Outbox | Event persists in same transaction as business mutation |
| Architecture | No cross-module repository imports or cross-schema joins |
| API slices | Happy path, 4xx validation, auth rejection per major flow |
| Deployment | `/health` works against deployed URL |

---

## Definition of Done

The 20-week build is complete only when every item below is true.

### Backend

- [ ] FastAPI app boots locally.
- [ ] PostgreSQL migrations run from a clean database.
- [ ] Module schemas exist.
- [ ] RBAC and RLS are tested.
- [ ] Soft deletes are implemented for tenant-owned tables.
- [ ] Event bus and outbox patterns are present.
- [ ] All modules follow router/service/repository boundaries.
- [ ] No cross-module SQL joins exist.

### Product Features

- [ ] Auth flow works.
- [ ] Batch lifecycle works.
- [ ] Daily operational records work.
- [ ] Batch summary calculates useful metrics.
- [ ] Finance records income and expenses.
- [ ] M-Pesa callback idempotency works.
- [ ] Feed inventory and harvest economics work.
- [ ] Health rules produce alerts.
- [ ] Alert lifecycle works.
- [ ] Vaccination schedule works.
- [ ] Emergency protocols are represented.

### Quality

- [ ] `pytest` passes.
- [ ] `pytest --cov=app --cov-fail-under=80` passes.
- [ ] Unit tests cover service logic.
- [ ] Slice tests cover major routes.
- [ ] Architecture tests enforce boundaries.
- [ ] Swagger docs load cleanly.

### Deployment and Portfolio

- [ ] App is deployed to Render.
- [ ] Public `/health` endpoint returns 200.
- [ ] Production secrets are not defaults.
- [ ] README is complete.
- [ ] Demo flow works end to end.
- [ ] Post-20 Backlog is documented honestly.

---

## Post-20 Backlog

These are important, but they should not distract from completing the core 20-week backend.

### Scale Layer

- PgBouncer between FastAPI/Celery and PostgreSQL.
- Redis caching for read-heavy reference data and dashboard summaries.
- Load testing for 10,000+ active farmers.
- Gunicorn/Uvicorn worker tuning.
- Connection pool monitoring.

### Mobile and Offline Sync

- Flutter WorkManager background sync.
- Shorter 3G-friendly timeout strategy.
- Offline outbox conflict handling.
- Push notification integration through FCM.

### Advanced AI and ML

- pgvector knowledge/context store.
- LangGraph advisory workflows.
- Disease risk prediction.
- Harvest date prediction.
- Feed brand performance index.
- Inter-batch machine learning from anonymized historical data.

### IoT and Telemetry

- MQTT broker integration.
- Partitioned `telemetry_raw` table.
- 15-minute moving average processors.
- Sensor failover protocol.
- Actuation logs for fans, lights, fogging, and water systems.

### Extraction Readiness

- Module contract hardening.
- Anti-corruption layers.
- Service-to-service auth design.
- Strangler-fig extraction plan.
- Dedicated workers for high-volume advisory or telemetry modules.

---

## The Interview Explanation

KukuFiti is a FastAPI modular monolith for broiler farm intelligence. It uses PostgreSQL schema isolation, raw SQL, RLS, soft deletes, idempotent M-Pesa callbacks, event-driven module communication, and deterministic health rules to turn daily farm records into operational and financial insight.

It is intentionally not built as microservices in the first 20 weeks. The design keeps one deployable service while enforcing module boundaries so future extraction is possible when scale or team structure demands it.

The first version proves the core business system: auth, batches, daily operations, finance, M-Pesa, alerts, tests, deployment, and documentation. Advanced AI, IoT, caching, and microservice extraction come after the foundation is stable.

---

## Appendix A - Code-Bearing Modular Monolith Guide

This appendix is the implementation companion for the roadmap. It keeps the production code shape explicit without turning every week into a copy-paste exercise.

### A.1 Project Layout

```text
kukufiti-api/
  app/
    main.py
    core/
      config.py
      database.py
      events.py
      event_bus.py
      outbox.py
      tenancy.py
      security.py
      middleware.py
      exceptions.py
      logging.py
    shared/
      base_schema.py
      types.py
    modules/
      auth/
      batches/
      finance/
      health/
      advisory/
  migrations/
    core/
    auth/
    batches/
    finance/
    health/
    advisory/
  tests/
    unit/
    architecture/
````

### A.2 Core Config

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    batches_db_url: str
    finance_db_url: str
    health_db_url: str
    auth_db_url: str
    advisory_db_url: str | None = None

    app_name: str = "kukufiti-api"
    app_version: str = "0.2.0"
    debug: bool = False
    environment: str = "local"
    log_level: str = "info"

    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
```

### A.3 Database Pool and Tenant Context

```python
async def create_pool(dsn: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=2,
        max_size=10,
        statement_cache_size=0,
        command_timeout=30,
    )


async def set_tenant_context(conn: asyncpg.Connection, farm_id: UUID) -> None:
    await conn.execute("SELECT set_config('app.current_farm_id', $1, true)", str(farm_id))
```

### A.4 Event Bus and Outbox

```python
@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    aggregate_id: UUID
    farm_id: UUID | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    def subscribe(self, event_type: str, handler: EventHandler) -> None: ...
    async def publish(self, event: DomainEvent) -> None: ...


async def write_outbox_event(conn: asyncpg.Connection, event: DomainEvent) -> UUID:
    return await conn.fetchval(
        """
        INSERT INTO core.outbox_events
            (event_type, aggregate_id, farm_id, payload, occurred_at)
        VALUES ($1, $2, $3, $4::jsonb, $5)
        RETURNING id
        """,
        event.event_type,
        event.aggregate_id,
        event.farm_id,
        json.dumps(event.payload),
        event.occurred_at,
    )
```

### A.5 Repository Rule

Repositories own SQL. Routers do not contain SQL. Services do not import FastAPI request objects.

```python
class BatchRepository:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def find_by_id(self, batch_id: UUID, farm_id: UUID) -> Batch | None:
        row = await self._conn.fetchrow(
            """
            SELECT *
            FROM batches.batches
            WHERE id = $1 AND farm_id = $2 AND deleted_at IS NULL
            """,
            batch_id,
            farm_id,
        )
        return Batch.from_row(row) if row else None
```

### A.6 M-Pesa Idempotency Pattern

```python
async def record_mpesa_callback(self, payload: dict[str, Any]) -> MpesaCallbackResult:
    checkout_request_id = payload["Body"]["stkCallback"]["CheckoutRequestID"]

    async with self._conn.transaction():
        inserted = await self._repo.insert_callback_once(checkout_request_id, payload)
        if not inserted:
            return MpesaCallbackResult(status="duplicate", checkout_request_id=checkout_request_id)

        await self._repo.apply_success_or_failure(checkout_request_id, payload)
        await write_outbox_event(self._conn, DomainEvent("PaymentReceived", ...))
```

### A.7 Health Rule Shape

```python
@dataclass(frozen=True)
class RuleResult:
    rule_code: str
    severity: str
    confidence: Decimal
    title: str
    recommended_action: str


def evaluate_heat_stress(snapshot: BatchHealthSnapshot) -> RuleResult | None:
    if (
        snapshot.temperature_c is not None
        and snapshot.target_temperature_c is not None
        and snapshot.temperature_c > snapshot.target_temperature_c + Decimal("2.0")
        and snapshot.water_to_feed_ratio is not None
        and snapshot.water_to_feed_ratio > Decimal("2.0")
    ):
        return RuleResult(
            rule_code="HEAT_STRESS",
            severity="critical",
            confidence=Decimal("0.95"),
            title="Heat stress pattern detected",
            recommended_action="Increase ventilation, inspect drinkers, and add electrolytes.",
        )
    return None
```

### A.8 Architecture Tests

```python
def test_modules_do_not_import_other_module_repositories():
    for path in Path("app/modules").glob("*/**/*.py"):
        source = path.read_text()
        module = path.parts[2]
        forbidden = [
            f"app.modules.{other}.repository"
            for other in MODULES
            if other != module
        ]
        assert not any(pattern in source for pattern in forbidden), path
```

### A.9 Do Not Use

```python
# DO NOT USE: finance must not query batches tables directly.
await conn.fetch("SELECT * FROM finance.expenses e JOIN batches.batches b ON ...")

# DO NOT USE: routers must not contain business SQL.
@router.post("/x")
async def route(conn=Depends(get_conn)):
    await conn.execute("UPDATE ...")
```

            "breed": "Ross",
            "quantity": 100,
            "start_date": "2026-05-01",
        })
        assert response.status_code == 422

    async def test_returns_404_for_nonexistent_batch(self, client):
        response = await client.get(f"/api/v1/batches/{uuid4()}")
        assert response.status_code == 404

    async def test_status_transition_active_to_closed(self, client):
        # Create
        create = await client.post("/api/v1/batches/", json={
            "batch_name": "Close Test", "breed": "Ross 308",
            "quantity": 100, "start_date": "2026-04-01",
        })
        batch_id = create.json()["id"]

        # Close
        close = await client.post(f"/api/v1/batches/{batch_id}/close")
        assert close.status_code == 200
        assert close.json()["status"] == "closed"

    async def test_invalid_transition_returns_400(self, client):
        create = await client.post("/api/v1/batches/", json={
            "batch_name": "Transition Test", "breed": "Ross 308",
            "quantity": 100, "start_date": "2026-04-01",
        })
        batch_id = create.json()["id"]

        # Try to go active → archived (skipping closed)
        response = await client.patch(
            f"/api/v1/batches/{batch_id}/status",
            json={"status": "archived"},
        )
        assert response.status_code == 400

````

### Phase 5 Deliverable

`pytest --cov=app` shows ≥80% on all `service.py` files. All slice tests pass. Integration tests pass against Testcontainers PostgreSQL.

### Go/No-Go Checkpoint

```bash
pytest -m unit           # all pass, <5s
pytest -m integration    # all pass, <60s
pytest -m slice          # all pass
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
````

All four commands must pass without skipped tests.

---

## Phase 6 — Weeks 19–20: Deployment + Portfolio Packaging

### Chain-of-Thought

**What Fredrick already knows:** Complete working system with tests. Docker Compose for local dev.

**What this phase teaches:** Render deployment with managed PostgreSQL, environment variable management in production, Dockerfile optimisation, README writing, Swagger documentation completeness, portfolio presentation.

**Track C sync:** This phase is the cumulative product of all 20 weeks. No specific Track C sync — it produces the portfolio item that makes the roadmap's employment target credible.

**Vibe Coding workflow:** Use Claude to review your README before publishing. Ask: "Does this README allow a hiring manager to run this project locally in under 10 minutes?" Fix every gap it identifies. The README is a product, not an afterthought.

**Go/No-Go:** `curl https://kukufiti-api.onrender.com/health` returns `200`. All endpoints documented in Swagger. README has setup instructions, demo flow, and architecture diagram. `pytest --cov-fail-under=80` still passes.

**Junior mistake:** Deploying with `DEBUG=True` and no `SECRET_KEY` set in production environment. Prevention: write a startup check that refuses to start if `SECRET_KEY` is the default value and `DEBUG=True` in a non-local environment.

---

### Week 19 — Production Dockerfile and Render Deploy

```dockerfile
# Dockerfile
FROM python:3.12.2-slim-bookworm AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12.2-slim-bookworm AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 curl \
    && rm -rf /var/lib/apt/lists/*
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=appuser:appgroup . .
USER appuser
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Render deployment steps:**

1. Push to GitHub: `git push origin main`
2. Create Render account (free tier — no payment required for this stack)
3. New Web Service → connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add PostgreSQL: New PostgreSQL → free tier → copy internal connection string
7. Set all environment variables in Render dashboard
8. Deploy

### Week 20 — README, Swagger Polish, Demo Flow

```markdown
# kukufiti-api

Broiler farm management API for Kenyan smallholder farmers.
Track batches, record M-Pesa transactions, and receive disease alerts.

**Live API:** https://kukufiti-api.onrender.com
**Swagger docs:** https://kukufiti-api.onrender.com/docs

## Architecture

Modular monolith — schema-per-module PostgreSQL isolation.
Raw SQL via asyncpg. No ORM.

Modules:

- **batches** — broiler batch lifecycle, FCR calculation
- **finance** — KES income/expense, M-Pesa Daraja STK push
- **health** — daily health logs, threshold-based disease alerts
- **auth** — OTP via Africa's Talking SMS, JWT tokens

## Quick Start (Local)

\`\`\`bash
git clone https://github.com/fredricknyangau/kukufiti-api
cd kukufiti-api
cp .env.example .env # fill in your values
docker compose up -d
curl http://localhost:8000/health
\`\`\`

## Demo Flow (Full System)

1. Register: POST /api/v1/auth/register
2. Request OTP: POST /api/v1/auth/request-otp
3. Verify OTP → get JWT: POST /api/v1/auth/verify-otp
4. Create batch: POST /api/v1/batches/
5. Log health data: POST /api/v1/health/logs
6. Initiate M-Pesa payment: POST /api/v1/finance/mpesa/stk-push
7. View P&L: GET /api/v1/finance/batches/{id}/pl
8. View batch summary: GET /api/v1/batches/{id}/summary
9. Acknowledge alert: POST /api/v1/health/alerts/{id}/acknowledge

## Environment Variables

See .env.example for all required variables.

## Running Tests

\`\`\`bash
source .venv/bin/activate
pytest --cov=app --cov-report=term-missing
\`\`\`
```

---

## Definition of Done — Portfolio Checklist

This is the binary checklist Fredrick presents to a Nairobi hiring manager. Every item is either done or not done. No partial credit.

---

### Endpoints (Minimum 20 operational)

| Module    | Endpoints                                                                        |
| --------- | -------------------------------------------------------------------------------- |
| Auth      | register, request-otp, verify-otp, refresh-token, me (5)                         |
| Batches   | create, list, get, update-status, close, summary (6)                             |
| Finance   | record-income, record-expense, get-pl, list-transactions, stk-push, callback (6) |
| Health    | log-health, get-history, get-alerts, get-alert, acknowledge-alert (5)            |
| System    | health, docs (2)                                                                 |
| **Total** | **24 endpoints**                                                                 |

---

### Test Coverage

- [ ] `pytest --cov=app --cov-fail-under=80` passes
- [ ] All `service.py` files ≥80% coverage
- [ ] All slice tests cover happy path, 4xx errors, and auth rejection per endpoint
- [ ] No SQLite — all tests run against real PostgreSQL via Testcontainers

---

### Deployment

- [ ] `curl https://kukufiti-api.onrender.com/health` → `200 {"status":"healthy"}`
- [ ] Render dashboard shows no crash restarts in last 24 hours
- [ ] `DEBUG=False` in production environment
- [ ] `SECRET_KEY` is a real random secret (not the example value)
- [ ] All module database schemas exist on the production Postgres instance

---

### Swagger Documentation

- [ ] `/docs` loads without errors
- [ ] Every endpoint has a description string
- [ ] Every request body has field descriptions
- [ ] Response schemas are defined for every endpoint
- [ ] Tags group endpoints by module
- [ ] Auth endpoints show the OAuth2 lock icon

---

### README Sections

- [ ] Project description (2 sentences — what it is, who it is for)
- [ ] Architecture overview (modules, schema isolation, raw SQL)
- [ ] Quick start (clone → .env → docker compose up → /health in under 10 minutes)
- [ ] Full demo flow (9-step sequence covering all modules)
- [ ] Environment variables table (name, description, example value)
- [ ] Running tests locally
- [ ] Live URL

---

### The One Live Demo Flow

This is the sequence you run in front of a hiring manager, live, against the production URL:

```
1. POST /auth/register        → 201, user created
2. POST /auth/request-otp     → 200, SMS sent (show Twilio/AT log)
3. POST /auth/verify-otp      → 200, JWT returned
4. POST /batches/             → 201, batch created with ID
5. POST /health/logs          → 201, health logged (mortality: 20 birds)
6. GET  /health/batches/{id}/alerts  → 200, critical alert triggered automatically
7. POST /finance/mpesa/stk-push     → 202, CheckoutRequestID returned
8. GET  /finance/batches/{id}/pl    → 200, P&L in KES
9. GET  /batches/{id}/summary       → 200, FCR and mortality rate calculated
```

Nine requests. Four modules. One live production URL. JWT auth on every request after step 3. This is a working system, not a tutorial.

---

### The Differentiator Statement

When the hiring manager asks "tell me about this project", the answer is:

> "kukufiti-api is a broiler farm management backend for Kenyan smallholder farmers. It tracks batch performance, handles M-Pesa Daraja payments natively, and fires automatic disease alerts when mortality or feed consumption crosses clinical thresholds. The architecture is a modular monolith — four PostgreSQL schemas with role-level isolation, raw SQL via asyncpg, no ORM. I built it over 20 weeks as my primary learning project. It has 24 endpoints, 80% test coverage on business logic, and it's deployed on Render. The M-Pesa integration and agritech domain are specific to the Kenyan market — this is not a tutorial clone."

That answer, backed by a live URL and working Swagger docs, is what gets you the interview to the next round.
