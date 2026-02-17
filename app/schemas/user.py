from pydantic import BaseModel, Field,EmailStr
from typing import Optional
from enum import Enum

class userStatus(Enum):
    active = "active"
    inactive = "inactive"


class user(BaseModel):
    name: str = Field(..., max_length=50, min_length=5)
    email: EmailStr
    password: str = Field(..., max_length=10,min_length=5)
    status: userStatus = userStatus.active

class userResponse(BaseModel):
    name: str
    email: EmailStr

class userUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[userStatus] = None

class Login(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id:int | None = None
    email: EmailStr | None = None