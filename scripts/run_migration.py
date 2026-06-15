"""
Migration runner for kukufiti-api.

ARCHITECTURE
------------
All migrations run under the DATABASE_URL (superuser) so they can issue DDL
(CREATE TABLE, CREATE INDEX, ALTER TABLE, etc.) and grant privileges across
schemas. Module-specific application roles (batches_app, finance_app, etc.)
have DML privileges only and MUST NOT be used for migrations.

TRACKING
--------
Applied migrations are recorded in public.schema_migrations. The tracking table
lives in the `public` schema (not in any module schema) so the superuser always
has access regardless of which module is being migrated. Each row records:
  - module:    which module the migration belongs to (e.g. "batches").
  - filename:  the SQL file name (e.g. "001_create_batches_tables.sql").
  - applied_at: when the migration was applied (UTC timestamp).

Re-running a migration file that has already been recorded is safe: the
runner prints a skip message and exits with code 0. This makes it safe to
include `run_migration --all` in a Docker entrypoint or CI step without
worrying about double-application.

IDEMPOTENCY IN SQL
------------------
Migration SQL files should use `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF
NOT EXISTS`, and similar guards so that re-running a file (e.g. after a
partial failure) does not raise errors. The tracking table prevents re-runs
under normal conditions, but defensive SQL is a second safety layer.

Usage:
    # Run ALL pending migrations across all modules (Docker / CI mode):
    python -m scripts.run_migration --all

    # Run a single specific migration:
    python -m scripts.run_migration <module> <migration_id>

    # Examples:
    python -m scripts.run_migration batches 001
    python -m scripts.run_migration finance 001
"""

import asyncio
import sys
from pathlib import Path

import asyncpg

from app.core.config import settings

# ---------------------------------------------------------------------------
# Module registry
# ---------------------------------------------------------------------------
# Canonical list of modules. Order matters for any future cross-module foreign
# keys: a module that references another must be migrated after its dependency.
# For example, finance.transactions references batches.batches — so "batches"
# must appear before "finance".
MODULES = ["batches", "finance", "health", "auth"]

# Resolve the project root as the parent of the `scripts/` directory.
# Using __file__ makes the script location-independent — it works whether
# run from the project root (`python -m scripts.run_migration`) or from any
# other working directory.
BASE_DIR = Path(__file__).resolve().parents[1]
MIGRATIONS_DIR = BASE_DIR / "migrations"

