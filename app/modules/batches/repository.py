"""Data-access layer for the batches module.

This class is the ONLY component that issues SQL against the batches schema.
All other layers (service, router) interact with batch data through methods
on BatchRepository, never by constructing raw SQL themselves.

WIRING:
  dependencies.py creates a BatchRepository with the per-request asyncpg
  connection it acquired from app.state.batches_pool, then passes it to
  BatchService. The connection's lifetime equals the HTTP request lifetime:
  it is released back to the pool when the dependency's `async with` block
  exits (see get_batches_connection in dependencies.py).

ISOLATION:
  The connection uses the batches_app database role, which has DML privileges
  only on the batches schema. Attempting to query other schemas (finance,
  auth, etc.) will be rejected by PostgreSQL at the network layer.

SOFT DELETE:
  Rows are never physically deleted. Instead, a `deleted_at` timestamp is
  set when a batch is removed. Every SELECT includes `AND deleted_at IS NULL`
  to exclude those rows from normal queries. This preserves historical data
  for audit trails and makes accidental deletions recoverable.
"""
from datetime import date
from decimal import Decimal
from uuid import UUID

import asyncpg

from .models import Batch, BatchSummary


class BatchRepository:
    def __init__(self, connection: asyncpg.Connection):
        # Store the connection for the lifetime of this request. The connection
        # is NOT thread-safe but asyncio guarantees single-threaded execution
        # within one event loop iteration, so sharing it across methods within
        # a single request is safe. Never store this repository beyond the
        # request scope — the connection will be released back to the pool.
        self._conn = connection

    def transaction(self):
        """Return the connection's transaction context manager.

        Used by service.transition_status to wrap a read-check-write cycle
        in one atomic database transaction, preventing TOCTOU (Time-of-Check
        Time-of-Use) race conditions.

        Example of the race without a transaction:
          Request A reads batch status = "active" → passes check
          Request B reads batch status = "active" → passes check
          Request A writes status = "closed"      ← correct
          Request B writes status = "closed"      ← duplicate, incorrect

        With a transaction + SELECT FOR UPDATE (find_by_id_for_update):
          Request A acquires row lock + reads "active" → passes check
          Request B tries to acquire lock → BLOCKS until A commits
          Request A writes "closed" → commits → releases lock
          Request B reads "closed" → fails transition check → 400 error
        """
        return self._conn.transaction()

    async def create(
        self,
        batch_name: str,
        breed: str,
        quantity: int,
        start_date: date,
    ) -> Batch:
        # asyncpg uses positional placeholders ($1, $2, …) not named parameters.
        # The `$4::date` cast is a safety measure: even though asyncpg knows
        # start_date is a datetime.date, the explicit cast prevents errors if a
        # caller ever passes a string (e.g. "2026-05-01") by mistake — PostgreSQL
        # will cast it correctly or raise a clear type error.
        #
        # RETURNING lists every column that Batch.from_row expects. Omitting a
        # column here would cause from_row to raise a KeyError, surfacing the
        # mismatch at the earliest possible point rather than further up the call
        # stack or in a response serialisation error.
        row = await self._conn.fetchrow(
            """
            INSERT INTO batches.batches
                (batch_name, breed, quantity, start_date)
            VALUES ($1, $2, $3, $4::date)
            RETURNING id, batch_name, breed, quantity, start_date,
                      end_date, status, total_feed_kg, mortality_count,
                      created_at, updated_at
            """,
            batch_name,
            breed,
            quantity,
            start_date,
        )
        if row is None:
            # fetchrow returns None when INSERT … RETURNING produces no row,
            # which should never happen for a successful insert. Raising here
            # rather than letting from_row crash on None gives a clearer error.
            raise RuntimeError("Failed to create batch")
        # Delegate row→dataclass conversion to the model's from_row class method
        # so the mapping logic lives in one place.
        return Batch.from_row(row)

    async def find_by_id(self, batch_id: UUID) -> Batch | None:
        """Return the batch with the given ID, or None if not found or soft-deleted.

        The `deleted_at IS NULL` clause silently excludes soft-deleted rows.
        Callers (service.get_batch) decide what None means in context — usually
        a 404 response. This method deliberately does NOT raise an exception so
        the service layer controls HTTP semantics.
        """
        row = await self._conn.fetchrow(
            """
            SELECT id, batch_name, breed, quantity, start_date,
                   end_date, status, total_feed_kg, mortality_count,
                   created_at, updated_at
            FROM batches.batches
            WHERE id = $1 AND deleted_at IS NULL
            """,
            batch_id,
        )
        return Batch.from_row(row) if row else None

    async def find_by_id_for_update(self, batch_id: UUID) -> Batch | None:
        """Return the batch and acquire a row-level exclusive lock.

        MUST be called inside an active transaction (use the `transaction()`
        context manager from this class). The `FOR UPDATE` clause tells
        PostgreSQL to lock the selected row until the transaction commits or
        rolls back. Any concurrent transaction that tries to lock or update the
        same row will block until the first transaction completes.

        This is the locking half of the TOCTOU fix described in transaction().
        Without the lock, two concurrent calls to transition_status could both
        read the same status, both pass the allowed-transition check, and both
        write a new status — only one transition should be allowed.

        Returns None (without holding a lock) if the row does not exist or is
        soft-deleted, so the caller still handles the not-found case.
        """
        row = await self._conn.fetchrow(
            """
            SELECT id, batch_name, breed, quantity, start_date,
                   end_date, status, total_feed_kg, mortality_count,
                   created_at, updated_at
            FROM batches.batches
            WHERE id = $1 AND deleted_at IS NULL
            FOR UPDATE
            """,
            batch_id,
        )
        return Batch.from_row(row) if row else None

    async def list_all(
        self,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Batch]:
        # The single query handles both "all batches" and "filtered by status"
        # using the `$1::text IS NULL OR status = $1` trick:
        #   - When status is None → `NULL IS NULL` is TRUE → the OR short-circuits,
        #     so every non-deleted row is included.
        #   - When status is "active" → `'active' IS NULL` is FALSE → the database
        #     evaluates `status = 'active'` and filters accordingly.
        # This avoids branching in Python to construct different SQL strings.
        #
        # ORDER BY start_date DESC puts the most recent batches first, which is
        # the most useful default for a farmer reviewing their current and recent
        # flocks. LIMIT / OFFSET implement cursor-free pagination; for very large
        # result sets a keyset cursor (WHERE start_date < $last_seen_date) would
        # be more efficient, but OFFSET is sufficient for the expected data volume.
        rows = await self._conn.fetch(
            """
            SELECT id, batch_name, breed, quantity, start_date,
                   end_date, status, total_feed_kg, mortality_count,
                   created_at, updated_at
            FROM batches.batches
            WHERE deleted_at IS NULL
              AND ($1::text IS NULL OR status = $1)
            ORDER BY start_date DESC
            LIMIT $2 OFFSET $3
            """,
            status,
            limit,
            offset,
        )
        return [Batch.from_row(row) for row in rows]

    async def count_all(self, status: str | None = None) -> int:
        """Return the total number of non-deleted batches matching the optional filter.

        Called by the router alongside list_all to provide a `total` field in
        the paginated list response. The client needs `total` to calculate:
          - How many pages exist (ceil(total / limit)).
          - Whether there is a next page (offset + len(current_page) < total).

        WHY a separate query instead of `len(list_all())`?
        list_all applies LIMIT, so it never returns more than `limit` rows.
        Counting the full list with `SELECT COUNT(*)` is the only way to get
        the true total. The COUNT query uses the same WHERE clause as list_all
        so the numbers are always consistent.
        """
        return await self._conn.fetchval(
            """
            SELECT COUNT(*)
            FROM batches.batches
            WHERE deleted_at IS NULL
              AND ($1::text IS NULL OR status = $1)
            """,
            status,
        )

    async def update_status(
        self,
        batch_id: UUID,
        new_status: str,
        end_date: date | None = None,
    ) -> Batch | None:
        # The service validates that `new_status` is a legal transition BEFORE
        # calling this method. The repository trusts the service layer to enforce
        # business rules; it only handles the SQL write.
        #
        # COALESCE($3::date, end_date):
        #   - If a new end_date is provided (not None), use it.
        #   - If None is passed, keep the existing end_date value unchanged.
        #   This avoids a two-step read-then-write cycle when end_date is not
        #   being changed and prevents accidentally clearing an existing end_date.
        #
        # RETURNING after UPDATE gives us the final state of the row in one
        # round-trip. Without RETURNING we would need a separate SELECT to read
        # back the updated row, which would be slower and introduce a race window.
        row = await self._conn.fetchrow(
            """
            UPDATE batches.batches
            SET status = $2,
                end_date = COALESCE($3::date, end_date),
                updated_at = NOW()
            WHERE id = $1 AND deleted_at IS NULL
            RETURNING id, batch_name, breed, quantity, start_date,
                      end_date, status, total_feed_kg, mortality_count,
                      created_at, updated_at
            """,
            batch_id,
            new_status,
            end_date,
        )
        return Batch.from_row(row) if row else None

    async def update_performance(
        self,
        batch_id: UUID,
        additional_feed_kg: Decimal,
        additional_mortality: int,
    ) -> None:
        """Increment feed and mortality counters for a batch.

        WHY additive (+=) rather than absolute (=)?
        Performance data comes from individual health or feeding logs created
        throughout the day. Each log records the *delta* (e.g. "50 kg of feed
        today", "2 deaths today"). The repository accumulates these deltas
        into running totals. Using absolute values would require reading the
        current total first, computing the new total in Python, and writing
        it back — three steps instead of one, and a potential race condition
        if two logs arrive simultaneously.

        The SQL `total_feed_kg + $2` lets PostgreSQL do the addition atomically
        within the UPDATE transaction, making concurrent updates safe without
        explicit locking.

        Returns None because callers (e.g. health module events) do not need
        the updated batch record — they only need confirmation that the write
        succeeded (an exception would propagate if it did not).
        """
        await self._conn.execute(
            """
            UPDATE batches.batches
            SET total_feed_kg    = total_feed_kg + $2,
                mortality_count  = mortality_count + $3,
                updated_at       = NOW()
            WHERE id = $1 AND deleted_at IS NULL
            """,
            batch_id,
            additional_feed_kg,
            additional_mortality,
        )

    async def get_summary(self, batch_id: UUID) -> BatchSummary | None:
        """Return a computed summary for the batch, or None if not found.

        The SQL query computes several derived metrics in-database rather than
        in Python. Doing the arithmetic in SQL is safer (NULLIF guards against
        division by zero) and faster (one round-trip, no extra Python objects):

        surviving_birds:
            quantity - mortality_count. Used as the FCR denominator.

        fcr (Feed Conversion Ratio):
            total_feed_kg / surviving_birds, rounded to 3 dp.
            NULLIF(surviving_birds, 0) returns NULL instead of raising a
            division-by-zero error when all birds have died. The CASE block
            adds a second guard (`surviving_birds > 0`) for clarity.
            Industry target: FCR < 2.0 means <2 kg of feed per kg of bird weight.

        mortality_rate_pct:
            mortality_count / quantity * 100, rounded to 2 dp.
            NULLIF(quantity, 0) guards against batches with 0 initial quantity
            (should not exist due to CHECK constraint, but defensive programming).

        age_days:
            Days from start_date to end_date (if closed) or CURRENT_DATE (if
            still active). Cast to int because date subtraction in PostgreSQL
            returns an INTERVAL, not an integer.

        The column aliases (e.g. `b.quantity AS initial_quantity`) must exactly
        match the field names in models.BatchSummary because from_row uses the
        dict-unpacking pattern `cls(**{k: row[k] for k in row})`.
        """
        row = await self._conn.fetchrow(
            """
            SELECT
                b.id,
                b.batch_name,
                b.breed,
                b.quantity                                    AS initial_quantity,
                b.mortality_count,
                b.quantity - b.mortality_count                AS surviving_birds,
                b.total_feed_kg,
                b.start_date,
                b.end_date,
                b.status,
                CASE
                    WHEN b.quantity - b.mortality_count > 0
                    THEN ROUND(
                        b.total_feed_kg /
                        NULLIF((b.quantity - b.mortality_count)::numeric, 0),
                        3
                    )
                    ELSE NULL
                END                                           AS fcr,
                ROUND(
                    b.mortality_count * 100.0 /
                    NULLIF(b.quantity, 0),
                    2
                )                                             AS mortality_rate_pct,
                (COALESCE(b.end_date, CURRENT_DATE) - b.start_date)::int AS age_days
            FROM batches.batches b
            WHERE b.id = $1 AND b.deleted_at IS NULL
            """,
            batch_id,
        )
        return BatchSummary.from_row(row) if row else None
