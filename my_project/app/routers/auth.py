from fastapi import APIRouter, status, HTTPException, responses, Depends, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from my_project.app.database import get_db
from my_project.app import schemas
from my_project.app import models
from my_project.app import utils
from my_project.app import oauth2
from my_project.app.routers import user

router = APIRouter(tags=['login'])

# login endpoint
@router.post("/login")
def login(request:Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_in = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user_in:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentilas")
    if not utils.verify(user_credentials.password, user_in.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    # Get user location
    user_location = user.get_user_location(request)
    #create token
    access_token = oauth2.create_access_token(data = {"user_id":user_in.userid, "location":user_location})
    #return token
    return {"access_token":access_token, "token_type":"bearer"}