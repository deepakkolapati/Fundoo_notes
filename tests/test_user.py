import pytest


def test_register_user_should_return_success_response(user_client):
    register_data = {
        "username":"Karan",
        "email":"joshikfelix22@gmail.com",
        "password":"Kc5656$ef",
        "location":"srm"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 201

def test_login_user_should_return_invalid_response(user_client):
    register_data = {
        "username":"Karan",
        "email":"joshikfelix22@gmail.com",
        "password":"Kc5656$ef",
        "location":"srm"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})

    login_data = {
        "username":"Karan",
        "password":"Kc5656$ef"
    }
    response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200