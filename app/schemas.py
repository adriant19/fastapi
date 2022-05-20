from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

""" PYDANTIC MODELS

- defining shape of the request & response
- ensures the body of the request is as expected

"""


# -- User Models ---------------------------------------------------------------

class UserBase(BaseModel):
    email: EmailStr  # to validate email


class UserIn(UserBase):  # input format
    password: str


class UserOut(UserBase):  # response format
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# -- Login Models --------------------------------------------------------------

class UserLogin(BaseModel):  # input format
    email: str
    password: str


# -- Token Models --------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# -- Post Models ---------------------------------------------------------------

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostIn(PostBase):  # input format
    pass


class PostOut(PostBase):  # response format
    # pydantic response
    # to shape the structure of the response
    # handle msg sent to user

    id: int
    user_id: int
    user: UserOut  # take from other schema
    created_at: datetime
    updated_at: datetime

    class Config:
        # convert sqlalchemy model to pydantic model
        orm_mode = True


class PostVote(BaseModel):
    Post: PostOut  # take from other schema
    votes: int

    class Config:
        orm_mode = True


# -- Vote Models ---------------------------------------------------------------

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
