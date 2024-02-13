import jwt
from flask_mail import Message
from . import mail
from settings import settings

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

