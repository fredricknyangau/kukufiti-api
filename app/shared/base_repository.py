# Abstract base class and common query helpers for all module repositories.
#
# PURPOSE
# -------
# Every module (batches, finance, health, auth) has its own repository class
# that wraps an asyncpg connection and issues SQL. Many of those repositories
# share common patterns:
#   - Fetching a single row by primary key and returning None when not found
#   - Soft-deleting a row by setting deleted_at = NOW()
#   - Paginating a list query with LIMIT / OFFSET
#   - Counting rows for a pagination total
#
# Placing these helpers in a base class avoids copy-pasting the same logic
# across every repository and provides a consistent interface for testing
# (e.g. a shared test fixture that exercises the base CRUD behaviour).
#
# PLANNED INTERFACE (to be implemented)
# --------------------------------------
#
#   class BaseRepository:
#       def __init__(self, connection: asyncpg.Connection) -> None:
#           # Every repository receives a per-request connection from the
#           # module's dependency function (e.g. get_batches_connection).
#           self._conn = connection
#
#       def transaction(self):
#           # Expose the connection's transaction context manager so service
#           # methods can wrap multi-step operations atomically.
#           return self._conn.transaction()
#
#       async def _fetch_one(self, sql: str, *args) -> asyncpg.Record | None:
#           # Centralised fetchrow wrapper; subclasses use this to avoid
#           # repeating the None-check idiom.
#           ...
#
#       async def _fetch_all(self, sql: str, *args) -> list[asyncpg.Record]:
#           ...
#
#       async def _execute(self, sql: str, *args) -> None:
#           ...
#
# USAGE
# -----
# from app.shared.base_repository import BaseRepository
#
# class BatchRepository(BaseRepository):
#     async def find_by_id(self, batch_id: UUID) -> Batch | None:
#         row = await self._fetch_one("SELECT … FROM batches WHERE id=$1", batch_id)
#         return Batch.from_row(row) if row else None