from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class createuser(BaseModel):
    username: str
    email: EmailStr
    role: str
    password: str

class userlogin(BaseModel):
    email: EmailStr
    password: str


class advert(BaseModel):
    title: str
    content: str

# Pydantic model for request body
class PolygonCreate(BaseModel):
    boundary: List[List[float]]  # List of lists of float coordinates


class user_account(BaseModel):
    userid: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    class Config:
        orm_mode = True

# Pydantic model for response body
class CreatedPolygon(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: user_account
    class Config:
        orm_mode: True

class advert_post(advert):
    adid: int
    owner_id: int
    created_at: datetime
    owner: user_account
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None