from core import db, init_app
from flask import request,jsonify
from core.models import User
from jwt import PyJWTError
from core.utils import JWT, send_mail
from schemas.user_schemas import UserSchema, UsernameValidator
from pydantic import ValidationError
import json
from flask_restx import Api, Resource, fields
from core.tasks import celery_send_mail
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = init_app()
api = Api(app=app, prefix='/api',doc="/docs", default_label="User", title="Fundoo User", default="Fundoo")
limiter = Limiter(app=app,key_func=get_remote_address, storage_uri="redis://localhost:6379/1")


@app.route('/')
def index():
    return {'message': 'Fundoo Notes'}


@api.route('/user')
class UserAPI(Resource):    
    @api.expect(api.model('register', {'username': fields.String(),'email' : fields.String(), 
    'password': fields.String(),'location' : fields.String()}))
    @limiter.limit('20 per second')
    def post(self):
        """
        Register a new user.

        Returns:
            JSON: User data and authentication token if user is registered successfully,
            error message otherwise.

        Raises:
            ValidationError: If the request body is not a valid JSON or does not
            match the UserSchema.
            IntegrityError: If the username or email already exists in the database.
            Exception: If any other error occurs.
        """
        try:
            serializer = UserSchema(**request.json)
            user=User(**serializer.model_dump())
            db.session.add(user)
            db.session.commit()
            token=user.token('register',60)
            # celery_send_mail(user.username, user.email, token)
            return {"message": "user registered", "status" : 201, "data" : user.json,"token":token}, 201
        except ValidationError as e:
            app.logger.exception(e,exc_info=False)
            err = json.loads(e.json())
            return {'message': f'{err[0]['input']}-{err[0]['msg']}', "status": 400}, 400
        except IntegrityError as e:
            app.logger.exception(e,exc_info=False)
            return {'message': 'Username or email already exists', 'status': 409}, 409
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message':str(e),'status':500},500

    @api.doc(params={"token": "Jwt token to verify user"})
    @limiter.limit('20 per second')
    def get(self):
        """
        Verify user data based on the JWT token in the request.

        Returns:
            JSON: Verified successfully message if token is valid else error message

        Raises:
            PyJWTError: If the token is invalid.
            Exception: If any other error occurs.
        """
        try:
            token=request.args.get('token')
            if not token:
                return {'message': 'Token not found'}, 404
            decoded=JWT.to_decode(token,"register")
            user_id=decoded["user_id"]
            user=User.query.filter_by(id=user_id).first()
            if not user:
                return {'message': 'User not found'}, 404
            user.is_verified=True
            db.session.commit()
            return {"message": "User verified successfully"},200
        except PyJWTError:
            return {'msg': 'Invalid Token','status': 401}, 401
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e)},500
    @api.expect(api.model('delete', {'username': fields.String(), 'password': fields.String()}))
    @limiter.limit('20 per second')
    def delete(self):
        """Deletes a user based on their username and password

        Args:
            username (str): The username of the user to be deleted
            password (str): The password of the user to be deleted

        Returns:
            HTTP status code: 204 if the user was successfully deleted, 401 if the
                username or password is incorrect, or 400 if the username is invalid

        Raises:
            ValidationError: If the username is not a valid string
            Exception: For any other unexpected errors
        """
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
            app.logger.exception(e,exc_info=False)
            return {'message': 'Invalid username'}, 400
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status" :500},500


@api.route('/login')
class LoginAPI(Resource):

    @api.expect(api.model('login', {'username': fields.String(), 'password': fields.String()}))
    @limiter.limit('20 per second')
    def post(self):
        """
        Logs in a user based on their username and password.

        Args:
            username (str): The username of the user to log in
            password (str): The password of the user to log in

        Returns:
            JSON: A JSON object containing a message indicating whether the login was
            successful, and a JWT token if the login was successful. The HTTP status code
            will be 200 if the login was successful, or 401 if the username or password is
            incorrect.

        Raises:
            ValidationError: If the username is not a valid string
            Exception: For any other unexpected errors
        """
        data = request.get_json()
        try:
            serializer = UsernameValidator(username=data['username'])
            user=User.query.filter_by(username=data['username']).first()
            if user and user.verify_password(data['password']):
                return {"message":" User logged in successfully", 'token': user.token('login', 60)}, 200
            return {"message" : "Username or Password is incorrect"}, 401
        except ValidationError as e:
            app.logger.exception(e,exc_info=False)
            return {'message': 'Invalid username'}, 400
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status" :500},500



