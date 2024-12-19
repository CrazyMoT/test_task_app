import sys
import os
# from fastapi.testclient import TestClient

# Добавляем путь к src в sys.path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src/modules/data_collector_service'))

# from src.modules.data_collector_service.main import app

# client = TestClient(app)
#
# def test_collect_sales():
#     sale = {
#         "transaction_id": "12345",
#         "product_id": "54321",
#         "amount": 100.0,
#         "timestamp": "2024-12-14T12:00:00Z"
#     }
#     response = client.post("/sales/", json=sale)
#     assert response.status_code == 200
#     assert response.json() == {"status": "success", "message": "Sale data sent to Kafka"}

import requests
import datetime

def test_collect_sales():
    sale = {
        "transaction_id": 12345,
        "product_id": 54321,
        'quantity': 1,
        "amount": 100.0,
        "timestamp": "2024-12-14T12:00:00Z"
    }

    url = "http://localhost:5001/sales/send_data"
    response = requests.post(url, json=sale)

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Sale data sent to Kafka"}

if __name__ == '__main__':
    test_collect_sales()