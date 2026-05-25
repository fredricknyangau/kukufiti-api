from datetime import date
from decimal import Decimal
from uuid import UUID

import asyncpg

from .models import Batch, BatchSummary


# dependencies.py imports BatchRepository and gives it a per-request asyncpg connection.
# This is the only batch layer that talks directly to the batches schema.
class BatchRepository:
    def __init__(self, connection: asyncpg.Connection):
        # The service uses this repository; the repository uses this connection for SQL.
        self._conn = connection

    async def create(
        self,
        batch_name: str,
        breed: str,
        quantity: int,
        start_date: date,
    ) -> Batch:
        # asyncpg binds Python values to $1, $2, etc. start_date must be datetime.date
        # because PostgreSQL start_date is a DATE column.
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
            raise RuntimeError("Failed to create batch")
        # models.Batch.from_row centralizes conversion from asyncpg.Record to dataclass.
        return Batch.from_row(row)

    async def find_by_id(self, batch_id: UUID) -> Batch | None:
        # Soft-deleted rows are hidden from the rest of the app.
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
        # Service methods decide whether None becomes a 404 or another response.
        return Batch.from_row(row) if row else None

    async def list_all(
        self,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Batch]:
        # The nullable status parameter lets one query handle both filtered and
        # unfiltered lists.
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

    async def update_status(
        self,
        batch_id: UUID,
        new_status: str,
        end_date: date | None = None,
    ) -> Batch | None:
        # The service validates whether this transition is allowed before this SQL runs.
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
        # Other modules can call this repository method when feed or health events
        # affect a batch.
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
        # This read model is shaped to match BatchSummary.from_row
        # and BatchSummaryResponse.
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
