from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_root_endpoint():
    response = client.get('/')
    assert response.status_code == 200
    assert 'Shopping Comparison API' in response.json()['name']


def test_search_products():
    response = client.get('/api/v1/products/search?query=shirt&category=daily_wear')
    assert response.status_code == 200
    data = response.json()
    assert 'products' in data
    assert len(data['products']) > 0


def test_filter_products():
    response = client.get('/api/v1/products/filter?category=daily_wear&min_price=500&max_price=2000')
    assert response.status_code == 200
    data = response.json()
    assert 'products' in data


def test_get_platforms():
    response = client.get('/api/v1/platforms')
    assert response.status_code == 200
    data = response.json()
    assert 'platforms' in data
    assert len(data['platforms']) == 5


def test_compare_products():
    response = client.post(
        '/api/v1/compare',
        json={
            'product_ids': ['prod_123', 'prod_456'],
            'platforms': ['amazon', 'flipkart']
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
