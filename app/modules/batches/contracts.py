# Shared interfaces (protocols / abstract types) for the batches module.
#
# PURPOSE — when to add something here vs to service.py or models.py
# -------------------------------------------------------------------
# This file is the *public contract* of the batches module. Other modules
# (finance, health) that need to interact with batch data should depend on
# the interfaces defined here — NOT on service.py or repository.py directly.
#
# Depending on the concrete service or repository would couple modules
# together at the implementation level. If BatchService ever changes a method
# signature, every module that imported it would need updating. Depending on
# a protocol (structural subtype) defined here means the finance module only
# needs to know "I need something that has a `get_batch(batch_id) -> Batch`
# method" — the concrete implementation can change freely.
#
# EXAMPLE — cross-module batch lookup (to be implemented)
# --------------------------------------------------------
# The finance module needs to verify a batch exists before recording a
# transaction. Instead of importing BatchService:
#
#   from typing import Protocol
#   from uuid import UUID
#   from .models import Batch
#
#   class BatchReader(Protocol):
#       """Read-only view of batch data needed by other modules."""
#       async def get_batch(self, batch_id: UUID) -> Batch:
#           """Return the batch or raise BatchNotFoundError."""
#           ...
#
# The finance service then accepts a `BatchReader` rather than a `BatchService`:
#
#   class FinanceService:
#       def __init__(self, repo: FinanceRepository, batches: BatchReader):
#           self._batches = batches
#
# This pattern is sometimes called "dependency inversion" or the
# "ports and adapters" (hexagonal) architecture style.