# ---------------------------------------------------------------------------
# Tracking table DDL
# ---------------------------------------------------------------------------
# The tracking table is created in the `public` schema, which every PostgreSQL
# role can access. This avoids the chicken-and-egg problem of needing to
# create a module schema before tracking migrations for that module.
# The UNIQUE constraint on (module, filename) prevents duplicate records and
# is the basis of the idempotency check in _is_applied.
_TRACKING_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public.schema_migrations (
    id         SERIAL      PRIMARY KEY,
    module     TEXT        NOT NULL,
    filename   TEXT        NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (module, filename)
);
"""


async def _ensure_tracking_table(conn: asyncpg.Connection) -> None:
    """Create the schema_migrations tracking table if it does not exist.

    Uses `CREATE TABLE IF NOT EXISTS` so this function is safe to call on
    every runner invocation without checking first. PostgreSQL performs the
    existence check atomically, so concurrent runner invocations (e.g. in a
    multi-replica deployment) cannot create the table twice.

    Must be called before _is_applied or _record_migration to guarantee the
    table exists when those functions query it.
    """
    await conn.execute(_TRACKING_TABLE_SQL)


async def _is_applied(conn: asyncpg.Connection, module: str, filename: str) -> bool:
    """Return True if the migration file has already been applied.

    Queries the UNIQUE (module, filename) index — a fast point lookup.
    This is the idempotency gate: if True, _apply_file skips the migration
    entirely, so re-running the runner is always safe.

    The check is NOT inside a transaction lock, which means two concurrent
    runners could both see `is_applied=False` for the same file and both try
    to apply it. The UNIQUE constraint on schema_migrations ensures only one
    INSERT succeeds; the other gets a unique-violation error. For robustness,
    production deployments should ensure only one runner executes at a time
    (e.g. a Kubernetes Job with parallelism=1).
    """
    row = await conn.fetchrow(
        "SELECT 1 FROM public.schema_migrations WHERE module = $1 AND filename = $2",
        module,
        filename,
    )
    return row is not None


async def _record_migration(conn: asyncpg.Connection, module: str, filename: str) -> None:
    """Insert a record into schema_migrations to mark the migration as applied.

    Always called INSIDE the transaction in _apply_file, AFTER the migration
    SQL has been executed. This ordering is critical: if the migration SQL
    fails and the transaction rolls back, no tracking record is inserted, so
    the migration will be retried on the next run. If the INSERT were done
    first and the migration SQL failed, the file would be permanently skipped
    even though it was never actually applied.
    """
    await conn.execute(
        "INSERT INTO public.schema_migrations (module, filename) VALUES ($1, $2)",
        module,
        filename,
    )


# ---------------------------------------------------------------------------
# Core: run one migration file against an open connection
# ---------------------------------------------------------------------------
async def _apply_file(
    conn: asyncpg.Connection,
    module: str,
    migration_file: Path,
) -> None:
    """Read and execute a single SQL migration file, then record it as applied.

    TRANSACTION WRAPPING
    The migration SQL and the tracking INSERT are wrapped in a single database
    transaction. This guarantees atomicity: either both succeed (migration is
    applied and recorded) or both fail (migration is not applied and not
    recorded). Without the transaction, a crash between `conn.execute(sql)` and
    `_record_migration(...)` would leave the database partially migrated and
    the tracking table out of sync — subsequent runs would skip the file
    because _is_applied returns False (no record), but the DDL may have
    partially succeeded.

    NOTE: `CREATE INDEX CONCURRENTLY` cannot run inside a transaction. Do not
    use it in migration files if you need the transactional safety guarantee.
    Use `CREATE INDEX` (non-concurrent) in migrations instead, and run
    concurrent index builds manually during maintenance windows if needed.

    Args:
        conn:           An open asyncpg connection using the superuser DSN.
        module:         The module name (e.g. "batches") for logging and tracking.
        migration_file: Path to the .sql file to execute.
    """
    filename = migration_file.name

    if await _is_applied(conn, module, filename):
        print(f"  [{module}] SKIP  {filename} — already applied")
        return

    print(f"  [{module}] APPLY {filename} ...")
    sql = migration_file.read_text(encoding="utf-8")

    # Wrap the migration + tracking insert in one transaction so a partial
    # migration failure never leaves the DB half-migrated and untracked.
    async with conn.transaction():
        await conn.execute(sql)
        await _record_migration(conn, module, filename)

    print(f"  [{module}] OK    {filename}")


# ---------------------------------------------------------------------------
# Public: run every pending migration across all modules
# ---------------------------------------------------------------------------
async def run_all() -> None:
    """Apply every pending migration for every module in MODULES order.

    Iterates through modules in the order defined in MODULES (important when
    cross-module FK dependencies exist). For each module, it globs all *.sql
    files in `migrations/<module>/` and applies them in sorted (ascending)
    order. The numeric prefix convention (001_, 002_, …) ensures migrations
    run in the correct sequence.

    Modules without a migrations directory or without any .sql files are
    silently skipped with an informational message — this is not an error
    because new modules are added incrementally.

    A single superuser connection is reused for all modules. This avoids the
    overhead of reconnecting for each module and ensures all migrations run
    within the same session (useful if a migration sets session-level config).
    """
    print("Running all pending migrations...")
    conn = await asyncpg.connect(settings.database_url)
    try:
        await _ensure_tracking_table(conn)

        for module in MODULES:
            module_dir = MIGRATIONS_DIR / module
            if not module_dir.exists():
                print(f"  [{module}] No migrations directory — skipping")
                continue

            # Sort ensures 001_... runs before 002_..., regardless of
            # filesystem ordering (which may differ between OS/filesystems).
            sql_files = sorted(module_dir.glob("*.sql"))
            if not sql_files:
                print(f"  [{module}] No SQL files found — skipping")
                continue

            for migration_file in sql_files:
                await _apply_file(conn, module, migration_file)

        print("Migration run complete.")
    finally:
        # Always close the connection, even if a migration raises an exception.
        # asyncpg.Connection.close() is a coroutine; the finally block runs in
        # the asyncio event loop, so `await` is safe here.
        await conn.close()


# ---------------------------------------------------------------------------
# Public: run a single migration identified by module + numeric prefix
# ---------------------------------------------------------------------------
async def run_one(module: str, migration_id: str) -> None:
    """Apply a single migration file identified by module name and numeric prefix.

    Args:
        module:       One of the values in MODULES (e.g. "batches").
        migration_id: The numeric prefix of the filename (e.g. "001").
                      Matched with a glob pattern: "001*.sql" matches
                      "001_create_batches_tables.sql".

    The glob pattern allows the descriptive part of the filename to change
    without breaking the CLI command. If multiple files match the pattern
    (which should not happen with well-named migrations), the alphabetically
    first match is used.

    Exits with code 1 if the module is unknown or no matching file is found,
    so the caller (Docker, CI script) can detect the error without parsing
    stdout.
    """
    if module not in MODULES:
        print(f"Unknown module: {module!r}. Valid modules: {MODULES}")
        sys.exit(1)

    pattern = f"{migration_id}*.sql"
    files = list((MIGRATIONS_DIR / module).glob(pattern))

    if not files:
        print(f"No migration file found matching migrations/{module}/{pattern}")
        sys.exit(1)

    # Take the first sorted match. Sorting is defensive; there should only
    # ever be one file matching a given numeric prefix.
    migration_file = sorted(files)[0]

    conn = await asyncpg.connect(settings.database_url)
    try:
        await _ensure_tracking_table(conn)
        await _apply_file(conn, module, migration_file)
    finally:
        await conn.close()


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    args = sys.argv[1:]

    # No arguments or "--all": run all pending migrations across all modules.
    # The "--all" flag is explicit for clarity in CI scripts and Dockerfiles:
    #     CMD ["python", "-m", "scripts.run_migration", "--all"]
    if not args or args[0] == "--all":
        asyncio.run(run_all())
    # Two arguments: module name + migration ID prefix → single migration mode.
    elif len(args) == 2:
        module_arg, migration_id_arg = args
        asyncio.run(run_one(module_arg, migration_id_arg))
    else:
        # Any other argument combination is invalid — print the module docstring
        # (which contains the usage examples) and exit with a non-zero code.
        print(__doc__)
        sys.exit(1)
