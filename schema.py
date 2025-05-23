from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime





class updated_base_model(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class Users(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    

    class Config:
       from_attributes = True

class Post(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    id:int
    owner:UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes:int

    class Config:
        from_attributes = True

class user_login(BaseModel):
    email:EmailStr
    password:str


# TO VERIFY TOKEN VALIDITY 
class token(BaseModel):
    acess_token:str
    token_type:str

class token_data(BaseModel):
    id:   Optional[int] = None

class vote(BaseModel):
    post_id:int
    dir:bool
    # class Config:
    #     from_attributes = True


