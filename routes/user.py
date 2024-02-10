from core import db, init_app
from flask import request,jsonify
from core.models import User
from core.utils import JWT
from schemas.user_schemas import UserSchema, UsernameValidator
from pydantic import ValidationError
import json


app = init_app()

@app.route('/')
def index():
    return {'message': 'Fundoo Notes'}

@app.post("/register")
def create_user():
    try:
        serializer = UserSchema(**request.json)
        user=User(**serializer.model_dump())
        db.session.add(user)
        db.session.commit()
        return {"message": "user registered", "status" : 201, "data" : user.json}
    except ValidationError as e:
        err = json.loads(e.json())
        return {'message': f'{err[0]['input']}-{err[0]['msg']}', "status": 400}, 400
    
@app.post("/login")
def login_user():
    data = request.get_json()
    try:
        serializer = UsernameValidator(username=data['username'])
        user=User.query.filter_by(username=data['username']).first()
        if user and user.verify_password(data['password']):
            return {"message":" User logged in successfully", 'token': user.token('login', 60)}, 200
        return {"message" : "Username or Password is incorrect"}, 401
    except ValidationError as e:
        return {'message': 'Invalid username'}, 400

