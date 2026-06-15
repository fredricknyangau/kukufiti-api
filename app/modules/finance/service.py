# app/modules/finance/service.py
import logging
from datetime import date
from decimal import Decimal
from uuid import UUID
from typing import Optional

from .repository import FinanceRepository
from .mpesa_client import MpesaClient, MpesaError
from .schemas import BatchPLResponse

logger = logging.getLogger(__name__)


class FinanceService:
    def __init__(self, repository: FinanceRepository, mpesa_client: MpesaClient):
        self._repo = repository
        self._mpesa = mpesa_client

    async def record_income(
        self,
        batch_id: UUID,
        category: str,
        amount_kes: Decimal,
        transaction_date: date,
        notes: Optional[str] = None,
    ) -> dict:
        return await self._repo.create_confirmed_transaction(
            batch_id=batch_id,
            transaction_type="income",
            category=category,
            amount_kes=amount_kes,
            transaction_date=transaction_date,
            notes=notes,
        )

    async def record_expense(
        self,
        batch_id: UUID,
        category: str,
        amount_kes: Decimal,
        transaction_date: date,
        notes: Optional[str] = None,
    ) -> dict:
        return await self._repo.create_confirmed_transaction(
            batch_id=batch_id,
            transaction_type="expense",
            category=category,
            amount_kes=amount_kes,
            transaction_date=transaction_date,
            notes=notes,
        )

    async def initiate_mpesa_payment(
        self,
        batch_id: UUID,
        phone_number: str,
        amount_kes: Decimal,
        category: str,
        description: str,
    ) -> dict:
        """
        Two-step process:
        1. Create a pending transaction in our DB first
        2. Then call Daraja — if Daraja fails we can clean up our record
        3. If Daraja succeeds, record the checkout_request_id

        WHY create DB record first:
        We need a transaction_id to link to the mpesa_request.
        Creating it first also means if Daraja is slow/down,
        we have a record of the attempted payment.
        """
        # Step 1 — create pending transaction
        transaction = await self._repo.create_pending_transaction(
            batch_id=batch_id,
            transaction_type="income",
            category=category,
            amount_kes=amount_kes,
            transaction_date=date.today(),
            notes=f"M-Pesa payment: {description}",
        )

        # Step 2 — initiate STK push
        try:
            daraja_response = await self._mpesa.initiate_stk_push(
                phone_number=phone_number,
                amount=amount_kes,
                account_reference=str(batch_id)[:12],
                transaction_desc=description,
            )
        except MpesaError as e:
            # Daraja rejected — mark our transaction as failed
            logger.warning(
                "M-Pesa STK push rejected — marking transaction failed",
                extra={"transaction_id": str(transaction["id"]), "error": str(e)},
            )
            from app.modules.finance.exceptions import MpesaInitiationError
            raise MpesaInitiationError(str(e)) from e

        # Step 3 — record the M-Pesa request with checkout ID
        await self._repo.record_mpesa_request(
            transaction_id=transaction["id"],
            checkout_request_id=daraja_response["CheckoutRequestID"],
            merchant_request_id=daraja_response["MerchantRequestID"],
            phone_number=phone_number,
            amount_kes=amount_kes,
        )

        return {
            "transaction_id": transaction["id"],
            "checkout_request_id": daraja_response["CheckoutRequestID"],
            "message": "STK push sent. Customer will receive a PIN prompt.",
        }

    async def process_mpesa_callback(self, callback_body: dict) -> None:
        """
        Processes the callback Daraja POSTs to our server
        after the customer completes (or cancels) the payment.

        WHY this structure:
        Daraja sends a nested JSON. We need to carefully extract
        the result fields and handle both success and failure cases.
        """
        # Extract the callback data
        # Daraja wraps everything in Body.stkCallback
        try:
            stk_callback = callback_body["Body"]["stkCallback"]
            checkout_request_id = stk_callback["CheckoutRequestID"]
            result_code = stk_callback["ResultCode"]
            result_desc = stk_callback["ResultDesc"]
        except KeyError as e:
            logger.error(
                "Malformed M-Pesa callback received",
                extra={"body": callback_body, "missing_key": str(e)},
            )
            return  # Don't raise — Daraja will retry if we return non-200

        # Extract receipt number from callback metadata (only present on success)
        mpesa_receipt = None
        if result_code == 0:
            try:
                items = stk_callback["CallbackMetadata"]["Item"]
                for item in items:
                    if item["Name"] == "MpesaReceiptNumber":
                        mpesa_receipt = str(item["Value"])
                        break
            except (KeyError, TypeError):
                logger.warning("Could not extract receipt from successful callback")

        logger.info(
            "M-Pesa callback received",
            extra={
                "checkout_request_id": checkout_request_id,
                "result_code": result_code,
                "result_desc": result_desc,
                "receipt": mpesa_receipt,
            },
        )

        await self._repo.handle_mpesa_callback(
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc,
            mpesa_receipt_number=mpesa_receipt,
        )

    async def get_batch_pl(self, batch_id: UUID) -> BatchPLResponse:
        data = await self._repo.get_batch_pl(batch_id)
        return BatchPLResponse(**data)

    async def list_transactions(
        self,
        batch_id: UUID,
        transaction_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        return await self._repo.list_transactions(
            batch_id=batch_id,
            transaction_type=transaction_type,
            limit=limit,
            offset=offset,
        )