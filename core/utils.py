import jwt
from flask_mail import Message
from . import mail
from settings import settings
import redis

class JWT:
    """
    This class provides methods for encoding and decoding JSON Web Tokens (JWTs).

    Attributes:
        key (str): The secret key used for encoding and decoding JWTs.
        algorithm (str): The algorithm used for encoding and decoding JWTs.

    """

    key= 'fundoo_notes'
    algorithm = 'HS256'

    @classmethod
    def to_encode(cls, user_dict):
        """
        Encodes a dictionary of user information into a JWT.

        Args:
            user_dict (dict): A dictionary containing user information.

        Returns:
            str: The encoded JWT.

        """
        encoded = jwt.encode(user_dict,cls.key, algorithm=cls.algorithm)
        return encoded

    @classmethod
    def to_decode(cls, encoded, aud):
        """
        Decodes a JWT and returns the decoded user information.

        Args:
            encoded (str): The encoded JWT.
            aud (str): The expected audience for the JWT.

        Returns:
            dict: The decoded user information.

        """
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
    """
    This class provides methods for interacting with Redis.

    Attributes:
        redis_client (redis.StrictRedis): A Redis client that can be used to interact with Redis.

    Methods:
        save(key: str, field: str, value: str)
            Saves a value in Redis as a hash field.

        get(key: str) -> dict
            Returns all the fields and values of a hash in Redis.

        get_one(key: str, field: str) -> str
            Returns the value of a specific field in a hash in Redis.

        delete(key: str, val: str)
            Deletes a field and its value from a hash in Redis.
    """
    redis_client= redis.StrictRedis(host=settings.host, port=settings.redis_port, db=settings.redis_db)

    @classmethod
    def save(cls,key,field,value):
        """
        Saves a value in Redis as a hash field.

        Args:
            key (str): The key of the hash in Redis.
            field (str): The field of the hash.
            value (str): The value to be saved.
        """
        cls.redis_client.hset(key,field,value)

    @classmethod
    def get(cls,key):
        """
        Returns all the fields and values of a hash in Redis.

        Args:
            key (str): The key of the hash in Redis.

        Returns:
            dict: A dictionary of all the fields and values of the hash.
        """
        return cls.redis_client.hgetall(key)
    
    @classmethod
    def get_one(cls,key,field):
        """
        Returns the value of a specific field in a hash in Redis.

        Args:
            key (str): The key of the hash in Redis.
            field (str): The field of the hash.

        Returns:
            str: The value of the specified field.
        """
        return cls.redis_client.hget(key,field)
    
    @classmethod
    def delete(cls,key,val):
        """
        Deletes a field and its value from a hash in Redis.

        Args:
            key (str): The key of the hash in Redis.
            val (str): The value of the field to be deleted.
        """
        cls.redis_client.hdel(key,val)
