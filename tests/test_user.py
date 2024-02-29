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

def test_register_user_invalid_password_should_return_success_response(user_client):
    register_data = {
        "username":"Karan",
        "email":"joshikfelix22@gmail.com",
        "password":"kc5656$ef",
        "location":"srm"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_register_user_invalid_username_should_return_success_response(user_client):
    register_data = {
        "username":"Kn",
        "email":"joshikfelix22@gmail.com",
        "password":"kc5656$ef",
        "location":"srm"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_reister_duplicate_username_should_return_success_response(user_client):
    register_data = {
        "username":"Karan",
        "email":"joshikfelix22@gmail.com",
        "password":"Kc5656$ef",
        "location":"srm"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 201
    register_data = {
        "username":"Karan",
        "email":"deepakfelix22@gmail.com",
        "password":"Kc656$ef",
        "location":"chennai"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 409

def test_register_user_missing_fields_should_return_success_response(user_client):
    register_data = {
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 400  # Missing username

def test_login_user_should_return_valid_response(user_client):
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

def test_login_user_invalid_password_credentials_should_return_success_response(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})

    invalid_login_data = {
        "username": "Karan",
        "password": "WrongPassword"
    }
    invalid_login_response = user_client.post('/api/login', json=invalid_login_data, headers={"Content-Type": "application/json"})
    assert invalid_login_response.status_code == 401  # Unauthorized

def test_login_user_invalid_user_credentials_should_return_success_response(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})

    invalid_login_data = {
        "username": "Kara",
        "password": "Kc5656$ef"
    }
    invalid_login_response = user_client.post('/api/login', json=invalid_login_data, headers={"Content-Type": "application/json"})
    assert invalid_login_response.status_code == 401  # Unauthorized


def test_verify_user_with_valid_token_should_return_success_response(user_client):
    # Register a user to get a valid token
    register_data = {
        "username": "TestUser",
        "email": "testuser@example.com",
        "password": "SecurePass123!",
        "location": "TestCity"
    }
    register_response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert register_response.status_code == 201

    token = register_response.json['token']  # Extract the token from the registration response

    # Use the token to verify the user
    verify_response = user_client.get(f'/api/user?token={token}')
    assert verify_response.status_code == 200
    assert verify_response.json['message'] == "User verified successfully"

def test_verify_user_with_invalid_token_should_return_success_response(user_client):
    # Register a user to get a valid token
    register_data = {
        "username": "TestUser",
        "email": "testuser@example.com",
        "password": "Secure@Pass123!",
        "location": "TestCity"
    }
    register_response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert register_response.status_code == 201

    token = register_response.json['token'] +'fsdg' # Extract the token from the registration response
    
    # Use the token to verify the user
    verify_response = user_client.get(f'/api/user?token={token}')
    assert verify_response.status_code == 401

def test_delete_user_should_return_success(user_client):
    # Register a user to get a valid token
    register_data = {
        "username": "TestUser",
        "email": "testuser@example.com",
        "password": "Secure@Pass123!",
        "location": "TestCity"
    }
    register_response = user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    assert register_response.status_code == 201

    delete_data={
        "username": "TestUser",
        "password": "Secure@Pass123!"
    }
    delete_response=user_client.delete('/api/user',json=delete_data,headers={"Content-Type": "application/json"})
    assert delete_response.status_code == 204



  