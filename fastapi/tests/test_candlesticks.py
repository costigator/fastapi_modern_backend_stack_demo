import requests

# variables
base_url = "http://localhost:8000"

def test_list_candlesticks():
    response = requests.get(f"{base_url}/candlesticks")
    assert response.status_code == 200

def test_list_candlesticks_with_redis_cache():
    response = requests.get(f"{base_url}/candlesticks/withrediscache")
    assert response.status_code == 200

def test_list_candlesticks_with_rate_limiter():
    response = requests.get(f"{base_url}/candlesticks/withratelimit")
    assert response.status_code == 200

def test_list_candlesticks_with_rate_limiter_too_many_request():
    response = requests.get(f"{base_url}/candlesticks/withratelimit")
    assert response.status_code == 429