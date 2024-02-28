import pytest
from core import init_app,db
from flask_restx import Api
from routes import user,notes
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
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def user_client(user_app):
    return user_app.test_client()
