from flask import request
from .utils import JWT
from jwt import PyJWTError
from .models import User

def authorize_user(function):
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return {'msg': 'Token not found'}, 404
            payload = JWT.to_decode(token, aud='login')
            user = User.query.get(payload.get('user_id'))
            if not user:
                return {}
            if request.method in ['POST', 'PUT']:
                request.json.update(user_id=user.id)
            else:
                kwargs.update(user_id=user.id)
        except PyJWTError:
            return {'msg': 'Invalid Token'}, 401
        except Exception:
            return {}
        return function(*args, **kwargs)
    wrapper.__name__ == function.__name__
    return wrapper