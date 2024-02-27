import pytest
from core import init_app, db
from flask_restx import Api
from routes import user
from pathlib import Path
import os


@pytest.fixture
def user_app():
    path = Path(__file__).resolve().parent
    app = init_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(path, 'test.sqlite3')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    api = Api(app)
    api.add_resource(user.UserAPI, '/api/user')
    api.add_resource(user.LoginAPI, '/api/login')
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def user_client(user_app):
    return user_app.test_client()