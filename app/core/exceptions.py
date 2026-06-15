"""Base exception class for the kukufiti-api domain layer.

KukuFitiError is a framework-agnostic base that all module exceptions
should subclass. It carries HTTP metadata as class attributes so a single
exception handler registered in app/main.py can translate any domain
exception to the correct HTTP response — without the service or repository
layers importing FastAPI.

HOW IT WORKS
------------
Subclasses declare `http_status_code` and `error_code` as class attributes:

    class TransactionNotFoundError(KukuFitiError):
        http_status_code = 404
        error_code = "transaction_not_found"

The global handler in main.py catches KukuFitiError and builds the response:

    @app.exception_handler(KukuFitiError)
    async def kukufiti_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.http_status_code,
            content={"error": exc.error_code, "message": str(exc)},
        )

BENEFITS OVER HTTPException SUBCLASSES
---------------------------------------
  - Service / repository code has zero FastAPI imports.
  - Unit tests can `raise TransactionNotFoundError("...")` and catch it
    without spinning up a FastAPI test client.
  - Error codes are machine-readable strings (not just HTTP status ints),
    so API clients can branch on `error_code` without parsing messages.
  - Adding a new error type only requires defining the subclass here —
    the handler in main.py handles it automatically.
"""


class KukuFitiError(Exception):
    """Root domain exception for all kukufiti-api business errors.

    Every module should define its own subclasses of this class in its
    `exceptions.py` file. Do NOT raise KukuFitiError directly — always
    use a specific subclass so callers can distinguish error types.

    Class attributes (must be set on every subclass):
        http_status_code (int): The HTTP status code the handler will use.
        error_code (str):       Machine-readable snake_case error identifier
                                returned in the JSON response body.
    """
    http_status_code: int = 500
    error_code: str = "internal_error"

    def __init__(self, message: str = "An unexpected error occurred"):
        # Store the human-readable message so `str(exc)` returns it and
        # the exception handler can include it in the JSON response body.
        super().__init__(message)
        self.message = message
