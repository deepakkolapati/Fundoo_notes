import pytest
from core import init_app,db
from flask_restx import Api
from routes import user,notes,label
from pathlib import Path
import os


@pytest.fixture
def user_app():
   
    app = init_app(mode="testing")
    with app.app_context():
        db.create_all()
    api = Api(app)
    api.add_resource(user.UserAPI, '/api/user')
    api.add_resource(user.LoginAPI, '/api/login')
    api.add_resource(notes.NotesApi, '/api/notes')
    api.add_resource(notes.NoteApi, '/api/notes/<int:id>')
    api.add_resource(notes.ArchiveApi, '/api/archive')
    api.add_resource(notes.TrashApi, '/api/trash')
    api.add_resource(notes.CollaborateApi,'/api/collaborate')
    api.add_resource(label.LabelApi, '/api/labels')
    api.add_resource(label.LabelDeleteApi,'/api/labels/<int:id>')
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def user_client(user_app):
    return user_app.test_client()

@pytest.fixture
def token(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response = user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token = login_response.json['token']
    return token

@pytest.fixture
def collaborate_token(user_client):
    register_data = {
        "username": "Karan",
        "email": "joshikfelix22@gmail.com",
        "password": "Kc5656$ef",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data, headers={"Content-Type": "application/json"})
    register_data_2 = {
        "username": "Chandu",
        "email": "chandufelix22@gmail.com",
        "password": "Abv4&uuuuu",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data_2, headers={"Content-Type": "application/json"})
    register_data_3 = {
        "username": "Deepak",
        "email": "deepakfelix22@gmail.com",
        "password": "K5656$fjjjjj",
        "location": "srm"
    }
    user_client.post('/api/user', json=register_data_3, headers={"Content-Type": "application/json"})
    login_data = {
        "username": "Karan",
        "password": "Kc5656$ef"
    }
    login_response=user_client.post('/api/login', json=login_data, headers={"Content-Type": "application/json"})
    token=login_response.json['token']
    return token