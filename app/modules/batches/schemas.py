from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

# router.py imports these schemas.
# Request schemas validate HTTP input; response schemas define what the API sends back.
class AppBaseModel(BaseModel):
    # from_attributes lets router.py validate dataclass model objects directly.
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class CreateBatchRequest(AppBaseModel):
    # FastAPI parses JSON like {"start_date": "2026-05-01"} into datetime.date here.
    batch_name: str
    breed: str
    quantity: int
    start_date: date

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    @field_validator("batch_name")
    @classmethod
    def batch_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Batch name cannot be empty")
        return v.strip()

    @field_validator("breed")
    @classmethod
    def breed_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Breed cannot be empty")
        return v.strip()

class UpdateBatchStatusRequest(AppBaseModel):
    # router.py passes these fields to service.transition_status.
    status: str
    end_date: Optional[date] = None

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str) -> str:
        allowed = {"closed", "archived"}
        if v not in allowed:
            raise ValueError(f"Status must be one of: {allowed}")
        return v

class BatchResponse(AppBaseModel):
    # Mirrors models.Batch, but stays separate so the public HTTP contract is explicit.
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
    # Mirrors models.BatchSummary, which is built from repository.get_summary SQL aliases.
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
    fcr: Optional[Decimal]
    mortality_rate_pct: Optional[Decimal]
    age_days: int

class BatchListResponse(AppBaseModel):
    # Used by router.list_batches to wrap the current page of batch rows.
    batches: list[BatchResponse]
    total: int
    limit: int
    offset: int
