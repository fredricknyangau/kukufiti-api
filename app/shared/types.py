# Shared type aliases, domain-specific scalar types, and re-usable type
# constructs for the kukufiti-api codebase.
#
# PURPOSE
# -------
# Python's type system allows creating *aliases* — names that refer to an
# existing type but carry domain meaning:
#
#   BatchId = UUID        # communicates intent at function signatures
#   KES = Decimal         # Kenyan Shilling monetary amount (2 decimal places)
#
# Defining these aliases in one place provides three benefits:
#
#   1. READABILITY — `def get_batch(batch_id: BatchId)` is clearer than
#      `def get_batch(batch_id: UUID)` when reading unfamiliar code.
#
#   2. SINGLE SOURCE OF TRUTH — if the ID type ever changes (e.g. UUID → int
#      for a legacy migration), updating the alias here propagates everywhere.
#
#   3. AVOIDS CIRCULAR IMPORTS — placing aliases in `app/shared/types.py`
#      means any module (models, schemas, repository, service) can import from
#      here without creating import cycles. If aliases lived inside individual
#      modules (e.g. batches/models.py) and another module needed to reference
#      them, it would have to import from batches — coupling modules that
#      should be independent.
#
# USAGE
# -----
# from app.shared.types import BatchId, KES
#
# CONVENTIONS
# -----------
# - Monetary amounts are always Decimal, never float. Floating-point
#   arithmetic loses precision for currency (0.1 + 0.2 ≠ 0.3). PostgreSQL's
#   NUMERIC type maps to Python Decimal via asyncpg.
# - Identifiers are UUID unless the schema explicitly uses another type.