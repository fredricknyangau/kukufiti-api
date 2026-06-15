# app/modules/finance/exceptions.py
from app.core.exceptions import KukuFitiError


class MpesaInitiationError(KukuFitiError):
    """STK push could not be initiated — Daraja rejected or timed out.

    Raised by FinanceService.initiate_mpesa_payment() when the Daraja API
    call fails for any reason (auth failure, request rejection, validation).
    The handler in main.py returns HTTP 502 Bad Gateway, signalling to the
    client that our server received a bad response from an upstream service
    (Safaricom), not that the client's request was malformed.
    """
    http_status_code = 502
    error_code = "mpesa_initiation_failed"


class TransactionNotFoundError(KukuFitiError):
    """Raised when a finance transaction ID does not exist in the database.

    Raised by FinanceService (and future repository methods) when a lookup
    by transaction UUID returns no row. The handler in main.py returns
    HTTP 404 Not Found.
    """
    http_status_code = 404
    error_code = "transaction_not_found"
