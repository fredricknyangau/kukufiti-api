# app/modules/finance/repository.py
import asyncpg
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import date
from typing import Optional


class FinanceRepository:
    def __init__(self, connection: asyncpg.Connection):
        self._conn = connection

    async def create_pending_transaction(
        self,
        batch_id: UUID,
        transaction_type: str,
        category: str,
        amount_kes: Decimal,
        transaction_date: date,
        notes: Optional[str] = None,
    ) -> dict:
        """Creates a transaction with status='pending' — used for M-Pesa flows
        where we create the record before the customer pays."""
        row = await self._conn.fetchrow(
            """
            INSERT INTO finance.transactions
                (batch_id, transaction_type, category, amount_kes,
                 transaction_date, notes, status)
            VALUES ($1, $2, $3, $4, $5, $6, 'pending')
            RETURNING id, batch_id, transaction_type, category,
                      amount_kes, mpesa_reference, transaction_date, notes, status, created_at
            """,
            batch_id, transaction_type, category,
            amount_kes, transaction_date, notes,
        )
        return dict(row)

    async def create_confirmed_transaction(
        self,
        batch_id: UUID,
        transaction_type: str,
        category: str,
        amount_kes: Decimal,
        transaction_date: date,
        notes: Optional[str] = None,
    ) -> dict:
        """Creates a transaction already confirmed — for manual cash entries."""
        row = await self._conn.fetchrow(
            """
            INSERT INTO finance.transactions
                (batch_id, transaction_type, category, amount_kes,
                 transaction_date, notes, status)
            VALUES ($1, $2, $3, $4, $5, $6, 'confirmed')
            RETURNING id, batch_id, transaction_type, category,
                      amount_kes, mpesa_reference, transaction_date, notes, status, created_at
            """,
            batch_id, transaction_type, category,
            amount_kes, transaction_date, notes,
        )
        return dict(row)

    async def record_mpesa_request(
        self,
        transaction_id: UUID,
        checkout_request_id: str,
        merchant_request_id: str,
        phone_number: str,
        amount_kes: Decimal,
    ) -> dict:
        row = await self._conn.fetchrow(
            """
            INSERT INTO finance.mpesa_requests
                (transaction_id, checkout_request_id, merchant_request_id,
                 phone_number, amount_kes)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, checkout_request_id, status, created_at
            """,
            transaction_id, checkout_request_id,
            merchant_request_id, phone_number, amount_kes,
        )
        return dict(row)

    async def handle_mpesa_callback(
        self,
        checkout_request_id: str,
        result_code: int,
        result_desc: str,
        mpesa_receipt_number: Optional[str] = None,
    ) -> None:
        """
        Called by the callback handler when Daraja POSTs back.

        result_code 0 = success, anything else = failure.
        Updates the mpesa_request record AND the transaction record.
        """
        new_status = "completed" if result_code == 0 else "failed"

        # Update M-Pesa request record
        await self._conn.execute(
            """
            UPDATE finance.mpesa_requests
            SET status               = $2,
                result_code          = $3,
                result_desc          = $4,
                mpesa_receipt_number = $5,
                completed_at         = NOW()
            WHERE checkout_request_id = $1
            """,
            checkout_request_id, new_status,
            result_code, result_desc, mpesa_receipt_number,
        )

        # If payment succeeded, confirm the linked transaction
        if result_code == 0:
            await self._conn.execute(
                """
                UPDATE finance.transactions t
                SET status          = 'confirmed',
                    mpesa_reference = $2
                FROM finance.mpesa_requests mr
                WHERE mr.checkout_request_id = $1
                  AND mr.transaction_id = t.id
                """,
                checkout_request_id, mpesa_receipt_number,
            )
        else:
            # Payment failed — mark transaction as failed
            await self._conn.execute(
                """
                UPDATE finance.transactions t
                SET status = 'failed'
                FROM finance.mpesa_requests mr
                WHERE mr.checkout_request_id = $1
                  AND mr.transaction_id = t.id
                """,
                checkout_request_id,
            )

    async def get_batch_pl(self, batch_id: UUID) -> dict:
        """Profit/loss summary for one batch."""
        row = await self._conn.fetchrow(
            """
            SELECT
                batch_id,
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'income' AND status = 'confirmed'
                ), 0) AS total_income_kes,
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'expense' AND status = 'confirmed'
                ), 0) AS total_expense_kes,
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'income' AND status = 'confirmed'
                ), 0) -
                COALESCE(SUM(amount_kes) FILTER (
                    WHERE transaction_type = 'expense' AND status = 'confirmed'
                ), 0) AS profit_loss_kes,
                COUNT(*) FILTER (WHERE transaction_type = 'income')  AS income_count,
                COUNT(*) FILTER (WHERE transaction_type = 'expense') AS expense_count,
                COUNT(*) FILTER (WHERE status = 'pending')           AS pending_count
            FROM finance.transactions
            WHERE batch_id = $1
            GROUP BY batch_id
            """,
            batch_id,
        )
        if not row:
            return {
                "batch_id": batch_id,
                "total_income_kes": Decimal("0"),
                "total_expense_kes": Decimal("0"),
                "profit_loss_kes": Decimal("0"),
                "income_count": 0,
                "expense_count": 0,
                "pending_count": 0,
            }
        return dict(row)

    async def list_transactions(
        self,
        batch_id: UUID,
        transaction_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        rows = await self._conn.fetch(
            """
            SELECT id, batch_id, transaction_type, category, amount_kes,
                   mpesa_reference, transaction_date, notes, status, created_at
            FROM finance.transactions
            WHERE batch_id = $1
              AND ($2::text IS NULL OR transaction_type = $2)
            ORDER BY transaction_date DESC, created_at DESC
            LIMIT $3 OFFSET $4
            """,
            batch_id, transaction_type, limit, offset,
        )
        return [dict(row) for row in rows]