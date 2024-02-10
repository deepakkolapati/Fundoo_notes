import jwt

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
    