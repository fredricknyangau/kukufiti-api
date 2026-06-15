"""FastAPI application factory and process-lifetime manager for kukufiti-api.

This module is the single entry point that:
  1. Defines the asynccontextmanager lifespan that opens and closes all
     database connection pools when the process starts and stops.
  2. Creates the FastAPI app instance with its OpenAPI metadata.
  3. Mounts all module routers under their version prefix.
  4. Exposes the /health endpoint used by load balancers and orchestrators.

Uvicorn is told to run `app.main:app`. Everything else is wired from here.
"""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import create_pool
from app.core.exceptions import KukuFitiError
from app.core.logging import configure_logging
from app.modules.batches.router import router as batches_router
from app.modules.finance.router import router as finance_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and graceful shutdown.

    FastAPI calls this asynccontextmanager exactly once per process lifetime:
      - Everything before `yield` runs at startup.
      - Everything after `yield` runs at shutdown (normal exit or SIGTERM).

    WHY asynccontextmanager instead of on_event("startup")?
    FastAPI deprecated on_event in favour of the lifespan pattern because it
    allows startup/shutdown logic to share local variables (like the pools here)
    and makes error handling during startup cleaner — if any `await create_pool`
    call raises, the exception propagates before `yield` and FastAPI cancels the
    startup, preventing the app from serving requests with broken state.

    WHY store pools on app.state?
    FastAPI/Starlette's app.state is a simple namespace object that lives for
    the duration of the process. Storing pools there (rather than as module-
    level globals) means:
      - Each test can create a fresh `app` instance with its own pools.
      - The pools are accessible to dependency functions via the `request`
        object (request.app.state.<module>_pool) without circular imports.
    """
    configure_logging(settings.log_level)
    logger.info("kukufiti-api starting up")

    # Create one pool per module — each connects as its own restricted DB role,
    # enforcing schema-level isolation at the network layer. A bug in the
    # batches module that tries to query finance tables will be rejected by
    # PostgreSQL because batches_app has no privileges on the finance schema.
    # See app/core/database.py and app/core/config.py for details.
    app.state.batches_pool = await create_pool(settings.batches_db_url)
    app.state.finance_pool = await create_pool(settings.finance_db_url)
    app.state.health_pool  = await create_pool(settings.health_db_url)
    app.state.auth_pool    = await create_pool(settings.auth_db_url)

    logger.info("All connection pools ready")
    yield

    # Graceful shutdown: close every pool before the process exits.
    # asyncpg.Pool.close() waits for in-flight queries on acquired connections
    # to finish before closing the underlying TCP connections. This prevents
    # "connection closed" errors for requests that are still being processed
    # when a SIGTERM arrives (e.g. during a rolling Kubernetes deployment).
    # The order mirrors startup so log output is symmetric and easy to follow.
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
    # docs_url and redoc_url control where the interactive API documentation
    # is served. The README and any external references use /docs and /redoc,
    # so these values must stay aligned. A previous version used /api/docs
    # which broke the documented URLs (MISMATCH-2 fix).
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount the batches router. The prefix "/api/v1" is applied here so that
# all routes in the router live under /api/v1/batches/... The "v1" prefix
# allows future non-breaking versions (v2, etc.) to coexist on the same
# process without modifying the router files.
app.include_router(batches_router, prefix="/api/v1")
app.include_router(finance_router, prefix="/api/v1")


@app.exception_handler(KukuFitiError)
async def kukufiti_error_handler(request: Request, exc: KukuFitiError) -> JSONResponse:
    """Translate any KukuFitiError subclass into a structured JSON HTTP response.

    This single handler covers every module's domain exceptions without each
    router needing its own try/except. The response body always has the same
    shape so API clients can parse errors consistently:

        {"error": "mpesa_initiation_failed", "message": "Failed to get access token: 401"}

    HTTP status code and error code come from the exception's class attributes,
    set when the subclass is defined in each module's exceptions.py.
    """
    return JSONResponse(
        status_code=exc.http_status_code,
        content={"error": exc.error_code, "message": exc.message},
    )


@app.get("/health", tags=["health"])
async def health_check():
    """Liveness + readiness probe for orchestrators and load balancers.

    LIVENESS vs READINESS:
    This single endpoint serves both roles. Kubernetes typically uses:
      - Liveness probe  → "is the process alive?" (restarts the pod if not)
      - Readiness probe → "can it serve traffic?" (removes pod from LB if not)
    Because a pool failure makes the service unable to handle real requests,
    a failed database check should trigger *both* — hence returning 503
    instead of a partial healthy response.

    WHAT IS CHECKED:
    For each module pool, the handler acquires a connection and runs
    `SELECT 1` — the cheapest possible round-trip that verifies the connection
    is alive and PostgreSQL is responding. It does NOT run business queries.

    WHY CHECK ALL POOLS (not just batches)?
    Prior to the MED-5 fix this endpoint only checked the batches pool.
    A load balancer using /health would see "healthy" even when finance or
    auth pools were broken, routing real traffic to a pod that could not
    complete those requests.

    RESPONSE:
      200 OK  + {"status": "healthy",   ...}  → all pools connected
      503     + {"status": "unhealthy", ...}  → one or more pools failed
    """
    pools = {
        "batches": app.state.batches_pool,
        "finance": app.state.finance_pool,
        "health":  app.state.health_pool,
        "auth":    app.state.auth_pool,
    }

    db_status: dict[str, str] = {}
    all_healthy = True

    for name, pool in pools.items():
        try:
            async with pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            db_status[name] = "connected"
        except Exception as exc:  # noqa: BLE001
            # Catch-all is intentional: any exception (connection error,
            # timeout, pool exhaustion) counts as unhealthy. The error
            # message is included in the response body so operators can
            # diagnose the failure without grepping logs.
            db_status[name] = f"error: {exc}"
            all_healthy = False

    payload = {
        "status": "healthy" if all_healthy else "unhealthy",
        "databases": db_status,
        # Include the app version so operators can confirm which deployment
        # is currently serving traffic without checking container metadata.
        "version": settings.app_version,
    }

    if all_healthy:
        return payload

    # Return 503 Service Unavailable so orchestrators and load balancers
    # remove this instance from the rotation automatically. A 200 with an
    # "unhealthy" body would not trigger automatic remediation.
    return JSONResponse(status_code=503, content=payload)