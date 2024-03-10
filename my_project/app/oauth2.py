from jose import JWTError, jwt
from datetime import datetime, timedelta
from my_project.app.routers import user
from my_project.app import schemas
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from my_project.app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# parse the data as a payload
def create_access_token(data : dict):
    # copy the data because it being manipulated and we don't want to change it
    to_encode = data.copy()

    # create the expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # updating the payload with the expiration 
    to_encode.update({"exp":expire})
    #create the jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
	try:
        #decode
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		#extract data
		id = str(payload.get("user_id"))
		if id is None:
			raise credentials_exception
		#validation of token schema
		token_data = schemas.TokenData(id=id)
	except JWTError:
		raise credentials_exception
	return token_data

# The function takes a token automatically, extrats the id and verifies it.
def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"could not validate credentials", headers = {"Mal-Authenticate": "Bearer"})
	#call the verifying function to verify the token by using the logic provided
	return verify_access_token(token, credentials_exception)