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