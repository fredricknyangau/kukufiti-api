"""Business-logic layer for the batches module.

LAYER RESPONSIBILITIES
----------------------
  Router   → validates HTTP input, calls service methods, serialises responses.
  Service  → enforces business rules, orchestrates repository calls.
  Repository → executes SQL, maps rows to domain dataclasses.

BatchService lives in the middle layer. It knows about business concepts
("a batch can only move from active → closed") but does not know about HTTP
concepts (status codes, request bodies). This separation means:
  - Service logic can be unit-tested without spinning up an HTTP server.
  - The same service can be called from a CLI script, a background job, or
    a different router version without duplication.
  - Replacing the repository with a fake/mock for tests is straightforward
    because the service depends on the repository interface, not on asyncpg.
"""
from uuid import UUID
from datetime import date
from typing import Optional
from .repository import BatchRepository
from .models import Batch, BatchSummary
from .exceptions import (
    BatchNotFoundError,
    InvalidStatusTransitionError,
)

# ---------------------------------------------------------------------------
# Batch lifecycle state machine
# ---------------------------------------------------------------------------
# A batch always starts in "active" status (set by the DB default).
# Valid transitions define a strict directed graph:
#
#   active ──► closed ──► archived
#                │
#                └── (terminal: no transitions out of archived)
#
# WHY enforce this here and not in the database?
# A CHECK constraint on the status column ensures only valid string values
# are stored, but it cannot enforce *directional* transitions (e.g. it cannot
# prevent "archived" → "active"). The service layer is the right place for
# this rule because it is business logic that may need to change (e.g. adding
# a "suspended" state) without a database migration.
VALID_TRANSITIONS: dict[str, list[str]] = {
    "active": ["closed"],
    "closed": ["archived"],
    "archived": [],  # terminal state — no further transitions allowed
}


class BatchService:
    def __init__(self, repository: BatchRepository):
        # The repository is injected by dependencies.py, which builds it from
        # the per-request database connection. BatchService never creates its
        # own connection or pool — it is purely a consumer of the repository.
        self._repo = repository

    async def create_batch(
        self,
        batch_name: str,
        breed: str,
        quantity: int,
        start_date: date,
    ) -> Batch:
        """Create a new batch and return the persisted domain object.

        Pre-conditions (enforced by CreateBatchRequest in schemas.py):
          - batch_name and breed are non-empty strings.
          - quantity > 0.
          - start_date is a valid calendar date.

        The router passes a `datetime.date` for start_date (not a string),
        so the repository can pass it directly to asyncpg without parsing.

        Post-condition:
          The returned Batch has a server-assigned UUID, default status
          "active", and zeroed performance counters (total_feed_kg=0,
          mortality_count=0) as set by the database column defaults.
        """
        return await self._repo.create(
            batch_name=batch_name,
            breed=breed,
            quantity=quantity,
            start_date=start_date,
        )

    async def get_batch(self, batch_id: UUID) -> Batch:
        """Retrieve a batch by ID, raising HTTP 404 if not found.

        The repository returns None for soft-deleted rows and missing IDs.
        The service translates that None into a BatchNotFoundError (which is
        an HTTPException subclass) so the router can return a 404 response
        without needing its own None-check logic. This keeps the router thin.
        """
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
        """Return a paginated, optionally filtered list of batches.

        The router validates query parameter constraints (ge=1, le=100 for
        limit; ge=0 for offset; status must be a known value) before calling
        this method, so no additional validation is needed here.

        Returns an empty list rather than raising an error when no batches
        match the filter — an empty result set is not an error condition.
        """
        return await self._repo.list_all(status=status, limit=limit, offset=offset)

    async def count_batches(self, status: Optional[str] = None) -> int:
        """Return the total number of batches matching the optional status filter.

        Called alongside list_batches by the router. The two methods use the
        same filter so the total count and the page content are always
        consistent. The router combines them into a BatchListResponse:
            {batches: [...], total: N, limit: 20, offset: 0}
        The client uses `total` to determine whether more pages exist.
        """
        return await self._repo.count_all(status=status)

    async def transition_status(
        self,
        batch_id: UUID,
        new_status: str,
        end_date: Optional[date] = None,
    ) -> Batch:
        """Move a batch to a new lifecycle status, enforcing valid transitions.

        CONCURRENCY SAFETY — SELECT FOR UPDATE
        This method wraps the read-validate-write cycle in a serialisable
        transaction using a row-level lock. The problem it solves:

          Without locking:
            Two simultaneous POST /close requests both read status="active",
            both pass the transition check, both write status="closed". Only
            one should succeed; the other should receive a 400 error.

          With SELECT FOR UPDATE (via find_by_id_for_update):
            The first request acquires a lock on the row. The second request
            blocks at the SELECT until the first commits. After the first
            commits, the second reads status="closed", fails the transition
            check (closed → closed is not in VALID_TRANSITIONS), and returns
            a 400 response. Correct behaviour.

        END DATE DEFAULTING
        If new_status is "closed" and no end_date was provided by the caller,
        date.today() is used. This ensures the end_date column is never NULL
        for a closed batch. date.today() returns a datetime.date (not datetime),
        which matches the PostgreSQL DATE column type that asyncpg expects.
        """
        # MED-4 fix: wrap the read-validate-write cycle in a transaction with
        # SELECT FOR UPDATE.
        async with self._repo.transaction():
            batch = await self._repo.find_by_id_for_update(batch_id)
            if batch is None:
                raise BatchNotFoundError(batch_id)

            allowed = VALID_TRANSITIONS.get(batch.status, [])
            if new_status not in allowed:
                raise InvalidStatusTransitionError(
                    current=batch.status,
                    attempted=new_status,
                    allowed=allowed,
                )

            # Default the end date for closed batches so the column is
            # never NULL after a close operation. The caller may provide an
            # explicit end_date (e.g. when back-dating a close); if not,
            # today's date is used.
            if new_status == "closed" and not end_date:
                end_date = date.today()

            updated = await self._repo.update_status(batch_id, new_status, end_date)
            if updated is None:
                # Should not happen because find_by_id_for_update holds the lock,
                # but guarding here makes the type checker and future readers happy.
                raise BatchNotFoundError(batch_id)
            return updated

    async def close_batch(self, batch_id: UUID, end_date: Optional[date] = None) -> Batch:
        """Convenience wrapper: transition a batch to "closed" status.

        The dedicated POST /{batch_id}/close endpoint calls this method so
        callers do not need to know the string "closed" or construct an
        UpdateBatchStatusRequest. Internally it delegates to transition_status,
        which applies the same locking, validation, and end_date defaulting
        logic as the PATCH /status endpoint.
        """
        return await self.transition_status(batch_id, "closed", end_date)

    async def get_batch_summary(self, batch_id: UUID) -> BatchSummary:
        """Return the computed summary for a batch, raising 404 if not found.

        BatchSummary is a read-only aggregate view (write model = Batch,
        read model = BatchSummary). It contains computed fields (FCR,
        mortality rate, age in days) that are calculated by the SQL query
        in repository.get_summary, not stored in the database.

        Missing rows are still surfaced as 404 responses — a request for the
        summary of a non-existent batch should fail the same way as a request
        for the batch itself.
        """
        summary = await self._repo.get_summary(batch_id)
        if summary is None:
            raise BatchNotFoundError(batch_id)
        return summary
