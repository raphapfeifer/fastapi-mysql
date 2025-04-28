import re
from pydantic import BaseModel, validator

class UserBase(BaseModel):
    id: int
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str    

    #@validator('username')
    #def validate_username(cls,value):
    #    if not re.match(r'^[a-z0-9@]+$',value):
    #        raise ValueError('Username format invalid')