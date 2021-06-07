import uuid
import requests
import json

from requests.api import head

# variables
global headers
id = str(uuid.uuid4)
base_url = "http://localhost:8000"

def test_list_users():
    response = requests.get(base_url + "/users")
    assert response.status_code == 200

def test_create_user_with_wrong_format():
    user = {
        "wrongkey": 0
    }
    response = requests.post(f"{base_url}/users", data=user)
    assert response.status_code == 422

def test_create_user_without_token():
    user = {
        "id": id,
        "name": "Test User",
        "email": "test.user@example.com",
        "login": {
            "username": "testuser",
            "password": "testpassword"
        },
        "birthday": "1980-04-21",
        "active": False
    }
    response = requests.post(f"{base_url}/users", json=user)
    assert response.status_code == 401

def test_login_with_wrong_credentials():
    data = {"username": "notexistinguser", "password": "wrongpassword"}
    response = requests.post(f"{base_url}/login/token", data=data)
    assert response.status_code == 401

def test_login_token():
    global headers
    data = {"username": "demo", "password": "demo"}
    response = requests.post(f"{base_url}/login/token", data=data)
    auth_token = response.json()['access_token']
    headers = {"Authorization": f"Bearer {auth_token}"}
    assert response.status_code == 200

def test_create_user():
    global headers
    user = {
        "id": id,
        "name": "Test User",
        "email": "test.user@example.com",
        "login": {
            "username": "testuser",
            "password": "testpassword"
        },
        "birthday": "1980-04-21",
        "active": False
    }
    response = requests.post(f"{base_url}/users", json=user, headers=headers)
    content = json.loads(response.text)
    assert response.status_code == 201
    assert content['login']['password'].startswith("$2b$12$") == True

def test_get_user():
    response = requests.get(f"{base_url}/users/{id}")
    assert response.status_code == 200

def test_get_user_with_wrong_id():
    response = requests.get(f"{base_url}/users/wrongid")
    assert response.status_code == 404

def test_update_user():
    global headers
    user = {
        "name": "Test User Updated",
        "email": "test.user.updated@example.com",
        "login": {
            "username": "testuserupdated",
            "password": "testpasswordupdated"
        },
        "birthday": "1990-04-21",
        "active": True
    }
    response = requests.put(f"{base_url}/users/{id}", json=user, headers=headers)
    content = json.loads(response.text)
    assert response.status_code == 200
    assert content['login']['password'].startswith("$2b$12$") == True

def test_update_user_with_wrong_id():
    global headers
    user = {
        "name": "Test with wrong ID",
    }
    response = requests.put(f"{base_url}/users/wrongid", json=user, headers=headers)
    assert response.status_code == 404

def test_update_user_with_wrong_data():
    global headers
    user = {
        "wrongkey": 0,
    }
    response = requests.put(f"{base_url}/users/{id}", json=user, headers=headers)
    assert response.status_code == 422

def test_delete_user():
    global headers
    response = requests.delete(f"{base_url}/users/{id}", headers=headers)
    assert response.status_code == 204

def test_delete_user_with_id():
    global headers
    response = requests.delete(f"{base_url}/users/wrongid", headers=headers)
    assert response.status_code == 404
