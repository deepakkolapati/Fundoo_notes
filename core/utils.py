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
    msg.body=f'''
Dear {user},

Welcome to Fundoo_Notes! We're thrilled to have you as part of our community. To get started, please verify your email address by entering the following verification token within the website:

Verification Link: {f'{settings.base_url}/verify?token={token}'}

This verification step ensures the security of your account and helps us keep our community safe. If you didn't create an account with Fundoo_Notes, please ignore this email.

Thank you for choosing Fundoo_Notes! If you have any questions or need assistance, feel free to reach out to our support team at deepakchandu9@gmail.com.

Best regards,
Fundoo_Notes Team'''
    mail.send(msg)