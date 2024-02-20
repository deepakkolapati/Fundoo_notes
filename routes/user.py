from core import db, init_app
from flask import request,jsonify
from core.models import User
from core.utils import JWT, send_mail
from schemas.user_schemas import UserSchema, UsernameValidator
from pydantic import ValidationError
import json
from flask_restx import Api, Resource
from core.tasks import celery_send_mail

app = init_app()
api = Api(app=app, prefix='/api')

@app.route('/')
def index():
    return {'message': 'Fundoo Notes'}


@api.route('/user')
class UserAPI(Resource):    

    def post(self):
        try:
            serializer = UserSchema(**request.json)
            user=User(**serializer.model_dump())
            db.session.add(user)
            db.session.commit()
            token=user.token('register',60)
            celery_send_mail(user.username, user.email, token)
            return {"message": "user registered", "status" : 201, "data" : user.json}
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]['input']}-{err[0]['msg']}', "status": 400}, 400
        
    def get(self):
        try:
            token=request.args.get('token')
            if not token:
                return {'message': 'Token not found'}, 400
            decoded=JWT.to_decode(token,"register")
            user_id=decoded["user_id"]
            user=User.query.filter_by(id=user_id).first()
            if not user:
                return {'message': 'User not found'}, 400
            user.is_verified=True
            db.session.commit()
            return {"message": "User verified successfully"},200
        except Exception as e:
            return {"message": "Something went wrong"},400

    def delete(self):
        data = request.get_json()
        try:
            serializer = UsernameValidator(username=data['username'])
            user=User.query.filter_by(username=data['username']).first()
            if user and user.verify_password(data['password']):
                db.session.delete(user)
                db.session.commit()
                return {"message":" User successfully deleted"}, 204
            return {"message" : "Username or Password is incorrect"}, 401
        except ValidationError as e:
            return {'message': 'Invalid username'}, 400


@api.route('/login')
class LoginAPI(Resource):

    def post(self):
        data = request.get_json()
        try:
            serializer = UsernameValidator(username=data['username'])
            user=User.query.filter_by(username=data['username']).first()
            if user and user.verify_password(data['password']):
                return {"message":" User logged in successfully", 'token': user.token('login', 60)}, 200
            return {"message" : "Username or Password is incorrect"}, 401
        except ValidationError as e:
            return {'message': 'Invalid username'}, 400



