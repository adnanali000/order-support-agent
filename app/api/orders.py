from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.schemas import OrderCreate, OrderRead
from app.orders import service
from app.core.db import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(payload: OrderCreate, session: AsyncSession = Depends(get_db)) -> OrderRead:
    return await service.create_order(session, payload)

@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: str, session: AsyncSession = Depends(get_db)) -> OrderRead:
    return await service.get_order(session, order_id)

@router.post("/{order_id}/cancel", response_model=OrderRead)
async def cancel_order(order_id: str, session: AsyncSession = Depends(get_db)) -> OrderRead:
    return await service.cancel_order(session, order_id)