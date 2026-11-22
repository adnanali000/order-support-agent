from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_get_and_cancel_order() -> None:
    create = client.post(
        "/orders",
        json={"customer_name": "Adnan", "item": "Biryani", "quantity": 2},
    )
    assert create.status_code == 201
    body = create.json()
    assert body["status"] == "created"
    order_id = body["id"]

    fetched = client.get(f"/orders/{order_id}")
    assert fetched.status_code == 200
    assert fetched.json()["item"] == "Biryani"

    cancelled = client.post(f"/orders/{order_id}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"

    again = client.post(f"/orders/{order_id}/cancel")
    assert again.status_code == 409