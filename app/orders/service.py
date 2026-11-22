from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException, status
from app.orders.schemas import OrderCreate, OrderRead, OrderStatus

_orders: dict[str, OrderRead] = {}

def create_order(payload: OrderCreate) -> OrderRead:
    order = OrderRead(
        id=str(uuid4()),
        customer_name=payload.customer_name,
        item=payload.item,
        quantity=payload.quantity,
        status=OrderStatus.CREATED,
        created_at=datetime.now(timezone.utc),
    )
    _orders[order.id] = order
    return order

def get_order(order_id: str) -> OrderRead:
    order = _orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

def cancel_order(order_id: str) -> OrderRead:
    order = _orders.get(order_id)
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already cancelled")
    if order.status == OrderStatus.DELIVERED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delivered orders cannot be cancelled")
    
    cancelled = order.model_copy(update={"status": OrderStatus.CANCELLED})
    _orders[order.id] = cancelled
    return cancelled