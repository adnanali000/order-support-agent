from fastapi import APIRouter
from app.orders.schemas import OrderCreate, OrderRead
from app.orders import service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=201)
def create_order(payload: OrderCreate) -> OrderRead:
    return service.create_order(payload)

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: str) -> OrderRead:
    return service.get_order(order_id)

@router.post("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(order_id: str) -> OrderRead:
    return service.cancel_order(order_id)