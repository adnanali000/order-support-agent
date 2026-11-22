from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.orders.models import Order

async def create(session: AsyncSession, order: Order) -> Order:
    session.add(order)
    await session.flush()
    await session.refresh(order)
    return order


async def get_by_id(session: AsyncSession, order_id: str) -> Order | None:
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def save(session: AsyncSession, order: Order) -> Order:
    await session.flush()
    await session.refresh(order)
    return order