# app/modules/finance/schemas.py
from pydantic import BaseModel, field_validator, ConfigDict
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class RecordTransactionRequest(BaseModel):
    batch_id: UUID
    category: str
    amount_kes: Decimal
    transaction_date: date
    notes: Optional[str] = None

    @field_validator("amount_kes")
    @classmethod
    def amount_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()


class InitiateMpesaRequest(BaseModel):
    batch_id: UUID
    phone_number: str
    amount_kes: Decimal
    category: str
    description: str = "kukufiti payment"

    @field_validator("phone_number")
    @classmethod
    def valid_kenyan_phone(cls, v: str) -> str:
        cleaned = v.strip().replace(" ", "").replace("-", "")
        # Accept: 07XXXXXXXX, +2547XXXXXXXX, 2547XXXXXXXX
        if cleaned.startswith("+"):
            cleaned = cleaned[1:]
        if cleaned.startswith("0"):
            cleaned = f"254{cleaned[1:]}"
        if not (cleaned.startswith("254") and len(cleaned) == 12):
            raise ValueError(
                "Invalid Kenyan phone number. Use format: 0712345678 or 254712345678"
            )
        return cleaned

    @field_validator("amount_kes")
    @classmethod
    def amount_valid(cls, v: Decimal) -> Decimal:
        if v < 1:
            raise ValueError("Minimum M-Pesa transaction is KES 1")
        if v > 150000:
            raise ValueError("Maximum M-Pesa transaction is KES 150,000")
        return v


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    batch_id: UUID
    transaction_type: str
    category: str
    amount_kes: Decimal
    mpesa_reference: Optional[str]
    transaction_date: date
    notes: Optional[str]
    status: str
    created_at: datetime


class MpesaStkResponse(BaseModel):
    message: str
    checkout_request_id: str
    transaction_id: UUID


class BatchPLResponse(BaseModel):
    batch_id: UUID
    total_income_kes: Decimal
    total_expense_kes: Decimal
    profit_loss_kes: Decimal
    income_count: int
    expense_count: int
    pending_count: int