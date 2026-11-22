from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.orders import router as orders_router
from app.core.config import get_settings
from app.core.db import init_db

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Delivery order support backend. Grows through LLM, RAG, evals, tools, and ops.",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(orders_router)