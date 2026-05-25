from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from .dependencies import get_batch_service
from .schemas import (
    BatchListResponse,
    BatchResponse,
    BatchSummaryResponse,
    CreateBatchRequest,
    UpdateBatchStatusRequest,
)
from .service import BatchService

# app/main.py imports this router and mounts it with prefix="/api/v1".
# This local prefix makes every endpoint in this file live under /api/v1/batches.
router = APIRouter(prefix="/batches", tags=["batches"])
BatchServiceDep = Annotated[BatchService, Depends(get_batch_service)]


@router.post("/", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
async def create_batch(
    payload: CreateBatchRequest,
    service: BatchServiceDep,
):
    # FastAPI has already validated payload with CreateBatchRequest from schemas.py.
    # payload.start_date is a datetime.date, so keep it as a date for asyncpg/PostgreSQL
    #  DATE.
    batch = await service.create_batch(
        batch_name=payload.batch_name,
        breed=payload.breed,
        quantity=payload.quantity,
        start_date=payload.start_date,
    )
    # BatchResponse is the HTTP contract; Batch is the internal
    # dataclass from models.py.
    return BatchResponse.model_validate(batch)


@router.get("/", response_model=BatchListResponse)
async def list_batches(
    service: BatchServiceDep,
    # The router validates simple HTTP query constraints before calling the service.
    status: Annotated[
        Literal["active", "closed", "archived"] | None,
        Query(description="Filter by status"),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    # The service handles business flow; the repository handles the SQL.
    batches = await service.list_batches(status=status, limit=limit, offset=offset)
    return BatchListResponse(
        batches=[BatchResponse.model_validate(batch) for batch in batches],
        total=len(batches),
        limit=limit,
        offset=offset,
    )


@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(
    batch_id: UUID,
    service: BatchServiceDep,
):
    # FastAPI parses the path parameter into UUID before this function runs.
    batch = await service.get_batch(batch_id)
    return BatchResponse.model_validate(batch)


@router.patch("/{batch_id}/status", response_model=BatchResponse)
async def update_batch_status(
    batch_id: UUID,
    payload: UpdateBatchStatusRequest,
    service: BatchServiceDep,
):
    # payload.end_date is Optional[date]. Passing it unchanged prevents the asyncpg
    # "'str' object has no attribute 'toordinal'" error for DATE columns.
    batch = await service.transition_status(
        batch_id=batch_id,
        new_status=payload.status,
        end_date=payload.end_date,
    )
    return BatchResponse.model_validate(batch)


@router.post("/{batch_id}/close", response_model=BatchResponse)
async def close_batch(
    batch_id: UUID,
    service: BatchServiceDep,
):
    # Convenience route: it reuses the same service transition rules as PATCH /status.
    batch = await service.close_batch(batch_id)
    return BatchResponse.model_validate(batch)


@router.get("/{batch_id}/summary", response_model=BatchSummaryResponse)
async def get_batch_summary(batch_id: UUID, service: BatchServiceDep, s):
    # Summary data is shaped by repository.get_summary
    # and exposed by BatchSummaryResponse.
    summary = await service.get_batch_summary(batch_id)
    return BatchSummaryResponse.model_validate(summary)
