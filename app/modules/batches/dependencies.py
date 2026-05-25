from collections.abc import AsyncGenerator

import asyncpg
from fastapi import Depends, Request

from .repository import BatchRepository
from .service import BatchService


# router.py imports get_batch_service.
# FastAPI uses these dependency functions to wire requests to service/repository objects
# without manually instantiating them in route handlers. This keeps handlers clean and
# focused on request/response logic.
async def get_batches_connection(
    request: Request,
) -> AsyncGenerator[asyncpg.Connection, None]:
    # main.py creates app.state.batches_pool during application startup.
    # Each request gets one acquired connection for batch operations.
    async with request.app.state.batches_pool.acquire() as conn:
        yield conn


get_batch_service_dependency = Depends(get_batches_connection)


async def get_batch_service(
    conn: asyncpg.Connection = get_batch_service_dependency,
) -> BatchService:
    # Route handlers depend on BatchService. FastAPI calls this function automatically,
    # then injects the returned service into the handler parameter.
    repo = BatchRepository(conn)
    return BatchService(repository=repo)
