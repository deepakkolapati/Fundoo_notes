from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class UsernameValidator(BaseModel):
    username: str = Field(min_length=3, max_length=6, pattern='^[A-Z]+[a-zA-Z]$')

class UserSchema(UsernameValidator):
    email: str
    password: str
    location: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        password_pattern = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&]).{8,}$'
        #  "password": "A1&12vbfhdj"
        if re.match(password_pattern,value):
             return value
        raise ValueError(f'password must contain one atleast upper case, one number, one special character')
    
