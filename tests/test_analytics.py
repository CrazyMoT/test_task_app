import requests

def test_analytics():
    sale = {
        "product_id": 1,
    }

    url = "http://localhost:5002/sales/daily_sales"
    response = requests.post(url, json=sale)
    print(response.text)
    assert response.status_code == 200

if __name__ == '__main__':
    test_analytics()