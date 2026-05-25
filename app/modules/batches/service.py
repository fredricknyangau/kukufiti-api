from uuid import UUID
from datetime import date
from typing import Optional
from .repository import BatchRepository
from .models import Batch, BatchSummary
from .exceptions import (
    BatchNotFoundError,
    InvalidStatusTransitionError,
)

# router.py imports BatchService and calls these methods after HTTP validation.
# This layer keeps business rules here so repository.py can stay focused on SQL.

# Valid status transitions: the allowed state machine for a batch.
VALID_TRANSITIONS = {
    "active": ["closed"],
    "closed": ["archived"],
    "archived": [],  # terminal state
}

class BatchService:
    def __init__(self, repository: BatchRepository):
        # dependencies.py builds this repository with the current request's DB connection.
        self._repo = repository

    async def create_batch(
        self,
        batch_name: str,
        breed: str,
        quantity: int,
        start_date: date,
    ) -> Batch:
        # The router passes a date from CreateBatchRequest; the repository inserts it
        # directly into the PostgreSQL DATE column.
        return await self._repo.create(
            batch_name=batch_name,
            breed=breed,
            quantity=quantity,
            start_date=start_date,
        )

    async def get_batch(self, batch_id: UUID) -> Batch:
        # Repository returns None when no row exists; the service converts that into
        # a FastAPI HTTPException from exceptions.py for the router to return as 404.
        batch = await self._repo.find_by_id(batch_id)
        if batch is None:
            raise BatchNotFoundError(batch_id)
        return batch

    async def list_batches(
        self,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Batch]:
        # Filtering and pagination values are already validated by router Query parameters.
        return await self._repo.list_all(status=status, limit=limit, offset=offset)

    async def transition_status(
        self,
        batch_id: UUID,
        new_status: str,
        end_date: Optional[date] = None,
    ) -> Batch:
        # Load the current row first because allowed transitions depend on its status.
        batch = await self._repo.find_by_id(batch_id)
        if batch is None:
            raise BatchNotFoundError(batch_id)

        allowed = VALID_TRANSITIONS.get(batch.status, [])
        if new_status not in allowed:
            raise InvalidStatusTransitionError(
                current=batch.status,
                attempted=new_status,
                allowed=allowed,
            )

        # Closing a batch requires an end date. date.today() keeps the type compatible
        # with repository.update_status and the database DATE column.
        if new_status == "closed" and not end_date:
            end_date = date.today()

        updated = await self._repo.update_status(batch_id, new_status, end_date)
        if updated is None:
            raise BatchNotFoundError(batch_id)
        return updated

    async def close_batch(self, batch_id: UUID, end_date: Optional[date] = None) -> Batch:
        # The close endpoint imports this method as a shortcut for transition_status(..., "closed").
        return await self.transition_status(batch_id, "closed", end_date)

    async def get_batch_summary(self, batch_id: UUID) -> BatchSummary:
        # Summary is read-only aggregate data. Missing rows are still exposed as 404.
        summary = await self._repo.get_summary(batch_id)
        if summary is None:
            raise BatchNotFoundError(batch_id)
        return summary
