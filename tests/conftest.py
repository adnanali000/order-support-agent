import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    # One app lifespan for the whole test session (avoids Windows asyncpg loop issues).
    with TestClient(app) as test_client:
        yield test_client
