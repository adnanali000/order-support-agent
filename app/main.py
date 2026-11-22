from fastapi import FastAPI

app = FastAPI(
    title="Order Support Agent",
    version="0.1.0",
    description="Delivery order support backend. Grows through LLM, RAG, evals, tools, and ops.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
