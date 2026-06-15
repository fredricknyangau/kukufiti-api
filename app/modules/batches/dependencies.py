"""FastAPI dependency injection functions for the batches module.

DEPENDENCY INJECTION IN FASTAPI
--------------------------------
FastAPI's Depends() system is a lightweight inversion-of-control container.
Instead of route handlers constructing their own database connections and
service objects (which would make them hard to test and tightly coupled to
infrastructure), they declare what they need as function parameters with
`Annotated[Type, Depends(factory_function)]`. FastAPI calls the factory
functions automatically on each request and injects the results.

This file is the *composition root* for the batches module: the only place
that knows how to wire a database connection → repository → service. Route
handlers only see BatchService and do not need to know about asyncpg or pools.

REQUEST LIFETIME
----------------
Each HTTP request gets its own database connection (acquired from the pool)
and therefore its own BatchRepository and BatchService instances. This is the
correct scope for database transactions: a connection must not be shared across
concurrent requests because transaction state would leak between them.
"""
from collections.abc import AsyncGenerator

import asyncpg
from fastapi import Depends, Request

from .repository import BatchRepository
from .service import BatchService


async def get_batches_connection(
    request: Request,
) -> AsyncGenerator[asyncpg.Connection, None]:
    """Acquire a database connection from the batches pool for this request.

    This is an async generator dependency. FastAPI recognises the `yield`
    pattern and:
      1. Calls the function, running code up to `yield`.
      2. Injects the yielded value into the dependent function.
      3. After the route handler finishes (including error paths), resumes
         the generator to run any cleanup after `yield`.

    The `async with pool.acquire()` context manager guarantees the connection
    is returned to the pool even if the route handler raises an exception. This
    prevents connection leaks that would eventually exhaust the pool and make
    the service unable to accept new requests.

    The pool itself is stored on app.state.batches_pool, which is created at
    startup in app/main.py. Accessing it via `request.app.state` avoids a
    module-level import of `app` (which would create a circular import:
    main.py → batches/router.py → batches/dependencies.py → main.py).
    """
    async with request.app.state.batches_pool.acquire() as conn:
        yield conn


# Pre-build the Depends object once so FastAPI does not create a new
# Depends wrapper on every request. This is a minor optimisation that also
# makes the dependency declaration in get_batch_service slightly cleaner.
get_batch_service_dependency = Depends(get_batches_connection)


async def get_batch_service(
    conn: asyncpg.Connection = get_batch_service_dependency,
) -> BatchService:
    """Build and return a BatchService wired to the request's DB connection.

    FastAPI calls this function automatically when a route handler declares
    `service: BatchServiceDep` (defined in router.py). The injected `conn`
    comes from get_batches_connection above.

    The composition order is:
        connection  (asyncpg.Connection, 1 per request)
            └─ BatchRepository  (SQL layer, wraps connection)
                └─ BatchService (business logic, wraps repository)
                    └─ route handler  (HTTP layer, calls service methods)

    This function returns a plain BatchService instance — not a generator —
    because there is no cleanup to perform after the service is used. The
    connection cleanup is handled by get_batches_connection.
    """
    repo = BatchRepository(conn)
    return BatchService(repository=repo)
