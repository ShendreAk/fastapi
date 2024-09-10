from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    body: str
    published: bool = True
    ratings: int


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    # id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut
    class Config:
        from_attributes = True

 
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    password: str
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type:str
    
class Token_data(BaseModel):
    id: Optional[int]=None
    
class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)