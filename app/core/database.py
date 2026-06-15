# asyncpg connection-pool creation and lifecycle helpers.
#
# ARCHITECTURE — why one pool per module, not one shared pool
# -----------------------------------------------------------
# Each module (batches, finance, health, auth) connects to PostgreSQL using
# its own restricted database role (e.g. batches_app). Those roles have DML
# privileges only on their own schema, enforcing isolation at the network
# layer: a bug in the finance module literally cannot query the auth schema
# because the database will reject the connection.
#
# At startup (app/main.py lifespan), `create_pool` is called once per module
# and the resulting Pool is stored on `app.state.<module>_pool`. Each module's
# dependencies.py acquires a connection from its own pool for every request.
#
# DO NOT add a generic `get_db_connection` here. A shared connection helper
# would couple all modules to a single role and undermine the isolation model.
# Every module must acquire from its own pool; see, for example,
# app/modules/batches/dependencies.py → get_batches_connection.

from asyncpg import Pool


async def create_pool(dsn: str) -> Pool:
    """Create and return an asyncpg connection pool for the given DSN.

    Called once per module during application startup. The returned Pool
    is stored on app.state and reused for the lifetime of the process.
    asyncpg manages connection health internally: it reconnects broken
    connections automatically so callers do not need retry logic.

    Args:
        dsn: A libpq-compatible PostgreSQL connection string, e.g.
             postgresql://user:pass@host:5432/dbname
             Read from module-specific env vars (batches_db_url, etc.)
             defined in app/core/config.py.
    """
    import asyncpg
    return await asyncpg.create_pool(
        dsn=dsn,
        # Keep 2 connections alive even when the service is idle.
        # This prevents the first request after a quiet period from
        # paying the full TCP + TLS + PostgreSQL auth handshake cost.
        min_size=2,
        # Cap the pool at 10 connections per module. With 4 modules that
        # is a maximum of 40 connections to PostgreSQL. Tune this value
        # according to PostgreSQL's max_connections setting and the number
        # of API replicas. Exceeding max_connections causes connection
        # errors under load.
        max_size=10,
        # asyncpg caches prepared statements by default using the connection
        # as the cache key. PgBouncer in transaction-pooling mode reassigns
        # connections between transactions, so a cached statement ID from
        # connection A may be sent on connection B — causing "prepared
        # statement does not exist" errors. Disabling the cache makes
        # asyncpg safe to use behind PgBouncer without any code changes.
        statement_cache_size=0,
        # Abort any query that takes longer than 30 seconds. This protects
        # against runaway queries holding a connection (and potentially a
        # lock) for an unbounded time, which would starve other requests.
        # Adjust the value for operations known to be legitimately slow
        # (e.g. bulk exports) or set it per-connection using SET statement_timeout.
        command_timeout=30,
    )
