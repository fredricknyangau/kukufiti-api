"""HTTP exception classes for the batches module.

DESIGN — HTTPException subclasses vs custom exception handlers
--------------------------------------------------------------
FastAPI's HTTPException is the simplest way to map a business failure to an
HTTP response: raising it anywhere inside a route handler (or inside code
called by a route handler, like a service method) causes FastAPI to stop
processing the request and return a JSON error response with the given
status_code and detail.

By subclassing HTTPException, each exception type:
  1. Carries its own status code and detail format, so callers raise a
     semantically named exception (BatchNotFoundError) rather than a magic
     number (HTTPException(status_code=404, ...)).
  2. Can be caught by type in tests:
         with pytest.raises(BatchNotFoundError):
             await service.get_batch(unknown_id)
  3. Can be intercepted by a FastAPI exception handler registered in main.py
     if more complex error formatting is ever needed.

FUTURE DIRECTION
If the service layer moves to framework-agnostic domain exceptions (see
app/core/exceptions.py), these classes would become thin translators that
the HTTP layer uses to convert domain exceptions to HTTP responses, rather
than being raised directly by the service.
"""
from uuid import UUID

from fastapi import HTTPException, status


class BatchNotFoundError(HTTPException):
    """Raised when a batch ID does not exist or has been soft-deleted.

    Results in HTTP 404 Not Found. The batch UUID is included in the detail
    message so the client (and any log aggregator) can immediately identify
    which resource was missing without parsing the request URL.

    Raised by: BatchService.get_batch, BatchService.transition_status,
               BatchService.get_batch_summary.
    """
    def __init__(self, batch_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch {batch_id} not found",
        )


class InvalidStatusTransitionError(HTTPException):
    """Raised when a requested status transition is not in VALID_TRANSITIONS.

    Results in HTTP 400 Bad Request. The detail is a structured dict (not a
    plain string) so the client can programmatically extract:
      - error:               machine-readable error code for client-side logic.
      - message:             human-readable description of what was rejected.
      - allowed_transitions: the list of states the batch *could* move to,
                             so the client can present valid options to the user.

    Example response body:
        {
            "detail": {
                "error": "invalid_status_transition",
                "message": "Cannot transition from 'archived' to 'active'",
                "allowed_transitions": []
            }
        }

    Raised by: BatchService.transition_status (after checking VALID_TRANSITIONS).
    """
    def __init__(self, current: str, attempted: str, allowed: list[str]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_status_transition",
                "message": f"Cannot transition from '{current}' to '{attempted}'",
                "allowed_transitions": allowed,
            },
        )


class BatchAlreadyClosedError(HTTPException):
    """Raised when an operation requires an active batch but finds a closed one.

    Results in HTTP 409 Conflict. Currently unused — the general-purpose
    InvalidStatusTransitionError covers this case via VALID_TRANSITIONS —
    but this class is kept for callers that want to signal a more specific
    "already closed" conflict rather than a generic "invalid transition".

    Example future use: a dedicated "re-open batch" endpoint that should
    clearly distinguish "this batch is closed (conflict)" from "you cannot
    re-open a batch (bad request)".
    """
    def __init__(self, batch_id: UUID):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Batch {batch_id} is already closed",
        )
