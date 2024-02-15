import jwt
from flask_mail import Message
from . import mail
from settings import settings
import redis

class JWT:

    key= 'fundoo_notes'
    algorithm = 'HS256'

    @classmethod
    def to_encode(cls, user_dict):
        encoded = jwt.encode(user_dict,cls.key, algorithm=cls.algorithm)
        return encoded

    @classmethod
    def to_decode(cls, encoded, aud):
        decoded= jwt.decode(encoded, cls.key, algorithms=[cls.algorithm], audience=aud)
        return decoded
    

def send_mail(user, email, token):
    msg=Message("Welcome to Fundoo_Notes! Verify Your Email to Get Started",
                sender=f"{settings.sender}",recipients=[email])
    
    with open('message.txt') as file:
        content = file.read()
        content = content.format(user=user, base_url=settings.base_url, token=token, sender=settings.sender)
        msg.body= content
    mail.send(msg)

class RedisManager:
    redis_client= redis.StrictRedis(host=settings.host, port=settings.redis_port, db=settings.redis_db)

    @classmethod
    def save(cls,key,field,value):
        cls.redis_client.hset(key,field,value)

    @classmethod
    def get(cls,key):
        return cls.redis_client.hgetall(key)
    
    @classmethod
    def get_one(cls,key,field):
        return cls.redis_client.hget(key,field)
    
    @classmethod
    def delete(cls,key,val):
        cls.redis_client.hdel(key,val)
