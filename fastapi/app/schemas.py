from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Pydantic model for request body
class createuser(BaseModel):
    username: str
    email: EmailStr
    role: str
    password: str

# Pydantic model for request body
class userlogin(BaseModel):
    email: EmailStr
    password: str

# Pydantic model for request body
class advert(BaseModel):
    title: str
    content: str

# Pydantic model for request body
class feedback_post(BaseModel):
    comments: str

# Pydantic model for request body
class PolygonCreate(BaseModel):
    boundary: List[List[float]]  # List of lists of float coordinates

# Pydantic model for response body
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
    boundary: List[List[float]]
    created_at: datetime
    owner_id: int
    owner: user_account
    class Config:
        orm_mode: True

# Pydantic model for response body
class advert_post(advert):
    adid: int
    owner_id: int
    created_at: datetime
    owner: user_account
    polygon_id: int
    polygon: CreatedPolygon
    class Config:
        orm_mode = True

# Pydantic model for response body
class posted_feedback(BaseModel):
    feedback_id: int
    comments: str
    created_at: datetime
    owner_id: int
    post_id: int
    owner: user_account
    post: advert_post

    class Config:
        orm_mode = True

# Pydantic model for response body
class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None