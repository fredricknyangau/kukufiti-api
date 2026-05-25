from uuid import UUID

from fastapi import HTTPException, status


# service.py imports these exceptions.
# Raising them in the service lets FastAPI convert business failures into HTTP responses
class BatchNotFoundError(HTTPException):
    def __init__(self, batch_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch {batch_id} not found",
        )


class InvalidStatusTransitionError(HTTPException):
    # Used when service.transition_status rejects a move outside VALID_TRANSITIONS.
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
    # Kept for callers that may later need a specific conflict response.
    def __init__(self, batch_id: UUID):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Batch {batch_id} is already closed",
        )
