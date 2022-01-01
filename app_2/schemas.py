from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

""" PYDANTIC MODELS

    - defining shape of the request & response
    - ensures the body of the request is as expected
"""


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
    created_at: datetime

    class Config:
        # convert sqlalchemy model to pydantic model
        orm_mode = True


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
