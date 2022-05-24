from typing import List, Optional
from pydantic import BaseModel


class MonumentBase(BaseModel):
    name: str
    pincode: int


class Monument(MonumentBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    role: str
    email: str
    password: str


class ShowUser(BaseModel):
    role: str
    email: str
    monument: List[Monument] = []

    class Config():
        orm_mode = True


class ShowMonument(BaseModel):
    name: str
    pincode: int
    creator: ShowUser


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
