from core import db, init_app,mail
from flask import request,jsonify
from core.models import User
from core.utils import JWT
from schemas.user_schemas import UserSchema, UsernameValidator
from pydantic import ValidationError
from flask_mail import Message
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
        token=user.token('register',60)
        receivers=[user.email]
        msg=Message("Welcome to Fundoo_Notes! Verify Your Email to Get Started",sender="deepakchandu9@gmail.com",recipients=receivers)
        msg.body=f'''
 Dear {user.username},

Welcome to Fundoo_Notes! We're thrilled to have you as part of our community. To get started, please verify your email address by entering the following verification token within the website:

Verification Token: {token}

This verification step ensures the security of your account and helps us keep our community safe. If you didn't create an account with Fundoo_Notes, please ignore this email.

Thank you for choosing Fundoo_Notes! If you have any questions or need assistance, feel free to reach out to our support team at deepakchandu9@gmail.com.

Best regards,
Fundoo_Notes Team'''
        mail.send(msg)
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


@app.get("/verify")
def verify_user():
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

