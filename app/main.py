from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.orders import router as orders_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Delivery order support backend. Grows through LLM, RAG, evals, tools, and ops.",
)

app.include_router(health_router)
app.include_router(orders_router)