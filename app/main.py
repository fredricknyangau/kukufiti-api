from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import create_pool
from app.core.logging import configure_logging
from app.modules.batches.router import router as batches_router
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
    docs_url="/api/docs",

)

app.include_router(batches_router, prefix="/api/v1")

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