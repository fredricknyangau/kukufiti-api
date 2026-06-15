"""Pydantic request and response schemas for the batches HTTP API.

ROLE OF THIS FILE
-----------------
This file defines the HTTP contract for the batches module. It is the only
place where HTTP-layer concerns (JSON field names, input validation rules,
response shape) are expressed. The internal domain layer (models.py, service.py,
repository.py) knows nothing about these schemas.

REQUEST SCHEMAS  (CreateBatchRequest, UpdateBatchStatusRequest)
  FastAPI parses the incoming JSON body and coerces field types before the
  route handler runs. If the body is malformed or violates a validator, FastAPI
  automatically returns a 422 Unprocessable Entity response with a structured
  error body — the route handler is never called.

RESPONSE SCHEMAS  (BatchResponse, BatchSummaryResponse, BatchListResponse)
  Route handlers call `Schema.model_validate(dataclass_instance)` to convert
  a domain dataclass into a Pydantic model for serialisation. The schema is
  the explicit HTTP contract; the dataclass is the internal representation.
  Keeping them separate allows the API shape to diverge from the internal model
  (e.g. renaming a field in the response, adding computed fields, or hiding
  internal fields) without changing the domain layer.

TYPE COERCION — dates
  Pydantic parses ISO-8601 date strings from JSON ("2026-05-01") into
  Python datetime.date objects automatically. This means route handlers and
  service methods always receive a datetime.date, never a raw string, which
  is safe to pass directly to asyncpg DATE columns.
"""
from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class AppBaseModel(BaseModel):
    """Shared Pydantic configuration for all request and response schemas.

    from_attributes=True:
        Allows model_validate() to accept Python dataclasses and ORM objects
        (not just dicts). The router uses this to construct response schemas
        directly from the domain dataclasses returned by the service:
            BatchResponse.model_validate(batch)   # batch is models.Batch
        Without from_attributes, Pydantic would raise a validation error
        because models.Batch is not a dict.

    populate_by_name=True:
        When a field has an alias (e.g. via alias_generator), both the alias
        and the Python field name can be used to set the field value. This is
        required when using alias_generator for camelCase output while still
        wanting to construct schemas with snake_case keyword arguments in tests.
    """
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class CreateBatchRequest(AppBaseModel):
    """Request body for POST /api/v1/batches/.

    FastAPI parses the JSON body and runs these validators before the route
    handler is invoked. A failed validator produces a 422 response; the handler
    only runs when all fields are valid.
    """
    batch_name: str
    breed: str
    # Pydantic parses "2026-05-01" → datetime.date automatically.
    # asyncpg accepts datetime.date directly for PostgreSQL DATE columns,
    # so no further conversion is needed in the repository.
    quantity: int
    start_date: date

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        """Reject quantities ≤ 0.

        A batch represents a real flock of birds; placing 0 or negative
        birds is not meaningful and would corrupt FCR and mortality rate
        calculations (division by zero). The database also has a CHECK
        constraint (quantity > 0) as a second line of defence.
        """
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    @field_validator("batch_name")
    @classmethod
    def batch_name_not_empty(cls, v: str) -> str:
        """Reject blank or whitespace-only batch names.

        `.strip()` is applied to the value before returning so that names
        with leading/trailing spaces are silently normalised. A name like
        "  " (spaces only) fails the check; "  Batch A  " becomes "Batch A".
        """
        if not v.strip():
            raise ValueError("Batch name cannot be empty")
        return v.strip()

    @field_validator("breed")
    @classmethod
    def breed_not_empty(cls, v: str) -> str:
        """Reject blank or whitespace-only breed strings.

        Same normalisation logic as batch_name_not_empty. The breed field
        is a free-text string rather than an enum because broiler breed names
        are not standardised and vary by region and supplier.
        """
        if not v.strip():
            raise ValueError("Breed cannot be empty")
        return v.strip()


class UpdateBatchStatusRequest(AppBaseModel):
    """Request body for PATCH /api/v1/batches/{batch_id}/status.

    Only the `status` and optional `end_date` are accepted. The service
    (via VALID_TRANSITIONS) enforces which status transitions are allowed;
    this schema only ensures the requested value is one of the known
    non-initial statuses. "active" is excluded because batches are always
    created active and cannot be moved back to active from any other state.
    """
    # Only "closed" and "archived" are valid targets — batches always start
    # "active" from the DB default, so that value is excluded here.
    status: str
    # end_date is optional in the request body. If omitted when closing a
    # batch, the service defaults to date.today(). Passing an explicit date
    # allows back-dating (e.g. recording that a batch was actually closed
    # yesterday). The type is date (not datetime) because the DB column is DATE.
    end_date: Optional[date] = None

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        """Reject status values that are not valid transition targets.

        "active" is excluded because it is the initial state set by the
        database default and no valid transition leads back to it. "archived"
        can only be set from "closed"; the service enforces that rule — this
        validator only ensures the string is one of the known non-initial values.
        """
        allowed = {"closed", "archived"}
        if v not in allowed:
            raise ValueError(f"Status must be one of: {allowed}")
        return v


class BatchResponse(AppBaseModel):
    """Response schema for a single batch.

    This schema mirrors models.Batch but is kept deliberately separate.
    Benefits of the separation:
      - The API contract is explicit and versioned independently of the
        internal model. Adding a field to models.Batch does not automatically
        expose it in the API; it must be added here intentionally.
      - Fields can be renamed in the response (via aliases) without changing
        the internal model.
      - The Pydantic model performs output serialisation (UUID → string,
        Decimal → string/number, datetime → ISO-8601) that the dataclass
        does not.
    """
    id: UUID
    batch_name: str
    breed: str
    quantity: int
    start_date: date
    end_date: Optional[date]
    status: str
    total_feed_kg: Decimal
    mortality_count: int
    created_at: datetime
    updated_at: datetime


class BatchSummaryResponse(AppBaseModel):
    """Response schema for the computed batch summary endpoint.

    Mirrors models.BatchSummary. Fields like `fcr` and `mortality_rate_pct`
    are Optional because they are NULL in the database when the batch has
    no surviving birds or zero initial quantity (NULLIF guards in SQL).
    The `initial_quantity` name (instead of `quantity`) is an intentional
    API design choice: it clarifies that the value reflects the original
    placement count, not the current live count.
    """
    id: UUID
    batch_name: str
    breed: str
    initial_quantity: int
    mortality_count: int
    surviving_birds: int
    total_feed_kg: Decimal
    start_date: date
    end_date: Optional[date]
    status: str
    fcr: Optional[Decimal]              # Feed Conversion Ratio; null when 0 survivors
    mortality_rate_pct: Optional[Decimal]  # % of flock lost; null when quantity = 0
    age_days: int


class BatchListResponse(AppBaseModel):
    """Paginated list response for GET /api/v1/batches/.

    Wraps the current page of batch rows together with the pagination metadata
    the client needs to fetch subsequent pages or display a page count:

        batches: the rows on the current page (up to `limit` items).
        total:   the total number of matching rows across all pages.
        limit:   the page size that was requested (echoed back for clarity).
        offset:  the starting index of this page (echoed back for clarity).

    A client can calculate whether a next page exists:
        has_next = offset + len(batches) < total
    """
    batches: list[BatchResponse]
    total: int    # total matching rows — used by clients to compute page count
    limit: int    # requested page size
    offset: int   # requested starting index
