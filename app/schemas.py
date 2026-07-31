from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class UsersCreate(BaseModel):
    email: EmailStr
    password: str


class UsersOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class Userlogin(BaseModel):
    id:Optional[int] =None
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[int] =None

class Vote(BaseModel):
    post_id : int
    dir: int

    

