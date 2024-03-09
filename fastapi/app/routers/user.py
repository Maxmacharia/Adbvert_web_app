from fastapi import APIRouter, status, HTTPException, Depends
import models
import utils
import schemas
from sqlalchemy.orm import Session
from database import get_db
from geopy.geocoders import Nominatim

router = APIRouter(prefix="/users", tags=['users'])

#endpoint to create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.user_account)
def create_user(user: schemas.createuser, db: Session = Depends(get_db)):
    #use unpack dictionary **user.dict() to avoid lots of texting
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.user_account)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userid == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id {id} does not exist")
    return user