from fastapi import APIRouter, status, HTTPException, Depends,Request
from typing import Optional
from my_project.app import models
from my_project.app import utils
from my_project.app import schemas
from sqlalchemy.orm import Session
from my_project.app.database import get_db
import requests

router = APIRouter(prefix="/users", tags=['users'])

# Third-party IP geolocation API URL and your API key
IP_GEOLOCATION_API_URL = "https://ipinfo.io/"
IP_GEOLOCATION_API_KEY = "614e5bfa102eb7"

# function Get location information from third-party IP geolocation service
def get_user_location(request: Request) -> Optional[str]:
    try:
        # Get IP address from request
        client_ip = request.client
        print(client_ip)
        response = requests.get(f"{IP_GEOLOCATION_API_URL}{client_ip}?token={IP_GEOLOCATION_API_KEY}")
        response.raise_for_status()
        data = response.json()
        user_location = data.get("city") + ", " + data.get("region") + ", " + data.get("country")
    except requests.RequestException as e:
        # Handle network-related errors (e.g., connection issues, timeout)
        user_location = "Unknown (Network Error)"
    except Exception as e:
        # Handle other types of exceptions
        user_location = "Unknown (Error)"
    return user_location

#endpoint to create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.user_account)
def create_user(request: Request, user: schemas.createuser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    # Get user location
    user_location = get_user_location(request)

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