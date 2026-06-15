"""HTTP route handlers for the batches module.

This module defines the FastAPI APIRouter that is mounted by app/main.py
with prefix="/api/v1". The local prefix="/batches" means every endpoint
in this file is served under /api/v1/batches/...

ROUTER RESPONSIBILITIES
-----------------------
  - Parse and validate incoming HTTP requests (path params, query params,
    request bodies) using FastAPI's automatic schema validation.
  - Call the appropriate BatchService method with validated, typed arguments.
  - Serialise the service's domain dataclass return value into the declared
    response schema (BatchResponse, BatchListResponse, etc.).
  - Return the correct HTTP status codes (201 for creation, 200 for reads, etc.).

The router does NOT contain business logic — it delegates everything to the
service. A route handler that grows business logic (e.g. computing something
before or after the service call) is a sign that logic belongs in the service.

OPENAPI DOCUMENTATION
---------------------
FastAPI generates interactive API docs at /docs (Swagger UI) and /redoc using
the type annotations, response_model declarations, and Query() descriptions
in this file. Keep parameter descriptions up-to-date so the docs remain
accurate for developers integrating with the API.
"""
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

# The router is imported by app/main.py:
#     app.include_router(batches_router, prefix="/api/v1")
# The combined prefix of the router ("/api/v1") and this local prefix
# ("/batches") makes every endpoint live under /api/v1/batches/...
# The `tags` list groups all batch endpoints under a single "batches"
# section in the OpenAPI documentation.
router = APIRouter(prefix="/batches", tags=["batches"])

# Type alias for the injected service dependency. Using Annotated + Depends
# here (instead of a default parameter value) is the modern FastAPI pattern
# that works correctly with type checkers and avoids mutable default arguments.
BatchServiceDep = Annotated[BatchService, Depends(get_batch_service)]


@router.post("/", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
async def create_batch(
    payload: CreateBatchRequest,
    service: BatchServiceDep,
):
    """Create a new broiler batch.

    FastAPI validates the JSON body against CreateBatchRequest (including the
    field validators for quantity > 0 and non-empty strings) before this
    handler runs. A malformed body results in a 422 response automatically.

    `payload.start_date` is a `datetime.date` (not a string) because Pydantic
    parsed the ISO-8601 string from the JSON body. It is passed as-is to the
    service and then to asyncpg, which maps it correctly to the PostgreSQL
    DATE column without any further conversion.

    Returns HTTP 201 Created (not 200) because a new resource was created.
    The response body contains the persisted batch with its server-assigned UUID.
    """
    batch = await service.create_batch(
        batch_name=payload.batch_name,
        breed=payload.breed,
        quantity=payload.quantity,
        start_date=payload.start_date,
    )
    # model_validate converts the internal Batch dataclass to a BatchResponse
    # Pydantic model. from_attributes=True (set on AppBaseModel) enables this
    # without needing to convert the dataclass to a dict first.
    return BatchResponse.model_validate(batch)


@router.get("/", response_model=BatchListResponse)
async def list_batches(
    service: BatchServiceDep,
    # status is a Literal type so FastAPI validates it against the enum before
    # calling the handler. An invalid value ("suspended", etc.) returns 422.
    status: Annotated[
        Literal["active", "closed", "archived"] | None,
        Query(description="Filter by status"),
    ] = None,
    # ge=1, le=100 constraints are enforced by FastAPI's Query validation.
    # A request with limit=0 or limit=200 returns 422 before hitting the handler.
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    # ge=0 ensures offset is non-negative. Negative offsets have undefined
    # behaviour in PostgreSQL and should never reach the repository.
    offset: Annotated[int, Query(ge=0)] = 0,
):
    """List batches with optional status filter and pagination.

    Two service calls are made:
      1. list_batches  → fetches the current page of rows.
      2. count_batches → fetches the total count for pagination metadata.

    Both calls use the same `status` filter so the `total` in the response
    is always consistent with the number of rows across all pages. The client
    can compute whether there is a next page: `offset + len(batches) < total`.
    """
    batches = await service.list_batches(status=status, limit=limit, offset=offset)
    total = await service.count_batches(status=status)
    return BatchListResponse(
        batches=[BatchResponse.model_validate(batch) for batch in batches],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(
    batch_id: UUID,
    service: BatchServiceDep,
):
    """Retrieve a single batch by its UUID.

    FastAPI automatically parses the `{batch_id}` path segment into a Python
    UUID before this handler is called. An invalid UUID string (e.g. "abc")
    results in a 422 response from FastAPI before the handler runs.

    The service raises BatchNotFoundError (HTTP 404) if the ID does not exist
    or the batch has been soft-deleted.
    """
    batch = await service.get_batch(batch_id)
    return BatchResponse.model_validate(batch)


@router.patch("/{batch_id}/status", response_model=BatchResponse)
async def update_batch_status(
    batch_id: UUID,
    payload: UpdateBatchStatusRequest,
    service: BatchServiceDep,
):
    """Update the lifecycle status of a batch.

    The request body must contain a `status` field with a valid target value
    ("closed" or "archived"). An optional `end_date` field may be provided
    when closing a batch; if omitted, the service defaults to today's date.

    ASYNCPG DATE TYPE NOTE:
    `payload.end_date` is Optional[datetime.date] (parsed by Pydantic from the
    JSON body). Passing a datetime.date to asyncpg for a DATE column works
    correctly. If a string were passed instead, asyncpg would raise
    "'str' object has no attribute 'toordinal'". The Pydantic schema
    guarantees the correct Python type reaches the service and repository.

    The service enforces valid transition rules and uses SELECT FOR UPDATE
    to prevent concurrent double-transitions. Invalid transitions return 400;
    non-existent batches return 404.
    """
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
    """Close a batch without requiring an explicit status body.

    This is a convenience endpoint for the common "close this batch" action.
    It is equivalent to PATCH /{batch_id}/status with body {"status": "closed"},
    but requires no request body and is more discoverable in the API docs.

    Internally it calls service.close_batch, which delegates to
    transition_status with the same locking, validation, and end_date defaulting
    logic. The two endpoints are kept consistent because they share the same
    service method.
    """
    batch = await service.close_batch(batch_id)
    return BatchResponse.model_validate(batch)


@router.get("/{batch_id}/summary", response_model=BatchSummaryResponse)
async def get_batch_summary(batch_id: UUID, service: BatchServiceDep):
    """Return the computed performance summary for a batch.

    The summary is a read-only, aggregate view that includes metrics calculated
    by the database query (FCR, mortality rate, age in days). It is served from
    a separate endpoint rather than embedded in BatchResponse because:
      - It is more expensive to compute (more SQL arithmetic).
      - Not every caller needs it — the list endpoint returns basic BatchResponse
        objects to keep payloads small.
      - The computed fields (fcr, mortality_rate_pct) are conceptually distinct
        from the batch record's operational fields.

    Returns 404 if the batch does not exist or is soft-deleted, matching the
    behaviour of GET /{batch_id}.
    """
    summary = await service.get_batch_summary(batch_id)
    return BatchSummaryResponse.model_validate(summary)
