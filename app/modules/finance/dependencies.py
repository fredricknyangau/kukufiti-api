# app/modules/finance/dependencies.py
from fastapi import Depends, Request
import asyncpg

from .repository import FinanceRepository
from .service import FinanceService
from .mpesa_client import MpesaClient


async def get_finance_connection(request: Request):
    async with request.app.state.finance_pool.acquire() as conn:
        yield conn


def get_finance_service(
    conn: asyncpg.Connection = Depends(get_finance_connection),
) -> FinanceService:
    repo = FinanceRepository(connection=conn)
    mpesa = MpesaClient()
    return FinanceService(repository=repo, mpesa_client=mpesa)