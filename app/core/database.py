# asyncpg pool, connection lifecycle
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import asyncpg
from fastapi import Request


async def create_pool(dsn: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=dsn,
        min_size=2,  # minimum connections kept alive at idle
        max_size=10,  # maximum connections in pool
        statement_cache_size=0,  # required when using PgBouncer later
        command_timeout=30,  # kill any query running longer than 30 seconds
    )


@asynccontextmanager
async def get_connection(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        yield conn


# FastAPI dependency — yields a connection from the request-scoped pool.
# Return type is AsyncGenerator because `yield` makes this an async generator
# function, not a coroutine. FastAPI's Depends() handles the generator protocol.
async def get_db_connection(
    request: Request,
) -> AsyncGenerator[asyncpg.Connection, None]:
    async with request.app.state.batches_pool.acquire() as conn:
        yield conn
