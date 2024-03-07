from fastapi import APIRouter, status, HTTPException, responses, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
import utils
import oauth2

router = APIRouter(tags=['login'])

@router.post("/login")
#instead of passing the user_credentials "user_credentials: schemas.userlogin"
#we are going to use a buil-in utility in the fastapi library
#When you retrieve the user_credential from oAuth2PasswordRequestForm it's going to store it in a field called username
#Not email
# the testing is done in the form data and not raw in postman
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentilas")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    #create token
    access_token = oauth2.create_access_token(data = {"user_id":user.userid})
    #return token
    return {"access_token":access_token, "token_type":"bearer"}