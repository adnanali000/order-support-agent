from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    CREATED = "created"
    PREAPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=100)
    item: str = Field(min_length=1, max_length=200)
    quantity: int = Field(default=1, ge=1, le=20)

class OrderRead(BaseModel):
    id: str
    customer_name: str
    item: str
    quantity: int
    status: OrderStatus
    created_at: datetime
    