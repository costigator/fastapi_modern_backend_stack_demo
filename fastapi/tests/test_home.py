import requests

# variables
base_url = "http://localhost:8000"

def test_get_home():
    response = requests.get(f"{base_url}")
    assert response.status_code == 200