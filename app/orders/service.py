from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.schemas import OrderCreate, OrderRead, OrderStatus
from app.orders.models import Order
from app.orders import repository


def _to_read(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        customer_name=order.customer_name,
        item=order.item,
        quantity=order.quantity,
        status=OrderStatus(order.status),
        created_at=order.created_at,
    )


async def create_order(session: AsyncSession, payload: OrderCreate) -> OrderRead:
    order = Order(
        id=str(uuid4()),
        customer_name=payload.customer_name,
        item=payload.item,
        quantity=payload.quantity,
        status=OrderStatus.CREATED.value,
        created_at=datetime.now(timezone.utc),
    )
    saved = await repository.create(session, order)
    return _to_read(saved)

async def get_order(session: AsyncSession, order_id: str) -> OrderRead:
    order = await repository.get_by_id(session, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return _to_read(order)

async def cancel_order(session: AsyncSession, order_id: str) -> OrderRead:
    order = await repository.get_by_id(session, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.status == OrderStatus.CANCELLED.value:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already cancelled")
    if order.status == OrderStatus.DELIVERED.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delivered orders cannot be cancelled")
    
    order.status = OrderStatus.CANCELLED.value
    saved = await repository.save(session, order)
    return _to_read(saved)