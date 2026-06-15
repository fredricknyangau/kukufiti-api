# app/modules/finance/router.py
from uuid import UUID
from fastapi import APIRouter, Depends, Request, status, Query
from typing import Optional

from .schemas import (
    RecordTransactionRequest, InitiateMpesaRequest,
    TransactionResponse, MpesaStkResponse, BatchPLResponse,
)
from .service import FinanceService
from .dependencies import get_finance_service
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/finance",
    tags=["Finance"],
)


@router.post(
    "/transactions/income",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record cash income for a batch",
)
async def record_income(
    payload: RecordTransactionRequest,
    service: FinanceService = Depends(get_finance_service),
    user: dict = Depends(get_current_user),
):
    tx = await service.record_income(
        batch_id=payload.batch_id,
        category=payload.category,
        amount_kes=payload.amount_kes,
        transaction_date=payload.transaction_date,
        notes=payload.notes,
    )
    return TransactionResponse.model_validate(tx)


@router.post(
    "/transactions/expense",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record an expense for a batch",
)
async def record_expense(
    payload: RecordTransactionRequest,
    service: FinanceService = Depends(get_finance_service),
    user: dict = Depends(get_current_user),
):
    tx = await service.record_expense(
        batch_id=payload.batch_id,
        category=payload.category,
        amount_kes=payload.amount_kes,
        transaction_date=payload.transaction_date,
        notes=payload.notes,
    )
    return TransactionResponse.model_validate(tx)


@router.get(
    "/batches/{batch_id}/pl",
    response_model=BatchPLResponse,
    summary="Get profit/loss summary for a batch",
)
async def get_batch_pl(
    batch_id: UUID,
    service: FinanceService = Depends(get_finance_service),
    user: dict = Depends(get_current_user),
):
    return await service.get_batch_pl(batch_id)


@router.get(
    "/batches/{batch_id}/transactions",
    summary="List transactions for a batch",
)
async def list_transactions(
    batch_id: UUID,
    transaction_type: Optional[str] = Query(None, description="income or expense"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: FinanceService = Depends(get_finance_service),
    user: dict = Depends(get_current_user),
):
    return await service.list_transactions(
        batch_id=batch_id,
        transaction_type=transaction_type,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/mpesa/stk-push",
    response_model=MpesaStkResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Initiate M-Pesa STK push payment",
    description="Sends a PIN prompt to the customer's phone. "
                "Payment confirmed via /mpesa/callback.",
)
async def initiate_mpesa_payment(
    payload: InitiateMpesaRequest,
    service: FinanceService = Depends(get_finance_service),
    user: dict = Depends(get_current_user),
):
    result = await service.initiate_mpesa_payment(
        batch_id=payload.batch_id,
        phone_number=payload.phone_number,
        amount_kes=payload.amount_kes,
        category=payload.category,
        description=payload.description,
    )
    return MpesaStkResponse(
        message=result["message"],
        checkout_request_id=result["checkout_request_id"],
        transaction_id=result["transaction_id"],
    )


@router.post(
    "/mpesa/callback",
    status_code=status.HTTP_200_OK,
    summary="M-Pesa callback — called by Daraja after payment",
    include_in_schema=False,  # Don't show in Swagger — it's for Daraja only
)
async def mpesa_callback(
    request: Request,
    service: FinanceService = Depends(get_finance_service),
):
    """
    Daraja POSTs here after the customer completes or cancels payment.

    CRITICAL RULES:
    1. Must respond with HTTP 200 quickly — Daraja times out in 30 seconds
    2. Must NOT require auth — Daraja doesn't send a token
    3. Must be idempotent — Daraja may call this more than once

    This route has NO auth dependency intentionally.
    """
    body = await request.json()
    await service.process_mpesa_callback(body)
    # Daraja requires this exact response format to consider the callback successful
    return {"ResultCode": 0, "ResultDesc": "Accepted"}