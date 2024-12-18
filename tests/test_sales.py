from fastapi.testclient import TestClient
from src.modules.data_collector_service import app

client = TestClient(app)

def test_collect_sales():
    sale = {
        "transaction_id": "12345",
        "product_id": "54321",
        "amount": 100.0,
        "timestamp": "2024-12-14T12:00:00Z"
    }
    response = client.post("/sales/", json=sale)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Sale data sent to Kafka"}
