# import requests
import pytest
import json

@pytest.fixture
def client():
    from app import app
    with app.test_client() as client:
        yield client
    
def test_home_page(client):
    response = client.get('/users')
    assert response.status_code == 200
    json.loads(response.text)
