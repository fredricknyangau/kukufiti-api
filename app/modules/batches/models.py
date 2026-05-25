from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import asyncpg


# repository.py imports these dataclasses.
# They represent trusted Python objects after data has been read from PostgreSQL.
@dataclass
class Batch:
    # Field names match the SELECT/RETURNING columns in repository.py.
    id: UUID
    batch_name: str
    breed: str
    quantity: int
    start_date: date
    end_date: date | None
    status: str
    total_feed_kg: Decimal
    mortality_count: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: asyncpg.Record) -> "Batch":
        # asyncpg.Record acts like a dict. This method keeps row mapping in one place.
        return cls(
            id=row["id"],
            batch_name=row["batch_name"],
            breed=row["breed"],
            quantity=row["quantity"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            status=row["status"],
            total_feed_kg=row["total_feed_kg"],
            mortality_count=row["mortality_count"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


@dataclass
class BatchSummary:
    # Field names match the aliases in BatchRepository.get_summary.
    id: UUID
    batch_name: str
    breed: str
    initial_quantity: int
    mortality_count: int
    surviving_birds: int
    total_feed_kg: Decimal
    start_date: date
    end_date: date | None
    status: str
    fcr: Decimal | None  # Feed Conversion Ratio
    mortality_rate_pct: Decimal | None
    age_days: int

    @classmethod
    def from_row(cls, row: asyncpg.Record) -> "BatchSummary":
        # The repository query already names every selected column to match this
        #  dataclass.
        return cls(**{k: row[k] for k in row})
